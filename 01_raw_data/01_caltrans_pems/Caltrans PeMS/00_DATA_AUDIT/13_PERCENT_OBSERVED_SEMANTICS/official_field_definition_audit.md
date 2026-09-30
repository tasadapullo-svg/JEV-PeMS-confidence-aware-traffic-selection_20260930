# Official field definition audit

Only Caltrans and PeMS official materials are used for definitions.

## Samples

- Definition: Total number of samples received for all lanes.
- Source: https://dot.ca.gov/-/media/dot-media/programs/research-innovation-system-information/documents/final-reports/ca22-task3253-a11y.pdf
- Applicability: Caltrans report Table 8 describes Station Hour; same-named Station 5-Minute field needs direct specification confirmation.
- Status: OFFICIAL_DEFINITION_INCOMPLETE

## % Observed

- Definition: Percentage of 5-minute lane points that were observed, meaning not imputed.
- Source: https://dot.ca.gov/-/media/dot-media/programs/research-innovation-system-information/documents/final-reports/ca22-task3253-a11y.pdf
- Applicability: Definition explicitly names 5-minute lane points within a Station Hour specification; 0 indicates no lane point classified as observed in that aggregate.
- Status: SUPPORTED_WITH_GRANULARITY_CAVEAT

## Total Flow

- Definition: Caltrans Station Hour table: sum of 5-minute flows over the hour; the basic 5-minute rollup normalizes flow by the number of good samples.
- Source: https://dot.ca.gov/-/media/dot-media/programs/research-innovation-system-information/documents/final-reports/ca22-task3253-a11y.pdf
- Applicability: Hourly formula is not the exact 5-minute field definition; do not apply Veh/Hour units to these raw files.
- Status: OFFICIAL_DEFINITION_INCOMPLETE

## Avg Occupancy

- Definition: Caltrans Station Hour table: average of 5-minute station occupancies, a decimal fraction from 0 to 1.
- Source: https://dot.ca.gov/-/media/dot-media/programs/research-innovation-system-information/documents/final-reports/ca22-task3253-a11y.pdf
- Applicability: Exact Station 5-Minute aggregation formula not independently verified.
- Status: OFFICIAL_DEFINITION_INCOMPLETE

## Avg Speed

- Definition: Caltrans Station Hour table: flow-weighted mean of 5-minute station speeds; if flow is zero, arithmetic mean.
- Source: https://dot.ca.gov/-/media/dot-media/programs/research-innovation-system-information/documents/final-reports/ca22-task3253-a11y.pdf
- Applicability: Exact Station 5-Minute aggregation and estimation lineage not independently verified.
- Status: OFFICIAL_DEFINITION_INCOMPLETE

## Estimated data at low observation

- Definition: A Caltrans technical report contrasts direct measurements with estimated data based on surrounding sensors; it excluded low-observation counts because estimates may contain error.
- Source: https://dot.ca.gov/-/media/dot-media/programs/research-innovation-system-information/documents/final-reports/ca22-3141_final_reportv3-a11y.pdf
- Applicability: Supports possibility of neighboring-sensor estimation, not the exact source for any individual Speed, Flow or Occupancy cell.
- Status: SUPPORTED_WITH_RECORD_LEVEL_LIMITATION

## PeMS processing version

- Definition: Caltrans states PeMS 14 updated algorithms used to compute speed compared with PeMS 12.
- Source: https://dot.ca.gov/programs/traffic-operations/mpr/pems-source
- Applicability: The raw file does not carry a per-record algorithm provenance field.
- Status: OFFICIAL_DEFINITION_INCOMPLETE

## Interpretation of `% Observed = 0`

The official wording supports that no 5-minute lane point contributing to the reported percentage was classified as directly observed. Caltrans documentation also establishes that PeMS can provide estimated values using surrounding sensors when direct observations are insufficient. A non-null Speed, Flow, or Occupancy value in a 0% row therefore cannot be certified as direct detector ground truth. The exact algorithm and input source for each such cell are not identifiable from these files: **OFFICIAL_DEFINITION_INCOMPLETE** at record-level lineage.

The reviewed table documents Station Hour fields. It does not independently establish every Station 5-Minute aggregation formula or unit; these are explicitly left unresolved.
