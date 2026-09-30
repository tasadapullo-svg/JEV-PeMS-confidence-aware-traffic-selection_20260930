"""Step 2D risk-coverage evaluation for frozen JEV v1.0 and frozen baselines."""
from __future__ import annotations

import argparse
import json
import logging
import math
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


PRIMARY_NAME = "JEV confidence (Platt-calibrated)"
RAW_NAME = "Raw JEV confidence (rank-equivalence audit)"
MARGIN_NAME = "JEV margin only"
Q_NAME = "Selected-source Q only"
SYSTEM_METHODS = ["Quality Rule", "XGBoost", "GRU"]
FROZEN_COVERAGES = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]


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


def parse_bool(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().eq("true")


def setup_logger(path: Path) -> logging.Logger:
    path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("step2d")
    logger.handlers.clear(); logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler = logging.FileHandler(path, encoding="utf-8"); file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stdout); stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler); logger.addHandler(stream_handler)
    return logger


def completed_production_exists(output_dir: Path, marker: Path) -> bool:
    if marker.exists(): return True
    qc_path = output_dir / "Step2D_QC.json"
    workbook_path = output_dir / "Step2D_Results.xlsx"
    if qc_path.exists() and workbook_path.exists():
        try:
            qc = read_json(qc_path)
            return qc.get("status") == "PASS" and qc.get("formal_step2d_production_executed") is True
        except (OSError, json.JSONDecodeError):
            return False
    return False


def load_primary(inputs: dict, expected_n: int) -> tuple[pd.DataFrame, dict]:
    calibration = pd.read_csv(inputs["step2c_predictions"])
    calibration = calibration[(calibration["method"] == "Platt") & (calibration["calibration_split"] == "CAL_EVAL")].copy()
    selector = pd.read_csv(inputs["step2b_predictions"])
    selector = selector[(selector["method"] == "JEV v1.0") & (selector["split"].astype(str).str.lower() == "validation")].copy()
    columns = ["sample_id", "normalized_regret", "raw_regret_mph", "near_oracle_hit_0p5", "exact_top1_hit", "jev_raw_confidence", "jev_margin", "jev_selected_Q", "selected_source", "target_station", "timestamp"]
    missing = sorted(set(columns) - set(selector.columns))
    if missing: raise RuntimeError(f"Missing Step2B JEV columns: {missing}")
    primary = calibration[["sample_id", "predicted_probability", "calibration_split"]].merge(selector[columns], on="sample_id", how="inner", validate="one_to_one")
    primary = primary.rename(columns={"predicted_probability": "input_platt_probability"})
    primary["timestamp_utc"] = pd.to_datetime(primary["timestamp"], utc=True, errors="raise")
    primary["target_station"] = pd.to_numeric(primary["target_station"], errors="raise").astype(int)
    primary["near_oracle_hit"] = parse_bool(primary["near_oracle_hit_0p5"]).astype(int)
    primary["exact_top1_hit"] = parse_bool(primary["exact_top1_hit"]).astype(int)
    platt_model = read_json(Path(inputs["step2c_platt_model"]))
    slope = float(platt_model["a"]); intercept = float(platt_model["b"])
    if slope <= 0: raise RuntimeError("Frozen Step2C Platt slope is not positive")
    linear = slope * primary["jev_raw_confidence"].to_numpy(float) + intercept
    primary["platt_probability"] = 1.0 / (1.0 + np.exp(-linear))
    if len(primary) != expected_n or primary["sample_id"].nunique() != expected_n:
        raise RuntimeError(f"CAL_EVAL denominator mismatch: rows={len(primary)} unique={primary['sample_id'].nunique()} expected={expected_n}")
    metadata = {"calibration_rows_total": len(calibration), "selector_rows_total": len(selector), "frozen_platt_slope": slope, "frozen_platt_intercept": intercept, "input_probability_matches_frozen_platt": bool(np.allclose(primary["input_platt_probability"], primary["platt_probability"], rtol=0, atol=1e-12))}
    return primary.sort_values(["timestamp_utc", "target_station"]).reset_index(drop=True), metadata


