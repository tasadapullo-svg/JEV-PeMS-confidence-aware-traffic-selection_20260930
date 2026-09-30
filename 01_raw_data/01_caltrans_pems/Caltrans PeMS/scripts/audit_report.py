"""Consolidate completed per-file checkpoints into PeMS audit outputs."""
from __future__ import annotations
import calendar, csv, gzip, hashlib, json, math, statistics
import numpy as np
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
import run_full_pems_audit as a

def read_checkpoint(item):
    key=hashlib.sha256(item['full_path'].encode()).hexdigest()[:16]
    p=a.TEMP/f'{key}.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else None

def hist_quantile(hist,q):
    n=sum(hist.values())
    if not n:return None
    def at(rank):
        c=0
        for v,k in sorted(hist.items()):
            c+=k
            if c>rank:return v
        return max(hist)
    pos=(n-1)*q; lo=math.floor(pos); hi=math.ceil(pos)
    return at(lo)+(at(hi)-at(lo))*(pos-lo)

def varstats(v, scope, period):
    n=v['n']; miss=v['missing']; hist=v['hist']; total=n+miss
    return dict(scope=scope,period=period,field=v['field'],N=total,missing_N=miss,missing_pct=a.pct(miss,total),min=min(hist) if hist else '',P001=hist_quantile(hist,.001),P01=hist_quantile(hist,.01),P05=hist_quantile(hist,.05),P25=hist_quantile(hist,.25),median=hist_quantile(hist,.5),P75=hist_quantile(hist,.75),P95=hist_quantile(hist,.95),P99=hist_quantile(hist,.99),P999=hist_quantile(hist,.999),max=max(hist) if hist else '',mean=v['sum']/n if n else '',std=math.sqrt(max(0,v['sum_sq']/n-(v['sum']/n)**2)) if n else '')

def blank_var(field):return {'field':field,'n':0,'missing':0,'sum':0.,'sum_sq':0.,'hist':Counter()}
def add_var(dst,src):
    for k in ['n','missing','sum','sum_sq']:dst[k]+=src[k]
    dst['hist'].update({float(v):int(n) for v,n in src['hist']})

def meta_inventory():
    files=sorted(a.ROOT.rglob('d07_text_meta_*.txt'))
    records={}; inventory=[]; schemas=[]
    for p in files:
        with p.open(encoding='utf-8-sig',errors='replace',newline='') as f:
            rdr=csv.DictReader(f,delimiter='\t'); cols=rdr.fieldnames or []
            rows=list(rdr)
        counts=Counter(r.get('ID','') for r in rows)
        records[p.name]=rows
        inventory.append(dict(filename=p.name,full_path=str(p),rows=len(rows),unique_stations=len(counts),duplicate_ids=sum(n-1 for n in counts.values() if n>1),ml_stations=sum(r.get('Type')=='ML' for r in rows),columns=';'.join(cols)))
        schemas.append(dict(filename=p.name,columns=';'.join(cols),column_count=len(cols)))
    a.write_csv(a.OUT/'09_METADATA_MATCH'/'metadata_inventory.csv',inventory,['filename','full_path','rows','unique_stations','duplicate_ids','ml_stations','columns'])
    a.write_csv(a.OUT/'09_METADATA_MATCH'/'metadata_schema.csv',schemas,['filename','columns','column_count'])
    return records,inventory

def metadata_outputs(meta,stations,station_info):
    names=list(meta); indexes={name:defaultdict(list) for name in names}
    for name,rows in meta.items():
        for r in rows:indexes[name][r.get('ID','')].append(r)
    all_ids=set().union(*(set(x) for x in indexes.values())) if indexes else set()
    comp=[]; joins=[]; pool=[]
    fields={'fwy_stable':'Fwy','dir_stable':'Dir','lat_stable':'Latitude','lon_stable':'Longitude','length_stable':'Length','lanes_stable':'Lanes','name_stable':'Name'}
    stable_map={}; match_map={}
    for st in sorted(all_ids|set(stations)):
        rs=[indexes[name][st][0] if indexes[name].get(st) else None for name in names]
        present=[r for r in rs if r]
        ml_present=[r for r in present if r.get('Type')=='ML']
        compares={k:(len({r.get(col,'') for r in ml_present})<=1) if ml_present else None for k,col in fields.items()}
        stable=bool(names) and len(ml_present)==len(names) and all(v is True for v in compares.values())
        stable_map[st]=stable
        comp.append(dict(station=st,**{f'present_in_snapshot_{i+1}':bool(rs[i]) if i<len(rs) else False for i in range(3)},**compares,overall_metadata_stable=stable))
        if st not in stations:continue
        matched=sum(bool(indexes[name].get(st)) for name in names)
        multiples=any(len(indexes[name][st])>1 for name in names)
        status='UNMATCHED' if not matched else 'MULTIPLE_MATCH' if multiples else 'METADATA_CHANGED' if not stable else 'MATCHED'
        match_map[st]=status
        joins.append(dict(station=st,matched_snapshots=matched,multiple_match=multiples,metadata_changed=not stable if matched else '',status=status,snapshots=';'.join(name for name in names if indexes[name].get(st))))
        r=next((r for r in reversed(rs) if r and r.get('Type')=='ML'),None)
        info=station_info.get(st,{})
        candidate='METADATA_MISSING' if not r else 'METADATA_UNSTABLE' if not stable else 'TEMPORAL_INCOMPLETE' if info.get('temporal_completeness',0)<100 else 'ELIGIBLE'
        pool.append(dict(station=st,fwy=r.get('Fwy','') if r else '',direction=r.get('Dir','') if r else '',latitude=r.get('Latitude','') if r else '',longitude=r.get('Longitude','') if r else '',length=r.get('Length','') if r else '',lanes=r.get('Lanes','') if r else '',name=r.get('Name','') if r else '',first_seen=info.get('first_seen',''),last_seen=info.get('last_seen',''),days_present=info.get('days_present',0),temporal_completeness=info.get('temporal_completeness',''),mean_observed_pct=info.get('mean_observed_pct',''),median_observed_pct=info.get('median_observed_pct',''),metadata_stable=stable,candidate_status=candidate))
    a.write_csv(a.OUT/'09_METADATA_MATCH'/'metadata_snapshot_comparison.csv',comp,['station','present_in_snapshot_1','present_in_snapshot_2','present_in_snapshot_3',*fields,'overall_metadata_stable'])
    a.write_csv(a.OUT/'09_METADATA_MATCH'/'station_metadata_join_audit.csv',joins)
    a.write_csv(a.OUT/'10_RESEARCH_READINESS'/'ml_candidate_station_pool.csv',pool)
    return stable_map,match_map,comp,joins,pool

