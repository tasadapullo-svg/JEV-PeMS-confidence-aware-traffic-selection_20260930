# STEP 0B — % Observed semantics and ground-truth feasibility

## Scope and canonical files

The analysis reads only the 243 files in `canonical_243_files.csv`, one per day from 2026-01-01 through 2026-08-31. Four nonstandard `(1)` copies were SHA256-matched to their canonical counterparts and deleted at the user's request. `excluded_duplicate_files.csv` records them as `DUPLICATE_EXCLUDED_FROM_ANALYSIS`. Raw canonical files were not edited. No model, Jev call, label set, or final station selection was created.

## Official field semantics

A [Caltrans technical report](https://dot.ca.gov/-/media/dot-media/programs/research-innovation-system-information/documents/final-reports/ca22-task3253-a11y.pdf) defines `% Observed` as the share of five-minute lane points actually observed rather than imputed. Its field table also defines Samples, Total Flow, Avg Occupancy, and Avg Speed, but it is a **Station Hour** table. Therefore exact Station 5-Minute formulas and units beyond the directly stated lane-point meaning remain **OFFICIAL_DEFINITION_INCOMPLETE**. A separate [Caltrans report](https://dot.ca.gov/-/media/dot-media/programs/research-innovation-system-information/documents/final-reports/ca22-3141_final_reportv3-a11y.pdf) describes estimated values based on surrounding sensors as distinct from direct measurements. These sources support the possibility of imputed or estimated traffic values when `% Observed = 0`; they do not reveal the exact method or source for an individual Speed, Flow, or Occupancy cell. See `official_field_definition_audit.md` for each definition and its limit.

## ML observation quality

Canonical ML rows: **134,324,329**, ML stations: **1,936**. `% Observed = 0`: **114,694,672 (85.386373%)**. `>=80`: **10.832997%**; `>=90`: **10.107745%**; `=100`: **10.107745%**. The zero-observation fraction by month ranges from **80.16%–87.15%**. Monthly and daily tables show every period; the largest absolute previous-day percentage-point changes are 2026-03-01 (-14.24 pp), 2026-08-30 (+13.23 pp), 2026-02-28 (+11.82 pp), 2026-05-26 (+8.14 pp), 2026-05-29 (-6.79 pp). These are rankings, not thresholded anomaly decisions.

Station profiles: 1,405 stations are zero-observed for every available ML row, 0 are `>=90` for every row, and 403 have at least one adjacent five-minute transition between `0` and `>=90`. Full station and freeway × direction distributions are in the CSV tables.

Samples and variables: among zero-observation rows, Speed non-null is **100.0%**. The paired Speed/Flow/Occupancy distributions for zero and `>=90` observation, and Samples quantiles by observation band, are in `zero_observed_variable_comparison.csv` and `percent_observed_vs_samples.csv`. These comparisons do not establish an imputation method or a causal effect.

Exact repeated-value runs under zero observation: **28,221** Speed/Flow/Occupancy runs last at least 120 minutes. The station table also counts 30- and 60-minute runs. Exact repetition is a flag only, not proof of imputation.

## Input and target quality

At prediction time `t`, low `% Observed` can remain in a candidate degraded-input condition. The future `t+h` value is assessed separately as a candidate target. A non-null speed with low future observation is not automatically accepted as detector ground truth. An aligned target means the future station-time row exists and its `% Observed` is available; it does not certify an independent measurement.

H30 aligned targets: **134,311,835**. H30 target `>=90`: **13,575,300** across **424 stations, 50,902 station-days, 241 days, 18 freeways**. H30 target `=100`: **13,575,300**.

H60 aligned targets: **134,300,219**. H60 target `>=90`: **13,573,518** across **424 stations, 50,912 station-days, 241 days, 18 freeways**. H60 target `=100`: **13,573,518**.

`ground_truth_threshold_sensitivity.csv` compares `=100`, `>=90`, `>=80`, and `>0` without adopting any threshold. Candidate design A permits every input state and requires target `>=90`; design B requires target `=100`. Candidate design C stratifies input observation into 0, 1–49, 50–79, 80–89, 90–99, and 100 while retaining target `>=90`. The design-C matrix shows sample and coverage counts. No design is frozen.

## Metadata-stable cohort

**1,886** canonical ML stations match the previous metadata-stable list. Their zero-observation share is **85.231322%**, versus **85.386373%** in all ML stations. Under target `>=90`, stable stations provide H30 **13,453,767** samples at **420** stations and H60 **13,452,003** samples at **420** stations. Under target `=100`, H30/H60 provide **13,453,767/13,452,003** samples at **420/420** stations. `station_high_observation_target_availability.csv` reports eligible counts and days for every station; its companion table provides P10/P25/median/P75/P90 without a deletion threshold. No final 200-station set is selected.

## Go / No-Go assessment

**GROUND_TRUTH_FEASIBILITY: MEDIUM. JEV_DECISION_GATING_FEASIBILITY: MEDIUM. INPUT_QUALITY_VARIATION: HIGH.** Ratings concern data structure only. Ground-truth HIGH requires both horizons to have at least one million `>=90` targets, at least half of ML stations, 200 days, and five freeways; MEDIUM requires 100,000 targets, 100 stations, 100 days, and three freeways. Jev HIGH additionally requires 100,000 `0`-input to `>=90` target cases at each horizon across 500 stations, 200 days, five freeways, plus 100,000 high-input cases; MEDIUM uses 10,000 cases, 100 stations, 100 days, three freeways. Smaller nonzero cohorts are LOW; absent cohorts are FAIL. These are audit breadth descriptors, not final sample-selection or training thresholds. Chronological out-of-sample forecast errors have not been computed; statistical independence is not established by time separation alone.

## Critical risks

- 85.386373% of ML input rows have % Observed = 0; non-null speed is not direct-observation proof.
- Official sources support observed-versus-imputed semantics, but per-record Speed/Flow/Occupancy estimation lineage and exact Station 5-Minute formulas remain OFFICIAL_DEFINITION_INCOMPLETE.
- H30 0%-input to >=90 target: 18,714 rows across 392 stations; H60: 33,210 rows across 391 stations. These are the directly relevant degraded-input cohorts.
- 28,221 zero-observation exact-value runs last at least 120 minutes across Speed/Flow/Occupancy combined; repetition alone does not identify imputation.

## Recommended next step

Review official-definition caveats and H30/H60 threshold sensitivity; then decide a target-quality policy and chronological study design. Do not freeze 200 stations or train models yet.