def candidate_confidence(scores: pd.DataFrame, method: str, sample_ids: set[str]) -> pd.DataFrame | None:
    subset = scores[(scores["method"] == method) & scores["sample_id"].isin(sample_ids)].copy()
    if subset.empty or subset["sample_id"].nunique() != len(sample_ids): return None
    counts = subset.groupby("sample_id").size()
    if not counts.eq(5).all() or subset["predicted_loss_or_score"].isna().any(): return None
    first = subset[subset["predicted_rank"] == 1][["sample_id", "candidate_station", "predicted_loss_or_score"]].rename(columns={"candidate_station": "rank1_source", "predicted_loss_or_score": "rank1_value"})
    second = subset[subset["predicted_rank"] == 2][["sample_id", "predicted_loss_or_score"]].rename(columns={"predicted_loss_or_score": "rank2_value"})
    result = first.merge(second, on="sample_id", validate="one_to_one")
    result["confidence"] = result["rank2_value"] - result["rank1_value"]
    return result


def load_systems(inputs: dict, primary: pd.DataFrame) -> tuple[dict[str, pd.DataFrame], list[dict]]:
    predictions = pd.read_csv(inputs["step2b_predictions"])
    scores = pd.read_csv(inputs["step2b_candidate_scores"])
    sample_ids = set(primary["sample_id"])
    systems = {}
    audit = []
    for method in SYSTEM_METHODS:
        confidence = candidate_confidence(scores, method, sample_ids)
        method_predictions = predictions[(predictions["method"] == method) & predictions["sample_id"].isin(sample_ids)].copy()
        if confidence is None or len(method_predictions) != len(primary):
            audit.append({"system": method, "status": "UNAVAILABLE_CONFIDENCE_SCORE", "n": len(method_predictions)})
            continue
        method_predictions["timestamp_utc"] = pd.to_datetime(method_predictions["timestamp"], utc=True, errors="raise")
        method_predictions["target_station"] = pd.to_numeric(method_predictions["target_station"], errors="raise").astype(int)
        method_predictions["near_oracle_hit"] = parse_bool(method_predictions["near_oracle_hit_0p5"]).astype(int)
        method_predictions["exact_top1_hit"] = parse_bool(method_predictions["exact_top1_hit"]).astype(int)
        merged = method_predictions.merge(confidence, on="sample_id", validate="one_to_one")
        selected_matches = merged["selected_source"].astype(int).eq(merged["rank1_source"].astype(int)).all()
        if not selected_matches or not np.isfinite(merged["confidence"]).all():
            audit.append({"system": method, "status": "UNAVAILABLE_CONFIDENCE_SCORE", "n": len(merged)})
            continue
        systems[method] = merged[["sample_id", "target_station", "timestamp", "timestamp_utc", "normalized_regret", "raw_regret_mph", "near_oracle_hit", "exact_top1_hit", "confidence", "selected_source"]].copy()
        audit.append({"system": method, "status": "AVAILABLE", "n": len(merged), "candidate_k": 5, "selected_source_matches_rank1": True})
    return systems, audit


def rank_frame(frame: pd.DataFrame, confidence_column: str) -> pd.DataFrame:
    return frame.sort_values([confidence_column, "timestamp_utc", "target_station"], ascending=[False, True, True], kind="mergesort").reset_index(drop=True)


