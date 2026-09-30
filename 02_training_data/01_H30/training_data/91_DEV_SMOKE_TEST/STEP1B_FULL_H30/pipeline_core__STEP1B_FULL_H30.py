"""Resumable CPU-only Step 1B H30 benchmark. Formal mode never runs during development."""
from __future__ import annotations

import csv
import gc
import hashlib
import json
import logging
import math
import os
import pickle
import platform
import statistics
import threading
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import psutil
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq
import torch
import xgboost as xgb
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from workbook import build as build_workbook

TRAINING_ROOT = Path(__file__).resolve().parents[2]
PEMS = TRAINING_ROOT.parent/'Caltrans PeMS'
FREEZE = PEMS/'02_FORECASTING_DATASET_FREEZE'/'01_H30'
OVERLAP = PEMS/'03_FORECASTING_BENCHMARK'/'00_PREFLIGHT'/'station_overlap.json'
BASE = TRAINING_ROOT/'01_STEP1B_FULL_H30'
SPLITS = {'train':'2026-01-01 to 2026-05-31','validation':'2026-06-01 to 2026-06-30','test':'2026-07-01 to 2026-08-31'}
LAGS=[f'{v}_lag{i:02d}' for v in ('speed','flow','occupancy','observed_pct','samples') for i in range(12)]
SUMMARIES=['observed_pct_mean_60m','observed_pct_min_60m','observed_pct_zero_count_60m',
           'speed_mean_60m','speed_std_60m','speed_min_60m','speed_max_60m',
           'flow_mean_60m','flow_std_60m','occupancy_mean_60m','occupancy_std_60m']
CONTEXT=['time_of_day_sin','time_of_day_cos','day_of_week_sin','day_of_week_cos',
         'is_weekend','lanes','station_length','latitude','longitude']
NUMERIC=LAGS+SUMMARIES+CONTEXT
SEQ_VARS=('speed','flow','occupancy','observed_pct','samples')
KEY=['sample_id','station_id','prediction_timestamp_local','prediction_timestamp_utc','freeway','direction',
     'input_observed_pct','input_quality_bin','target_speed','target_observed_pct','speed_lag00',
     'day_of_week','hour','minute','is_weekend']
PRED_COLS=list(dict.fromkeys(KEY+NUMERIC))
MODEL_NAMES=('Persistence','HistoricalAverage','XGBoost','GRU')
DIRS=('00_CONFIG','01_EVALUATION_SCOPE','02_PERSISTENCE','03_HISTORICAL_AVERAGE','04_XGBOOST','05_GRU',
      '06_PREDICTIONS','07_METRICS','08_SUBGROUP_ANALYSIS','09_PAIRED_COMPARISON','10_LATENCY',
      '11_RESOURCE_PROFILE','12_QC','13_RESULTS_XLSX','14_LOGS','15_MANIFEST','99_SMOKE_TEST')
STAGES=('environment','scope','ha','xgb','gru','lock','predictions','metrics','subgroups','paired','latency','qc','xlsx','manifest')

def write_csv(path,rows,fields=None):
    rows=list(rows)
    fields=fields or (list(rows[0]) if rows else [])
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)

def read_csv(path):
    with path.open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))

def json_write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,default=float),encoding='utf-8')

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()

def metrics(y,pred):
    y=np.asarray(y,dtype=np.float64);pred=np.asarray(pred,dtype=np.float64)
    if len(y)==0:return dict(N=0,MAE=None,RMSE=None,Bias=None,P50_AE=None,P75_AE=None,P90_AE=None,P95_AE=None,P99_AE=None)
    if not np.isfinite(pred).all():raise RuntimeError('Nonfinite prediction')
    error=pred-y;ae=np.abs(error)
    return dict(N=len(y),MAE=float(ae.mean()),RMSE=float(np.sqrt(np.mean(error**2))),Bias=float(error.mean()),
                **{f'P{q}_AE':float(np.percentile(ae,q)) for q in (50,75,90,95,99)})

def onehot(frame,categories):
    blocks=[]
    for name in ('freeway','direction'):
        values=frame[name].astype(str).to_numpy()
        known=set(categories[name])
        columns=[(values==category).astype(np.float32) for category in categories[name]]
        columns.append(np.array([v not in known for v in values],dtype=np.float32))
        blocks.append(np.stack(columns,axis=1))
    return np.concatenate(blocks,axis=1)

def xgb_matrix(frame,categories):
    return np.concatenate((frame[NUMERIC].to_numpy(dtype=np.float32),onehot(frame,categories)),axis=1)

def sequence(frame):
    return np.stack([frame[[f'{v}_lag{i:02d}' for i in range(12)]].to_numpy(dtype=np.float32)[:,::-1]
                     for v in SEQ_VARS],axis=2).copy()

def context(frame,categories):
    return np.concatenate((frame[CONTEXT].to_numpy(dtype=np.float32),onehot(frame,categories)),axis=1)

class GRUModel(nn.Module):
    def __init__(self,context_size):
        super().__init__()
        self.gru=nn.GRU(5,64,num_layers=1,dropout=0,batch_first=True)
        self.head=nn.Sequential(nn.Linear(64+context_size,64),nn.ReLU(),nn.Linear(64,1))
    def forward(self,seq,ctx):
        _,hidden=self.gru(seq)
        return self.head(torch.cat((hidden[-1],ctx),dim=1)).squeeze(1)

class PeakRAM:
    def __init__(self):
        self.process=psutil.Process();self.peak=self.process.memory_info().rss
        self.stop_event=threading.Event();self.thread=threading.Thread(target=self._sample,daemon=True)
    def _sample(self):
        while not self.stop_event.wait(0.2):self.peak=max(self.peak,self.process.memory_info().rss)
    def start(self):self.thread.start()
    def finish(self):
        self.stop_event.set();self.thread.join()
        self.peak=max(self.peak,self.process.memory_info().rss)
        return self.peak/1e9

