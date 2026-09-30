"""Consolidate STEP 0B daily checkpoints without rereading raw archives."""
from __future__ import annotations

import csv
import json
import math
import statistics
from collections import Counter, defaultdict
from datetime import date, timedelta

import numpy as np

import importlib
s = importlib.import_module('12_step0b_percent_observed')

BINS = [
    ('0', lambda x: x == 0),
    ('(0,25)', lambda x: (x > 0) & (x < 25)),
    ('[25,50)', lambda x: (x >= 25) & (x < 50)),
    ('[50,80)', lambda x: (x >= 50) & (x < 80)),
    ('[80,90)', lambda x: (x >= 80) & (x < 90)),
    ('[90,100)', lambda x: (x >= 90) & (x < 100)),
    ('100', lambda x: x == 100),
]
SAMPLE_BINS = [
    ('0', lambda x: x == 0),
    ('(0,50)', lambda x: (x > 0) & (x < 50)),
    ('[50,80)', lambda x: (x >= 50) & (x < 80)),
    ('[80,90)', lambda x: (x >= 80) & (x < 90)),
    ('[90,100)', lambda x: (x >= 90) & (x < 100)),
    ('100', lambda x: x == 100),
]
INPUT_BINS = [
    ('0', lambda x: x == 0),
    ('1-49', lambda x: (x > 0) & (x < 50)),
    ('50-79', lambda x: (x >= 50) & (x < 80)),
    ('80-89', lambda x: (x >= 80) & (x < 90)),
    ('90-99', lambda x: (x >= 90) & (x < 100)),
    ('100', lambda x: x == 100),
]
THRESHOLDS = [
    ('100', lambda x: x == 100),
    ('ge90', lambda x: x >= 90),
    ('ge80', lambda x: x >= 80),
    ('gt0', lambda x: x > 0),
]

def pct(n, d):
    return round(100 * n / d, 6) if d else None

def hist_quantile(hist, q):
    n = sum(hist.values())
    if not n:
        return None
    ordered = sorted(hist.items())
    def at(rank):
        cumulative = 0
        for value, count in ordered:
            cumulative += count
            if cumulative > rank:
                return value
        return ordered[-1][0]
    rank = (n - 1) * q
    low, high = math.floor(rank), math.ceil(rank)
    return at(low) + (at(high) - at(low)) * (rank - low)

def count_hist(hist, values):
    if len(values):
        unique, counts = np.unique(values, return_counts=True)
        hist.update({float(v): int(n) for v, n in zip(unique, counts)})

def load_day(day):
    with np.load(s.TEMP / f'{day}.npz', allow_pickle=False) as file:
        return {name: file[name] for name in file.files}

def ensure_acc(mapping, key):
    if key not in mapping:
        mapping[key] = {'n': 0, 'stations': set(), 'station_days': 0, 'days': set(), 'freeways': set(), 'directions': set()}
    return mapping[key]

def add_coverage(acc, counts, stations, day, freeways, directions):
    acc['n'] += int(np.sum(counts))
    acc['station_days'] += int(np.count_nonzero(counts))
    for i in np.flatnonzero(counts):
        station = int(stations[i])
        acc['stations'].add(station)
        acc['days'].add(day)
        acc['freeways'].add(str(freeways[i]))
        acc['directions'].add(str(directions[i]))

def coverage_row(acc):
    return dict(N=acc['n'], unique_stations=len(acc['stations']), unique_station_days=acc['station_days'], unique_days=len(acc['days']), unique_freeways=len(acc['freeways']), unique_directions=len(acc['directions']))

def make_official_definitions():
    hourly = 'https://dot.ca.gov/-/media/dot-media/programs/research-innovation-system-information/documents/final-reports/ca22-task3253-a11y.pdf'
    sensor = 'https://dot.ca.gov/-/media/dot-media/programs/research-innovation-system-information/documents/final-reports/ca22-3141_final_reportv3-a11y.pdf'
    source = 'https://dot.ca.gov/programs/traffic-operations/mpr/pems-source'
    rows = [
        dict(field='Samples', official_definition='Total number of samples received for all lanes.', source_url=hourly, applicability='Caltrans report Table 8 describes Station Hour; same-named Station 5-Minute field needs direct specification confirmation.', status='OFFICIAL_DEFINITION_INCOMPLETE'),
        dict(field='% Observed', official_definition='Percentage of 5-minute lane points that were observed, meaning not imputed.', source_url=hourly, applicability='Definition explicitly names 5-minute lane points within a Station Hour specification; 0 indicates no lane point classified as observed in that aggregate.', status='SUPPORTED_WITH_GRANULARITY_CAVEAT'),
        dict(field='Total Flow', official_definition='Caltrans Station Hour table: sum of 5-minute flows over the hour; the basic 5-minute rollup normalizes flow by the number of good samples.', source_url=hourly, applicability='Hourly formula is not the exact 5-minute field definition; do not apply Veh/Hour units to these raw files.', status='OFFICIAL_DEFINITION_INCOMPLETE'),
        dict(field='Avg Occupancy', official_definition='Caltrans Station Hour table: average of 5-minute station occupancies, a decimal fraction from 0 to 1.', source_url=hourly, applicability='Exact Station 5-Minute aggregation formula not independently verified.', status='OFFICIAL_DEFINITION_INCOMPLETE'),
        dict(field='Avg Speed', official_definition='Caltrans Station Hour table: flow-weighted mean of 5-minute station speeds; if flow is zero, arithmetic mean.', source_url=hourly, applicability='Exact Station 5-Minute aggregation and estimation lineage not independently verified.', status='OFFICIAL_DEFINITION_INCOMPLETE'),
        dict(field='Estimated data at low observation', official_definition='A Caltrans technical report contrasts direct measurements with estimated data based on surrounding sensors; it excluded low-observation counts because estimates may contain error.', source_url=sensor, applicability='Supports possibility of neighboring-sensor estimation, not the exact source for any individual Speed, Flow or Occupancy cell.', status='SUPPORTED_WITH_RECORD_LEVEL_LIMITATION'),
        dict(field='PeMS processing version', official_definition='Caltrans states PeMS 14 updated algorithms used to compute speed compared with PeMS 12.', source_url=source, applicability='The raw file does not carry a per-record algorithm provenance field.', status='OFFICIAL_DEFINITION_INCOMPLETE'),
    ]
    s.write_csv(s.OUT / 'official_field_definitions.csv', rows, ['field', 'official_definition', 'source_url', 'applicability', 'status'])
    md = ['# Official field definition audit', '', 'Only Caltrans and PeMS official materials are used for definitions.', '']
    for row in rows:
        md += [f"## {row['field']}", '', f"- Definition: {row['official_definition']}", f"- Source: {row['source_url']}", f"- Applicability: {row['applicability']}", f"- Status: {row['status']}", '']
    md += ['## Interpretation of `% Observed = 0`', '', 'The official wording supports that no 5-minute lane point contributing to the reported percentage was classified as directly observed. Caltrans documentation also establishes that PeMS can provide estimated values using surrounding sensors when direct observations are insufficient. A non-null Speed, Flow, or Occupancy value in a 0% row therefore cannot be certified as direct detector ground truth. The exact algorithm and input source for each such cell are not identifiable from these files: **OFFICIAL_DEFINITION_INCOMPLETE** at record-level lineage.', '', 'The reviewed table documents Station Hour fields. It does not independently establish every Station 5-Minute aggregation formula or unit; these are explicitly left unresolved.', '']
    (s.OUT / 'official_field_definition_audit.md').write_text('\n'.join(md), encoding='utf-8')
    return rows

