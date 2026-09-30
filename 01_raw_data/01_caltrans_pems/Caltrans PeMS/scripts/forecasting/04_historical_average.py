"""Train-only hierarchical historical average for the fixed H30 pilot."""
from __future__ import annotations

import time
from collections import Counter

import numpy as np
import pandas as pd


def fit(train):
    start=time.perf_counter()
    t=train[['station_id','day_of_week','hour','minute','target_speed']].copy()
    t['slot']=t['hour'].astype(int)*12+t['minute'].astype(int)//5
    exact=t.groupby(['station_id','day_of_week','slot'],sort=False)['target_speed'].mean()
    station_slot=t.groupby(['station_id','slot'],sort=False)['target_speed'].mean()
    station=t.groupby('station_id',sort=False)['target_speed'].mean()
    global_mean=float(t['target_speed'].mean())
    def predict(frame):
        fallback_counts=Counter()
        station_id=frame['station_id'].to_numpy()
        weekday=frame['day_of_week'].to_numpy()
        slot=frame['hour'].to_numpy(dtype=int)*12+frame['minute'].to_numpy(dtype=int)//5
        keys=pd.MultiIndex.from_arrays([station_id,weekday,slot],names=exact.index.names)
        values=exact.reindex(keys).to_numpy(dtype=np.float32).copy()
        fallback_counts['exact']+=int(np.isfinite(values).sum())
        missing=~np.isfinite(values)
        if missing.any():
            keys2=pd.MultiIndex.from_arrays([station_id[missing],slot[missing]],names=station_slot.index.names)
            vals2=station_slot.reindex(keys2).to_numpy(dtype=np.float32)
            values[missing]=vals2
            fallback_counts['station_slot']+=int(np.isfinite(vals2).sum())
        missing=~np.isfinite(values)
        if missing.any():
            vals3=station.reindex(station_id[missing]).to_numpy(dtype=np.float32)
            values[missing]=vals3
            fallback_counts['station_overall']+=int(np.isfinite(vals3).sum())
        missing=~np.isfinite(values)
        fallback_counts['global']+=int(missing.sum())
        values[missing]=global_mean
        detail['fallback_counts']=dict(fallback_counts)
        return values

    detail=dict(training_seconds=time.perf_counter()-start,device='CPU',model_size_MB=0.0,
                source='PILOT_TRAIN_ONLY',fallback_counts={})
    return predict,detail
