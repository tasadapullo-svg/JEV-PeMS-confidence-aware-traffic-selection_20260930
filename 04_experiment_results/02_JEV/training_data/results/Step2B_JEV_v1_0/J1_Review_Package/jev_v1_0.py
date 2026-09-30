"""Frozen JEV v1.0 implementation. Mathematical structure is immutable."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import math
import platform

import numpy as np
import pandas as pd
import scipy
from scipy.optimize import minimize

VERSION = "1.0"
EVIDENCE_NAMES = ["Q", "S", "D", "C"]
LOWER_PERCENTILE = 5.0
UPPER_PERCENTILE = 95.0
EPSILON = 1e-6
Z_CLIP_MAX = 10.0
INITIAL_WEIGHTS = np.array([0.25, 0.25, 0.25, 0.25], dtype=float)
OPTIMIZER = "SLSQP"
CONFIDENCE_FORMULA = "margin * selected_Q"

SCALER_INPUTS = {
    "recent_observed_mean_60": ("recent_observed_mean_60", False),
    "recent_observed_min_60": ("recent_observed_min_60", False),
    "recent_missing_count_60": ("recent_missing_count_60", False),
    "train_candidate_observed_mean": ("train_candidate_observed_mean", False),
    "speed_std_60": ("speed_std_60", False),
    "speed_range_60": ("speed_range_60", False),
    "abs_speed_slope_60": ("speed_slope_60", True),
    "abs_speed_delta_15": ("speed_delta_15", True),
    "abs_speed_delta_30": ("speed_delta_30", True),
}


def _input_values(frame: pd.DataFrame, source: str, absolute: bool) -> np.ndarray:
    values = frame[source].to_numpy(dtype=float)
    return np.abs(values) if absolute else values


def fit_normalization(train: pd.DataFrame) -> tuple[dict, list[str]]:
    params = {}
    degenerate = []
    for name, (source, absolute) in SCALER_INPUTS.items():
        values = _input_values(train, source, absolute)
        finite = values[np.isfinite(values)]
        if not len(finite):
            raise RuntimeError(f"No finite Train values for JEV scaler: {name}")
        p05, p95 = np.percentile(finite, [LOWER_PERCENTILE, UPPER_PERCENTILE])
        is_degenerate = bool(p95 <= p05)
        if is_degenerate: degenerate.append(name)
        params[name] = {"source_feature": source, "absolute_value": absolute, "p05": float(p05), "p95": float(p95), "degenerate": is_degenerate, "fit_split": "train"}
    return params, degenerate


def robust_scale(values: np.ndarray, params: dict) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    if params["degenerate"]: return np.full(values.shape, 0.5, dtype=float)
    return np.clip((values - params["p05"]) / (params["p95"] - params["p05"]), 0.0, 1.0)


def compute_evidence(frame: pd.DataFrame, normalization: dict, tau_d: float) -> pd.DataFrame:
    scaled = {}
    for name, (source, absolute) in SCALER_INPUTS.items():
        scaled[name] = robust_scale(_input_values(frame, source, absolute), normalization[name])
    q = np.clip((scaled["recent_observed_mean_60"] + scaled["recent_observed_min_60"] + (1.0 - scaled["recent_missing_count_60"]) + scaled["train_candidate_observed_mean"]) / 4.0, 0.0, 1.0)
    s = np.clip(1.0 - (scaled["speed_std_60"] + scaled["speed_range_60"] + scaled["abs_speed_slope_60"] + scaled["abs_speed_delta_15"] + scaled["abs_speed_delta_30"]) / 5.0, 0.0, 1.0)
    if not np.isfinite(tau_d) or tau_d <= 0: raise RuntimeError("JEV tau_d must be finite and > 0")
    d = np.exp(-frame["abs_postmile_distance"].to_numpy(dtype=float) / tau_d)
    z = np.abs(frame["speed_lag00"].to_numpy(dtype=float) - frame["speed_mean_60"].to_numpy(dtype=float)) / (frame["speed_std_60"].to_numpy(dtype=float) + EPSILON)
    c = np.exp(-np.clip(z, 0.0, Z_CLIP_MAX))
    return pd.DataFrame({"Q": q, "S": s, "D": d, "C": c}, index=frame.index)


def relative_utility(train: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    utility = np.empty(len(train), dtype=float)
    ties = np.zeros(len(train), dtype=bool)
    positions = pd.Series(np.arange(len(train)), index=train.index)
    for _, group in train.groupby("sample_id", sort=False):
        losses = group["candidate_loss"].to_numpy(dtype=float)
        best, worst = float(losses.min()), float(losses.max())
        idx = positions.loc[group.index].to_numpy(dtype=int)
        if worst - best > 0:
            utility[idx] = 1.0 - (losses - best) / (worst - best)
        else:
            utility[idx] = 1.0; ties[idx] = True
    return utility, ties


def fit_jev(train: pd.DataFrame, freeze_hash: str) -> tuple[dict, pd.DataFrame, np.ndarray, np.ndarray]:
    normalization, degenerate = fit_normalization(train)
    tau_d = float(np.median(train["abs_postmile_distance"].to_numpy(dtype=float)))
    if tau_d <= 0: raise RuntimeError("JEV tau_d <= 0")
    evidence = compute_evidence(train, normalization, tau_d)
    utility, ties = relative_utility(train)
    matrix = evidence[EVIDENCE_NAMES].to_numpy(dtype=float)
    objective = lambda weights: float(np.mean((utility - matrix @ weights) ** 2))
    result = minimize(objective, INITIAL_WEIGHTS.copy(), method=OPTIMIZER, bounds=[(0.0, 1.0)] * 4, constraints=[{"type": "eq", "fun": lambda weights: float(np.sum(weights) - 1.0)}], options={"ftol": 1e-12, "maxiter": 1000, "disp": False})
    raw_weights = np.asarray(result.x, dtype=float)
    if not result.success: raise RuntimeError(f"JEV SLSQP failed: {result.message}")
    if abs(float(raw_weights.sum()) - 1.0) > 1e-8 or np.any(raw_weights < -1e-10): raise RuntimeError("JEV fitted weight constraints failed")
    adjusted = bool(np.any(raw_weights < 0.0) or not np.isclose(raw_weights.sum(), 1.0, atol=1e-15))
    weights = np.clip(raw_weights, 0.0, None)
    weights = weights / weights.sum()
    model = {
        "version": VERSION, "freeze_hash": freeze_hash,
        "feature_evidence_definitions": {"Q": "frozen quality average", "S": "frozen inverse adverse stability average", "D": "exp(-distance/tau_d)", "C": "exp(-clipped standardized current-speed deviation)"},
        "normalization": normalization, "degenerate_features": degenerate, "tau_d": tau_d,
        "weights": dict(zip(EVIDENCE_NAMES, map(float, weights))),
        "optimizer": {"name": OPTIMIZER, "success": bool(result.success), "status": int(result.status), "message": str(result.message), "iterations": int(result.nit), "objective": float(result.fun), "initial_weights": INITIAL_WEIGHTS.tolist(), "floating_adjustment_applied": adjusted, "raw_weights": raw_weights.tolist()},
        "software_versions": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "scipy": scipy.__version__},
        "fitting_timestamp_utc": datetime.now(timezone.utc).isoformat(), "train_candidate_rows": int(len(train)), "train_target_times": int(train["sample_id"].nunique()), "test_status": "HELD_OUT_NOT_LOADED",
    }
    return model, evidence, utility, ties


def score(frame: pd.DataFrame, model: dict) -> pd.DataFrame:
    evidence = compute_evidence(frame, model["normalization"], float(model["tau_d"]))
    weights = np.array([model["weights"][name] for name in EVIDENCE_NAMES], dtype=float)
    evidence["jev_score"] = np.clip(evidence[EVIDENCE_NAMES].to_numpy(dtype=float) @ weights, 0.0, 1.0)
    return evidence


def rank_and_select(frame: pd.DataFrame, evidence: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    scored = frame.copy()
    for name in EVIDENCE_NAMES + ["jev_score"]: scored[name] = evidence[name].to_numpy(dtype=float)
    scored = scored.sort_values(["sample_id", "jev_score", "Q", "abs_postmile_distance", "candidate_station"], ascending=[True, False, False, True, True], kind="mergesort")
    scored["predicted_rank"] = scored.groupby("sample_id").cumcount() + 1
    prediction_rows = []
    for sample_id, group in scored.groupby("sample_id", sort=False):
        selected = group.iloc[0]; second = group.iloc[1]
        best = float(group["candidate_loss"].min()); worst = float(group["candidate_loss"].max()); spread = worst - best
        selected_loss = float(selected["candidate_loss"]); regret = max(0.0, selected_loss - best)
        top1, top2 = float(selected["jev_score"]), float(second["jev_score"]); margin = max(0.0, top1 - top2)
        confidence = margin * float(selected["Q"]); oracle_source = int(group.iloc[0]["oracle_source"])
        prediction_rows.append({"split": str(selected["split"]), "target_station": int(selected["target_station"]), "timestamp": str(selected["timestamp"]), "sample_id": str(sample_id), "method": "JEV v1.0", "selected_source": int(selected["candidate_station"]), "oracle_source": oracle_source, "selected_loss": selected_loss, "oracle_loss": best, "worst_loss": worst, "raw_regret_mph": regret, "normalized_regret": 0.0 if spread == 0 else regret / spread, "all_candidate_tie": spread == 0, "exact_top1_hit": int(selected["candidate_station"]) == oracle_source, "near_oracle_hit_0p5": regret <= 0.5 + 1e-12, "top2_hit": oracle_source in set(group.head(2)["candidate_station"].astype(int)), "jev_top1_score": top1, "jev_top2_score": top2, "jev_margin": margin, "jev_selected_Q": float(selected["Q"]), "jev_raw_confidence": confidence})
    score_columns = ["split", "target_station", "timestamp", "sample_id", "candidate_station", "candidate_rank", "Q", "S", "D", "C", "jev_score", "predicted_rank"]
    return pd.DataFrame(prediction_rows), scored[score_columns]


def distribution(values) -> dict:
    array = np.asarray(values, dtype=float)
    return {"N": int(len(array)), "mean": float(array.mean()), "median": float(np.median(array)), "min": float(array.min()), "max": float(array.max()), "p05": float(np.percentile(array, 5)), "p25": float(np.percentile(array, 25)), "p75": float(np.percentile(array, 75)), "p95": float(np.percentile(array, 95))}