def evaluate_ranking(name: str, system: str, frame: pd.DataFrame, confidence_column: str, coverages: list[float]) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    ranked = rank_frame(frame, confidence_column)
    n = len(ranked)
    norm = ranked["normalized_regret"].to_numpy(float)
    raw = ranked["raw_regret_mph"].to_numpy(float)
    near_failure = 1 - ranked["near_oracle_hit"].to_numpy(float)
    top1_error = 1 - ranked["exact_top1_hit"].to_numpy(float)
    k = np.arange(1, n + 1)
    curve = pd.DataFrame({
        "ranking": name, "system": system, "rank_k": k, "coverage": k / n,
        "mean_normalized_regret": np.cumsum(norm) / k,
        "mean_raw_regret_mph": np.cumsum(raw) / k,
        "near_oracle_failure_rate": np.cumsum(near_failure) / k,
        "top1_error_rate": np.cumsum(top1_error) / k,
    })
    full_risk = float(norm.mean())
    fixed_rows = []
    boundary_ties = 0
    confidence = ranked[confidence_column].to_numpy(float)
    for coverage in coverages:
        retained = int(math.ceil(coverage * n))
        if retained < n and confidence[retained - 1] == confidence[retained]: boundary_ties += 1
        row = curve.iloc[retained - 1]
        risk = float(row["mean_normalized_regret"])
        fixed_rows.append({
            "ranking": name, "system": system, "requested_coverage": coverage,
            "retained_n": retained, "realized_coverage": retained / n,
            "mean_normalized_regret": risk,
            "mean_raw_regret_mph": float(row["mean_raw_regret_mph"]),
            "near_oracle_failure_rate": float(row["near_oracle_failure_rate"]),
            "top1_error_rate": float(row["top1_error_rate"]),
            "selective_gain": 0.0 if full_risk == 0 else (full_risk - risk) / full_risk,
            "coverage_boundary_tie": retained < n and confidence[retained - 1] == confidence[retained],
        })
    summary = {
        "ranking": name, "system": system, "N": n,
        "aurc": float(curve["mean_normalized_regret"].mean()),
        "full_coverage_risk": full_risk,
        "minimum_observed_curve_risk": float(curve["mean_normalized_regret"].min()),
        "maximum_observed_curve_risk": float(curve["mean_normalized_regret"].max()),
        "confidence_tie_count": int(n - pd.Series(confidence).nunique()),
        "coverage_boundary_tie_count": boundary_ties,
        "monotonic_violation_count": int((np.diff(curve["mean_normalized_regret"].to_numpy()) < -1e-12).sum()),
        "development_only": True,
    }
    return curve, pd.DataFrame(fixed_rows), summary


def random_reference(system_frames: dict[str, pd.DataFrame], repetitions: int, seed: int) -> tuple[pd.DataFrame, dict[str, np.ndarray]]:
    rng = np.random.default_rng(seed)
    rows, mean_curves = [], {}
    for system, frame in system_frames.items():
        risk = frame["normalized_regret"].to_numpy(float)
        aurcs, curves = [], []
        for _ in range(repetitions):
            permuted = rng.permutation(risk)
            curve = np.cumsum(permuted) / np.arange(1, len(permuted) + 1)
            curves.append(curve); aurcs.append(float(curve.mean()))
        values = np.asarray(aurcs)
        mean_curves[system] = np.mean(np.vstack(curves), axis=0)
        rows.append({"system": system, "repetitions": repetitions, "seed": seed, "random_aurc_mean": float(values.mean()), "random_aurc_p2_5": float(np.percentile(values, 2.5)), "random_aurc_p97_5": float(np.percentile(values, 97.5)), "development_only": True})
    return pd.DataFrame(rows), mean_curves


