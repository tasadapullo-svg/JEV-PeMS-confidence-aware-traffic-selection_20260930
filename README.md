# JEV Traffic Data Selection and Confidence-Aware Decision Study

This repository contains the organized data, experimental results, evaluation metrics, figure-source data, table-source data, and reproducibility materials associated with the JEV traffic data selection and confidence-aware decision study.

## 1. Overview

This archive organizes the research materials for a traffic-data selection and confidence-aware decision study prepared for submission to *Transportmetrica A: Transport Science*. The project materials include Caltrans PeMS-derived traffic data, training-ready datasets, JEV and baseline experiment outputs, confidence and selection outputs, risk-coverage and calibration metrics, and figure/table source data.

The repository is designed as a traceable research archive rather than a local backup. Files are arranged so that manuscript results can be traced, where the available materials permit, from raw or derived inputs to training data, experiment outputs, metrics, and final figure/table source data.

JEV is treated conservatively in this README: the archive records its observed role in the project files as a selection/decision and confidence-aware evaluation component. Claims about statistical superiority or final scientific conclusions should be taken from the accepted manuscript, not inferred from this repository structure alone.

## 2. Research Objective

The study addresses traffic data or sensor/candidate selection under uncertainty. The repository emphasizes candidate selection correctness, confidence scores, selective decision-making, coverage, risk, risk-coverage evaluation, calibration, and computational efficiency. Exact task definitions should be verified from the experiment configuration and manuscript files before public release.

## 3. Research Workflow

```text
Raw Traffic Data
        ↓
Data Quality Control
        ↓
Station / Sample Screening
        ↓
Training / Validation / Test Construction
        ↓
Feature Preparation
        ↓
Baseline Models
        ↓
JEV Decision Layer
        ↓
Confidence Estimation
        ↓
Selective Decision
        ↓
Coverage Control
        ↓
Risk-Coverage Evaluation
        ↓
Calibration / Efficiency Analysis
        ↓
Figures and Tables
```

## 4. Repository Structure

```text
.
├── 01_raw_data/
├── 02_training_data/
├── 03_intermediate_data/
├── 04_experiment_results/
├── 05_metrics/
├── 06_figure_data/
├── 07_figures/
├── 08_table_data/
├── 09_model_outputs/
├── 10_configs/
├── 11_logs/
├── 12_reproducibility/
└── 99_archive/
```

- `01_raw_data/`: raw-source metadata, Caltrans PeMS audit materials, and other raw-source descriptors. Some provider-origin raw files are registered but not copied pending redistribution review.
- `02_training_data/`: H30/H60 dataset freeze files, train/validation/test split files, features, and targets where identified.
- `03_intermediate_data/`: cleaned, aligned, filtered, feature-engineering, and model-input artifacts where identified.
- `04_experiment_results/`: baseline, JEV, ablation, sensitivity, robustness, selective-prediction, calibration, and runtime result files.
- `05_metrics/`: overall metrics, fixed-coverage metrics, risk-coverage curves, AURC, calibration, and statistical-test files.
- `06_figure_data/`: Fig. 1-Fig. 5 source and processed data folders with per-figure README files.
- `07_figures/`: final figure exports grouped by image format.
- `08_table_data/`: manuscript table source files and per-table README files.
- `09_model_outputs/`: predictions, confidence scores, selections, checkpoints, and model summaries.
- `10_configs/`: experiment, dataset, and seed configuration files.
- `11_logs/`: training, runtime, error, and QC logs.
- `12_reproducibility/`: scripts, manifests, checksum files, and environment-related materials.
- `99_archive/`: files requiring manual classification review. Currently used only when automatic classification is uncertain.

## 5. Data Sources

| ID | Dataset | Provider | Period | Role | Repository Status |
| --- | --- | --- | --- | --- | --- |
| D1 | Caltrans PeMS traffic data and audit materials | Caltrans PeMS | Not automatically verified | Raw external source / audit input | Redistribution status should be verified before public release. |
| D2 | Forecasting dataset freeze H30/H60 | Derived from project data | Not automatically verified | Training/validation/test data | Included where classified; large files are split. |
| D3 | JEV experiment outputs and final-test results | Project-generated | Not automatically verified | Experiment results, metrics, model outputs | Included where classified. |
| D4 | Figure and table source data | Project-generated | Not automatically verified | Manuscript reproduction support | Included where classified. |

## 6. Dataset Scope

| Item | Value |
| --- | --- |
| Raw files | 339 |
| Training files | 134 |
| Experiment result files | 374 |
| Metric files | 91 |
| Figure source files | 55 |
| Final figures | 39 |
| Table source files | 4 |
| Files >=90 MiB in source scan | 12 |
| Files >=90 MiB remaining in repository | 0 |
| Study period | Not automatically verified |
| Stations | Not automatically verified |
| Observations | Not automatically verified |

## 7. Data Preparation

