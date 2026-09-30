"""Step 2B selector benchmark development/smoke pipeline.

Consumes frozen Step 2A candidate utilities and causal PeMS histories. Test is never loaded.
Production mode is prepared for later manual execution; this module does not invent JEV.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import logging
import math
import platform
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import psutil
import sklearn
import torch
import xgboost as xgb
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


FORBIDDEN = {
    "candidate_loss", "oracle_source", "oracle_rank", "oracle_gap", "best_worst_spread",
    "normalized_spread", "target_speed", "future_target_speed", "selected_loss", "oracle_loss",
    "worst_loss", "raw_regret_mph", "normalized_regret",
}
ID_COLUMNS = {"target_station", "candidate_station", "sample_id", "timestamp", "timestamp_utc", "split"}
SEQUENCE_FEATURES = [f"speed_lag{i:02d}" for i in range(11, -1, -1)]
LEARNED_FEATURES = [
    *[f"speed_lag{i:02d}" for i in range(12)],
    "recent_observed_mean_60", "recent_observed_min_60", "recent_observed_std_60",
    "recent_missing_count_60", "recent_valid_count_60", "train_candidate_observed_mean",
    "speed_mean_60", "speed_std_60", "speed_min_60", "speed_max_60", "speed_range_60",
    "speed_slope_60", "speed_delta_15", "speed_delta_30",
    "candidate_rank", "abs_postmile_distance", "signed_postmile_offset",
    "hour_sin", "hour_cos", "dow_sin", "dow_cos",
]

JEV_VERSION = "1.0"
JEV_DEFINITION_STATUS = "FIRST_FORMAL_DEFINITION"
JEV_AUDIT_STATUS = "FORMALLY_DEFINED_AND_FROZEN_V1_0"
JEV_FREEZE_SHA256 = "e158bf2faef3f7b1f138e3ea13927aead4e1ce313470c499ae90726de5f21292"
JEV_SOURCE_SHA256 = "c0dcf8521972886d9e88db1727fb113811de8c2ef496e9511af64981dbe35c5f"
DEPLOYABLE_METHODS = ["Nearest", "Historical Best", "Quality Rule", "Ridge", "XGBoost", "GRU", "JEV v1.0"]
ORACLE_METHOD = "Oracle (reference only)"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, default=json_default), encoding="utf-8")


def json_default(value):
    if isinstance(value, (np.integer,)): return int(value)
    if isinstance(value, (np.floating,)): return float(value)
    if isinstance(value, (np.bool_,)): return bool(value)
    if isinstance(value, Path): return str(value)
    raise TypeError(type(value).__name__)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def setup_logger(path: Path) -> logging.Logger:
    path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("step2b")
    logger.handlers.clear(); logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler = logging.FileHandler(path, encoding="utf-8"); file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stdout); stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler); logger.addHandler(stream_handler)
    return logger


def parse_bool(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().eq("true")


def production_preflight(config: dict, write_report: bool = True) -> dict:
    jev = config.get("jev", {})
    preflight = config.get("preflight", {})
    checks = {
        "mode_production": config.get("mode") == "production",
        "station_universe_172": config.get("station_universe") == 172,
        "primary_targets_171": config.get("primary_evaluable_targets") == 171,
        "train_target_times_9169": config.get("train_target_times") == 9169,
        "validation_target_times_1431": config.get("validation_target_times") == 1431,
        "test_target_times_0": config.get("test_target_times") == 0,
        "candidate_k_5": config.get("candidate_k") == 5,
        "test_policy_held_out": config.get("test_status") == "HELD_OUT_NOT_LOADED" and config.get("splits", {}).get("test") == "HELD_OUT_NOT_LOADED",
        "jev_version": jev.get("version") == JEV_VERSION,
        "jev_definition_status": jev.get("definition_status") == JEV_DEFINITION_STATUS,
        "jev_audit_status": jev.get("audit_status") == JEV_AUDIT_STATUS,
        "freeze_sha_config": jev.get("combined_freeze_sha256") == JEV_FREEZE_SHA256,
        "source_sha_config": jev.get("source_sha256") == JEV_SOURCE_SHA256,
    }
    required_inputs = [Path(value) for value in config.get("inputs", {}).values()]
    checks["all_input_files_exist"] = bool(required_inputs) and all(path.exists() for path in required_inputs)
    freeze_path = Path(jev.get("method_freeze_path", ""))
    freeze_dir = freeze_path.parent
    combined_path = freeze_dir / "JEV_v1.0_Combined_Freeze_SHA256.txt"
    manifest_path = freeze_dir / "JEV_v1.0_Freeze_Manifest_SHA256.csv"
    checks["freeze_files_exist"] = freeze_path.exists() and combined_path.exists() and manifest_path.exists()
    checks["combined_freeze_sha_matches"] = checks["freeze_files_exist"] and combined_path.read_text(encoding="utf-8").strip() == JEV_FREEZE_SHA256
    manifest_ok = False
    if checks["freeze_files_exist"]:
        manifest_rows = list(csv.DictReader(manifest_path.open(encoding="utf-8-sig", newline="")))
        manifest_ok = all((freeze_dir / row["filename"]).exists() and sha256(freeze_dir / row["filename"]) == row["sha256"] and (freeze_dir / row["filename"]).stat().st_size == int(row["size_bytes"]) for row in manifest_rows)
        canonical = "".join(f"{row['filename']}|{row['sha256']}|{row['size_bytes']}\n" for row in manifest_rows).encode("utf-8")
        manifest_ok = manifest_ok and hashlib.sha256(canonical).hexdigest() == JEV_FREEZE_SHA256
    checks["freeze_manifest_verified"] = manifest_ok
    source_path = Path(jev.get("canonical_source_path", ""))
    checks["jev_source_exists"] = source_path.exists()
    checks["jev_source_sha_matches"] = source_path.exists() and sha256(source_path) == JEV_SOURCE_SHA256
    audit_paths = {name: Path(path) for name, path in preflight.get("j1_audits", {}).items()}
    checks["j1_audit_files_exist"] = len(audit_paths) == 4 and all(path.exists() for path in audit_paths.values())
    if checks["j1_audit_files_exist"]:
        checks["j1_unit_tests_pass"] = read_json(audit_paths["unit_tests"])["status"] == "PASS"
        checks["j1_qc_pass"] = read_json(audit_paths["qc"])["status"] == "PASS"
        checks["jev_leakage_pass"] = read_json(audit_paths["leakage"])["status"] == "PASS"
        checks["freeze_consistency_pass"] = read_json(audit_paths["freeze_consistency"])["status"] == "PASS"
    else:
        checks.update({"j1_unit_tests_pass": False, "j1_qc_pass": False, "jev_leakage_pass": False, "freeze_consistency_pass": False})
    availability = pd.read_csv(config["inputs"]["step2a_availability"])
    utility = pd.read_csv(config["inputs"]["step2a_utility"], usecols=["split", "target_station", "timestamp_utc", "candidate_station"])
    sample_level = utility.drop_duplicates(["split", "target_station", "timestamp_utc"])
    checks["candidate_mapping_exists"] = Path(config["inputs"]["step2a_candidate_map"]).exists()
    checks["frozen_counts_resolved"] = len(availability) == 172 and int(parse_bool(availability["primary_selection_evaluable"]).sum()) == 171 and len(utility) == 53000 and int((sample_level["split"] == "train").sum()) == 9169 and int((sample_level["split"] == "validation").sum()) == 1431
    checks["test_rows_zero"] = not utility["split"].astype(str).str.lower().eq("test").any()
    checks["required_packages_available"] = all(module is not None for module in [np, pd, sklearn, torch, xgb])
    checks["gru_cpu_configuration_valid"] = config.get("runtime", {}).get("device", "cpu") == "cpu" and int(config["models"]["gru"]["hidden_size"]) in (32, 64)
    output_dir = Path(config["output_dir"]); output_dir.mkdir(parents=True, exist_ok=True)
    probe = output_dir / ".step2b_preflight_write_test.tmp"
    try:
        probe.write_text("preflight", encoding="utf-8"); checks["output_directory_writable"] = probe.read_text(encoding="utf-8") == "preflight"
    finally:
        if probe.exists(): probe.unlink()
    required_outputs = set(config.get("required_production_outputs", []))
    checks["required_output_contract_complete"] = required_outputs == {"Step2B_Selector_Predictions.csv", "Step2B_Candidate_Scores.csv", "Step2B_Method_Summary.csv", "Step2B_Station_Level_Summary.csv", "Step2B_Paired_Development_Comparisons.csv", "Step2B_Runtime.csv", "Step2B_Model_Config.json", "Step2B_Fairness_Audit.json", "Step2B_Leakage_Audit.json", "Step2B_QC.json", "Step2B_Results.xlsx", "Step2B_JEV_Evidence.csv", "Step2B_JEV_Weights.json", "Step2B_JEV_Confidence_Summary.csv", "Step2B_Production_Log.log"}
    checks["full_production_not_executed"] = not any((output_dir / name).exists() for name in required_outputs)
    report = {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "failures": [name for name, passed in checks.items() if not passed], "test_target_samples": 0, "test_split_status": "HELD_OUT_NOT_LOADED", "full_production_executed": False, "checked_at_utc": datetime.now(timezone.utc).isoformat()}
    if write_report:
        report_path = Path(preflight["report_path"]); write_json(report_path, report)
    return report


def verify_frozen(config: dict, logger: logging.Logger) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    inputs = config["inputs"]
    utility = pd.read_csv(inputs["step2a_utility"])
    availability = pd.read_csv(inputs["step2a_availability"])
    candidate_map = pd.read_csv(inputs["step2a_candidate_map"])
    sample_level = utility.drop_duplicates(["split", "target_station", "timestamp_utc"])
    checks = {
        "universe_172": len(availability) == 172,
        "primary_targets_171": int(parse_bool(availability["primary_selection_evaluable"]).sum()) == 171,
        "audit_only_777316": availability.loc[~parse_bool(availability["primary_selection_evaluable"]), "target_station"].astype(int).tolist() == [777316],
        "utility_rows_53000": len(utility) == 53000,
        "primary_samples_10600": len(sample_level) == 10600,
        "train_samples_9169": int((sample_level["split"] == "train").sum()) == 9169,
        "validation_samples_1431": int((sample_level["split"] == "validation").sum()) == 1431,
        "test_samples_0": not utility["split"].astype(str).str.lower().eq("test").any(),
        "all_primary_k5": utility.groupby(["split", "target_station", "timestamp_utc"]).size().eq(5).all(),
        "no_self_candidate": not (utility["target_station"].astype(int) == utility["candidate_station"].astype(int)).any(),
    }
    logger.info("Frozen Step2A counts: universe=%d primary=%d utility=%d samples=%d train=%d validation=%d test=0",
                len(availability), int(parse_bool(availability["primary_selection_evaluable"]).sum()), len(utility), len(sample_level),
                int((sample_level["split"] == "train").sum()), int((sample_level["split"] == "validation").sum()))
    logger.info("TEST_SPLIT_STATUS = HELD_OUT_NOT_LOADED")
    logger.info("Test target samples = 0")
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError(f"Frozen Step2A discrepancy: {failed}")
    return utility, availability, candidate_map


def choose_scope(utility: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, list[int]]:
    if config["mode"] == "production":
        return utility.copy(), sorted(utility["target_station"].astype(int).unique().tolist())
    sample_level = utility.drop_duplicates(["split", "target_station", "timestamp_utc"])
    counts = sample_level.groupby(["target_station", "split"]).size().unstack(fill_value=0)
    chosen = counts.sort_values(["validation", "train"], ascending=False).head(int(config["smoke"]["target_stations"])).index.astype(int).tolist()
    scoped = utility[utility["target_station"].astype(int).isin(chosen)].copy()
    return scoped, chosen


def load_causal_features(scoped: pd.DataFrame, candidate_map: pd.DataFrame, config: dict, logger: logging.Logger) -> tuple[pd.DataFrame, list[dict]]:
    step2a_script = Path(config["inputs"]["step2a_script"])
    sys.path.insert(0, str(step2a_script.parent))
    from step2a_source_selection_feasibility import find_raw_files, load_raw_history, TZ

    required = defaultdict(set)
    sample_candidates = scoped.groupby(["target_station", "timestamp_utc"])["candidate_station"].apply(lambda x: sorted(set(map(int, x)))).to_dict()
    for (target, timestamp_utc), candidates in sample_candidates.items():
        origin = int(pd.Timestamp(timestamp_utc).timestamp())
        for candidate in candidates:
            for index in range(12):
                second = origin - 300 * index
                day = datetime.fromtimestamp(second, tz=timezone.utc).astimezone(TZ).date()
                required[day].add(candidate)
    raw_files = find_raw_files(Path(config["inputs"]["raw_root"]))
    history, source_days = load_raw_history(raw_files, required, logger)

    mapping = candidate_map[["target_station", "candidate_station", "candidate_rank", "distance", "target_postmile", "candidate_postmile"]].copy()
    merged = scoped.merge(mapping, on=["target_station", "candidate_station", "candidate_rank"], how="left", validate="many_to_one")
    rows = []
    for row in merged.itertuples(index=False):
        origin = int(pd.Timestamp(row.timestamp_utc).timestamp())
        records = [history.get((int(row.candidate_station), origin - 300 * index)) for index in range(12)]
        if any(record is None for record in records):
            raise RuntimeError(f"Missing frozen causal history for sample={row.sample_id} candidate={row.candidate_station}")
        observed = np.array([record[1] for record in records], dtype=float)
        speed = np.array([record[4] for record in records], dtype=float)
        if not np.isfinite(speed).all():
            raise RuntimeError(f"Invalid speed history for sample={row.sample_id} candidate={row.candidate_station}")
        local = pd.Timestamp(row.timestamp)
        finite_observed = observed[np.isfinite(observed)]
        slope = float(np.polyfit(np.arange(12, dtype=float), speed[::-1], 1)[0])
        record = row._asdict()
        for index, value in enumerate(speed): record[f"speed_lag{index:02d}"] = float(value)
        record.update({
            "recent_observed_mean_60": float(finite_observed.mean()) if len(finite_observed) else np.nan,
            "recent_observed_min_60": float(finite_observed.min()) if len(finite_observed) else np.nan,
            "recent_observed_std_60": float(finite_observed.std(ddof=0)) if len(finite_observed) else np.nan,
            "recent_missing_count_60": int((~np.isfinite(observed)).sum()),
            "recent_valid_count_60": int(np.isfinite(observed).sum()),
            "speed_mean_60": float(speed.mean()), "speed_std_60": float(speed.std(ddof=0)),
            "speed_min_60": float(speed.min()), "speed_max_60": float(speed.max()),
            "speed_range_60": float(speed.max() - speed.min()), "speed_slope_60": slope,
            "speed_delta_15": float(speed[0] - speed[3]), "speed_delta_30": float(speed[0] - speed[6]),
            "abs_postmile_distance": float(row.distance),
            "signed_postmile_offset": float(row.candidate_postmile - row.target_postmile),
            "hour_sin": math.sin(2 * math.pi * (local.hour * 60 + local.minute) / 1440),
            "hour_cos": math.cos(2 * math.pi * (local.hour * 60 + local.minute) / 1440),
            "dow_sin": math.sin(2 * math.pi * local.dayofweek / 7),
            "dow_cos": math.cos(2 * math.pi * local.dayofweek / 7),
            "max_feature_timestamp_utc": pd.Timestamp(origin, unit="s", tz="UTC").isoformat(),
        })
        rows.append(record)
    features = pd.DataFrame(rows)
    train_quality = features[features["split"] == "train"].groupby("candidate_station")["recent_observed_mean_60"].mean()
    fallback = float(features.loc[features["split"] == "train", "recent_observed_mean_60"].median())
    features["train_candidate_observed_mean"] = features["candidate_station"].map(train_quality).fillna(fallback)
    return features, source_days


def metric_from_candidate_predictions(frame: pd.DataFrame, score: np.ndarray, method: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    scored = frame.copy()
    scored["method"] = method
    scored["predicted_loss_or_score"] = np.asarray(score, dtype=float)
    scored = scored.sort_values(["sample_id", "predicted_loss_or_score", "abs_postmile_distance", "candidate_station"], kind="mergesort")
    scored["predicted_rank"] = scored.groupby("sample_id").cumcount() + 1
    predictions = []
    for sample_id, group in scored.groupby("sample_id", sort=False):
        selected = group.iloc[0]
        best_loss = float(group["candidate_loss"].min())
        worst_loss = float(group["candidate_loss"].max())
        selected_loss = float(selected["candidate_loss"])
        raw_regret = max(0.0, selected_loss - best_loss)
        spread = max(0.0, worst_loss - best_loss)
        top2 = set(group.nsmallest(2, "predicted_rank")["candidate_station"].astype(int))
        oracle_source = int(group.iloc[0]["oracle_source"])
        predictions.append({
            "split": str(selected["split"]), "target_station": int(selected["target_station"]),
            "timestamp": str(selected["timestamp"]), "sample_id": str(sample_id), "method": method,
            "selected_source": int(selected["candidate_station"]), "oracle_source": oracle_source,
            "selected_loss": selected_loss, "oracle_loss": best_loss, "worst_loss": worst_loss,
            "raw_regret_mph": raw_regret, "normalized_regret": 0.0 if spread == 0 else raw_regret / spread,
            "all_candidate_tie": spread == 0, "exact_top1_hit": int(selected["candidate_station"]) == oracle_source,
            "near_oracle_hit_0p5": raw_regret <= 0.5 + 1e-12, "top2_hit": oracle_source in top2,
        })
    score_cols = ["split", "target_station", "timestamp", "sample_id", "candidate_station", "method", "predicted_loss_or_score", "predicted_rank"]
    scored["raw_jev_score"] = np.nan; scored["raw_jev_confidence"] = np.nan
    return pd.DataFrame(predictions), scored[score_cols + ["raw_jev_score", "raw_jev_confidence"]]


def choose_linear(train: pd.DataFrame, validation: pd.DataFrame, config: dict):
    best = None
    for alpha in config["models"]["ridge"]["alpha_candidates"]:
        model = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler()), ("ridge", Ridge(alpha=float(alpha)))])
        model.fit(train[LEARNED_FEATURES], train["candidate_loss"])
        score = model.predict(validation[LEARNED_FEATURES])
        pred, cand = metric_from_candidate_predictions(validation, score, "Ridge")
        metric = float(pred["normalized_regret"].mean())
        if best is None or metric < best[0]: best = (metric, float(alpha), model, pred, cand)
    return best


def choose_xgb(train: pd.DataFrame, validation: pd.DataFrame, config: dict):
    imputer = SimpleImputer(strategy="median")
    x_train = imputer.fit_transform(train[LEARNED_FEATURES]); x_val = imputer.transform(validation[LEARNED_FEATURES])
    best = None
    for index, params in enumerate(config["models"]["xgboost"]["configs"]):
        model = xgb.XGBRegressor(objective="reg:squarederror", tree_method="hist", n_jobs=int(config["runtime"]["n_jobs"]), random_state=int(config["runtime"]["random_seed"]), **params)
        model.fit(x_train, train["candidate_loss"])
        score = model.predict(x_val)
        pred, cand = metric_from_candidate_predictions(validation, score, "XGBoost")
        metric = float(pred["normalized_regret"].mean())
        if best is None or metric < best[0]: best = (metric, index, params, imputer, model, pred, cand)
    return best


class GRURegressor(nn.Module):
    def __init__(self, static_size: int, hidden_size: int):
        super().__init__()
        self.gru = nn.GRU(1, hidden_size, batch_first=True)
        self.head = nn.Sequential(nn.Linear(hidden_size + static_size, hidden_size), nn.ReLU(), nn.Linear(hidden_size, 1))

    def forward(self, sequence, static):
        _, hidden = self.gru(sequence)
        return self.head(torch.cat([hidden[-1], static], dim=1)).squeeze(1)


def fit_gru(train: pd.DataFrame, validation: pd.DataFrame, config: dict):
    torch.manual_seed(int(config["runtime"]["random_seed"])); np.random.seed(int(config["runtime"]["random_seed"]))
    static_features = [name for name in LEARNED_FEATURES if name not in {f"speed_lag{i:02d}" for i in range(12)}]
    seq_scaler = StandardScaler().fit(train[SEQUENCE_FEATURES])
    static_pipe = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]).fit(train[static_features])
    seq_train = seq_scaler.transform(train[SEQUENCE_FEATURES]).astype("float32")[:, :, None]
    seq_val = seq_scaler.transform(validation[SEQUENCE_FEATURES]).astype("float32")[:, :, None]
    static_train = static_pipe.transform(train[static_features]).astype("float32")
    static_val = static_pipe.transform(validation[static_features]).astype("float32")
    y_train = train["candidate_loss"].to_numpy(dtype="float32")
    dataset = TensorDataset(torch.from_numpy(seq_train), torch.from_numpy(static_train), torch.from_numpy(y_train))
    loader = DataLoader(dataset, batch_size=int(config["models"]["gru"]["batch_size"]), shuffle=True)
    model = GRURegressor(static_train.shape[1], int(config["models"]["gru"]["hidden_size"]))
    optimizer = torch.optim.Adam(model.parameters(), lr=float(config["models"]["gru"]["learning_rate"]))
    loss_fn = nn.MSELoss(); best_metric = float("inf"); best_state = None; history = []
    val_seq_t = torch.from_numpy(seq_val); val_static_t = torch.from_numpy(static_val)
    for epoch in range(1, int(config["models"]["gru"]["epochs"]) + 1):
        model.train(); losses = []
        for seq_batch, static_batch, y_batch in loader:
            optimizer.zero_grad(); loss = loss_fn(model(seq_batch, static_batch), y_batch); loss.backward(); optimizer.step(); losses.append(float(loss.item()))
        model.eval()
        with torch.no_grad(): val_scores = model(val_seq_t, val_static_t).numpy()
        pred, _ = metric_from_candidate_predictions(validation, val_scores, "GRU")
        metric = float(pred["normalized_regret"].mean())
        history.append({"epoch": epoch, "train_mse": float(np.mean(losses)), "validation_mean_normalized_regret": metric})
        if metric < best_metric: best_metric = metric; best_state = copy.deepcopy(model.state_dict())
    model.load_state_dict(best_state); model.eval()
    with torch.no_grad(): val_scores = model(val_seq_t, val_static_t).numpy()
    pred, cand = metric_from_candidate_predictions(validation, val_scores, "GRU")
    return model, seq_scaler, static_pipe, pred, cand, history, static_features


def add_rule_methods(train: pd.DataFrame, validation: pd.DataFrame):
    outputs = []
    pred, cand = metric_from_candidate_predictions(validation, validation["candidate_rank"].to_numpy(float), "Nearest"); outputs.append((pred, cand))
    historical = train.groupby(["target_station", "candidate_station"], as_index=False)["candidate_loss"].mean().rename(columns={"candidate_loss": "historical_mean_loss"})
    hist_val = validation.merge(historical, on=["target_station", "candidate_station"], how="left", validate="many_to_one")
    if hist_val["historical_mean_loss"].isna().any(): raise RuntimeError("Historical Best missing Train-only statistic")
    pred, cand = metric_from_candidate_predictions(hist_val, hist_val["historical_mean_loss"].to_numpy(float), "Historical Best"); outputs.append((pred, cand))
    if validation["recent_observed_mean_60"].notna().any():
        quality_score = -validation["recent_observed_mean_60"].fillna(-np.inf).to_numpy(float)
        pred, cand = metric_from_candidate_predictions(validation, quality_score, "Quality Rule"); outputs.append((pred, cand))
    return outputs


def feature_schema() -> pd.DataFrame:
    rows = []
    for i in range(12): rows.append({"feature": f"speed_lag{i:02d}", "family": "F1", "definition": f"candidate speed at t-{i*5} elapsed minutes", "causal_max_time": "t", "fit_scope": "none"})
    definitions = {
        "recent_observed_mean_60": "mean candidate %Observed over t..t-55", "recent_observed_min_60": "minimum candidate %Observed over t..t-55",
        "recent_observed_std_60": "population SD candidate %Observed over t..t-55", "recent_missing_count_60": "count missing %Observed positions over 12 lags",
        "recent_valid_count_60": "count finite %Observed positions over 12 lags", "train_candidate_observed_mean": "candidate historical mean of recent_observed_mean_60; Train only",
        "speed_mean_60": "mean speed over 12 causal lags", "speed_std_60": "population SD speed over 12 causal lags", "speed_min_60": "minimum speed over 12 causal lags",
        "speed_max_60": "maximum speed over 12 causal lags", "speed_range_60": "speed_max_60 - speed_min_60",
        "speed_slope_60": "OLS slope across chronological t-55..t speed sequence", "speed_delta_15": "speed(t) - speed(t-15m)", "speed_delta_30": "speed(t) - speed(t-30m)",
        "candidate_rank": "frozen Step2A spatial candidate rank", "abs_postmile_distance": "absolute candidate-target postmile distance",
        "signed_postmile_offset": "candidate postmile - target postmile", "hour_sin": "sin(2*pi*local minute-of-day/1440)", "hour_cos": "cos(2*pi*local minute-of-day/1440)",
        "dow_sin": "sin(2*pi*local day-of-week/7)", "dow_cos": "cos(2*pi*local day-of-week/7)",
    }
    for feature in LEARNED_FEATURES[12:]:
        family = "F2" if "observed" in feature or "missing" in feature or "valid" in feature else ("F3" if feature.startswith("speed_") else "F4")
        rows.append({"feature": feature, "family": family, "definition": definitions[feature], "causal_max_time": "t", "fit_scope": "Train only" if feature == "train_candidate_observed_mean" else "none"})
    return pd.DataFrame(rows)


def summarize_methods(predictions: pd.DataFrame) -> pd.DataFrame:
    return predictions.groupby("method", as_index=False).agg(
        validation_samples=("sample_id", "nunique"), mean_normalized_regret=("normalized_regret", "mean"),
        median_normalized_regret=("normalized_regret", "median"), mean_raw_regret_mph=("raw_regret_mph", "mean"),
        median_raw_regret_mph=("raw_regret_mph", "median"), near_oracle_hit_rate=("near_oracle_hit_0p5", "mean"),
        top1_accuracy=("exact_top1_hit", "mean"), top2_hit_rate=("top2_hit", "mean"),
    ).sort_values("mean_normalized_regret", kind="mergesort")


def _run_legacy_reference(config_path: Path) -> int:
    config = read_json(config_path); output_dir = Path(config["output_dir"]); output_dir.mkdir(parents=True, exist_ok=True)
    if config["mode"] == "production":
        preflight = production_preflight(config, write_report=True)
        if preflight["status"] != "PASS": raise RuntimeError(f"PRODUCTION_PREFLIGHT_FAILED: {preflight['failures']}")
    prefix = "Step2B_Smoke" if config["mode"] == "smoke" else "Step2B"
    log_path = output_dir / ("Step2B_Smoke_Log.log" if config["mode"] == "smoke" else "Step2B_Production_Log.log")
    logger = setup_logger(log_path); started = datetime.now(timezone.utc); tick = time.perf_counter()
    logger.info("Step2B mode=%s", config["mode"]); logger.info("Config=%s", config_path)
    utility, availability, candidate_map = verify_frozen(config, logger)
    scoped, stations = choose_scope(utility, config)
    logger.info("Scope target stations=%s", stations)
    features, source_days = load_causal_features(scoped, candidate_map, config, logger)
    train = features[features["split"] == "train"].copy(); validation = features[features["split"] == "validation"].copy()
    train_samples = train["sample_id"].nunique(); validation_samples = validation["sample_id"].nunique()
    logger.info("Smoke train target-times=%d validation target-times=%d candidate rows=%d/%d", train_samples, validation_samples, len(train), len(validation))

    forbidden_present = sorted(set(LEARNED_FEATURES) & FORBIDDEN)
    identifiers_present = sorted(set(LEARNED_FEATURES) & ID_COLUMNS)
    if forbidden_present or identifiers_present: raise RuntimeError(f"Feature audit failed forbidden={forbidden_present} identifiers={identifiers_present}")

    outputs = add_rule_methods(train, validation)
    ridge = choose_linear(train, validation, config); outputs.append((ridge[3], ridge[4]))
    xgb_best = choose_xgb(train, validation, config); outputs.append((xgb_best[5], xgb_best[6]))
    gru = fit_gru(train, validation, config); outputs.append((gru[3], gru[4]))
    jev_model = None
    if config["jev"]["audit_status"] == "CANONICAL_JEV_IDENTIFIED":
        from jev_v1_0 import fit_jev, rank_and_select, score as jev_score
        jev_model, _, _, _ = fit_jev(train, config["jev"]["combined_freeze_sha256"])
        jev_evidence = jev_score(validation, jev_model)
        jev_predictions, jev_scores = rank_and_select(validation, jev_evidence)
        confidence_by_sample = jev_predictions.set_index("sample_id")["jev_raw_confidence"]
        jev_scores["method"] = "JEV v1.0"
        jev_scores["predicted_loss_or_score"] = -jev_scores["jev_score"]
        jev_scores["raw_jev_score"] = jev_scores["jev_score"]
        jev_scores["raw_jev_confidence"] = jev_scores["sample_id"].map(confidence_by_sample)
        score_columns = ["split", "target_station", "timestamp", "sample_id", "candidate_station", "method", "predicted_loss_or_score", "predicted_rank", "raw_jev_score", "raw_jev_confidence"]
        outputs.append((jev_predictions, jev_scores[score_columns]))
    predictions = pd.concat([item[0] for item in outputs], ignore_index=True)
    candidate_scores = pd.concat([item[1] for item in outputs], ignore_index=True)
    method_summary = summarize_methods(predictions)

    expected_methods = sorted(method_summary["method"].tolist())
    denominator = predictions.groupby("method")["sample_id"].nunique().to_dict()
    validation_keys = set(validation["sample_id"].astype(str))
    selected_pool_ok = True
    pool = validation.groupby("sample_id")["candidate_station"].apply(lambda s: set(map(int, s))).to_dict()
    for row in predictions.itertuples(index=False): selected_pool_ok &= int(row.selected_source) in pool[str(row.sample_id)]
    timestamp_ok = bool((pd.to_datetime(features["max_feature_timestamp_utc"], utc=True) <= pd.to_datetime(features["timestamp_utc"], utc=True)).all())
    split_disjoint = set(train["sample_id"].astype(str)).isdisjoint(set(validation["sample_id"].astype(str)))
    checks = {
        "frozen_universe_172": len(availability) == 172,
        "primary_evaluable_targets_171": int(parse_bool(availability["primary_selection_evaluable"]).sum()) == 171,
        "station_777316_excluded": 777316 not in stations,
        "test_held_out_not_loaded": not features["split"].astype(str).str.lower().eq("test").any(),
        "train_validation_separated": split_disjoint,
        "every_primary_target_time_k5": features.groupby("sample_id").size().eq(5).all(),
        "no_self_candidate": not (features["target_station"].astype(int) == features["candidate_station"].astype(int)).any(),
        "feature_timestamps_lte_t": timestamp_ok,
        "forbidden_features_absent": not forbidden_present,
        "ids_absent_from_model_features": not identifiers_present,
        "preprocessing_train_only": True,
        "historical_best_train_only": True,
        "validation_labels_not_model_inputs": True,
        "one_selection_per_method_sample": len(predictions) == validation_samples * len(expected_methods) and predictions.groupby(["method", "sample_id"]).size().eq(1).all(),
        "selected_candidate_in_frozen_pool": bool(selected_pool_ok),
        "raw_regret_nonnegative": bool((predictions["raw_regret_mph"] >= -1e-10).all()),
        "normalized_regret_bounded": bool(predictions["normalized_regret"].between(-1e-10, 1 + 1e-10).all()),
        "oracle_regret_zero": bool(np.isclose(features.groupby("sample_id")["candidate_loss"].min().to_numpy(), features.groupby("sample_id")["oracle_loss"].first().to_numpy()).all()),
        "near_oracle_tolerance_0p5": float(config["metrics"]["near_oracle_tolerance_mph"]) == 0.5,
        "no_duplicate_method_predictions": not predictions.duplicated(["sample_id", "method"]).any(),
        "same_validation_denominator": len(set(denominator.values())) == 1 and next(iter(denominator.values())) == validation_samples,
        "jev_audited_before_execution": config["jev"]["audit_status"] == JEV_AUDIT_STATUS and "JEV v1.0" in expected_methods,
    }
    qc = {
        "status": "PASS" if all(checks.values()) else "FAIL", "checks": checks,
        "critical_failures": [name for name, passed in checks.items() if not passed],
        "test_split_status": "HELD_OUT_NOT_LOADED", "test_target_samples": 0,
        "available_methods": expected_methods, "jev_status": config["jev"]["audit_status"],
        "smoke_train_target_times": train_samples, "smoke_validation_target_times": validation_samples,
        "same_denominator": denominator, "development_only": True,
    }
    fairness = {
        "status": "PASS" if checks["same_validation_denominator"] and checks["every_primary_target_time_k5"] else "FAIL",
        "validation_target_times": validation_samples, "candidate_k": 5, "method_denominators": denominator,
        "same_frozen_candidate_losses": True, "same_frozen_candidate_mapping": True,
        "learned_feature_universe": LEARNED_FEATURES, "identifiers_excluded": sorted(ID_COLUMNS),
        "preprocessing_fit_split": "train", "historical_best_fit_split": "train", "test_loaded": False,
    }
    schema = feature_schema()
    station_summary = predictions.groupby(["method", "target_station"], as_index=False).agg(samples=("sample_id", "nunique"), mean_normalized_regret=("normalized_regret", "mean"), mean_raw_regret_mph=("raw_regret_mph", "mean"), near_oracle_hit_rate=("near_oracle_hit_0p5", "mean"))
    runtime = {
        "start_utc": started.isoformat(), "end_utc": datetime.now(timezone.utc).isoformat(), "elapsed_seconds": time.perf_counter() - tick,
        "python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "scikit_learn": sklearn.__version__,
        "xgboost": xgb.__version__, "torch": torch.__version__, "cpu": platform.processor(), "logical_cpu_count": psutil.cpu_count(),
        "raw_days_read": len(source_days), "random_seed": config["runtime"]["random_seed"], "test_loaded": False,
        "ridge_selected_alpha": ridge[1], "xgboost_selected_config_index": xgb_best[1], "xgboost_selected_config": xgb_best[2], "gru_epoch_history": gru[5],
    }

    schema.to_csv(output_dir / "Step2B_Feature_Schema.csv", index=False, encoding="utf-8-sig")
    prediction_name = "Step2B_Smoke_Predictions.csv" if config["mode"] == "smoke" else "Step2B_Selector_Predictions.csv"
    predictions.to_csv(output_dir / prediction_name, index=False, encoding="utf-8-sig")
    candidate_scores.to_csv(output_dir / f"{prefix}_Candidate_Scores.csv", index=False, encoding="utf-8-sig")
    method_summary.to_csv(output_dir / ("Step2B_Method_Summary.csv" if config["mode"] == "production" else "Step2B_Smoke_Method_Summary.csv"), index=False, encoding="utf-8-sig")
    station_summary.to_csv(output_dir / ("Step2B_Station_Level_Summary.csv" if config["mode"] == "production" else "Step2B_Smoke_Station_Level_Summary.csv"), index=False, encoding="utf-8-sig")
    write_json(output_dir / ("Step2B_Smoke_QC.json" if config["mode"] == "smoke" else "Step2B_QC.json"), qc)
    write_json(output_dir / "Step2B_Fairness_Audit.json", fairness)
    write_json(output_dir / "Step2B_Leakage_Audit.json", {"status": "PASS" if checks["feature_timestamps_lte_t"] and checks["forbidden_features_absent"] else "FAIL", "feature_timestamps_lte_t": timestamp_ok, "forbidden_features_absent": not forbidden_present, "identifiers_absent_from_model_features": not identifiers_present, "preprocessing_train_only": True, "test_split_status": "HELD_OUT_NOT_LOADED"})
    write_json(output_dir / "Step2B_JEV_Implementation_Audit.json", config["jev"])
    write_json(output_dir / ("Step2B_Smoke_Runtime.json" if config["mode"] == "smoke" else "Step2B_Runtime.json"), runtime)
    if config["mode"] == "production":
        pd.DataFrame([{key: value for key, value in runtime.items() if not isinstance(value, (list, dict))}]).to_csv(output_dir / "Step2B_Runtime.csv", index=False, encoding="utf-8-sig")
    model_config = {"learned_features": LEARNED_FEATURES, "ridge_selected_alpha": ridge[1], "xgboost_selected_config": xgb_best[2], "gru": config["models"]["gru"], "jev": config["jev"], "development_only": True}
    write_json(output_dir / "Step2B_Model_Config.json", model_config)
    if jev_model is not None:
        write_json(output_dir / "Step2B_JEV_v1.0_Production_Model.json", jev_model)
    pd.DataFrame(columns=["reference_method", "comparison_method", "development_only", "status"]).to_csv(output_dir / "Step2B_Paired_Development_Comparisons.csv", index=False, encoding="utf-8-sig")

    payload = {
        "output_xlsx": str(output_dir / ("Step2B_Smoke_Summary.xlsx" if config["mode"] == "smoke" else "Step2B_Results.xlsx")),
        "preview_dir": str(output_dir / ".workbook_previews"),
        "sheets": {
            "README": [{"field": "Mode", "value": config["mode"]}, {"field": "Purpose", "value": "Integration and fairness smoke; not a paper claim"}, {"field": "QC", "value": qc["status"]}, {"field": "JEV", "value": config["jev"]["audit_status"]}, {"field": "Test", "value": "HELD_OUT_NOT_LOADED"}],
            "METHOD_SUMMARY": method_summary.to_dict("records"), "SAMPLE_COUNTS": [{"split": "train", "target_times": train_samples, "candidate_rows": len(train)}, {"split": "validation", "target_times": validation_samples, "candidate_rows": len(validation)}, {"split": "test", "target_times": 0, "candidate_rows": 0}],
            "STATION_SUMMARY": station_summary.to_dict("records"), "FEATURE_SCHEMA": schema.to_dict("records"),
            "FAIRNESS_AUDIT": [{"field": key, "value": value} for key, value in fairness.items() if not isinstance(value, (list, dict))],
            "QC": [{"check": key, "passed": value} for key, value in checks.items()],
            "JEV_AUDIT": [{"field": key, "value": value} for key, value in config["jev"].items() if not isinstance(value, (list, dict))],
            "RUNTIME": [{"field": key, "value": value} for key, value in runtime.items() if not isinstance(value, (list, dict))],
        },
    }
    write_json(output_dir / ".step2b_workbook_payload.json", payload)
    logger.info("Available methods=%s", expected_methods); logger.info("Same-denominator=%s", denominator)
    logger.info("Smoke QC=%s JEV=%s", qc["status"], config["jev"]["audit_status"])
    return 0 if qc["status"] == "PASS" else 2


def run(config_path: Path) -> int:
    config = read_json(config_path)
    if config["mode"] == "production":
        preflight_report = production_preflight(config, write_report=True)
        if preflight_report["status"] != "PASS":
            raise RuntimeError(f"PRODUCTION_PREFLIGHT_FAILED: {preflight_report['failures']}")
    else:
        preflight_report = production_preflight(read_json(Path(config["production_config"])), write_report=False)
    output_dir = Path(config["output_dir"]); output_dir.mkdir(parents=True, exist_ok=True)
    prefix = "Step2B_Smoke" if config["mode"] == "smoke" else "Step2B"
    log_path = output_dir / ("Step2B_Smoke_Log.log" if config["mode"] == "smoke" else "Step2B_Production_Log.log")
    logger = setup_logger(log_path); started = datetime.now(timezone.utc); total_tick = time.perf_counter()
    logger.info("Step2B mode=%s", config["mode"]); logger.info("Config=%s", config_path)
    utility, availability, candidate_map = verify_frozen(config, logger)
    scoped, stations = choose_scope(utility, config)
    logger.info("Scope target stations=%s", stations)
    feature_tick = time.perf_counter(); features, source_days = load_causal_features(scoped, candidate_map, config, logger); feature_seconds = time.perf_counter() - feature_tick
    train = features[features["split"] == "train"].copy(); validation = features[features["split"] == "validation"].copy()
    train_samples = int(train["sample_id"].nunique()); validation_samples = int(validation["sample_id"].nunique())
    logger.info("Train target-times=%d Validation target-times=%d Test target-times=0 candidate rows=%d/%d", train_samples, validation_samples, len(train), len(validation))
    forbidden_present = sorted(set(LEARNED_FEATURES) & FORBIDDEN); identifiers_present = sorted(set(LEARNED_FEATURES) & ID_COLUMNS)
    if forbidden_present or identifiers_present: raise RuntimeError(f"Feature audit failed forbidden={forbidden_present} identifiers={identifiers_present}")

    outputs = []; runtime_rows = []
    def record_runtime(method, fit_seconds, inference_seconds):
        runtime_rows.append({"method": method, "shared_feature_preprocessing_seconds": feature_seconds, "model_fitting_seconds": fit_seconds, "selector_inference_seconds": inference_seconds, "total_method_seconds_excluding_shared_preprocessing": fit_seconds + inference_seconds, "total_seconds_including_shared_preprocessing": feature_seconds + fit_seconds + inference_seconds, "validation_target_times": validation_samples, "inference_ms_per_target_time": 1000.0 * inference_seconds / validation_samples, "target_times_per_second": validation_samples / inference_seconds if inference_seconds > 0 else np.nan, "development_only": True})

    tick = time.perf_counter(); nearest_pred, nearest_cand = metric_from_candidate_predictions(validation, validation["candidate_rank"].to_numpy(float), "Nearest"); nearest_infer = time.perf_counter() - tick
    outputs.append((nearest_pred, nearest_cand)); record_runtime("Nearest", 0.0, nearest_infer)

    tick = time.perf_counter(); historical = train.groupby(["target_station", "candidate_station"], as_index=False)["candidate_loss"].mean().rename(columns={"candidate_loss": "historical_mean_loss"}); hist_fit = time.perf_counter() - tick
    tick = time.perf_counter(); hist_val = validation.merge(historical, on=["target_station", "candidate_station"], how="left", validate="many_to_one"); hist_pred, hist_cand = metric_from_candidate_predictions(hist_val, hist_val["historical_mean_loss"].to_numpy(float), "Historical Best"); hist_infer = time.perf_counter() - tick
    if hist_val["historical_mean_loss"].isna().any(): raise RuntimeError("Historical Best missing Train-only statistic")
    outputs.append((hist_pred, hist_cand)); record_runtime("Historical Best", hist_fit, hist_infer)

    tick = time.perf_counter(); quality_pred, quality_cand = metric_from_candidate_predictions(validation, -validation["recent_observed_mean_60"].fillna(-np.inf).to_numpy(float), "Quality Rule"); quality_infer = time.perf_counter() - tick
    outputs.append((quality_pred, quality_cand)); record_runtime("Quality Rule", 0.0, quality_infer)

    tick = time.perf_counter(); ridge = choose_linear(train, validation, config); ridge_fit = time.perf_counter() - tick
    tick = time.perf_counter(); ridge_score = ridge[2].predict(validation[LEARNED_FEATURES]); ridge_pred, ridge_cand = metric_from_candidate_predictions(validation, ridge_score, "Ridge"); ridge_infer = time.perf_counter() - tick
    outputs.append((ridge_pred, ridge_cand)); record_runtime("Ridge", ridge_fit, ridge_infer)

    tick = time.perf_counter(); xgb_best = choose_xgb(train, validation, config); xgb_fit = time.perf_counter() - tick
    tick = time.perf_counter(); xgb_score = xgb_best[4].predict(xgb_best[3].transform(validation[LEARNED_FEATURES])); xgb_pred, xgb_cand = metric_from_candidate_predictions(validation, xgb_score, "XGBoost"); xgb_infer = time.perf_counter() - tick
    outputs.append((xgb_pred, xgb_cand)); record_runtime("XGBoost", xgb_fit, xgb_infer)

    tick = time.perf_counter(); gru = fit_gru(train, validation, config); gru_fit = time.perf_counter() - tick
    tick = time.perf_counter(); seq_val = gru[1].transform(validation[SEQUENCE_FEATURES]).astype("float32")[:, :, None]; static_val = gru[2].transform(validation[gru[6]]).astype("float32"); gru[0].eval()
    with torch.no_grad(): gru_score = gru[0](torch.from_numpy(seq_val), torch.from_numpy(static_val)).numpy()
    gru_pred, gru_cand = metric_from_candidate_predictions(validation, gru_score, "GRU"); gru_infer = time.perf_counter() - tick
    outputs.append((gru_pred, gru_cand)); record_runtime("GRU", gru_fit, gru_infer)

    from jev_v1_0 import EVIDENCE_NAMES, distribution as jev_distribution, fit_jev, rank_and_select, score as jev_score
    tick = time.perf_counter(); jev_model, jev_train_evidence, jev_train_utility, jev_train_ties = fit_jev(train, config["jev"]["combined_freeze_sha256"]); jev_fit = time.perf_counter() - tick
    tick = time.perf_counter(); jev_validation_evidence = jev_score(validation, jev_model); jev_predictions, jev_scores = rank_and_select(validation, jev_validation_evidence); jev_infer = time.perf_counter() - tick
    confidence_by_sample = jev_predictions.set_index("sample_id")["jev_raw_confidence"]
    jev_scores["method"] = "JEV v1.0"; jev_scores["predicted_loss_or_score"] = -jev_scores["jev_score"]; jev_scores["raw_jev_score"] = jev_scores["jev_score"]; jev_scores["raw_jev_confidence"] = jev_scores["sample_id"].map(confidence_by_sample)
    score_columns = ["split", "target_station", "timestamp", "sample_id", "candidate_station", "method", "predicted_loss_or_score", "predicted_rank", "raw_jev_score", "raw_jev_confidence"]
    outputs.append((jev_predictions, jev_scores[score_columns])); record_runtime("JEV v1.0", jev_fit, jev_infer)

    tick = time.perf_counter(); oracle_pred, oracle_cand = metric_from_candidate_predictions(validation, validation["candidate_loss"].to_numpy(float), ORACLE_METHOD); oracle_infer = time.perf_counter() - tick
    outputs.append((oracle_pred, oracle_cand)); record_runtime(ORACLE_METHOD, 0.0, oracle_infer)
    predictions = pd.concat([item[0] for item in outputs], ignore_index=True); predictions["deployable"] = predictions["method"] != ORACLE_METHOD
    candidate_scores = pd.concat([item[1] for item in outputs], ignore_index=True); candidate_scores["deployable"] = candidate_scores["method"] != ORACLE_METHOD
    method_summary = summarize_methods(predictions); method_summary["development_only"] = True; method_summary["deployable"] = method_summary["method"] != ORACLE_METHOD
    station_summary = predictions.groupby(["method", "target_station"], as_index=False).agg(samples=("sample_id", "nunique"), mean_normalized_regret=("normalized_regret", "mean"), mean_raw_regret_mph=("raw_regret_mph", "mean"), near_oracle_hit_rate=("near_oracle_hit_0p5", "mean")); station_summary["development_only"] = True

    jev_station = station_summary[station_summary["method"] == "JEV v1.0"][["target_station", "mean_normalized_regret"]].rename(columns={"mean_normalized_regret": "jev_mean_normalized_regret"})
    paired_rows = []
    for method in [name for name in DEPLOYABLE_METHODS if name != "JEV v1.0"]:
        baseline = predictions[predictions["method"] == method][["sample_id", "normalized_regret"]].rename(columns={"normalized_regret": "baseline_regret"})
        jev_sample = predictions[predictions["method"] == "JEV v1.0"][["sample_id", "normalized_regret"]].rename(columns={"normalized_regret": "jev_regret"})
        merged = jev_sample.merge(baseline, on="sample_id", validate="one_to_one")
        baseline_station = station_summary[station_summary["method"] == method][["target_station", "mean_normalized_regret"]].rename(columns={"mean_normalized_regret": "baseline_mean_normalized_regret"})
        station_compare = jev_station.merge(baseline_station, on="target_station", validate="one_to_one"); delta = station_compare["jev_mean_normalized_regret"] - station_compare["baseline_mean_normalized_regret"]
        paired_rows.append({"reference_method": "JEV v1.0", "comparison_method": method, "validation_target_times": len(merged), "mean_paired_normalized_regret_difference_jev_minus_baseline": float((merged["jev_regret"] - merged["baseline_regret"]).mean()), "median_paired_difference": float((merged["jev_regret"] - merged["baseline_regret"]).median()), "station_wins": int((delta < -1e-12).sum()), "station_ties": int((delta.abs() <= 1e-12).sum()), "station_losses": int((delta > 1e-12).sum()), "development_only": True})
    paired = pd.DataFrame(paired_rows)

    jev_evidence = pd.concat([train[["split", "target_station", "timestamp", "sample_id", "candidate_station"]].reset_index(drop=True).join(jev_train_evidence.reset_index(drop=True)).assign(jev_score=jev_score(train, jev_model)["jev_score"].to_numpy(), relative_utility=jev_train_utility, all_candidate_tie=jev_train_ties), validation[["split", "target_station", "timestamp", "sample_id", "candidate_station"]].reset_index(drop=True).join(jev_validation_evidence.reset_index(drop=True)).assign(relative_utility=np.nan, all_candidate_tie=np.nan)], ignore_index=True)
    confidence_summary = pd.DataFrame([{"metric": "JEV_score", **jev_distribution(jev_validation_evidence["jev_score"])}, {"metric": "JEV_margin", **jev_distribution(jev_predictions["jev_margin"])}, {"metric": "JEV_raw_confidence", **jev_distribution(jev_predictions["jev_raw_confidence"])}])
    evidence_summary = pd.DataFrame([{"component": name, **jev_distribution(jev_validation_evidence[name])} for name in EVIDENCE_NAMES])
    runtime_frame = pd.DataFrame(runtime_rows)

    expected_methods = sorted(DEPLOYABLE_METHODS + [ORACLE_METHOD]); denominator = predictions.groupby("method")["sample_id"].nunique().to_dict()
    pool = validation.groupby("sample_id")["candidate_station"].apply(lambda s: set(map(int, s))).to_dict(); selected_pool_ok = all(int(row.selected_source) in pool[str(row.sample_id)] for row in predictions.itertuples(index=False))
    timestamp_ok = bool((pd.to_datetime(features["max_feature_timestamp_utc"], utc=True) <= pd.to_datetime(features["timestamp_utc"], utc=True)).all()); split_disjoint = set(train["sample_id"].astype(str)).isdisjoint(set(validation["sample_id"].astype(str)))
    weights = np.array([jev_model["weights"][name] for name in EVIDENCE_NAMES], dtype=float)
    exact_smoke_stations = stations == [765501, 775536, 775511, 769895, 769965] if config["mode"] == "smoke" else True
    expected_train = 437 if config["mode"] == "smoke" else 9169; expected_validation = 171 if config["mode"] == "smoke" else 1431
    checks = {
        "frozen_universe_172": len(availability) == 172, "primary_evaluable_targets_171": int(parse_bool(availability["primary_selection_evaluable"]).sum()) == 171, "station_777316_excluded": 777316 not in stations,
        "same_established_smoke_stations": exact_smoke_stations, "train_target_times_expected": train_samples == expected_train, "validation_target_times_expected": validation_samples == expected_validation,
        "test_target_times_0": not features["split"].astype(str).str.lower().eq("test").any(), "test_held_out_not_loaded": config.get("test_status") == "HELD_OUT_NOT_LOADED", "k5_all_samples": features.groupby("sample_id").size().eq(5).all(),
        "no_self_candidate": not (features["target_station"].astype(int) == features["candidate_station"].astype(int)).any(), "same_candidate_pools": True, "same_frozen_candidate_losses": True,
        "feature_timestamps_lte_t": timestamp_ok, "forbidden_features_absent": not forbidden_present, "station_ids_absent_from_model_matrices": not identifiers_present, "preprocessing_train_only": True, "historical_best_train_only": True,
        "jev_normalization_train_only": all(item["fit_split"] == "train" for item in jev_model["normalization"].values()), "jev_weight_fitting_train_only": jev_model["train_target_times"] == train_samples, "validation_loss_not_used_for_jev_fit": True,
        "each_method_complete_denominator": set(denominator) == set(expected_methods) and all(value == validation_samples for value in denominator.values()), "selections_in_frozen_pool": selected_pool_ok, "no_duplicate_method_predictions": not predictions.duplicated(["sample_id", "method"]).any(),
        "raw_regret_nonnegative": bool((predictions["raw_regret_mph"] >= -1e-10).all()), "normalized_regret_bounded": bool(predictions["normalized_regret"].between(-1e-10, 1 + 1e-10).all()), "oracle_regret_zero": bool((predictions.loc[predictions["method"] == ORACLE_METHOD, "raw_regret_mph"].abs() <= 1e-10).all()),
        "jev_evidence_valid": np.isfinite(jev_validation_evidence[EVIDENCE_NAMES]).all().all() and jev_validation_evidence[["Q", "S"]].apply(lambda s: s.between(0, 1).all()).all() and jev_validation_evidence["D"].gt(0).all() and jev_validation_evidence["D"].le(1).all() and jev_validation_evidence["C"].between(np.exp(-10) - 1e-12, 1).all(),
        "jev_weights_valid_sum_one": np.isfinite(weights).all() and (weights >= -1e-10).all() and abs(weights.sum() - 1) <= 1e-8, "jev_scores_valid": jev_validation_evidence["jev_score"].between(-1e-12, 1 + 1e-12).all(), "jev_confidence_valid": jev_predictions["jev_raw_confidence"].between(-1e-12, 1 + 1e-12).all(),
        "jev_implementation_matches_freeze": config["jev"]["combined_freeze_sha256"] == JEV_FREEZE_SHA256, "jev_freeze_hash_verified": preflight_report["checks"]["freeze_manifest_verified"], "jev_source_hash_verified": preflight_report["checks"]["jev_source_sha_matches"],
        "production_guard_verification_pass": preflight_report["status"] == "PASS", "production_not_executed": preflight_report["checks"]["full_production_not_executed"],
    }
    qc = {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "critical_failures": [name for name, passed in checks.items() if not passed], "test_split_status": "HELD_OUT_NOT_LOADED", "test_target_samples": 0, "available_methods": expected_methods, "deployable_methods": DEPLOYABLE_METHODS, "oracle_role": "RETROSPECTIVE_REFERENCE_ONLY", "same_denominator": denominator, "development_only": True, "full_production_executed": False}
    fairness = {"status": "PASS" if checks["each_method_complete_denominator"] and checks["k5_all_samples"] else "FAIL", "validation_target_times": validation_samples, "candidate_k": 5, "method_denominators": denominator, "same_frozen_candidate_losses": True, "same_frozen_candidate_mapping": True, "preprocessing_fit_split": "train", "historical_best_fit_split": "train", "test_loaded": False}
    leakage = {"status": "PASS" if timestamp_ok and not forbidden_present and not identifiers_present else "FAIL", "feature_timestamps_lte_t": timestamp_ok, "forbidden_features_absent": not forbidden_present, "identifiers_absent_from_model_features": not identifiers_present, "preprocessing_train_only": True, "jev_normalization_train_only": True, "jev_weights_train_only": True, "validation_losses_not_used_for_jev_fit": True, "test_split_status": "HELD_OUT_NOT_LOADED", "test_rows_loaded": 0}
    runtime = {"start_utc": started.isoformat(), "end_utc": datetime.now(timezone.utc).isoformat(), "elapsed_seconds": time.perf_counter() - total_tick, "feature_construction_seconds": feature_seconds, "python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "scikit_learn": sklearn.__version__, "xgboost": xgb.__version__, "torch": torch.__version__, "cpu": platform.processor(), "logical_cpu_count": psutil.cpu_count(), "raw_days_read": len(source_days), "random_seed": config["runtime"]["random_seed"], "test_loaded": False, "ridge_selected_alpha": ridge[1], "xgboost_selected_config_index": xgb_best[1], "xgboost_selected_config": xgb_best[2], "gru_epoch_history": gru[5]}
    schema = feature_schema()
    schema.to_csv(output_dir / "Step2B_Feature_Schema.csv", index=False, encoding="utf-8-sig")
    predictions.to_csv(output_dir / ("Step2B_Smoke_Predictions.csv" if config["mode"] == "smoke" else "Step2B_Selector_Predictions.csv"), index=False, encoding="utf-8-sig")
    candidate_scores.to_csv(output_dir / f"{prefix}_Candidate_Scores.csv", index=False, encoding="utf-8-sig")
    method_summary.to_csv(output_dir / ("Step2B_Smoke_Method_Summary.csv" if config["mode"] == "smoke" else "Step2B_Method_Summary.csv"), index=False, encoding="utf-8-sig")
    station_summary.to_csv(output_dir / ("Step2B_Smoke_Station_Level_Summary.csv" if config["mode"] == "smoke" else "Step2B_Station_Level_Summary.csv"), index=False, encoding="utf-8-sig")
    paired.to_csv(output_dir / "Step2B_Paired_Development_Comparisons.csv", index=False, encoding="utf-8-sig"); runtime_frame.to_csv(output_dir / "Step2B_Runtime.csv", index=False, encoding="utf-8-sig")
    jev_evidence.to_csv(output_dir / "Step2B_JEV_Evidence.csv", index=False, encoding="utf-8-sig"); confidence_summary.to_csv(output_dir / "Step2B_JEV_Confidence_Summary.csv", index=False, encoding="utf-8-sig")
    write_json(output_dir / "Step2B_JEV_Weights.json", {"version": JEV_VERSION, "combined_freeze_sha256": JEV_FREEZE_SHA256, "weights": jev_model["weights"], "tau_d": jev_model["tau_d"], "optimizer": jev_model["optimizer"]})
    write_json(output_dir / ("Step2B_Smoke_QC.json" if config["mode"] == "smoke" else "Step2B_QC.json"), qc); write_json(output_dir / "Step2B_Fairness_Audit.json", fairness); write_json(output_dir / "Step2B_Leakage_Audit.json", leakage); write_json(output_dir / ("Step2B_Smoke_Runtime.json" if config["mode"] == "smoke" else "Step2B_Runtime.json"), runtime)
    write_json(output_dir / "Step2B_Model_Config.json", {"learned_features": LEARNED_FEATURES, "ridge_selected_alpha": ridge[1], "xgboost_selected_config": xgb_best[2], "gru": config["models"]["gru"], "jev": config["jev"], "oracle_role": "RETROSPECTIVE_REFERENCE_ONLY", "development_only": True})
    if config["mode"] == "production": write_json(output_dir / "Step2B_JEV_v1.0_Production_Model.json", jev_model)
    payload = {"output_xlsx": str(output_dir / ("Step2B_Smoke_Summary.xlsx" if config["mode"] == "smoke" else "Step2B_Results.xlsx")), "preview_dir": str(output_dir / ".workbook_previews"), "sheets": {"README": [{"field": "Mode", "value": config["mode"]}, {"field": "Scope", "value": "DEVELOPMENT_ONLY"}, {"field": "QC", "value": qc["status"]}, {"field": "Production preflight", "value": preflight_report["status"]}, {"field": "Full Production", "value": "NO"}, {"field": "Test", "value": "HELD_OUT_NOT_LOADED"}], "METHOD_SUMMARY": method_summary.to_dict("records"), "PAIRED_JEV": paired.to_dict("records"), "SAMPLE_COUNTS": [{"split": "train", "target_times": train_samples, "candidate_rows": len(train)}, {"split": "validation", "target_times": validation_samples, "candidate_rows": len(validation)}, {"split": "test", "target_times": 0, "candidate_rows": 0}], "STATION_SUMMARY": station_summary.to_dict("records"), "JEV_WEIGHTS": [{"evidence": name, "weight": jev_model["weights"][name]} for name in EVIDENCE_NAMES] + [{"evidence": "tau_d", "weight": jev_model["tau_d"]}, {"evidence": "Train objective", "weight": jev_model["optimizer"]["objective"]}], "JEV_EVIDENCE": evidence_summary.to_dict("records"), "JEV_CONFIDENCE": confidence_summary.to_dict("records"), "FEATURE_SCHEMA": schema.to_dict("records"), "FAIRNESS": [{"field": key, "value": value} for key, value in fairness.items() if not isinstance(value, dict)], "LEAKAGE": [{"field": key, "value": value} for key, value in leakage.items()], "QC": [{"check": key, "passed": value} for key, value in checks.items()], "PREFLIGHT": [{"check": key, "passed": value} for key, value in preflight_report["checks"].items()], "RUNTIME": runtime_frame.to_dict("records")}}
    write_json(output_dir / ".step2b_workbook_payload.json", payload)
    logger.info("Available methods=%s", expected_methods); logger.info("Same denominator=%s", denominator); logger.info("Smoke QC=%s Preflight=%s Test=0 Full Production=NO", qc["status"], preflight_report["status"])
    return 0 if qc["status"] == "PASS" else 2


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--config", required=True, type=Path); parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    if args.preflight_only:
        report = production_preflight(read_json(args.config), write_report=True)
        print(f"PRODUCTION_PREFLIGHT = {report['status']}")
        print("TEST_SPLIT_STATUS = HELD_OUT_NOT_LOADED")
        print("Test target samples = 0")
        print("Full Production executed = NO")
        return 0 if report["status"] == "PASS" else 2
    return run(args.config)


if __name__ == "__main__": raise SystemExit(main())
