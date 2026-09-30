"""Fixed-parameter XGBoost H30 fast-model pilot."""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import psutil
import xgboost as xgb


def fit(train, validation, numeric_columns, output, prefer_cuda=True):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    categories={name:sorted(train[name].dropna().astype(str).unique().tolist()) for name in ('freeway','direction')}
    known={name:set(values) for name,values in categories.items()}
    def transform(frame):
        numeric=frame[numeric_columns].to_numpy(dtype=np.float32)
        blocks=[numeric]
        for name in ('freeway','direction'):
            values=frame[name].astype(str).to_numpy()
            cols=[(values==category).astype(np.float32)[:,None] for category in categories[name]]
            cols.append(np.array([v not in known[name] for v in values],dtype=np.float32)[:,None])
            blocks.extend(cols)
        return np.concatenate(blocks,axis=1)
    xtrain=transform(train);xval=transform(validation)
    ytrain=train['target_speed'].to_numpy(dtype=np.float32)
    yval=validation['target_speed'].to_numpy(dtype=np.float32)
    params=dict(objective='reg:squarederror',n_estimators=500,learning_rate=0.05,max_depth=8,
                min_child_weight=5,subsample=0.8,colsample_bytree=0.8,random_state=20260922,
                n_jobs=6,tree_method='hist',early_stopping_rounds=30)
    model=None; device='cpu'; fallback_reason=None
    start=time.perf_counter()
    for candidate in (['cuda','cpu'] if prefer_cuda else ['cpu']):
        try:
            model=xgb.XGBRegressor(**params,device=candidate)
            model.fit(xtrain,ytrain,eval_set=[(xval,yval)],verbose=False)
            device=candidate
            break
        except Exception as exc:
            fallback_reason=str(exc)
            if candidate=='cpu': raise
    training_seconds=time.perf_counter()-start
    model_path=output/'xgboost_H30_pilot.json'
    model.save_model(model_path)
    (output/'xgboost_encoder.json').write_text(json.dumps(dict(categories=categories,unknown_category='explicit one-hot column',
        fit_source='PILOT_TRAIN_ONLY',numeric_columns=numeric_columns),indent=2),encoding='utf-8')
    def predict(frame):
        return model.predict(transform(frame)).astype(np.float32)
    info=dict(training_seconds=training_seconds,device=device,model_size_MB=model_path.stat().st_size/1e6,
              peak_ram_gb=psutil.Process().memory_info().rss/1e9,best_iteration=int(model.best_iteration),
              category_fit_source='PILOT_TRAIN_ONLY',early_stopping_source='PILOT_VALIDATION_ONLY',
              cuda_fallback_reason=fallback_reason if device=='cpu' else None)
    return predict,info