def evaluate_targets(previous, current, threshold_acc, target_acc, input_acc, station_eligible, stable_ids, target_day_summary):
    day = str(previous['date'])
    stations = previous['stations']
    old_len = previous['present'].shape[1]
    stable_rows = np.isin(stations, np.fromiter(stable_ids, dtype=np.int32))
    next_present = np.zeros((len(stations), 12), dtype=bool)
    next_obs = np.full((len(stations), 12), np.nan, dtype=np.float32)
    if current is not None and date.fromisoformat(str(current['date'])) - date.fromisoformat(day) == timedelta(days=1):
        indices = np.searchsorted(current['stations'], stations)
        within = indices < len(current['stations'])
        matched = np.flatnonzero(within & (current['stations'][np.minimum(indices, len(current['stations']) - 1)] == stations))
        if len(matched):
            next_present[matched] = current['present'][indices[matched], :12]
            next_obs[matched] = current['observed'][indices[matched], :12]
    extended_present = np.concatenate((previous['present'], next_present), axis=1)
    extended_obs = np.concatenate((previous['observed'], next_obs), axis=1)
    for horizon in (30, 60):
        steps = horizon // 5
        target_present = extended_present[:, steps:steps + old_len]
        target_obs = extended_obs[:, steps:steps + old_len]
        origin = previous['present']
        aligned = origin & target_present & np.isfinite(target_obs)
        target_day_summary.append(dict(date=day, horizon_minutes=horizon, origin_rows=int(origin.sum()), aligned_targets=int(aligned.sum()), missing_targets=int(origin.sum() - aligned.sum())))
        for label, predicate in BINS:
            mask = aligned & predicate(target_obs)
            counts = mask.sum(axis=1)
            add_coverage(ensure_acc(target_acc, (horizon, label)), counts, stations, day, previous['freeway'], previous['direction'])
        for label, predicate in THRESHOLDS:
            mask = aligned & predicate(target_obs)
            counts = mask.sum(axis=1)
            add_coverage(ensure_acc(threshold_acc, ('ALL', horizon, label)), counts, stations, day, previous['freeway'], previous['direction'])
            stable_counts = counts.copy()
            stable_counts[~stable_rows] = 0
            add_coverage(ensure_acc(threshold_acc, ('STABLE', horizon, label)), stable_counts, stations, day, previous['freeway'], previous['direction'])
            if label == 'ge90':
                for index in np.flatnonzero(counts):
                    key = (horizon, int(stations[index]))
                    station_eligible[key]['count'] += int(counts[index])
                    station_eligible[key]['days'].add(day)
        high_target = aligned & (target_obs >= 90)
        input_obs = previous['observed']
        for label, predicate in INPUT_BINS:
            counts = (high_target & predicate(input_obs)).sum(axis=1)
            add_coverage(ensure_acc(input_acc, ('ALL', horizon, label)), counts, stations, day, previous['freeway'], previous['direction'])
            stable_counts = counts.copy()
            stable_counts[~stable_rows] = 0
            add_coverage(ensure_acc(input_acc, ('STABLE', horizon, label)), stable_counts, stations, day, previous['freeway'], previous['direction'])

def run_audit(previous, current, state, stats):
    """Record exact repeated values under zero observation, including midnight joins."""
    day = str(previous['date'])
    length = previous['present'].shape[1]
    previous_day = date.fromisoformat(day) - timedelta(days=1)
    for key, run in list(state.items()):
        if run['last_day'] != previous_day:
            record_run(key, run, stats)
            del state[key]
    for field in ('speed', 'flow', 'occupancy'):
        matrix = previous[field]
        eligible_matrix = previous['present'] & (previous['observed'] == 0) & np.isfinite(matrix)
        for i, station_value in enumerate(previous['stations']):
            key = (int(station_value), field)
            indices = np.flatnonzero(eligible_matrix[i])
            if len(indices) == 0:
                if key in state:
                    record_run(key, state.pop(key), stats)
                continue
            values = matrix[i, indices]
            breaks = np.flatnonzero((np.diff(indices) != 1) | (np.diff(values) != 0)) + 1
            boundaries = np.concatenate(([0], breaks, [len(indices)]))
            starts = indices[boundaries[:-1]]
            ends = indices[boundaries[1:] - 1]
            lengths = np.diff(boundaries)
            prior = state.pop(key, None)
            if prior:
                if starts[0] == 0 and prior['last_day'] == previous_day and prior['last_index'] == prior['day_length'] - 1 and prior['value'] == float(values[0]):
                    lengths[0] += prior['length']
                    first_start = prior['start_day']
                else:
                    record_run(key, prior, stats)
                    first_start = day
            else:
                first_start = day
            for j in range(len(lengths)):
                run = dict(value=float(values[boundaries[j]]), length=int(lengths[j]), start_day=first_start if j == 0 else day, last_day=day, last_index=int(ends[j]), day_length=length)
                if j == len(lengths) - 1 and ends[j] == length - 1:
                    state[key] = run
                else:
                    record_run(key, run, stats)