The available files indicate a workflow from Caltrans PeMS data audits and dataset freezing to training-ready H30/H60 datasets, model outputs, and final-test summaries. The archive preserves existing audit files, split files, result files, and configuration files as copied binary artifacts with SHA256 verification. It does not clean, reorder, rewrite, or recompress source data.

Where missing-data QC, duplicate checks, station filtering, temporal filtering, feature engineering, or target-generation artifacts were identified by filename or folder, they were copied into the corresponding repository section. Steps that cannot be reconstructed from explicit scripts are marked as manual or partial.

## 8. Forecast Horizons / Tasks

The archive contains files and folders labeled `H30` and `H60`. The exact horizon definition should be verified from the corresponding experiment configuration before public release.

## 9. Train / Validation / Test Split

Training, validation, and test split files are organized under `02_training_data/`. Leakage-related audit files, where detected, are preserved in experiment, metric, or QC-log sections. No leakage claim is made here unless a specific audit file is reviewed manually and marked as final.

## 10. Experimental Design

### 10.1 Baseline Models

Automatically identified model or baseline labels: Historical Average, Persistence, XGBoost.

Each baseline file is preserved according to its detected role and path. Configuration and output locations are listed in `SOURCE_MANIFEST.csv` and `FILE_INVENTORY.xlsx`.

### 10.2 JEV

The project files identify JEV-related outputs in experiment, model-output, figure-source, and metric folders. In this archive, JEV is documented as a decision/selection layer that is evaluated with confidence, selective-decision, risk-coverage, calibration, and efficiency materials where those outputs exist. Whether JEV directly performs prediction or acts only as a downstream decision layer should be verified from the final manuscript and experiment scripts before public release.

### 10.3 Ablation

Ablation-related files were detected and placed under `04_experiment_results/03_ablation/` and related figure/metric folders when filenames indicated `ablation` or `Step2G`.

### 10.4 Sensitivity Analysis

Sensitivity-related files were detected and placed under `04_experiment_results/04_sensitivity/` when filenames indicated sensitivity analyses.

### 10.5 Robustness Analysis

Robustness, boundary, and failure-profile files were detected and placed under `04_experiment_results/05_robustness/` when identifiable.

### 10.6 Runtime / Efficiency

Runtime, latency, throughput, efficiency, and Pareto-analysis files were detected and placed under `04_experiment_results/08_runtime_efficiency/` or `05_metrics/` according to file role.

## 11. Confidence-Aware Decision Evaluation

Confidence, selection, accept/reject, coverage, risk, risk-coverage, AURC, calibration, and fixed-coverage materials are preserved where detected by filename and path. Fixed coverage levels such as 100%, 50%, 40%, and 20% appear in the source filenames only where copied files explicitly include those labels. Exact definitions and operating-point criteria should be verified from the corresponding configuration and result files.

## 12. Evaluation Metrics

| Metric | Meaning | Repository Location |
| --- | --- | --- |
| AURC | Area under the risk-coverage curve. | 06_figure_data/Fig02/processed_data/fig/图片数据/02_Fig2_Workflow/Step2D_AURC_Summary__02_Fig2_Workflow.csv; 05_metrics/04_AURC/training_data/results/Step2D/production/.workbook_previews/AURC__.workbook_previews.png; 05_metrics/04_AURC/training_data/results/Step2D/smoke/.workbook_previews/AURC__.workbook_previews.png; 05_metrics/04_AURC/training_data/results/Step2D/smoke/Step2D_AURC_Summary__smoke.csv |
| Calibration | Reliability/calibration assessment for confidence scores. | 06_figure_data/Fig02/processed_data/fig/图片数据/02_Fig2_Workflow/Step2C_Calibration_Method_Summary__02_Fig2_Workflow.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_Calibration.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/Step2C_Reliability_Bins__04_Fig4_Confidence_SelectiveRisk.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/Step2C_Reliability_Diagram_SourceData__04_Fig4_Confidence_SelectiveRisk.csv; 05_metrics/05_calibration/training_data/results/FinalTest/workbook_previews/CALIBRATION.png; 04_experiment_results/07_confidence_calibration/training_data/results/Step2C.zip; 04_experiment_results/07_confidence_calibration/training_data/results/Step2C/production/.workbook_previews/ISOTONIC__.workbook_previews.png; 04_experiment_results/07_confidence_calibration/training_data/results/Step2C/production/.workbook_previews/LEAKAGE__.workbook_previews.png |
| Coverage | Fraction or target level of accepted/evaluated decisions. | 01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/14_STEP0C_CHRONOLOGICAL_SPLIT/step0c_station_coverage.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_RiskCoverage_Curve.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_RiskCoverage_FixedCoverage.csv; 05_metrics/03_risk_coverage/training_data/results/FinalTest/workbook_previews/RISK_COVERAGE.png; 05_metrics/02_fixed_coverage_metrics/training_data/results/Step2D/production/.workbook_previews/FIXED_COVERAGE__.workbook_previews.png; 05_metrics/02_fixed_coverage_metrics/training_data/results/Step2D/production/Step2D_Fixed_Coverage_Summary__production.csv; 05_metrics/03_risk_coverage/training_data/results/Step2D/production/Step2D_Risk_Coverage_Curve__production.csv; 05_metrics/02_fixed_coverage_metrics/training_data/results/Step2D/smoke/.workbook_previews/FIXED_COVERAGE__.workbook_previews.png |
| Risk | Observed error or loss among accepted/evaluated decisions. | 01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/99_TEMP/preview_14_Risks.png; 01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/step0b_risks.csv; 07_figures/PNG/fig/历史/fig4/Fig4_JEV_Confidence_SelectiveRisk_MERGED_REAL.png; 06_figure_data/Fig04/source_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/Fig4_operating_points_100_50_40_20.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_Calibration.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_Confidence_Comparisons.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_RiskCoverage_Curve.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_RiskCoverage_FixedCoverage.csv |
| Runtime | Computation time, latency, throughput, or efficiency measure. | 02_training_data/01_H30/Caltrans PeMS/03_FORECASTING_BENCHMARK/10_FULL_H30/00_CPU_RUNTIME_PREFLIGHT/cpu_runtime_estimate.json; 02_training_data/01_H30/Caltrans PeMS/03_FORECASTING_BENCHMARK/10_FULL_H30/00_CPU_RUNTIME_PREFLIGHT/cpu_runtime_preflight.log; 02_training_data/01_H30/Caltrans PeMS/03_FORECASTING_BENCHMARK/10_FULL_H30/00_CPU_RUNTIME_PREFLIGHT/cpu_runtime_profile.csv; 06_figure_data/Fig05/source_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Fig5a_end_to_end_latency_plot_source.csv; 06_figure_data/Fig05/source_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Fig5b_Pareto_plot_source.csv; 06_figure_data/Fig05/source_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Fig5c_Selection_Ablation_plot_source.csv; 06_figure_data/Fig05/processed_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Step2E_Inference_Latency.csv; 06_figure_data/Fig05/processed_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Step2E_Pareto_Analysis.csv |