def target_quality(items):
    ordered=sorted((x for x in items if x['filename_date']),key=lambda x:x['filename_date'])
    result=[]
    prev=None
    def assess(prev,cur):
        prev_day=date.fromisoformat(prev['date']); cur_day=date.fromisoformat(cur['date']) if cur else None
        adjacent=bool(cur_day and cur_day-prev_day==timedelta(days=1))
        per={6:Counter(),12:Counter()};origins=0
        for st,indices in prev.get('station_intervals',{}).items():
            origin_idx=np.asarray(indices,dtype=np.int32);origins+=len(origin_idx)
            arr=np.asarray(prev.get('target_obs',{}).get(st,[]),dtype=float)
            next_arr=np.asarray(cur.get('target_obs',{}).get(st,[]) if adjacent else [],dtype=float)
            extended=np.concatenate((arr,next_arr,np.full(12,np.nan)))
            for horizon in (6,12):
                target=extended[origin_idx+horizon];valid=~np.isnan(target);v=target[valid];counts=per[horizon]
                counts['target_available']+=int(valid.sum());counts['target_missing']+=int((~valid).sum())
                counts['target_pct_observed_100']+=int(np.count_nonzero(v==100))
                counts['target_pct_observed_ge_90']+=int(np.count_nonzero(v>=90))
                counts['target_pct_observed_ge_80']+=int(np.count_nonzero(v>=80))
                counts['target_pct_observed_below_80']+=int(np.count_nonzero(v<80))
                counts['target_pct_observed_zero']+=int(np.count_nonzero(v==0))
        for horizon in (6,12):
            counts=per[horizon]
            result.append(dict(date=prev['date'],horizon_minutes=horizon*5,origin_rows=origins,matched_targets=counts['target_available'],missing_targets=counts['target_missing'],**{k:counts[k] for k in ['target_pct_observed_100','target_pct_observed_ge_90','target_pct_observed_ge_80','target_pct_observed_below_80','target_pct_observed_zero']},status='YES' if origins and counts['target_available']==origins else 'PARTIAL' if counts['target_available'] else 'NO'))
    for item in ordered:
        cur=read_checkpoint(item)
        if not cur or cur.get('gzip_status')!='PASS':continue
        if prev:assess(prev,cur)
        prev=cur
    if prev:assess(prev,None)
    a.write_csv(a.OUT/'10_RESEARCH_READINESS'/'forecast_target_quality_audit.csv',result,['date','horizon_minutes','origin_rows','matched_targets','missing_targets','target_pct_observed_100','target_pct_observed_ge_90','target_pct_observed_ge_80','target_pct_observed_below_80','target_pct_observed_zero','status'])
    return result

