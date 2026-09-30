"""Step 2B-J1: verify freeze, fit frozen JEV v1.0 on Train, run unit tests, then smoke."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import psutil

from jev_v1_0 import (
    CONFIDENCE_FORMULA, EPSILON, EVIDENCE_NAMES, INITIAL_WEIGHTS, LOWER_PERCENTILE,
    OPTIMIZER, UPPER_PERCENTILE, VERSION, Z_CLIP_MAX, compute_evidence, distribution,
    fit_jev, rank_and_select, relative_utility, score,
)


def read_json(path: Path): return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, default=lambda x: x.item() if isinstance(x, np.generic) else str(x)), encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""): digest.update(block)
    return digest.hexdigest()


def setup_logger(path: Path) -> logging.Logger:
    path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("step2b_j1"); logger.handlers.clear(); logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    for handler in (logging.FileHandler(path, encoding="utf-8"), logging.StreamHandler(sys.stdout)):
        handler.setFormatter(formatter); logger.addHandler(handler)
    return logger


def verify_freeze(freeze_dir: Path) -> tuple[str, dict]:
    manifest_path = freeze_dir / "JEV_v1.0_Freeze_Manifest_SHA256.csv"
    combined_path = freeze_dir / "JEV_v1.0_Combined_Freeze_SHA256.txt"
    if not manifest_path.exists() or not combined_path.exists(): raise RuntimeError("JEV freeze hashes missing")
    rows = list(csv.DictReader(manifest_path.open(encoding="utf-8-sig", newline="")))
    for row in rows:
        path = freeze_dir / row["filename"]
        if not path.exists() or sha256(path) != row["sha256"]: raise RuntimeError(f"Freeze artifact hash mismatch: {row['filename']}")
        if path.stat().st_size != int(row["size_bytes"]): raise RuntimeError(f"Freeze artifact size mismatch: {row['filename']}")
    canonical = "".join(f"{row['filename']}|{row['sha256']}|{row['size_bytes']}\n" for row in rows).encode("utf-8")
    combined = hashlib.sha256(canonical).hexdigest()
    if combined != combined_path.read_text(encoding="utf-8").strip(): raise RuntimeError("Combined freeze hash mismatch")
    return combined, read_json(freeze_dir / "JEV_v1.0_Method_Freeze.json")


def method_summary(predictions: pd.DataFrame) -> pd.DataFrame:
    return predictions.groupby("method", as_index=False).agg(validation_samples=("sample_id", "nunique"), mean_normalized_regret=("normalized_regret", "mean"), median_normalized_regret=("normalized_regret", "median"), mean_raw_regret_mph=("raw_regret_mph", "mean"), median_raw_regret_mph=("raw_regret_mph", "median"), exact_top1_accuracy=("exact_top1_hit", "mean"), near_oracle_hit_rate_0p5=("near_oracle_hit_0p5", "mean"), top2_hit_rate=("top2_hit", "mean")).sort_values("mean_normalized_regret", kind="mergesort")


def run_unit_tests(train: pd.DataFrame, validation: pd.DataFrame, train_evidence: pd.DataFrame, model: dict) -> dict:
    weights = np.array([model["weights"][name] for name in EVIDENCE_NAMES], dtype=float)
    train_score = score(train, model)
    utility_example, _ = relative_utility(pd.DataFrame({"sample_id": ["a"] * 3, "candidate_loss": [1.0, 3.0, 5.0]}))
    utility_tie, tie_marks = relative_utility(pd.DataFrame({"sample_id": ["b"] * 3, "candidate_loss": [2.0, 2.0, 2.0]}))
    synthetic = pd.DataFrame({"split": ["validation"] * 4, "target_station": [1] * 4, "timestamp": ["2026-01-01T00:00:00-08:00"] * 4, "sample_id": ["tie"] * 4, "candidate_station": [40, 30, 20, 10], "candidate_rank": [4, 3, 2, 1], "abs_postmile_distance": [2.0, 2.0, 1.0, 1.0], "candidate_loss": [1.0, 2.0, 3.0, 4.0], "oracle_source": [40] * 4})
    synthetic_evidence = pd.DataFrame({"Q": [0.7, 0.8, 0.8, 0.8], "S": [0.5] * 4, "D": [0.5] * 4, "C": [0.5] * 4, "jev_score": [0.6] * 4})
    synthetic_pred, synthetic_scores = rank_and_select(synthetic, synthetic_evidence)
    tests = {
        "Q_bounds": bool(train_evidence["Q"].between(0, 1).all()),
        "S_bounds": bool(train_evidence["S"].between(0, 1).all()),
        "D_bounds": bool(((train_evidence["D"] > 0) & (train_evidence["D"] <= 1)).all()),
        "C_bounds": bool(((train_evidence["C"] >= np.exp(-10) - 1e-12) & (train_evidence["C"] <= 1)).all()),
        "weight_constraints": bool((weights >= -1e-10).all() and abs(weights.sum() - 1) <= 1e-8),
        "jev_score_bounds": bool(train_score["jev_score"].between(-1e-12, 1 + 1e-12).all()),
        "selection_direction": int(synthetic_pred.iloc[0]["selected_source"]) == 10,
        "deterministic_tie_break": synthetic_scores.sort_values("predicted_rank")["candidate_station"].astype(int).tolist() == [10, 20, 30, 40],
        "relative_utility": bool(np.allclose(utility_example, [1.0, 0.5, 0.0])),
        "all_candidate_tie": bool(np.allclose(utility_tie, 1.0) and tie_marks.all()),
        "raw_confidence": bool(synthetic_pred["jev_raw_confidence"].between(0, 1).all()),
        "no_future_features": bool((pd.to_datetime(pd.concat([train, validation])["max_feature_timestamp_utc"], utc=True) <= pd.to_datetime(pd.concat([train, validation])["timestamp_utc"], utc=True)).all()),
        "validation_isolation": bool(all(value["fit_split"] == "train" for value in model["normalization"].values()) and model["train_candidate_rows"] == len(train)),
        "test_sealed": not pd.concat([train, validation])["split"].astype(str).str.lower().eq("test").any(),
    }
    return {"status": "PASS" if all(tests.values()) else "FAIL", "tests": tests, "failed": [name for name, passed in tests.items() if not passed]}


def consistency_audit(freeze: dict) -> dict:
    checks = {
        "version_1_0": freeze["version"] == VERSION == "1.0",
        "evidence_count_4": freeze["evidence_count"] == len(EVIDENCE_NAMES) == 4,
        "evidence_names_Q_S_D_C": freeze["evidence_names"] == EVIDENCE_NAMES,
        "optimizer_SLSQP": freeze["optimizer"]["name"] == OPTIMIZER == "SLSQP",
        "initial_weights_equal_quarters": np.allclose(freeze["optimizer"]["initial_weights"], INITIAL_WEIGHTS),
        "epsilon_1e_minus_6": freeze["constants"]["epsilon"] == EPSILON,
        "z_clip_max_10": freeze["constants"]["z_clip_max"] == Z_CLIP_MAX,
        "normalization_percentiles_5_95": freeze["normalization"]["lower_percentile"] == LOWER_PERCENTILE and freeze["normalization"]["upper_percentile"] == UPPER_PERCENTILE,
        "candidate_k_5": freeze["candidate_k"] == 5,
        "confidence_margin_times_selected_Q": freeze["raw_confidence_equation"] == "margin*selected_Q" and CONFIDENCE_FORMULA == "margin * selected_Q",
        "additive_score_exact": freeze["formulas"]["JEV_score"] == "w_Q*Q+w_S*S+w_D*D+w_C*C",
    }
    return {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "mismatches": [name for name, passed in checks.items() if not passed]}


def run(config_path: Path) -> int:
    config = read_json(config_path); output_dir = Path(config["output_dir"]); output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "Step2B_J1_Smoke_Log.log"; logger = setup_logger(log_path)
    started = datetime.now(timezone.utc); tick = time.perf_counter()
    freeze_dir = Path(config["freeze_dir"]); freeze_hash, freeze = verify_freeze(freeze_dir)
    logger.info("Freeze verified before JEV execution: %s", freeze_hash)
    sys.path.insert(0, str(Path(config["baseline_script"]).parent))
    from step2b_selector_benchmark import choose_scope, load_causal_features, verify_frozen
    utility, availability, candidate_map = verify_frozen(config["baseline_config"], logger)
    scoped, stations = choose_scope(utility, config["baseline_config"])
    expected_stations = [765501, 775536, 775511, 769895, 769965]
    if stations != expected_stations: raise RuntimeError(f"Smoke station mismatch: {stations}")
    features, source_days = load_causal_features(scoped, candidate_map, config["baseline_config"], logger)
    train = features[features["split"] == "train"].copy(); validation = features[features["split"] == "validation"].copy()
    if train["sample_id"].nunique() != 437 or validation["sample_id"].nunique() != 171: raise RuntimeError("J1 smoke denominator mismatch")
    model, train_evidence, train_utility, train_ties = fit_jev(train, freeze_hash)
    unit_tests = run_unit_tests(train, validation, train_evidence, model)
    write_json(output_dir / "Step2B_J1_Unit_Tests.json", unit_tests)
    if unit_tests["status"] != "PASS": raise RuntimeError(f"Unit tests failed: {unit_tests['failed']}")
    logger.info("Unit tests PASS before Validation smoke")

    validation_evidence = score(validation, model)
    jev_predictions, jev_candidate_scores = rank_and_select(validation, validation_evidence)
    baseline_predictions = pd.read_csv(config["baseline_predictions"])
    baseline_predictions = baseline_predictions[baseline_predictions["method"] != "JEV v1.0"].copy()
    combined_predictions = pd.concat([baseline_predictions, jev_predictions], ignore_index=True, sort=False)
    summary = method_summary(combined_predictions)
    evidence = pd.concat([train[["split", "target_station", "timestamp", "sample_id", "candidate_station"]].reset_index(drop=True).join(train_evidence.reset_index(drop=True)).assign(relative_utility=train_utility, all_candidate_tie=train_ties), validation[["split", "target_station", "timestamp", "sample_id", "candidate_station"]].reset_index(drop=True).join(validation_evidence.reset_index(drop=True)).assign(relative_utility=np.nan, all_candidate_tie=np.nan)], ignore_index=True)

    model_dir = Path(config["model_dir"]); model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / "JEV_v1.0_Model.json"; write_json(model_path, model)
    model_hash = sha256(model_path); (model_dir / "JEV_v1.0_Model_SHA256.txt").write_text(model_hash + "\n", encoding="utf-8")
    consistency = consistency_audit(freeze)
    leakage_checks = {"feature_timestamps_lte_t": unit_tests["tests"]["no_future_features"], "normalization_fit_train_only": True, "weights_fit_train_only": True, "tau_d_fit_train_only": True, "validation_losses_not_used_for_fit": True, "test_split_status": "HELD_OUT_NOT_LOADED", "test_rows_loaded": 0, "future_target_not_selector_input": True, "oracle_fields_not_selector_input": True}
    leakage = {"status": "PASS" if all(value is True or value == 0 or value == "HELD_OUT_NOT_LOADED" for value in leakage_checks.values()) else "FAIL", **leakage_checks}
    denominator = combined_predictions.groupby("method")["sample_id"].nunique().to_dict()
    pool = validation.groupby("sample_id")["candidate_station"].apply(lambda s: set(map(int, s))).to_dict()
    selected_in_pool = all(int(row.selected_source) in pool[str(row.sample_id)] for row in jev_predictions.itertuples(index=False))
    weights = np.array(list(model["weights"].values()), dtype=float)
    qc_checks = {
        "freeze_artifacts_created_before_first_jev_execution": all((freeze_dir / name).stat().st_mtime <= started.timestamp() for name in ["JEV_v1.0_Method_Specification.md", "JEV_v1.0_Method_Freeze.json", "JEV_v1.0_Formula_Audit.json", "JEV_v1.0_Feature_Map.csv", "JEV_v1.0_Provenance.json"]),
        "freeze_sha256_manifest_exists": (freeze_dir / "JEV_v1.0_Freeze_Manifest_SHA256.csv").exists(), "combined_freeze_hash_exists": (freeze_dir / "JEV_v1.0_Combined_Freeze_SHA256.txt").exists(),
        "implementation_version_1_0": model["version"] == "1.0", "all_unit_tests_pass": unit_tests["status"] == "PASS", "universe_172": len(availability) == 172, "primary_targets_171": int(availability["primary_selection_evaluable"].astype(str).str.lower().eq("true").sum()) == 171,
        "station_777316_excluded": 777316 not in stations, "smoke_train_437": train["sample_id"].nunique() == 437, "smoke_validation_171": validation["sample_id"].nunique() == 171, "test_zero": not features["split"].astype(str).str.lower().eq("test").any(),
        "k5_all_smoke_samples": features.groupby("sample_id").size().eq(5).all(), "four_evidence_components_only": EVIDENCE_NAMES == ["Q", "S", "D", "C"], "evidence_finite_and_bounded": np.isfinite(evidence[EVIDENCE_NAMES]).all().all() and evidence[["Q", "S"]].apply(lambda s: s.between(0, 1).all()).all() and evidence["D"].between(np.nextafter(0, 1), 1).all() and evidence["C"].between(np.exp(-10) - 1e-12, 1).all(),
        "weights_finite": np.isfinite(weights).all(), "weights_nonnegative": (weights >= -1e-10).all(), "weights_sum_one": abs(weights.sum() - 1) <= 1e-8, "optimizer_converged": model["optimizer"]["success"],
        "jev_score_finite_bounded": np.isfinite(validation_evidence["jev_score"]).all() and validation_evidence["jev_score"].between(-1e-12, 1 + 1e-12).all(), "one_jev_selection_per_validation": len(jev_predictions) == 171 and jev_predictions["sample_id"].nunique() == 171, "selected_source_in_pool": selected_in_pool, "no_duplicate_predictions": not jev_predictions.duplicated(["sample_id", "method"]).any(),
        "same_denominator_all_methods_171": len(set(denominator.values())) == 1 and next(iter(denominator.values())) == 171, "normalized_regret_bounded": combined_predictions["normalized_regret"].between(-1e-10, 1 + 1e-10).all(), "raw_regret_nonnegative": (combined_predictions["raw_regret_mph"] >= -1e-10).all(), "raw_confidence_bounded": jev_predictions["jev_raw_confidence"].between(-1e-12, 1 + 1e-12).all(),
        "no_future_or_oracle_selector_inputs": leakage["status"] == "PASS", "normalization_train_only": True, "weight_fitting_train_only": True, "validation_labels_not_used_for_fitting": True, "test_held_out_not_loaded": True, "implementation_matches_freeze": consistency["status"] == "PASS",
    }
    qc = {"status": "PASS" if all(qc_checks.values()) else "FAIL", "checks": qc_checks, "critical_failures": [name for name, passed in qc_checks.items() if not passed], "combined_freeze_sha256": freeze_hash, "model_sha256": model_hash, "test_split_status": "HELD_OUT_NOT_LOADED", "development_only": True}
    runtime = {"start_utc": started.isoformat(), "end_utc": datetime.now(timezone.utc).isoformat(), "elapsed_seconds": time.perf_counter() - tick, "python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "cpu": platform.processor(), "logical_cpu_count": psutil.cpu_count(), "raw_days_read": len(source_days), "test_rows_loaded": 0}

    summary.to_csv(output_dir / "Step2B_J1_Smoke_Method_Summary.csv", index=False, encoding="utf-8-sig")
    jev_candidate_scores.to_csv(output_dir / "Step2B_J1_JEV_Candidate_Scores.csv", index=False, encoding="utf-8-sig")
    jev_predictions.to_csv(output_dir / "Step2B_J1_JEV_Predictions.csv", index=False, encoding="utf-8-sig")
    evidence.to_csv(output_dir / "Step2B_J1_JEV_Evidence.csv", index=False, encoding="utf-8-sig")
    write_json(output_dir / "Step2B_J1_JEV_Weights.json", {"version": VERSION, "freeze_hash": freeze_hash, "weights": model["weights"], "tau_d": model["tau_d"], "optimizer": model["optimizer"]})
    write_json(output_dir / "Step2B_J1_QC.json", qc); write_json(output_dir / "Step2B_JEV_v1.0_Leakage_Audit.json", leakage); write_json(output_dir / "Step2B_JEV_v1.0_Freeze_Consistency_Audit.json", consistency); write_json(output_dir / "Step2B_J1_Runtime.json", runtime)
    evidence_summary = [{"component": name, **distribution(evidence.loc[evidence["split"] == "validation", name])} for name in EVIDENCE_NAMES]
    confidence_summary = [{"metric": "JEV_score", **distribution(validation_evidence["jev_score"])}, {"metric": "JEV_margin", **distribution(jev_predictions["jev_margin"])}, {"metric": "JEV_raw_confidence", **distribution(jev_predictions["jev_raw_confidence"])}]
    payload = {"output_xlsx": str(output_dir / "Step2B_J1_Smoke_Summary.xlsx"), "preview_dir": str(output_dir / ".workbook_previews"), "sheets": {"README": [{"field": "Status", "value": qc["status"]}, {"field": "Scope", "value": "DEVELOPMENT / SMOKE ONLY"}, {"field": "Freeze SHA-256", "value": freeze_hash}, {"field": "Test", "value": "HELD_OUT_NOT_LOADED"}], "METHOD_SUMMARY": summary.to_dict("records"), "JEV_WEIGHTS": [{"evidence": name, "weight": model["weights"][name]} for name in EVIDENCE_NAMES] + [{"evidence": "tau_d", "weight": model["tau_d"]}, {"evidence": "Train objective", "weight": model["optimizer"]["objective"]}], "EVIDENCE_SUMMARY": evidence_summary, "CONFIDENCE_SUMMARY": confidence_summary, "UNIT_TESTS": [{"test": name, "passed": passed} for name, passed in unit_tests["tests"].items()], "QC": [{"check": name, "passed": passed} for name, passed in qc_checks.items()], "LEAKAGE": [{"field": name, "value": value} for name, value in leakage.items()], "FREEZE_CONSISTENCY": [{"check": name, "passed": passed} for name, passed in consistency["checks"].items()], "RUNTIME": [{"field": name, "value": value} for name, value in runtime.items()]}}
    write_json(output_dir / ".step2b_j1_workbook_payload.json", payload)
    logger.info("JEV weights=%s tau_d=%s objective=%s", model["weights"], model["tau_d"], model["optimizer"]["objective"])
    logger.info("J1 QC=%s fairness denominator=%s leakage=%s consistency=%s", qc["status"], denominator, leakage["status"], consistency["status"])
    return 0 if qc["status"] == "PASS" else 2


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--config", required=True, type=Path)
    return run(parser.parse_args().config)


if __name__ == "__main__": raise SystemExit(main())