## 13. Figure Reproduction

| Figure | Panel | Purpose | Source Data | Metric | Script | Final Output |
| --- | --- | --- | --- | --- | --- | --- |
| Fig. 1 | Not automatically verified | Study setup / cohort and task construction. | 06_figure_data/Fig01/plot_config/fig/图片数据/00_README/FIGURE_SUPPORT_AUDIT.txt; 06_figure_data/Fig01/plot_config/fig/图片数据/00_README/README_CN.txt; 06_figure_data/Fig01/source_data/fig/图片数据/00_README/SHA256_MANIFEST.csv; 06_figure_data/Fig01/source_data/fig/图片数据/00_README/SOURCE_DATA_INDEX.csv; 06_figure_data/Fig01/source_data/fig/图片数据/01_Fig1_Study_Setup/Fig1_cohort_task_plot_source.csv; 06_figure_data/Fig01/processed_data/fig/图片数据/01_Fig1_Study_Setup/FinalTest_Cohort_Audit.csv; 06_figure_data/Fig01/plot_config/fig/图片数据/01_Fig1_Study_Setup/NOTE_Fig1_schematic_elements.txt; 06_figure_data/Fig01/processed_data/fig/图片数据/01_Fig1_Study_Setup/Step2A_Candidate_Availability_Audit.csv | 05_metrics/06_statistical_tests/training_data/results/FinalTest/FinalTest_Multiplicity.csv; 05_metrics/01_overall_metrics/training_data/results/FinalTest/FinalTest_Runtime.json; 05_metrics/05_calibration/training_data/results/FinalTest/workbook_previews/CALIBRATION.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/CONFIDENCE_COMPARISONS.png; 05_metrics/06_statistical_tests/training_data/results/FinalTest/workbook_previews/MULTIPLICITY.png; 05_metrics/03_risk_coverage/training_data/results/FinalTest/workbook_previews/RISK_COVERAGE.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/RUNTIME__workbook_previews.png; 05_metrics/01_overall_metrics/training_data/results/Step2A/production/.workbook_previews/RUNTIME__.workbook_previews.png | Manual plotting step. | 07_figures/PNG/fig/历史/fig01.png; 07_figures/PNG/fig/正式图/all/Fig1_FINAL_16x9_300dpi.png; 07_figures/TIFF/fig/正式图/fig01/Fig1_FINAL_16x9_300dpi.tiff; 07_figures/PNG/fig/正式图/fig01/Fig1_FINAL_16x9_600dpi.png; 07_figures/TIFF/fig/正式图/fig01/Fig1_FINAL_16x9_600dpi.tiff; 07_figures/PNG/fig/正式图/JEV_Fig1-Fig5_FINAL_SCI_Multiformat_16x9_20260927.zip |
| Fig. 2 | Not automatically verified | JEV workflow and frozen weights / method summary. | 06_figure_data/Fig02/source_data/fig/图片数据/02_Fig2_Workflow/Fig2_JEV_frozen_weights_plot_source.csv; 06_figure_data/Fig02/source_data/fig/图片数据/02_Fig2_Workflow/FINAL_TEST_PROTOCOL.md; 06_figure_data/Fig02/processed_data/fig/图片数据/02_Fig2_Workflow/FinalTest_QC.json; 06_figure_data/Fig02/plot_config/fig/图片数据/02_Fig2_Workflow/NOTE_Fig2_is_workflow_not_result_plot.txt; 06_figure_data/Fig02/plot_config/fig/图片数据/02_Fig2_Workflow/Stats_Freeze_Config.json; 06_figure_data/Fig02/processed_data/fig/图片数据/02_Fig2_Workflow/Step2B_JEV_Weights__02_Fig2_Workflow.json; 06_figure_data/Fig02/processed_data/fig/图片数据/02_Fig2_Workflow/Step2B_Method_Summary.csv; 06_figure_data/Fig02/processed_data/fig/图片数据/02_Fig2_Workflow/Step2C_Calibration_Method_Summary__02_Fig2_Workflow.csv | 05_metrics/06_statistical_tests/training_data/results/FinalTest/FinalTest_Multiplicity.csv; 05_metrics/01_overall_metrics/training_data/results/FinalTest/FinalTest_Runtime.json; 05_metrics/05_calibration/training_data/results/FinalTest/workbook_previews/CALIBRATION.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/CONFIDENCE_COMPARISONS.png; 05_metrics/06_statistical_tests/training_data/results/FinalTest/workbook_previews/MULTIPLICITY.png; 05_metrics/03_risk_coverage/training_data/results/FinalTest/workbook_previews/RISK_COVERAGE.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/RUNTIME__workbook_previews.png; 05_metrics/01_overall_metrics/training_data/results/Step2A/production/.workbook_previews/RUNTIME__.workbook_previews.png | Manual plotting step. | 07_figures/PNG/fig/历史/fig2/ChatGPT 图像 2026年9月27日 12_55_50.png; 07_figures/PNG/fig/历史/fig2/ChatGPT 图像 2026年9月27日 12_55_56.png; 07_figures/PNG/fig/历史/fig2/ChatGPT 图像 2026年9月27日 12_55_59.png; 07_figures/PNG/fig/历史/fig2/fig2.png; 07_figures/PNG/fig/正式图/all/Fig2_FINAL_16x9_300dpi.png; 07_figures/TIFF/fig/正式图/fig02/Fig2_FINAL_16x9_300dpi.tiff; 07_figures/PNG/fig/正式图/fig02/Fig2_FINAL_16x9_600dpi.png; 07_figures/TIFF/fig/正式图/fig02/Fig2_FINAL_16x9_600dpi.tiff |
| Fig. 3 | Not automatically verified | Selection-reality benchmark and candidate utility. | 06_figure_data/Fig03/plot_config/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/FIG3_SOURCE_MISMATCH_NOTE.txt; 06_figure_data/Fig03/source_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Fig3a_Oracle_Switching_plot_source.csv; 06_figure_data/Fig03/source_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Fig3a_unique_oracle_candidate_counts.csv; 06_figure_data/Fig03/source_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Fig3b_Candidate_Utility_Spread_target_time_plot_source.csv; 06_figure_data/Fig03/processed_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Fig3b_spread_summary.csv; 06_figure_data/Fig03/source_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Fig3c_Selector_Performance_plot_source.csv; 06_figure_data/Fig03/source_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Fig3d_DisplayMeanNR_Differences.csv; 06_figure_data/Fig03/processed_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/FinalTest_Primary_Comparisons.csv | 05_metrics/06_statistical_tests/training_data/results/FinalTest/FinalTest_Multiplicity.csv; 05_metrics/01_overall_metrics/training_data/results/FinalTest/FinalTest_Runtime.json; 05_metrics/05_calibration/training_data/results/FinalTest/workbook_previews/CALIBRATION.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/CONFIDENCE_COMPARISONS.png; 05_metrics/06_statistical_tests/training_data/results/FinalTest/workbook_previews/MULTIPLICITY.png; 05_metrics/03_risk_coverage/training_data/results/FinalTest/workbook_previews/RISK_COVERAGE.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/RUNTIME__workbook_previews.png; 05_metrics/01_overall_metrics/training_data/results/Step2A/production/.workbook_previews/RUNTIME__.workbook_previews.png | Manual plotting step. | 07_figures/PNG/fig/历史/fig3/ChatGPT 图像 2026年9月27日 12_57_10.png; 07_figures/PNG/fig/历史/fig3/ChatGPT 图像 2026年9月27日 12_57_25.png; 07_figures/PNG/fig/历史/fig3/fig3.png; 07_figures/PNG/fig/正式图/all/Fig3_300dpi.png; 07_figures/PNG/fig/正式图/fig03/fig03.png; 07_figures/TIFF/fig/正式图/fig03/历史/Fig3_300dpi.tiff; 07_figures/PNG/fig/正式图/fig03/历史/Fig3_600dpi.png; 07_figures/TIFF/fig/正式图/fig03/历史/Fig3_600dpi.tiff |
| Fig. 4 | Not automatically verified | Confidence, calibration, selective-risk, and risk-coverage evaluation. | 06_figure_data/Fig04/source_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/Fig4_operating_points_100_50_40_20.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_Calibration.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_Confidence_Comparisons.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_RiskCoverage_Curve.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_RiskCoverage_FixedCoverage.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/Step2C_Reliability_Bins__04_Fig4_Confidence_SelectiveRisk.csv; 06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/Step2C_Reliability_Diagram_SourceData__04_Fig4_Confidence_SelectiveRisk.csv; 06_figure_data/Fig04/source_data/fig/图片数据/90_Reference_Images/Fig4_uploaded.png | 05_metrics/06_statistical_tests/training_data/results/FinalTest/FinalTest_Multiplicity.csv; 05_metrics/01_overall_metrics/training_data/results/FinalTest/FinalTest_Runtime.json; 05_metrics/05_calibration/training_data/results/FinalTest/workbook_previews/CALIBRATION.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/CONFIDENCE_COMPARISONS.png; 05_metrics/06_statistical_tests/training_data/results/FinalTest/workbook_previews/MULTIPLICITY.png; 05_metrics/03_risk_coverage/training_data/results/FinalTest/workbook_previews/RISK_COVERAGE.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/RUNTIME__workbook_previews.png; 05_metrics/01_overall_metrics/training_data/results/Step2A/production/.workbook_previews/RUNTIME__.workbook_previews.png | Manual plotting step. | 07_figures/PNG/fig/历史/fig4/ChatGPT 图像 2026年9月27日 13_06_58.png; 07_figures/PNG/fig/历史/fig4/ChatGPT 图像 2026年9月27日 14_11_36.png; 07_figures/PNG/fig/历史/fig4/ChatGPT 图像 2026年9月27日 14_27_26.png; 07_figures/PNG/fig/历史/fig4/Fig4_JEV_Confidence_SelectiveRisk_MERGED_REAL.png; 07_figures/PNG/fig/正式图/all/Fig4_FINAL_16x9_300dpi.png; 07_figures/TIFF/fig/正式图/fig04/Fig4_FINAL_16x9_300dpi.tiff; 07_figures/PNG/fig/正式图/fig04/Fig4_FINAL_16x9_600dpi.png; 07_figures/TIFF/fig/正式图/fig04/Fig4_FINAL_16x9_600dpi.tiff |
| Fig. 5 | Not automatically verified | Runtime efficiency, Pareto analysis, and ablation summaries. | 06_figure_data/Fig05/source_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Fig5a_end_to_end_latency_plot_source.csv; 06_figure_data/Fig05/source_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Fig5b_Pareto_plot_source.csv; 06_figure_data/Fig05/source_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Fig5c_Selection_Ablation_plot_source.csv; 06_figure_data/Fig05/processed_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Step2E_Inference_Latency.csv; 06_figure_data/Fig05/processed_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Step2E_Pareto_Analysis.csv; 06_figure_data/Fig05/processed_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Step2E_Regret_Latency_SourceData.csv; 06_figure_data/Fig05/processed_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Step2E_Throughput.csv; 06_figure_data/Fig05/processed_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Step2G_Ablation_Weights__05_Fig5_Efficiency_Ablation.csv | 05_metrics/06_statistical_tests/training_data/results/FinalTest/FinalTest_Multiplicity.csv; 05_metrics/01_overall_metrics/training_data/results/FinalTest/FinalTest_Runtime.json; 05_metrics/05_calibration/training_data/results/FinalTest/workbook_previews/CALIBRATION.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/CONFIDENCE_COMPARISONS.png; 05_metrics/06_statistical_tests/training_data/results/FinalTest/workbook_previews/MULTIPLICITY.png; 05_metrics/03_risk_coverage/training_data/results/FinalTest/workbook_previews/RISK_COVERAGE.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/RUNTIME__workbook_previews.png; 05_metrics/01_overall_metrics/training_data/results/Step2A/production/.workbook_previews/RUNTIME__.workbook_previews.png | Manual plotting step. | 07_figures/PNG/fig/历史/fig5/ChatGPT 图像 2026年9月27日 13_08_29.png; 07_figures/PNG/fig/正式图/all/Fig5_FINAL_16x9_300dpi.png; 07_figures/TIFF/fig/正式图/fig05/Fig5_FINAL_16x9_300dpi.tiff; 07_figures/PNG/fig/正式图/fig05/Fig5_FINAL_16x9_600dpi.png; 07_figures/TIFF/fig/正式图/fig05/Fig5_FINAL_16x9_600dpi.tiff; 07_figures/PNG/fig/正式图/JEV_Fig1-Fig5_FINAL_SCI_Multiformat_16x9_20260927.zip |