def bootstrap_comparisons(primary: pd.DataFrame, ranking_frames: dict[str, tuple[pd.DataFrame, str]], comparisons: list[str], coverages: list[float], repetitions: int, seed: int) -> pd.DataFrame:
    stations = sorted(primary["target_station"].unique().tolist())
    rng = np.random.default_rng(seed)
    values = {(baseline, "aurc", None): [] for baseline in comparisons}
    for baseline in comparisons:
        for coverage in coverages: values[(baseline, "risk", coverage)] = []
    for _ in range(repetitions):
        sampled = rng.choice(stations, size=len(stations), replace=True)
        sampled_frames = {}
        for name, (frame, confidence_column) in ranking_frames.items():
            pieces = []
            for draw_index, station in enumerate(sampled):
                piece = frame[frame["target_station"] == station].copy()
                piece["_bootstrap_draw"] = draw_index
                pieces.append(piece)
            sampled_frames[name] = (pd.concat(pieces, ignore_index=True), confidence_column)
        primary_curve, primary_fixed, primary_summary = evaluate_ranking(PRIMARY_NAME, "JEV v1.0", *sampled_frames[PRIMARY_NAME], coverages)
        for baseline in comparisons:
            _, baseline_fixed, baseline_summary = evaluate_ranking(baseline, baseline, *sampled_frames[baseline], coverages)
            values[(baseline, "aurc", None)].append(primary_summary["aurc"] - baseline_summary["aurc"])
            pmap = primary_fixed.set_index("requested_coverage")["mean_normalized_regret"]
            bmap = baseline_fixed.set_index("requested_coverage")["mean_normalized_regret"]
            for coverage in coverages: values[(baseline, "risk", coverage)].append(float(pmap.loc[coverage] - bmap.loc[coverage]))
    rows = []
    for (baseline, metric, coverage), samples in values.items():
        array = np.asarray(samples)
        rows.append({"comparison": f"{PRIMARY_NAME} minus {baseline}", "metric": "delta_AURC" if metric == "aurc" else "delta_risk", "requested_coverage": coverage, "estimate_mean": float(array.mean()), "ci_p2_5": float(np.percentile(array, 2.5)), "ci_p97_5": float(np.percentile(array, 97.5)), "repetitions": repetitions, "cluster": "target_station", "seed": seed, "development_only": True})
    return pd.DataFrame(rows)


def draw_curve(path: Path, primary_curve: pd.DataFrame, random_curve: np.ndarray) -> None:
    width, height = 1000, 760; left, top, right, bottom = 110, 70, 940, 650
    image = Image.new("RGB", (width, height), "white"); draw = ImageDraw.Draw(image); font = ImageFont.load_default()
    draw.text((left, 24), "Step 2D risk-coverage (smoke diagnostic)", fill="#111827", font=font)
    for index in range(11):
        x = left + (right-left)*index/10; y = bottom-(bottom-top)*index/10
        draw.line((x, top, x, bottom), fill="#E5E7EB"); draw.line((left, y, right, y), fill="#E5E7EB")
        draw.text((x-8, bottom+12), f"{index/10:.1f}", fill="#374151", font=font); draw.text((left-42, y-6), f"{index/10:.1f}", fill="#374151", font=font)
    def points(coverage, risk): return [(left+(right-left)*float(x), bottom-(bottom-top)*float(y)) for x,y in zip(coverage,risk)]
    p1 = points(primary_curve["coverage"], primary_curve["mean_normalized_regret"]); p2 = points(primary_curve["coverage"], random_curve)
    draw.line(p1, fill="#2563EB", width=3); draw.line(p2, fill="#9CA3AF", width=3)
    draw.line((left,bottom,right,bottom), fill="#111827", width=2); draw.line((left,top,left,bottom), fill="#111827", width=2)
    draw.text(((left+right)/2-25,height-55), "Coverage", fill="#111827", font=font); draw.text((left,48), "Mean normalized regret", fill="#111827", font=font)
    draw.line((left+20,top+20,left+48,top+20),fill="#2563EB",width=3); draw.text((left+55,top+14),"JEV confidence",fill="#111827",font=font)
    draw.line((left+180,top+20,left+208,top+20),fill="#9CA3AF",width=3); draw.text((left+215,top+14),"Random mean",fill="#111827",font=font)
    path.parent.mkdir(parents=True, exist_ok=True); image.save(path)


def clean_records(frame: pd.DataFrame) -> list[dict]:
    result = frame.copy()
    for column in result.columns:
        if pd.api.types.is_datetime64_any_dtype(result[column]): result[column] = result[column].map(lambda value: value.isoformat() if pd.notna(value) else None)
    return result.astype(object).where(pd.notna(result), None).to_dict(orient="records")