def record_run(key, run, stats):
    station, field = key
    slot_count = run['length']
    if slot_count < 6:
        return
    item = stats[(station, field)]
    item['runs_ge_30min'] += 1
    if slot_count >= 12:
        item['runs_ge_60min'] += 1
    if slot_count >= 24:
        item['runs_ge_120min'] += 1
    item['longest_run_minutes'] = max(item['longest_run_minutes'], slot_count * 5)
    item['first_example_date'] = min(item['first_example_date'], run['start_day']) if item['first_example_date'] else run['start_day']

def build():
    items = s.read_csv(s.CANON)
    if len(items) != 243 or len({x['date'] for x in items}) != 243:
        raise RuntimeError('canonical file list is not 243 unique dates')
    missing_checkpoints = [x['date'] for x in items if not (s.TEMP / f"{x['date']}.npz").exists()]
    if missing_checkpoints:
        raise RuntimeError(f'Missing STEP 0B daily checkpoints: {missing_checkpoints}')
    official = make_official_definitions()
    meta_rows = s.read_csv(s.ROOT / '00_DATA_AUDIT' / '09_METADATA_MATCH' / 'metadata_snapshot_comparison.csv')
    stable_ids = {int(x['station']) for x in meta_rows if str(x.get('overall_metadata_stable', '')).lower() == 'true'}
    bin_acc = {}
    stable_bin_acc = {}
    month_acc = defaultdict(Counter)
    daily_rows = []
    station_hist = defaultdict(lambda: np.zeros(101, dtype=np.int64))
    station_days = defaultdict(set)
    station_freeways = defaultdict(set)
    station_directions = defaultdict(set)
    station_transitions = Counter()
    quality_last = {}
    fd_acc = defaultdict(lambda: {'stations': set(), 'rows': 0, 'zero': 0, 'ge80': 0, 'ge90': 0, 'eq100': 0})
    sample_hist = defaultdict(Counter)
    sample_counts = defaultdict(Counter)
    variable_hist = defaultdict(Counter)
    variable_counts = defaultdict(Counter)
    threshold_acc = {}
    target_acc = {}
    input_acc = {}
    station_eligible = defaultdict(lambda: {'count': 0, 'days': set()})
    target_day_summary = []
    run_state = {}
    run_stats = defaultdict(lambda: {'runs_ge_30min': 0, 'runs_ge_60min': 0, 'runs_ge_120min': 0, 'longest_run_minutes': 0, 'first_example_date': ''})
    identity_issues = []
    all_stations = set()
    ml_rows = 0
    stable_ml_rows = 0
    previous = None
    for item in items:
        data = load_day(item['date'])
        day = item['date']
        month = day[:7]
        stations = data['stations']
        all_stations.update(map(int, stations))
        if int(data['duplicate_keys']) or int(data['identity_variants']):
            identity_issues.append(dict(date=day, duplicate_station_time_keys=int(data['duplicate_keys']), station_identity_variants=int(data['identity_variants'])))
        present = data['present']
        observed = data['observed']
        valid = present & np.isfinite(observed)
        counts_by_station = valid.sum(axis=1)
        day_n = int(present.sum())
        ml_rows += int(data['ml_rows'])
        stable_rows = np.isin(stations, np.fromiter(stable_ids, dtype=np.int32))
        stable_ml_rows += int(counts_by_station[stable_rows].sum())
        if int(data['ml_rows']) != day_n:
            raise RuntimeError(f'ML station-time grid cannot represent all rows on {day}: raw={int(data["ml_rows"])} unique={day_n}')
        obs_values = observed[valid]
        if np.any((obs_values < 0) | (obs_values > 100) | (np.abs(obs_values - np.rint(obs_values)) > 1e-5)):
            raise RuntimeError(f'Unexpected noninteger or out-of-range % Observed values on {day}; exact histogram method must be revised')
        ob_int = obs_values.astype(np.int32)
        station_index = np.broadcast_to(np.arange(len(stations), dtype=np.int32)[:, None], present.shape)[valid]
        day_hist = np.bincount(station_index * 101 + ob_int, minlength=len(stations) * 101).reshape(len(stations), 101)
        for i, station_value in enumerate(stations):
            st = int(station_value)
            station_hist[st] += day_hist[i]
            if counts_by_station[i]:
                station_days[st].add(day)
                station_freeways[st].add(str(data['freeway'][i]))
                station_directions[st].add(str(data['direction'][i]))
            idx = np.flatnonzero(valid[i])
            if len(idx):
                quality = np.where(observed[i, idx] == 0, 0, np.where(observed[i, idx] >= 90, 2, 1))
                station_transitions[st] += int(np.count_nonzero((np.diff(idx) == 1) & (((quality[:-1] == 0) & (quality[1:] == 2)) | ((quality[:-1] == 2) & (quality[1:] == 0)))))
                old = quality_last.get(st)
                if old and date.fromisoformat(day) - date.fromisoformat(old[0]) == timedelta(days=1) and old[1] == old[2] - 1 and idx[0] == 0 and {old[3], int(quality[0])} == {0, 2}:
                    station_transitions[st] += 1
                quality_last[st] = (day, int(idx[-1]), present.shape[1], int(quality[-1]))
            fd_key = (str(data['freeway'][i]), str(data['direction'][i]))
            fda = fd_acc[fd_key]
            fda['stations'].add(st)
            fda['rows'] += int(counts_by_station[i])
            fda['zero'] += int(day_hist[i, 0])
            fda['ge80'] += int(day_hist[i, 80:].sum())
            fda['ge90'] += int(day_hist[i, 90:].sum())
            fda['eq100'] += int(day_hist[i, 100])
        day_counts = Counter()
        day_counts['ML_rows'] = day_n
        day_counts['observed_missing'] = day_n - int(valid.sum())
        day_counts['zero'] = int(np.count_nonzero(valid & (observed == 0)))
        day_counts['below50'] = int(np.count_nonzero(valid & (observed < 50)))
        day_counts['below80'] = int(np.count_nonzero(valid & (observed < 80)))
        day_counts['ge80'] = int(np.count_nonzero(valid & (observed >= 80)))
        day_counts['ge90'] = int(np.count_nonzero(valid & (observed >= 90)))
        day_counts['eq100'] = int(np.count_nonzero(valid & (observed == 100)))
        month_acc[month].update(day_counts)
        daily_rows.append(dict(date=day, ML_rows=day_n, pct_observed_zero=pct(day_counts['zero'], day_n), pct_observed_ge_80=pct(day_counts['ge80'], day_n), pct_observed_ge_90=pct(day_counts['ge90'], day_n), pct_observed_100=pct(day_counts['eq100'], day_n), observed_missing=day_counts['observed_missing']))
        for label, predicate in BINS:
            mask = valid & predicate(observed)
            counts = mask.sum(axis=1)
            add_coverage(ensure_acc(bin_acc, label), counts, stations, day, data['freeway'], data['direction'])
            stable_counts = counts.copy()
            stable_counts[~stable_rows] = 0
            add_coverage(ensure_acc(stable_bin_acc, label), stable_counts, stations, day, data['freeway'], data['direction'])
        for label, predicate in SAMPLE_BINS:
            mask = valid & predicate(observed)
            vals = data['samples'][mask]
            finite = vals[np.isfinite(vals)]
            count_hist(sample_hist[label], finite)
            sample_counts[label]['rows'] += int(mask.sum())
            sample_counts[label]['non_null'] += len(finite)
            sample_counts[label]['zero_samples'] += int(np.count_nonzero(finite == 0))
        for group, group_mask in [('zero', valid & (observed == 0)), ('ge90', valid & (observed >= 90))]:
            for field in ('speed', 'flow', 'occupancy'):
                vals = data[field][group_mask]
                finite = vals[np.isfinite(vals)]
                count_hist(variable_hist[(group, field)], finite)
                variable_counts[(group, field)]['rows'] += int(group_mask.sum())
                variable_counts[(group, field)]['non_null'] += len(finite)
        run_audit(data, None, run_state, run_stats)
        if previous is not None:
            evaluate_targets(previous, data, threshold_acc, target_acc, input_acc, station_eligible, stable_ids, target_day_summary)
        previous = data
    if previous is not None:
        evaluate_targets(previous, None, threshold_acc, target_acc, input_acc, station_eligible, stable_ids, target_day_summary)
    for key, run in run_state.items():
        record_run(key, run, run_stats)
    summarize(official, items, ml_rows, stable_ml_rows, all_stations, stable_ids, bin_acc, stable_bin_acc, month_acc, daily_rows, station_hist, station_days, station_freeways, station_directions, station_transitions, fd_acc, sample_hist, sample_counts, variable_hist, variable_counts, run_stats, threshold_acc, target_acc, input_acc, station_eligible, target_day_summary, identity_issues)