## 14. Table Reproduction

| Table | Purpose | Source Data | Metric | Experiment |
| --- | --- | --- | --- | --- |
| Table 1 | Manuscript table source data; exact table role requires manual verification. | 08_table_data/Supplementary_Tables/processed_data/Caltrans PeMS/00_DATA_AUDIT/11_SUMMARY_TABLES/monthly_data_summary.csv; 08_table_data/Supplementary_Tables/processed_data/Caltrans PeMS/00_DATA_AUDIT/11_SUMMARY_TABLES/quantity_reconciliation.csv; 08_table_data/Supplementary_Tables/processed_data/表数据/JEV_Paper_Tables_and_TableData_FINAL_20260927.xlsx; 08_table_data/Supplementary_Tables/processed_data/表数据/JEV_Paper_Tables_Package_FINAL_20260927.zip | 05_metrics/06_statistical_tests/training_data/results/FinalTest/FinalTest_Multiplicity.csv; 05_metrics/01_overall_metrics/training_data/results/FinalTest/FinalTest_Runtime.json; 05_metrics/05_calibration/training_data/results/FinalTest/workbook_previews/CALIBRATION.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/CONFIDENCE_COMPARISONS.png; 05_metrics/06_statistical_tests/training_data/results/FinalTest/workbook_previews/MULTIPLICITY.png; 05_metrics/03_risk_coverage/training_data/results/FinalTest/workbook_previews/RISK_COVERAGE.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/RUNTIME__workbook_previews.png; 05_metrics/01_overall_metrics/training_data/results/Step2A/production/.workbook_previews/RUNTIME__.workbook_previews.png | 04_experiment_results/02_JEV/training_data/results/FinalTest.zip; 04_experiment_results/02_JEV/training_data/results/FinalTest/FINAL_TEST_COMPLETE.json; 04_experiment_results/02_JEV/training_data/results/FinalTest/FINAL_TEST_OPENED.json; 04_experiment_results/05_robustness/training_data/results/FinalTest/FinalTest_Boundary_Confirmatory.csv; 04_experiment_results/05_robustness/training_data/results/FinalTest/FinalTest_Boundary_Supporting.csv; 04_experiment_results/02_JEV/training_data/results/FinalTest/FinalTest_Claim_Decision_Matrix.csv; 04_experiment_results/01_baselines/training_data/results/FinalTest/FinalTest_Downstream_GRU_Sensitivity.csv; 04_experiment_results/01_baselines/training_data/results/FinalTest/FinalTest_Downstream_XGB.csv |
| Table 2 | Manuscript table source data; exact table role requires manual verification. | 08_table_data/Supplementary_Tables/processed_data/Caltrans PeMS/00_DATA_AUDIT/11_SUMMARY_TABLES/monthly_data_summary.csv; 08_table_data/Supplementary_Tables/processed_data/Caltrans PeMS/00_DATA_AUDIT/11_SUMMARY_TABLES/quantity_reconciliation.csv; 08_table_data/Supplementary_Tables/processed_data/表数据/JEV_Paper_Tables_and_TableData_FINAL_20260927.xlsx; 08_table_data/Supplementary_Tables/processed_data/表数据/JEV_Paper_Tables_Package_FINAL_20260927.zip | 05_metrics/06_statistical_tests/training_data/results/FinalTest/FinalTest_Multiplicity.csv; 05_metrics/01_overall_metrics/training_data/results/FinalTest/FinalTest_Runtime.json; 05_metrics/05_calibration/training_data/results/FinalTest/workbook_previews/CALIBRATION.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/CONFIDENCE_COMPARISONS.png; 05_metrics/06_statistical_tests/training_data/results/FinalTest/workbook_previews/MULTIPLICITY.png; 05_metrics/03_risk_coverage/training_data/results/FinalTest/workbook_previews/RISK_COVERAGE.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/RUNTIME__workbook_previews.png; 05_metrics/01_overall_metrics/training_data/results/Step2A/production/.workbook_previews/RUNTIME__.workbook_previews.png | 04_experiment_results/02_JEV/training_data/results/FinalTest.zip; 04_experiment_results/02_JEV/training_data/results/FinalTest/FINAL_TEST_COMPLETE.json; 04_experiment_results/02_JEV/training_data/results/FinalTest/FINAL_TEST_OPENED.json; 04_experiment_results/05_robustness/training_data/results/FinalTest/FinalTest_Boundary_Confirmatory.csv; 04_experiment_results/05_robustness/training_data/results/FinalTest/FinalTest_Boundary_Supporting.csv; 04_experiment_results/02_JEV/training_data/results/FinalTest/FinalTest_Claim_Decision_Matrix.csv; 04_experiment_results/01_baselines/training_data/results/FinalTest/FinalTest_Downstream_GRU_Sensitivity.csv; 04_experiment_results/01_baselines/training_data/results/FinalTest/FinalTest_Downstream_XGB.csv |
| Table 3 | Manuscript table source data; exact table role requires manual verification. | 08_table_data/Supplementary_Tables/processed_data/Caltrans PeMS/00_DATA_AUDIT/11_SUMMARY_TABLES/monthly_data_summary.csv; 08_table_data/Supplementary_Tables/processed_data/Caltrans PeMS/00_DATA_AUDIT/11_SUMMARY_TABLES/quantity_reconciliation.csv; 08_table_data/Supplementary_Tables/processed_data/表数据/JEV_Paper_Tables_and_TableData_FINAL_20260927.xlsx; 08_table_data/Supplementary_Tables/processed_data/表数据/JEV_Paper_Tables_Package_FINAL_20260927.zip | 05_metrics/06_statistical_tests/training_data/results/FinalTest/FinalTest_Multiplicity.csv; 05_metrics/01_overall_metrics/training_data/results/FinalTest/FinalTest_Runtime.json; 05_metrics/05_calibration/training_data/results/FinalTest/workbook_previews/CALIBRATION.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/CONFIDENCE_COMPARISONS.png; 05_metrics/06_statistical_tests/training_data/results/FinalTest/workbook_previews/MULTIPLICITY.png; 05_metrics/03_risk_coverage/training_data/results/FinalTest/workbook_previews/RISK_COVERAGE.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/RUNTIME__workbook_previews.png; 05_metrics/01_overall_metrics/training_data/results/Step2A/production/.workbook_previews/RUNTIME__.workbook_previews.png | 04_experiment_results/02_JEV/training_data/results/FinalTest.zip; 04_experiment_results/02_JEV/training_data/results/FinalTest/FINAL_TEST_COMPLETE.json; 04_experiment_results/02_JEV/training_data/results/FinalTest/FINAL_TEST_OPENED.json; 04_experiment_results/05_robustness/training_data/results/FinalTest/FinalTest_Boundary_Confirmatory.csv; 04_experiment_results/05_robustness/training_data/results/FinalTest/FinalTest_Boundary_Supporting.csv; 04_experiment_results/02_JEV/training_data/results/FinalTest/FinalTest_Claim_Decision_Matrix.csv; 04_experiment_results/01_baselines/training_data/results/FinalTest/FinalTest_Downstream_GRU_Sensitivity.csv; 04_experiment_results/01_baselines/training_data/results/FinalTest/FinalTest_Downstream_XGB.csv |
| Table 4 | Manuscript table source data; exact table role requires manual verification. | 08_table_data/Supplementary_Tables/processed_data/Caltrans PeMS/00_DATA_AUDIT/11_SUMMARY_TABLES/monthly_data_summary.csv; 08_table_data/Supplementary_Tables/processed_data/Caltrans PeMS/00_DATA_AUDIT/11_SUMMARY_TABLES/quantity_reconciliation.csv; 08_table_data/Supplementary_Tables/processed_data/表数据/JEV_Paper_Tables_and_TableData_FINAL_20260927.xlsx; 08_table_data/Supplementary_Tables/processed_data/表数据/JEV_Paper_Tables_Package_FINAL_20260927.zip | 05_metrics/06_statistical_tests/training_data/results/FinalTest/FinalTest_Multiplicity.csv; 05_metrics/01_overall_metrics/training_data/results/FinalTest/FinalTest_Runtime.json; 05_metrics/05_calibration/training_data/results/FinalTest/workbook_previews/CALIBRATION.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/CONFIDENCE_COMPARISONS.png; 05_metrics/06_statistical_tests/training_data/results/FinalTest/workbook_previews/MULTIPLICITY.png; 05_metrics/03_risk_coverage/training_data/results/FinalTest/workbook_previews/RISK_COVERAGE.png; 05_metrics/01_overall_metrics/training_data/results/FinalTest/workbook_previews/RUNTIME__workbook_previews.png; 05_metrics/01_overall_metrics/training_data/results/Step2A/production/.workbook_previews/RUNTIME__.workbook_previews.png | 04_experiment_results/02_JEV/training_data/results/FinalTest.zip; 04_experiment_results/02_JEV/training_data/results/FinalTest/FINAL_TEST_COMPLETE.json; 04_experiment_results/02_JEV/training_data/results/FinalTest/FINAL_TEST_OPENED.json; 04_experiment_results/05_robustness/training_data/results/FinalTest/FinalTest_Boundary_Confirmatory.csv; 04_experiment_results/05_robustness/training_data/results/FinalTest/FinalTest_Boundary_Supporting.csv; 04_experiment_results/02_JEV/training_data/results/FinalTest/FinalTest_Claim_Decision_Matrix.csv; 04_experiment_results/01_baselines/training_data/results/FinalTest/FinalTest_Downstream_GRU_Sensitivity.csv; 04_experiment_results/01_baselines/training_data/results/FinalTest/FinalTest_Downstream_XGB.csv |

