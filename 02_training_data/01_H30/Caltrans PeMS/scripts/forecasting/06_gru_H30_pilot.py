"""Fixed single-layer GRU H30 strong-model pilot, trained only on pilot train."""
from __future__ import annotations

import copy
import json
import statistics
import time
from pathlib import Path

import numpy as np
import psutil
import torch
from torch import nn
from torch.utils.data import DataLoader,TensorDataset

VARIABLES=('speed','flow','occupancy','observed_pct','samples')
CONTEXT=('time_of_day_sin','time_of_day_cos','day_of_week_sin','day_of_week_cos','is_weekend','lanes','station_length')


class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.gru=nn.GRU(input_size=5,hidden_size=64,num_layers=1,dropout=0,batch_first=True)
        self.head=nn.Sequential(nn.Linear(64+7,64),nn.ReLU(),nn.Linear(64,1))
    def forward(self,sequence,context):
        _,hidden=self.gru(sequence)
        return self.head(torch.cat((hidden[-1],context),dim=1)).squeeze(1)


def raw_sequence(frame):
    # Frozen lag00=t. Reversing produces chronological t-55 ... t.
    return np.stack([frame[[f'{v}_lag{i:02d}' for i in range(12)]].to_numpy(dtype=np.float32)[:,::-1]
                     for v in VARIABLES],axis=2).copy()


def context(frame):
    return frame[list(CONTEXT)].to_numpy(dtype=np.float32)


def fit(train,validation,output,max_runtime_seconds=900):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    np.random.seed(20260922);torch.manual_seed(20260922)
    torch.set_num_threads(6)
    device='cuda' if torch.cuda.is_available() else 'cpu'
    gpu_name=torch.cuda.get_device_name(0) if device=='cuda' else None
    seq_train=raw_sequence(train)
    means=np.nanmean(seq_train,axis=(0,1)).astype(np.float32)
    stds=np.nanstd(seq_train,axis=(0,1)).astype(np.float32)
    stds=np.where((stds>1e-8)&np.isfinite(stds),stds,1).astype(np.float32)
    if not np.isfinite(seq_train).all(): raise RuntimeError('GRU pilot requires explicit handling for missing sequence features')
    seq_train=(seq_train-means)/stds
    seq_val=raw_sequence(validation)
    if not np.isfinite(seq_val).all(): raise RuntimeError('GRU validation sequence has missing features')
    seq_val=(seq_val-means)/stds
    ctx_train=context(train);ctx_val=context(validation)
    if not np.isfinite(ctx_train).all() or not np.isfinite(ctx_val).all(): raise RuntimeError('GRU context has missing values')
    ytrain=train['target_speed'].to_numpy(dtype=np.float32)
    yval=validation['target_speed'].to_numpy(dtype=np.float32)
    (output/'gru_scaler.json').write_text(json.dumps(dict(variables=VARIABLES,mean=means.tolist(),std=stds.tolist(),
        fit_source='PILOT_TRAIN_ONLY',sequence_order='lag11_to_lag00',context_features=CONTEXT),indent=2),encoding='utf-8')
    train_ds=TensorDataset(torch.from_numpy(seq_train),torch.from_numpy(ctx_train),torch.from_numpy(ytrain))
    val_ds=TensorDataset(torch.from_numpy(seq_val),torch.from_numpy(ctx_val),torch.from_numpy(yval))
    batch_size=2048
    model=Model().to(device)
    optimizer=torch.optim.Adam(model.parameters(),lr=1e-3)
    criterion=nn.MSELoss()
    train_loader=DataLoader(train_ds,batch_size=batch_size,shuffle=True,generator=torch.Generator().manual_seed(20260922),num_workers=0)
    val_loader=DataLoader(val_ds,batch_size=4096,shuffle=False,num_workers=0)
    best_loss=float('inf');best_state=None;best_epoch=0;bad_epochs=0;seconds=[]
    start=time.perf_counter();peak_ram=psutil.Process().memory_info().rss/1e9
    runtime_limit=False
    for epoch in range(1,31):
        epoch_start=time.perf_counter();model.train()
        try:
            for xs,xc,y in train_loader:
                xs=xs.to(device);xc=xc.to(device);y=y.to(device)
                optimizer.zero_grad(set_to_none=True)
                loss=criterion(model(xs,xc),y)
                loss.backward();optimizer.step()
        except torch.OutOfMemoryError:
            if epoch>1 or batch_size==512: raise
            batch_size=1024 if batch_size==2048 else 512
            if device=='cuda': torch.cuda.empty_cache()
            train_loader=DataLoader(train_ds,batch_size=batch_size,shuffle=True,generator=torch.Generator().manual_seed(20260922),num_workers=0)
            continue
        model.eval(); val_sum=0.0; val_n=0
        with torch.inference_mode():
            for xs,xc,y in val_loader:
                pred=model(xs.to(device),xc.to(device))
                val_sum+=float(((pred-y.to(device))**2).sum().item());val_n+=len(y)
        val_loss=val_sum/val_n
        elapsed=time.perf_counter()-epoch_start;seconds.append(elapsed)
        peak_ram=max(peak_ram,psutil.Process().memory_info().rss/1e9)
        if val_loss < best_loss-1e-6:
            best_loss=val_loss;best_epoch=epoch;best_state=copy.deepcopy(model.state_dict());bad_epochs=0
        else: bad_epochs+=1
        if epoch>=3 and statistics.median(seconds)*30>max_runtime_seconds:
            runtime_limit=True;break
        if bad_epochs>=5:break
    training_seconds=time.perf_counter()-start
    model.load_state_dict(best_state);model.eval()
    model_path=output/'gru_H30_pilot.pt'
    torch.save(dict(state_dict=best_state,architecture=dict(input_size=5,hidden_size=64,num_layers=1,dropout=0,
                   head='Dense64-ReLU-Dense1',context_size=7),best_epoch=best_epoch,
                   train_source='PILOT_TRAIN_ONLY',early_stopping_source='PILOT_VALIDATION_ONLY'),model_path)
    def predict(frame):
        sequence=raw_sequence(frame)
        if not np.isfinite(sequence).all():raise RuntimeError('Missing GRU inference sequence values')
        sequence=(sequence-means)/stds
        ctx=context(frame)
        outputs=[]
        with torch.inference_mode():
            for i in range(0,len(frame),batch_size):
                xs=torch.from_numpy(sequence[i:i+batch_size]).to(device)
                xc=torch.from_numpy(ctx[i:i+batch_size]).to(device)
                outputs.append(model(xs,xc).cpu().numpy())
        if device=='cuda': torch.cuda.synchronize()
        return np.concatenate(outputs).astype(np.float32)
    info=dict(device=device,gpu_model=gpu_name,epochs_completed=len(seconds),best_epoch=best_epoch,
              batch_size=batch_size,seconds_per_epoch=seconds,seconds_per_epoch_median=statistics.median(seconds),
              estimated_30_epoch_time=statistics.median(seconds)*30,training_seconds=training_seconds,
              peak_ram_gb=peak_ram,peak_vram_gb=(torch.cuda.max_memory_allocated()/1e9 if device=='cuda' else None),
              model_size_MB=model_path.stat().st_size/1e6,runtime_limit=runtime_limit,
              scaler_fit_source='PILOT_TRAIN_ONLY',early_stopping_source='PILOT_VALIDATION_ONLY',
              validation_mse_best=best_loss)
    return predict,info