def build():
    a.logging.info('START audit_report.build')
    items=a.read_csv(a.OUT/'01_FILE_INVENTORY'/'raw_file_inventory.csv')
    complete=a.read_csv(a.OUT/'04_DATE_COMPLETENESS'/'date_completeness_by_month.csv')
    bymonth={x['year_month']:x for x in complete}
    varoverall={f:blank_var(f) for f in a.NUMERIC}; varmonths=defaultdict(lambda:{f:blank_var(f) for f in a.NUMERIC})
    stations=defaultdict(lambda:{'dates':set(),'indices':{},'obs_hist':Counter(),'obs_sum':0.,'obs_n':0})
    lane_rows=Counter(); lane_stations=defaultdict(set); district_rows=Counter(); bin_rows=Counter(); bin_stations=defaultdict(set); bin_months=defaultdict(set); bin_days=defaultdict(set); avail=defaultdict(Counter)
    gz=[]; schemas=[]; dailies=[]; temporal=[]; duplicates=[]; anomalies=[]; district_bad=[]; variable_rows=[]; all_stations=set(); ml_stations=set(); failed=[]
    for item in items:
        r=read_checkpoint(item); date_s=item['filename_date']; month=date_s[:7] if date_s else ''
        if not r:
            failed.append(item['filename'])
            gz.append(dict(filename=item['filename'],date=date_s,compressed_size=item['file_size_bytes'],gzip_open_pass=False,gzip_full_stream_pass=False,decompressed_bytes_if_available='',error_message='scan checkpoint missing',status='UNREADABLE'))
            continue
        gz.append(dict(filename=r['filename'],date=date_s,compressed_size=r['compressed_size'],gzip_open_pass=r['gzip_status'] in ('PASS','EMPTY'),gzip_full_stream_pass=r['gzip_status'] in ('PASS','EMPTY'),decompressed_bytes_if_available=r['decompressed_bytes'],error_message=r['gzip_error'],status=r['gzip_status']))
        if r['gzip_status']!='PASS':failed.append(r['filename'])
        colcounts=r['columns']; signature='52|'+'|'.join(a.FIELDS) if list(colcounts)==['52'] or (not colcounts and r['gzip_status']=='PASS') else 'VARIANT:'+','.join(colcounts)
        dtype_errors=0;sample_rows=0
        if r['gzip_status']=='PASS':
            with gzip.open(item['full_path'],'rt',encoding='utf-8',errors='replace',newline='') as sf:
                for row in csv.reader(sf):
                    sample_rows+=1
                    if len(row)==52:
                        for value in row[6:]:
                            if value.strip():
                                try:float(value)
                                except ValueError:dtype_errors+=1
                    if sample_rows>=300:break
        schemas.append(dict(filename=r['filename'],date=date_s,sample_column_counts=json.dumps(colcounts),sample_rows=sample_rows,lane_numeric_type_errors=dtype_errors,schema_signature=signature,parse_errors=r['parse_errors'] if date_s else '',status='INVALID_FILENAME' if not date_s else 'PASS' if signature.startswith('52|') and not r['parse_errors'] and not dtype_errors else 'FAIL'))
        if not date_s:continue
        day=date.fromisoformat(date_s); expected=a.expected_grid(day); present=set(r['timestamps']); unexpected=sorted(present-set(expected)); missing=sorted(set(expected)-present)
        if len(expected)>len(set(expected)):
            observed_positions=set().union(*(set(v) for v in r['station_intervals'].values())) if r['station_intervals'] else set()
            missing_positions=set(range(len(expected)))-observed_positions
            missing=[f'{expected[i]} occurrence {a.expected_grid(day)[:i+1].count(expected[i])}' for i in sorted(missing_positions)]
            observed_timestamp_intervals=len(observed_positions)
        else:observed_timestamp_intervals=len(present)
        dst=len(expected)!=288
        temporal.append(dict(date=date_s,source_file=r['source_file'],min_timestamp=min(present) if present else '',max_timestamp=max(present) if present else '',unique_timestamps=len(present),observed_intervals=observed_timestamp_intervals,expected_intervals=len(expected),missing_intervals=len(missing),unexpected_timestamps=len(unexpected),dst_transition=dst,timezone='America/Los_Angeles',interval='00:05:00',status='PASS' if not missing and not unexpected else 'PARTIAL' if present else 'FAIL'))
        dupkeys=len(r['duplicate_keys']); duprows=sum(x['duplicate_count']-1 for x in r['duplicate_keys'])
        for x in r['duplicate_keys']:duplicates.append(dict(date=date_s,**x))
        for x in r['district_violations']:district_bad.append(dict(date=date_s,filename=r['filename'],**x))
        anomalies.extend(r['anomalies'])
        all_stations.update(r['stations']); ml_stations.update(r['ml_stations'])
        for k,v in r['districts'].items():district_rows[k]+=v
        for lt,n in r['lane_types'].items():lane_rows[lt]+=n;lane_stations[lt].update(r.get('lane_stations',{}).get(lt,[]))
        for b,n in r['bins'].items():bin_rows[b]+=n;bin_stations[b].update(r['bin_stations'].get(b,[]));bin_months[b].add(month);bin_days[b].add(date_s)
        for b,counts in r['avail'].items():avail[b].update(counts)
        for f in a.NUMERIC:
            raw=r['variables'][f]; add_var(varoverall[f],raw);add_var(varmonths[month][f],raw)
            v=blank_var(f);add_var(v,raw);variable_rows.append(varstats(v,'date',date_s))
        for st,idx in r['station_intervals'].items():stations[st]['dates'].add(date_s);stations[st]['indices'][date_s]=sum(1<<i for i in idx)
        for st,ob in r['station_observed'].items():
            stations[st]['obs_n']+=ob['n'];stations[st]['obs_sum']+=ob['sum'];stations[st]['obs_hist'].update({float(v):int(n) for v,n in ob['hist']})
        daily=dict(date=date_s,source_file=r['source_file'],gzip_status=r['gzip_status'],rows=r['rows'],ML_rows=r['ml_rows'],stations=len(r['stations']),ML_stations=len(r['ml_stations']),timestamps=len(present),expected_timestamps_DST_aware=len(expected),min_timestamp=min(present) if present else '',max_timestamp=max(present) if present else '',duplicate_keys=dupkeys,duplicate_rows=duprows,speed_missing_pct=a.pct(r['variables']['avg_speed']['missing'],r['ml_rows']),flow_missing_pct=a.pct(r['variables']['total_flow']['missing'],r['ml_rows']),occupancy_missing_pct=a.pct(r['variables']['avg_occupancy']['missing'],r['ml_rows']),mean_observed_pct=(r['variables']['percent_observed']['sum']/r['variables']['percent_observed']['n'] if r['variables']['percent_observed']['n'] else ''),median_observed_pct=hist_quantile({float(v):int(n) for v,n in r['variables']['percent_observed']['hist']},.5),status='PASS' if r['gzip_status']=='PASS' and not missing and not unexpected and not dupkeys and not r['parse_errors'] else 'PARTIAL' if r['gzip_status']=='PASS' else 'FAIL')
        dailies.append(daily)
    a.write_csv(a.OUT/'02_GZIP_INTEGRITY'/'gzip_integrity_audit.csv',gz)
    a.write_csv(a.OUT/'03_SCHEMA_AUDIT'/'schema_by_file.csv',schemas)
    variants=Counter(s['schema_signature'] for s in schemas)
    (a.OUT/'03_SCHEMA_AUDIT'/'schema_variation_report.md').write_text('# Schema variation\n\n'+ '\n'.join(f'- {k[:100]}: {v} files' for k,v in variants.items())+'\n',encoding='utf-8')
    dictionary=[]
    for i,f in enumerate(a.FIELDS):
        official='core name from supplied field list, checked against observed values' if i<12 else 'inferred lane group from repeated 5-column pattern'
        dictionary.append(dict(column_index=i+1,field_name=f,official_or_inferred_name=official,data_type='local datetime' if i==0 else 'string' if i in (1,4,5) else 'numeric',unit='percent' if 'observed' in f else 'mph' if 'speed' in f else 'fraction' if 'occupancy' in f else 'vehicles/5min' if 'flow' in f else '',required_for_forecasting=f in ('timestamp','station','avg_speed','total_flow','avg_occupancy'),required_for_reliability=f in ('timestamp','station','percent_observed','avg_speed'),notes='Lane 1-8 groups: samples, flow, occupancy, speed, observed flag' if i>=12 else ''))
    a.write_csv(a.OUT/'03_SCHEMA_AUDIT'/'station_5min_field_dictionary.csv',dictionary)
    a.write_csv(a.OUT/'05_TEMPORAL_QC'/'daily_temporal_summary.csv',temporal)
    a.write_csv(a.OUT/'05_TEMPORAL_QC'/'duplicate_station_timestamp.csv',duplicates,['date','station','timestamp','duplicate_count'])
    a.write_csv(a.OUT/'05_TEMPORAL_QC'/'dst_transition_audit.csv',[x for x in temporal if x['dst_transition']],list(temporal[0]) if temporal else [])
    a.write_csv(a.OUT/'06_STATION_QC'/'district_distribution.csv',[dict(district=k,rows=v,percentage=a.pct(v,sum(district_rows.values()))) for k,v in sorted(district_rows.items())],['district','rows','percentage'])
    a.write_csv(a.OUT/'06_STATION_QC'/'non_district_7_records.csv',district_bad,['date','filename','station','district','rows'])
    a.write_csv(a.OUT/'06_STATION_QC'/'lane_type_distribution.csv',[dict(lane_type=k,rows=v,unique_stations=len(lane_stations[k]),percentage=a.pct(v,sum(lane_rows.values()))) for k,v in sorted(lane_rows.items())],['lane_type','rows','unique_stations','percentage'])
    dailies.sort(key=lambda x:x['date']); month_median={m:statistics.median(x['ML_stations'] for x in dailies if x['date'][:7]==m) for m in bymonth}
    prev=None; daily_station=[]
    for x in dailies:
        n=x['ML_stations']; prior=prev['ML_stations'] if prev and date.fromisoformat(x['date'])-date.fromisoformat(prev['date'])==timedelta(days=1) else None
        med=month_median.get(x['date'][:7]);daily_station.append(dict(date=x['date'],all_unique_stations=x['stations'],ml_unique_stations=n,all_rows=x['rows'],ml_rows=x['ML_rows'],relative_change_previous_day=(n-prior)/prior if prior else '',relative_change_monthly_median=(n-med)/med if med else ''))
        prev=x
    a.write_csv(a.OUT/'06_STATION_QC'/'daily_station_counts.csv',daily_station)
    station_changes=sorted((x for x in daily_station if x['relative_change_previous_day']!=''),key=lambda x:abs(x['relative_change_previous_day']),reverse=True)[:20]
    a.write_csv(a.OUT/'06_STATION_QC'/'largest_ml_station_count_changes.csv',station_changes,list(daily_station[0]) if daily_station else [])
    a.write_csv(a.OUT/'07_TRAFFIC_VARIABLE_QC'/'traffic_value_anomaly_inventory.csv',anomalies,['date','timestamp','station','field','value','reason','source_file'])
    anomaly_counts=Counter((x['field'],x['reason']) for x in anomalies)
    a.write_csv(a.OUT/'07_TRAFFIC_VARIABLE_QC'/'traffic_value_anomaly_summary.csv',[dict(field=f,reason=reason,flag_rows=n) for (f,reason),n in sorted(anomaly_counts.items())],['field','reason','flag_rows'])
    for f in a.NUMERIC:variable_rows.append(varstats(varoverall[f],'overall','all'))
    for m,vs in sorted(varmonths.items()):
        for f in a.NUMERIC:variable_rows.append(varstats(vs[f],'month',m))
    a.write_csv(a.OUT/'07_TRAFFIC_VARIABLE_QC'/'traffic_variable_statistics.csv',variable_rows)
    a.write_csv(a.OUT/'08_PERCENT_OBSERVED_QC'/'percent_observed_distribution.csv',[dict(bin=b,rows=bin_rows[b],percentage=a.pct(bin_rows[b],sum(bin_rows.values())),unique_stations=len(bin_stations[b]),months=len(bin_months[b]),days=len(bin_days[b])) for b in ['100','[90,100)','[80,90)','[50,80)','[25,50)','(0,25)','0','MISSING','OUT_OF_RANGE']],['bin','rows','percentage','unique_stations','months','days'])
    a.write_csv(a.OUT/'08_PERCENT_OBSERVED_QC'/'observed_pct_vs_variable_availability.csv',[dict(bin=b,rows=v['rows'],speed_missing_pct=a.pct(v['avg_speed_missing'],v['rows']),flow_missing_pct=a.pct(v['total_flow_missing'],v['rows']),occupancy_missing_pct=a.pct(v['avg_occupancy_missing'],v['rows']),speed_present=v['avg_speed_present'],flow_present=v['total_flow_present'],occupancy_present=v['avg_occupancy_present']) for b,v in sorted(avail.items())],['bin','rows','speed_missing_pct','flow_missing_pct','occupancy_missing_pct','speed_present','flow_present','occupancy_present'])
    profile=[]; temporal_station=[]; station_info={}
    global_dates=sorted(x['date'] for x in dailies)
    if global_dates:
        gd0=date.fromisoformat(global_dates[0]); gd1=date.fromisoformat(global_dates[-1]); lengths={gd0+timedelta(days=i):len(a.expected_grid(gd0+timedelta(days=i))) for i in range((gd1-gd0).days+1)}
    else:lengths={}
    for st,info in sorted(stations.items()):
        days=sorted(info['dates']); first=date.fromisoformat(days[0]);last=date.fromisoformat(days[-1]);span=(last-first).days+1
        expected=sum(lengths[first+timedelta(days=i)] for i in range(span))
        observed=sum(v.bit_count() for v in info['indices'].values())
        # Count gaps in the station's first-to-last calendar span, including absent daily files.
        absolute=[]; offset=0
        for i in range(span):
            ds=(first+timedelta(days=i)).isoformat()
            mask=info['indices'].get(ds,0)
            while mask:
                bit=mask & -mask;absolute.append(offset+bit.bit_length()-1);mask^=bit
            offset+=lengths[first+timedelta(days=i)]
        absolute.sort(); gaps=[absolute[i]-absolute[i-1]-1 for i in range(1,len(absolute)) if absolute[i]-absolute[i-1]>1]
        hist=info['obs_hist']; n=info['obs_n']; median=hist_quantile(hist,.5)
        prof=dict(station=st,N=n,mean=info['obs_sum']/n if n else '',median=median,P10=hist_quantile(hist,.1),P25=hist_quantile(hist,.25),P75=hist_quantile(hist,.75),P90=hist_quantile(hist,.9),pct_eq_100=a.pct(sum(k for v,k in hist.items() if v==100),n),pct_ge_90=a.pct(sum(k for v,k in hist.items() if v>=90),n),pct_below_80=a.pct(sum(k for v,k in hist.items() if v<80),n),pct_below_50=a.pct(sum(k for v,k in hist.items() if v<50),n),pct_eq_0=a.pct(hist.get(0,0),n))
        profile.append(prof)
        completeness=a.pct(observed,expected)
        temporal_station.append(dict(station=st,first_seen=days[0],last_seen=days[-1],days_present=len(days),expected_intervals=expected,observed_intervals=observed,missing_intervals=max(0,expected-observed),completeness_pct=completeness,gap_event_count=len(gaps),longest_gap_minutes=max(gaps,default=0)*5))
        station_info[st]=dict(first_seen=days[0],last_seen=days[-1],days_present=len(days),temporal_completeness=completeness,mean_observed_pct=prof['mean'],median_observed_pct=median)
    a.write_csv(a.OUT/'05_TEMPORAL_QC'/'station_temporal_completeness.csv',temporal_station)
    a.write_csv(a.OUT/'08_PERCENT_OBSERVED_QC'/'station_percent_observed_profile.csv',profile)
    a.write_csv(a.OUT/'11_SUMMARY_TABLES'/'daily_data_summary.csv',dailies)
    months=[]
    for ym,c in sorted(bymonth.items()):
        ds=[x for x in dailies if x['date'].startswith(ym)]
        month_stations=set();month_ml=set()
        for item in items:
            if item['filename_date'].startswith(ym):
                r=read_checkpoint(item)
                if r:month_stations.update(r['stations']);month_ml.update(r['ml_stations'])
        vs=varmonths.get(ym,{});speed=vs.get('avg_speed',blank_var('avg_speed'));flow=vs.get('total_flow',blank_var('total_flow'));occ=vs.get('avg_occupancy',blank_var('avg_occupancy'));obs=vs.get('percent_observed',blank_var('percent_observed'))
        obhist=obs['hist'];month_ml_rows=sum(x['ML_rows'] for x in ds);month_dup=sum(x['duplicate_keys'] for x in ds)
        months.append(dict(month=ym,expected_days=c['expected_days'],downloaded_days=c['actual_unique_days'],gzip_pass_days=sum(x['gzip_status']=='PASS' for x in ds),total_rows=sum(x['rows'] for x in ds),ML_rows=month_ml_rows,unique_stations=len(month_stations),unique_ML_stations=len(month_ml),timestamp_count=sum(x['timestamps'] for x in ds),speed_missing_pct=a.pct(speed['missing'],month_ml_rows),flow_missing_pct=a.pct(flow['missing'],month_ml_rows),occupancy_missing_pct=a.pct(occ['missing'],month_ml_rows),median_percent_observed=hist_quantile(obhist,.5),pct_observed_below_80=a.pct(sum(n for v,n in obhist.items() if v<80),obs['n']),duplicate_station_time_keys=month_dup,status='PASS' if c['status']=='PASS' and all(x['status']=='PASS' for x in ds) else 'PARTIAL' if ds else 'FAIL'))
    a.write_csv(a.OUT/'11_SUMMARY_TABLES'/'monthly_data_summary.csv',months)
    meta,meta_inv=meta_inventory();stable_map,match_map,comp,joins,pool=metadata_outputs(meta,ml_stations,station_info)
    targets=target_quality(items)
    feat=[]
    for f in ['avg_speed','total_flow','avg_occupancy','percent_observed']:
        hist=varoverall[f]['hist'];feat.append(dict(feature=f,distinct_values=len(hist),available_rows=varoverall[f]['n'],variation='HIGH' if len(hist)>100 else 'MEDIUM' if len(hist)>2 else 'LOW' if hist else 'UNRESOLVED',note='Observed distinct values; predictive utility not tested'))
    feat.extend([dict(feature='missingness',distinct_values=2 if any(varoverall[f]['missing'] for f in a.NUMERIC) else 1,available_rows=sum(x['ML_rows'] for x in dailies),variation='MEDIUM' if any(varoverall[f]['missing'] for f in a.NUMERIC) else 'LOW',note='Missing values are retained'),dict(feature='recent_gap',distinct_values=2 if any(x['gap_event_count'] for x in temporal_station) else 1,available_rows=sum(x['ML_rows'] for x in dailies),variation='MEDIUM' if any(x['gap_event_count'] for x in temporal_station) else 'LOW',note='Gap events identified by station'),dict(feature='time_of_day',distinct_values=288,available_rows=sum(x['ML_rows'] for x in dailies),variation='HIGH',note='Local five-minute slot'),dict(feature='day_of_week',distinct_values=len({date.fromisoformat(x['date']).weekday() for x in dailies}),available_rows=sum(x['ML_rows'] for x in dailies),variation='HIGH',note='Calendar'),dict(feature='station',distinct_values=len(ml_stations),available_rows=sum(x['ML_rows'] for x in dailies),variation='HIGH',note='ML station ID'),dict(feature='freeway',distinct_values=len({r.get('Fwy') for rows in meta.values() for r in rows if r.get('Type')=='ML'}),available_rows=sum(x['ML_rows'] for x in dailies),variation='HIGH',note='Metadata'),dict(feature='direction',distinct_values=len({r.get('Dir') for rows in meta.values() for r in rows if r.get('Type')=='ML'}),available_rows=sum(x['ML_rows'] for x in dailies),variation='MEDIUM',note='Metadata')])
    a.write_csv(a.OUT/'10_RESEARCH_READINESS'/'decision_gating_feature_variation.csv',feat)
    expected_days=sum(int(x['expected_days']) for x in complete); actual_days=sum(int(x['actual_unique_days']) for x in complete)
    missing_dates=[s for x in complete for s in x['missing_dates'].split(';') if s]
    duplicate_dates=sum(int(x['duplicate_days_count']) for x in complete)
    pass_gzip=sum(x['status']=='PASS' for x in gz); bad_gzip=sum(x['status'] in ('CORRUPT','EMPTY','UNREADABLE') for x in gz)
    invalid_names=sum(not x['filename_date'] for x in items)
    total_rows=sum(x['rows'] for x in dailies); ml_rows=sum(x['ML_rows'] for x in dailies)
    undated_rows=sum((read_checkpoint(x) or {}).get('rows',0) for x in items if not x['filename_date'])
    undated_ml_rows=sum((read_checkpoint(x) or {}).get('ml_rows',0) for x in items if not x['filename_date'])
    dup_keys=sum(x['duplicate_keys'] for x in dailies);dup_rows=sum(x['duplicate_rows'] for x in dailies)
    stable_matched=sum(p['candidate_status'] in ('ELIGIBLE','TEMPORAL_INCOMPLETE') for p in pool)
    obs=varoverall['percent_observed']; obs_n=obs['n']; obs_hist=obs['hist'];median_obs=hist_quantile(obs_hist,.5)
    low80=sum(n for v,n in obs_hist.items() if v<80);zero=obs_hist.get(0,0)
    availability={f:a.pct(v['n'],ml_rows) for f,v in varoverall.items()}
    temporal_expected=sum(x['expected_intervals'] for x in temporal_station);temporal_observed=sum(x['observed_intervals'] for x in temporal_station)
    mismatch_days=sum(x['status']!='PASS' for x in temporal)
    dst_rows=[x for x in temporal if x['dst_transition']]
    dst_status='PASS' if all(x['status']=='PASS' for x in dst_rows) and dst_rows else 'PARTIAL' if dst_rows else 'UNRESOLVED'
    meta_status='PASS' if joins and all(x['status']=='MATCHED' for x in joins) else 'PARTIAL' if any(x['status']=='MATCHED' for x in joins) else 'FAIL'
    dated_schemas=[x for x in schemas if x['date']]
    schema_status='PASS' if dated_schemas and all(x['status']=='PASS' for x in dated_schemas) else 'PARTIAL' if any(x['status']=='PASS' for x in dated_schemas) else 'FAIL'
    def tri(yes,partial):return 'PASS' if yes else 'PARTIAL' if partial else 'FAIL'
    target_matched=sum(x['matched_targets'] for x in targets);target_origins=sum(x['origin_rows'] for x in targets)
    target_zeros=sum(x['target_pct_observed_zero'] for x in targets)
    summary={
        'raw_download_complete':tri(actual_days==expected_days and not duplicate_dates and not invalid_names,actual_days>0),
        'gzip_integrity':tri(pass_gzip==len(items) and len(items)>0,pass_gzip>0),
        'schema_consistency':schema_status,
        'temporal_completeness':tri(mismatch_days==0 and actual_days==expected_days and temporal_observed==temporal_expected,mismatch_days<len(temporal) and temporal_observed>0),
        'station_stability':tri(bool(comp) and all(x['overall_metadata_stable'] for x in comp if x['station'] in ml_stations),stable_matched>0),
        'metadata_match':meta_status,
        'speed_usability':tri(availability['avg_speed']==100 and low80==0 and not any(x['field']=='avg_speed' for x in anomalies),availability['avg_speed']>0),
        'flow_usability':tri(availability['total_flow']==100 and not any(x['field']=='total_flow' for x in anomalies),availability['total_flow']>0),
        'occupancy_usability':tri(availability['avg_occupancy']==100 and not any(x['field']=='avg_occupancy' for x in anomalies),availability['avg_occupancy']>0),
        'percent_observed_usability':tri(availability['percent_observed']==100 and low80==0,availability['percent_observed']>0),
        'forecast_target_usability':tri(target_origins>0 and target_matched==target_origins and target_zeros==0,target_matched>0),
        'traffic_forecasting_readiness':'YES' if actual_days==expected_days and mismatch_days==0 and availability['avg_speed']==100 and stable_matched==len(ml_stations) and target_matched==target_origins and target_zeros==0 else 'PARTIAL' if target_matched>0 and stable_matched>0 else 'NO',
        'decision_gating_data_readiness':'YES' if actual_days==expected_days and availability['percent_observed']==100 and low80>0 and target_matched==target_origins and target_zeros==0 else 'PARTIAL' if target_matched>0 and obs_n>0 else 'NO',
    }
    issues=[]
    if missing_dates:issues.append(f'{len(missing_dates)} calendar dates lack a file')
    if bad_gzip:issues.append(f'{bad_gzip} gzip files corrupt, empty or unreadable')
    if invalid_names:issues.append(f'{invalid_names} invalid filenames')
    if any(x['status']!='PASS' for x in dated_schemas):issues.append('Schema or parse variants detected in dated files')
    if mismatch_days:issues.append(f'{mismatch_days} available days have incomplete or unexpected timestamp grids')
    if dup_keys:issues.append(f'{dup_keys} duplicate ML station-time keys')
    if district_bad:issues.append(f'{len(district_bad)} non-District-7 station/date combinations')
    if any(x['status']!='MATCHED' for x in joins):issues.append(f'{sum(x["status"]!="MATCHED" for x in joins)} ML stations lack a stable one-to-one metadata match')
    if low80:issues.append(f'{low80} ML rows have % Observed below 80; nonmissing speed is not assured detector ground truth')
    if target_zeros:issues.append(f'{target_zeros} matched future targets have zero % Observed across 30/60-minute horizons')
    if failed:issues.append(f'{len(failed)} files lacked a completed successful scan')
    summary.update(critical_issues=issues,recommended_next_step='Review missing/corrupt files and low-observation target policy; then approve a chronological split and station selection without altering RAW.',metrics=dict(files=len(items),expected_days=expected_days,actual_days=actual_days,missing_dates=missing_dates,duplicate_dates=duplicate_dates,gzip_pass=pass_gzip,gzip_fail=bad_gzip,invalid_filenames=invalid_names,total_readable_raw_rows=total_rows+undated_rows,dated_raw_rows=total_rows,undated_raw_rows=undated_rows,dated_ml_rows=ml_rows,undated_ml_rows=undated_ml_rows,unique_stations=len(all_stations),unique_ml_stations=len(ml_stations),stable_metadata_matched_ml_stations=stable_matched,station_temporal_completeness_pct=a.pct(temporal_observed,temporal_expected),dst_status=dst_status,median_percent_observed=median_obs,percent_observed_below_80_pct=a.pct(low80,obs_n),percent_observed_zero_pct=a.pct(zero,obs_n),duplicate_station_time_keys=dup_keys,duplicate_station_time_rows=dup_rows,availability_pct=availability,target_origin_rows=target_origins,target_matched_rows=target_matched,failed_files=failed))
    (a.OUT/'research_readiness.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    readiness=[dict(dimension=k,status=v) for k,v in summary.items() if k not in ('critical_issues','recommended_next_step','metrics')]
    a.write_csv(a.OUT/'10_RESEARCH_READINESS'/'readiness_assessment.csv',readiness)
    end_date=dailies[-1]['date'] if dailies else '';first_date=dailies[0]['date'] if dailies else ''
    split='Unresolved: calendar gaps require review.'
    if len(months)>=3:split=f"Suggested only: train {months[0]['month']}–{months[-3]['month']}; validation {months[-2]['month']}; test {months[-1]['month']}. Keep chronological order; do not freeze until gaps and target policy are reviewed."
    speed_flag_keys={(x['date'],x['timestamp'],x['station']) for x in anomalies if x['field']=='avg_speed'}
    speed_missing=varoverall['avg_speed']['missing'];speed_flagged=len(speed_flag_keys);speed_valid=max(0,ml_rows-speed_missing-speed_flagged)
    # Counts for the specified 5-minute station-time grid; extra duplicates are reported separately.
    file_closure=dict(total_files=len(items),valid_name_gzip_pass=sum(bool(x['filename_date']) and g['status']=='PASS' for x,g in zip(items,gz)),valid_name_gzip_fail=sum(bool(x['filename_date']) and g['status']!='PASS' for x,g in zip(items,gz)),invalid_filename=invalid_names)
    a.write_csv(a.OUT/'11_SUMMARY_TABLES'/'quantity_reconciliation.csv',[dict(check='files',total=file_closure['total_files'],part_1=file_closure['valid_name_gzip_pass'],part_2=file_closure['valid_name_gzip_fail'],part_3=file_closure['invalid_filename'],difference=file_closure['total_files']-sum(v for k,v in file_closure.items() if k!='total_files')),dict(check='calendar_days',total=expected_days,part_1=actual_days,part_2=len(missing_dates),part_3=0,difference=expected_days-actual_days-len(missing_dates)),dict(check='ML_speed_rows',total=ml_rows,part_1=speed_valid,part_2=speed_missing,part_3=speed_flagged,difference=ml_rows-speed_valid-speed_missing-speed_flagged)],['check','total','part_1','part_2','part_3','difference'])
    report=f'''# PeMS Data Integrity and Research Readiness Report

## 1. Executive Summary

District 7 data: {len(items):,} compressed files, {actual_days}/{expected_days} calendar days, {total_rows+undated_rows:,} readable raw rows including {undated_rows:,} in invalid-name files, {ml_rows:,} dated ML rows. Forecasting readiness: **{summary['traffic_forecasting_readiness']}**. Decision-gating data readiness: **{summary['decision_gating_data_readiness']}**.

## 2. Data Scope

Source: `{a.RAW}`. Detected dates: {first_date} to {end_date}; {len(months)} months. Times are PeMS local time in America/Los_Angeles. No raw file was modified. All results are derived audit artifacts.

## 3. Raw File Inventory

Inventory and SHA256 manifest are in `01_FILE_INVENTORY`. File closure: {file_closure['total_files']} = {file_closure['valid_name_gzip_pass']} valid-name gzip PASS + {file_closure['valid_name_gzip_fail']} valid-name gzip fail + {file_closure['invalid_filename']} invalid filename.

## 4. Download Completeness

Expected {expected_days} days, available {actual_days}, missing {len(missing_dates)}. Missing dates: {', '.join(missing_dates) or 'none'}. Duplicate date surplus: {duplicate_dates}. Calendar closure: {expected_days} = {actual_days} + {len(missing_dates)}.

## 5. GZIP Integrity

PASS {pass_gzip}; failed/empty/unreadable {bad_gzip}. Every tested gzip stream was read through EOF. Failed files: {', '.join(failed) or 'none'}.

## 6. Schema Consistency

{schema_status}. Observed schema signatures: {len(variants)}. The 52 fields are 12 station fields plus eight five-field lane groups. Core names follow the supplied field list and observed values; lane group names are inferred from the repeated layout. The official PeMS field specification was not independently retrieved, so the lane-level naming remains provisional. See the field dictionary and variation report.

## 7. Temporal Completeness

Station grid completeness over each station's first-to-last observed date: {a.pct(temporal_observed,temporal_expected)}%. {mismatch_days} available days have missing or unexpected timestamps. This grid metric does not measure direct detector observation.

## 8. DST Handling

Timezone: America/Los_Angeles. DST transition records: {len(dst_rows)}. {', '.join(f"{x['date']} expected {x['expected_intervals']} observed {x['unique_timestamps']} ({x['status']})" for x in dst_rows) or 'none'}. Expected grids derive from the timezone, including a 276-interval spring day and a 300-interval fall day when those dates are within the scan.

## 9. Station Coverage

Unique stations: {len(all_stations)}. Daily ML station median/min/max: {statistics.median(x['ML_stations'] for x in dailies) if dailies else 'NA'}/{min((x['ML_stations'] for x in dailies),default='NA')}/{max((x['ML_stations'] for x in dailies),default='NA')}. Largest absolute previous-day relative changes: {', '.join(f"{x['date']} {x['relative_change_previous_day']:+.2%}" for x in station_changes[:5]) or 'none'}. The full ranked list and monthly-median comparisons are tabulated without an arbitrary alert threshold.

## 10. Mainline Station Coverage

ML rows: {ml_rows:,}; unique ML stations: {len(ml_stations):,}; ML share of all rows: {a.pct(ml_rows,total_rows)}%. Duplicate ML station-time keys: {dup_keys:,}; surplus rows: {dup_rows:,}. No duplicate was removed.

## 11. Traffic Variable Quality

Available among ML rows: speed {availability['avg_speed']}%, flow {availability['total_flow']}%, occupancy {availability['avg_occupancy']}%, samples {availability['samples']}%. Full distribution statistics and flagged values are in `07_TRAFFIC_VARIABLE_QC`. Flags are retained, including extreme values.

## 12. % Observed Analysis

Availability {availability['percent_observed']}%; median {median_obs}; below 80: {low80:,} ({a.pct(low80,obs_n)}% of nonmissing); zero: {zero:,} ({a.pct(zero,obs_n)}%). At zero % Observed, present speed/flow/occupancy counts: {avail['0']['avg_speed_present']:,}/{avail['0']['total_flow_present']:,}/{avail['0']['avg_occupancy_present']:,}. Nonmissing values at zero observation are not treated as verified ground truth.

## 13. Metadata Stability

Metadata snapshots: {', '.join(meta) or 'none'}. Stable metadata-matched ML stations: {stable_matched:,} of {len(ml_stations):,}. Match status: {meta_status}. The candidate pool is provisional; no 200-station set is frozen. Low % Observed alone does not exclude a station.

## 14. Forecast Target Quality

30/60-minute origin rows assessed: {target_origins:,}; matched future targets: {target_matched:,}; target % Observed zero: {target_zeros:,}. Target values use actual future station-time alignment; absent targets remain missing. Threshold choice is deferred.

## 15. Forecasting Readiness

**{summary['traffic_forecasting_readiness']}**. Speed, flow, occupancy and station identity exist, but calendar gaps, timestamp/station gaps and future target observation quality must be accounted for. {split}

## 16. Decision-Gating Readiness

**{summary['decision_gating_data_readiness']}**. Feature variation is documented in `10_RESEARCH_READINESS`. This is signal potential only; no model or Jev was run.

## 17. Critical Risks

{chr(10).join('- '+x for x in issues) or '- None detected'}

## 18. Recommended Next Step

{summary['recommended_next_step']}

### Quantity and interpretation notes

FILE COMPLETE means daily archives exist. TEMPORAL COMPLETE means station-time positions exist. OBSERVATION COMPLETE requires direct detector observations; % Observed shows this separately. The speed-row closure is {ml_rows:,} = {speed_valid:,} present/unflagged + {speed_missing:,} missing + {speed_flagged:,} flagged present rows. Flagged speed rows are unique station-time keys; duplicate-key surplus is counted separately. Percentages are based on the stated denominator, and all QC is read-only.
'''
    (a.OUT/'PeMS_Data_Integrity_and_Research_Readiness_Report.md').write_text(report,encoding='utf-8')
    final=f'''============================================================
CALTRANS PEMS DATA INTEGRITY AUDIT — FINAL
============================================================
Root: {a.ROOT}
Raw data directory: {a.RAW}
Detected date range: {first_date} to {end_date}
Detected months: {', '.join(x['month'] for x in months)}
Expected daily files: {expected_days}
Actual daily files: {actual_days}
Missing dates: {len(missing_dates)} ({', '.join(missing_dates) or 'none'})
Duplicate dates: {duplicate_dates}
GZIP PASS: {pass_gzip}
GZIP FAIL: {bad_gzip}
Schema: {schema_status}
Total raw rows: {total_rows+undated_rows} ({undated_rows} from invalid-name files, excluded from date-based QC)
Total ML rows: {ml_rows} dated (+ {undated_ml_rows} in invalid-name files)
Unique stations: {len(all_stations)}
Unique ML stations: {len(ml_stations)}
Stable metadata-matched ML stations: {stable_matched}
Temporal completeness: {a.pct(temporal_observed,temporal_expected)}%
DST audit: {dst_status}
Speed availability: {availability['avg_speed']}%
Flow availability: {availability['total_flow']}%
Occupancy availability: {availability['avg_occupancy']}%
% Observed availability: {availability['percent_observed']}%
Median % Observed: {median_obs}
% Observed <80: {a.pct(low80,obs_n)}%
% Observed =0: {a.pct(zero,obs_n)}%
Duplicate station-time keys: {dup_keys}
Traffic variable QC: {tri(not anomalies and all(availability[f]==100 for f in ['avg_speed','total_flow','avg_occupancy']),ml_rows>0)}
Metadata match: {meta_status}
30-min target readiness: {tri(all(x['status']=='YES' for x in targets if x['horizon_minutes']==30),any(x['matched_targets'] for x in targets if x['horizon_minutes']==30)).replace('PASS','YES').replace('FAIL','NO')}
60-min target readiness: {tri(all(x['status']=='YES' for x in targets if x['horizon_minutes']==60),any(x['matched_targets'] for x in targets if x['horizon_minutes']==60)).replace('PASS','YES').replace('FAIL','NO')}
TRAFFIC_FORECASTING_READINESS: {summary['traffic_forecasting_readiness']}
DECISION_GATING_DATA_READINESS: {summary['decision_gating_data_readiness']}
Critical issues: {'; '.join(issues) or 'none'}
Main methodological risks: low % Observed may mean estimated speed; missing calendar days and target grid gaps
Recommended next step: {summary['recommended_next_step']}
Main report: {a.OUT/'PeMS_Data_Integrity_and_Research_Readiness_Report.md'}
Excel audit: {a.OUT/'PeMS_Data_Integrity_Audit_2026.xlsx'}
============================================================'''
    (a.OUT/'11_SUMMARY_TABLES'/'final_terminal_summary.txt').write_text(final,encoding='utf-8')
    a.logging.info('END audit_report.build files=%s dated_rows=%s ml_rows=%s',len(items),total_rows,ml_rows)
    print(final)
