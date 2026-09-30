"""H30 persistence baseline: current speed predicts future speed."""
from __future__ import annotations

import numpy as np


def fit(_train):
    return lambda frame: frame['speed_lag00'].to_numpy(dtype=np.float32), {'training_seconds':0.0,'device':'CPU','model_size_MB':0.0}