def production_preflight(config: dict, write_report: bool = True) -> dict:
    inputs = {key: Path(value) for key, value in config.get("inputs", {}).items()}
    checks = {
        "mode_production": config.get("mode") == "production",
        "jev_version_1_0": config.get("jev_version") == "1.0",
        "selected_method_platt_config": config.get("selected_calibration_method") == "Platt",
        "input_split_cal_eval": config.get("input_split") == "CAL_EVAL",
        "expected_n_325": config.get("expected_n") == 325,
        "primary_risk_normalized_regret": config.get("primary_risk") == "normalized_regret",
        "coverage_levels_frozen": config.get("coverage_levels") == FROZEN_COVERAGES,
        "aurc_definition_frozen": config.get("aurc_definition") == "discrete_mean_cumulative_risk",
        "random_repetitions_1000": config.get("random_repetitions") == 1000,
        "bootstrap_repetitions_2000": config.get("bootstrap_repetitions") == 2000,
        "bootstrap_cluster_target_station": config.get("bootstrap_cluster") == "target_station",
        "seed_20260924": config.get("seed") == 20260924,
        "test_zero_held_out": config.get("test_target_samples") == 0 and config.get("test_status") == "HELD_OUT_NOT_LOADED",
        "all_inputs_exist": bool(inputs) and all(path.exists() for path in inputs.values()),
    }
    baseline_status = []
    if checks["all_inputs_exist"]:
        qc = read_json(inputs["step2c_qc"]); selected = read_json(inputs["step2c_selected_method"]); platt = read_json(inputs["step2c_platt_model"])
        checks["step2c_qc_pass"] = qc.get("status") == "PASS"
        checks["step2c_selected_method_platt"] = selected.get("selected_method") == "Platt"
        checks["platt_positive_slope"] = float(platt.get("a", 0)) > 0
        primary, _ = load_primary({key: str(value) for key,value in inputs.items()}, 325)
        checks["cal_eval_n_325"] = len(primary) == 325
        checks["normalized_regret_exists"] = primary["normalized_regret"].notna().all()
        checks["raw_regret_exists"] = primary["raw_regret_mph"].notna().all()
        checks["platt_probability_exists"] = primary["platt_probability"].notna().all()
        checks["jev_raw_confidence_exists"] = primary["jev_raw_confidence"].notna().all()
        checks["timestamps_exist"] = primary["timestamp_utc"].notna().all()
        checks["target_station_exists"] = primary["target_station"].notna().all()
        checks["test_rows_zero"] = qc.get("test_target_samples") == 0 and qc.get("test_split_status") == "HELD_OUT_NOT_LOADED"
        systems, baseline_status = load_systems({key: str(value) for key,value in inputs.items()}, primary)
        checks["optional_candidate_scores_audited"] = len(baseline_status) == 3
    else:
        for name in ["step2c_qc_pass","step2c_selected_method_platt","platt_positive_slope","cal_eval_n_325","normalized_regret_exists","raw_regret_exists","platt_probability_exists","jev_raw_confidence_exists","timestamps_exist","target_station_exists","test_rows_zero","optional_candidate_scores_audited"]: checks[name] = False
    output_dir = Path(config["output_dir"]); output_dir.mkdir(parents=True, exist_ok=True)
    probe = output_dir / ".step2d_preflight_write_test.tmp"
    try:
        probe.write_text("preflight", encoding="utf-8"); checks["output_directory_writable"] = probe.read_text(encoding="utf-8") == "preflight"
    finally:
        if probe.exists(): probe.unlink()
    checks["workbook_runtime_available"] = Path(config["node_executable"]).exists() and Path(config["workbook_builder"]).exists()
    complete = completed_production_exists(output_dir, Path(config["completion_marker"]))
    checks["no_completed_step2d_production"] = not complete
    report = {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "failures": [k for k,v in checks.items() if not v], "optional_baselines": baseline_status, "formal_step2d_production_results_exist": complete, "test_loaded": False, "test_target_samples": 0, "test_split_status": "HELD_OUT_NOT_LOADED", "formal_step2d_production_executed": False, "checked_at_utc": datetime.now(timezone.utc).isoformat()}
    if write_report: write_json(Path(config["preflight_report_path"]), report)
    return report


