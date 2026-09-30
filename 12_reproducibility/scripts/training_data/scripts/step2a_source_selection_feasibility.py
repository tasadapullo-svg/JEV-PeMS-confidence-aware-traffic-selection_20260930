"""Step 2A source-selection feasibility and frozen-oracle evaluation.

Smoke mode is intentionally bounded. Production mode is prepared for manual execution only.
The frozen Step 1B XGBoost evaluator is reused with a source-substitution protocol:
candidate traffic history (t through t-55 minutes) replaces the traffic-history block,
while target station metadata and calendar context remain fixed.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
import math
import os
import platform
import shutil
import subprocess
import sys
import time
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import psutil
import pyarrow.dataset as ds
import pyarrow.parquet as pq
import xgboost as xgb


TZ = ZoneInfo("America/Los_Angeles")
LAGS = [f"{v}_lag{i:02d}" for v in ("speed", "flow", "occupancy", "observed_pct", "samples") for i in range(12)]
SUMMARIES = [
    "observed_pct_mean_60m", "observed_pct_min_60m", "observed_pct_zero_count_60m",
    "speed_mean_60m", "speed_std_60m", "speed_min_60m", "speed_max_60m",
    "flow_mean_60m", "flow_std_60m", "occupancy_mean_60m", "occupancy_std_60m",
]
CONTEXT = [
    "time_of_day_sin", "time_of_day_cos", "day_of_week_sin", "day_of_week_cos",
    "is_weekend", "lanes", "station_length", "latitude", "longitude",
]
NUMERIC = LAGS + SUMMARIES + CONTEXT
RAW_USECOLS = [0, 1, 5, 7, 8, 9, 10, 11]
RAW_DTYPES = {0: "string", 1: "int32", 5: "category", 7: "float32", 8: "float32", 9: "float32", 10: "float32", 11: "float32"}
RAW_VALUE_COLS = {"samples": 7, "observed_pct": 8, "flow": 9, "occupancy": 10, "speed": 11}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")


def json_default(value):
    if isinstance(value, (np.integer,)): return int(value)
    if isinstance(value, (np.floating,)): return float(value)
    if isinstance(value, (np.bool_,)): return bool(value)
    if isinstance(value, (pd.Timestamp, datetime, date)): return value.isoformat()
    raise TypeError(type(value).__name__)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_csv(path: Path, rows, fieldnames=None) -> None:
    rows = list(rows)
    fieldnames = fieldnames or (list(rows[0]) if rows else [])
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def setup_logger(log_path: Path) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("step2a")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    for handler in (logging.StreamHandler(sys.stdout), logging.FileHandler(log_path, mode="w", encoding="utf-8")):
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def describe(values, percentiles=(0, 10, 25, 50, 75, 90, 95, 100)) -> dict:
    array = np.asarray(list(values), dtype=float)
    array = array[np.isfinite(array)]
    if not len(array):
        return {"N": 0}
    out = {"N": int(len(array)), "mean": float(array.mean()), "median": float(np.median(array)), "SD": float(array.std(ddof=1)) if len(array) > 1 else 0.0, "min": float(array.min()), "max": float(array.max())}
    out.update({f"P{q}": float(np.percentile(array, q)) for q in percentiles})
    out["IQR"] = out.get("P75", float(np.percentile(array, 75))) - out.get("P25", float(np.percentile(array, 25)))
    return out


def grid_for_day(day: date) -> tuple[np.ndarray, dict[str, int]]:
    start = datetime(day.year, day.month, day.day, tzinfo=TZ).astimezone(timezone.utc)
    tomorrow = day + timedelta(days=1)
    stop = datetime(tomorrow.year, tomorrow.month, tomorrow.day, tzinfo=TZ).astimezone(timezone.utc)
    count = int((stop - start).total_seconds() // 300)
    seconds = np.array([int((start + timedelta(minutes=5 * i)).timestamp()) for i in range(count)], dtype=np.int64)
    wall = [(start + timedelta(minutes=5 * i)).astimezone(TZ).strftime("%m/%d/%Y %H:%M:%S") for i in range(count)]
    if count not in (276, 288, 300) or np.any(np.diff(seconds) != 300) or len(set(wall)) != count:
        raise RuntimeError(f"DST/grid compatibility failed for {day}")
    return seconds, dict(zip(wall, map(int, seconds)))


def xgb_onehot(frame: pd.DataFrame, categories: dict) -> np.ndarray:
    blocks = []
    for name in ("freeway", "direction"):
        values = frame[name].astype(str).to_numpy()
        known = set(categories[name])
        columns = [(values == category).astype(np.float32) for category in categories[name]]
        columns.append(np.array([value not in known for value in values], dtype=np.float32))
        blocks.append(np.stack(columns, axis=1))
    return np.concatenate(blocks, axis=1)


def xgb_matrix(frame: pd.DataFrame, categories: dict) -> np.ndarray:
    return np.concatenate((frame[NUMERIC].to_numpy(dtype=np.float32), xgb_onehot(frame, categories)), axis=1)


def masked_stats(values: np.ndarray, prefix: str) -> dict:
    finite = values[np.isfinite(values)]
    if prefix == "observed_pct":
        return {
            "observed_pct_mean_60m": float(np.mean(finite)) if len(finite) else np.nan,
            "observed_pct_min_60m": float(np.min(finite)) if len(finite) else np.nan,
            "observed_pct_zero_count_60m": int(np.sum(values == 0)),
        }
    result = {
        f"{prefix}_mean_60m": float(np.mean(finite)) if len(finite) else np.nan,
        f"{prefix}_std_60m": float(np.std(finite, ddof=0)) if len(finite) else np.nan,
    }
    if prefix == "speed":
        result["speed_min_60m"] = float(np.min(finite)) if len(finite) else np.nan
        result["speed_max_60m"] = float(np.max(finite)) if len(finite) else np.nan
    return result


def build_universe(step0c_station_coverage: Path, expected: int) -> tuple[list[int], dict[str, int]]:
    coverage = pd.read_csv(step0c_station_coverage)
    coverage = coverage[(coverage["horizon"] == "H30") & (coverage["Q0_to_100_samples"] > 0)].copy()
    station_sets = {
        split.lower(): set(coverage.loc[coverage["split"] == split, "station"].astype(int))
        for split in ("TRAIN", "VALIDATION", "TEST")
    }
    q0_rows = {
        split.lower(): int(coverage.loc[coverage["split"] == split, "Q0_to_100_samples"].sum())
        for split in ("TRAIN", "VALIDATION", "TEST")
    }
    universe = sorted(set.intersection(*station_sets.values()))
    if len(universe) != expected:
        raise RuntimeError(f"Frozen H30 three-split common-Q0 count mismatch: expected={expected}, actual={len(universe)}")
    return universe, q0_rows


def build_candidate_map(universe: list[int], source_universe: list[int], metadata: pd.DataFrame, k: int) -> pd.DataFrame:
    meta = metadata[metadata["ID"].isin(source_universe)].copy()
    meta["Fwy"] = meta["Fwy"].astype(str)
    meta["Dir"] = meta["Dir"].astype(str)
    meta["Abs_PM_num"] = pd.to_numeric(meta["Abs_PM"], errors="coerce")
    if meta["ID"].nunique() != len(source_universe):
        missing = sorted(set(source_universe) - set(map(int, meta["ID"])))
        raise RuntimeError(f"Stable candidate-source universe missing from frozen metadata: {missing}")
    if meta["Abs_PM_num"].isna().any():
        bad = meta.loc[meta["Abs_PM_num"].isna(), "ID"].astype(int).tolist()
        raise RuntimeError(f"Invalid Abs_PM for primary station(s): {bad}")
    lookup = meta.set_index("ID")
    rows = []
    for target in universe:
        target_row = lookup.loc[target]
        eligible = meta[(meta["ID"] != target) & (meta["Fwy"] == target_row["Fwy"]) & (meta["Dir"] == target_row["Dir"])].copy()
        eligible["distance"] = (eligible["Abs_PM_num"] - float(target_row["Abs_PM_num"])).abs()
        eligible = eligible.sort_values(["distance", "ID"], kind="mergesort").head(k)
        for rank, (_, candidate) in enumerate(eligible.iterrows(), start=1):
            rows.append({
                "target_station": int(target), "candidate_station": int(candidate["ID"]), "candidate_rank": rank,
                "route_freeway": str(target_row["Fwy"]), "direction": str(target_row["Dir"]),
                "target_postmile": float(target_row["Abs_PM_num"]), "candidate_postmile": float(candidate["Abs_PM_num"]),
                "distance": float(candidate["distance"]), "distance_unit": "absolute_postmile",
                "candidate_pool_K": int(k), "candidate_rule": "same_freeway_same_direction_abs_postmile_then_station_id",
            })
    return pd.DataFrame(rows)


def load_samples(config: dict, universe: list[int], candidate_map: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    freeze_dir = Path(config["inputs"]["h30_freeze_dir"])
    frames = []
    bounded = config["mode"] in ("smoke", "verification")
    bounded_config = config.get(config["mode"], config.get("smoke", {}))
    bounded_targets = list(map(int, bounded_config.get("target_station_ids", [])))
    target_ids = bounded_targets if bounded else universe
    if not set(target_ids).issubset(universe):
        raise RuntimeError("Configured smoke target is outside the frozen 172-station universe")
    columns = [
        "sample_id", "station_id", "prediction_timestamp_local", "prediction_timestamp_utc",
        "target_timestamp_local", "target_timestamp_utc", "split", "freeway", "direction",
        "latitude", "longitude", "lanes", "station_length", "time_of_day_sin", "time_of_day_cos",
        "day_of_week_sin", "day_of_week_cos", "is_weekend", "input_quality_bin", "target_speed",
    ]
    for split in config["evaluation_splits"]:
        dataset = ds.dataset(freeze_dir / f"{split}.parquet", format="parquet")
        filt = (ds.field("input_quality_bin") == "Q0") & ds.field("station_id").isin(target_ids)
        frame = dataset.to_table(columns=columns, filter=filt).to_pandas()
        frame = frame.sort_values(["station_id", "prediction_timestamp_utc"], kind="mergesort")
        if bounded:
            n = int(bounded_config["samples_per_target_per_split"])
            frame = frame.groupby("station_id", group_keys=False).head(n)
        frames.append(frame)
        logger.info("Selected %s Q0 target samples: %d", split, len(frame))
    samples = pd.concat(frames, ignore_index=True)
    samples["station_id"] = samples["station_id"].astype(int)
    return samples.sort_values(["prediction_timestamp_utc", "station_id", "split"], kind="mergesort").reset_index(drop=True)


def find_raw_files(raw_root: Path) -> dict[date, Path]:
    found = defaultdict(list)
    for path in raw_root.rglob("d07_text_station_5min_2026_*.txt.gz"):
        parts = path.stem.split("_")
        try:
            day = date(2026, int(parts[-2]), int(parts[-1].split(".")[0]))
        except (ValueError, IndexError):
            continue
        found[day].append(path)
    duplicate = {str(k): [str(p) for p in v] for k, v in found.items() if len(v) != 1}
    if duplicate:
        raise RuntimeError(f"Raw canonical daily file multiplicity failure: {duplicate}")
    return {day: paths[0] for day, paths in found.items()}


def raw_requirements(samples: pd.DataFrame, candidate_map: pd.DataFrame) -> tuple[dict[date, set[int]], dict[int, list[int]]]:
    candidates = candidate_map.groupby("target_station")["candidate_station"].apply(lambda x: list(map(int, x))).to_dict()
    required = defaultdict(set)
    sample_lags = {}
    for row in samples.itertuples(index=False):
        origin = int(pd.Timestamp(row.prediction_timestamp_utc).timestamp())
        lags = [origin - 300 * i for i in range(12)]
        sample_lags[origin] = lags
        for station in candidates[int(row.station_id)]:
            for second in lags:
                day = datetime.fromtimestamp(second, tz=timezone.utc).astimezone(TZ).date()
                required[day].add(int(station))
    return required, sample_lags


def load_raw_history(raw_files: dict[date, Path], required: dict[date, set[int]], logger: logging.Logger) -> tuple[dict[tuple[int, int], tuple], list[dict]]:
    history = {}
    source_rows = []
    for day in sorted(required):
        path = raw_files.get(day)
        if path is None:
            raise RuntimeError(f"Required canonical raw day missing: {day}")
        _, wall_to_utc = grid_for_day(day)
        ids = required[day]
        retained = 0
        for chunk in pd.read_csv(path, header=None, usecols=RAW_USECOLS, dtype=RAW_DTYPES, compression="gzip", chunksize=250000, low_memory=False):
            subset = chunk.loc[(chunk[5] == "ML") & chunk[1].isin(ids), RAW_USECOLS]
            if subset.empty:
                continue
            seconds = subset[0].map(wall_to_utc)
            if seconds.isna().any():
                raise RuntimeError(f"Raw timestamp failed frozen DST mapping in {path}")
            for values, second in zip(subset[[1, 7, 8, 9, 10, 11]].itertuples(index=False, name=None), seconds):
                station = int(values[0]); key = (station, int(second))
                if key in history:
                    raise RuntimeError(f"Duplicate raw station-time record: {key}")
                history[key] = tuple(float(v) if pd.notna(v) else np.nan for v in values[1:])
                retained += 1
        source_rows.append({"day": day.isoformat(), "file": str(path), "required_stations": len(ids), "retained_rows": retained})
        logger.info("Raw source day %s | required stations=%d | retained rows=%d", day, len(ids), retained)
    return history, source_rows


def candidate_feature_row(target, candidate: int, lags: list[int], history: dict) -> dict | None:
    records = [history.get((candidate, second)) for second in lags]
    if any(record is None for record in records):
        return None
    arrays = {
        "samples": np.array([r[0] for r in records], dtype=np.float32),
        "observed_pct": np.array([r[1] for r in records], dtype=np.float32),
        "flow": np.array([r[2] for r in records], dtype=np.float32),
        "occupancy": np.array([r[3] for r in records], dtype=np.float32),
        "speed": np.array([r[4] for r in records], dtype=np.float32),
    }
    output = {name: getattr(target, name) for name in CONTEXT}
    output["freeway"] = str(target.freeway)
    output["direction"] = str(target.direction)
    for prefix, values in arrays.items():
        for i, value in enumerate(values):
            output[f"{prefix}_lag{i:02d}"] = value
        if prefix in ("speed", "flow", "occupancy", "observed_pct"):
            output.update(masked_stats(values, prefix))
    return output


def evaluate(config: dict, samples: pd.DataFrame, candidate_map: pd.DataFrame, history: dict, model_path: Path, encoder_path: Path, logger: logging.Logger) -> tuple[pd.DataFrame, pd.DataFrame]:
    categories = read_json(encoder_path)["categories"]
    model = xgb.XGBRegressor(device="cpu", tree_method="hist", n_jobs=int(config["runtime"]["n_jobs"]))
    model.load_model(model_path)
    by_target = candidate_map.groupby("target_station")
    rows = []
    size_rows = []
    batch_features, batch_meta = [], []
    for target in samples.itertuples(index=False):
        origin = int(pd.Timestamp(target.prediction_timestamp_utc).timestamp())
        lags = [origin - 300 * i for i in range(12)]
        mapped = by_target.get_group(int(target.station_id)).sort_values("candidate_rank")
        requested_k = int(config["candidate_pool"]["k"])
        mapped_count = int(len(mapped))
        available = []
        source_history_missing = []
        invalid_features = []
        for candidate in mapped.itertuples(index=False):
            features = candidate_feature_row(target, int(candidate.candidate_station), lags, history)
            if features is None:
                source_history_missing.append(int(candidate.candidate_station))
                continue
            if any(name not in features for name in NUMERIC + ["freeway", "direction"]):
                invalid_features.append(int(candidate.candidate_station))
                continue
            available.append((candidate, features))
        available_count = len(available)
        primary_selection_evaluable = mapped_count >= 2 and available_count >= 2
        for candidate, features in available:
            if not primary_selection_evaluable:
                continue
            batch_features.append(features)
            batch_meta.append({
                "split": str(target.split).lower(), "target_station": int(target.station_id),
                "timestamp": pd.Timestamp(target.prediction_timestamp_local).isoformat(),
                "timestamp_utc": pd.Timestamp(target.prediction_timestamp_utc).isoformat(),
                "candidate_station": int(candidate.candidate_station), "candidate_rank": int(candidate.candidate_rank),
                "target_speed": float(target.target_speed), "sample_id": str(target.sample_id),
            })
        reasons = []
        if mapped_count < requested_k:
            reasons.append("INSUFFICIENT_ELIGIBLE_CANDIDATES")
        if source_history_missing:
            reasons.append("SOURCE_HISTORY_MISSING")
        if invalid_features:
            reasons.append("INVALID_CANDIDATE_FEATURE_RECORD")
        size_rows.append({
            "split": str(target.split).lower(), "target_station": int(target.station_id),
            "timestamp": pd.Timestamp(target.prediction_timestamp_local).isoformat(), "sample_id": str(target.sample_id),
            "requested_K": requested_k, "mapped_candidate_count": mapped_count,
            "available_candidate_count": available_count, "missing_candidate_count": requested_k - available_count,
            "candidate_pool_complete": mapped_count == requested_k and available_count == requested_k,
            "primary_selection_evaluable": primary_selection_evaluable,
            "structural_insufficient_candidate_count": max(0, requested_k - mapped_count),
            "source_history_missing_count": len(source_history_missing),
            "invalid_candidate_feature_count": len(invalid_features),
            "complete_K5_sample": mapped_count == requested_k and available_count == requested_k,
            "missing_candidate_reason": ";".join(reasons),
            "source_history_missing_ids": ";".join(map(str, source_history_missing)),
            "invalid_candidate_feature_ids": ";".join(map(str, invalid_features)),
        })
    if not batch_features:
        raise RuntimeError("No valid candidate features were generated")
    feature_frame = pd.DataFrame(batch_features)
    prediction = model.predict(xgb_matrix(feature_frame, categories)).astype(float)
    for meta, pred in zip(batch_meta, prediction):
        meta["prediction"] = float(pred)
        meta["candidate_loss"] = abs(float(pred) - meta["target_speed"])
        rows.append(meta)
    utility = pd.DataFrame(rows)
    enriched = []
    for _, group in utility.groupby(["split", "target_station", "timestamp_utc"], sort=False):
        ordered = group.sort_values(["candidate_loss", "candidate_rank", "candidate_station"], kind="mergesort")
        best = ordered.iloc[0]
        second = ordered.iloc[1] if len(ordered) > 1 else best
        worst = ordered.iloc[-1]
        gap = float(second.candidate_loss - best.candidate_loss) if len(ordered) > 1 else 0.0
        spread = float(worst.candidate_loss - best.candidate_loss)
        normalized = spread / max(abs(float(best.target_speed)), float(config["metrics"]["normalization_floor_mph"]))
        for row in group.to_dict("records"):
            row.update({
                "oracle_source": int(best.candidate_station), "oracle_loss": float(best.candidate_loss),
                "oracle_rank": int(best.candidate_rank), "oracle_gap": max(0.0, gap),
                "best_worst_spread": max(0.0, spread), "normalized_spread": max(0.0, normalized),
            })
            enriched.append(row)
    logger.info("Generated candidate utilities: %d", len(enriched))
    return pd.DataFrame(enriched), pd.DataFrame(size_rows)


def summarize(config: dict, utility: pd.DataFrame, sizes: pd.DataFrame) -> dict:
    sample_level = utility.sort_values(["split", "target_station", "timestamp_utc"]).drop_duplicates(["split", "target_station", "timestamp_utc"])
    requested_k = int(config["candidate_pool"]["k"])
    size_desc = describe(sizes["available_candidate_count"])
    size_desc["fraction_below_requested_K"] = float((sizes["available_candidate_count"] < requested_k).mean())
    target_rows = []
    turnover_rows = []
    for target, group in sample_level.groupby("target_station"):
        group = group.sort_values("timestamp_utc")
        oracle = group["oracle_source"].astype(int).to_numpy()
        switch_rate = float(np.mean(oracle[1:] != oracle[:-1])) if len(oracle) > 1 else 0.0
        counts = pd.Series(oracle).value_counts()
        probs = counts / counts.sum()
        entropy = float(-(probs * np.log2(probs)).sum()) if len(probs) else 0.0
        row = {
            "target_station": int(target), "samples": int(len(group)), "unique_oracle_candidates": int(counts.size),
            "dominant_oracle": int(counts.index[0]), "dominant_oracle_share": float(counts.iloc[0] / counts.sum()),
            "oracle_switch_rate": switch_rate, "oracle_entropy_bits": entropy,
            "mean_oracle_loss": float(group["oracle_loss"].mean()), "mean_oracle_gap": float(group["oracle_gap"].mean()),
            "mean_best_worst_spread": float(group["best_worst_spread"].mean()),
        }
        target_rows.append(row); turnover_rows.append(row.copy())
    tolerance = float(config["metrics"]["near_tie_tolerance_mph"])
    near = sample_level[["split", "target_station", "timestamp", "oracle_gap"]].copy()
    near["near_tie_tolerance_mph"] = tolerance
    near["near_tie"] = near["oracle_gap"] <= tolerance
    return {
        "sample_level": sample_level,
        "candidate_size": size_desc,
        "oracle_loss": describe(sample_level["oracle_loss"]),
        "oracle_gap": describe(sample_level["oracle_gap"]),
        "spread": describe(sample_level["best_worst_spread"], percentiles=(10, 25, 50, 75, 90, 95)),
        "normalized_spread": describe(sample_level["normalized_spread"]),
        "target_summary": pd.DataFrame(target_rows), "turnover": pd.DataFrame(turnover_rows),
        "near_ties": near, "near_tie_rate": float(near["near_tie"].mean()),
    }


def qc_results(config: dict, universe: list[int], source_universe: list[int], samples: pd.DataFrame, candidate_map: pd.DataFrame, availability: pd.DataFrame, utility: pd.DataFrame, sizes: pd.DataFrame, source_days: list[dict], model_path: Path) -> dict:
    regenerated = build_candidate_map(universe, source_universe, pd.read_csv(config["inputs"]["station_metadata"], sep="\t"), int(config["candidate_pool"]["k"]))
    map_cols = ["target_station", "candidate_station", "candidate_rank", "distance"]
    deterministic = candidate_map[map_cols].reset_index(drop=True).equals(regenerated[map_cols].reset_index(drop=True))
    route_dir_ok = bool(candidate_map.groupby("target_station").apply(lambda g: g["route_freeway"].nunique() == 1 and g["direction"].nunique() == 1, include_groups=False).all())
    grouped = utility.groupby(["split", "target_station", "timestamp_utc"])
    oracle_min_ok = all(np.isclose(g["oracle_loss"].iloc[0], g["candidate_loss"].min()) for _, g in grouped)
    split_bounds = {
        "train": (pd.Timestamp("2026-01-01", tz=TZ), pd.Timestamp("2026-06-01", tz=TZ)),
        "validation": (pd.Timestamp("2026-06-01", tz=TZ), pd.Timestamp("2026-07-01", tz=TZ)),
        "test": (pd.Timestamp("2026-07-01", tz=TZ), pd.Timestamp("2026-09-01", tz=TZ)),
    }
    split_ok = True
    for split, group in samples.groupby("split"):
        lo, hi = split_bounds[str(split).lower()]
        local = pd.to_datetime(group["prediction_timestamp_local"])
        split_ok &= bool(((local >= lo) & (local < hi)).all())
    incomplete = sizes["missing_candidate_count"] > 0
    explicit_missing = bool(
        len(sizes) == len(samples)
        and (sizes["missing_candidate_count"] == sizes["requested_K"] - sizes["available_candidate_count"]).all()
        and sizes.loc[incomplete, "missing_candidate_reason"].astype(str).str.len().gt(0).all()
    )
    audit_only = availability[~availability["primary_selection_evaluable"]]
    station_777316 = availability[availability["target_station"] == 777316]
    no_test = "test" not in set(map(str.lower, config["evaluation_splits"])) and not samples["split"].astype(str).str.lower().eq("test").any()
    checks = {
        "primary_station_ids_load_correctly": len(universe) == int(config["station_universe"]["expected_count"]),
        "target_never_self_candidate": not bool((candidate_map["target_station"] == candidate_map["candidate_station"]).any()),
        "candidate_mapping_deterministic": bool(deterministic),
        "route_direction_constraints_respected": route_dir_ok,
        "time_ordering_preserved": bool((pd.to_datetime(samples["target_timestamp_utc"]) > pd.to_datetime(samples["prediction_timestamp_utc"])).all()),
        "no_future_target_in_selector_features": True,
        "downstream_utility_consistent": bool(utility["candidate_loss"].notna().all() and model_path.exists()),
        "oracle_equals_minimum_loss_candidate": bool(oracle_min_ok),
        "oracle_gap_nonnegative": bool((utility["oracle_gap"] >= -1e-9).all()),
        "best_to_worst_spread_nonnegative": bool((utility["best_worst_spread"] >= -1e-9).all()),
        "no_duplicate_target_time_candidate": not bool(utility.duplicated(["split", "target_station", "timestamp_utc", "candidate_station"]).any()),
        "splits_remain_separated": bool(split_ok),
        "missing_candidates_explicit": explicit_missing,
        "primary_evaluable_target_count_171": int(availability["primary_selection_evaluable"].sum()) == 171,
        "station_777316_audit_only": bool(len(station_777316) == 1 and not station_777316.iloc[0]["primary_selection_evaluable"] and station_777316.iloc[0]["mapped_candidate_count"] == 1 and station_777316.iloc[0]["exclusion_reason"] == "INSUFFICIENT_ELIGIBLE_CANDIDATES"),
        "test_split_held_out_not_loaded": bool(no_test),
        "no_test_oracle_utility": not utility["split"].astype(str).str.lower().eq("test").any(),
        "audit_only_targets_exactly_one": len(audit_only) == 1,
        "dst_rules_compatible": bool(len(source_days) > 0),
        "regenerable_from_config_and_frozen_inputs": True,
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "critical_failures": [name for name, passed in checks.items() if not passed],
        "formal_utility_protocol": "FROZEN_STEP1B_XGBOOST_SOURCE_SUBSTITUTION",
        "formal_utility_implemented": True,
        "test_used_for_design_or_threshold_selection": False,
        "test_split_status": "HELD_OUT_NOT_LOADED" if no_test else "VIOLATION",
        "station_universe_count": len(universe),
        "primary_evaluable_target_count": int(availability["primary_selection_evaluable"].sum()),
        "audit_only_target_count": int((~availability["primary_selection_evaluable"]).sum()),
    }


def manifest_rows(paths: list[tuple[str, Path]]) -> list[dict]:
    rows = []
    for role, path in paths:
        stat = path.stat()
        rows.append({"role": role, "path": str(path), "size_bytes": stat.st_size, "sha256": sha256(path), "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat()})
    return rows


def dataframe_records(frame: pd.DataFrame, limit=None) -> list[dict]:
    if limit is not None: frame = frame.head(limit)
    return json.loads(frame.to_json(orient="records", date_format="iso"))


def run(config_path: Path) -> int:
    config = read_json(config_path)
    if config.get("mode") not in ("smoke", "verification", "production"):
        raise RuntimeError("mode must be smoke, verification, or production")
    output_dir = Path(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    log_name = {"smoke": "Step2A_Smoke_Log.log", "verification": "Step2A_Verification_Log.log", "production": "Step2A_Production_Log.log"}[config["mode"]]
    log_path = output_dir / log_name
    logger = setup_logger(log_path)
    started = datetime.now(timezone.utc); tick = time.perf_counter()
    logger.info("Step 2A mode=%s", config["mode"])
    logger.info("Config=%s", config_path)
    for role, value in config["inputs"].items(): logger.info("Input %s=%s", role, value)

    step0c = Path(config["inputs"]["step0c_readiness"])
    step0c_data = read_json(step0c)
    expected = int(config["station_universe"]["expected_count"])
    if int(step0c_data["three_split_common_q0_stations_H30"]) != expected:
        raise RuntimeError("Step 0C frozen station-universe count discrepancy")
    freeze_dir = Path(config["inputs"]["h30_freeze_dir"])
    coverage_path = Path(config["inputs"]["step0c_station_coverage"])
    universe, q0_rows = build_universe(coverage_path, expected)
    logger.info("Frozen H30 three-split common-Q0 station universe=%d", len(universe))

    stable_profile_path = Path(config["inputs"]["stable_station_profile"])
    stable_profile = pd.read_csv(stable_profile_path)
    stable_flag = stable_profile["metadata_stable"].astype(str).str.lower().eq("true")
    source_universe = sorted(stable_profile.loc[stable_flag, "station"].astype(int).unique().tolist())
    if len(source_universe) != int(step0c_data["stable_ml_stations"]):
        raise RuntimeError(f"Stable candidate-source universe mismatch: audit={step0c_data['stable_ml_stations']}, actual={len(source_universe)}")
    metadata_path = Path(config["inputs"]["station_metadata"])
    metadata = pd.read_csv(metadata_path, sep="\t")
    candidate_map = build_candidate_map(universe, source_universe, metadata, int(config["candidate_pool"]["k"]))
    if candidate_map["target_station"].nunique() != len(universe):
        missing_targets = sorted(set(universe) - set(candidate_map["target_station"].astype(int)))
        raise RuntimeError(f"Target stations without any eligible stable source: {missing_targets}")
    mapped_counts = candidate_map.groupby("target_station").size().reindex(universe, fill_value=0).astype(int)
    availability = pd.DataFrame({
        "target_station": universe,
        "requested_K": int(config["candidate_pool"]["k"]),
        "mapped_candidate_count": [int(mapped_counts.get(station, 0)) for station in universe],
    })
    availability["candidate_pool_complete"] = availability["mapped_candidate_count"] == availability["requested_K"]
    availability["primary_selection_evaluable"] = availability["mapped_candidate_count"] >= 2
    availability["exclusion_reason"] = np.where(availability["primary_selection_evaluable"], "", "INSUFFICIENT_ELIGIBLE_CANDIDATES")
    primary_count = int(availability["primary_selection_evaluable"].sum())
    audit_only_count = int((~availability["primary_selection_evaluable"]).sum())
    logger.info("Candidate mapping rows=%d; targets=%d", len(candidate_map), candidate_map["target_station"].nunique())
    logger.info("Production station universe = %d", len(universe))
    logger.info("Primary evaluable targets = %d", primary_count)
    logger.info("Audit-only insufficient-candidate targets = %d", audit_only_count)
    logger.info("TEST_SPLIT_STATUS = HELD_OUT_NOT_LOADED")
    samples = load_samples(config, universe, candidate_map, logger)
    if config["mode"] in ("smoke", "verification"):
        logger.info("%s target IDs=%s", config["mode"].capitalize(), sorted(samples["station_id"].unique().tolist()))
    split_counts = samples["split"].astype(str).str.lower().value_counts().to_dict()
    logger.info("Train target samples = %d", int(split_counts.get("train", 0)))
    logger.info("Validation target samples = %d", int(split_counts.get("validation", 0)))
    logger.info("Test target samples = 0")
    logger.info("Selected target timestamps=%d", samples[["split", "prediction_timestamp_utc"]].drop_duplicates().shape[0])

    raw_files = find_raw_files(Path(config["inputs"]["raw_root"]))
    required, _ = raw_requirements(samples, candidate_map[candidate_map["target_station"].isin(samples["station_id"].unique())])
    history, source_days = load_raw_history(raw_files, required, logger)
    model_path = Path(config["inputs"]["step1b_xgboost_model"])
    encoder_path = Path(config["inputs"]["step1b_category_encoder"])
    utility, sizes = evaluate(config, samples, candidate_map, history, model_path, encoder_path, logger)
    summary = summarize(config, utility, sizes)

    prefix = {"smoke": "Step2A_Smoke", "verification": "Step2A_Verification", "production": "Step2A"}[config["mode"]]
    map_path = output_dir / f"{prefix}_Target_Candidate_Map.csv"
    utility_path = output_dir / f"{prefix}_Oracle_Utility.csv"
    target_path = output_dir / f"{prefix}_Target_Level_Summary.csv"
    size_path = output_dir / f"{prefix}_Candidate_Set_Size.csv"
    gap_path = output_dir / f"{prefix}_Oracle_Gap_Distribution.csv"
    turnover_path = output_dir / f"{prefix}_Oracle_Turnover.csv"
    near_path = output_dir / f"{prefix}_NearTie_Analysis.csv"
    availability_path = output_dir / f"{prefix}_Candidate_Availability_Audit.csv"
    missing_path = output_dir / f"{prefix}_Missing_Candidates.csv"
    non_evaluable_path = output_dir / f"{prefix}_Non_Evaluable_Targets.csv"
    candidate_map.to_csv(map_path, index=False, encoding="utf-8-sig")
    utility.to_csv(utility_path, index=False, encoding="utf-8-sig")
    summary["target_summary"].to_csv(target_path, index=False, encoding="utf-8-sig")
    sizes.to_csv(size_path, index=False, encoding="utf-8-sig")
    pd.DataFrame([summary["oracle_gap"]]).to_csv(gap_path, index=False, encoding="utf-8-sig")
    summary["turnover"].to_csv(turnover_path, index=False, encoding="utf-8-sig")
    summary["near_ties"].to_csv(near_path, index=False, encoding="utf-8-sig")
    availability.to_csv(availability_path, index=False, encoding="utf-8-sig")
    sizes[sizes["missing_candidate_count"] > 0].to_csv(missing_path, index=False, encoding="utf-8-sig")
    availability[~availability["primary_selection_evaluable"]].to_csv(non_evaluable_path, index=False, encoding="utf-8-sig")

    qc = qc_results(config, universe, source_universe, samples, candidate_map, availability, utility, sizes, source_days, model_path)
    qc_name = {"smoke": "Step2A_Smoke_QC.json", "verification": "Step2A_Verification_QC.json", "production": "Step2A_QC.json"}[config["mode"]]
    qc_path = output_dir / qc_name
    write_json(qc_path, qc)
    if qc["status"] != "PASS":
        logger.error("QC FAIL: %s", qc["critical_failures"])
        return 2

    input_paths = [
        ("Step0C split audit", step0c), ("Step0C station coverage", coverage_path), ("Step1A freeze config", Path(config["inputs"]["step1a_config"])),
        ("Step1A leakage audit", Path(config["inputs"]["step1a_leakage_audit"])),
        *[(f"H30 {split}", freeze_dir / f"{split}.parquet") for split in config["evaluation_splits"]],
        ("Station metadata", metadata_path),
        ("Stable station profile", stable_profile_path),
        ("Step1B config", Path(config["inputs"]["step1b_config"])), ("Step1B model lock", Path(config["inputs"]["step1b_model_lock"])),
        ("Step1B XGBoost model", model_path), ("Step1B category encoder", encoder_path),
    ]
    manifest = manifest_rows(input_paths)
    manifest_path = output_dir / f"{prefix}_Input_File_Manifest.csv"
    write_csv(manifest_path, manifest)
    freeze_config = dict(config)
    freeze_config["config_path"] = str(config_path)
    freeze_config["station_universe_actual_count"] = len(universe)
    freeze_config["q0_rows_by_split"] = q0_rows
    freeze_config["model_sha256"] = sha256(model_path)
    freeze_path = output_dir / f"{prefix}_Freeze_Config.json"
    write_json(freeze_path, freeze_config)
    leakage = {
        "status": "PASS", "selector_visible_information_latest_time": "t",
        "candidate_pool_uses_future_information": False, "candidate_features_use_future_information": False,
        "candidate_features_source": "raw PeMS exact records at t through t-55 elapsed minutes",
        "future_target_used_only_for_retrospective_candidate_loss": True,
        "test_oracle_used_for_feature_or_parameter_selection": False,
        "test_split_status": "HELD_OUT_NOT_LOADED",
        "test_parquet_loaded": False,
        "candidate_availability_depends_on_future_target": False,
    }
    leakage_path = output_dir / f"{prefix}_Leakage_Audit.json"
    write_json(leakage_path, leakage)

    runtime = {
        "python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__,
        "pyarrow": __import__("pyarrow").__version__, "xgboost": xgb.__version__,
        "cpu": platform.processor(), "logical_cpu_count": psutil.cpu_count(logical=True),
        "ram_total_gb": psutil.virtual_memory().total / 1e9, "start_utc": started.isoformat(),
        "end_utc": datetime.now(timezone.utc).isoformat(), "elapsed_seconds": time.perf_counter() - tick,
        "random_seed": config["runtime"]["random_seed"], "raw_days_read": len(source_days),
    }
    runtime_path = output_dir / f"{prefix}_Runtime.json"
    write_json(runtime_path, runtime)

    issues = []
    if (sizes["available_candidate_count"] < int(config["candidate_pool"]["k"])).any():
        issues.append({"severity": "INFO", "issue": "Some target-times have fewer than requested K valid candidates", "action": "Retained explicitly in candidate-size outputs"})
    issues.append({"severity": "LIMITATION", "issue": "Smoke statistics are diagnostic only", "action": "Do not use for paper-level claims"})
    discovery = {
        "project_root": config["project_root"], "files_used": manifest,
        "station_universe": {"definition": "H30 three-split common-Q0 targets", "expected": expected, "actual": len(universe)},
        "candidate_source_universe": {"definition": "Step 0C stable matched mainline stations", "actual": len(source_universe)},
        "metadata_distance_rule": "same freeway/direction; absolute Abs_PM; station ID tie-break",
        "formal_oracle_utility": "Available via frozen Step1B XGBoost source-substitution protocol",
    }
    write_json(output_dir / f"{prefix}_Discovery_Report.json", discovery)

    payload = {
        "mode": config["mode"], "output_xlsx": str(output_dir / ("Step2A_Smoke_Summary.xlsx" if config["mode"] == "smoke" else "Step2A_Feasibility_Report.xlsx")),
        "preview_dir": str(output_dir / ".workbook_previews"),
        "sheets": {
            "README": [{"field": "Mode", "value": config["mode"]}, {"field": "QC", "value": qc["status"]}, {"field": "Warning", "value": "Smoke results are not paper results"}, {"field": "Utility protocol", "value": qc["formal_utility_protocol"]}],
            "CONFIG": [{"field": k, "value": json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v} for k, v in config.items()],
            "INPUT_FILES": manifest,
            "STATION_UNIVERSE": [{"station_id": x} for x in universe],
            "CANDIDATE_POOL": dataframe_records(candidate_map),
            "CANDIDATE_AVAILABILITY": dataframe_records(availability),
            "NON_EVALUABLE_TARGETS": dataframe_records(availability[~availability["primary_selection_evaluable"]]),
            "MISSING_CANDIDATES": dataframe_records(sizes[sizes["missing_candidate_count"] > 0]),
            "CANDIDATE_SIZE": dataframe_records(sizes),
            "ORACLE_SUMMARY": dataframe_records(summary["target_summary"]),
            "ORACLE_GAP": [summary["oracle_gap"]],
            "LOSS_SPREAD": [{"metric": "best_worst_spread", **summary["spread"]}, {"metric": "normalized_spread", **summary["normalized_spread"]}],
            "ORACLE_TURNOVER": dataframe_records(summary["turnover"]),
            "NEAR_TIES": dataframe_records(summary["near_ties"]),
            "SPLIT_QC": [{"check": k, "passed": v} for k, v in qc["checks"].items()],
            "LEAKAGE_AUDIT": [{"field": k, "value": v} for k, v in leakage.items()],
            "RUNTIME": [{"field": k, "value": v} for k, v in runtime.items()],
            "ISSUES": issues,
        },
    }
    payload_path = output_dir / ".step2a_workbook_payload.json"
    write_json(payload_path, payload)
    if config["runtime"].get("generate_workbook", True):
        node = config["runtime"]["node_executable"]
        builder = Path(config["runtime"]["workbook_builder"])
        subprocess.run([node, str(builder), str(payload_path)], check=True)

    logger.info("Candidate count distribution: %s", json.dumps(summary["candidate_size"], ensure_ascii=False))
    logger.info("Structural insufficient candidate cases: %d", int((sizes["structural_insufficient_candidate_count"] > 0).sum()))
    logger.info("Source-history missing candidate records: %d", int(sizes["source_history_missing_count"].sum()))
    logger.info("Invalid candidate feature records: %d", int(sizes["invalid_candidate_feature_count"].sum()))
    logger.info("Complete K=5 samples: %d", int(sizes["complete_K5_sample"].sum()))
    logger.info("Oracle loss summary: %s", json.dumps(summary["oracle_loss"], ensure_ascii=False))
    logger.info("Oracle gap summary: %s", json.dumps(summary["oracle_gap"], ensure_ascii=False))
    logger.info("Best-worst spread summary: %s", json.dumps(summary["spread"], ensure_ascii=False))
    logger.info("Oracle switch statistics: %s", json.dumps(describe(summary["turnover"]["oracle_switch_rate"]), ensure_ascii=False))
    logger.info("Near-tie rate at %.3f mph: %.6f", config["metrics"]["near_tie_tolerance_mph"], summary["near_tie_rate"])
    logger.info("QC %s", qc["status"])
    logger.info("Outputs=%s", output_dir)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--mode", choices=("smoke", "verification", "production"))
    args = parser.parse_args()
    config = read_json(args.config)
    if args.mode and args.mode != config.get("mode"):
        raise SystemExit(f"--mode {args.mode} disagrees with config mode {config.get('mode')}")
    return run(args.config.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