## 15. Model Outputs

Model outputs are organized under `09_model_outputs/` when files were identified as predictions, confidence scores, selections, checkpoints, or model summaries. Run IDs, seeds, horizons, and model names are not inferred unless explicitly present in filenames or configuration files. See `SOURCE_MANIFEST.csv` and `FILE_INVENTORY.xlsx` for file-level locations.

## 16. Reproducibility

### Step 1. Verify File Integrity

Use `SOURCE_MANIFEST.csv`, `LARGE_FILES_MANIFEST.csv`, and `QC_REPORT.md` to verify copied files and split-file parts.

### Step 2. Reassemble Large Files

```bash
python reassemble_large_files.py
```

### Step 3. Prepare Environment

Environment files are included under `12_reproducibility/environment/` if present. Otherwise, manual step required.

### Step 4. Prepare Dataset

Use scripts under `12_reproducibility/scripts/` and dataset files under `02_training_data/` where applicable. Manual step required for any stage without an explicit script.

### Step 5. Run Baselines

Baseline scripts and outputs are included where identified. Manual step required for missing commands or environment definitions.

### Step 6. Run JEV

JEV scripts and outputs are included where identified. Manual step required for missing commands or environment definitions.

### Step 7. Generate Metrics

Metric source files are under `05_metrics/`; scripts are under `12_reproducibility/scripts/` where identified.