def summarize(official, items, ml_rows, stable_ml_rows, all_stations, stable_ids, bin_acc, stable_bin_acc, month_acc, daily_rows, station_hist, station_days, station_freeways, station_directions, station_transitions, fd_acc, sample_hist, sample_counts, variable_hist, variable_counts, run_stats, threshold_acc, target_acc, input_acc, station_eligible, target_day_summary, identity_issues):
    overall_rows = []
    for label, _ in BINS:
        acc = ensure_acc(bin_acc, label)
        overall_rows.append(dict(percent_observed_bin=label, rows=acc['n'], percentage=pct(acc['n'], ml_rows), unique_stations=len(acc['stations']), unique_days=len(acc['days']), unique_freeways=len(acc['freeways'])))
    s.write_csv(s.OUT / 'percent_observed_global_distribution.csv', overall_rows, ['percent_observed_bin', 'rows', 'percentage', 'unique_stations', 'unique_days', 'unique_freeways'])
    if sum(row['rows'] for row in overall_rows) != ml_rows:
        raise RuntimeError('Global % Observed bins do not close to ML rows')
    month_rows = []
    for month, counts in sorted(month_acc.items()):
        n = counts['ML_rows']
        month_rows.append(dict(month=month, total_ML_rows=n, pct_observed_zero=pct(counts['zero'], n), pct_observed_below_50=pct(counts['below50'], n), pct_observed_below_80=pct(counts['below80'], n), pct_observed_ge_80=pct(counts['ge80'], n), pct_observed_ge_90=pct(counts['ge90'], n), pct_observed_100=pct(counts['eq100'], n), missing_observed_rows=counts['observed_missing']))
    s.write_csv(s.OUT / 'percent_observed_by_month.csv', month_rows, list(month_rows[0]))
    month_median = {m['month']: statistics.median(row['pct_observed_zero'] for row in daily_rows if row['date'].startswith(m['month'])) for m in month_rows}
    for i, row in enumerate(daily_rows):
        row['zero_pct_change_previous_day_pp'] = round(row['pct_observed_zero'] - daily_rows[i-1]['pct_observed_zero'], 6) if i else ''
        row['zero_pct_difference_month_median_pp'] = round(row['pct_observed_zero'] - month_median[row['date'][:7]], 6)
    s.write_csv(s.OUT / 'percent_observed_by_day.csv', daily_rows, list(daily_rows[0]))
    station_rows = []
    for st in sorted(all_stations):
        hist = station_hist[st]
        n = int(hist.sum())
        exact_hist = {float(i): int(v) for i, v in enumerate(hist) if v}
        zero = int(hist[0]); high = int(hist[90:].sum())
        station_rows.append(dict(station=st, N=n, days_present=len(station_days[st]), freeways=';'.join(sorted(station_freeways[st])), directions=';'.join(sorted(station_directions[st])), mean_percent_observed=float(np.dot(np.arange(101), hist) / n) if n else '', median=hist_quantile(exact_hist, .5), P10=hist_quantile(exact_hist, .1), P25=hist_quantile(exact_hist, .25), P75=hist_quantile(exact_hist, .75), P90=hist_quantile(exact_hist, .9), pct_zero=pct(zero, n), pct_below_50=pct(int(hist[:50].sum()), n), pct_below_80=pct(int(hist[:80].sum()), n), pct_ge_80=pct(int(hist[80:].sum()), n), pct_ge_90=pct(high, n), pct_100=pct(int(hist[100]), n), zero_to_high_adjacent_transitions=station_transitions[st], profile='ALL_ZERO' if zero == n else 'ALL_GE90' if high == n else 'ZERO_HIGH_TRANSITIONS' if station_transitions[st] > 0 else 'MIXED_OR_INTERMEDIATE', metadata_stable=st in stable_ids))
    s.write_csv(s.OUT / 'percent_observed_by_station.csv', station_rows, list(station_rows[0]))
    fd_rows = []
    for (freeway, direction), acc in sorted(fd_acc.items()):
        n = acc['rows']
        fd_rows.append(dict(Fwy=freeway, Dir=direction, stations=len(acc['stations']), rows=n, pct_zero=pct(acc['zero'], n), pct_ge_80=pct(acc['ge80'], n), pct_ge_90=pct(acc['ge90'], n), pct_100=pct(acc['eq100'], n)))
    s.write_csv(s.OUT / 'percent_observed_by_freeway_direction.csv', fd_rows, list(fd_rows[0]))
    sample_rows = []
    for label, _ in SAMPLE_BINS:
        hist = sample_hist[label]
        n = sample_counts[label]['non_null']
        sample_rows.append(dict(percent_observed_bin=label, rows=sample_counts[label]['rows'], samples_non_null=n, samples_non_null_pct=pct(n, sample_counts[label]['rows']), samples_median=hist_quantile(hist, .5), samples_P10=hist_quantile(hist, .1), samples_P90=hist_quantile(hist, .9), zero_samples_pct=pct(sample_counts[label]['zero_samples'], n)))
    s.write_csv(s.OUT / 'percent_observed_vs_samples.csv', sample_rows, list(sample_rows[0]))
    variable_rows = []
    for group in ('zero', 'ge90'):
        for field in ('speed', 'flow', 'occupancy'):
            hist = variable_hist[(group, field)]
            counts = variable_counts[(group, field)]
            n = counts['non_null']
            total = counts['rows']
            mean = sum(v * c for v, c in hist.items()) / n if n else None
            variance = sum((v - mean) ** 2 * c for v, c in hist.items()) / n if n else None
            variable_rows.append(dict(observation_group=group, field=field, rows=total, non_null_N=n, non_null_pct=pct(n, total), min=min(hist) if hist else '', P10=hist_quantile(hist, .1), median=hist_quantile(hist, .5), P90=hist_quantile(hist, .9), max=max(hist) if hist else '', mean=mean, std=math.sqrt(variance) if variance is not None else ''))
    s.write_csv(s.OUT / 'zero_observed_variable_comparison.csv', variable_rows, list(variable_rows[0]))
    run_rows = [dict(station=st, field=field, **stats) for (st, field), stats in sorted(run_stats.items())]
    s.write_csv(s.OUT / 'perfect_repeat_runs_by_station.csv', run_rows, ['station', 'field', 'runs_ge_30min', 'runs_ge_60min', 'runs_ge_120min', 'longest_run_minutes', 'first_example_date'])
    s.write_csv(s.OUT / 'station_identity_issues.csv', identity_issues, ['date', 'duplicate_station_time_keys', 'station_identity_variants'])
    s.write_csv(s.OUT / 'forecast_target_alignment_by_day.csv', target_day_summary, ['date', 'horizon_minutes', 'origin_rows', 'aligned_targets', 'missing_targets'])
    target_rows = []
    threshold_rows = []
    input_rows = []
    for horizon in (30, 60):
        aligned = sum(x['aligned_targets'] for x in target_day_summary if x['horizon_minutes'] == horizon)
        for label, _ in BINS:
            acc = ensure_acc(target_acc, (horizon, label))
            target_rows.append(dict(horizon_minutes=horizon, percent_observed_bin=label, **coverage_row(acc), percentage_of_aligned=pct(acc['n'], aligned)))
        if sum(x['N'] for x in target_rows if x['horizon_minutes'] == horizon) != aligned:
            raise RuntimeError(f'Target % Observed bins do not close for H{horizon}')
        for scope in ('ALL', 'STABLE'):
            for threshold, _ in THRESHOLDS:
                acc = ensure_acc(threshold_acc, (scope, horizon, threshold))
                threshold_rows.append(dict(scope=scope, horizon_minutes=horizon, target_observed_threshold=threshold, **coverage_row(acc)))
            for input_bin, _ in INPUT_BINS:
                acc = ensure_acc(input_acc, (scope, horizon, input_bin))
                input_rows.append(dict(scope=scope, horizon_minutes=horizon, input_percent_observed_bin=input_bin, target_threshold='ge90', **coverage_row(acc)))
    s.write_csv(s.OUT / 'forecast_target_percent_observed_distribution.csv', target_rows, ['horizon_minutes', 'percent_observed_bin', 'N', 'percentage_of_aligned', 'unique_stations', 'unique_station_days', 'unique_days', 'unique_freeways', 'unique_directions'])
    s.write_csv(s.OUT / 'ground_truth_threshold_sensitivity.csv', threshold_rows, ['scope', 'horizon_minutes', 'target_observed_threshold', 'N', 'unique_stations', 'unique_station_days', 'unique_days', 'unique_freeways', 'unique_directions'])
    s.write_csv(s.OUT / 'candidate_design_C_input_strata.csv', input_rows, ['scope', 'horizon_minutes', 'input_percent_observed_bin', 'target_threshold', 'N', 'unique_stations', 'unique_station_days', 'unique_days', 'unique_freeways', 'unique_directions'])
    availability_rows = []
    availability_distribution = []
    for horizon in (30, 60):
        for st in sorted(all_stations):
            item = station_eligible[(horizon, st)]
            availability_rows.append(dict(station=st, horizon_minutes=horizon, metadata_stable=st in stable_ids, target_ge90_eligible_samples=item['count'], days_with_eligible_target=len(item['days'])))
        for scope, station_set in [('ALL', all_stations), ('STABLE', all_stations & stable_ids)]:
            values = np.array([station_eligible[(horizon, st)]['count'] for st in station_set], dtype=np.int64)
            days = np.array([len(station_eligible[(horizon, st)]['days']) for st in station_set], dtype=np.int64)
            availability_distribution.append(dict(scope=scope, horizon_minutes=horizon, stations=len(station_set), stations_with_eligible_target=int(np.count_nonzero(values)), eligible_samples_P10=float(np.quantile(values, .1)), eligible_samples_P25=float(np.quantile(values, .25)), eligible_samples_median=float(np.quantile(values, .5)), eligible_samples_P75=float(np.quantile(values, .75)), eligible_samples_P90=float(np.quantile(values, .9)), eligible_days_P10=float(np.quantile(days, .1)), eligible_days_P25=float(np.quantile(days, .25)), eligible_days_median=float(np.quantile(days, .5)), eligible_days_P75=float(np.quantile(days, .75)), eligible_days_P90=float(np.quantile(days, .9))))
    s.write_csv(s.OUT / 'station_high_observation_target_availability.csv', availability_rows, list(availability_rows[0]))
    s.write_csv(s.OUT / 'station_target_availability_distribution.csv', availability_distribution, list(availability_distribution[0]))
    stable_comparison = []
    for scope, source, denominator in [('ALL', bin_acc, ml_rows), ('STABLE', stable_bin_acc, stable_ml_rows)]:
        for label, _ in BINS:
            acc = ensure_acc(source, label)
            stable_comparison.append(dict(scope=scope, percent_observed_bin=label, rows=acc['n'], percentage=pct(acc['n'], denominator), unique_stations=len(acc['stations']), unique_days=len(acc['days']), unique_freeways=len(acc['freeways'])))
    s.write_csv(s.OUT / 'metadata_stable_station_comparison.csv', stable_comparison, list(stable_comparison[0]))
    threshold_lookup = {(r['scope'], r['horizon_minutes'], r['target_observed_threshold']): r for r in threshold_rows}
    input_lookup = {(r['scope'], r['horizon_minutes'], r['input_percent_observed_bin']): r for r in input_rows}
    gt30 = threshold_lookup[('ALL', 30, 'ge90')]
    gt60 = threshold_lookup[('ALL', 60, 'ge90')]
    zero_input_30 = input_lookup[('ALL', 30, '0')]
    zero_input_60 = input_lookup[('ALL', 60, '0')]
    high_input_30 = input_lookup[('ALL', 30, '100')]
    high_input_60 = input_lookup[('ALL', 60, '100')]
    if all(r['N'] >= 1_000_000 and r['unique_stations'] >= len(all_stations) * .5 and r['unique_days'] >= 200 and r['unique_freeways'] >= 5 for r in (gt30, gt60)):
        ground_truth = 'HIGH'
    elif all(r['N'] >= 100_000 and r['unique_stations'] >= 100 and r['unique_days'] >= 100 and r['unique_freeways'] >= 3 for r in (gt30, gt60)):
        ground_truth = 'MEDIUM'
    elif gt30['N'] and gt60['N']:
        ground_truth = 'LOW'
    else:
        ground_truth = 'FAIL'
    if all(r['N'] >= 100_000 and r['unique_stations'] >= 500 and r['unique_days'] >= 200 and r['unique_freeways'] >= 5 for r in (zero_input_30, zero_input_60)) and high_input_30['N'] >= 100_000 and high_input_60['N'] >= 100_000:
        jev = 'HIGH'
    elif all(r['N'] >= 10_000 and r['unique_stations'] >= 100 and r['unique_days'] >= 100 and r['unique_freeways'] >= 3 for r in (zero_input_30, zero_input_60)) and high_input_30['N'] and high_input_60['N']:
        jev = 'MEDIUM'
    elif all(r['N'] > 0 for r in (zero_input_30, zero_input_60, high_input_30, high_input_60)):
        jev = 'LOW'
    else:
        jev = 'FAIL'
    nonempty_bins = sum(ensure_acc(bin_acc, label)['n'] > 0 for label, _ in BINS)
    zero_pct = pct(ensure_acc(bin_acc, '0')['n'], ml_rows)
    hundred_pct = pct(ensure_acc(bin_acc, '100')['n'], ml_rows)
    intermediate_pct = pct(ml_rows - ensure_acc(bin_acc, '0')['n'] - ensure_acc(bin_acc, '100')['n'], ml_rows)
    input_variation = 'HIGH' if zero_pct >= 5 and hundred_pct >= 5 and intermediate_pct >= 1 else 'MEDIUM' if nonempty_bins >= 2 else 'LOW'
    feasibility_rows = [
        dict(dimension='INPUT_QUALITY_VARIATION', rating=input_variation, evidence=f'zero={zero_pct}%; 100={hundred_pct}%; intermediate={intermediate_pct}%; nonempty bins={nonempty_bins}'),
        dict(dimension='GROUND_TRUTH_FEASIBILITY', rating=ground_truth, evidence=f"H30>=90: {gt30['N']} rows/{gt30['unique_stations']} stations/{gt30['unique_days']} days/{gt30['unique_freeways']} freeways; H60>=90: {gt60['N']} rows/{gt60['unique_stations']} stations/{gt60['unique_days']} days/{gt60['unique_freeways']} freeways"),
        dict(dimension='JEV_DECISION_GATING_FEASIBILITY', rating=jev, evidence=f"0%-input to >=90 target: H30={zero_input_30['N']} rows/{zero_input_30['unique_stations']} stations/{zero_input_30['unique_days']} days; H60={zero_input_60['N']} rows/{zero_input_60['unique_stations']} stations/{zero_input_60['unique_days']} days. Out-of-sample errors remain uncomputed."),
    ]
    s.write_csv(s.OUT / 'step0b_feasibility.csv', feasibility_rows, ['dimension', 'rating', 'evidence'])
    zero_variable = next(r for r in variable_rows if r['observation_group'] == 'zero' and r['field'] == 'speed')
    aligned30 = sum(x['aligned_targets'] for x in target_day_summary if x['horizon_minutes'] == 30)
    aligned60 = sum(x['aligned_targets'] for x in target_day_summary if x['horizon_minutes'] == 60)
    month_zeros = [(r['month'], r['pct_observed_zero']) for r in month_rows]
    greatest_daily_changes = sorted((r for r in daily_rows[1:] if r['zero_pct_change_previous_day_pp'] != ''), key=lambda r: abs(r['zero_pct_change_previous_day_pp']), reverse=True)[:5]
    all_zero_stations = sum(r['profile'] == 'ALL_ZERO' for r in station_rows)
    all_high_stations = sum(r['profile'] == 'ALL_GE90' for r in station_rows)
    alternating_stations = sum(r['profile'] == 'ZERO_HIGH_TRANSITIONS' for r in station_rows)
    high_runs = sum(r['runs_ge_120min'] for r in run_rows)
    stable_zero_pct = next(r['percentage'] for r in stable_comparison if r['scope'] == 'STABLE' and r['percent_observed_bin'] == '0')
    risks = [
        f'{zero_pct}% of ML input rows have % Observed = 0; non-null speed is not direct-observation proof.',
        'Official sources support observed-versus-imputed semantics, but per-record Speed/Flow/Occupancy estimation lineage and exact Station 5-Minute formulas remain OFFICIAL_DEFINITION_INCOMPLETE.',
        f"H30 0%-input to >=90 target: {zero_input_30['N']:,} rows across {zero_input_30['unique_stations']} stations; H60: {zero_input_60['N']:,} rows across {zero_input_60['unique_stations']} stations. These are the directly relevant degraded-input cohorts.",
        f'{high_runs:,} zero-observation exact-value runs last at least 120 minutes across Speed/Flow/Occupancy combined; repetition alone does not identify imputation.',
    ]
    if identity_issues:
        risks.append(f'{len(identity_issues)} days have duplicate ML station-time keys or inconsistent station freeway/direction identity in the STEP 0B scan.')
    recommended = 'Review official-definition caveats and H30/H60 threshold sensitivity; then decide a target-quality policy and chronological study design. Do not freeze 200 stations or train models yet.'
    results = dict(canonical_raw_files=len(items), ML_rows=ml_rows, ML_stations=len(all_stations), stable_ML_stations=len(all_stations & stable_ids), percent_observed_zero_pct=zero_pct, percent_observed_ge80_pct=pct(sum(ensure_acc(bin_acc, k)['n'] for k in ('[80,90)', '[90,100)', '100')), ml_rows), percent_observed_ge90_pct=pct(sum(ensure_acc(bin_acc, k)['n'] for k in ('[90,100)', '100')), ml_rows), percent_observed_100_pct=hundred_pct, official_interpretation='0% means no 5-minute lane points classified as observed; non-null aggregate variables may be estimated. Exact per-record method unresolved.', speed_non_null_when_zero_pct=zero_variable['non_null_pct'], H30_aligned_targets=aligned30, H30_target_ge90=gt30['N'], H30_target_100=threshold_lookup[('ALL', 30, '100')]['N'], H60_aligned_targets=aligned60, H60_target_ge90=gt60['N'], H60_target_100=threshold_lookup[('ALL', 60, '100')]['N'], stations_H30_target_ge90=gt30['unique_stations'], stations_H60_target_ge90=gt60['unique_stations'], input_quality_variation=input_variation, ground_truth_feasibility=ground_truth, jev_decision_gating_feasibility=jev, critical_risks=risks, recommended_next_step=recommended)
    (s.OUT / 'Step0B_results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    s.write_csv(s.OUT / 'step0b_risks.csv', [dict(risk_number=i + 1, risk=issue) for i, issue in enumerate(risks)], ['risk_number', 'risk'])
    source_hourly = 'https://dot.ca.gov/-/media/dot-media/programs/research-innovation-system-information/documents/final-reports/ca22-task3253-a11y.pdf'
    source_sensor = 'https://dot.ca.gov/-/media/dot-media/programs/research-innovation-system-information/documents/final-reports/ca22-3141_final_reportv3-a11y.pdf'
    month_range = f"{min(v for _, v in month_zeros):.2f}%–{max(v for _, v in month_zeros):.2f}%"
    high_stable30 = threshold_lookup[('STABLE', 30, 'ge90')]
    high_stable60 = threshold_lookup[('STABLE', 60, 'ge90')]
    exact_stable30 = threshold_lookup[('STABLE', 30, '100')]
    exact_stable60 = threshold_lookup[('STABLE', 60, '100')]
    report = f'''# STEP 0B — % Observed semantics and ground-truth feasibility

## Scope and canonical files

The analysis reads only the 243 files in `canonical_243_files.csv`, one per day from 2026-01-01 through 2026-08-31. Four nonstandard `(1)` copies were SHA256-matched to their canonical counterparts and deleted at the user's request. `excluded_duplicate_files.csv` records them as `DUPLICATE_EXCLUDED_FROM_ANALYSIS`. Raw canonical files were not edited. No model, Jev call, label set, or final station selection was created.

## Official field semantics

A [Caltrans technical report]({source_hourly}) defines `% Observed` as the share of five-minute lane points actually observed rather than imputed. Its field table also defines Samples, Total Flow, Avg Occupancy, and Avg Speed, but it is a **Station Hour** table. Therefore exact Station 5-Minute formulas and units beyond the directly stated lane-point meaning remain **OFFICIAL_DEFINITION_INCOMPLETE**. A separate [Caltrans report]({source_sensor}) describes estimated values based on surrounding sensors as distinct from direct measurements. These sources support the possibility of imputed or estimated traffic values when `% Observed = 0`; they do not reveal the exact method or source for an individual Speed, Flow, or Occupancy cell. See `official_field_definition_audit.md` for each definition and its limit.

## ML observation quality

Canonical ML rows: **{ml_rows:,}**, ML stations: **{len(all_stations):,}**. `% Observed = 0`: **{ensure_acc(bin_acc, '0')['n']:,} ({zero_pct}%)**. `>=80`: **{results['percent_observed_ge80_pct']}%**; `>=90`: **{results['percent_observed_ge90_pct']}%**; `=100`: **{hundred_pct}%**. The zero-observation fraction by month ranges from **{month_range}**. Monthly and daily tables show every period; the largest absolute previous-day percentage-point changes are {', '.join(f"{r['date']} ({r['zero_pct_change_previous_day_pp']:+.2f} pp)" for r in greatest_daily_changes)}. These are rankings, not thresholded anomaly decisions.

Station profiles: {all_zero_stations:,} stations are zero-observed for every available ML row, {all_high_stations:,} are `>=90` for every row, and {alternating_stations:,} have at least one adjacent five-minute transition between `0` and `>=90`. Full station and freeway × direction distributions are in the CSV tables.

Samples and variables: among zero-observation rows, Speed non-null is **{zero_variable['non_null_pct']}%**. The paired Speed/Flow/Occupancy distributions for zero and `>=90` observation, and Samples quantiles by observation band, are in `zero_observed_variable_comparison.csv` and `percent_observed_vs_samples.csv`. These comparisons do not establish an imputation method or a causal effect.

Exact repeated-value runs under zero observation: **{high_runs:,}** Speed/Flow/Occupancy runs last at least 120 minutes. The station table also counts 30- and 60-minute runs. Exact repetition is a flag only, not proof of imputation.

## Input and target quality

At prediction time `t`, low `% Observed` can remain in a candidate degraded-input condition. The future `t+h` value is assessed separately as a candidate target. A non-null speed with low future observation is not automatically accepted as detector ground truth. An aligned target means the future station-time row exists and its `% Observed` is available; it does not certify an independent measurement.

H30 aligned targets: **{aligned30:,}**. H30 target `>=90`: **{gt30['N']:,}** across **{gt30['unique_stations']:,} stations, {gt30['unique_station_days']:,} station-days, {gt30['unique_days']} days, {gt30['unique_freeways']} freeways**. H30 target `=100`: **{threshold_lookup[('ALL', 30, '100')]['N']:,}**.

H60 aligned targets: **{aligned60:,}**. H60 target `>=90`: **{gt60['N']:,}** across **{gt60['unique_stations']:,} stations, {gt60['unique_station_days']:,} station-days, {gt60['unique_days']} days, {gt60['unique_freeways']} freeways**. H60 target `=100`: **{threshold_lookup[('ALL', 60, '100')]['N']:,}**.

`ground_truth_threshold_sensitivity.csv` compares `=100`, `>=90`, `>=80`, and `>0` without adopting any threshold. Candidate design A permits every input state and requires target `>=90`; design B requires target `=100`. Candidate design C stratifies input observation into 0, 1–49, 50–79, 80–89, 90–99, and 100 while retaining target `>=90`. The design-C matrix shows sample and coverage counts. No design is frozen.

## Metadata-stable cohort

**{len(all_stations & stable_ids):,}** canonical ML stations match the previous metadata-stable list. Their zero-observation share is **{stable_zero_pct}%**, versus **{zero_pct}%** in all ML stations. Under target `>=90`, stable stations provide H30 **{high_stable30['N']:,}** samples at **{high_stable30['unique_stations']}** stations and H60 **{high_stable60['N']:,}** samples at **{high_stable60['unique_stations']}** stations. Under target `=100`, H30/H60 provide **{exact_stable30['N']:,}/{exact_stable60['N']:,}** samples at **{exact_stable30['unique_stations']}/{exact_stable60['unique_stations']}** stations. `station_high_observation_target_availability.csv` reports eligible counts and days for every station; its companion table provides P10/P25/median/P75/P90 without a deletion threshold. No final 200-station set is selected.

## Go / No-Go assessment

**GROUND_TRUTH_FEASIBILITY: {ground_truth}. JEV_DECISION_GATING_FEASIBILITY: {jev}. INPUT_QUALITY_VARIATION: {input_variation}.** Ratings concern data structure only. Ground-truth HIGH requires both horizons to have at least one million `>=90` targets, at least half of ML stations, 200 days, and five freeways; MEDIUM requires 100,000 targets, 100 stations, 100 days, and three freeways. Jev HIGH additionally requires 100,000 `0`-input to `>=90` target cases at each horizon across 500 stations, 200 days, five freeways, plus 100,000 high-input cases; MEDIUM uses 10,000 cases, 100 stations, 100 days, three freeways. Smaller nonzero cohorts are LOW; absent cohorts are FAIL. These are audit breadth descriptors, not final sample-selection or training thresholds. Chronological out-of-sample forecast errors have not been computed; statistical independence is not established by time separation alone.

## Critical risks

{chr(10).join('- ' + risk for risk in risks)}

## Recommended next step

{recommended}
'''
    (s.OUT / 'Step0B_PercentObserved_and_GroundTruth_Audit.md').write_text(report, encoding='utf-8')
    terminal = f'''============================================================
STEP 0B — % OBSERVED / GROUND TRUTH AUDIT
============================================================
Canonical raw files:
243
ML rows:
{ml_rows}
ML stations:
{len(all_stations)}
Stable ML stations:
{len(all_stations & stable_ids)}
%Observed = 0:
{zero_pct}%
%Observed >=80:
{results['percent_observed_ge80_pct']}%
%Observed >=90:
{results['percent_observed_ge90_pct']}%
%Observed =100:
{hundred_pct}%
Official interpretation of %Observed:
0 means no 5-minute lane points classified as directly observed; non-null traffic values may be estimated. Per-record method unresolved.
Speed non-null when %Observed=0:
{zero_variable['non_null_pct']}%
H30 aligned targets:
{aligned30}
H30 target >=90:
{gt30['N']}
H30 target =100:
{threshold_lookup[('ALL', 30, '100')]['N']}
H60 aligned targets:
{aligned60}
H60 target >=90:
{gt60['N']}
H60 target =100:
{threshold_lookup[('ALL', 60, '100')]['N']}
Stations with H30 target >=90:
{gt30['unique_stations']}
Stations with H60 target >=90:
{gt60['unique_stations']}
Input-quality variation:
{input_variation}
GROUND_TRUTH_FEASIBILITY:
{ground_truth}
JEV_DECISION_GATING_FEASIBILITY:
{jev}
Critical risks:
{'; '.join(risks)}
Recommended next step:
{recommended}
============================================================'''
    (s.OUT / 'Step0B_final_terminal_summary.txt').write_text(terminal, encoding='utf-8')
    print(terminal)