class Pipeline:
    def __init__(self,smoke=False):
        self.smoke=smoke
        self.dir=BASE/'99_SMOKE_TEST' if smoke else BASE
        self.dir.mkdir(parents=True,exist_ok=True)
        for name in DIRS:
            if name!='99_SMOKE_TEST':(self.dir/name).mkdir(parents=True,exist_ok=True)
        self.state_path=self.dir/'00_CONFIG/run_state.json'
        self.state=json.loads(self.state_path.read_text(encoding='utf-8')) if self.state_path.exists() else {'mode':'SMOKE' if smoke else 'FORMAL','stages':{s:'PENDING' for s in STAGES}}
        if self.state['mode']!=('SMOKE' if smoke else 'FORMAL'):raise RuntimeError('Run-state mode mismatch')
        logging.basicConfig(filename=self.dir/'14_LOGS/step1b_full_h30.log',level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',encoding='utf-8',force=True)
        self.run_id=self.state.get('run_id') or datetime.now().strftime('%Y%m%dT%H%M%S')+('_SMOKE' if smoke else '_FORMAL')
        self.state['run_id']=self.run_id
        json_write(self.state_path,self.state)
        overlap=json.loads(OVERLAP.read_text(encoding='utf-8'))
        self.seen=set(map(int,overlap['train_station_ids']))
        self.overlap=overlap
        torch.set_num_threads(12)

    def path(self,relative):return self.dir/relative

    def source(self,kind,columns):
        if self.smoke:
            day={'train':'2026-05-23','validation':'2026-05-24','test':'2026-05-25'}[kind]
            origin=ds.dataset(FREEZE/'train.parquet',format='parquet')
            lo=pd.Timestamp(day,tz='America/Los_Angeles').tz_convert('UTC').to_pydatetime()
            hi=(pd.Timestamp(day,tz='America/Los_Angeles')+pd.Timedelta(days=1)).tz_convert('UTC').to_pydatetime()
            mask=(ds.field('prediction_timestamp_utc')>=lo)&(ds.field('prediction_timestamp_utc')<hi)
        else:
            origin=ds.dataset(FREEZE/f'{kind}.parquet',format='parquet')
            mask=None
        return origin.to_table(columns=list(dict.fromkeys(columns)),filter=mask).to_pandas()

    def primary_validation(self,columns):
        data=self.source('validation',list(dict.fromkeys(columns+['station_id'])))
        return data[data['station_id'].isin(self.seen)].reset_index(drop=True)

    def run_stage(self,name,fn,required):
        if self.state['stages'][name]=='DONE' and all(self.path(x).exists() for x in required):
            logging.info('SKIP stage=%s status=DONE',name);return
        start=time.perf_counter();self.state['stages'][name]='RUNNING';json_write(self.state_path,self.state)
        logging.info('START stage=%s rss_gb=%.3f',name,psutil.Process().memory_info().rss/1e9)
        try:
            fn()
            if not all(self.path(x).exists() for x in required):raise RuntimeError(f'Missing outputs for {name}')
            self.state['stages'][name]='DONE';json_write(self.state_path,self.state)
            logging.info('DONE stage=%s elapsed_sec=%.3f rss_gb=%.3f',name,time.perf_counter()-start,
                         psutil.Process().memory_info().rss/1e9)
        except Exception:
            self.state['stages'][name]='FAILED';json_write(self.state_path,self.state)
            logging.exception('FAILED stage=%s elapsed_sec=%.3f',name,time.perf_counter()-start)
            raise

    def run(self):
        required={
          'environment':['00_CONFIG/Step1B_Full_H30_Config.json'],
          'scope':['01_EVALUATION_SCOPE/evaluation_scope.json'],
          'ha':['03_HISTORICAL_AVERAGE/ha_train_stats.pkl'],
          'xgb':['04_XGBOOST/xgboost_H30.json','04_XGBOOST/category_encoder.json'],
          'gru':['05_GRU/gru_H30.pt','05_GRU/gru_scaler.json','05_GRU/gru_epoch_history.csv'],
          'lock':['00_CONFIG/model_lock.json'],
          'predictions':['06_PREDICTIONS/validation_predictions_H30.parquet','06_PREDICTIONS/test_predictions_H30.parquet'],
          'metrics':['07_METRICS/full_h30_forecasting_results.csv'],
          'subgroups':['08_SUBGROUP_ANALYSIS/full_h30_quality_results.csv','08_SUBGROUP_ANALYSIS/subgroup_results.csv'],
          'paired':['09_PAIRED_COMPARISON/xgb_vs_gru_paired_error.csv'],
          'latency':['10_LATENCY/latency_benchmark.csv'],
          'qc':['12_QC/full_h30_qc.json'],
          'xlsx':['Step1B_SMOKE_TEST_Results.xlsx' if self.smoke else '13_RESULTS_XLSX/Step1B_Full_H30_Results.xlsx'],
          'manifest':['15_MANIFEST/Step1B_Full_H30_Manifest.csv'],
        }
        mapping={'environment':self.environment,'scope':self.scope,'ha':self.ha,'xgb':self.xgb,
                 'gru':self.gru,'lock':self.lock,'predictions':self.predictions,'metrics':self.evaluate,
                 'subgroups':self.subgroups,'paired':self.paired,'latency':self.latency,'qc':self.qc,
                 'xlsx':self.xlsx,'manifest':self.manifest}
        for stage in STAGES:self.run_stage(stage,mapping[stage],required[stage])
        logging.info('PIPELINE COMPLETE mode=%s',self.state['mode'])
        logging.shutdown()
        self.manifest()  # Refresh hashes after final state/log writes.

    def environment(self):
        for name in ('train','validation','test'):
            if not (FREEZE/f'{name}.parquet').exists():raise RuntimeError(f'Missing frozen {name}')
        if not OVERLAP.is_file():raise RuntimeError('Missing station overlap source')
        config=dict(run_id=self.run_id,run_date=datetime.now().isoformat(),smoke=self.smoke,
            data_paths={k:str(FREEZE/f'{k}.parquet') for k in ('train','validation','test')},
            provenance={'station_overlap':str(OVERLAP),'step1a_config':str(PEMS/'02_FORECASTING_DATASET_FREEZE/00_README/Step1A_Freeze_Config.json')},
            splits=SPLITS,horizon='H30',target_policy='%Observed = 100',lookback='12 x 5-minute elapsed intervals',
            features=dict(lags=LAGS,summaries=SUMMARIES,context=CONTEXT,categorical=['freeway','direction'],excluded=['station_id']),
            models={'XGBoost':dict(objective='reg:squarederror',learning_rate=0.05,max_depth=8,min_child_weight=5,
                subsample=0.8,colsample_bytree=0.8,n_estimators=20 if self.smoke else 2000,random_state=20260922,
                n_jobs=12,tree_method='hist',device='cpu',early_stopping_rounds=5 if self.smoke else 50),
                'GRU':dict(input_size=5,hidden_size=64,num_layers=1,dropout=0,head='Dense64-ReLU-Dense1',
                optimizer='Adam',learning_rate=1e-3,batch_size=2048,max_epochs=1 if self.smoke else 30,
                early_stopping_patience=5,device='cpu')},
            seed=20260922,cpu=platform.processor(),cpu_threads=12,
            evaluation_scope='Train-seen primary Validation/Test; full and unseen Test secondary',
            latency_protocol='100000 sorted Primary Test sample IDs; warm-up; 5 repetitions; model-only and end-to-end; CPU',
            subgroup_definitions={'AM_peak':'07:00–09:59','PM_peak':'16:00–18:59','Off_peak':'other',
                                  'quality_bins':['Q0','Q1','Q2','Q3','Q4','Q5']},xlsx_schema_version='1.0')
        json_write(self.path('00_CONFIG/Step1B_Full_H30_Config.json'),config)

    def scope(self):
        counts={}
        stations={}
        time_valid=True
        for kind in ('train','validation','test'):
            compact=self.source(kind,['station_id','prediction_timestamp_local'])
            ids=compact['station_id'].to_numpy()
            counts[kind]=len(ids);stations[kind]=set(map(int,ids))
            dates=compact['prediction_timestamp_local'].dt.strftime('%Y-%m-%d')
            if self.smoke:
                lo=hi={'train':'2026-05-23','validation':'2026-05-24','test':'2026-05-25'}[kind]
            else:
                lo,hi={'train':('2026-01-01','2026-05-31'),'validation':('2026-06-01','2026-06-30'),
                       'test':('2026-07-01','2026-08-31')}[kind]
            time_valid=time_valid and bool(dates.between(lo,hi).all())
            if kind=='validation':val_seen=int(np.isin(ids,list(self.seen)).sum())
            if kind=='test':test_seen=int(np.isin(ids,list(self.seen)).sum())
            del compact
        if not time_valid:raise RuntimeError('Frozen chronological split dates changed')
        scope=dict(primary_task='temporal generalization on stations observed in training',
            primary_validation='validation AND station in train',primary_test='test AND station in train',
            secondary_test='full chronological test',robustness_test='test stations absent from train',
            source='station_overlap.json',train_rows=counts['train'],train_stations=len(stations['train']),
            primary_validation_rows=val_seen,primary_validation_stations=len(stations['validation']&self.seen),
            primary_test_rows=test_seen,primary_test_stations=len(stations['test']&self.seen),
            full_test_rows=counts['test'],full_test_stations=len(stations['test']),
            unseen_test_rows=counts['test']-test_seen,unseen_test_stations=len(stations['test']-self.seen),
            unseen_validation_rows=counts['validation']-val_seen,
            frozen=True,smoke=self.smoke,chronological_ranges_valid=time_valid)
        if not self.smoke and (scope['train_rows']!=8702892 or scope['primary_test_rows']!=2951376):
            raise RuntimeError('Full scope disagrees with frozen Step 1A / overlap')
        json_write(self.path('01_EVALUATION_SCOPE/evaluation_scope.json'),scope)
        rows=[]
        for k in ('train','validation','test'):
            rows.append(dict(split=k,rows=counts[k],stations=len(stations[k]),seen_rows=val_seen if k=='validation' else test_seen if k=='test' else counts[k]))
        write_csv(self.path('01_EVALUATION_SCOPE/evaluation_sample_counts.csv'),rows)
        for title,ids in [('seen_validation',stations['validation']&self.seen),('seen_test',stations['test']&self.seen),
                          ('unseen_validation',stations['validation']-self.seen),('unseen_test',stations['test']-self.seen)]:
            write_csv(self.path(f'01_EVALUATION_SCOPE/{title}_station_ids.csv'),
                      [{'station_id':x} for x in sorted(ids)],['station_id'])

    def ha(self):
        frame=self.source('train',['station_id','freeway','direction','day_of_week','hour','minute','target_speed'])
        frame['slot']=frame['hour'].astype(np.int16)*12+frame['minute'].astype(np.int16)//5
        keys=[['station_id','day_of_week','slot'],['station_id','slot'],['station_id'],
              ['freeway','direction','day_of_week','slot'],['freeway','direction','slot'],['day_of_week','slot']]
        start=time.perf_counter()
        levels=[frame.groupby(k,sort=False)['target_speed'].mean() for k in keys]
        data=dict(levels=levels,keys=keys,global_mean=float(frame['target_speed'].mean()),
                  fit_source='TRAIN_ONLY',training_seconds=time.perf_counter()-start)
        with self.path('03_HISTORICAL_AVERAGE/ha_train_stats.pkl').open('wb') as f:pickle.dump(data,f,protocol=5)
        json_write(self.path('03_HISTORICAL_AVERAGE/ha_config.json'),
                   dict(levels=keys+[['global_train_mean']],fit_source='TRAIN_ONLY',training_seconds=data['training_seconds']))

    def predict_ha(self,frame,model):
        temp=frame[['station_id','freeway','direction','day_of_week','hour','minute']].copy()
        temp['slot']=temp['hour'].astype(np.int16)*12+temp['minute'].astype(np.int16)//5
        result=np.full(len(frame),np.nan,dtype=np.float32)
        level=np.zeros(len(frame),dtype=np.int8)
        for index,(series,keys) in enumerate(zip(model['levels'],model['keys']),1):
            missing=np.flatnonzero(~np.isfinite(result))
            if not len(missing):break
            subset=temp.iloc[missing]
            if len(keys)==1:
                value=series.reindex(subset[keys[0]].to_numpy()).to_numpy(dtype=np.float32)
            else:
                lookup=pd.MultiIndex.from_frame(subset[keys])
                value=series.reindex(lookup).to_numpy(dtype=np.float32)
            good=np.isfinite(value)
            result[missing[good]]=value[good];level[missing[good]]=index
        missing=~np.isfinite(result)
        result[missing]=model['global_mean'];level[missing]=7
        return result,level

    def xgb(self):
        columns=list(dict.fromkeys(['station_id','freeway','direction','target_speed']+NUMERIC))
        train=self.source('train',columns)
        val=self.primary_validation(columns)
        ram_monitor=PeakRAM();ram_monitor.start()
        categories={k:sorted(train[k].dropna().astype(str).unique().tolist()) for k in ('freeway','direction')}
        json_write(self.path('04_XGBOOST/category_encoder.json'),
                   dict(categories=categories,fit_source='TRAIN_ONLY',unknown='explicit one-hot column',numeric_features=NUMERIC))
        start=time.perf_counter()
        xtrain=xgb_matrix(train,categories);xval=xgb_matrix(val,categories)
        ytrain=train['target_speed'].to_numpy(dtype=np.float32)
        yval=val['target_speed'].to_numpy(dtype=np.float32)
        prepare_seconds=time.perf_counter()-start
        settings=json.loads(self.path('00_CONFIG/Step1B_Full_H30_Config.json').read_text(encoding='utf-8'))['models']['XGBoost']
        model=xgb.XGBRegressor(**settings)
        start=time.perf_counter()
        model.fit(xtrain,ytrain,eval_set=[(xval,yval)],verbose=False)
        training_seconds=time.perf_counter()-start
        model.save_model(self.path('04_XGBOOST/xgboost_H30.json'))
        peak_ram_gb=ram_monitor.finish()
        json_write(self.path('04_XGBOOST/xgb_train_profile.json'),
                   dict(device='cpu',training_seconds=training_seconds,feature_prepare_seconds=prepare_seconds,
                        best_iteration=int(model.best_iteration),train_rows=len(train),
                        primary_validation_rows=len(val),peak_ram_gb=peak_ram_gb,
                        early_stopping_source='PRIMARY_VALIDATION_ONLY'))
        del train,val,xtrain,xval,ytrain,yval,model;gc.collect()

    def gru(self):
        columns=list(dict.fromkeys(['station_id','freeway','direction','target_speed']+LAGS+CONTEXT))
        train=self.source('train',columns)
        val=self.primary_validation(columns)
        ram_monitor=PeakRAM();ram_monitor.start()
        categories=json.loads(self.path('04_XGBOOST/category_encoder.json').read_text(encoding='utf-8'))['categories']
        np.random.seed(20260922);torch.manual_seed(20260922)
        seq_train=sequence(train)
        means=seq_train.mean(axis=(0,1),dtype=np.float64).astype(np.float32)
        stds=seq_train.std(axis=(0,1),dtype=np.float64).astype(np.float32)
        stds=np.where(stds>1e-8,stds,1).astype(np.float32)
        if not np.isfinite(seq_train).all():raise RuntimeError('GRU Train contains missing/nonfinite sequence cells')
        seq_train-=means;seq_train/=stds
        seq_val=sequence(val)
        if not np.isfinite(seq_val).all():raise RuntimeError('GRU Validation contains missing/nonfinite sequence cells')
        seq_val-=means;seq_val/=stds
        ctx_train=context(train,categories);ctx_val=context(val,categories)
        if not np.isfinite(ctx_train).all() or not np.isfinite(ctx_val).all():raise RuntimeError('GRU context missing/nonfinite')
        ytrain=train['target_speed'].to_numpy(dtype=np.float32).copy()
        yval=val['target_speed'].to_numpy(dtype=np.float32).copy()
        json_write(self.path('05_GRU/gru_scaler.json'),dict(variables=SEQ_VARS,mean=means.tolist(),std=stds.tolist(),
            fit_source='TRAIN_ONLY',sequence_order='lag11_to_lag00',context=CONTEXT+['freeway_onehot','direction_onehot']))
        model=GRUModel(ctx_train.shape[1]).to('cpu')
        optimizer=torch.optim.Adam(model.parameters(),lr=1e-3)
        criterion=nn.MSELoss()
        batch_size=2048
        train_loader=DataLoader(TensorDataset(torch.from_numpy(seq_train),torch.from_numpy(ctx_train),torch.from_numpy(ytrain)),
            batch_size=batch_size,shuffle=True,num_workers=0,generator=torch.Generator().manual_seed(20260922))
        val_loader=DataLoader(TensorDataset(torch.from_numpy(seq_val),torch.from_numpy(ctx_val),torch.from_numpy(yval)),
            batch_size=4096,shuffle=False,num_workers=0)
        max_epochs=1 if self.smoke else 30
        best=float('inf');best_epoch=0;best_state=None;bad=0;history=[];started=time.perf_counter()
        for epoch in range(1,max_epochs+1):
            model.train();begin=time.perf_counter();train_sum=0.;train_n=0
            for xs,xc,y in train_loader:
                optimizer.zero_grad(set_to_none=True)
                pred=model(xs,xc);loss=criterion(pred,y);loss.backward();optimizer.step()
                train_sum+=float(((pred-y)**2).sum().item());train_n+=len(y)
            train_sec=time.perf_counter()-begin
            model.eval();begin=time.perf_counter();val_sum=0.;val_n=0
            with torch.inference_mode():
                for xs,xc,y in val_loader:
                    pred=model(xs,xc)
                    val_sum+=float(((pred-y)**2).sum().item());val_n+=len(y)
            val_sec=time.perf_counter()-begin
            val_loss=val_sum/val_n
            history.append(dict(epoch=epoch,train_loss=train_sum/train_n,validation_loss=val_loss,
                                train_seconds=train_sec,validation_seconds=val_sec))
            logging.info('GRU epoch=%d train_loss=%.6f val_loss=%.6f train_sec=%.3f val_sec=%.3f',
                         epoch,train_sum/train_n,val_loss,train_sec,val_sec)
            if val_loss<best-1e-6:
                best=val_loss;best_epoch=epoch;best_state={k:v.detach().clone() for k,v in model.state_dict().items()};bad=0
            else:bad+=1
            if bad>=5:break
        torch.save(dict(state_dict=best_state,context_size=ctx_train.shape[1],best_epoch=best_epoch,
                        train_source='TRAIN_ONLY',early_stopping_source='PRIMARY_VALIDATION_ONLY'),
                   self.path('05_GRU/gru_H30.pt'))
        write_csv(self.path('05_GRU/gru_epoch_history.csv'),history)
        peak_ram_gb=ram_monitor.finish()
        json_write(self.path('05_GRU/gru_train_profile.json'),
            dict(device='cpu',training_seconds=time.perf_counter()-started,epochs_completed=len(history),best_epoch=best_epoch,
                 median_train_seconds_per_epoch=statistics.median(x['train_seconds'] for x in history),
                 median_validation_seconds_per_epoch=statistics.median(x['validation_seconds'] for x in history),
                 batch_size=batch_size,peak_ram_gb=peak_ram_gb,
                 early_stopping_source='PRIMARY_VALIDATION_ONLY'))
        del train,val,seq_train,seq_val,ctx_train,ctx_val,ytrain,yval,model;gc.collect()

    def lock(self):
        xgb_profile=json.loads(self.path('04_XGBOOST/xgb_train_profile.json').read_text(encoding='utf-8'))
        gru_profile=json.loads(self.path('05_GRU/gru_train_profile.json').read_text(encoding='utf-8'))
        files=['04_XGBOOST/xgboost_H30.json','04_XGBOOST/category_encoder.json','05_GRU/gru_H30.pt','05_GRU/gru_scaler.json']
        hashes={item:sha256(self.path(item)) for item in files}
        lock=dict(xgb_best_iteration=xgb_profile['best_iteration'],gru_best_epoch=gru_profile['best_epoch'],
            xgb_feature_set_locked=True,gru_architecture_locked=True,scaler_locked=True,encoder_locked=True,
            test_used_for_tuning=False,locked_before_test=True,training_complete=True,
            created_before_test_inference=datetime.now(timezone.utc).isoformat(),artifact_sha256=hashes,
            smoke=self.smoke)
        json_write(self.path('00_CONFIG/model_lock.json'),lock)

    def load_models(self):
        lock=json.loads(self.path('00_CONFIG/model_lock.json').read_text(encoding='utf-8'))
        if not lock.get('locked_before_test') or lock.get('test_used_for_tuning'):
            raise RuntimeError('Model lock missing before Test inference')
        for relative,expected in lock['artifact_sha256'].items():
            if sha256(self.path(relative))!=expected:raise RuntimeError(f'Locked artifact changed: {relative}')
        ha=pickle.load(self.path('03_HISTORICAL_AVERAGE/ha_train_stats.pkl').open('rb'))
        xgb_model=xgb.XGBRegressor(device='cpu',tree_method='hist',n_jobs=12)
        xgb_model.load_model(self.path('04_XGBOOST/xgboost_H30.json'))
        categories=json.loads(self.path('04_XGBOOST/category_encoder.json').read_text(encoding='utf-8'))['categories']
        scaler=json.loads(self.path('05_GRU/gru_scaler.json').read_text(encoding='utf-8'))
        checkpoint=torch.load(self.path('05_GRU/gru_H30.pt'),map_location='cpu',weights_only=False)
        gru=GRUModel(checkpoint['context_size']).to('cpu')
        gru.load_state_dict(checkpoint['state_dict']);gru.eval()
        return ha,xgb_model,gru,categories,scaler

    def gru_predict(self,frame,gru,categories,scaler,batch_size=2048):
        seq=sequence(frame)
        seq-=np.asarray(scaler['mean'],dtype=np.float32)
        seq/=np.asarray(scaler['std'],dtype=np.float32)
        ctx=context(frame,categories)
        output=[]
        with torch.inference_mode():
            for start in range(0,len(frame),batch_size):
                xs=torch.from_numpy(seq[start:start+batch_size]);xc=torch.from_numpy(ctx[start:start+batch_size])
                output.append(gru(xs,xc).numpy())
        return np.concatenate(output).astype(np.float32)

    def predictions(self):
        ha,xgb_model,gru,categories,scaler=self.load_models()
        fallback=Counter()
        for kind in ('validation','test'):
            frame=self.source(kind,PRED_COLS)
            if not frame['target_observed_pct'].eq(100).all():raise RuntimeError('Target quality violation')
            if frame['sample_id'].duplicated().any():raise RuntimeError('Duplicate source sample_id')
            target_path=self.path(f'06_PREDICTIONS/{kind}_predictions_H30.parquet')
            writer=None;written=0
            try:
                for start in range(0,len(frame),100000):
                    batch=frame.iloc[start:start+100000]
                    y=batch['target_speed'].to_numpy(dtype=np.float32)
                    persist=batch['speed_lag00'].to_numpy(dtype=np.float32)
                    ha_pred,levels=self.predict_ha(batch,ha)
                    xgb_pred=xgb_model.predict(xgb_matrix(batch,categories)).astype(np.float32)
                    gru_pred=self.gru_predict(batch,gru,categories,scaler)
                    for level,n in zip(*np.unique(levels,return_counts=True)):
                        fallback[(kind,int(level))]+=int(n)
                    seen=batch['station_id'].isin(self.seen).to_numpy()
                    local=batch['prediction_timestamp_local']
                    hour=local.dt.hour.to_numpy()
                    peak=np.where((hour>=7)&(hour<10),'AM_PEAK',np.where((hour>=16)&(hour<19),'PM_PEAK','OFF_PEAK'))
                    out=batch[['sample_id','station_id','prediction_timestamp_local','prediction_timestamp_utc',
                               'freeway','direction','input_observed_pct','input_quality_bin','target_speed',
                               'target_observed_pct','is_weekend']].copy()
                    out['prediction_persistence']=persist;out['prediction_HA']=ha_pred
                    out['prediction_XGB']=xgb_pred;out['prediction_GRU']=gru_pred
                    for name,pred in [('persistence',persist),('HA',ha_pred),('XGB',xgb_pred),('GRU',gru_pred)]:
                        error=pred-y
                        out[f'error_{name}']=error
                        out[f'AE_{name}']=np.abs(error)
                    out['SE_XGB']=(xgb_pred-y)**2
                    out['SE_GRU']=(gru_pred-y)**2
                    out['delta_AE_XGB_GRU']=out['AE_XGB']-out['AE_GRU']
                    out['is_seen_station']=seen;out['is_unseen_station']=~seen;out['peak_period']=peak
                    table=pa.Table.from_pandas(out,preserve_index=False)
                    if writer is None:writer=pq.ParquetWriter(target_path,table.schema,compression='zstd')
                    writer.write_table(table);written+=len(out)
                if written!=len(frame):raise RuntimeError('Prediction row count mismatch')
            finally:
                if writer:writer.close()
            logging.info('PREDICTIONS kind=%s rows=%d',kind,written)
            del frame;gc.collect()
        total=sum(fallback.values())
        rows=[dict(split=split,fallback_level=level,count=fallback[(split,level)],
                   percentage=100*fallback[(split,level)]/sum(fallback[(split,x)] for x in range(1,8)))
              for split in ('validation','test') for level in range(1,8)]
        write_csv(self.path('03_HISTORICAL_AVERAGE/historical_average_fallback_summary.csv'),rows)

    def prediction_frames(self):
        val=pq.read_table(self.path('06_PREDICTIONS/validation_predictions_H30.parquet')).to_pandas()
        test=pq.read_table(self.path('06_PREDICTIONS/test_predictions_H30.parquet')).to_pandas()
        return val,test

    def scopes(self,val,test):
        return {'PRIMARY_VALIDATION':val[val['is_seen_station']],
                'PRIMARY_TEST':test[test['is_seen_station']],
                'FULL_TEST':test,
                'UNSEEN_TEST':test[test['is_unseen_station']]}

    def evaluate(self):
        val,test=self.prediction_frames()
        rows=[]
        for scope,frame in self.scopes(val,test).items():
            for model,col in [('Persistence','prediction_persistence'),('HistoricalAverage','prediction_HA'),
                              ('XGBoost','prediction_XGB'),('GRU','prediction_GRU')]:
                rows.append(dict(model=model,scope=scope,stations=frame['station_id'].nunique(),
                                 **metrics(frame['target_speed'],frame[col])))
        write_csv(self.path('07_METRICS/full_h30_forecasting_results.csv'),rows)

    def subgroups(self):
        _,test=self.prediction_frames()
        primary=test[test['is_seen_station']].copy()
        quality=[];q0=[];sub=[]
        def collect(dimension,group,frame,target):
            for model,col in [('Persistence','prediction_persistence'),('HistoricalAverage','prediction_HA'),
                              ('XGBoost','prediction_XGB'),('GRU','prediction_GRU')]:
                target.append(dict(dimension=dimension,group=group,model=model,stations=frame['station_id'].nunique(),
                                   days=frame['prediction_timestamp_local'].dt.date.nunique() if len(frame) else 0,
                                   **metrics(frame['target_speed'],frame[col])))
        for q in ('Q0','Q1','Q2','Q3','Q4','Q5'):
            frame=primary[primary['input_quality_bin']==q]
            collect('quality_bin',q,frame,quality)
            if q=='Q0':collect('degraded_input','Q0_to_target100',frame,q0)
        collect('seen_unseen','PRIMARY_TEST_SEEN',primary,sub)
        collect('seen_unseen','UNSEEN_TEST',test[test['is_unseen_station']],sub)
        for group,frame in primary.groupby('peak_period',sort=True):collect('peak_period',group,frame,sub)
        for weekend,frame in primary.groupby('is_weekend',sort=True):
            collect('weekday_weekend','WEEKEND' if weekend else 'WEEKDAY',frame,sub)
        for fw,frame in primary.groupby('freeway',sort=True):collect('freeway',str(fw),frame,sub)
        write_csv(self.path('08_SUBGROUP_ANALYSIS/full_h30_quality_results.csv'),quality)
        write_csv(self.path('08_SUBGROUP_ANALYSIS/q0_degraded_results.csv'),q0)
        write_csv(self.path('08_SUBGROUP_ANALYSIS/subgroup_results.csv'),sub)

    def paired(self):
        val,test=self.prediction_frames()
        scopes=self.scopes(val,test)
        primary=scopes['PRIMARY_TEST']
        scopes.update({'Q0_PRIMARY_TEST':primary[primary['input_quality_bin']=='Q0'],
                       'Q5_PRIMARY_TEST':primary[primary['input_quality_bin']=='Q5']})
        for peak in ('AM_PEAK','PM_PEAK','OFF_PEAK'):
            scopes[peak]=primary[primary['peak_period']==peak]
        rows=[]
        for name,frame in scopes.items():
            delta=frame['delta_AE_XGB_GRU'].to_numpy(dtype=np.float64)
            n=len(delta)
            rows.append(dict(scope=name,N=n,mean_delta_AE=float(delta.mean()) if n else None,
                median_delta_AE=float(np.median(delta)) if n else None,
                P25=float(np.percentile(delta,25)) if n else None,
                P75=float(np.percentile(delta,75)) if n else None,
                P90=float(np.percentile(delta,90)) if n else None,
                GRU_better_n=int((delta>0).sum()),GRU_better_pct=100*float((delta>0).mean()) if n else None,
                XGB_better_n=int((delta<0).sum()),XGB_better_pct=100*float((delta<0).mean()) if n else None,
                tie_n=int((delta==0).sum()),tie_pct=100*float((delta==0).mean()) if n else None))
        write_csv(self.path('09_PAIRED_COMPARISON/xgb_vs_gru_paired_error.csv'),rows)
        threshold=[]
        for scope in ('PRIMARY_VALIDATION','PRIMARY_TEST'):
            frame=scopes[scope]
            for model in ('XGB','GRU'):
                ae=frame[f'AE_{model}'].to_numpy(dtype=np.float64)
                for relation,value in [('LE',1),('LE',2),('LE',3),('LE',5),('GT',5),('GT',10)]:
                    count=int((ae<=value).sum()) if relation=='LE' else int((ae>value).sum())
                    threshold.append(dict(scope=scope,model=model,relation=relation,threshold_mph=value,
                                          N=len(ae),count=count,percentage=100*count/len(ae) if len(ae) else 0))
        write_csv(self.path('09_PAIRED_COMPARISON/error_thresholds.csv'),threshold)

    def latency(self):
        _,test=self.prediction_frames()
        primary=test[test['is_seen_station']]
        ids=primary['sample_id'].sort_values().iloc[:100000].tolist()
        write_csv(self.path('10_LATENCY/latency_sample_ids.csv'),[{'sample_id':x} for x in ids],['sample_id'])
        selected=set(ids)
        raw=self.source('test',PRED_COLS)
        raw=raw[raw['sample_id'].isin(selected)].set_index('sample_id').loc[ids].reset_index()
        if len(raw)!=len(ids):raise RuntimeError('Latency sample alignment failed')
        ha,xgb_model,gru,categories,scaler=self.load_models()
        x_matrix=xgb_matrix(raw,categories)
        s=sequence(raw)
        s-=np.asarray(scaler['mean'],dtype=np.float32);s/=np.asarray(scaler['std'],dtype=np.float32)
        c=context(raw,categories)
        seq=torch.from_numpy(s);ctx=torch.from_numpy(c)
        ha_cache,_=self.predict_ha(raw,ha)
        persistence_cache=raw['speed_lag00'].to_numpy(dtype=np.float32)
        def gru_prepared():
            pieces=[]
            with torch.inference_mode():
                for i in range(0,len(raw),2048):pieces.append(gru(seq[i:i+2048],ctx[i:i+2048]).numpy())
            return np.concatenate(pieces)
        tasks={
            'Persistence':(lambda:persistence_cache.copy(),lambda:raw['speed_lag00'].to_numpy(dtype=np.float32).copy()),
            'HistoricalAverage':(lambda:ha_cache.copy(),lambda:self.predict_ha(raw,ha)[0]),
            'XGBoost':(lambda:xgb_model.predict(x_matrix),lambda:xgb_model.predict(xgb_matrix(raw,categories))),
            'GRU':(gru_prepared,lambda:self.gru_predict(raw,gru,categories,scaler)),
        }
        rows=[]
        for model,(model_only,end_to_end) in tasks.items():
            for mode,fn in [('MODEL_ONLY',model_only),('END_TO_END',end_to_end)]:
                fn()  # warm-up
                times=[]
                for _ in range(5):
                    start=time.perf_counter();pred=fn();times.append(time.perf_counter()-start)
                    if len(pred)!=len(raw) or not np.isfinite(pred).all():raise RuntimeError('Latency prediction invalid')
                median=float(np.median(times))
                rows.append(dict(model=model,mode=mode,N=len(raw),median_seconds=median,P90_seconds=float(np.percentile(times,90)),
                    min_seconds=min(times),max_seconds=max(times),samples_per_second=len(raw)/median,
                    microseconds_per_sample=median*1e6/len(raw),device='CPU',runs=5,batch_size=2048 if model=='GRU' else 'N/A'))
        write_csv(self.path('10_LATENCY/latency_benchmark.csv'),rows)

    def qc(self):
        val,test=self.prediction_frames()
        scope=json.loads(self.path('01_EVALUATION_SCOPE/evaluation_scope.json').read_text(encoding='utf-8'))
        lock=json.loads(self.path('00_CONFIG/model_lock.json').read_text(encoding='utf-8'))
        xgb_profile=json.loads(self.path('04_XGBOOST/xgb_train_profile.json').read_text(encoding='utf-8'))
        gru_profile=json.loads(self.path('05_GRU/gru_train_profile.json').read_text(encoding='utf-8'))
        scaler=json.loads(self.path('05_GRU/gru_scaler.json').read_text(encoding='utf-8'))
        encoder=json.loads(self.path('04_XGBOOST/category_encoder.json').read_text(encoding='utf-8'))
        dup=int(val['sample_id'].duplicated().sum()+test['sample_id'].duplicated().sum()+
                val['sample_id'].isin(set(test['sample_id'])).sum())
        missing=int(val['target_speed'].isna().sum()+test['target_speed'].isna().sum())
        quality=int((val['target_observed_pct']!=100).sum()+(test['target_observed_pct']!=100).sum())
        pred_cols=[f'prediction_{x}' for x in ('persistence','HA','XGB','GRU')]
        nan_pred=int(sum(val[c].isna().sum()+test[c].isna().sum() for c in pred_cols))
        inf_pred=int(sum(np.isinf(val[c]).sum()+np.isinf(test[c]).sum() for c in pred_cols))
        val_seen=val[val['is_seen_station']];test_seen=test[test['is_seen_station']]
        test_unseen=test[test['is_unseen_station']]
        scope_ok=(len(val_seen)==scope['primary_validation_rows'] and len(test_seen)==scope['primary_test_rows'] and
                  len(test)==scope['full_test_rows'] and len(test_unseen)==scope['unseen_test_rows'])
        mask_ok=(set(val_seen['station_id']).issubset(self.seen) and set(test_seen['station_id']).issubset(self.seen) and
                 not set(test_unseen['station_id'])&self.seen)
        date_ok=(val['prediction_timestamp_local'].dt.strftime('%Y-%m-%d').between('2026-05-24','2026-05-24').all() and
                 test['prediction_timestamp_local'].dt.strftime('%Y-%m-%d').between('2026-05-25','2026-05-25').all()) if self.smoke else (
                 val['prediction_timestamp_local'].dt.strftime('%Y-%m-%d').between('2026-06-01','2026-06-30').all() and
                 test['prediction_timestamp_local'].dt.strftime('%Y-%m-%d').between('2026-07-01','2026-08-31').all())
        lock_before=lock['locked_before_test'] and datetime.fromisoformat(lock['created_before_test_inference']).timestamp() <= self.path('06_PREDICTIONS/test_predictions_H30.parquet').stat().st_mtime
        qc=dict(mode='SMOKE' if self.smoke else 'FORMAL',train_validation_test_time_unchanged=bool(date_ok and scope['chronological_ranges_valid']),
            primary_validation_seen_only=bool(set(val_seen['station_id']).issubset(self.seen)),
            primary_test_seen_only=bool(set(test_seen['station_id']).issubset(self.seen)),
            unseen_test_all_absent_from_train=bool(not set(test_unseen['station_id'])&self.seen),
            duplicate_sample_id=dup,missing_target=missing,target100_violations=quality,
            nan_prediction=nan_pred,infinite_prediction=inf_pred,
            xgb_early_stopping_test_leakage=0 if xgb_profile['early_stopping_source']=='PRIMARY_VALIDATION_ONLY' else 1,
            gru_early_stopping_test_leakage=0 if gru_profile['early_stopping_source']=='PRIMARY_VALIDATION_ONLY' else 1,
            scaler_test_leakage=0 if scaler['fit_source']=='TRAIN_ONLY' else 1,
            encoder_test_leakage=0 if encoder['fit_source']=='TRAIN_ONLY' else 1,
            model_locked_before_test=bool(lock_before),prediction_rows_equal_scope=scope_ok,
            all_models_same_sample_scope=True,leakage_violations=0 if mask_ok and date_ok and lock_before else 1,
            smoke_results_not_paper_results=self.smoke)
        fail=dup or missing or quality or nan_pred or inf_pred or not scope_ok or not mask_ok or not date_ok or not scope['chronological_ranges_valid'] or not lock_before
        qc['status']='FAIL' if fail else 'PASS'
        json_write(self.path('12_QC/full_h30_qc.json'),qc)
        resource={'Persistence':{'training_seconds':0},'HistoricalAverage':json.loads(self.path('03_HISTORICAL_AVERAGE/ha_config.json').read_text(encoding='utf-8')),
                  'XGBoost':xgb_profile,'GRU':gru_profile,'cpu':platform.processor(),'ram_total_gb':psutil.virtual_memory().total/1e9}
        json_write(self.path('11_RESOURCE_PROFILE/compute_profile.json'),resource)
        if fail:raise RuntimeError(f'QC failed: {qc}')

    def xlsx(self):
        output=self.path('Step1B_SMOKE_TEST_Results.xlsx' if self.smoke else '13_RESULTS_XLSX/Step1B_Full_H30_Results.xlsx')
        self.manifest()  # Populate the workbook's FileManifest sheet before XLSX creation.
        count=build_workbook(self.dir,output,self.run_id,'SMOKE_PASS' if self.smoke else 'PASS')
        if count!=25:raise RuntimeError('XLSX sheet count mismatch')
        qc_path=self.path('12_QC/full_h30_qc.json')
        qc=json.loads(qc_path.read_text(encoding='utf-8'));qc['xlsx_readback']='PASS';qc['xlsx_sheets']=count
        json_write(qc_path,qc)
        self.manifest()
        build_workbook(self.dir,output,self.run_id,'SMOKE_PASS' if self.smoke else 'PASS')

    def manifest(self):
        candidates=[p for p in self.dir.rglob('*') if p.is_file() and p.name!='Step1B_Full_H30_Manifest.csv']
        if not self.smoke:candidates=[p for p in candidates if '99_SMOKE_TEST' not in p.parts]
        candidates += list(Path(__file__).parent.glob('*.py'))
        rows=[]
        for p in sorted(candidates,key=str):
            rows.append(dict(filename=p.name,relative_path=str(p.relative_to(TRAINING_ROOT)),
                size_bytes=p.stat().st_size,sha256=sha256(p),created_time=datetime.fromtimestamp(p.stat().st_ctime).isoformat(),
                purpose='Step1B '+('smoke' if self.smoke else 'formal')+' code/config/model/result/prediction/log',run_id=self.run_id))
        write_csv(self.path('15_MANIFEST/Step1B_Full_H30_Manifest.csv'),rows)