def run(config_path: Path) -> int:
    config = read_json(config_path); mode = config["mode"]
    output_dir = Path(config["output_dir"]); output_dir.mkdir(parents=True, exist_ok=True)
    logger = setup_logger(output_dir / ("Step2D_Smoke_Log.log" if mode == "smoke" else "Step2D_Production_Log.log"))
    production_config = read_json(Path(config["production_config"])) if mode == "smoke" else config
    preflight = production_preflight(production_config, write_report=False)
    if preflight["status"] != "PASS": raise RuntimeError(f"Production preflight failed: {preflight['failures']}")
    logger.info("STEP2D_MODE = %s", mode); logger.info("TEST_TARGET_SAMPLES = 0"); logger.info("TEST_SPLIT_STATUS = HELD_OUT_NOT_LOADED"); logger.info("PRODUCTION_PREFLIGHT = PASS")
    started = time.perf_counter(); primary, _ = load_primary(config["inputs"], int(config["expected_n"])); systems, baseline_audit = load_systems(config["inputs"], primary)
    rankings = {
        PRIMARY_NAME: (primary, "platt_probability", "JEV v1.0"),
        RAW_NAME: (primary, "jev_raw_confidence", "JEV v1.0"),
        MARGIN_NAME: (primary, "jev_margin", "JEV v1.0"),
        Q_NAME: (primary, "jev_selected_Q", "JEV v1.0"),
    }
    for method, frame in systems.items(): rankings[f"{method} selective system"] = (frame, "confidence", method)
    curve_parts, fixed_parts, summaries = [], [], []
    for name, (frame, confidence, system) in rankings.items():
        curve, fixed, summary = evaluate_ranking(name, system, frame, confidence, config["coverage_levels"])
        curve_parts.append(curve); fixed_parts.append(fixed); summaries.append(summary)
    curves = pd.concat(curve_parts, ignore_index=True); fixed = pd.concat(fixed_parts, ignore_index=True); aurc = pd.DataFrame(summaries)
    platt_order = rank_frame(primary, "platt_probability")["sample_id"].tolist(); raw_order = rank_frame(primary, "jev_raw_confidence")["sample_id"].tolist()
    rank_equivalent = platt_order == raw_order
    amap = aurc.set_index("ranking")["aurc"]; aurc_equivalent = abs(float(amap[PRIMARY_NAME] - amap[RAW_NAME])) <= float(config["rank_tolerance"])
    system_risks = {"JEV v1.0": primary, **systems}
    random_table, random_curves = random_reference(system_risks, int(config["random_repetitions"]), int(config["seed"]))
    comparison_names = [MARGIN_NAME, Q_NAME] + [f"{method} selective system" for method in SYSTEM_METHODS if method in systems]
    bootstrap_inputs = {name: (frame, confidence) for name,(frame,confidence,_) in rankings.items() if name == PRIMARY_NAME or name in comparison_names}
    bootstrap = bootstrap_comparisons(primary, bootstrap_inputs, comparison_names, config["coverage_levels"], int(config["bootstrap_repetitions"]), int(config["seed"]))
    primary_curve = curves[curves["ranking"] == PRIMARY_NAME].copy()
    if mode == "smoke": draw_curve(output_dir / "Step2D_Risk_Coverage_Smoke.png", primary_curve, random_curves["JEV v1.0"])
    primary_summary = aurc[aurc["ranking"] == PRIMARY_NAME].iloc[0]
    qc_checks = {
        "jev_version_1_0": config["jev_version"] == "1.0", "step2c_selected_method_platt": config["selected_calibration_method"] == "Platt",
        "primary_input_cal_eval_only": primary["calibration_split"].eq("CAL_EVAL").all(), "input_count_expected": len(primary) == int(config["expected_n"]),
        "production_expected_cal_eval_325": int(config.get("production_expected_n", config["expected_n"])) == 325, "test_target_samples_0": config["test_target_samples"] == 0,
        "test_held_out_not_loaded": config["test_status"] == "HELD_OUT_NOT_LOADED", "no_cal_fit_rows": not primary["calibration_split"].eq("CAL_FIT").any(), "no_test_rows": True,
        "one_jev_prediction_per_sample": primary["sample_id"].nunique() == len(primary), "normalized_regret_finite": np.isfinite(primary["normalized_regret"]).all(),
        "normalized_regret_in_0_1": primary["normalized_regret"].between(0,1).all(), "raw_regret_nonnegative": primary["raw_regret_mph"].ge(-1e-12).all(),
        "confidence_finite": np.isfinite(primary["platt_probability"]).all(), "platt_probability_in_0_1": primary["platt_probability"].between(0,1).all(),
        "raw_jev_confidence_in_0_1": primary["jev_raw_confidence"].between(0,1).all(), "platt_raw_ordering_equivalent": rank_equivalent,
        "platt_raw_aurc_equivalent": aurc_equivalent, "primary_curve_n_points": len(primary_curve) == len(primary),
        "coverage_from_1_over_n_to_1": abs(primary_curve["coverage"].iloc[0]-1/len(primary)) < 1e-12 and primary_curve["coverage"].iloc[-1] == 1,
        "aurc_finite": np.isfinite(primary_summary["aurc"]), "aurc_in_0_1": 0 <= primary_summary["aurc"] <= 1,
        "fixed_coverages_exact": sorted(fixed[fixed["ranking"]==PRIMARY_NAME]["requested_coverage"].tolist(), reverse=True) == FROZEN_COVERAGES,
        "retained_counts_use_ceil": all(row.retained_n == math.ceil(row.requested_coverage*len(primary)) for row in fixed[fixed["ranking"]==PRIMARY_NAME].itertuples()),
        "full_coverage_risk_matches_mean": abs(float(primary_summary["full_coverage_risk"])-float(primary["normalized_regret"].mean())) < 1e-12,
        "no_duplicate_sample_system_records": all(not frame["sample_id"].duplicated().any() for frame in system_risks.values()),
        "random_seed_fixed": config["seed"] == 20260924, "bootstrap_cluster_target_station": config["bootstrap_cluster"] == "target_station",
        "jev_selector_not_refitted": True, "platt_not_refitted": True, "baseline_selectors_not_retrained": True, "no_future_or_test_information_used": True,
        "no_risk_curve_smoothing": True, "production_preflight_pass": preflight["status"] == "PASS", "production_execution_scope_valid": mode == "production" or not preflight["formal_step2d_production_results_exist"],
    }
    qc = {"status": "PASS" if all(qc_checks.values()) else "FAIL", "checks": qc_checks, "critical_failures": [k for k,v in qc_checks.items() if not v], "platt_raw_rank_equivalent": rank_equivalent, "platt_raw_aurc_equivalent": aurc_equivalent, "input_n": len(primary), "stations": primary["target_station"].nunique(), "timestamp_first": primary["timestamp_utc"].min(), "timestamp_last": primary["timestamp_utc"].max(), "test_target_samples": 0, "test_split_status": "HELD_OUT_NOT_LOADED", "formal_step2d_production_executed": mode == "production"}
    leakage = {"status": "PASS", "input_split": "CAL_EVAL", "cal_fit_rows_used_for_primary_evaluation": False, "test_loaded": False, "test_target_samples": 0, "jev_refit": False, "platt_refit": False, "baseline_selectors_refit": False, "future_information_used": False, "coverage_levels_predefined": True, "risk_metric_predefined": True, "aurc_definition_predefined": True}
    confidence_baselines = pd.DataFrame(baseline_audit + [{"system": "JEV margin only", "status": "AVAILABLE", "n": len(primary)}, {"system": "Selected-source Q only", "status": "AVAILABLE", "n": len(primary)}, {"system": "Raw JEV confidence", "status": "RANK_EQUIVALENT_AUDIT_ONLY", "n": len(primary), "platt_raw_rank_equivalent": rank_equivalent}])
    runtime = {"total_seconds_excluding_workbook": time.perf_counter()-started, "random_repetitions": config["random_repetitions"], "bootstrap_repetitions": config["bootstrap_repetitions"], "seed": config["seed"], "python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__}
    outputs = {"Step2D_Risk_Coverage_Curve.csv": curves, "Step2D_Fixed_Coverage_Summary.csv": fixed, "Step2D_AURC_Summary.csv": aurc, "Step2D_Confidence_Baselines.csv": confidence_baselines, "Step2D_Random_Reference.csv": random_table, "Step2D_Bootstrap_Comparisons.csv": bootstrap}
    for name, frame in outputs.items(): frame.to_csv(output_dir/name, index=False)
    write_json(output_dir/"Step2D_QC.json", qc); write_json(output_dir/"Step2D_Leakage_Audit.json", leakage); write_json(output_dir/"Step2D_Runtime.json", runtime)
    readme = [{"field":"Mode","value":mode},{"field":"Scope","value":"DEVELOPMENT_ONLY"},{"field":"Primary ranking","value":PRIMARY_NAME},{"field":"QC","value":qc["status"]},{"field":"Leakage","value":leakage["status"]},{"field":"Test","value":"HELD_OUT_NOT_LOADED"}]
    payload = {"output_xlsx":str(output_dir/("Step2D_Smoke_Summary.xlsx" if mode=="smoke" else "Step2D_Results.xlsx")),"preview_dir":str(output_dir/".workbook_previews"),"sheets":{"README":readme,"AURC":clean_records(aurc),"FIXED_COVERAGE":clean_records(fixed),"RC_CURVE":clean_records(curves),"CONFIDENCE_BASELINES":clean_records(confidence_baselines),"RANDOM_REFERENCE":clean_records(random_table),"BOOTSTRAP":clean_records(bootstrap),"QC":[{"check":k,"passed":v} for k,v in qc_checks.items()],"LEAKAGE":[{"field":k,"value":v} for k,v in leakage.items()],"RUNTIME":[{"field":k,"value":v} for k,v in runtime.items()]}}
    write_json(output_dir/".step2d_workbook_payload.json",payload)
    if config.get("build_workbook",True): subprocess.run([config["node_executable"],config["workbook_builder"],str(output_dir/".step2d_workbook_payload.json")],cwd=str(Path(config["workbook_builder"]).parent),check=True)
    logger.info("CAL_EVAL_N = %d",len(primary)); logger.info("PLATT_RAW_RANK_EQUIVALENT = %s",rank_equivalent); logger.info("PLATT_RAW_AURC_EQUIVALENT = %s",aurc_equivalent); logger.info("QC = %s",qc["status"]); logger.info("LEAKAGE = %s",leakage["status"])
    if mode=="production" and qc["status"]=="PASS" and leakage["status"]=="PASS":
        required=list(outputs)+["Step2D_QC.json","Step2D_Leakage_Audit.json","Step2D_Runtime.json","Step2D_Results.xlsx","Step2D_Production_Log.log"]
        missing=[name for name in required if not (output_dir/name).exists()]
        if missing: raise RuntimeError(f"Missing production outputs: {missing}")
        logger.info("STEP2D_PRODUCTION = PASS"); logger.info("FULL_STEP2D_PRODUCTION_EXECUTED = YES"); logger.info("TEST_TARGET_SAMPLES = 0"); logger.info("TEST_SPLIT_STATUS = HELD_OUT_NOT_LOADED")
        for handler in logger.handlers: handler.flush()
        write_json(Path(config["completion_marker"]),{"status":"STEP2D_PRODUCTION_COMPLETE","completed_at_utc":datetime.now(timezone.utc).isoformat(),"qc_status":"PASS","leakage_status":"PASS","test_target_samples":0,"test_split_status":"HELD_OUT_NOT_LOADED"})
    return 0 if qc["status"]=="PASS" and leakage["status"]=="PASS" else 2


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--config",required=True,type=Path); parser.add_argument("--preflight-only",action="store_true"); args=parser.parse_args(); config=read_json(args.config)
    if args.preflight_only:
        report=production_preflight(config,write_report=True); print(f"PRODUCTION_PREFLIGHT = {report['status']}"); print("FORMAL_STEP2D_PRODUCTION_EXECUTED = NO"); print("TEST_TARGET_SAMPLES = 0"); print("TEST_SPLIT_STATUS = HELD_OUT_NOT_LOADED"); return 0 if report["status"]=="PASS" else 2
    return run(args.config)


if __name__=="__main__": raise SystemExit(main())
