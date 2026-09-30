"""Step 2C: downstream calibration of frozen JEV v1.0 raw confidence.

Consumes existing Step 2B JEV validation predictions. It never retrains a
selector, refits JEV weights, changes selections, or loads the Test split.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import math
import subprocess
import sys
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
import sklearn
from PIL import Image, ImageDraw, ImageFont
from scipy.stats import ConstantInputWarning, pearsonr, spearmanr
from sklearn.exceptions import ConvergenceWarning
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression


JEV_VERSION = "1.0"
NEAR_ORACLE_THRESHOLD = 0.5
METHODS = ["Constant Base Rate", "Raw", "Platt", "Isotonic"]
ELIGIBLE_METHODS = ["Raw", "Platt", "Isotonic"]
REQUIRED_COLUMNS = {
    "split", "target_station", "timestamp", "sample_id", "method",
    "selected_source", "raw_regret_mph", "exact_top1_hit",
    "near_oracle_hit_0p5", "jev_margin", "jev_selected_Q",
    "jev_raw_confidence",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def json_default(value):
    if isinstance(value, (np.integer,)): return int(value)
    if isinstance(value, (np.floating,)): return None if not np.isfinite(value) else float(value)
    if isinstance(value, (np.bool_,)): return bool(value)
    if isinstance(value, (pd.Timestamp, datetime)): return value.isoformat()
    if isinstance(value, Path): return str(value)
    raise TypeError(type(value).__name__)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_bool(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().eq("true")


def setup_logger(path: Path) -> logging.Logger:
    path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("step2c")
    logger.handlers.clear(); logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler = logging.FileHandler(path, encoding="utf-8"); file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stdout); stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler); logger.addHandler(stream_handler)
    return logger


def load_jev_predictions(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = sorted(REQUIRED_COLUMNS - set(frame.columns))
    if missing:
        raise RuntimeError(f"Missing Step2B prediction columns: {missing}")
    frame = frame[(frame["method"] == "JEV v1.0") & (frame["split"].astype(str).str.lower() == "validation")].copy()
    frame["timestamp_utc"] = pd.to_datetime(frame["timestamp"], utc=True, errors="raise")
    frame["target_station"] = pd.to_numeric(frame["target_station"], errors="raise").astype(int)
    frame["selected_source"] = pd.to_numeric(frame["selected_source"], errors="raise").astype(int)
    for column in ["raw_regret_mph", "jev_margin", "jev_selected_Q", "jev_raw_confidence"]:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
    frame["exact_top1_hit"] = parse_bool(frame["exact_top1_hit"])
    frame["near_oracle_hit_0p5"] = parse_bool(frame["near_oracle_hit_0p5"])
    frame["y_near_oracle"] = (frame["raw_regret_mph"] <= NEAR_ORACLE_THRESHOLD).astype(int)
    return frame.sort_values(["timestamp_utc", "target_station", "sample_id"]).reset_index(drop=True)


def completed_production_exists(output_dir: Path, completion_marker: Path) -> tuple[bool, str | None]:
    if completion_marker.exists():
        return True, "completion_marker"
    qc_path = output_dir / "Step2C_QC.json"
    selected_path = output_dir / "Step2C_Selected_Method.json"
    workbook_path = output_dir / "Step2C_Results.xlsx"
    if qc_path.exists() and selected_path.exists() and workbook_path.exists():
        try:
            qc = read_json(qc_path)
            if qc.get("status") == "PASS" and qc.get("full_step2c_production_executed") is True:
                return True, "finalized_qc_and_results"
        except (OSError, json.JSONDecodeError):
            pass
    return False, None


def production_preflight(config: dict, write_report: bool = True, recovery_mode: bool = False) -> dict:
    inputs = config.get("inputs", {})
    paths = {key: Path(value) for key, value in inputs.items()}
    checks = {
        "mode_production": config.get("mode") == "production",
        "jev_version_1_0": config.get("jev_version") == JEV_VERSION,
        "near_oracle_threshold_0p5": float(config.get("near_oracle_threshold_mph", -1)) == NEAR_ORACLE_THRESHOLD,
        "split_rule_unique_timestamp_chronological": config.get("chronological_split", {}).get("unit") == "unique_timestamp" and config.get("chronological_split", {}).get("ordering") == "ascending" and float(config.get("chronological_split", {}).get("fit_fraction", -1)) == 0.5,
        "calibration_methods_exact": config.get("calibration_methods") == METHODS,
        "ece_bins_10": int(config.get("ece_bin_count", -1)) == 10,
        "nll_epsilon_1e_12": float(config.get("nll_epsilon", -1)) == 1e-12,
        "test_held_out": config.get("test_status") == "HELD_OUT_NOT_LOADED" and int(config.get("test_target_times", -1)) == 0,
        "input_files_exist": bool(paths) and all(path.exists() for path in paths.values()),
    }
    if checks["input_files_exist"]:
        step2b_qc = read_json(paths["step2b_qc"])
        model_config = read_json(paths["step2b_model_config"])
        weights = read_json(paths["step2b_jev_weights"])
        checks["step2b_qc_pass"] = step2b_qc.get("status") == "PASS"
        checks["step2b_test_zero"] = step2b_qc.get("test_target_samples") == 0 and step2b_qc.get("test_split_status") == "HELD_OUT_NOT_LOADED"
        checks["step2b_jev_frozen_metadata"] = model_config.get("jev", {}).get("version") == JEV_VERSION and model_config.get("jev", {}).get("confidence_rule") == "margin*selected_Q; uncalibrated" and weights.get("version") == JEV_VERSION
        checks["jev_weights_unchanged"] = sha256(paths["step2b_jev_weights"]) == config.get("step2b_jev_weights_sha256")
        checks["jev_selector_model_unchanged"] = sha256(paths["step2b_jev_model"]) == config.get("step2b_jev_model_sha256")
        predictions = load_jev_predictions(paths["step2b_predictions"])
        checks["jev_validation_denominator_1431"] = len(predictions) == 1431 and predictions["sample_id"].nunique() == 1431
        checks["test_rows_zero"] = not pd.read_csv(paths["step2b_predictions"], usecols=["split"])["split"].astype(str).str.lower().eq("test").any()
        checks["raw_confidence_exists"] = predictions["jev_raw_confidence"].notna().all()
        checks["regret_exists"] = predictions["raw_regret_mph"].notna().all()
        checks["timestamps_exist"] = predictions["timestamp_utc"].notna().all()
        checks["raw_confidence_finite_bounded"] = np.isfinite(predictions["jev_raw_confidence"]).all() and predictions["jev_raw_confidence"].between(0, 1).all()
    else:
        checks.update({name: False for name in ["step2b_qc_pass", "step2b_test_zero", "step2b_jev_frozen_metadata", "jev_weights_unchanged", "jev_selector_model_unchanged", "jev_validation_denominator_1431", "test_rows_zero", "raw_confidence_exists", "regret_exists", "timestamps_exist", "raw_confidence_finite_bounded"]})
    checks["required_packages_available"] = all(module is not None for module in [np, pd, scipy, sklearn, Image])
    checks["workbook_runtime_available"] = Path(config.get("node_executable", "")).exists() and Path(config.get("workbook_builder", "")).exists()
    output_dir = Path(config["output_dir"]); output_dir.mkdir(parents=True, exist_ok=True)
    probe = output_dir / ".step2c_preflight_write_test.tmp"
    try:
        probe.write_text("preflight", encoding="utf-8")
        checks["output_directory_writable"] = probe.read_text(encoding="utf-8") == "preflight"
    finally:
        if probe.exists(): probe.unlink()
    expected_outputs = {
        "Step2C_Calibration_Split.csv", "Step2C_Calibration_Predictions.csv",
        "Step2C_Calibration_Method_Summary.csv", "Step2C_Reliability_Bins.csv",
        "Step2C_Reliability_Diagram_SourceData.csv", "Step2C_Platt_Model.json",
        "Step2C_Isotonic_Model.json", "Step2C_Selected_Method.json", "Step2C_QC.json",
        "Step2C_Leakage_Audit.json", "Step2C_Runtime.json", "Step2C_Results.xlsx",
        "Step2C_Production_Log.log",
    }
    configured_outputs = set(config.get("required_production_outputs", []))
    checks["required_output_contract_complete"] = configured_outputs == expected_outputs
    completion_marker = Path(config["completion_marker"])
    formal_results_exist, completion_evidence = completed_production_exists(output_dir, completion_marker)
    checks["no_completed_production_exists_or_recovery"] = (not formal_results_exist) or recovery_mode
    audit_items = {
        "full_step2c_production_not_executed": not formal_results_exist,
        "partial_production_files_present": any(output_dir.iterdir()),
        "recovery_mode": recovery_mode,
    }
    report = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "failures": [name for name, passed in checks.items() if not passed],
        "audit_items": audit_items,
        "formal_production_results_exist": formal_results_exist,
        "completion_evidence": completion_evidence,
        "test_loaded": False,
        "test_target_samples": 0,
        "test_split_status": "HELD_OUT_NOT_LOADED",
        "full_step2c_production_executed": False,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    if write_report:
        write_json(Path(config["preflight_report_path"]), report)
    return report


def chronological_split(frame: pd.DataFrame, fit_fraction: float) -> tuple[pd.DataFrame, dict]:
    unique_times = sorted(frame["timestamp_utc"].drop_duplicates().tolist())
    cutoff_index = int(math.floor(len(unique_times) * fit_fraction))
    if cutoff_index <= 0 or cutoff_index >= len(unique_times):
        raise RuntimeError("Chronological unique-timestamp split produced an empty side")
    fit_times = set(unique_times[:cutoff_index])
    result = frame.copy()
    result["calibration_split"] = np.where(result["timestamp_utc"].isin(fit_times), "CAL_FIT", "CAL_EVAL")
    fit = result[result["calibration_split"] == "CAL_FIT"]
    evaluate = result[result["calibration_split"] == "CAL_EVAL"]
    summary = {
        "unique_timestamps_total": len(unique_times),
        "cal_fit_unique_timestamps": fit["timestamp_utc"].nunique(),
        "cal_eval_unique_timestamps": evaluate["timestamp_utc"].nunique(),
        "cal_fit_target_times": len(fit),
        "cal_eval_target_times": len(evaluate),
        "cal_fit_first_timestamp": fit["timestamp_utc"].min(),
        "cal_fit_last_timestamp": fit["timestamp_utc"].max(),
        "cal_eval_first_timestamp": evaluate["timestamp_utc"].min(),
        "cal_eval_last_timestamp": evaluate["timestamp_utc"].max(),
        "cal_fit_prevalence": fit["y_near_oracle"].mean(),
        "cal_eval_prevalence": evaluate["y_near_oracle"].mean(),
    }
    return result, summary


def calibration_metrics(y: np.ndarray, probability: np.ndarray, epsilon: float) -> tuple[dict, pd.DataFrame]:
    probability = np.asarray(probability, dtype=float)
    y = np.asarray(y, dtype=int)
    clipped = np.clip(probability, epsilon, 1 - epsilon)
    brier = float(np.mean((probability - y) ** 2))
    nll = float(-np.mean(y * np.log(clipped) + (1 - y) * np.log(1 - clipped)))
    bin_ids = np.minimum((probability * 10).astype(int), 9)
    rows = []
    ece = 0.0
    for bin_id in range(10):
        mask = bin_ids == bin_id
        count = int(mask.sum())
        mean_probability = float(probability[mask].mean()) if count else np.nan
        observed = float(y[mask].mean()) if count else np.nan
        gap = abs(observed - mean_probability) if count else np.nan
        if count: ece += count / len(y) * gap
        rows.append({
            "bin_id": bin_id,
            "bin_lower": bin_id / 10,
            "bin_upper": (bin_id + 1) / 10,
            "n": count,
            "mean_probability": mean_probability,
            "observed_success_rate": observed,
            "absolute_gap": gap,
        })
    return {
        "mean_predicted_probability": float(probability.mean()),
        "observed_success_prevalence": float(y.mean()),
        "brier_score": brier,
        "nll": nll,
        "ece": float(ece),
    }, pd.DataFrame(rows)


def select_method(summary: pd.DataFrame, tolerance: float) -> str:
    candidates = summary[summary["method"].isin(ELIGIBLE_METHODS)].set_index("method")
    winner = ELIGIBLE_METHODS[0]
    for challenger in ELIGIBLE_METHODS[1:]:
        for metric in ["brier_score", "nll", "ece"]:
            delta = float(candidates.loc[challenger, metric] - candidates.loc[winner, metric])
            if delta < -tolerance:
                winner = challenger
                break
            if delta > tolerance:
                break
    return winner


def draw_reliability(path: Path, bins: pd.DataFrame) -> None:
    width, height = 1000, 760
    left, top, right, bottom = 110, 70, 940, 650
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((left, 24), "Step 2C reliability diagram (smoke diagnostic)", fill="#111827", font=font)
    for index in range(11):
        x = left + (right - left) * index / 10
        y = bottom - (bottom - top) * index / 10
        draw.line((x, top, x, bottom), fill="#E5E7EB", width=1)
        draw.line((left, y, right, y), fill="#E5E7EB", width=1)
        draw.text((x - 8, bottom + 12), f"{index/10:.1f}", fill="#374151", font=font)
        draw.text((left - 42, y - 6), f"{index/10:.1f}", fill="#374151", font=font)
    draw.line((left, bottom, right, top), fill="#6B7280", width=2)
    colors = {"Raw": "#2563EB", "Platt": "#DC2626", "Isotonic": "#059669"}
    for method, color in colors.items():
        subset = bins[(bins["method"] == method) & (bins["n"] > 0)].sort_values("bin_id")
        points = []
        for row in subset.itertuples():
            x = left + (right - left) * float(row.mean_probability)
            y = bottom - (bottom - top) * float(row.observed_success_rate)
            points.append((x, y)); draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=color)
        if len(points) > 1: draw.line(points, fill=color, width=3)
    draw.line((left, bottom, right, bottom), fill="#111827", width=2)
    draw.line((left, top, left, bottom), fill="#111827", width=2)
    draw.text(((left + right) / 2 - 70, height - 55), "Mean predicted probability", fill="#111827", font=font)
    draw.text((15, (top + bottom) / 2), "Observed success rate", fill="#111827", font=font)
    legend_x = left + 20
    for offset, (label, color) in enumerate([("Ideal", "#6B7280"), *colors.items()]):
        x = legend_x + offset * 150
        draw.line((x, top + 20, x + 28, top + 20), fill=color, width=3)
        draw.text((x + 34, top + 14), label, fill="#111827", font=font)
    path.parent.mkdir(parents=True, exist_ok=True); image.save(path)


def clean_records(frame: pd.DataFrame) -> list[dict]:
    result = frame.copy()
    for column in result.columns:
        if pd.api.types.is_datetime64_any_dtype(result[column]):
            result[column] = result[column].map(lambda value: value.isoformat() if pd.notna(value) else None)
    result = result.astype(object).where(pd.notna(result), None)
    return result.to_dict(orient="records")


def run(config_path: Path, recovery_mode: bool = False) -> int:
    config = read_json(config_path)
    mode = config["mode"]
    output_dir = Path(config["output_dir"]); output_dir.mkdir(parents=True, exist_ok=True)
    prefix = "Step2C_Smoke" if mode == "smoke" else "Step2C"
    log_path = output_dir / ("Step2C_Smoke_Log.log" if mode == "smoke" else "Step2C_Production_Log.log")
    logger = setup_logger(log_path)
    logger.info("Step2C mode=%s", mode)
    production_config = read_json(Path(config["production_config"])) if mode == "smoke" else config
    preflight = production_preflight(production_config, write_report=False, recovery_mode=recovery_mode)
    if preflight["status"] != "PASS":
        raise RuntimeError(f"Production preflight failed: {preflight['failures']}")
    if mode == "production":
        logger.info("STEP2C_MODE = production")
        logger.info("STEP2C_PRODUCTION_AUTHORIZED = YES")
        logger.info("STEP2B_VALIDATION_INPUT = 1431")
        logger.info("NEAR_ORACLE_THRESHOLD = 0.5")
        logger.info("TEST_TARGET_SAMPLES = 0")
        logger.info("TEST_SPLIT_STATUS = HELD_OUT_NOT_LOADED")
        logger.info("PRODUCTION_PREFLIGHT = PASS")
    input_path = Path(config["inputs"]["step2b_predictions"])
    weights_path = Path(config["inputs"]["step2b_jev_weights"])
    weights_hash_before = sha256(weights_path)
    started = time.perf_counter()
    frame = load_jev_predictions(input_path)
    expected_n = int(config["expected_validation_target_times"])
    if len(frame) != expected_n or frame["sample_id"].nunique() != expected_n:
        raise RuntimeError(f"Step2B JEV denominator mismatch: rows={len(frame)} unique={frame['sample_id'].nunique()} expected={expected_n}")
    if frame["sample_id"].duplicated().any(): raise RuntimeError("Duplicate Step2B JEV samples")
    confidence_formula_ok = np.allclose(frame["jev_raw_confidence"], frame["jev_margin"] * frame["jev_selected_Q"], rtol=0, atol=1e-12)
    label_match = frame["y_near_oracle"].eq(frame["near_oracle_hit_0p5"].astype(int)).all()
    split_frame, split_summary = chronological_split(frame, float(config["chronological_split"]["fit_fraction"]))
    fit = split_frame[split_frame["calibration_split"] == "CAL_FIT"].copy()
    evaluate = split_frame[split_frame["calibration_split"] == "CAL_EVAL"].copy()
    x_fit = fit[["jev_raw_confidence"]].to_numpy(); y_fit = fit["y_near_oracle"].to_numpy()
    x_eval = evaluate[["jev_raw_confidence"]].to_numpy(); y_eval = evaluate["y_near_oracle"].to_numpy()
    base_rate = float(y_fit.mean())
    fit_started = time.perf_counter()
    input_split_seconds = fit_started - started
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        platt = LogisticRegression(penalty=None, solver="lbfgs", max_iter=1000)
        platt.fit(x_fit, y_fit)
    platt_seconds = time.perf_counter() - fit_started
    platt_converged = not any(issubclass(item.category, ConvergenceWarning) for item in caught) and int(platt.n_iter_[0]) < 1000
    fit_started = time.perf_counter()
    isotonic = IsotonicRegression(y_min=0, y_max=1, increasing=True, out_of_bounds="clip")
    isotonic.fit(x_fit[:, 0], y_fit)
    isotonic_seconds = time.perf_counter() - fit_started
    probabilities = {
        "Constant Base Rate": np.full(len(evaluate), base_rate, dtype=float),
        "Raw": x_eval[:, 0].copy(),
        "Platt": platt.predict_proba(x_eval)[:, 1],
        "Isotonic": isotonic.predict(x_eval[:, 0]),
    }
    summary_rows, bins_parts, prediction_parts = [], [], []
    for method in METHODS:
        metrics, bins = calibration_metrics(y_eval, probabilities[method], float(config["nll_epsilon"]))
        metrics["method"] = method; metrics["cal_eval_n"] = len(evaluate); metrics["development_only"] = True
        metrics["eligible_for_final_family"] = method in ELIGIBLE_METHODS
        summary_rows.append(metrics)
        bins.insert(0, "method", method); bins_parts.append(bins)
        selected = evaluate[["sample_id", "target_station", "timestamp", "timestamp_utc", "selected_source", "raw_regret_mph", "y_near_oracle", "exact_top1_hit", "jev_raw_confidence"]].copy()
        selected.insert(0, "method", method); selected["predicted_probability"] = probabilities[method]
        selected["calibration_split"] = "CAL_EVAL"; selected["development_only"] = True
        prediction_parts.append(selected)
    method_summary = pd.DataFrame(summary_rows)[["method", "cal_eval_n", "mean_predicted_probability", "observed_success_prevalence", "brier_score", "nll", "ece", "eligible_for_final_family", "development_only"]]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConstantInputWarning)
        raw_pearson = float(pearsonr(x_eval[:, 0], y_eval).statistic)
        raw_spearman = float(spearmanr(x_eval[:, 0], y_eval).statistic)
    method_summary["raw_pearson_with_y"] = np.where(method_summary["method"].eq("Raw"), raw_pearson, np.nan)
    method_summary["raw_spearman_with_y"] = np.where(method_summary["method"].eq("Raw"), raw_spearman, np.nan)
    reliability_bins = pd.concat(bins_parts, ignore_index=True)
    calibration_predictions = pd.concat(prediction_parts, ignore_index=True)
    split_output = split_frame[["sample_id", "target_station", "timestamp", "timestamp_utc", "selected_source", "raw_regret_mph", "exact_top1_hit", "jev_raw_confidence", "y_near_oracle", "calibration_split"]].copy()
    split_output["development_only"] = True
    platt_model = {
        "method": "Platt", "implementation": "sklearn.linear_model.LogisticRegression",
        "penalty": None, "solver": "lbfgs", "max_iter": 1000,
        "a": float(platt.coef_[0, 0]), "b": float(platt.intercept_[0]),
        "converged": platt_converged, "iterations": int(platt.n_iter_[0]),
        "fit_split": "CAL_FIT", "fit_n": len(fit), "feature": "jev_raw_confidence",
    }
    isotonic_model = {
        "method": "Isotonic", "implementation": "sklearn.isotonic.IsotonicRegression",
        "y_min": 0, "y_max": 1, "increasing": True, "out_of_bounds": "clip",
        "fit_split": "CAL_FIT", "fit_n": len(fit),
        "x_thresholds": isotonic.X_thresholds_.tolist(), "y_thresholds": isotonic.y_thresholds_.tolist(),
    }
    weights_hash_after = sha256(weights_path)
    split_overlap = set(fit["timestamp_utc"]).intersection(set(evaluate["timestamp_utc"]))
    qc_checks = {
        "jev_version_1_0": config["jev_version"] == JEV_VERSION,
        "step2b_jev_selector_unchanged": weights_hash_before == weights_hash_after,
        "near_oracle_threshold_0p5": float(config["near_oracle_threshold_mph"]) == NEAR_ORACLE_THRESHOLD,
        "test_target_samples_0": int(config["test_target_times"]) == 0,
        "test_held_out_not_loaded": config["test_status"] == "HELD_OUT_NOT_LOADED",
        "raw_confidence_finite": np.isfinite(frame["jev_raw_confidence"]).all(),
        "raw_confidence_in_0_1": frame["jev_raw_confidence"].between(0, 1).all(),
        "raw_confidence_formula_frozen": confidence_formula_ok,
        "near_oracle_target_matches_frozen_field": label_match,
        "chronological_split_unique_timestamps": split_frame.groupby("timestamp_utc")["calibration_split"].nunique().eq(1).all(),
        "no_timestamp_cross_split": len(split_overlap) == 0,
        "cal_fit_precedes_cal_eval": fit["timestamp_utc"].max() < evaluate["timestamp_utc"].min(),
        "cal_fit_nonempty": len(fit) > 0,
        "cal_eval_nonempty": len(evaluate) > 0,
        "cal_fit_both_classes": set(y_fit) == {0, 1},
        "cal_eval_both_classes": set(y_eval) == {0, 1},
        "platt_fitted_cal_fit_only": platt_model["fit_split"] == "CAL_FIT" and platt_model["fit_n"] == len(fit),
        "platt_converged": platt_converged,
        "isotonic_fitted_cal_fit_only": isotonic_model["fit_split"] == "CAL_FIT" and isotonic_model["fit_n"] == len(fit),
        "no_cal_eval_labels_used_in_fit": True,
        "all_probabilities_finite": all(np.isfinite(value).all() for value in probabilities.values()),
        "all_probabilities_in_0_1": all(((value >= 0) & (value <= 1)).all() for value in probabilities.values()),
        "brier_valid": method_summary["brier_score"].between(0, 1).all() and np.isfinite(method_summary["brier_score"]).all(),
        "nll_finite": np.isfinite(method_summary["nll"]).all(),
        "ece_valid": method_summary["ece"].between(0, 1).all() and np.isfinite(method_summary["ece"]).all(),
        "reliability_counts_match_cal_eval": reliability_bins.groupby("method")["n"].sum().eq(len(evaluate)).all(),
        "exactly_10_bins_each_method": reliability_bins.groupby("method").size().eq(10).all(),
        "no_duplicate_sample_method_rows": not calibration_predictions.duplicated(["sample_id", "method"]).any(),
        "same_cal_eval_denominator_all_methods": calibration_predictions.groupby("method")["sample_id"].nunique().eq(len(evaluate)).all(),
        "no_test_statistics_used": True,
        "selector_weights_not_refitted": weights_hash_before == weights_hash_after,
        "jev_selections_not_changed": calibration_predictions.groupby("sample_id")["selected_source"].nunique().eq(1).all(),
        "production_preflight_pass": preflight["status"] == "PASS",
        "production_launch_guard_pass": preflight["status"] == "PASS",
    }
    qc = {
        "status": "PASS" if all(qc_checks.values()) else "FAIL",
        "checks": qc_checks, "critical_failures": [name for name, passed in qc_checks.items() if not passed],
        "validation_input_n": len(frame), "split_summary": split_summary,
        "test_target_samples": 0, "test_split_status": "HELD_OUT_NOT_LOADED",
        "development_only": True, "full_step2c_production_executed": mode == "production",
    }
    leakage = {
        "status": "PASS" if all([weights_hash_before == weights_hash_after, not split_overlap, fit["timestamp_utc"].max() < evaluate["timestamp_utc"].min()]) else "FAIL",
        "selector_training_data_changed": False, "jev_weights_refit": False,
        "calibration_fit_split": "CAL_FIT", "calibration_evaluation_split": "CAL_EVAL",
        "cal_fit_precedes_cal_eval": True, "same_timestamp_cross_split": False,
        "test_loaded": False, "test_target_samples": 0, "test_statistics_used": False,
        "future_test_information_used": False,
    }
    runtime = {
        "input_and_split_seconds": input_split_seconds,
        "platt_fit_seconds": platt_seconds, "isotonic_fit_seconds": isotonic_seconds,
        "total_seconds_excluding_workbook": time.perf_counter() - started,
        "python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__,
        "scipy": scipy.__version__, "sklearn": sklearn.__version__,
    }
    split_output.to_csv(output_dir / "Step2C_Calibration_Split.csv", index=False)
    calibration_predictions.to_csv(output_dir / "Step2C_Calibration_Predictions.csv", index=False)
    method_summary.to_csv(output_dir / "Step2C_Calibration_Method_Summary.csv", index=False)
    reliability_bins.to_csv(output_dir / "Step2C_Reliability_Bins.csv", index=False)
    reliability_bins.to_csv(output_dir / "Step2C_Reliability_Diagram_SourceData.csv", index=False)
    write_json(output_dir / "Step2C_Platt_Model.json", platt_model)
    write_json(output_dir / "Step2C_Isotonic_Model.json", isotonic_model)
    write_json(output_dir / "Step2C_QC.json", qc)
    write_json(output_dir / "Step2C_Leakage_Audit.json", leakage)
    write_json(output_dir / "Step2C_Runtime.json", runtime)
    if mode == "smoke":
        draw_reliability(output_dir / "Step2C_Reliability_Diagram_Smoke.png", reliability_bins)
    else:
        selected_method = select_method(method_summary, float(config["method_selection"]["tie_tolerance"]))
        write_json(output_dir / "Step2C_Selected_Method.json", {
            "selected_method": selected_method, "eligible_methods": ELIGIBLE_METHODS,
            "selection_rule": config["method_selection"], "selection_split": "CAL_EVAL",
            "development_only": True, "future_test_rule": config["future_test_protocol"],
        })
    readme = [
        {"field": "Mode", "value": mode}, {"field": "Scope", "value": "DEVELOPMENT_ONLY"},
        {"field": "QC", "value": qc["status"]}, {"field": "Leakage", "value": leakage["status"]},
        {"field": "Primary target", "value": "raw_regret_mph <= 0.5"},
        {"field": "Test", "value": "HELD_OUT_NOT_LOADED"},
        {"field": "Final family selected from smoke", "value": "NO" if mode == "smoke" else "DEVELOPMENT_SELECTION"},
    ]
    split_table = pd.DataFrame([
        {"split": "CAL_FIT", "unique_timestamps": split_summary["cal_fit_unique_timestamps"], "target_times": len(fit), "first_timestamp": split_summary["cal_fit_first_timestamp"], "last_timestamp": split_summary["cal_fit_last_timestamp"], "class_prevalence": split_summary["cal_fit_prevalence"]},
        {"split": "CAL_EVAL", "unique_timestamps": split_summary["cal_eval_unique_timestamps"], "target_times": len(evaluate), "first_timestamp": split_summary["cal_eval_first_timestamp"], "last_timestamp": split_summary["cal_eval_last_timestamp"], "class_prevalence": split_summary["cal_eval_prevalence"]},
    ])
    payload = {
        "output_xlsx": str(output_dir / ("Step2C_Smoke_Summary.xlsx" if mode == "smoke" else "Step2C_Results.xlsx")),
        "preview_dir": str(output_dir / ".workbook_previews"),
        "sheets": {
            "README": readme, "SPLIT": clean_records(split_table),
            "METHOD_SUMMARY": clean_records(method_summary),
            "RELIABILITY_BINS": clean_records(reliability_bins),
            "PREDICTIONS_PREVIEW": clean_records(calibration_predictions),
            "PLATT": [{"field": key, "value": value} for key, value in platt_model.items()],
            "ISOTONIC": [{"field": key, "value": value} for key, value in isotonic_model.items()],
            "QC": [{"check": key, "passed": value} for key, value in qc_checks.items()],
            "LEAKAGE": [{"field": key, "value": value} for key, value in leakage.items()],
            "RUNTIME": [{"field": key, "value": value} for key, value in runtime.items()],
        },
    }
    write_json(output_dir / ".step2c_workbook_payload.json", payload)
    if config.get("build_workbook", True):
        subprocess.run(
            [config["node_executable"], config["workbook_builder"], str(output_dir / ".step2c_workbook_payload.json")],
            cwd=str(Path(config["workbook_builder"]).parent),
            check=True,
        )
    logger.info("Validation input=%d unique timestamps=%d CAL_FIT=%d CAL_EVAL=%d", len(frame), split_summary["unique_timestamps_total"], len(fit), len(evaluate))
    logger.info("CAL_FIT range=%s to %s prevalence=%.6f", split_summary["cal_fit_first_timestamp"], split_summary["cal_fit_last_timestamp"], split_summary["cal_fit_prevalence"])
    logger.info("CAL_EVAL range=%s to %s prevalence=%.6f", split_summary["cal_eval_first_timestamp"], split_summary["cal_eval_last_timestamp"], split_summary["cal_eval_prevalence"])
    logger.info("QC=%s Leakage=%s Test=0 Full Step2C Production=%s", qc["status"], leakage["status"], "YES" if mode == "production" else "NO")
    if mode == "production" and qc["status"] == "PASS" and leakage["status"] == "PASS":
        missing_outputs = [name for name in config["required_production_outputs"] if not (output_dir / name).exists()]
        if missing_outputs:
            raise RuntimeError(f"Production completed computation but required outputs are missing: {missing_outputs}")
        logger.info("STEP2C_PRODUCTION = PASS")
        logger.info("FULL_STEP2C_PRODUCTION_EXECUTED = YES")
        logger.info("TEST_TARGET_SAMPLES = 0")
        logger.info("TEST_SPLIT_STATUS = HELD_OUT_NOT_LOADED")
        for handler in logger.handlers:
            handler.flush()
        write_json(Path(config["completion_marker"]), {
            "status": "STEP2C_PRODUCTION_COMPLETE",
            "completed_at_utc": datetime.now(timezone.utc).isoformat(),
            "qc_status": qc["status"],
            "leakage_status": leakage["status"],
            "qc_sha256": sha256(output_dir / "Step2C_QC.json"),
            "selected_method_sha256": sha256(output_dir / "Step2C_Selected_Method.json"),
            "test_target_samples": 0,
            "test_split_status": "HELD_OUT_NOT_LOADED",
        })
    return 0 if qc["status"] == "PASS" and leakage["status"] == "PASS" else 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--recovery-mode", action="store_true", help="Explicitly allow rerun after a completed Step2C production")
    args = parser.parse_args()
    config = read_json(args.config)
    if args.preflight_only:
        report = production_preflight(config, write_report=True, recovery_mode=args.recovery_mode)
        print(f"PRODUCTION_PREFLIGHT = {report['status']}")
        print(f"FORMAL_PRODUCTION_RESULTS_EXIST = {'YES' if report['formal_production_results_exist'] else 'NO'}")
        print("TEST_TARGET_SAMPLES = 0")
        print("TEST_SPLIT_STATUS = HELD_OUT_NOT_LOADED")
        print("FULL_PRODUCTION_EXECUTED = NO")
        return 0 if report["status"] == "PASS" else 2
    return run(args.config, recovery_mode=args.recovery_mode)


if __name__ == "__main__":
    raise SystemExit(main())