### Step 8. Generate Figures

Figure source data are under `06_figure_data/`; final images are under `07_figures/`. Manual plotting step for figures without a confirmed plotting script.

### Step 9. Generate Tables

Table source data are under `08_table_data/`. Manual step required for exact manuscript table-to-sheet verification.

## 17. Large File Handling

The archive uses a 90 MiB safety threshold for ordinary GitHub repositories. Source files were not modified. Large repository copies were converted into byte-level binary parts such as `filename.part001`, `filename.part002`, and `filename.part003`. Reassembled file SHA256 values are verified against the original source SHA256.

See `LARGE_FILES_MANIFEST.csv` for all part-level checksums.

## 18. File Integrity

All copied files are recorded in `SOURCE_MANIFEST.csv`. For ordinary copied files, `source_sha256` and `destination_sha256` must match. For split files, part checksums and reconstruction verification are recorded in `LARGE_FILES_MANIFEST.csv`.

Audit files:

- `SOURCE_MANIFEST.csv`
- `DUPLICATE_REPORT.csv`
- `LARGE_FILES_MANIFEST.csv`
- `QC_REPORT.md`

## 19. Data Dictionary

`DATA_DICTIONARY.md` summarizes safely inspected CSV, XLSX, Parquet, and JSON files, including rows, columns, variable names, data types, date/time columns, date ranges where sampled or available from metadata, missingness when safely sampled, and notes.

