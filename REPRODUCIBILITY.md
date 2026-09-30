# Reproducibility Guide

## 1. Data Inputs

Data inputs are organized in `01_raw_data/` and `02_training_data/`. Raw external provider files may require redistribution review before public release.

## 2. Data Preparation

Use available audit, QC, and preparation scripts in `12_reproducibility/scripts/`. Manual step required where scripts are absent.

## 3. Train / Validation / Test Split

Split files are organized under `02_training_data/`. Exact split rules should be verified from copied configuration and audit files.

## 4. Baseline Experiments

Baseline outputs and scripts are preserved where identified. Partial reproducibility.

## 5. JEV Experiments

JEV outputs, configs, and scripts are preserved where identified. Partial reproducibility.

## 6. Confidence Estimation

Confidence-related outputs are preserved under `04_experiment_results/`, `05_metrics/`, and `09_model_outputs/` where detected.

## 7. Selective Decision Evaluation

Selection and fixed-coverage files are preserved where detected.

## 8. Risk-Coverage Analysis

Risk-coverage curve and fixed-coverage files are preserved under `05_metrics/03_risk_coverage/` where detected.

## 9. Calibration Analysis

Calibration and reliability files are preserved under `05_metrics/05_calibration/` where detected.

## 10. Runtime Evaluation

Runtime, efficiency, latency, throughput, and Pareto files are preserved where detected.

## 11. Figure Generation

Figure source data are organized under `06_figure_data/`; final figures are under `07_figures/`. Manual plotting step where scripts are missing.

## 12. Table Generation

Table source files are organized under `08_table_data/`. Manual table-to-sheet verification required.

## 13. Integrity Verification

Use `SOURCE_MANIFEST.csv`, `LARGE_FILES_MANIFEST.csv`, `DUPLICATE_REPORT.csv`, and `QC_REPORT.md`.

## 14. Large File Reconstruction

Run:

```bash
python reassemble_large_files.py
```

The script reconstructs split files and checks SHA256 against the original source hash.