## 20. Data Availability

### Publicly Accessible Data

Caltrans PeMS is identified as an external traffic data provider in the project structure. Public access and redistribution conditions must be checked from the provider before release.

### Derived Research Data

The archive includes derived metrics, figure-source data, table-source data, experimental outputs, logs, and scripts where classified.

### Restricted or Redistribution-Unverified Data

Redistribution status should be verified before public release. Raw external provider files are marked `PUBLICATION_REVIEW_REQUIRED` in `classification_plan.csv` and `SOURCE_MANIFEST.csv` when detected.

## 21. Relationship to the Manuscript

| Manuscript Component | Repository Location |
|---|---|
| Raw data | `01_raw_data/` |
| Training data | `02_training_data/` |
| Experiments | `04_experiment_results/` |
| Metrics | `05_metrics/` |
| Figure data | `06_figure_data/` |
| Table data | `08_table_data/` |

Detailed figure and table mappings are provided in `FIGURE_TABLE_MAP.csv`. Mappings marked `PARTIAL` or `REVIEW_REQUIRED` need manual confirmation before public release.

## 22. Versioning

Archive preparation date: 2026-09-30

Experiment version: Not automatically verified.

Run ID: Not automatically verified.

Git commit: Not automatically verified.

## 23. Known Repository Limitations

- Some raw external files may not be redistributable and are marked for publication review.
- Some large files require reconstruction with `reassemble_large_files.py`.
- Some figures and tables may require manual plotting or manual table-to-sheet verification.
- Some intermediate files are preserved for audit rather than direct reproduction.
- Some files require manual classification review.

## 24. Citation

If you use materials from this repository, please cite the associated article once the final bibliographic information becomes available.

## 25. Contact

Contact information will be added before public release.

## 26. Repository QC Status

| Check | Status |
| --- | --- |
| Source files modified | 0 |
| Source files deleted | 0 |
| Source files moved | 0 |
| Copied files | 1103 |
| SHA256 verified | 1103 |
| SHA256 failed | 0 |
| Files >90 MiB | 0 |
| Review-required files | 705 |
| GitHub readiness | PASS WITH WARNINGS |
