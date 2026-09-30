# Data Dictionary

This file was generated from read-only inspection of copied CSV, XLSX, Parquet, and JSON files. Source files were not rewritten.

## file_sha256_manifest.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/01_FILE_INVENTORY/file_sha256_manifest.csv`
- Dataset role: 01_raw_data
- Rows: 247
- Columns: 8
- Column names: filename; date; size_bytes; sha256; duplicate_name; duplicate_date; duplicate_hash; status
- Data types: filename:object; date:object; size_bytes:int64; sha256:object; duplicate_name:bool; duplicate_date:bool; duplicate_hash:bool; status:object
- Units if known: Not automatically verified
- Date/time column: date; duplicate_date
- Date range: 2026-01-01 00:00:00 to 2026-08-31 00:00:00
- Missing values: 4
- Unique identifiers: 
- Notes: 

## raw_file_inventory.xlsx

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/01_FILE_INVENTORY/raw_file_inventory.xlsx`
- Dataset role: 01_raw_data
- Rows: Raw File Inventory:None rows x None columns
- Columns: Workbook
- Column names: Raw File Inventory
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## gzip_integrity_audit.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/02_GZIP_INTEGRITY/gzip_integrity_audit.csv`
- Dataset role: 01_raw_data
- Rows: 247
- Columns: 8
- Column names: filename; date; compressed_size; gzip_open_pass; gzip_full_stream_pass; decompressed_bytes_if_available; error_message; status
- Data types: filename:object; date:object; compressed_size:int64; gzip_open_pass:bool; gzip_full_stream_pass:bool; decompressed_bytes_if_available:int64; error_message:float64; status:object
- Units if known: Not automatically verified
- Date/time column: date
- Date range: 2026-01-01 00:00:00 to 2026-08-31 00:00:00
- Missing values: 251
- Unique identifiers: 
- Notes: 

## schema_by_file.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/03_SCHEMA_AUDIT/schema_by_file.csv`
- Dataset role: 01_raw_data
- Rows: 229
- Columns: 8
- Column names: filename; date; sample_column_counts; sample_rows; lane_numeric_type_errors; schema_signature; parse_errors; status
- Data types: filename:object; date:object; sample_column_counts:object; sample_rows:int64; lane_numeric_type_errors:int64; schema_signature:object; parse_errors:float64; status:object
- Units if known: Not automatically verified
- Date/time column: date
- Date range: 2026-01-01 00:00:00 to 2026-08-31 00:00:00
- Missing values: 8
- Unique identifiers: 
- Notes: 

## station_5min_field_dictionary.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/03_SCHEMA_AUDIT/station_5min_field_dictionary.csv`
- Dataset role: 01_raw_data
- Rows: 52
- Columns: 8
- Column names: column_index; field_name; official_or_inferred_name; data_type; unit; required_for_forecasting; required_for_reliability; notes
- Data types: column_index:int64; field_name:object; official_or_inferred_name:object; data_type:object; unit:object; required_for_forecasting:bool; required_for_reliability:bool; notes:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 28
- Unique identifiers: 
- Notes: 

## date_completeness_by_month.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/04_DATE_COMPLETENESS/date_completeness_by_month.csv`
- Dataset role: 01_raw_data
- Rows: 8
- Columns: 9
- Column names: year_month; expected_days; actual_unique_days; missing_days_count; duplicate_days_count; extra_invalid_days_count; completion_pct; missing_dates; status
- Data types: year_month:object; expected_days:int64; actual_unique_days:int64; missing_days_count:int64; duplicate_days_count:int64; extra_invalid_days_count:int64; completion_pct:float64; missing_dates:float64; status:object
- Units if known: Not automatically verified
- Date/time column: missing_dates
- Date range: NaT to NaT
- Missing values: 8
- Unique identifiers: 
- Notes: 

## duplicate_station_timestamp.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/05_TEMPORAL_QC/duplicate_station_timestamp.csv`
- Dataset role: 01_raw_data
- Rows: 0
- Columns: 4
- Column names: date; station; timestamp; duplicate_count
- Data types: date:object; station:object; timestamp:object; duplicate_count:object
- Units if known: Not automatically verified
- Date/time column: date; timestamp
- Date range: NaT to NaT
- Missing values: 0
- Unique identifiers: 
- Notes: 

## station_temporal_completeness.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/05_TEMPORAL_QC/station_temporal_completeness.csv`
- Dataset role: 01_raw_data
- Rows: 1936
- Columns: 10
- Column names: station; first_seen; last_seen; days_present; expected_intervals; observed_intervals; missing_intervals; completeness_pct; gap_event_count; longest_gap_minutes
- Data types: station:int64; first_seen:object; last_seen:object; days_present:int64; expected_intervals:int64; observed_intervals:int64; missing_intervals:int64; completeness_pct:float64; gap_event_count:int64; longest_gap_minutes:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## daily_station_counts.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/06_STATION_QC/daily_station_counts.csv`
- Dataset role: 01_raw_data
- Rows: 225
- Columns: 7
- Column names: date; all_unique_stations; ml_unique_stations; all_rows; ml_rows; relative_change_previous_day; relative_change_monthly_median
- Data types: date:object; all_unique_stations:int64; ml_unique_stations:int64; all_rows:int64; ml_rows:int64; relative_change_previous_day:float64; relative_change_monthly_median:float64
- Units if known: Not automatically verified
- Date/time column: date
- Date range: 2026-01-01 00:00:00 to 2026-08-31 00:00:00
- Missing values: 12
- Unique identifiers: 
- Notes: 

## district_distribution.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/06_STATION_QC/district_distribution.csv`
- Dataset role: 01_raw_data
- Rows: 1
- Columns: 3
- Column names: district; rows; percentage
- Data types: district:int64; rows:int64; percentage:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## lane_type_distribution.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/06_STATION_QC/lane_type_distribution.csv`
- Dataset role: 01_raw_data
- Rows: 6
- Columns: 4
- Column names: lane_type; rows; unique_stations; percentage
- Data types: lane_type:object; rows:int64; unique_stations:int64; percentage:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## largest_ml_station_count_changes.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/06_STATION_QC/largest_ml_station_count_changes.csv`
- Dataset role: 01_raw_data
- Rows: 20
- Columns: 7
- Column names: date; all_unique_stations; ml_unique_stations; all_rows; ml_rows; relative_change_previous_day; relative_change_monthly_median
- Data types: date:object; all_unique_stations:int64; ml_unique_stations:int64; all_rows:int64; ml_rows:int64; relative_change_previous_day:float64; relative_change_monthly_median:float64
- Units if known: Not automatically verified
- Date/time column: date
- Date range: 2026-01-02 00:00:00 to 2026-07-17 00:00:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## non_district_7_records.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/06_STATION_QC/non_district_7_records.csv`
- Dataset role: 01_raw_data
- Rows: 0
- Columns: 5
- Column names: date; filename; station; district; rows
- Data types: date:object; filename:object; station:object; district:object; rows:object
- Units if known: Not automatically verified
- Date/time column: date
- Date range: NaT to NaT
- Missing values: 0
- Unique identifiers: 
- Notes: 

## traffic_value_anomaly_inventory.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/07_TRAFFIC_VARIABLE_QC/traffic_value_anomaly_inventory.csv`
- Dataset role: 01_raw_data
- Rows: 0
- Columns: 7
- Column names: date; timestamp; station; field; value; reason; source_file
- Data types: date:object; timestamp:object; station:object; field:object; value:object; reason:object; source_file:object
- Units if known: Not automatically verified
- Date/time column: date; timestamp
- Date range: NaT to NaT
- Missing values: 0
- Unique identifiers: 
- Notes: 

## traffic_value_anomaly_summary.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/07_TRAFFIC_VARIABLE_QC/traffic_value_anomaly_summary.csv`
- Dataset role: 01_raw_data
- Rows: 0
- Columns: 3
- Column names: field; reason; flag_rows
- Data types: field:object; reason:object; flag_rows:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## traffic_variable_statistics.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/07_TRAFFIC_VARIABLE_QC/traffic_variable_statistics.csv`
- Dataset role: 01_raw_data
- Rows: 1170
- Columns: 19
- Column names: scope; period; field; N; missing_N; missing_pct; min; P001; P01; P05; P25; median; P75; P95; P99; P999; max; mean; std
- Data types: scope:object; period:object; field:object; N:int64; missing_N:int64; missing_pct:float64; min:float64; P001:float64; P01:float64; P05:float64; P25:float64; median:float64; P75:float64; P95:float64; P99:float64; P999:float64; max:float64; mean:float64; std:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## observed_pct_vs_variable_availability.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/08_PERCENT_OBSERVED_QC/observed_pct_vs_variable_availability.csv`
- Dataset role: 01_raw_data
- Rows: 5
- Columns: 8
- Column names: bin; rows; speed_missing_pct; flow_missing_pct; occupancy_missing_pct; speed_present; flow_present; occupancy_present
- Data types: bin:object; rows:int64; speed_missing_pct:float64; flow_missing_pct:float64; occupancy_missing_pct:float64; speed_present:int64; flow_present:int64; occupancy_present:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## percent_observed_distribution.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/08_PERCENT_OBSERVED_QC/percent_observed_distribution.csv`
- Dataset role: 01_raw_data
- Rows: 9
- Columns: 6
- Column names: bin; rows; percentage; unique_stations; months; days
- Data types: bin:object; rows:int64; percentage:float64; unique_stations:int64; months:int64; days:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## station_percent_observed_profile.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/08_PERCENT_OBSERVED_QC/station_percent_observed_profile.csv`
- Dataset role: 01_raw_data
- Rows: 1936
- Columns: 13
- Column names: station; N; mean; median; P10; P25; P75; P90; pct_eq_100; pct_ge_90; pct_below_80; pct_below_50; pct_eq_0
- Data types: station:int64; N:int64; mean:float64; median:float64; P10:float64; P25:float64; P75:float64; P90:float64; pct_eq_100:float64; pct_ge_90:float64; pct_below_80:float64; pct_below_50:float64; pct_eq_0:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## metadata_schema.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/09_METADATA_MATCH/metadata_schema.csv`
- Dataset role: 01_raw_data
- Rows: 3
- Columns: 3
- Column names: filename; columns; column_count
- Data types: filename:object; columns:object; column_count:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## metadata_snapshot_comparison.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/09_METADATA_MATCH/metadata_snapshot_comparison.csv`
- Dataset role: 01_raw_data
- Rows: 4925
- Columns: 12
- Column names: station; present_in_snapshot_1; present_in_snapshot_2; present_in_snapshot_3; fwy_stable; dir_stable; lat_stable; lon_stable; length_stable; lanes_stable; name_stable; overall_metadata_stable
- Data types: station:int64; present_in_snapshot_1:bool; present_in_snapshot_2:bool; present_in_snapshot_3:bool; fwy_stable:object; dir_stable:object; lat_stable:object; lon_stable:object; length_stable:object; lanes_stable:object; name_stable:object; overall_metadata_stable:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 20923
- Unique identifiers: 
- Notes: 

## station_metadata_join_audit.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/09_METADATA_MATCH/station_metadata_join_audit.csv`
- Dataset role: 01_raw_data
- Rows: 1936
- Columns: 6
- Column names: station; matched_snapshots; multiple_match; metadata_changed; status; snapshots
- Data types: station:int64; matched_snapshots:int64; multiple_match:bool; metadata_changed:bool; status:object; snapshots:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## decision_gating_feature_variation.csv

- Relative path: `02_training_data/06_features/Caltrans PeMS/00_DATA_AUDIT/10_RESEARCH_READINESS/decision_gating_feature_variation.csv`
- Dataset role: 02_training_data
- Rows: 11
- Columns: 5
- Column names: feature; distinct_values; available_rows; variation; note
- Data types: feature:object; distinct_values:int64; available_rows:int64; variation:object; note:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## forecast_target_quality_audit.csv

- Relative path: `02_training_data/07_targets/Caltrans PeMS/00_DATA_AUDIT/10_RESEARCH_READINESS/forecast_target_quality_audit.csv`
- Dataset role: 02_training_data
- Rows: 450
- Columns: 11
- Column names: date; horizon_minutes; origin_rows; matched_targets; missing_targets; target_pct_observed_100; target_pct_observed_ge_90; target_pct_observed_ge_80; target_pct_observed_below_80; target_pct_observed_zero; status
- Data types: date:object; horizon_minutes:int64; origin_rows:int64; matched_targets:int64; missing_targets:int64; target_pct_observed_100:int64; target_pct_observed_ge_90:int64; target_pct_observed_ge_80:int64; target_pct_observed_below_80:int64; target_pct_observed_zero:int64; status:object
- Units if known: Not automatically verified
- Date/time column: date
- Date range: 2026-01-01 00:00:00 to 2026-08-31 00:00:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## ml_candidate_station_pool.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/10_RESEARCH_READINESS/ml_candidate_station_pool.csv`
- Dataset role: 01_raw_data
- Rows: 1936
- Columns: 16
- Column names: station; fwy; direction; latitude; longitude; length; lanes; name; first_seen; last_seen; days_present; temporal_completeness; mean_observed_pct; median_observed_pct; metadata_stable; candidate_status
- Data types: station:int64; fwy:int64; direction:object; latitude:float64; longitude:float64; length:float64; lanes:int64; name:object; first_seen:object; last_seen:object; days_present:int64; temporal_completeness:float64; mean_observed_pct:float64; median_observed_pct:float64; metadata_stable:bool; candidate_status:object
- Units if known: Not automatically verified
- Date/time column: candidate_status
- Date range: NaT to NaT
- Missing values: 4
- Unique identifiers: 
- Notes: 

## readiness_assessment.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/10_RESEARCH_READINESS/readiness_assessment.csv`
- Dataset role: 01_raw_data
- Rows: 13
- Columns: 2
- Column names: dimension; status
- Data types: dimension:object; status:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## monthly_data_summary.csv

- Relative path: `08_table_data/Supplementary_Tables/processed_data/Caltrans PeMS/00_DATA_AUDIT/11_SUMMARY_TABLES/monthly_data_summary.csv`
- Dataset role: 08_table_data
- Rows: 8
- Columns: 16
- Column names: month; expected_days; downloaded_days; gzip_pass_days; total_rows; ML_rows; unique_stations; unique_ML_stations; timestamp_count; speed_missing_pct; flow_missing_pct; occupancy_missing_pct; median_percent_observed; pct_observed_below_80; duplicate_station_time_keys; status
- Data types: month:object; expected_days:int64; downloaded_days:int64; gzip_pass_days:int64; total_rows:int64; ML_rows:int64; unique_stations:int64; unique_ML_stations:int64; timestamp_count:int64; speed_missing_pct:float64; flow_missing_pct:float64; occupancy_missing_pct:float64; median_percent_observed:float64; pct_observed_below_80:float64; duplicate_station_time_keys:int64; status:object
- Units if known: Not automatically verified
- Date/time column: timestamp_count; duplicate_station_time_keys
- Date range: 1970-01-01 00:00:00.000006912 to 1970-01-01 00:00:00.000008916
- Missing values: 0
- Unique identifiers: 
- Notes: 

## quantity_reconciliation.csv

- Relative path: `08_table_data/Supplementary_Tables/processed_data/Caltrans PeMS/00_DATA_AUDIT/11_SUMMARY_TABLES/quantity_reconciliation.csv`
- Dataset role: 08_table_data
- Rows: 3
- Columns: 6
- Column names: check; total; part_1; part_2; part_3; difference
- Data types: check:object; total:int64; part_1:int64; part_2:int64; part_3:int64; difference:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## candidate_design_C_input_strata.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/candidate_design_C_input_strata.csv`
- Dataset role: 01_raw_data
- Rows: 24
- Columns: 10
- Column names: scope; horizon_minutes; input_percent_observed_bin; target_threshold; N; unique_stations; unique_station_days; unique_days; unique_freeways; unique_directions
- Data types: scope:object; horizon_minutes:int64; input_percent_observed_bin:object; target_threshold:object; N:int64; unique_stations:int64; unique_station_days:int64; unique_days:int64; unique_freeways:int64; unique_directions:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## excluded_duplicate_files.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/excluded_duplicate_files.csv`
- Dataset role: 01_raw_data
- Rows: 4
- Columns: 4
- Column names: filename; sha256_from_previous_manifest; status; action
- Data types: filename:object; sha256_from_previous_manifest:object; status:object; action:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## forecast_target_alignment_by_day.csv

- Relative path: `02_training_data/07_targets/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/forecast_target_alignment_by_day.csv`
- Dataset role: 02_training_data
- Rows: 486
- Columns: 5
- Column names: date; horizon_minutes; origin_rows; aligned_targets; missing_targets
- Data types: date:object; horizon_minutes:int64; origin_rows:int64; aligned_targets:int64; missing_targets:int64
- Units if known: Not automatically verified
- Date/time column: date
- Date range: 2026-01-01 00:00:00 to 2026-08-31 00:00:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## forecast_target_percent_observed_distribution.csv

- Relative path: `02_training_data/07_targets/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/forecast_target_percent_observed_distribution.csv`
- Dataset role: 02_training_data
- Rows: 14
- Columns: 9
- Column names: horizon_minutes; percent_observed_bin; N; percentage_of_aligned; unique_stations; unique_station_days; unique_days; unique_freeways; unique_directions
- Data types: horizon_minutes:int64; percent_observed_bin:object; N:int64; percentage_of_aligned:float64; unique_stations:int64; unique_station_days:int64; unique_days:int64; unique_freeways:int64; unique_directions:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## ground_truth_threshold_sensitivity.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/ground_truth_threshold_sensitivity.csv`
- Dataset role: 01_raw_data
- Rows: 16
- Columns: 9
- Column names: scope; horizon_minutes; target_observed_threshold; N; unique_stations; unique_station_days; unique_days; unique_freeways; unique_directions
- Data types: scope:object; horizon_minutes:int64; target_observed_threshold:object; N:int64; unique_stations:int64; unique_station_days:int64; unique_days:int64; unique_freeways:int64; unique_directions:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## metadata_stable_station_comparison.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/metadata_stable_station_comparison.csv`
- Dataset role: 01_raw_data
- Rows: 14
- Columns: 7
- Column names: scope; percent_observed_bin; rows; percentage; unique_stations; unique_days; unique_freeways
- Data types: scope:object; percent_observed_bin:object; rows:int64; percentage:float64; unique_stations:int64; unique_days:int64; unique_freeways:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## official_field_definitions.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/official_field_definitions.csv`
- Dataset role: 01_raw_data
- Rows: 7
- Columns: 5
- Column names: field; official_definition; source_url; applicability; status
- Data types: field:object; official_definition:object; source_url:object; applicability:object; status:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## percent_observed_by_day.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/percent_observed_by_day.csv`
- Dataset role: 01_raw_data
- Rows: 243
- Columns: 9
- Column names: date; ML_rows; pct_observed_zero; pct_observed_ge_80; pct_observed_ge_90; pct_observed_100; observed_missing; zero_pct_change_previous_day_pp; zero_pct_difference_month_median_pp
- Data types: date:object; ML_rows:int64; pct_observed_zero:float64; pct_observed_ge_80:float64; pct_observed_ge_90:float64; pct_observed_100:float64; observed_missing:int64; zero_pct_change_previous_day_pp:float64; zero_pct_difference_month_median_pp:float64
- Units if known: Not automatically verified
- Date/time column: date
- Date range: 2026-01-01 00:00:00 to 2026-08-31 00:00:00
- Missing values: 1
- Unique identifiers: 
- Notes: 

## percent_observed_by_freeway_direction.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/percent_observed_by_freeway_direction.csv`
- Dataset role: 01_raw_data
- Rows: 45
- Columns: 8
- Column names: Fwy; Dir; stations; rows; pct_zero; pct_ge_80; pct_ge_90; pct_100
- Data types: Fwy:int64; Dir:object; stations:int64; rows:int64; pct_zero:float64; pct_ge_80:float64; pct_ge_90:float64; pct_100:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## percent_observed_by_month.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/percent_observed_by_month.csv`
- Dataset role: 01_raw_data
- Rows: 8
- Columns: 9
- Column names: month; total_ML_rows; pct_observed_zero; pct_observed_below_50; pct_observed_below_80; pct_observed_ge_80; pct_observed_ge_90; pct_observed_100; missing_observed_rows
- Data types: month:object; total_ML_rows:int64; pct_observed_zero:float64; pct_observed_below_50:float64; pct_observed_below_80:float64; pct_observed_ge_80:float64; pct_observed_ge_90:float64; pct_observed_100:float64; missing_observed_rows:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## percent_observed_by_station.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/percent_observed_by_station.csv`
- Dataset role: 01_raw_data
- Rows: 1936
- Columns: 20
- Column names: station; N; days_present; freeways; directions; mean_percent_observed; median; P10; P25; P75; P90; pct_zero; pct_below_50; pct_below_80; pct_ge_80; pct_ge_90; pct_100; zero_to_high_adjacent_transitions; profile; metadata_stable
- Data types: station:int64; N:int64; days_present:int64; freeways:int64; directions:object; mean_percent_observed:float64; median:float64; P10:float64; P25:float64; P75:float64; P90:float64; pct_zero:float64; pct_below_50:float64; pct_below_80:float64; pct_ge_80:float64; pct_ge_90:float64; pct_100:float64; zero_to_high_adjacent_transitions:int64; profile:object; metadata_stable:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## percent_observed_global_distribution.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/percent_observed_global_distribution.csv`
- Dataset role: 01_raw_data
- Rows: 7
- Columns: 6
- Column names: percent_observed_bin; rows; percentage; unique_stations; unique_days; unique_freeways
- Data types: percent_observed_bin:object; rows:int64; percentage:float64; unique_stations:int64; unique_days:int64; unique_freeways:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## percent_observed_vs_samples.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/percent_observed_vs_samples.csv`
- Dataset role: 01_raw_data
- Rows: 6
- Columns: 8
- Column names: percent_observed_bin; rows; samples_non_null; samples_non_null_pct; samples_median; samples_P10; samples_P90; zero_samples_pct
- Data types: percent_observed_bin:object; rows:int64; samples_non_null:int64; samples_non_null_pct:float64; samples_median:float64; samples_P10:float64; samples_P90:float64; zero_samples_pct:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 5
- Unique identifiers: 
- Notes: 

## perfect_repeat_runs_by_station.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/perfect_repeat_runs_by_station.csv`
- Dataset role: 01_raw_data
- Rows: 3778
- Columns: 7
- Column names: station; field; runs_ge_30min; runs_ge_60min; runs_ge_120min; longest_run_minutes; first_example_date
- Data types: station:int64; field:object; runs_ge_30min:int64; runs_ge_60min:int64; runs_ge_120min:int64; longest_run_minutes:int64; first_example_date:object
- Units if known: Not automatically verified
- Date/time column: first_example_date
- Date range: 2026-01-01 00:00:00 to 2026-08-31 00:00:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## station_high_observation_target_availability.csv

- Relative path: `02_training_data/07_targets/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/station_high_observation_target_availability.csv`
- Dataset role: 02_training_data
- Rows: 3872
- Columns: 5
- Column names: station; horizon_minutes; metadata_stable; target_ge90_eligible_samples; days_with_eligible_target
- Data types: station:int64; horizon_minutes:int64; metadata_stable:bool; target_ge90_eligible_samples:int64; days_with_eligible_target:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## station_identity_issues.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/station_identity_issues.csv`
- Dataset role: 01_raw_data
- Rows: 0
- Columns: 3
- Column names: date; duplicate_station_time_keys; station_identity_variants
- Data types: date:object; duplicate_station_time_keys:object; station_identity_variants:object
- Units if known: Not automatically verified
- Date/time column: date; duplicate_station_time_keys
- Date range: NaT to NaT
- Missing values: 0
- Unique identifiers: 
- Notes: 

## station_target_availability_distribution.csv

- Relative path: `02_training_data/07_targets/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/station_target_availability_distribution.csv`
- Dataset role: 02_training_data
- Rows: 4
- Columns: 14
- Column names: scope; horizon_minutes; stations; stations_with_eligible_target; eligible_samples_P10; eligible_samples_P25; eligible_samples_median; eligible_samples_P75; eligible_samples_P90; eligible_days_P10; eligible_days_P25; eligible_days_median; eligible_days_P75; eligible_days_P90
- Data types: scope:object; horizon_minutes:int64; stations:int64; stations_with_eligible_target:int64; eligible_samples_P10:float64; eligible_samples_P25:float64; eligible_samples_median:float64; eligible_samples_P75:float64; eligible_samples_P90:float64; eligible_days_P10:float64; eligible_days_P25:float64; eligible_days_median:float64; eligible_days_P75:float64; eligible_days_P90:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## step0b_feasibility.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/step0b_feasibility.csv`
- Dataset role: 01_raw_data
- Rows: 3
- Columns: 3
- Column names: dimension; rating; evidence
- Data types: dimension:object; rating:object; evidence:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step0B_PercentObserved_Audit.xlsx

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/Step0B_PercentObserved_Audit.xlsx`
- Dataset role: 01_raw_data
- Rows: 01_Summary:None rows x None columns; 02_Official_Definitions:None rows x None columns; 03_Month:None rows x None columns; 04_Day:None rows x None columns; 05_Station:None rows x None columns; 06_Freeway_Direction:None rows x None columns; 07_Samples:None rows x None columns; 08_ZeroObserved:None rows x None columns; 09_H30_Target:None rows x None columns; 10_H60_Target:None rows x None columns
- Columns: Workbook
- Column names: 01_Summary; 02_Official_Definitions; 03_Month; 04_Day; 05_Station; 06_Freeway_Direction; 07_Samples; 08_ZeroObserved; 09_H30_Target; 10_H60_Target; 11_Threshold_Sensitivity; 12_Stable_Stations; 13_Feasibility; 14_Risks
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step0B_results.json

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/Step0B_results.json`
- Dataset role: 01_raw_data
- Rows: JSON object
- Columns: 23
- Column names: canonical_raw_files; ML_rows; ML_stations; stable_ML_stations; percent_observed_zero_pct; percent_observed_ge80_pct; percent_observed_ge90_pct; percent_observed_100_pct; official_interpretation; speed_non_null_when_zero_pct; H30_aligned_targets; H30_target_ge90; H30_target_100; H60_aligned_targets; H60_target_ge90; H60_target_100; stations_H30_target_ge90; stations_H60_target_ge90; input_quality_variation; ground_truth_feasibility; jev_decision_gating_feasibility; critical_risks; recommended_next_step
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## step0b_risks.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/step0b_risks.csv`
- Dataset role: 01_raw_data
- Rows: 4
- Columns: 2
- Column names: risk_number; risk
- Data types: risk_number:int64; risk:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## zero_observed_variable_comparison.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS/zero_observed_variable_comparison.csv`
- Dataset role: 01_raw_data
- Rows: 6
- Columns: 12
- Column names: observation_group; field; rows; non_null_N; non_null_pct; min; P10; median; P90; max; mean; std
- Data types: observation_group:object; field:object; rows:int64; non_null_N:int64; non_null_pct:float64; min:float64; P10:float64; median:float64; P90:float64; max:float64; mean:float64; std:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step0C_manifest.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/14_STEP0C_CHRONOLOGICAL_SPLIT/Step0C_manifest.csv`
- Dataset role: 01_raw_data
- Rows: 5
- Columns: 4
- Column names: filename; size_bytes; sha256; purpose
- Data types: filename:object; size_bytes:int64; sha256:object; purpose:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## step0c_quality_cohorts.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/14_STEP0C_CHRONOLOGICAL_SPLIT/step0c_quality_cohorts.csv`
- Dataset role: 01_raw_data
- Rows: 36
- Columns: 5
- Column names: horizon; split; quality_bin; samples; unique_stations
- Data types: horizon:object; split:object; quality_bin:object; samples:int64; unique_stations:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## step0c_readiness.json

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/14_STEP0C_CHRONOLOGICAL_SPLIT/step0c_readiness.json`
- Dataset role: 01_raw_data
- Rows: JSON object
- Columns: 19
- Column names: stable_ml_stations; h30; h60; high_quality_reference; boundary_leakage; temporal_split_valid; three_split_common_q0_stations_H30; three_split_common_q0_stations_H60; temporal_concentration_risk; step0c_status; critical_issues; recommended_next_step; boundary_exclusions; test_out_of_range; missing_future_rows; q0_station_sample_distribution; q0_monthly_samples; q0_freeway_direction; source_canonical_files
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## step0c_split_summary.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/14_STEP0C_CHRONOLOGICAL_SPLIT/step0c_split_summary.csv`
- Dataset role: 01_raw_data
- Rows: 6
- Columns: 19
- Column names: horizon; split; target100_samples; Q0_to_100_samples; Q0_to_100_stations; Q0_to_100_station_days; Q0_to_100_days; Q0_to_100_freeways; Q0_to_100_directions; Q5_to_100_samples; Q5_to_100_stations; Q5_to_100_days; Q5_to_100_freeways; boundary_excluded; test_out_of_range_excluded; top1_day_share; top5_day_share; top10_day_share; top1_freeway_share
- Data types: horizon:object; split:object; target100_samples:int64; Q0_to_100_samples:int64; Q0_to_100_stations:int64; Q0_to_100_station_days:int64; Q0_to_100_days:int64; Q0_to_100_freeways:int64; Q0_to_100_directions:int64; Q5_to_100_samples:int64; Q5_to_100_stations:int64; Q5_to_100_days:int64; Q5_to_100_freeways:int64; boundary_excluded:int64; test_out_of_range_excluded:int64; top1_day_share:float64; top5_day_share:float64; top10_day_share:float64; top1_freeway_share:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## step0c_station_coverage.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/00_DATA_AUDIT/14_STEP0C_CHRONOLOGICAL_SPLIT/step0c_station_coverage.csv`
- Dataset role: 01_raw_data
- Rows: 1560
- Columns: 4
- Column names: horizon; split; station; Q0_to_100_samples
- Data types: horizon:object; split:object; station:int64; Q0_to_100_samples:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## PeMS_Data_Integrity_Audit_2026.xlsx

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/PeMS_Data_Integrity_Audit_2026.xlsx`
- Dataset role: 01_raw_data
- Rows: 01_Executive_Summary:None rows x None columns; 02_File_Inventory:None rows x None columns; 03_Date_Completeness:None rows x None columns; 04_Gzip_Integrity:None rows x None columns; 05_Schema:None rows x None columns; 06_Daily_Summary:None rows x None columns; 07_Monthly_Summary:None rows x None columns; 08_Station_Summary:None rows x None columns; 09_ML_Stations:None rows x None columns; 10_Percent_Observed:None rows x None columns
- Columns: Workbook
- Column names: 01_Executive_Summary; 02_File_Inventory; 03_Date_Completeness; 04_Gzip_Integrity; 05_Schema; 06_Daily_Summary; 07_Monthly_Summary; 08_Station_Summary; 09_ML_Stations; 10_Percent_Observed; 11_Anomalies; 12_Metadata_Match; 13_Target_Quality; 14_Readiness; 15_Critical_Issues
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## forecasting_dataset_dictionary.csv

- Relative path: `02_training_data/06_features/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/00_README/forecasting_dataset_dictionary.csv`
- Dataset role: 02_training_data
- Rows: 100
- Columns: 8
- Column names: feature; definition; unit; time_reference; source; model_role; leakage_safe; notes
- Data types: feature:object; definition:object; unit:object; time_reference:object; source:object; model_role:object; leakage_safe:object; notes:object
- Units if known: Not automatically verified
- Date/time column: time_reference
- Date range: NaT to NaT
- Missing values: 60
- Unique identifiers: 
- Notes: 

## test__01_H30.parquet

- Relative path: `02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/test__01_H30.parquet`
- Dataset role: 02_training_data
- Rows: 
- Columns: 
- Column names: 
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Inspection failed or skipped: FileNotFoundError: [WinError 2] Failed to open local file 'D:/OneDrive/桌面/论文/2027年投稿期刊/论文项目/01_JEV_小论文_Transportmetrica A Transport Science/github_update/02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/test__01_H30.parquet'. Detail: [Windows error 2] 系统找不到指定的文件。


## train__01_H30.parquet

- Relative path: `02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/train__01_H30.parquet`
- Dataset role: 02_training_data
- Rows: 
- Columns: 
- Column names: 
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Inspection failed or skipped: FileNotFoundError: [WinError 2] Failed to open local file 'D:/OneDrive/桌面/论文/2027年投稿期刊/论文项目/01_JEV_小论文_Transportmetrica A Transport Science/github_update/02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/train__01_H30.parquet'. Detail: [Windows error 2] 系统找不到指定的文件。


## validation__01_H30.parquet

- Relative path: `02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/validation__01_H30.parquet`
- Dataset role: 02_training_data
- Rows: 
- Columns: 
- Column names: 
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Inspection failed or skipped: FileNotFoundError: [WinError 2] Failed to open local file 'D:/OneDrive/桌面/论文/2027年投稿期刊/论文项目/01_JEV_小论文_Transportmetrica A Transport Science/github_update/02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/validation__01_H30.parquet'. Detail: [Windows error 2] 系统找不到指定的文件。


## test__02_H60.parquet

- Relative path: `02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/test__02_H60.parquet`
- Dataset role: 02_training_data
- Rows: 
- Columns: 
- Column names: 
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Inspection failed or skipped: FileNotFoundError: [WinError 2] Failed to open local file 'D:/OneDrive/桌面/论文/2027年投稿期刊/论文项目/01_JEV_小论文_Transportmetrica A Transport Science/github_update/02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/test__02_H60.parquet'. Detail: [Windows error 2] 系统找不到指定的文件。


## train__02_H60.parquet

- Relative path: `02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/train__02_H60.parquet`
- Dataset role: 02_training_data
- Rows: 
- Columns: 
- Column names: 
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Inspection failed or skipped: FileNotFoundError: [WinError 2] Failed to open local file 'D:/OneDrive/桌面/论文/2027年投稿期刊/论文项目/01_JEV_小论文_Transportmetrica A Transport Science/github_update/02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/train__02_H60.parquet'. Detail: [Windows error 2] 系统找不到指定的文件。


## validation__02_H60.parquet

- Relative path: `02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/validation__02_H60.parquet`
- Dataset role: 02_training_data
- Rows: 
- Columns: 
- Column names: 
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Inspection failed or skipped: FileNotFoundError: [WinError 2] Failed to open local file 'D:/OneDrive/桌面/论文/2027年投稿期刊/论文项目/01_JEV_小论文_Transportmetrica A Transport Science/github_update/02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/validation__02_H60.parquet'. Detail: [Windows error 2] 系统找不到指定的文件。


## dataset_split_summary.csv

- Relative path: `02_training_data/06_features/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/03_QC/dataset_split_summary.csv`
- Dataset role: 02_training_data
- Rows: 6
- Columns: 14
- Column names: horizon; split; rows; unique_stations; unique_days; unique_freeways; Q0_rows; Q1_rows; Q2_rows; Q3_rows; Q4_rows; Q5_rows; target100_rows; history_complete_pct
- Data types: horizon:object; split:object; rows:int64; unique_stations:int64; unique_days:int64; unique_freeways:int64; Q0_rows:int64; Q1_rows:int64; Q2_rows:int64; Q3_rows:int64; Q4_rows:int64; Q5_rows:int64; target100_rows:int64; history_complete_pct:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## feature_missingness.csv

- Relative path: `02_training_data/06_features/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/03_QC/feature_missingness.csv`
- Dataset role: 02_training_data
- Rows: 540
- Columns: 6
- Column names: horizon; split; feature; N; missing_n; missing_pct
- Data types: horizon:object; split:object; feature:object; N:int64; missing_n:int64; missing_pct:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## leakage_audit.json

- Relative path: `02_training_data/06_features/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/03_QC/leakage_audit.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 14
- Column names: feature_timestamp_after_t; target_not_after_t; horizon_elapsed_mismatch; target100_violations; split_leakage; test_out_of_range; duplicate_sample_ids; duplicate_primary_keys; source_canonical_files; source_stable_stations; exclusions; step0c_q0_reconciliation; unexplained_differences; status
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## target_speed_distribution.csv

- Relative path: `02_training_data/07_targets/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/03_QC/target_speed_distribution.csv`
- Dataset role: 02_training_data
- Rows: 6
- Columns: 14
- Column names: horizon; split; N; mean; std; min; P01; P05; P25; median; P75; P95; P99; max
- Data types: horizon:object; split:object; N:int64; mean:float64; std:float64; min:float64; P01:float64; P05:float64; P25:float64; median:float64; P75:float64; P95:float64; P99:float64; max:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step1A_Dataset_Manifest.csv

- Relative path: `02_training_data/06_features/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/04_MANIFEST/Step1A_Dataset_Manifest.csv`
- Dataset role: 02_training_data
- Rows: 6
- Columns: 7
- Column names: filename; size_bytes; sha256; row_count; unique_stations; min_timestamp; max_timestamp
- Data types: filename:object; size_bytes:int64; sha256:object; row_count:int64; unique_stations:int64; min_timestamp:object; max_timestamp:object
- Units if known: Not automatically verified
- Date/time column: min_timestamp; max_timestamp
- Date range: 2026-01-01 08:55:00+00:00 to 2026-07-01 07:00:00+00:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## station_overlap.json

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/03_FORECASTING_BENCHMARK/00_PREFLIGHT/station_overlap.json`
- Dataset role: 01_raw_data
- Rows: JSON object
- Columns: 18
- Column names: train_stations; validation_stations; test_stations; train_intersection_validation; train_intersection_test; validation_intersection_test; three_split_common; validation_only_not_in_train; test_only_not_in_train; train_only; temporal_generalization_cohort; seen_station_test_samples; unseen_station_test_samples; train_station_ids; validation_station_ids; test_station_ids; unseen_validation_station_ids; unseen_test_station_ids
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## station_overlap_summary.csv

- Relative path: `01_raw_data/02_station_metadata/Caltrans PeMS/03_FORECASTING_BENCHMARK/00_PREFLIGHT/station_overlap_summary.csv`
- Dataset role: 01_raw_data
- Rows: 1
- Columns: 13
- Column names: train_stations; validation_stations; test_stations; train_intersection_validation; train_intersection_test; validation_intersection_test; three_split_common; validation_only_not_in_train; test_only_not_in_train; train_only; temporal_generalization_cohort; seen_station_test_samples; unseen_station_test_samples
- Data types: train_stations:int64; validation_stations:int64; test_stations:int64; train_intersection_validation:int64; train_intersection_test:int64; validation_intersection_test:int64; three_split_common:int64; validation_only_not_in_train:int64; test_only_not_in_train:int64; train_only:int64; temporal_generalization_cohort:object; seen_station_test_samples:int64; unseen_station_test_samples:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## unseen_test_stations.csv

- Relative path: `02_training_data/05_test_split/Caltrans PeMS/03_FORECASTING_BENCHMARK/00_PREFLIGHT/unseen_test_stations.csv`
- Dataset role: 02_training_data
- Rows: 25
- Columns: 1
- Column names: station_id
- Data types: station_id:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## unseen_validation_stations.csv

- Relative path: `02_training_data/04_validation_split/Caltrans PeMS/03_FORECASTING_BENCHMARK/00_PREFLIGHT/unseen_validation_stations.csv`
- Dataset role: 02_training_data
- Rows: 9
- Columns: 1
- Column names: station_id
- Data types: station_id:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## pilot_dataset_summary.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/03_FORECASTING_BENCHMARK/01_PILOT_DATA/pilot_dataset_summary.csv`
- Dataset role: 01_raw_data
- Rows: 3
- Columns: 11
- Column names: pilot_split; rows; stations; first_local; last_local; Q0_rows; Q1_rows; Q2_rows; Q3_rows; Q4_rows; Q5_rows
- Data types: pilot_split:object; rows:int64; stations:int64; first_local:object; last_local:object; Q0_rows:int64; Q1_rows:int64; Q2_rows:int64; Q3_rows:int64; Q4_rows:int64; Q5_rows:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## xgboost_encoder.json

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/03_FORECASTING_BENCHMARK/04_XGBOOST/xgboost_encoder.json`
- Dataset role: 01_raw_data
- Rows: JSON object
- Columns: 4
- Column names: categories; unknown_category; fit_source; numeric_columns
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## xgboost_H30_pilot.json

- Relative path: `02_training_data/01_H30/Caltrans PeMS/03_FORECASTING_BENCHMARK/04_XGBOOST/xgboost_H30_pilot.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 2
- Column names: learner; version
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## gru_scaler__05_GRU.json

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/03_FORECASTING_BENCHMARK/05_GRU/gru_scaler__05_GRU.json`
- Dataset role: 01_raw_data
- Rows: JSON object
- Columns: 6
- Column names: variables; mean; std; fit_source; sequence_order; context_features
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## pilot_forecasting_results.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/03_FORECASTING_BENCHMARK/06_RESULTS/pilot_forecasting_results.csv`
- Dataset role: 01_raw_data
- Rows: 8
- Columns: 17
- Column names: model; split; n_samples; MAE; RMSE; P90_AE; P95_AE; training_seconds; inference_median_seconds; inference_P90_seconds; inference_min_seconds; inference_max_seconds; samples_per_second; microseconds_per_sample; five_runs_seconds; device; model_size_MB
- Data types: model:object; split:object; n_samples:int64; MAE:float64; RMSE:float64; P90_AE:float64; P95_AE:float64; training_seconds:float64; inference_median_seconds:float64; inference_P90_seconds:float64; inference_min_seconds:float64; inference_max_seconds:float64; samples_per_second:float64; microseconds_per_sample:float64; five_runs_seconds:object; device:object; model_size_MB:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## pilot_qc.json

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/03_FORECASTING_BENCHMARK/06_RESULTS/pilot_qc.json`
- Dataset role: 01_raw_data
- Rows: JSON object
- Columns: 18
- Column names: all_pilot_rows_from_formal_H30_train; formal_validation_test_not_used_for_modeling; target_is_H30_speed; target_observed_100; exact_h30_elapsed; feature_timestamp_not_after_prediction; duplicate_sample_ids; pilot_split_overlap; scaler_fit_source; categorical_fit_source; historical_average_fit_source; xgb_early_stopping_source; gru_early_stopping_source; pilot_mae_role; station_overlap_status; gru_runtime_limit; pilot_status; critical_issues
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## cloud_need_assessment.json

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/03_FORECASTING_BENCHMARK/07_RESOURCE_PROFILE/cloud_need_assessment.json`
- Dataset role: 01_raw_data
- Rows: JSON object
- Columns: 8
- Column names: status; reasons; source; estimate_status; xgboost_full_train_seconds; gru_full_seconds_per_epoch; gru_30_epochs_seconds; limitations
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## local_compute_profile.json

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/03_FORECASTING_BENCHMARK/07_RESOURCE_PROFILE/local_compute_profile.json`
- Dataset role: 01_raw_data
- Rows: JSON object
- Columns: 11
- Column names: cpu; cpu_logical_threads; ram_total_gb; gpu; gpu_vram_gb; pilot_rows; xgboost; gru; historical_average_test_fallback_counts; full_h30_estimate; historical_average_test_fallback_proportions
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step1B_Pilot_Manifest.csv

- Relative path: `01_raw_data/01_caltrans_pems/Caltrans PeMS/03_FORECASTING_BENCHMARK/09_MANIFEST/Step1B_Pilot_Manifest.csv`
- Dataset role: 01_raw_data
- Rows: 22
- Columns: 5
- Column names: file; relative_path; size_bytes; sha256; purpose
- Data types: file:object; relative_path:object; size_bytes:int64; sha256:object; purpose:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## cpu_runtime_estimate.json

- Relative path: `02_training_data/01_H30/Caltrans PeMS/03_FORECASTING_BENCHMARK/10_FULL_H30/00_CPU_RUNTIME_PREFLIGHT/cpu_runtime_estimate.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 11
- Column names: cpu; cpu_threads; ram_total_gb; data_scope; xgboost; gru; memory_risk; peak_ram_fraction_of_total; cpu_full_step1b_assessment; estimate_status; estimate_limitations
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## cpu_runtime_profile.csv

- Relative path: `02_training_data/01_H30/Caltrans PeMS/03_FORECASTING_BENCHMARK/10_FULL_H30/00_CPU_RUNTIME_PREFLIGHT/cpu_runtime_profile.csv`
- Dataset role: 02_training_data
- Rows: 11
- Columns: 6
- Column names: component; phase; epoch; seconds; rows; peak_ram_gb
- Data types: component:object; phase:object; epoch:float64; seconds:float64; rows:int64; peak_ram_gb:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 5
- Unique identifiers: 
- Notes: 

## cuda_preflight.json

- Relative path: `02_training_data/01_H30/Caltrans PeMS/03_FORECASTING_BENCHMARK/10_FULL_H30/00_CUDA_PREFLIGHT/cuda_preflight.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 15
- Column names: python; torch; torch_cuda_version; cuda_available; cuda_device_count; gpu_name; gpu_vram_gb; tensor_test; gru_forward_test; gru_backward_test; optimizer_step_test; cuda_preflight; issues; nvidia_smi; nvidia_driver
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Fig4a_source.csv

- Relative path: `99_archive/uncategorized_review/fig/历史/fig4/Fig4a_source.csv`
- Dataset role: 99_archive
- Rows: 16
- Columns: 13
- Column names: record_type; method; bin_id; bin_lower; bin_upper; n; mean_probability; observed_success_rate; absolute_gap; N_final_test; Brier; Holm_p; supported
- Data types: record_type:object; method:object; bin_id:float64; bin_lower:float64; bin_upper:float64; n:float64; mean_probability:float64; observed_success_rate:float64; absolute_gap:float64; N_final_test:float64; Brier:float64; Holm_p:float64; supported:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 75
- Unique identifiers: 
- Notes: 

## Fig4b_source.csv

- Relative path: `99_archive/uncategorized_review/fig/历史/fig4/Fig4b_source.csv`
- Dataset role: 99_archive
- Rows: 1579
- Columns: 15
- Column names: sample_id; target_station; calibrated_confidence; rank; coverage; cumulative_normalized_regret_risk; is_displayed_main_range; is_fixed_operating_point; fixed_requested_coverage; N_retained_fixed; AURC_full_discrete_mean; P4_delta_AURC_full_minus_random; P4_Holm_p; C3_delta_AURC_full_minus_margin; C3_Holm_p
- Data types: sample_id:object; target_station:int64; calibrated_confidence:float64; rank:int64; coverage:float64; cumulative_normalized_regret_risk:float64; is_displayed_main_range:bool; is_fixed_operating_point:bool; fixed_requested_coverage:float64; N_retained_fixed:float64; AURC_full_discrete_mean:float64; P4_delta_AURC_full_minus_random:float64; P4_Holm_p:float64; C3_delta_AURC_full_minus_margin:float64; C3_Holm_p:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 3150
- Unique identifiers: 
- Notes: 

## SHA256_MANIFEST.csv

- Relative path: `06_figure_data/Fig01/source_data/fig/图片数据/00_README/SHA256_MANIFEST.csv`
- Dataset role: 06_figure_data
- Rows: 64
- Columns: 3
- Column names: file; size_bytes; sha256
- Data types: file:object; size_bytes:int64; sha256:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## SOURCE_DATA_INDEX.csv

- Relative path: `06_figure_data/Fig01/source_data/fig/图片数据/00_README/SOURCE_DATA_INDEX.csv`
- Dataset role: 06_figure_data
- Rows: 56
- Columns: 7
- Column names: figure; panel; package_file; authoritative_origin; status; role; note
- Data types: figure:object; panel:object; package_file:object; authoritative_origin:object; status:object; role:object; note:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 44
- Unique identifiers: 
- Notes: 

## Fig1_cohort_task_plot_source.csv

- Relative path: `06_figure_data/Fig01/source_data/fig/图片数据/01_Fig1_Study_Setup/Fig1_cohort_task_plot_source.csv`
- Dataset role: 06_figure_data
- Rows: 9
- Columns: 5
- Column names: item; value; unit; provenance; note
- Data types: item:object; value:object; unit:object; provenance:object; note:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 1
- Unique identifiers: 
- Notes: 

## FinalTest_Cohort_Audit.csv

- Relative path: `06_figure_data/Fig01/processed_data/fig/图片数据/01_Fig1_Study_Setup/FinalTest_Cohort_Audit.csv`
- Dataset role: 06_figure_data
- Rows: 1579
- Columns: 18
- Column names: split; target_station; timestamp; sample_id; requested_K; mapped_candidate_count; available_candidate_count; missing_candidate_count; candidate_pool_complete; primary_selection_evaluable; structural_insufficient_candidate_count; source_history_missing_count; invalid_candidate_feature_count; complete_K5_sample; missing_candidate_reason; source_history_missing_ids; invalid_candidate_feature_ids; included_final_test
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; requested_K:int64; mapped_candidate_count:int64; available_candidate_count:int64; missing_candidate_count:int64; candidate_pool_complete:bool; primary_selection_evaluable:bool; structural_insufficient_candidate_count:int64; source_history_missing_count:int64; invalid_candidate_feature_count:int64; complete_K5_sample:bool; missing_candidate_reason:float64; source_history_missing_ids:float64; invalid_candidate_feature_ids:float64; included_final_test:bool
- Units if known: Not automatically verified
- Date/time column: timestamp; mapped_candidate_count; available_candidate_count; missing_candidate_count; candidate_pool_complete; structural_insufficient_candidate_count; invalid_candidate_feature_count; missing_candidate_reason; invalid_candidate_feature_ids
- Date range: 2026-07-01 23:30:00-07:00 to 2026-08-30 02:25:00-07:00
- Missing values: 4737
- Unique identifiers: 
- Notes: 

## Step2A_Candidate_Availability_Audit.csv

- Relative path: `06_figure_data/Fig01/processed_data/fig/图片数据/01_Fig1_Study_Setup/Step2A_Candidate_Availability_Audit.csv`
- Dataset role: 06_figure_data
- Rows: 172
- Columns: 6
- Column names: target_station; requested_K; mapped_candidate_count; candidate_pool_complete; primary_selection_evaluable; exclusion_reason
- Data types: target_station:int64; requested_K:int64; mapped_candidate_count:int64; candidate_pool_complete:bool; primary_selection_evaluable:bool; exclusion_reason:object
- Units if known: Not automatically verified
- Date/time column: mapped_candidate_count; candidate_pool_complete
- Date range: 1970-01-01 00:00:00.000000001 to 1970-01-01 00:00:00.000000005
- Missing values: 171
- Unique identifiers: 
- Notes: 

## Step2A_Candidate_Set_Size.csv

- Relative path: `06_figure_data/Fig01/processed_data/fig/图片数据/01_Fig1_Study_Setup/Step2A_Candidate_Set_Size.csv`
- Dataset role: 06_figure_data
- Rows: 10766
- Columns: 17
- Column names: split; target_station; timestamp; sample_id; requested_K; mapped_candidate_count; available_candidate_count; missing_candidate_count; candidate_pool_complete; primary_selection_evaluable; structural_insufficient_candidate_count; source_history_missing_count; invalid_candidate_feature_count; complete_K5_sample; missing_candidate_reason; source_history_missing_ids; invalid_candidate_feature_ids
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; requested_K:int64; mapped_candidate_count:int64; available_candidate_count:int64; missing_candidate_count:int64; candidate_pool_complete:bool; primary_selection_evaluable:bool; structural_insufficient_candidate_count:int64; source_history_missing_count:int64; invalid_candidate_feature_count:int64; complete_K5_sample:bool; missing_candidate_reason:object; source_history_missing_ids:float64; invalid_candidate_feature_ids:float64
- Units if known: Not automatically verified
- Date/time column: timestamp; mapped_candidate_count; available_candidate_count; missing_candidate_count; candidate_pool_complete; structural_insufficient_candidate_count; invalid_candidate_feature_count; missing_candidate_reason; invalid_candidate_feature_ids
- Date range: 2026-01-01 19:05:00-08:00 to 2026-06-06 07:35:00-07:00
- Missing values: 29862
- Unique identifiers: 
- Notes: 

## Step2A_QC.json

- Relative path: `06_figure_data/Fig01/processed_data/fig/图片数据/01_Fig1_Study_Setup/Step2A_QC.json`
- Dataset role: 06_figure_data
- Rows: JSON object
- Columns: 10
- Column names: status; checks; critical_failures; formal_utility_protocol; formal_utility_implemented; test_used_for_design_or_threshold_selection; test_split_status; station_universe_count; primary_evaluable_target_count; audit_only_target_count
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Fig2_JEV_frozen_weights_plot_source.csv

- Relative path: `06_figure_data/Fig02/source_data/fig/图片数据/02_Fig2_Workflow/Fig2_JEV_frozen_weights_plot_source.csv`
- Dataset role: 06_figure_data
- Rows: 4
- Columns: 2
- Column names: evidence; weight
- Data types: evidence:object; weight:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## FinalTest_QC.json

- Relative path: `06_figure_data/Fig02/processed_data/fig/图片数据/02_Fig2_Workflow/FinalTest_QC.json`
- Dataset role: 06_figure_data
- Rows: JSON object
- Columns: 7
- Column names: status; test_opened; primary_stations; candidate_k; equal_method_denominators; missing_primary_predictions; formula_errors
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Stats_Freeze_Config.json

- Relative path: `06_figure_data/Fig02/plot_config/fig/图片数据/02_Fig2_Workflow/Stats_Freeze_Config.json`
- Dataset role: 06_figure_data
- Rows: JSON object
- Columns: 25
- Column names: status; created_utc; test_loaded; selectors; selector_refit_on_validation; candidate_k; primary_station_universe; audit_only_station; near_oracle_threshold_mph; FINAL_BASE_RATE; raw_confidence_q75; final_platt_monotonic_increasing; alpha; bootstrap_repetitions; permutation_repetitions; random_rankings; seed; cluster; bootstrap_ci; holm_families; fixed_coverages; ece; risk_curve_smoothing; thresholds_inherited_exactly_from_step2h; manifest_payload_rule
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_JEV_Weights__02_Fig2_Workflow.json

- Relative path: `06_figure_data/Fig02/processed_data/fig/图片数据/02_Fig2_Workflow/Step2B_JEV_Weights__02_Fig2_Workflow.json`
- Dataset role: 06_figure_data
- Rows: JSON object
- Columns: 5
- Column names: version; combined_freeze_sha256; weights; tau_d; optimizer
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Method_Summary.csv

- Relative path: `06_figure_data/Fig02/processed_data/fig/图片数据/02_Fig2_Workflow/Step2B_Method_Summary.csv`
- Dataset role: 06_figure_data
- Rows: 8
- Columns: 11
- Column names: method; validation_samples; mean_normalized_regret; median_normalized_regret; mean_raw_regret_mph; median_raw_regret_mph; near_oracle_hit_rate; top1_accuracy; top2_hit_rate; development_only; deployable
- Data types: method:object; validation_samples:int64; mean_normalized_regret:float64; median_normalized_regret:float64; mean_raw_regret_mph:float64; median_raw_regret_mph:float64; near_oracle_hit_rate:float64; top1_accuracy:float64; top2_hit_rate:float64; development_only:bool; deployable:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2C_Calibration_Method_Summary__02_Fig2_Workflow.csv

- Relative path: `06_figure_data/Fig02/processed_data/fig/图片数据/02_Fig2_Workflow/Step2C_Calibration_Method_Summary__02_Fig2_Workflow.csv`
- Dataset role: 06_figure_data
- Rows: 4
- Columns: 11
- Column names: method; cal_eval_n; mean_predicted_probability; observed_success_prevalence; brier_score; nll; ece; eligible_for_final_family; development_only; raw_pearson_with_y; raw_spearman_with_y
- Data types: method:object; cal_eval_n:int64; mean_predicted_probability:float64; observed_success_prevalence:float64; brier_score:float64; nll:float64; ece:float64; eligible_for_final_family:bool; development_only:bool; raw_pearson_with_y:float64; raw_spearman_with_y:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 6
- Unique identifiers: 
- Notes: 

## Step2D_AURC_Summary__02_Fig2_Workflow.csv

- Relative path: `06_figure_data/Fig02/processed_data/fig/图片数据/02_Fig2_Workflow/Step2D_AURC_Summary__02_Fig2_Workflow.csv`
- Dataset role: 06_figure_data
- Rows: 7
- Columns: 11
- Column names: ranking; system; N; aurc; full_coverage_risk; minimum_observed_curve_risk; maximum_observed_curve_risk; confidence_tie_count; coverage_boundary_tie_count; monotonic_violation_count; development_only
- Data types: ranking:object; system:object; N:int64; aurc:float64; full_coverage_risk:float64; minimum_observed_curve_risk:float64; maximum_observed_curve_risk:float64; confidence_tie_count:int64; coverage_boundary_tie_count:int64; monotonic_violation_count:int64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2G_Selection_Ablation_Summary__02_Fig2_Workflow.csv

- Relative path: `06_figure_data/Fig02/processed_data/fig/图片数据/02_Fig2_Workflow/Step2G_Selection_Ablation_Summary__02_Fig2_Workflow.csv`
- Dataset role: 06_figure_data
- Rows: 7
- Columns: 12
- Column names: variant; N; mean_normalized_regret; median_normalized_regret; mean_raw_regret_mph; median_raw_regret_mph; exact_top1_accuracy; top2_hit_rate; near_oracle_hit_rate_0p5; development_smoke_only; delta_nr_vs_full; relative_degradation_pct
- Data types: variant:object; N:int64; mean_normalized_regret:float64; median_normalized_regret:float64; mean_raw_regret_mph:float64; median_raw_regret_mph:float64; exact_top1_accuracy:float64; top2_hit_rate:float64; near_oracle_hit_rate_0p5:float64; development_smoke_only:bool; delta_nr_vs_full:float64; relative_degradation_pct:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Fig3a_Oracle_Switching_plot_source.csv

- Relative path: `06_figure_data/Fig03/source_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Fig3a_Oracle_Switching_plot_source.csv`
- Dataset role: 06_figure_data
- Rows: 171
- Columns: 8
- Column names: target_station; samples; unique_oracle_candidates; oracle_switch_rate; dominant_oracle; dominant_oracle_share; oracle_entropy_bits; mean_best_worst_spread
- Data types: target_station:int64; samples:int64; unique_oracle_candidates:int64; oracle_switch_rate:float64; dominant_oracle:int64; dominant_oracle_share:float64; oracle_entropy_bits:float64; mean_best_worst_spread:float64
- Units if known: Not automatically verified
- Date/time column: unique_oracle_candidates
- Date range: 1970-01-01 00:00:00.000000002 to 1970-01-01 00:00:00.000000005
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Fig3a_unique_oracle_candidate_counts.csv

- Relative path: `06_figure_data/Fig03/source_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Fig3a_unique_oracle_candidate_counts.csv`
- Dataset role: 06_figure_data
- Rows: 4
- Columns: 2
- Column names: unique_oracle_candidates; station_count
- Data types: unique_oracle_candidates:int64; station_count:int64
- Units if known: Not automatically verified
- Date/time column: unique_oracle_candidates
- Date range: 1970-01-01 00:00:00.000000002 to 1970-01-01 00:00:00.000000005
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Fig3b_Candidate_Utility_Spread_target_time_plot_source.csv

- Relative path: `06_figure_data/Fig03/source_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Fig3b_Candidate_Utility_Spread_target_time_plot_source.csv`
- Dataset role: 06_figure_data
- Rows: 10600
- Columns: 7
- Column names: split; target_station; timestamp; timestamp_utc; sample_id; best_worst_spread; normalized_spread
- Data types: split:object; target_station:int64; timestamp:object; timestamp_utc:object; sample_id:object; best_worst_spread:float64; normalized_spread:float64
- Units if known: Not automatically verified
- Date/time column: timestamp; timestamp_utc
- Date range: 2026-01-01 19:05:00-08:00 to 2026-06-06 07:40:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Fig3b_spread_summary.csv

- Relative path: `06_figure_data/Fig03/processed_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Fig3b_spread_summary.csv`
- Dataset role: 06_figure_data
- Rows: 5
- Columns: 2
- Column names: metric; value
- Data types: metric:object; value:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Fig3c_Selector_Performance_plot_source.csv

- Relative path: `06_figure_data/Fig03/source_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Fig3c_Selector_Performance_plot_source.csv`
- Dataset role: 06_figure_data
- Rows: 7
- Columns: 9
- Column names: method; N; stations; mean_normalized_regret; ci95_low; ci95_high; mean_raw_regret_mph; exact_top1; near_oracle_hit_0p5
- Data types: method:object; N:int64; stations:int64; mean_normalized_regret:float64; ci95_low:float64; ci95_high:float64; mean_raw_regret_mph:float64; exact_top1:float64; near_oracle_hit_0p5:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Fig3d_DisplayMeanNR_Differences.csv

- Relative path: `06_figure_data/Fig03/source_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Fig3d_DisplayMeanNR_Differences.csv`
- Dataset role: 06_figure_data
- Rows: 3
- Columns: 5
- Column names: comparison; JEV_overall_mean_NR; baseline_overall_mean_NR; simple_difference_JEV_minus_baseline; warning
- Data types: comparison:object; JEV_overall_mean_NR:float64; baseline_overall_mean_NR:float64; simple_difference_JEV_minus_baseline:float64; warning:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## FinalTest_Primary_Comparisons.csv

- Relative path: `06_figure_data/Fig03/processed_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/FinalTest_Primary_Comparisons.csv`
- Dataset role: 06_figure_data
- Rows: 4
- Columns: 9
- Column names: hypothesis_id; family; comparison; raw_effect; effect_size_cohen_dz; raw_p; wilcoxon_sensitivity_p; Holm_p; supported
- Data types: hypothesis_id:object; family:object; comparison:object; raw_effect:float64; effect_size_cohen_dz:float64; raw_p:float64; wilcoxon_sensitivity_p:float64; Holm_p:float64; supported:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 2
- Unique identifiers: 
- Notes: 

## FinalTest_Selector_Performance.csv

- Relative path: `06_figure_data/Fig03/processed_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/FinalTest_Selector_Performance.csv`
- Dataset role: 06_figure_data
- Rows: 7
- Columns: 12
- Column names: method; N; stations; mean_normalized_regret; ci95_low; ci95_high; median_normalized_regret; mean_raw_regret_mph; median_raw_regret_mph; exact_top1; top2_hit; near_oracle_hit_0p5
- Data types: method:object; N:int64; stations:int64; mean_normalized_regret:float64; ci95_low:float64; ci95_high:float64; median_normalized_regret:float64; mean_raw_regret_mph:float64; median_raw_regret_mph:float64; exact_top1:float64; top2_hit:float64; near_oracle_hit_0p5:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Oracle_Turnover.csv

- Relative path: `06_figure_data/Fig03/processed_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Step2A_Oracle_Turnover.csv`
- Dataset role: 06_figure_data
- Rows: 171
- Columns: 10
- Column names: target_station; samples; unique_oracle_candidates; dominant_oracle; dominant_oracle_share; oracle_switch_rate; oracle_entropy_bits; mean_oracle_loss; mean_oracle_gap; mean_best_worst_spread
- Data types: target_station:int64; samples:int64; unique_oracle_candidates:int64; dominant_oracle:int64; dominant_oracle_share:float64; oracle_switch_rate:float64; oracle_entropy_bits:float64; mean_oracle_loss:float64; mean_oracle_gap:float64; mean_best_worst_spread:float64
- Units if known: Not automatically verified
- Date/time column: unique_oracle_candidates
- Date range: 1970-01-01 00:00:00.000000002 to 1970-01-01 00:00:00.000000005
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Oracle_Utility.csv

- Relative path: `06_figure_data/Fig03/processed_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Step2A_Oracle_Utility.csv`
- Dataset role: 06_figure_data
- Rows: 53000
- Columns: 16
- Column names: split; target_station; timestamp; timestamp_utc; candidate_station; candidate_rank; target_speed; sample_id; prediction; candidate_loss; oracle_source; oracle_loss; oracle_rank; oracle_gap; best_worst_spread; normalized_spread
- Data types: split:object; target_station:int64; timestamp:object; timestamp_utc:object; candidate_station:int64; candidate_rank:int64; target_speed:float64; sample_id:object; prediction:float64; candidate_loss:float64; oracle_source:int64; oracle_loss:float64; oracle_rank:int64; oracle_gap:float64; best_worst_spread:float64; normalized_spread:float64
- Units if known: Not automatically verified
- Date/time column: timestamp; timestamp_utc; candidate_station; candidate_rank; candidate_loss
- Date range: 2026-01-01 19:05:00-08:00 to 2026-02-01 13:10:00-08:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Target_Level_Summary.csv

- Relative path: `06_figure_data/Fig03/processed_data/fig/图片数据/03_Fig3_Selection_Reality_Benchmark/Step2A_Target_Level_Summary.csv`
- Dataset role: 06_figure_data
- Rows: 171
- Columns: 10
- Column names: target_station; samples; unique_oracle_candidates; dominant_oracle; dominant_oracle_share; oracle_switch_rate; oracle_entropy_bits; mean_oracle_loss; mean_oracle_gap; mean_best_worst_spread
- Data types: target_station:int64; samples:int64; unique_oracle_candidates:int64; dominant_oracle:int64; dominant_oracle_share:float64; oracle_switch_rate:float64; oracle_entropy_bits:float64; mean_oracle_loss:float64; mean_oracle_gap:float64; mean_best_worst_spread:float64
- Units if known: Not automatically verified
- Date/time column: unique_oracle_candidates
- Date range: 1970-01-01 00:00:00.000000002 to 1970-01-01 00:00:00.000000005
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Fig4_operating_points_100_50_40_20.csv

- Relative path: `06_figure_data/Fig04/source_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/Fig4_operating_points_100_50_40_20.csv`
- Dataset role: 06_figure_data
- Rows: 4
- Columns: 6
- Column names: coverage; N_retained; normalized_regret_risk; raw_regret_risk; near_oracle_failure_rate; Top1_error
- Data types: coverage:float64; N_retained:int64; normalized_regret_risk:float64; raw_regret_risk:float64; near_oracle_failure_rate:float64; Top1_error:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## FinalTest_Calibration.csv

- Relative path: `06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_Calibration.csv`
- Dataset role: 06_figure_data
- Rows: 3
- Columns: 5
- Column names: method; N; Brier; NLL; ECE_10_equal_width
- Data types: method:object; N:int64; Brier:float64; NLL:float64; ECE_10_equal_width:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## FinalTest_Confidence_Comparisons.csv

- Relative path: `06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_Confidence_Comparisons.csv`
- Dataset role: 06_figure_data
- Rows: 4
- Columns: 6
- Column names: hypothesis_id; comparison; raw_effect; raw_p; Holm_p; supported
- Data types: hypothesis_id:object; comparison:object; raw_effect:float64; raw_p:float64; Holm_p:float64; supported:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 2
- Unique identifiers: 
- Notes: 

## FinalTest_RiskCoverage_Curve.csv

- Relative path: `06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_RiskCoverage_Curve.csv`
- Dataset role: 06_figure_data
- Rows: 1579
- Columns: 10
- Column names: sample_id; target_station; calibrated_confidence; normalized_regret; raw_regret_mph; exact_top1_hit; near_oracle_hit_0p5; rank; coverage; cumulative_normalized_regret_risk
- Data types: sample_id:object; target_station:int64; calibrated_confidence:float64; normalized_regret:float64; raw_regret_mph:float64; exact_top1_hit:bool; near_oracle_hit_0p5:bool; rank:int64; coverage:float64; cumulative_normalized_regret_risk:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## FinalTest_RiskCoverage_FixedCoverage.csv

- Relative path: `06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/FinalTest_RiskCoverage_FixedCoverage.csv`
- Dataset role: 06_figure_data
- Rows: 9
- Columns: 6
- Column names: coverage; N_retained; normalized_regret_risk; raw_regret_risk; near_oracle_failure_rate; Top1_error
- Data types: coverage:float64; N_retained:int64; normalized_regret_risk:float64; raw_regret_risk:float64; near_oracle_failure_rate:float64; Top1_error:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2C_Reliability_Bins__04_Fig4_Confidence_SelectiveRisk.csv

- Relative path: `06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/Step2C_Reliability_Bins__04_Fig4_Confidence_SelectiveRisk.csv`
- Dataset role: 06_figure_data
- Rows: 40
- Columns: 8
- Column names: method; bin_id; bin_lower; bin_upper; n; mean_probability; observed_success_rate; absolute_gap
- Data types: method:object; bin_id:int64; bin_lower:float64; bin_upper:float64; n:int64; mean_probability:float64; observed_success_rate:float64; absolute_gap:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 78
- Unique identifiers: 
- Notes: 

## Step2C_Reliability_Diagram_SourceData__04_Fig4_Confidence_SelectiveRisk.csv

- Relative path: `06_figure_data/Fig04/processed_data/fig/图片数据/04_Fig4_Confidence_SelectiveRisk/Step2C_Reliability_Diagram_SourceData__04_Fig4_Confidence_SelectiveRisk.csv`
- Dataset role: 06_figure_data
- Rows: 40
- Columns: 8
- Column names: method; bin_id; bin_lower; bin_upper; n; mean_probability; observed_success_rate; absolute_gap
- Data types: method:object; bin_id:int64; bin_lower:float64; bin_upper:float64; n:int64; mean_probability:float64; observed_success_rate:float64; absolute_gap:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 78
- Unique identifiers: 
- Notes: 

## Fig5a_end_to_end_latency_plot_source.csv

- Relative path: `06_figure_data/Fig05/source_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Fig5a_end_to_end_latency_plot_source.csv`
- Dataset role: 06_figure_data
- Rows: 190
- Columns: 8
- Column names: method; timing_view; repeat; execution_order; validation_target_times; total_seconds; latency_ms_per_target; throughput_target_times_per_second
- Data types: method:object; timing_view:object; repeat:int64; execution_order:int64; validation_target_times:int64; total_seconds:float64; latency_ms_per_target:float64; throughput_target_times_per_second:float64
- Units if known: Not automatically verified
- Date/time column: validation_target_times; throughput_target_times_per_second
- Date range: 1970-01-01 00:00:00.000001431 to 1970-01-01 00:00:00.000001431
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Fig5b_Pareto_plot_source.csv

- Relative path: `06_figure_data/Fig05/source_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Fig5b_Pareto_plot_source.csv`
- Dataset role: 06_figure_data
- Rows: 7
- Columns: 11
- Column names: method; validation_samples; mean_normalized_regret; median_latency_ms; p95_latency_ms; median_throughput; median_fit_seconds; peak_inference_ram_bytes; model_size_kb; peak_inference_ram_mb; pareto_nondominated
- Data types: method:object; validation_samples:int64; mean_normalized_regret:float64; median_latency_ms:float64; p95_latency_ms:float64; median_throughput:float64; median_fit_seconds:float64; peak_inference_ram_bytes:int64; model_size_kb:float64; peak_inference_ram_mb:float64; pareto_nondominated:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Fig5c_Selection_Ablation_plot_source.csv

- Relative path: `06_figure_data/Fig05/source_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Fig5c_Selection_Ablation_plot_source.csv`
- Dataset role: 06_figure_data
- Rows: 7
- Columns: 12
- Column names: variant; N; mean_normalized_regret; median_normalized_regret; mean_raw_regret_mph; median_raw_regret_mph; exact_top1_accuracy; top2_hit_rate; near_oracle_hit_rate_0p5; development_smoke_only; delta_nr_vs_full; relative_degradation_pct
- Data types: variant:object; N:int64; mean_normalized_regret:float64; median_normalized_regret:float64; mean_raw_regret_mph:float64; median_raw_regret_mph:float64; exact_top1_accuracy:float64; top2_hit_rate:float64; near_oracle_hit_rate_0p5:float64; development_smoke_only:bool; delta_nr_vs_full:float64; relative_degradation_pct:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Inference_Latency.csv

- Relative path: `06_figure_data/Fig05/processed_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Step2E_Inference_Latency.csv`
- Dataset role: 06_figure_data
- Rows: 202
- Columns: 8
- Column names: method; timing_view; repeat; execution_order; validation_target_times; total_seconds; latency_ms_per_target; throughput_target_times_per_second
- Data types: method:object; timing_view:object; repeat:int64; execution_order:object; validation_target_times:int64; total_seconds:float64; latency_ms_per_target:float64; throughput_target_times_per_second:float64
- Units if known: Not automatically verified
- Date/time column: validation_target_times; throughput_target_times_per_second
- Date range: 1970-01-01 00:00:00.000001431 to 1970-01-01 00:00:00.000001431
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Pareto_Analysis.csv

- Relative path: `06_figure_data/Fig05/processed_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Step2E_Pareto_Analysis.csv`
- Dataset role: 06_figure_data
- Rows: 7
- Columns: 11
- Column names: method; validation_samples; mean_normalized_regret; median_latency_ms; p95_latency_ms; median_throughput; median_fit_seconds; peak_inference_ram_bytes; model_size_kb; peak_inference_ram_mb; pareto_nondominated
- Data types: method:object; validation_samples:int64; mean_normalized_regret:float64; median_latency_ms:float64; p95_latency_ms:float64; median_throughput:float64; median_fit_seconds:float64; peak_inference_ram_bytes:int64; model_size_kb:float64; peak_inference_ram_mb:float64; pareto_nondominated:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Regret_Latency_SourceData.csv

- Relative path: `06_figure_data/Fig05/processed_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Step2E_Regret_Latency_SourceData.csv`
- Dataset role: 06_figure_data
- Rows: 7
- Columns: 11
- Column names: method; validation_samples; mean_normalized_regret; median_latency_ms; p95_latency_ms; median_throughput; median_fit_seconds; peak_inference_ram_bytes; model_size_kb; peak_inference_ram_mb; pareto_nondominated
- Data types: method:object; validation_samples:int64; mean_normalized_regret:float64; median_latency_ms:float64; p95_latency_ms:float64; median_throughput:float64; median_fit_seconds:float64; peak_inference_ram_bytes:int64; model_size_kb:float64; peak_inference_ram_mb:float64; pareto_nondominated:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Throughput.csv

- Relative path: `06_figure_data/Fig05/processed_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Step2E_Throughput.csv`
- Dataset role: 06_figure_data
- Rows: 7
- Columns: 3
- Column names: method; mean_throughput; median_throughput
- Data types: method:object; mean_throughput:float64; median_throughput:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2G_Ablation_Weights__05_Fig5_Efficiency_Ablation.csv

- Relative path: `06_figure_data/Fig05/processed_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Step2G_Ablation_Weights__05_Fig5_Efficiency_Ablation.csv`
- Dataset role: 06_figure_data
- Rows: 7
- Columns: 12
- Column names: variant; components; fit_type; optimizer_success; objective; iterations; weight_Q; weight_S; weight_D; weight_C; optimizer_status; optimizer_message
- Data types: variant:object; components:object; fit_type:object; optimizer_success:bool; objective:float64; iterations:int64; weight_Q:float64; weight_S:float64; weight_D:float64; weight_C:float64; optimizer_status:float64; optimizer_message:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 5
- Unique identifiers: 
- Notes: 

## Step2G_Paired_Development_Comparisons__05_Fig5_Efficiency_Ablation.csv

- Relative path: `06_figure_data/Fig05/processed_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Step2G_Paired_Development_Comparisons__05_Fig5_Efficiency_Ablation.csv`
- Dataset role: 06_figure_data
- Rows: 12
- Columns: 10
- Column names: comparison; metric; observed_difference; bootstrap_mean; ci95_lower; ci95_upper; repetitions; cluster; seed; development_only
- Data types: comparison:object; metric:object; observed_difference:float64; bootstrap_mean:float64; ci95_lower:float64; ci95_upper:float64; repetitions:int64; cluster:object; seed:int64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2G_Station_Level_Ablation__05_Fig5_Efficiency_Ablation.csv

- Relative path: `06_figure_data/Fig05/processed_data/fig/图片数据/05_Fig5_Efficiency_Ablation/Step2G_Station_Level_Ablation__05_Fig5_Efficiency_Ablation.csv`
- Dataset role: 06_figure_data
- Rows: 1197
- Columns: 6
- Column names: variant; target_station; N; mean_normalized_regret; near_oracle_hit_rate_0p5; exact_top1_accuracy
- Data types: variant:object; target_station:int64; N:int64; mean_normalized_regret:float64; near_oracle_hit_rate_0p5:float64; exact_top1_accuracy:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## EXPORT_MANIFEST.csv

- Relative path: `07_figures/PNG/fig/正式图/EXPORT_MANIFEST.csv`
- Dataset role: 07_figures
- Rows: 20
- Columns: 7
- Column names: filename; format; width_px; height_px; aspect_ratio; size_bytes; sha256
- Data types: filename:object; format:object; width_px:int64; height_px:int64; aspect_ratio:object; size_bytes:int64; sha256:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## model_lock__00_CONFIG.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/00_CONFIG/model_lock__00_CONFIG.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 12
- Column names: xgb_best_iteration; gru_best_epoch; xgb_feature_set_locked; gru_architecture_locked; scaler_locked; encoder_locked; test_used_for_tuning; locked_before_test; training_complete; created_before_test_inference; artifact_sha256; smoke
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## run_state__00_CONFIG.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/00_CONFIG/run_state__00_CONFIG.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 3
- Column names: mode; stages; run_id
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## evaluation_sample_counts__01_EVALUATION_SCOPE.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/01_EVALUATION_SCOPE/evaluation_sample_counts__01_EVALUATION_SCOPE.csv`
- Dataset role: 02_training_data
- Rows: 3
- Columns: 4
- Column names: split; rows; stations; seen_rows
- Data types: split:object; rows:int64; stations:int64; seen_rows:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## evaluation_scope__01_EVALUATION_SCOPE.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/01_EVALUATION_SCOPE/evaluation_scope__01_EVALUATION_SCOPE.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 20
- Column names: primary_task; primary_validation; primary_test; secondary_test; robustness_test; source; train_rows; train_stations; primary_validation_rows; primary_validation_stations; primary_test_rows; primary_test_stations; full_test_rows; full_test_stations; unseen_test_rows; unseen_test_stations; unseen_validation_rows; frozen; smoke; chronological_ranges_valid
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## seen_test_station_ids__01_EVALUATION_SCOPE.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/01_EVALUATION_SCOPE/seen_test_station_ids__01_EVALUATION_SCOPE.csv`
- Dataset role: 02_training_data
- Rows: 231
- Columns: 1
- Column names: station_id
- Data types: station_id:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## seen_validation_station_ids__01_EVALUATION_SCOPE.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/01_EVALUATION_SCOPE/seen_validation_station_ids__01_EVALUATION_SCOPE.csv`
- Dataset role: 02_training_data
- Rows: 203
- Columns: 1
- Column names: station_id
- Data types: station_id:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## unseen_test_station_ids__01_EVALUATION_SCOPE.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/01_EVALUATION_SCOPE/unseen_test_station_ids__01_EVALUATION_SCOPE.csv`
- Dataset role: 02_training_data
- Rows: 25
- Columns: 1
- Column names: station_id
- Data types: station_id:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## unseen_validation_station_ids__01_EVALUATION_SCOPE.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/01_EVALUATION_SCOPE/unseen_validation_station_ids__01_EVALUATION_SCOPE.csv`
- Dataset role: 02_training_data
- Rows: 9
- Columns: 1
- Column names: station_id
- Data types: station_id:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## ha_config__03_HISTORICAL_AVERAGE.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/03_HISTORICAL_AVERAGE/ha_config__03_HISTORICAL_AVERAGE.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 3
- Column names: levels; fit_source; training_seconds
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## historical_average_fallback_summary__03_HISTORICAL_AVERAGE.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/03_HISTORICAL_AVERAGE/historical_average_fallback_summary__03_HISTORICAL_AVERAGE.csv`
- Dataset role: 02_training_data
- Rows: 14
- Columns: 4
- Column names: split; fallback_level; count; percentage
- Data types: split:object; fallback_level:int64; count:int64; percentage:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## category_encoder__04_XGBOOST.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/04_XGBOOST/category_encoder__04_XGBOOST.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 4
- Column names: categories; fit_source; unknown; numeric_features
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## xgb_train_profile__04_XGBOOST.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/04_XGBOOST/xgb_train_profile__04_XGBOOST.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 8
- Column names: device; training_seconds; feature_prepare_seconds; best_iteration; train_rows; primary_validation_rows; peak_ram_gb; early_stopping_source
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## xgboost_H30__04_XGBOOST.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/04_XGBOOST/xgboost_H30__04_XGBOOST.json`
- Dataset role: 02_training_data
- Rows: 
- Columns: 
- Column names: 
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Not inspected due to size / format.

## gru_epoch_history__05_GRU.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/05_GRU/gru_epoch_history__05_GRU.csv`
- Dataset role: 02_training_data
- Rows: 27
- Columns: 5
- Column names: epoch; train_loss; validation_loss; train_seconds; validation_seconds
- Data types: epoch:int64; train_loss:float64; validation_loss:float64; train_seconds:float64; validation_seconds:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## gru_scaler__05_GRU.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/05_GRU/gru_scaler__05_GRU.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 6
- Column names: variables; mean; std; fit_source; sequence_order; context
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## gru_train_profile__05_GRU.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/05_GRU/gru_train_profile__05_GRU.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 9
- Column names: device; training_seconds; epochs_completed; best_epoch; median_train_seconds_per_epoch; median_validation_seconds_per_epoch; batch_size; peak_ram_gb; early_stopping_source
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## test_predictions_H30__06_PREDICTIONS.parquet

- Relative path: `09_model_outputs/predictions/training_data/01_STEP1B_FULL_H30/06_PREDICTIONS/test_predictions_H30__06_PREDICTIONS.parquet`
- Dataset role: 09_model_outputs
- Rows: 
- Columns: 
- Column names: 
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Inspection failed or skipped: FileNotFoundError: [WinError 2] Failed to open local file 'D:/OneDrive/桌面/论文/2027年投稿期刊/论文项目/01_JEV_小论文_Transportmetrica A Transport Science/github_update/09_model_outputs/predictions/training_data/01_STEP1B_FULL_H30/06_PREDICTIONS/test_predictions_H30__06_PREDICTIONS.parquet'. Detail: [Windows error 2] 系统找不到指定的文件。


## validation_predictions_H30__06_PREDICTIONS.parquet

- Relative path: `09_model_outputs/predictions/training_data/01_STEP1B_FULL_H30/06_PREDICTIONS/validation_predictions_H30__06_PREDICTIONS.parquet`
- Dataset role: 09_model_outputs
- Rows: 
- Columns: 
- Column names: 
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Inspection failed or skipped: FileNotFoundError: [WinError 2] Failed to open local file 'D:/OneDrive/桌面/论文/2027年投稿期刊/论文项目/01_JEV_小论文_Transportmetrica A Transport Science/github_update/09_model_outputs/predictions/training_data/01_STEP1B_FULL_H30/06_PREDICTIONS/validation_predictions_H30__06_PREDICTIONS.parquet'. Detail: [Windows error 2] 系统找不到指定的文件。


## full_h30_forecasting_results__07_METRICS.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/07_METRICS/full_h30_forecasting_results__07_METRICS.csv`
- Dataset role: 02_training_data
- Rows: 16
- Columns: 12
- Column names: model; scope; stations; N; MAE; RMSE; Bias; P50_AE; P75_AE; P90_AE; P95_AE; P99_AE
- Data types: model:object; scope:object; stations:int64; N:int64; MAE:float64; RMSE:float64; Bias:float64; P50_AE:float64; P75_AE:float64; P90_AE:float64; P95_AE:float64; P99_AE:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## full_h30_quality_results__08_SUBGROUP_ANALYSIS.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/08_SUBGROUP_ANALYSIS/full_h30_quality_results__08_SUBGROUP_ANALYSIS.csv`
- Dataset role: 02_training_data
- Rows: 24
- Columns: 14
- Column names: dimension; group; model; stations; days; N; MAE; RMSE; Bias; P50_AE; P75_AE; P90_AE; P95_AE; P99_AE
- Data types: dimension:object; group:object; model:object; stations:int64; days:int64; N:int64; MAE:float64; RMSE:float64; Bias:float64; P50_AE:float64; P75_AE:float64; P90_AE:float64; P95_AE:float64; P99_AE:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 32
- Unique identifiers: 
- Notes: 

## q0_degraded_results__08_SUBGROUP_ANALYSIS.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/08_SUBGROUP_ANALYSIS/q0_degraded_results__08_SUBGROUP_ANALYSIS.csv`
- Dataset role: 02_training_data
- Rows: 4
- Columns: 14
- Column names: dimension; group; model; stations; days; N; MAE; RMSE; Bias; P50_AE; P75_AE; P90_AE; P95_AE; P99_AE
- Data types: dimension:object; group:object; model:object; stations:int64; days:int64; N:int64; MAE:float64; RMSE:float64; Bias:float64; P50_AE:float64; P75_AE:float64; P90_AE:float64; P95_AE:float64; P99_AE:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## subgroup_results__08_SUBGROUP_ANALYSIS.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/08_SUBGROUP_ANALYSIS/subgroup_results__08_SUBGROUP_ANALYSIS.csv`
- Dataset role: 02_training_data
- Rows: 88
- Columns: 14
- Column names: dimension; group; model; stations; days; N; MAE; RMSE; Bias; P50_AE; P75_AE; P90_AE; P95_AE; P99_AE
- Data types: dimension:object; group:object; model:object; stations:int64; days:int64; N:int64; MAE:float64; RMSE:float64; Bias:float64; P50_AE:float64; P75_AE:float64; P90_AE:float64; P95_AE:float64; P99_AE:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## error_thresholds__09_PAIRED_COMPARISON.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/09_PAIRED_COMPARISON/error_thresholds__09_PAIRED_COMPARISON.csv`
- Dataset role: 02_training_data
- Rows: 24
- Columns: 7
- Column names: scope; model; relation; threshold_mph; N; count; percentage
- Data types: scope:object; model:object; relation:object; threshold_mph:int64; N:int64; count:int64; percentage:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## xgb_vs_gru_paired_error__09_PAIRED_COMPARISON.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/09_PAIRED_COMPARISON/xgb_vs_gru_paired_error__09_PAIRED_COMPARISON.csv`
- Dataset role: 02_training_data
- Rows: 9
- Columns: 13
- Column names: scope; N; mean_delta_AE; median_delta_AE; P25; P75; P90; GRU_better_n; GRU_better_pct; XGB_better_n; XGB_better_pct; tie_n; tie_pct
- Data types: scope:object; N:int64; mean_delta_AE:float64; median_delta_AE:float64; P25:float64; P75:float64; P90:float64; GRU_better_n:int64; GRU_better_pct:float64; XGB_better_n:int64; XGB_better_pct:float64; tie_n:int64; tie_pct:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## latency_benchmark__10_LATENCY.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/10_LATENCY/latency_benchmark__10_LATENCY.csv`
- Dataset role: 02_training_data
- Rows: 8
- Columns: 12
- Column names: model; mode; N; median_seconds; P90_seconds; min_seconds; max_seconds; samples_per_second; microseconds_per_sample; device; runs; batch_size
- Data types: model:object; mode:object; N:int64; median_seconds:float64; P90_seconds:float64; min_seconds:float64; max_seconds:float64; samples_per_second:float64; microseconds_per_sample:float64; device:object; runs:int64; batch_size:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 6
- Unique identifiers: 
- Notes: 

## latency_sample_ids__10_LATENCY.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/10_LATENCY/latency_sample_ids__10_LATENCY.csv`
- Dataset role: 02_training_data
- Rows: 100000
- Columns: 1
- Column names: sample_id
- Data types: sample_id:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## compute_profile__11_RESOURCE_PROFILE.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/11_RESOURCE_PROFILE/compute_profile__11_RESOURCE_PROFILE.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 6
- Column names: Persistence; HistoricalAverage; XGBoost; GRU; cpu; ram_total_gb
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## full_h30_qc__12_QC.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/12_QC/full_h30_qc__12_QC.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 22
- Column names: mode; train_validation_test_time_unchanged; primary_validation_seen_only; primary_test_seen_only; unseen_test_all_absent_from_train; duplicate_sample_id; missing_target; target100_violations; nan_prediction; infinite_prediction; xgb_early_stopping_test_leakage; gru_early_stopping_test_leakage; scaler_test_leakage; encoder_test_leakage; model_locked_before_test; prediction_rows_equal_scope; all_models_same_sample_scope; leakage_violations; smoke_results_not_paper_results; status; xlsx_readback; xlsx_sheets
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step1B_Full_H30_Results.xlsx

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/13_RESULTS_XLSX/Step1B_Full_H30_Results.xlsx`
- Dataset role: 02_training_data
- Rows: 00_Summary:41 rows x 2 columns; 01_DataScope:21 rows x 2 columns; 02_FrozenDesign:19 rows x 2 columns; 03_ModelConfig:15 rows x 2 columns; 04_Accuracy_AllScopes:17 rows x 12 columns; 05_PrimaryTest:5 rows x 12 columns; 06_QualityBins:25 rows x 14 columns; 07_Q0_Degraded:5 rows x 14 columns; 08_SeenUnseen:9 rows x 14 columns; 09_PeakPeriod:13 rows x 14 columns
- Columns: Workbook
- Column names: 00_Summary; 01_DataScope; 02_FrozenDesign; 03_ModelConfig; 04_Accuracy_AllScopes; 05_PrimaryTest; 06_QualityBins; 07_Q0_Degraded; 08_SeenUnseen; 09_PeakPeriod; 10_WeekdayWeekend; 11_FreewayResults; 12_XGB_GRU_Paired; 13_ErrorThresholds; 14_Latency; 15_TrainingRuntime; 16_GRU_EpochHistory; 17_HA_Fallback; 18_ResourceUsage; 19_QC; 20_FileManifest; 21_PaperReady_Table1; 22_PaperReady_Table2; 23_PaperReady_Table3; 24_Notes_Limitations
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step1B_Full_H30_Manifest__15_MANIFEST.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/15_MANIFEST/Step1B_Full_H30_Manifest__15_MANIFEST.csv`
- Dataset role: 02_training_data
- Rows: 37
- Columns: 7
- Column names: filename; relative_path; size_bytes; sha256; created_time; purpose; run_id
- Data types: filename:object; relative_path:object; size_bytes:int64; sha256:object; created_time:object; purpose:object; run_id:object
- Units if known: Not automatically verified
- Date/time column: created_time
- Date range: 2026-09-22 19:19:35.711683 to 2026-09-22 21:50:51.765133
- Missing values: 0
- Unique identifiers: 
- Notes: 

## model_lock__00_CONFIG.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/00_CONFIG/model_lock__00_CONFIG.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 12
- Column names: xgb_best_iteration; gru_best_epoch; xgb_feature_set_locked; gru_architecture_locked; scaler_locked; encoder_locked; test_used_for_tuning; locked_before_test; training_complete; created_before_test_inference; artifact_sha256; smoke
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## run_state__00_CONFIG.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/00_CONFIG/run_state__00_CONFIG.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 3
- Column names: mode; stages; run_id
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## evaluation_sample_counts__01_EVALUATION_SCOPE.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/01_EVALUATION_SCOPE/evaluation_sample_counts__01_EVALUATION_SCOPE.csv`
- Dataset role: 02_training_data
- Rows: 3
- Columns: 4
- Column names: split; rows; stations; seen_rows
- Data types: split:object; rows:int64; stations:int64; seen_rows:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## evaluation_scope__01_EVALUATION_SCOPE.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/01_EVALUATION_SCOPE/evaluation_scope__01_EVALUATION_SCOPE.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 20
- Column names: primary_task; primary_validation; primary_test; secondary_test; robustness_test; source; train_rows; train_stations; primary_validation_rows; primary_validation_stations; primary_test_rows; primary_test_stations; full_test_rows; full_test_stations; unseen_test_rows; unseen_test_stations; unseen_validation_rows; frozen; smoke; chronological_ranges_valid
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## seen_test_station_ids__01_EVALUATION_SCOPE.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/01_EVALUATION_SCOPE/seen_test_station_ids__01_EVALUATION_SCOPE.csv`
- Dataset role: 02_training_data
- Rows: 196
- Columns: 1
- Column names: station_id
- Data types: station_id:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## seen_validation_station_ids__01_EVALUATION_SCOPE.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/01_EVALUATION_SCOPE/seen_validation_station_ids__01_EVALUATION_SCOPE.csv`
- Dataset role: 02_training_data
- Rows: 196
- Columns: 1
- Column names: station_id
- Data types: station_id:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## unseen_test_station_ids__01_EVALUATION_SCOPE.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/01_EVALUATION_SCOPE/unseen_test_station_ids__01_EVALUATION_SCOPE.csv`
- Dataset role: 02_training_data
- Rows: 0
- Columns: 1
- Column names: station_id
- Data types: station_id:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## unseen_validation_station_ids__01_EVALUATION_SCOPE.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/01_EVALUATION_SCOPE/unseen_validation_station_ids__01_EVALUATION_SCOPE.csv`
- Dataset role: 02_training_data
- Rows: 0
- Columns: 1
- Column names: station_id
- Data types: station_id:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## ha_config__03_HISTORICAL_AVERAGE.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/03_HISTORICAL_AVERAGE/ha_config__03_HISTORICAL_AVERAGE.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 3
- Column names: levels; fit_source; training_seconds
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## historical_average_fallback_summary__03_HISTORICAL_AVERAGE.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/03_HISTORICAL_AVERAGE/historical_average_fallback_summary__03_HISTORICAL_AVERAGE.csv`
- Dataset role: 02_training_data
- Rows: 14
- Columns: 4
- Column names: split; fallback_level; count; percentage
- Data types: split:object; fallback_level:int64; count:int64; percentage:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## category_encoder__04_XGBOOST.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/04_XGBOOST/category_encoder__04_XGBOOST.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 4
- Column names: categories; fit_source; unknown; numeric_features
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## xgb_train_profile__04_XGBOOST.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/04_XGBOOST/xgb_train_profile__04_XGBOOST.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 8
- Column names: device; training_seconds; feature_prepare_seconds; best_iteration; train_rows; primary_validation_rows; peak_ram_gb; early_stopping_source
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## xgboost_H30__04_XGBOOST.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/04_XGBOOST/xgboost_H30__04_XGBOOST.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 2
- Column names: learner; version
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## gru_epoch_history__05_GRU.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/05_GRU/gru_epoch_history__05_GRU.csv`
- Dataset role: 02_training_data
- Rows: 1
- Columns: 5
- Column names: epoch; train_loss; validation_loss; train_seconds; validation_seconds
- Data types: epoch:int64; train_loss:float64; validation_loss:float64; train_seconds:float64; validation_seconds:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## gru_scaler__05_GRU.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/05_GRU/gru_scaler__05_GRU.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 6
- Column names: variables; mean; std; fit_source; sequence_order; context
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## gru_train_profile__05_GRU.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/05_GRU/gru_train_profile__05_GRU.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 9
- Column names: device; training_seconds; epochs_completed; best_epoch; median_train_seconds_per_epoch; median_validation_seconds_per_epoch; batch_size; peak_ram_gb; early_stopping_source
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## test_predictions_H30__06_PREDICTIONS.parquet

- Relative path: `09_model_outputs/predictions/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/06_PREDICTIONS/test_predictions_H30__06_PREDICTIONS.parquet`
- Dataset role: 09_model_outputs
- Rows: 51851
- Columns: 29
- Column names: sample_id; station_id; prediction_timestamp_local; prediction_timestamp_utc; freeway; direction; input_observed_pct; input_quality_bin; target_speed; target_observed_pct; is_weekend; prediction_persistence; prediction_HA; prediction_XGB; prediction_GRU; error_persistence; AE_persistence; error_HA; AE_HA; error_XGB; AE_XGB; error_GRU; AE_GRU; SE_XGB; SE_GRU; delta_AE_XGB_GRU; is_seen_station; is_unseen_station; peak_period
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Inspection failed or skipped: TypeError: an integer is required

## validation_predictions_H30__06_PREDICTIONS.parquet

- Relative path: `09_model_outputs/predictions/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/06_PREDICTIONS/validation_predictions_H30__06_PREDICTIONS.parquet`
- Dataset role: 09_model_outputs
- Rows: 52857
- Columns: 29
- Column names: sample_id; station_id; prediction_timestamp_local; prediction_timestamp_utc; freeway; direction; input_observed_pct; input_quality_bin; target_speed; target_observed_pct; is_weekend; prediction_persistence; prediction_HA; prediction_XGB; prediction_GRU; error_persistence; AE_persistence; error_HA; AE_HA; error_XGB; AE_XGB; error_GRU; AE_GRU; SE_XGB; SE_GRU; delta_AE_XGB_GRU; is_seen_station; is_unseen_station; peak_period
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Inspection failed or skipped: TypeError: an integer is required

## full_h30_forecasting_results__07_METRICS.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/07_METRICS/full_h30_forecasting_results__07_METRICS.csv`
- Dataset role: 02_training_data
- Rows: 16
- Columns: 12
- Column names: model; scope; stations; N; MAE; RMSE; Bias; P50_AE; P75_AE; P90_AE; P95_AE; P99_AE
- Data types: model:object; scope:object; stations:int64; N:int64; MAE:float64; RMSE:float64; Bias:float64; P50_AE:float64; P75_AE:float64; P90_AE:float64; P95_AE:float64; P99_AE:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 32
- Unique identifiers: 
- Notes: 

## full_h30_quality_results__08_SUBGROUP_ANALYSIS.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/08_SUBGROUP_ANALYSIS/full_h30_quality_results__08_SUBGROUP_ANALYSIS.csv`
- Dataset role: 02_training_data
- Rows: 24
- Columns: 14
- Column names: dimension; group; model; stations; days; N; MAE; RMSE; Bias; P50_AE; P75_AE; P90_AE; P95_AE; P99_AE
- Data types: dimension:object; group:object; model:object; stations:int64; days:int64; N:int64; MAE:float64; RMSE:float64; Bias:float64; P50_AE:float64; P75_AE:float64; P90_AE:float64; P95_AE:float64; P99_AE:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 64
- Unique identifiers: 
- Notes: 

## q0_degraded_results__08_SUBGROUP_ANALYSIS.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/08_SUBGROUP_ANALYSIS/q0_degraded_results__08_SUBGROUP_ANALYSIS.csv`
- Dataset role: 02_training_data
- Rows: 4
- Columns: 14
- Column names: dimension; group; model; stations; days; N; MAE; RMSE; Bias; P50_AE; P75_AE; P90_AE; P95_AE; P99_AE
- Data types: dimension:object; group:object; model:object; stations:int64; days:int64; N:int64; MAE:float64; RMSE:float64; Bias:float64; P50_AE:float64; P75_AE:float64; P90_AE:float64; P95_AE:float64; P99_AE:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## subgroup_results__08_SUBGROUP_ANALYSIS.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/08_SUBGROUP_ANALYSIS/subgroup_results__08_SUBGROUP_ANALYSIS.csv`
- Dataset role: 02_training_data
- Rows: 80
- Columns: 14
- Column names: dimension; group; model; stations; days; N; MAE; RMSE; Bias; P50_AE; P75_AE; P90_AE; P95_AE; P99_AE
- Data types: dimension:object; group:object; model:object; stations:int64; days:int64; N:int64; MAE:float64; RMSE:float64; Bias:float64; P50_AE:float64; P75_AE:float64; P90_AE:float64; P95_AE:float64; P99_AE:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 32
- Unique identifiers: 
- Notes: 

## error_thresholds__09_PAIRED_COMPARISON.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/09_PAIRED_COMPARISON/error_thresholds__09_PAIRED_COMPARISON.csv`
- Dataset role: 02_training_data
- Rows: 24
- Columns: 7
- Column names: scope; model; relation; threshold_mph; N; count; percentage
- Data types: scope:object; model:object; relation:object; threshold_mph:int64; N:int64; count:int64; percentage:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## xgb_vs_gru_paired_error__09_PAIRED_COMPARISON.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/09_PAIRED_COMPARISON/xgb_vs_gru_paired_error__09_PAIRED_COMPARISON.csv`
- Dataset role: 02_training_data
- Rows: 9
- Columns: 13
- Column names: scope; N; mean_delta_AE; median_delta_AE; P25; P75; P90; GRU_better_n; GRU_better_pct; XGB_better_n; XGB_better_pct; tie_n; tie_pct
- Data types: scope:object; N:int64; mean_delta_AE:float64; median_delta_AE:float64; P25:float64; P75:float64; P90:float64; GRU_better_n:int64; GRU_better_pct:float64; XGB_better_n:int64; XGB_better_pct:float64; tie_n:int64; tie_pct:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 8
- Unique identifiers: 
- Notes: 

## latency_benchmark__10_LATENCY.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/10_LATENCY/latency_benchmark__10_LATENCY.csv`
- Dataset role: 02_training_data
- Rows: 8
- Columns: 12
- Column names: model; mode; N; median_seconds; P90_seconds; min_seconds; max_seconds; samples_per_second; microseconds_per_sample; device; runs; batch_size
- Data types: model:object; mode:object; N:int64; median_seconds:float64; P90_seconds:float64; min_seconds:float64; max_seconds:float64; samples_per_second:float64; microseconds_per_sample:float64; device:object; runs:int64; batch_size:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 6
- Unique identifiers: 
- Notes: 

## latency_sample_ids__10_LATENCY.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/10_LATENCY/latency_sample_ids__10_LATENCY.csv`
- Dataset role: 02_training_data
- Rows: 51851
- Columns: 1
- Column names: sample_id
- Data types: sample_id:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## compute_profile__11_RESOURCE_PROFILE.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/11_RESOURCE_PROFILE/compute_profile__11_RESOURCE_PROFILE.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 6
- Column names: Persistence; HistoricalAverage; XGBoost; GRU; cpu; ram_total_gb
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## full_h30_qc__12_QC.json

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/12_QC/full_h30_qc__12_QC.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 22
- Column names: mode; train_validation_test_time_unchanged; primary_validation_seen_only; primary_test_seen_only; unseen_test_all_absent_from_train; duplicate_sample_id; missing_target; target100_violations; nan_prediction; infinite_prediction; xgb_early_stopping_test_leakage; gru_early_stopping_test_leakage; scaler_test_leakage; encoder_test_leakage; model_locked_before_test; prediction_rows_equal_scope; all_models_same_sample_scope; leakage_violations; smoke_results_not_paper_results; status; xlsx_readback; xlsx_sheets
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step1B_Full_H30_Manifest__15_MANIFEST.csv

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/15_MANIFEST/Step1B_Full_H30_Manifest__15_MANIFEST.csv`
- Dataset role: 02_training_data
- Rows: 36
- Columns: 7
- Column names: filename; relative_path; size_bytes; sha256; created_time; purpose; run_id
- Data types: filename:object; relative_path:object; size_bytes:int64; sha256:object; created_time:object; purpose:object; run_id:object
- Units if known: Not automatically verified
- Date/time column: created_time
- Date range: 2026-09-22 19:09:42.594831 to 2026-09-22 19:14:41.023158
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step1B_SMOKE_TEST_Results.xlsx

- Relative path: `02_training_data/01_H30/training_data/01_STEP1B_FULL_H30/99_SMOKE_TEST/Step1B_SMOKE_TEST_Results.xlsx`
- Dataset role: 02_training_data
- Rows: 00_Summary:41 rows x 2 columns; 01_DataScope:21 rows x 2 columns; 02_FrozenDesign:19 rows x 2 columns; 03_ModelConfig:15 rows x 2 columns; 04_Accuracy_AllScopes:17 rows x 12 columns; 05_PrimaryTest:5 rows x 12 columns; 06_QualityBins:25 rows x 14 columns; 07_Q0_Degraded:5 rows x 14 columns; 08_SeenUnseen:9 rows x 14 columns; 09_PeakPeriod:13 rows x 14 columns
- Columns: Workbook
- Column names: 00_Summary; 01_DataScope; 02_FrozenDesign; 03_ModelConfig; 04_Accuracy_AllScopes; 05_PrimaryTest; 06_QualityBins; 07_Q0_Degraded; 08_SeenUnseen; 09_PeakPeriod; 10_WeekdayWeekend; 11_FreewayResults; 12_XGB_GRU_Paired; 13_ErrorThresholds; 14_Latency; 15_TrainingRuntime; 16_GRU_EpochHistory; 17_HA_Fallback; 18_ResourceUsage; 19_QC; 20_FileManifest; 21_PaperReady_Table1; 22_PaperReady_Table2; 23_PaperReady_Table3; 24_Notes_Limitations
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## production_code_manifest.csv

- Relative path: `02_training_data/01_H30/training_data/90_PRODUCTION_SCRIPTS/STEP1B_FULL_H30/production_code_manifest.csv`
- Dataset role: 02_training_data
- Rows: 3
- Columns: 4
- Column names: filename; size_bytes; sha256; status
- Data types: filename:object; size_bytes:int64; sha256:object; status:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Final_Platt_Refit.json

- Relative path: `02_training_data/06_features/training_data/audit/Stats_Freeze/Final_Platt_Refit.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 17
- Column names: status; calibration_family; family_reselection; fit_split; validation_n; target_definition; input; coefficient; intercept; validation_prevalence; FINAL_BASE_RATE; raw_confidence_q75; monotonic_increasing; model_sha256; input_sha256; source_predictions_sha256; test_loaded
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Final_Platt_Training_Predictions.csv

- Relative path: `09_model_outputs/predictions/training_data/audit/Stats_Freeze/Final_Platt_Training_Predictions.csv`
- Dataset role: 09_model_outputs
- Rows: 1431
- Columns: 7
- Column names: target_station; timestamp; sample_id; jev_raw_confidence; raw_regret_mph; near_oracle_y; final_platt_probability
- Data types: target_station:int64; timestamp:object; sample_id:object; jev_raw_confidence:float64; raw_regret_mph:float64; near_oracle_y:int64; final_platt_probability:float64
- Units if known: Not automatically verified
- Date/time column: timestamp
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-28 23:55:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Stats_Freeze_Boundary_Confirmatory.csv

- Relative path: `02_training_data/06_features/training_data/audit/Stats_Freeze/Stats_Freeze_Boundary_Confirmatory.csv`
- Dataset role: 02_training_data
- Rows: 4
- Columns: 13
- Column names: hypothesis_id; family; endpoint; comparison; difference; alternative; procedure; confirmatory; designation; descriptive_min_n; confirmatory_min_n; confirmatory_min_stations; ineligible_action
- Data types: hypothesis_id:object; family:object; endpoint:object; comparison:object; difference:object; alternative:object; procedure:object; confirmatory:bool; designation:object; descriptive_min_n:int64; confirmatory_min_n:int64; confirmatory_min_stations:int64; ineligible_action:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Stats_Freeze_Boundary_Supporting.csv

- Relative path: `02_training_data/06_features/training_data/audit/Stats_Freeze/Stats_Freeze_Boundary_Supporting.csv`
- Dataset role: 02_training_data
- Rows: 16
- Columns: 5
- Column names: analysis; role; descriptive_min_n; allowed; confirmatory_test
- Data types: analysis:object; role:object; descriptive_min_n:int64; allowed:object; confirmatory_test:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Stats_Freeze_Claims.csv

- Relative path: `02_training_data/06_features/training_data/audit/Stats_Freeze/Stats_Freeze_Claims.csv`
- Dataset role: 02_training_data
- Rows: 6
- Columns: 3
- Column names: claim; value; basis
- Data types: claim:object; value:object; basis:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Stats_Freeze_Comparisons.csv

- Relative path: `02_training_data/06_features/training_data/audit/Stats_Freeze/Stats_Freeze_Comparisons.csv`
- Dataset role: 02_training_data
- Rows: 11
- Columns: 4
- Column names: hypothesis_id; comparison; difference; direction
- Data types: hypothesis_id:object; comparison:object; difference:object; direction:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## STATS_FREEZE_COMPLETE.json

- Relative path: `02_training_data/06_features/training_data/audit/Stats_Freeze/STATS_FREEZE_COMPLETE.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 4
- Column names: status; combined_stats_freeze_sha256; created_utc; test_loaded
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Stats_Freeze_EffectSizes.csv

- Relative path: `02_training_data/06_features/training_data/audit/Stats_Freeze/Stats_Freeze_EffectSizes.csv`
- Dataset role: 02_training_data
- Rows: 5
- Columns: 3
- Column names: domain; natural_scale; standardized_or_relative
- Data types: domain:object; natural_scale:object; standardized_or_relative:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Stats_Freeze_Hypotheses.csv

- Relative path: `02_training_data/06_features/training_data/audit/Stats_Freeze/Stats_Freeze_Hypotheses.csv`
- Dataset role: 02_training_data
- Rows: 11
- Columns: 8
- Column names: hypothesis_id; family; endpoint; comparison; difference; alternative; procedure; confirmatory
- Data types: hypothesis_id:object; family:object; endpoint:object; comparison:object; difference:object; alternative:object; procedure:object; confirmatory:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Stats_Freeze_Metrics.csv

- Relative path: `02_training_data/06_features/training_data/audit/Stats_Freeze/Stats_Freeze_Metrics.csv`
- Dataset role: 02_training_data
- Rows: 14
- Columns: 4
- Column names: domain; metric; role; definition
- Data types: domain:object; metric:object; role:object; definition:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Stats_Freeze_Multiplicity.csv

- Relative path: `02_training_data/06_features/training_data/audit/Stats_Freeze/Stats_Freeze_Multiplicity.csv`
- Dataset role: 02_training_data
- Rows: 3
- Columns: 4
- Column names: family; members; method; alpha
- Data types: family:object; members:object; method:object; alpha:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Stats_Freeze_Summary.json

- Relative path: `02_training_data/06_features/training_data/audit/Stats_Freeze/Stats_Freeze_Summary.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 14
- Column names: status; stats_freeze_status; combined_stats_freeze_sha256; step2h_freeze_sha256; validation_n; final_platt_coefficient; final_platt_intercept; FINAL_BASE_RATE; raw_confidence_q75; final_platt_model_sha256; test_loaded; final_test_executed; python; sklearn
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Production_Preflight.json

- Relative path: `02_training_data/06_features/training_data/audit/Step2B/Step2B_Production_Preflight.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 7
- Column names: status; checks; failures; test_target_samples; test_split_status; full_production_executed; checked_at_utc
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## JEV_v1.0_Feature_Map.csv

- Relative path: `02_training_data/06_features/training_data/audit/Step2B_JEV_v1_0/JEV_v1.0_Feature_Map.csv`
- Dataset role: 02_training_data
- Rows: 13
- Columns: 5
- Column names: evidence; input_feature; transform; fit_scope; max_information_time
- Data types: evidence:object; input_feature:object; transform:object; fit_scope:object; max_information_time:object
- Units if known: Not automatically verified
- Date/time column: max_information_time
- Date range: NaT to NaT
- Missing values: 3
- Unique identifiers: 
- Notes: 

## JEV_v1.0_Formula_Audit.json

- Relative path: `02_training_data/06_features/training_data/audit/Step2B_JEV_v1_0/JEV_v1.0_Formula_Audit.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 5
- Column names: version; status; score_interpretation; checks; forbidden_selector_inputs
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## JEV_v1.0_Freeze_Manifest_SHA256.csv

- Relative path: `02_training_data/06_features/training_data/audit/Step2B_JEV_v1_0/JEV_v1.0_Freeze_Manifest_SHA256.csv`
- Dataset role: 02_training_data
- Rows: 5
- Columns: 3
- Column names: filename; size_bytes; sha256
- Data types: filename:object; size_bytes:int64; sha256:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## JEV_v1.0_Method_Freeze.json

- Relative path: `02_training_data/06_features/training_data/audit/Step2B_JEV_v1_0/JEV_v1.0_Method_Freeze.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 25
- Column names: version; definition_date; status_before_execution; data_previously_viewed; jev_performance_previously_viewed; production_jev_results_viewed; test_results_viewed; test_status; candidate_k; evidence_names; evidence_count; formulas; constants; normalization; tau_d; training_utility; weight_constraints; optimizer; selection_rule; tie_break_rule; raw_confidence_equation; forbidden_future_modifications; score_direction; validation_use; test_use
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## JEV_v1.0_Provenance.json

- Relative path: `02_training_data/06_features/training_data/audit/Step2B_JEV_v1_0/JEV_v1.0_Provenance.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 11
- Column names: JEV_VERSION; JEV_STATUS_BEFORE_THIS_STEP; FORMAL_DEFINITION_DATE; canonical_historical_implementation_found; definition_status; previously_viewed_information; previously_viewed_jev_performance; production_jev_results_viewed; test_results_viewed; test_status; frozen_basis
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2C_Production_Preflight.json

- Relative path: `02_training_data/06_features/training_data/audit/Step2C/Step2C_Production_Preflight.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 11
- Column names: status; checks; failures; audit_items; formal_production_results_exist; completion_evidence; test_loaded; test_target_samples; test_split_status; full_step2c_production_executed; checked_at_utc
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2D_Production_Preflight.json

- Relative path: `02_training_data/06_features/training_data/audit/Step2D/Step2D_Production_Preflight.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 10
- Column names: status; checks; failures; optional_baselines; formal_step2d_production_results_exist; test_loaded; test_target_samples; test_split_status; formal_step2d_production_executed; checked_at_utc
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2D_Freeze_Claims.csv

- Relative path: `02_training_data/06_features/training_data/audit/Step2D_Freeze/Step2D_Freeze_Claims.csv`
- Dataset role: 02_training_data
- Rows: 6
- Columns: 3
- Column names: claim; value; source
- Data types: claim:object; value:object; source:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2D_Freeze_Manifest_SHA256.csv

- Relative path: `02_training_data/06_features/training_data/audit/Step2D_Freeze/Step2D_Freeze_Manifest_SHA256.csv`
- Dataset role: 02_training_data
- Rows: 12
- Columns: 3
- Column names: filename; size_bytes; sha256
- Data types: filename:object; size_bytes:int64; sha256:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Freeze_Claims.csv

- Relative path: `02_training_data/06_features/training_data/audit/Step2E_Freeze/Step2E_Freeze_Claims.csv`
- Dataset role: 02_training_data
- Rows: 5
- Columns: 3
- Column names: claim; value; source
- Data types: claim:object; value:object; source:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Freeze_Manifest_SHA256.csv

- Relative path: `02_training_data/06_features/training_data/audit/Step2E_Freeze/Step2E_Freeze_Manifest_SHA256.csv`
- Dataset role: 02_training_data
- Rows: 15
- Columns: 3
- Column names: filename; size_bytes; sha256
- Data types: filename:object; size_bytes:int64; sha256:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2F_Freeze_Claims.csv

- Relative path: `02_training_data/06_features/training_data/audit/Step2F_Freeze/Step2F_Freeze_Claims.csv`
- Dataset role: 02_training_data
- Rows: 8
- Columns: 3
- Column names: claim; value; source
- Data types: claim:object; value:object; source:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2F_Freeze_Manifest_SHA256.csv

- Relative path: `02_training_data/06_features/training_data/audit/Step2F_Freeze/Step2F_Freeze_Manifest_SHA256.csv`
- Dataset role: 02_training_data
- Rows: 14
- Columns: 3
- Column names: filename; size_bytes; sha256
- Data types: filename:object; size_bytes:int64; sha256:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2G_Freeze_Claims.csv

- Relative path: `02_training_data/06_features/training_data/audit/Step2G_Freeze/Step2G_Freeze_Claims.csv`
- Dataset role: 02_training_data
- Rows: 7
- Columns: 3
- Column names: claim; value; source
- Data types: claim:object; value:object; source:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2G_Freeze_Manifest_SHA256.csv

- Relative path: `02_training_data/06_features/training_data/audit/Step2G_Freeze/Step2G_Freeze_Manifest_SHA256.csv`
- Dataset role: 02_training_data
- Rows: 13
- Columns: 3
- Column names: filename; size_bytes; sha256
- Data types: filename:object; size_bytes:int64; sha256:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2H_Freeze_Claims.csv

- Relative path: `02_training_data/06_features/training_data/audit/Step2H_Freeze/Step2H_Freeze_Claims.csv`
- Dataset role: 02_training_data
- Rows: 10
- Columns: 3
- Column names: claim; value; source
- Data types: claim:object; value:object; source:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2H_Freeze_Manifest_SHA256.csv

- Relative path: `02_training_data/06_features/training_data/audit/Step2H_Freeze/Step2H_Freeze_Manifest_SHA256.csv`
- Dataset role: 02_training_data
- Rows: 14
- Columns: 3
- Column names: filename; size_bytes; sha256
- Data types: filename:object; size_bytes:int64; sha256:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## JEV_v1.0_Model.json

- Relative path: `02_training_data/06_features/training_data/models/Step2B/JEV_v1.0/JEV_v1.0_Model.json`
- Dataset role: 02_training_data
- Rows: JSON object
- Columns: 13
- Column names: version; freeze_hash; feature_evidence_definitions; normalization; degenerate_features; tau_d; weights; optimizer; software_versions; fitting_timestamp_utc; train_candidate_rows; train_target_times; test_status
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## FINAL_TEST_COMPLETE.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/FinalTest/FINAL_TEST_COMPLETE.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 15
- Column names: status; final_test_opened; final_test_opened_once; scientific_computation_status; scientific_qc; integrity; workbook_status; technical_recovery; technical_recovery_classification; technical_recovery_reason; raw_test_reloaded_during_recovery; scientific_recomputation_during_recovery; stats_freeze_sha256; scientific_hash_mismatches; completion_timestamp
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## FINAL_TEST_OPENED.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/FinalTest/FINAL_TEST_OPENED.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 7
- Column names: stats_freeze_sha256; script_sha256; config_sha256; all_model_hashes; opening_timestamp; test_status; run_type
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## FinalTest_Boundary_Confirmatory.csv

- Relative path: `04_experiment_results/05_robustness/training_data/results/FinalTest/FinalTest_Boundary_Confirmatory.csv`
- Dataset role: 04_experiment_results
- Rows: 4
- Columns: 9
- Column names: hypothesis_id; status; comparison; N; stations; raw_effect; raw_p; Holm_p; supported
- Data types: hypothesis_id:object; status:object; comparison:object; N:int64; stations:int64; raw_effect:float64; raw_p:float64; Holm_p:float64; supported:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## FinalTest_Boundary_Supporting.csv

- Relative path: `04_experiment_results/05_robustness/training_data/results/FinalTest/FinalTest_Boundary_Supporting.csv`
- Dataset role: 04_experiment_results
- Rows: 16
- Columns: 6
- Column names: analysis; role; descriptive_min_n; allowed; confirmatory_test; status
- Data types: analysis:object; role:object; descriptive_min_n:int64; allowed:object; confirmatory_test:object; status:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## FinalTest_Claim_Decision_Matrix.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/FinalTest/FinalTest_Claim_Decision_Matrix.csv`
- Dataset role: 04_experiment_results
- Rows: 11
- Columns: 15
- Column names: hypothesis_id; family; endpoint; comparison; direction; raw_effect; effect_size; CI_low; CI_high; raw_p; Holm_p; alpha; supported; allowed_wording; prohibited_wording
- Data types: hypothesis_id:object; family:object; endpoint:object; comparison:object; direction:object; raw_effect:float64; effect_size:float64; CI_low:float64; CI_high:float64; raw_p:float64; Holm_p:float64; alpha:float64; supported:bool; allowed_wording:object; prohibited_wording:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 44
- Unique identifiers: 
- Notes: 

## FinalTest_Downstream_GRU_Sensitivity.csv

- Relative path: `04_experiment_results/01_baselines/training_data/results/FinalTest/FinalTest_Downstream_GRU_Sensitivity.csv`
- Dataset role: 04_experiment_results
- Rows: 7
- Columns: 5
- Column names: method; N; MAE; RMSE; sMAPE
- Data types: method:object; N:int64; MAE:float64; RMSE:float64; sMAPE:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## FinalTest_Downstream_XGB.csv

- Relative path: `04_experiment_results/01_baselines/training_data/results/FinalTest/FinalTest_Downstream_XGB.csv`
- Dataset role: 04_experiment_results
- Rows: 7
- Columns: 5
- Column names: method; N; MAE; RMSE; sMAPE
- Data types: method:object; N:int64; MAE:float64; RMSE:float64; sMAPE:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## FinalTest_Evaluator_Sensitivity.csv

- Relative path: `04_experiment_results/04_sensitivity/training_data/results/FinalTest/FinalTest_Evaluator_Sensitivity.csv`
- Dataset role: 04_experiment_results
- Rows: 7
- Columns: 9
- Column names: method; N_XGB; MAE_XGB; RMSE_XGB; sMAPE_XGB; N_GRU; MAE_GRU; RMSE_GRU; sMAPE_GRU
- Data types: method:object; N_XGB:int64; MAE_XGB:float64; RMSE_XGB:float64; sMAPE_XGB:float64; N_GRU:int64; MAE_GRU:float64; RMSE_GRU:float64; sMAPE_GRU:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## FinalTest_Failure_Profile.csv

- Relative path: `04_experiment_results/05_robustness/training_data/results/FinalTest/FinalTest_Failure_Profile.csv`
- Dataset role: 04_experiment_results
- Rows: 4
- Columns: 3
- Column names: definition; criterion; N
- Data types: definition:object; criterion:object; N:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## FinalTest_Integrity_Audit.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/FinalTest/FinalTest_Integrity_Audit.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 6
- Column names: status; stats_freeze_sha256; script_sha256; config_sha256; scientific_logic_changed_after_open; selector_refit_on_validation
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## FinalTest_Multiplicity.csv

- Relative path: `05_metrics/06_statistical_tests/training_data/results/FinalTest/FinalTest_Multiplicity.csv`
- Dataset role: 05_metrics
- Rows: 11
- Columns: 5
- Column names: hypothesis_id; family; raw_p; Holm_p; supported
- Data types: hypothesis_id:object; family:object; raw_p:float64; Holm_p:float64; supported:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## FinalTest_PreRecovery_State.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/FinalTest/FinalTest_PreRecovery_State.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 9
- Column names: recovery_type; scientific_recomputation; raw_test_reloaded; stats_freeze_changed; scientific_logic_changed; workbook_failure_reason; stats_freeze_sha256; scientific_files_frozen; timestamp
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## FinalTest_Results.xlsx

- Relative path: `04_experiment_results/02_JEV/training_data/results/FinalTest/FinalTest_Results.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; COHORT:None rows x None columns; SELECTOR_PERFORMANCE:None rows x None columns; PRIMARY_COMPARISONS:None rows x None columns; CALIBRATION:None rows x None columns; CONFIDENCE_COMPARISONS:None rows x None columns; RISK_COVERAGE:None rows x None columns; DOWNSTREAM_XGB:None rows x None columns; DOWNSTREAM_GRU:None rows x None columns; BOUNDARY_CONFIRMATORY:None rows x None columns
- Columns: Workbook
- Column names: README; COHORT; SELECTOR_PERFORMANCE; PRIMARY_COMPARISONS; CALIBRATION; CONFIDENCE_COMPARISONS; RISK_COVERAGE; DOWNSTREAM_XGB; DOWNSTREAM_GRU; BOUNDARY_CONFIRMATORY; BOUNDARY_SUPPORTING; FAILURE_PROFILE; EVALUATOR_SENSITIVITY; MULTIPLICITY; CLAIM_MATRIX; QC; INTEGRITY; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## FinalTest_Results.xlsx.bounds.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/FinalTest/FinalTest_Results.xlsx.bounds.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 18
- Column names: README; COHORT; SELECTOR_PERFORMANCE; PRIMARY_COMPARISONS; CALIBRATION; CONFIDENCE_COMPARISONS; RISK_COVERAGE; DOWNSTREAM_XGB; DOWNSTREAM_GRU; BOUNDARY_CONFIRMATORY; BOUNDARY_SUPPORTING; FAILURE_PROFILE; EVALUATOR_SENSITIVITY; MULTIPLICITY; CLAIM_MATRIX; QC; INTEGRITY; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## FinalTest_Runtime.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/FinalTest/FinalTest_Runtime.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 3
- Column names: status; elapsed_seconds_before_workbook; run_type
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## FinalTest_Scientific_Immutability_Audit.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/FinalTest/FinalTest_Scientific_Immutability_Audit.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 9
- Column names: status; files_checked; hash_mismatches; mismatched_files; stats_freeze_changed; stats_freeze_mismatches; scientific_outputs_changed; raw_test_reloaded; timestamp
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## FinalTest_Technical_Recovery.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/FinalTest/FinalTest_Technical_Recovery.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 17
- Column names: status; classification; reason; original_run_opened_once; raw_test_reloaded; scientific_recomputation; statistics_recomputed; models_rerun; stats_freeze_changed; scientific_output_hash_mismatches; original_payload_sha256; sanitized_payload_sha256; nonfinite_value_count; workbook_generated; workbook_qc_status; recovery_timestamp; notes
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## FinalTest_Workbook_Recovery_QC.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/FinalTest/FinalTest_Workbook_Recovery_QC.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 11
- Column names: status; technical_recovery_only; scientific_recalculation; required_sheets; actual_sheets; checks; formula_errors; external_reference_parts; nonfinite_render_failures; workbook_sha256; timestamp
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## FinalTest_WorkbookPayload_NonFinite_Audit.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/FinalTest/FinalTest_WorkbookPayload_NonFinite_Audit.csv`
- Dataset role: 04_experiment_results
- Rows: 48
- Columns: 5
- Column names: json_path; field; original_value; replacement; reason
- Data types: json_path:object; field:object; original_value:float64; replacement:float64; reason:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 96
- Unique identifiers: 
- Notes: 

## Step2A_Feasibility_Report.xlsx

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/production/Step2A_Feasibility_Report.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; CONFIG:None rows x None columns; INPUT_FILES:None rows x None columns; STATION_UNIVERSE:None rows x None columns; CANDIDATE_POOL:None rows x None columns; CANDIDATE_AVAILABILITY:None rows x None columns; NON_EVALUABLE_TARGETS:None rows x None columns; MISSING_CANDIDATES:None rows x None columns; CANDIDATE_SIZE:None rows x None columns; ORACLE_SUMMARY:None rows x None columns
- Columns: Workbook
- Column names: README; CONFIG; INPUT_FILES; STATION_UNIVERSE; CANDIDATE_POOL; CANDIDATE_AVAILABILITY; NON_EVALUABLE_TARGETS; MISSING_CANDIDATES; CANDIDATE_SIZE; ORACLE_SUMMARY; ORACLE_GAP; LOSS_SPREAD; ORACLE_TURNOVER; NEAR_TIES; SPLIT_QC; LEAKAGE_AUDIT; RUNTIME; ISSUES
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2A_Leakage_Audit.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/production/Step2A_Leakage_Audit.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 10
- Column names: status; selector_visible_information_latest_time; candidate_pool_uses_future_information; candidate_features_use_future_information; candidate_features_source; future_target_used_only_for_retrospective_candidate_loss; test_oracle_used_for_feature_or_parameter_selection; test_split_status; test_parquet_loaded; candidate_availability_depends_on_future_target
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2A_Missing_Candidates.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/production/Step2A_Missing_Candidates.csv`
- Dataset role: 04_experiment_results
- Rows: 166
- Columns: 17
- Column names: split; target_station; timestamp; sample_id; requested_K; mapped_candidate_count; available_candidate_count; missing_candidate_count; candidate_pool_complete; primary_selection_evaluable; structural_insufficient_candidate_count; source_history_missing_count; invalid_candidate_feature_count; complete_K5_sample; missing_candidate_reason; source_history_missing_ids; invalid_candidate_feature_ids
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; requested_K:int64; mapped_candidate_count:int64; available_candidate_count:int64; missing_candidate_count:int64; candidate_pool_complete:bool; primary_selection_evaluable:bool; structural_insufficient_candidate_count:int64; source_history_missing_count:int64; invalid_candidate_feature_count:int64; complete_K5_sample:bool; missing_candidate_reason:object; source_history_missing_ids:float64; invalid_candidate_feature_ids:float64
- Units if known: Not automatically verified
- Date/time column: timestamp; mapped_candidate_count; available_candidate_count; missing_candidate_count; candidate_pool_complete; structural_insufficient_candidate_count; invalid_candidate_feature_count; missing_candidate_reason; invalid_candidate_feature_ids
- Date range: 2026-01-02 23:30:00-08:00 to 2026-06-29 23:55:00-07:00
- Missing values: 332
- Unique identifiers: 
- Notes: 

## Step2A_NearTie_Analysis.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/production/Step2A_NearTie_Analysis.csv`
- Dataset role: 04_experiment_results
- Rows: 10600
- Columns: 6
- Column names: split; target_station; timestamp; oracle_gap; near_tie_tolerance_mph; near_tie
- Data types: split:object; target_station:int64; timestamp:object; oracle_gap:float64; near_tie_tolerance_mph:float64; near_tie:bool
- Units if known: Not automatically verified
- Date/time column: timestamp
- Date range: 2026-01-01 19:05:00-08:00 to 2026-06-28 23:55:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Non_Evaluable_Targets.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/production/Step2A_Non_Evaluable_Targets.csv`
- Dataset role: 04_experiment_results
- Rows: 1
- Columns: 6
- Column names: target_station; requested_K; mapped_candidate_count; candidate_pool_complete; primary_selection_evaluable; exclusion_reason
- Data types: target_station:int64; requested_K:int64; mapped_candidate_count:int64; candidate_pool_complete:bool; primary_selection_evaluable:bool; exclusion_reason:object
- Units if known: Not automatically verified
- Date/time column: mapped_candidate_count; candidate_pool_complete
- Date range: 1970-01-01 00:00:00.000000001 to 1970-01-01 00:00:00.000000001
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Oracle_Gap_Distribution.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/production/Step2A_Oracle_Gap_Distribution.csv`
- Dataset role: 04_experiment_results
- Rows: 1
- Columns: 15
- Column names: N; mean; median; SD; min; max; P0; P10; P25; P50; P75; P90; P95; P100; IQR
- Data types: N:int64; mean:float64; median:float64; SD:float64; min:float64; max:float64; P0:float64; P10:float64; P25:float64; P50:float64; P75:float64; P90:float64; P95:float64; P100:float64; IQR:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Production_PreRepair_Manifest_20260923T190204.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/production/Step2A_Production_PreRepair_Manifest_20260923T190204.csv`
- Dataset role: 04_experiment_results
- Rows: 28
- Columns: 5
- Column names: relative_path; size_bytes; sha256; last_write_time; present_before_repair
- Data types: relative_path:object; size_bytes:int64; sha256:object; last_write_time:object; present_before_repair:bool
- Units if known: Not automatically verified
- Date/time column: last_write_time
- Date range: 2026-09-23 18:48:03.300041300+08:00 to 2026-09-23 18:48:36.015525300+08:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Runtime.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2A/production/Step2A_Runtime.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 13
- Column names: python; pandas; numpy; pyarrow; xgboost; cpu; logical_cpu_count; ram_total_gb; start_utc; end_utc; elapsed_seconds; random_seed; raw_days_read
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2A_Target_Candidate_Map.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/production/Step2A_Target_Candidate_Map.csv`
- Dataset role: 04_experiment_results
- Rows: 856
- Columns: 11
- Column names: target_station; candidate_station; candidate_rank; route_freeway; direction; target_postmile; candidate_postmile; distance; distance_unit; candidate_pool_K; candidate_rule
- Data types: target_station:int64; candidate_station:int64; candidate_rank:int64; route_freeway:int64; direction:object; target_postmile:float64; candidate_postmile:float64; distance:float64; distance_unit:object; candidate_pool_K:int64; candidate_rule:object
- Units if known: Not automatically verified
- Date/time column: candidate_station; candidate_rank; candidate_postmile; candidate_pool_K; candidate_rule
- Date range: 1970-01-01 00:00:00.000715938 to 1970-01-01 00:00:00.000777767
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Smoke_Candidate_Set_Size.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/smoke/Step2A_Smoke_Candidate_Set_Size.csv`
- Dataset role: 04_experiment_results
- Rows: 75
- Columns: 8
- Column names: split; target_station; timestamp; sample_id; requested_K; valid_candidates; missing_candidates; missing_candidate_ids
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; requested_K:int64; valid_candidates:int64; missing_candidates:int64; missing_candidate_ids:float64
- Units if known: Not automatically verified
- Date/time column: timestamp; valid_candidates; missing_candidates; missing_candidate_ids
- Date range: 2026-01-03 23:30:00-08:00 to 2026-06-17 11:15:00-07:00
- Missing values: 75
- Unique identifiers: 
- Notes: 

## Step2A_Smoke_Leakage_Audit.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/smoke/Step2A_Smoke_Leakage_Audit.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 9
- Column names: status; selector_visible_information_latest_time; candidate_pool_uses_future_information; candidate_features_use_future_information; candidate_features_source; future_target_used_only_for_retrospective_candidate_loss; test_oracle_used_for_feature_or_parameter_selection; test_used_in_smoke; candidate_availability_depends_on_future_target
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2A_Smoke_NearTie_Analysis.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/smoke/Step2A_Smoke_NearTie_Analysis.csv`
- Dataset role: 04_experiment_results
- Rows: 75
- Columns: 6
- Column names: split; target_station; timestamp; oracle_gap; near_tie_tolerance_mph; near_tie
- Data types: split:object; target_station:int64; timestamp:object; oracle_gap:float64; near_tie_tolerance_mph:float64; near_tie:bool
- Units if known: Not automatically verified
- Date/time column: timestamp
- Date range: 2026-01-03 23:30:00-08:00 to 2026-06-17 11:15:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Smoke_Oracle_Gap_Distribution.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/smoke/Step2A_Smoke_Oracle_Gap_Distribution.csv`
- Dataset role: 04_experiment_results
- Rows: 1
- Columns: 15
- Column names: N; mean; median; SD; min; max; P0; P10; P25; P50; P75; P90; P95; P100; IQR
- Data types: N:int64; mean:float64; median:float64; SD:float64; min:float64; max:float64; P0:float64; P10:float64; P25:float64; P50:float64; P75:float64; P90:float64; P95:float64; P100:float64; IQR:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Smoke_Oracle_Turnover.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/smoke/Step2A_Smoke_Oracle_Turnover.csv`
- Dataset role: 04_experiment_results
- Rows: 5
- Columns: 10
- Column names: target_station; samples; unique_oracle_candidates; dominant_oracle; dominant_oracle_share; oracle_switch_rate; oracle_entropy_bits; mean_oracle_loss; mean_oracle_gap; mean_best_worst_spread
- Data types: target_station:int64; samples:int64; unique_oracle_candidates:int64; dominant_oracle:int64; dominant_oracle_share:float64; oracle_switch_rate:float64; oracle_entropy_bits:float64; mean_oracle_loss:float64; mean_oracle_gap:float64; mean_best_worst_spread:float64
- Units if known: Not automatically verified
- Date/time column: unique_oracle_candidates
- Date range: 1970-01-01 00:00:00.000000003 to 1970-01-01 00:00:00.000000004
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Smoke_Oracle_Utility.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/smoke/Step2A_Smoke_Oracle_Utility.csv`
- Dataset role: 04_experiment_results
- Rows: 375
- Columns: 16
- Column names: split; target_station; timestamp; timestamp_utc; candidate_station; candidate_rank; target_speed; sample_id; prediction; candidate_loss; oracle_source; oracle_loss; oracle_rank; oracle_gap; best_worst_spread; normalized_spread
- Data types: split:object; target_station:int64; timestamp:object; timestamp_utc:object; candidate_station:int64; candidate_rank:int64; target_speed:float64; sample_id:object; prediction:float64; candidate_loss:float64; oracle_source:int64; oracle_loss:float64; oracle_rank:int64; oracle_gap:float64; best_worst_spread:float64; normalized_spread:float64
- Units if known: Not automatically verified
- Date/time column: timestamp; timestamp_utc; candidate_station; candidate_rank; candidate_loss
- Date range: 2026-01-03 23:30:00-08:00 to 2026-06-17 11:15:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Smoke_QC.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/smoke/Step2A_Smoke_QC.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 6
- Column names: status; checks; critical_failures; formal_utility_protocol; formal_utility_implemented; test_used_for_design_or_threshold_selection
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2A_Smoke_Runtime.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2A/smoke/Step2A_Smoke_Runtime.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 13
- Column names: python; pandas; numpy; pyarrow; xgboost; cpu; logical_cpu_count; ram_total_gb; start_utc; end_utc; elapsed_seconds; random_seed; raw_days_read
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2A_Smoke_Summary.xlsx

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/smoke/Step2A_Smoke_Summary.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; CONFIG:None rows x None columns; INPUT_FILES:None rows x None columns; STATION_UNIVERSE:None rows x None columns; CANDIDATE_POOL:None rows x None columns; CANDIDATE_SIZE:None rows x None columns; ORACLE_SUMMARY:None rows x None columns; ORACLE_GAP:None rows x None columns; LOSS_SPREAD:None rows x None columns; ORACLE_TURNOVER:None rows x None columns
- Columns: Workbook
- Column names: README; CONFIG; INPUT_FILES; STATION_UNIVERSE; CANDIDATE_POOL; CANDIDATE_SIZE; ORACLE_SUMMARY; ORACLE_GAP; LOSS_SPREAD; ORACLE_TURNOVER; NEAR_TIES; SPLIT_QC; LEAKAGE_AUDIT; RUNTIME; ISSUES
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2A_Smoke_Target_Candidate_Map.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/smoke/Step2A_Smoke_Target_Candidate_Map.csv`
- Dataset role: 04_experiment_results
- Rows: 856
- Columns: 11
- Column names: target_station; candidate_station; candidate_rank; route_freeway; direction; target_postmile; candidate_postmile; distance; distance_unit; candidate_pool_K; candidate_rule
- Data types: target_station:int64; candidate_station:int64; candidate_rank:int64; route_freeway:int64; direction:object; target_postmile:float64; candidate_postmile:float64; distance:float64; distance_unit:object; candidate_pool_K:int64; candidate_rule:object
- Units if known: Not automatically verified
- Date/time column: candidate_station; candidate_rank; candidate_postmile; candidate_pool_K; candidate_rule
- Date range: 1970-01-01 00:00:00.000715938 to 1970-01-01 00:00:00.000777767
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Smoke_Target_Level_Summary.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/smoke/Step2A_Smoke_Target_Level_Summary.csv`
- Dataset role: 04_experiment_results
- Rows: 5
- Columns: 10
- Column names: target_station; samples; unique_oracle_candidates; dominant_oracle; dominant_oracle_share; oracle_switch_rate; oracle_entropy_bits; mean_oracle_loss; mean_oracle_gap; mean_best_worst_spread
- Data types: target_station:int64; samples:int64; unique_oracle_candidates:int64; dominant_oracle:int64; dominant_oracle_share:float64; oracle_switch_rate:float64; oracle_entropy_bits:float64; mean_oracle_loss:float64; mean_oracle_gap:float64; mean_best_worst_spread:float64
- Units if known: Not automatically verified
- Date/time column: unique_oracle_candidates
- Date range: 1970-01-01 00:00:00.000000003 to 1970-01-01 00:00:00.000000004
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Verification_Candidate_Availability_Audit.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/verification/Step2A_Verification_Candidate_Availability_Audit.csv`
- Dataset role: 04_experiment_results
- Rows: 172
- Columns: 6
- Column names: target_station; requested_K; mapped_candidate_count; candidate_pool_complete; primary_selection_evaluable; exclusion_reason
- Data types: target_station:int64; requested_K:int64; mapped_candidate_count:int64; candidate_pool_complete:bool; primary_selection_evaluable:bool; exclusion_reason:object
- Units if known: Not automatically verified
- Date/time column: mapped_candidate_count; candidate_pool_complete
- Date range: 1970-01-01 00:00:00.000000001 to 1970-01-01 00:00:00.000000005
- Missing values: 171
- Unique identifiers: 
- Notes: 

## Step2A_Verification_Candidate_Set_Size.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/verification/Step2A_Verification_Candidate_Set_Size.csv`
- Dataset role: 04_experiment_results
- Rows: 20
- Columns: 17
- Column names: split; target_station; timestamp; sample_id; requested_K; mapped_candidate_count; available_candidate_count; missing_candidate_count; candidate_pool_complete; primary_selection_evaluable; structural_insufficient_candidate_count; source_history_missing_count; invalid_candidate_feature_count; complete_K5_sample; missing_candidate_reason; source_history_missing_ids; invalid_candidate_feature_ids
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; requested_K:int64; mapped_candidate_count:int64; available_candidate_count:int64; missing_candidate_count:int64; candidate_pool_complete:bool; primary_selection_evaluable:bool; structural_insufficient_candidate_count:int64; source_history_missing_count:int64; invalid_candidate_feature_count:int64; complete_K5_sample:bool; missing_candidate_reason:object; source_history_missing_ids:float64; invalid_candidate_feature_ids:float64
- Units if known: Not automatically verified
- Date/time column: timestamp; mapped_candidate_count; available_candidate_count; missing_candidate_count; candidate_pool_complete; structural_insufficient_candidate_count; invalid_candidate_feature_count; missing_candidate_reason; invalid_candidate_feature_ids
- Date range: 2026-01-02 23:30:00-08:00 to 2026-06-06 07:25:00-07:00
- Missing values: 56
- Unique identifiers: 
- Notes: 

## Step2A_Verification_Leakage_Audit.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/verification/Step2A_Verification_Leakage_Audit.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 10
- Column names: status; selector_visible_information_latest_time; candidate_pool_uses_future_information; candidate_features_use_future_information; candidate_features_source; future_target_used_only_for_retrospective_candidate_loss; test_oracle_used_for_feature_or_parameter_selection; test_split_status; test_parquet_loaded; candidate_availability_depends_on_future_target
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2A_Verification_Missing_Candidates.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/verification/Step2A_Verification_Missing_Candidates.csv`
- Dataset role: 04_experiment_results
- Rows: 4
- Columns: 17
- Column names: split; target_station; timestamp; sample_id; requested_K; mapped_candidate_count; available_candidate_count; missing_candidate_count; candidate_pool_complete; primary_selection_evaluable; structural_insufficient_candidate_count; source_history_missing_count; invalid_candidate_feature_count; complete_K5_sample; missing_candidate_reason; source_history_missing_ids; invalid_candidate_feature_ids
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; requested_K:int64; mapped_candidate_count:int64; available_candidate_count:int64; missing_candidate_count:int64; candidate_pool_complete:bool; primary_selection_evaluable:bool; structural_insufficient_candidate_count:int64; source_history_missing_count:int64; invalid_candidate_feature_count:int64; complete_K5_sample:bool; missing_candidate_reason:object; source_history_missing_ids:float64; invalid_candidate_feature_ids:float64
- Units if known: Not automatically verified
- Date/time column: timestamp; mapped_candidate_count; available_candidate_count; missing_candidate_count; candidate_pool_complete; structural_insufficient_candidate_count; invalid_candidate_feature_count; missing_candidate_reason; invalid_candidate_feature_ids
- Date range: 2026-01-02 23:30:00-08:00 to 2026-06-01 23:35:00-07:00
- Missing values: 8
- Unique identifiers: 
- Notes: 

## Step2A_Verification_NearTie_Analysis.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/verification/Step2A_Verification_NearTie_Analysis.csv`
- Dataset role: 04_experiment_results
- Rows: 16
- Columns: 6
- Column names: split; target_station; timestamp; oracle_gap; near_tie_tolerance_mph; near_tie
- Data types: split:object; target_station:int64; timestamp:object; oracle_gap:float64; near_tie_tolerance_mph:float64; near_tie:bool
- Units if known: Not automatically verified
- Date/time column: timestamp
- Date range: 2026-01-03 23:30:00-08:00 to 2026-06-06 07:25:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Verification_Non_Evaluable_Targets.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/verification/Step2A_Verification_Non_Evaluable_Targets.csv`
- Dataset role: 04_experiment_results
- Rows: 1
- Columns: 6
- Column names: target_station; requested_K; mapped_candidate_count; candidate_pool_complete; primary_selection_evaluable; exclusion_reason
- Data types: target_station:int64; requested_K:int64; mapped_candidate_count:int64; candidate_pool_complete:bool; primary_selection_evaluable:bool; exclusion_reason:object
- Units if known: Not automatically verified
- Date/time column: mapped_candidate_count; candidate_pool_complete
- Date range: 1970-01-01 00:00:00.000000001 to 1970-01-01 00:00:00.000000001
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Verification_Oracle_Gap_Distribution.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/verification/Step2A_Verification_Oracle_Gap_Distribution.csv`
- Dataset role: 04_experiment_results
- Rows: 1
- Columns: 15
- Column names: N; mean; median; SD; min; max; P0; P10; P25; P50; P75; P90; P95; P100; IQR
- Data types: N:int64; mean:float64; median:float64; SD:float64; min:float64; max:float64; P0:float64; P10:float64; P25:float64; P50:float64; P75:float64; P90:float64; P95:float64; P100:float64; IQR:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Verification_Oracle_Turnover.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/verification/Step2A_Verification_Oracle_Turnover.csv`
- Dataset role: 04_experiment_results
- Rows: 4
- Columns: 10
- Column names: target_station; samples; unique_oracle_candidates; dominant_oracle; dominant_oracle_share; oracle_switch_rate; oracle_entropy_bits; mean_oracle_loss; mean_oracle_gap; mean_best_worst_spread
- Data types: target_station:int64; samples:int64; unique_oracle_candidates:int64; dominant_oracle:int64; dominant_oracle_share:float64; oracle_switch_rate:float64; oracle_entropy_bits:float64; mean_oracle_loss:float64; mean_oracle_gap:float64; mean_best_worst_spread:float64
- Units if known: Not automatically verified
- Date/time column: unique_oracle_candidates
- Date range: 1970-01-01 00:00:00.000000002 to 1970-01-01 00:00:00.000000003
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Verification_Oracle_Utility.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/verification/Step2A_Verification_Oracle_Utility.csv`
- Dataset role: 04_experiment_results
- Rows: 80
- Columns: 16
- Column names: split; target_station; timestamp; timestamp_utc; candidate_station; candidate_rank; target_speed; sample_id; prediction; candidate_loss; oracle_source; oracle_loss; oracle_rank; oracle_gap; best_worst_spread; normalized_spread
- Data types: split:object; target_station:int64; timestamp:object; timestamp_utc:object; candidate_station:int64; candidate_rank:int64; target_speed:float64; sample_id:object; prediction:float64; candidate_loss:float64; oracle_source:int64; oracle_loss:float64; oracle_rank:int64; oracle_gap:float64; best_worst_spread:float64; normalized_spread:float64
- Units if known: Not automatically verified
- Date/time column: timestamp; timestamp_utc; candidate_station; candidate_rank; candidate_loss
- Date range: 2026-01-03 23:30:00-08:00 to 2026-06-06 07:25:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Verification_QC.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/verification/Step2A_Verification_QC.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 10
- Column names: status; checks; critical_failures; formal_utility_protocol; formal_utility_implemented; test_used_for_design_or_threshold_selection; test_split_status; station_universe_count; primary_evaluable_target_count; audit_only_target_count
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2A_Verification_Runtime.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2A/verification/Step2A_Verification_Runtime.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 13
- Column names: python; pandas; numpy; pyarrow; xgboost; cpu; logical_cpu_count; ram_total_gb; start_utc; end_utc; elapsed_seconds; random_seed; raw_days_read
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2A_Verification_Target_Candidate_Map.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/verification/Step2A_Verification_Target_Candidate_Map.csv`
- Dataset role: 04_experiment_results
- Rows: 856
- Columns: 11
- Column names: target_station; candidate_station; candidate_rank; route_freeway; direction; target_postmile; candidate_postmile; distance; distance_unit; candidate_pool_K; candidate_rule
- Data types: target_station:int64; candidate_station:int64; candidate_rank:int64; route_freeway:int64; direction:object; target_postmile:float64; candidate_postmile:float64; distance:float64; distance_unit:object; candidate_pool_K:int64; candidate_rule:object
- Units if known: Not automatically verified
- Date/time column: candidate_station; candidate_rank; candidate_postmile; candidate_pool_K; candidate_rule
- Date range: 1970-01-01 00:00:00.000715938 to 1970-01-01 00:00:00.000777767
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Verification_Target_Level_Summary.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/verification/Step2A_Verification_Target_Level_Summary.csv`
- Dataset role: 04_experiment_results
- Rows: 4
- Columns: 10
- Column names: target_station; samples; unique_oracle_candidates; dominant_oracle; dominant_oracle_share; oracle_switch_rate; oracle_entropy_bits; mean_oracle_loss; mean_oracle_gap; mean_best_worst_spread
- Data types: target_station:int64; samples:int64; unique_oracle_candidates:int64; dominant_oracle:int64; dominant_oracle_share:float64; oracle_switch_rate:float64; oracle_entropy_bits:float64; mean_oracle_loss:float64; mean_oracle_gap:float64; mean_best_worst_spread:float64
- Units if known: Not automatically verified
- Date/time column: unique_oracle_candidates
- Date range: 1970-01-01 00:00:00.000000002 to 1970-01-01 00:00:00.000000003
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2A_Production_QC.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2A/结果数据/Step2A_Production_QC.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 10
- Column names: status; checks; critical_failures; formal_utility_protocol; formal_utility_implemented; test_used_for_design_or_threshold_selection; test_split_status; station_universe_count; primary_evaluable_target_count; audit_only_target_count
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Candidate_Scores.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/production/Step2B_Candidate_Scores.csv`
- Dataset role: 04_experiment_results
- Rows: 57240
- Columns: 11
- Column names: split; target_station; timestamp; sample_id; candidate_station; method; predicted_loss_or_score; predicted_rank; raw_jev_score; raw_jev_confidence; deployable
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; candidate_station:int64; method:object; predicted_loss_or_score:float64; predicted_rank:int64; raw_jev_score:float64; raw_jev_confidence:float64; deployable:bool
- Units if known: Not automatically verified
- Date/time column: timestamp; candidate_station
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-28 23:55:00-07:00
- Missing values: 20000
- Unique identifiers: 
- Notes: 

## Step2B_Fairness_Audit__production.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/production/Step2B_Fairness_Audit__production.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 9
- Column names: status; validation_target_times; candidate_k; method_denominators; same_frozen_candidate_losses; same_frozen_candidate_mapping; preprocessing_fit_split; historical_best_fit_split; test_loaded
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Feature_Schema.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/production/Step2B_Feature_Schema.csv`
- Dataset role: 04_experiment_results
- Rows: 33
- Columns: 5
- Column names: feature; family; definition; causal_max_time; fit_scope
- Data types: feature:object; family:object; definition:object; causal_max_time:object; fit_scope:object
- Units if known: Not automatically verified
- Date/time column: causal_max_time
- Date range: NaT to NaT
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_JEV_Confidence_Summary__production.csv

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2B/production/Step2B_JEV_Confidence_Summary__production.csv`
- Dataset role: 05_metrics
- Rows: 3
- Columns: 10
- Column names: metric; N; mean; median; min; max; p05; p25; p75; p95
- Data types: metric:object; N:int64; mean:float64; median:float64; min:float64; max:float64; p05:float64; p25:float64; p75:float64; p95:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_JEV_Evidence__production.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/production/Step2B_JEV_Evidence__production.csv`
- Dataset role: 04_experiment_results
- Rows: 53000
- Columns: 12
- Column names: split; target_station; timestamp; sample_id; candidate_station; Q; S; D; C; jev_score; relative_utility; all_candidate_tie
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; candidate_station:int64; Q:float64; S:float64; D:float64; C:float64; jev_score:float64; relative_utility:float64; all_candidate_tie:bool
- Units if known: Not automatically verified
- Date/time column: timestamp; candidate_station; all_candidate_tie
- Date range: 2026-01-01 19:05:00-08:00 to 2026-02-01 13:10:00-08:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_JEV_v1.0_Production_Model.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/production/Step2B_JEV_v1.0_Production_Model.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 13
- Column names: version; freeze_hash; feature_evidence_definitions; normalization; degenerate_features; tau_d; weights; optimizer; software_versions; fitting_timestamp_utc; train_candidate_rows; train_target_times; test_status
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Leakage_Audit__production.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/production/Step2B_Leakage_Audit__production.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 10
- Column names: status; feature_timestamps_lte_t; forbidden_features_absent; identifiers_absent_from_model_features; preprocessing_train_only; jev_normalization_train_only; jev_weights_train_only; validation_losses_not_used_for_jev_fit; test_split_status; test_rows_loaded
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Paired_Development_Comparisons__production.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/production/Step2B_Paired_Development_Comparisons__production.csv`
- Dataset role: 04_experiment_results
- Rows: 6
- Columns: 9
- Column names: reference_method; comparison_method; validation_target_times; mean_paired_normalized_regret_difference_jev_minus_baseline; median_paired_difference; station_wins; station_ties; station_losses; development_only
- Data types: reference_method:object; comparison_method:object; validation_target_times:int64; mean_paired_normalized_regret_difference_jev_minus_baseline:float64; median_paired_difference:float64; station_wins:int64; station_ties:int64; station_losses:int64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: validation_target_times
- Date range: 1970-01-01 00:00:00.000001431 to 1970-01-01 00:00:00.000001431
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_QC.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/production/Step2B_QC.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 11
- Column names: status; checks; critical_failures; test_split_status; test_target_samples; available_methods; deployable_methods; oracle_role; same_denominator; development_only; full_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Runtime__production.csv

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2B/production/Step2B_Runtime__production.csv`
- Dataset role: 05_metrics
- Rows: 8
- Columns: 10
- Column names: method; shared_feature_preprocessing_seconds; model_fitting_seconds; selector_inference_seconds; total_method_seconds_excluding_shared_preprocessing; total_seconds_including_shared_preprocessing; validation_target_times; inference_ms_per_target_time; target_times_per_second; development_only
- Data types: method:object; shared_feature_preprocessing_seconds:float64; model_fitting_seconds:float64; selector_inference_seconds:float64; total_method_seconds_excluding_shared_preprocessing:float64; total_seconds_including_shared_preprocessing:float64; validation_target_times:int64; inference_ms_per_target_time:float64; target_times_per_second:float64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: validation_target_times; inference_ms_per_target_time; target_times_per_second
- Date range: 1970-01-01 00:00:00.000001431 to 1970-01-01 00:00:00.000001431
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_Runtime.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2B/production/Step2B_Runtime.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 19
- Column names: start_utc; end_utc; elapsed_seconds; feature_construction_seconds; python; numpy; pandas; scikit_learn; xgboost; torch; cpu; logical_cpu_count; raw_days_read; random_seed; test_loaded; ridge_selected_alpha; xgboost_selected_config_index; xgboost_selected_config; gru_epoch_history
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Selector_Predictions.csv

- Relative path: `09_model_outputs/predictions/training_data/results/Step2B/production/Step2B_Selector_Predictions.csv`
- Dataset role: 09_model_outputs
- Rows: 11448
- Columns: 22
- Column names: split; target_station; timestamp; sample_id; method; selected_source; oracle_source; selected_loss; oracle_loss; worst_loss; raw_regret_mph; normalized_regret; all_candidate_tie; exact_top1_hit; near_oracle_hit_0p5; top2_hit; jev_top1_score; jev_top2_score; jev_margin; jev_selected_Q; jev_raw_confidence; deployable
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; method:object; selected_source:int64; oracle_source:int64; selected_loss:float64; oracle_loss:float64; worst_loss:float64; raw_regret_mph:float64; normalized_regret:float64; all_candidate_tie:bool; exact_top1_hit:bool; near_oracle_hit_0p5:bool; top2_hit:bool; jev_top1_score:float64; jev_top2_score:float64; jev_margin:float64; jev_selected_Q:float64; jev_raw_confidence:float64; deployable:bool
- Units if known: Not automatically verified
- Date/time column: timestamp; all_candidate_tie
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-28 23:55:00-07:00
- Missing values: 42930
- Unique identifiers: 
- Notes: 

## Step2B_Station_Level_Summary.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/production/Step2B_Station_Level_Summary.csv`
- Dataset role: 04_experiment_results
- Rows: 1368
- Columns: 7
- Column names: method; target_station; samples; mean_normalized_regret; mean_raw_regret_mph; near_oracle_hit_rate; development_only
- Data types: method:object; target_station:int64; samples:int64; mean_normalized_regret:float64; mean_raw_regret_mph:float64; near_oracle_hit_rate:float64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_Fairness_Audit__smoke.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke/Step2B_Fairness_Audit__smoke.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 11
- Column names: status; validation_target_times; candidate_k; method_denominators; same_frozen_candidate_losses; same_frozen_candidate_mapping; learned_feature_universe; identifiers_excluded; preprocessing_fit_split; historical_best_fit_split; test_loaded
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Leakage_Audit__smoke.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke/Step2B_Leakage_Audit__smoke.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 6
- Column names: status; feature_timestamps_lte_t; forbidden_features_absent; identifiers_absent_from_model_features; preprocessing_train_only; test_split_status
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Paired_Development_Comparisons__smoke.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke/Step2B_Paired_Development_Comparisons__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 0
- Columns: 4
- Column names: reference_method; comparison_method; development_only; status
- Data types: reference_method:object; comparison_method:object; development_only:object; status:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_Smoke_Candidate_Scores__smoke.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke/Step2B_Smoke_Candidate_Scores__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 5130
- Columns: 10
- Column names: split; target_station; timestamp; sample_id; candidate_station; method; predicted_loss_or_score; predicted_rank; raw_jev_score; raw_jev_confidence
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; candidate_station:int64; method:object; predicted_loss_or_score:float64; predicted_rank:int64; raw_jev_score:float64; raw_jev_confidence:float64
- Units if known: Not automatically verified
- Date/time column: timestamp; candidate_station
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-27 23:55:00-07:00
- Missing values: 10260
- Unique identifiers: 
- Notes: 

## Step2B_Smoke_Method_Summary__smoke.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke/Step2B_Smoke_Method_Summary__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 6
- Columns: 9
- Column names: method; validation_samples; mean_normalized_regret; median_normalized_regret; mean_raw_regret_mph; median_raw_regret_mph; near_oracle_hit_rate; top1_accuracy; top2_hit_rate
- Data types: method:object; validation_samples:int64; mean_normalized_regret:float64; median_normalized_regret:float64; mean_raw_regret_mph:float64; median_raw_regret_mph:float64; near_oracle_hit_rate:float64; top1_accuracy:float64; top2_hit_rate:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_Smoke_Predictions__smoke.csv

- Relative path: `09_model_outputs/predictions/training_data/results/Step2B/smoke/Step2B_Smoke_Predictions__smoke.csv`
- Dataset role: 09_model_outputs
- Rows: 1026
- Columns: 16
- Column names: split; target_station; timestamp; sample_id; method; selected_source; oracle_source; selected_loss; oracle_loss; worst_loss; raw_regret_mph; normalized_regret; all_candidate_tie; exact_top1_hit; near_oracle_hit_0p5; top2_hit
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; method:object; selected_source:int64; oracle_source:int64; selected_loss:float64; oracle_loss:float64; worst_loss:float64; raw_regret_mph:float64; normalized_regret:float64; all_candidate_tie:bool; exact_top1_hit:bool; near_oracle_hit_0p5:bool; top2_hit:bool
- Units if known: Not automatically verified
- Date/time column: timestamp; all_candidate_tie
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-27 23:55:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_Smoke_QC__smoke.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke/Step2B_Smoke_QC__smoke.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 11
- Column names: status; checks; critical_failures; test_split_status; test_target_samples; available_methods; jev_status; smoke_train_target_times; smoke_validation_target_times; same_denominator; development_only
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Smoke_Runtime__smoke.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2B/smoke/Step2B_Smoke_Runtime__smoke.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 18
- Column names: start_utc; end_utc; elapsed_seconds; python; numpy; pandas; scikit_learn; xgboost; torch; cpu; logical_cpu_count; raw_days_read; random_seed; test_loaded; ridge_selected_alpha; xgboost_selected_config_index; xgboost_selected_config; gru_epoch_history
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Smoke_Station_Level_Summary__smoke.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke/Step2B_Smoke_Station_Level_Summary__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 30
- Columns: 6
- Column names: method; target_station; samples; mean_normalized_regret; mean_raw_regret_mph; near_oracle_hit_rate
- Data types: method:object; target_station:int64; samples:int64; mean_normalized_regret:float64; mean_raw_regret_mph:float64; near_oracle_hit_rate:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_Smoke_Summary__smoke.xlsx

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke/Step2B_Smoke_Summary__smoke.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; METHOD_SUMMARY:None rows x None columns; SAMPLE_COUNTS:None rows x None columns; STATION_SUMMARY:None rows x None columns; FEATURE_SCHEMA:None rows x None columns; FAIRNESS_AUDIT:None rows x None columns; QC:None rows x None columns; JEV_AUDIT:None rows x None columns; RUNTIME:None rows x None columns
- Columns: Workbook
- Column names: README; METHOD_SUMMARY; SAMPLE_COUNTS; STATION_SUMMARY; FEATURE_SCHEMA; FAIRNESS_AUDIT; QC; JEV_AUDIT; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2B_Fairness_Audit__smoke_final.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke_final/Step2B_Fairness_Audit__smoke_final.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 9
- Column names: status; validation_target_times; candidate_k; method_denominators; same_frozen_candidate_losses; same_frozen_candidate_mapping; preprocessing_fit_split; historical_best_fit_split; test_loaded
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_JEV_Confidence_Summary__smoke_final.csv

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2B/smoke_final/Step2B_JEV_Confidence_Summary__smoke_final.csv`
- Dataset role: 05_metrics
- Rows: 3
- Columns: 10
- Column names: metric; N; mean; median; min; max; p05; p25; p75; p95
- Data types: metric:object; N:int64; mean:float64; median:float64; min:float64; max:float64; p05:float64; p25:float64; p75:float64; p95:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_JEV_Evidence__smoke_final.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke_final/Step2B_JEV_Evidence__smoke_final.csv`
- Dataset role: 04_experiment_results
- Rows: 3040
- Columns: 12
- Column names: split; target_station; timestamp; sample_id; candidate_station; Q; S; D; C; jev_score; relative_utility; all_candidate_tie
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; candidate_station:int64; Q:float64; S:float64; D:float64; C:float64; jev_score:float64; relative_utility:float64; all_candidate_tie:object
- Units if known: Not automatically verified
- Date/time column: timestamp; candidate_station; all_candidate_tie
- Date range: 2026-01-01 23:30:00-08:00 to 2026-06-27 23:55:00-07:00
- Missing values: 1710
- Unique identifiers: 
- Notes: 

## Step2B_JEV_Weights__smoke_final.json

- Relative path: `09_model_outputs/checkpoints/training_data/results/Step2B/smoke_final/Step2B_JEV_Weights__smoke_final.json`
- Dataset role: 09_model_outputs
- Rows: JSON object
- Columns: 5
- Column names: version; combined_freeze_sha256; weights; tau_d; optimizer
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Paired_Development_Comparisons__smoke_final.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke_final/Step2B_Paired_Development_Comparisons__smoke_final.csv`
- Dataset role: 04_experiment_results
- Rows: 6
- Columns: 9
- Column names: reference_method; comparison_method; validation_target_times; mean_paired_normalized_regret_difference_jev_minus_baseline; median_paired_difference; station_wins; station_ties; station_losses; development_only
- Data types: reference_method:object; comparison_method:object; validation_target_times:int64; mean_paired_normalized_regret_difference_jev_minus_baseline:float64; median_paired_difference:float64; station_wins:int64; station_ties:int64; station_losses:int64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: validation_target_times
- Date range: 1970-01-01 00:00:00.000000171 to 1970-01-01 00:00:00.000000171
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_Runtime__smoke_final.csv

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2B/smoke_final/Step2B_Runtime__smoke_final.csv`
- Dataset role: 05_metrics
- Rows: 8
- Columns: 10
- Column names: method; shared_feature_preprocessing_seconds; model_fitting_seconds; selector_inference_seconds; total_method_seconds_excluding_shared_preprocessing; total_seconds_including_shared_preprocessing; validation_target_times; inference_ms_per_target_time; target_times_per_second; development_only
- Data types: method:object; shared_feature_preprocessing_seconds:float64; model_fitting_seconds:float64; selector_inference_seconds:float64; total_method_seconds_excluding_shared_preprocessing:float64; total_seconds_including_shared_preprocessing:float64; validation_target_times:int64; inference_ms_per_target_time:float64; target_times_per_second:float64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: validation_target_times; inference_ms_per_target_time; target_times_per_second
- Date range: 1970-01-01 00:00:00.000000171 to 1970-01-01 00:00:00.000000171
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_Smoke_Candidate_Scores__smoke_final.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke_final/Step2B_Smoke_Candidate_Scores__smoke_final.csv`
- Dataset role: 04_experiment_results
- Rows: 6840
- Columns: 11
- Column names: split; target_station; timestamp; sample_id; candidate_station; method; predicted_loss_or_score; predicted_rank; raw_jev_score; raw_jev_confidence; deployable
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; candidate_station:int64; method:object; predicted_loss_or_score:float64; predicted_rank:int64; raw_jev_score:float64; raw_jev_confidence:float64; deployable:bool
- Units if known: Not automatically verified
- Date/time column: timestamp; candidate_station
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-27 23:55:00-07:00
- Missing values: 11970
- Unique identifiers: 
- Notes: 

## Step2B_Smoke_Method_Summary__smoke_final.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke_final/Step2B_Smoke_Method_Summary__smoke_final.csv`
- Dataset role: 04_experiment_results
- Rows: 8
- Columns: 11
- Column names: method; validation_samples; mean_normalized_regret; median_normalized_regret; mean_raw_regret_mph; median_raw_regret_mph; near_oracle_hit_rate; top1_accuracy; top2_hit_rate; development_only; deployable
- Data types: method:object; validation_samples:int64; mean_normalized_regret:float64; median_normalized_regret:float64; mean_raw_regret_mph:float64; median_raw_regret_mph:float64; near_oracle_hit_rate:float64; top1_accuracy:float64; top2_hit_rate:float64; development_only:bool; deployable:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_Smoke_Predictions__smoke_final.csv

- Relative path: `09_model_outputs/predictions/training_data/results/Step2B/smoke_final/Step2B_Smoke_Predictions__smoke_final.csv`
- Dataset role: 09_model_outputs
- Rows: 1368
- Columns: 22
- Column names: split; target_station; timestamp; sample_id; method; selected_source; oracle_source; selected_loss; oracle_loss; worst_loss; raw_regret_mph; normalized_regret; all_candidate_tie; exact_top1_hit; near_oracle_hit_0p5; top2_hit; jev_top1_score; jev_top2_score; jev_margin; jev_selected_Q; jev_raw_confidence; deployable
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; method:object; selected_source:int64; oracle_source:int64; selected_loss:float64; oracle_loss:float64; worst_loss:float64; raw_regret_mph:float64; normalized_regret:float64; all_candidate_tie:bool; exact_top1_hit:bool; near_oracle_hit_0p5:bool; top2_hit:bool; jev_top1_score:float64; jev_top2_score:float64; jev_margin:float64; jev_selected_Q:float64; jev_raw_confidence:float64; deployable:bool
- Units if known: Not automatically verified
- Date/time column: timestamp; all_candidate_tie
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-27 23:55:00-07:00
- Missing values: 5985
- Unique identifiers: 
- Notes: 

## Step2B_Smoke_QC__smoke_final.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke_final/Step2B_Smoke_QC__smoke_final.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 11
- Column names: status; checks; critical_failures; test_split_status; test_target_samples; available_methods; deployable_methods; oracle_role; same_denominator; development_only; full_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Smoke_Runtime__smoke_final.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2B/smoke_final/Step2B_Smoke_Runtime__smoke_final.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 19
- Column names: start_utc; end_utc; elapsed_seconds; feature_construction_seconds; python; numpy; pandas; scikit_learn; xgboost; torch; cpu; logical_cpu_count; raw_days_read; random_seed; test_loaded; ridge_selected_alpha; xgboost_selected_config_index; xgboost_selected_config; gru_epoch_history
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_Smoke_Station_Level_Summary__smoke_final.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke_final/Step2B_Smoke_Station_Level_Summary__smoke_final.csv`
- Dataset role: 04_experiment_results
- Rows: 40
- Columns: 7
- Column names: method; target_station; samples; mean_normalized_regret; mean_raw_regret_mph; near_oracle_hit_rate; development_only
- Data types: method:object; target_station:int64; samples:int64; mean_normalized_regret:float64; mean_raw_regret_mph:float64; near_oracle_hit_rate:float64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_Smoke_Summary__smoke_final.xlsx

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B/smoke_final/Step2B_Smoke_Summary__smoke_final.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; METHOD_SUMMARY:None rows x None columns; PAIRED_JEV:None rows x None columns; SAMPLE_COUNTS:None rows x None columns; STATION_SUMMARY:None rows x None columns; JEV_WEIGHTS:None rows x None columns; JEV_EVIDENCE:None rows x None columns; JEV_CONFIDENCE:None rows x None columns; FEATURE_SCHEMA:None rows x None columns; FAIRNESS:None rows x None columns
- Columns: Workbook
- Column names: README; METHOD_SUMMARY; PAIRED_JEV; SAMPLE_COUNTS; STATION_SUMMARY; JEV_WEIGHTS; JEV_EVIDENCE; JEV_CONFIDENCE; FEATURE_SCHEMA; FAIRNESS; LEAKAGE; QC; PREFLIGHT; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2B_J1_QC.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B_JEV_v1_0/J1_Review_Package/Step2B_J1_QC.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 7
- Column names: status; checks; critical_failures; combined_freeze_sha256; model_sha256; test_split_status; development_only
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_J1_Smoke_Summary.xlsx

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B_JEV_v1_0/J1_Review_Package/Step2B_J1_Smoke_Summary.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; METHOD_SUMMARY:None rows x None columns; JEV_WEIGHTS:None rows x None columns; EVIDENCE_SUMMARY:None rows x None columns; CONFIDENCE_SUMMARY:None rows x None columns; UNIT_TESTS:None rows x None columns; QC:None rows x None columns; LEAKAGE:None rows x None columns; FREEZE_CONSISTENCY:None rows x None columns; RUNTIME:None rows x None columns
- Columns: Workbook
- Column names: README; METHOD_SUMMARY; JEV_WEIGHTS; EVIDENCE_SUMMARY; CONFIDENCE_SUMMARY; UNIT_TESTS; QC; LEAKAGE; FREEZE_CONSISTENCY; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2B_J1_Unit_Tests.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B_JEV_v1_0/J1_Review_Package/Step2B_J1_Unit_Tests.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 3
- Column names: status; tests; failed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_JEV_v1.0_Freeze_Consistency_Audit.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B_JEV_v1_0/J1_Review_Package/Step2B_JEV_v1.0_Freeze_Consistency_Audit.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 3
- Column names: status; checks; mismatches
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_JEV_v1.0_Leakage_Audit.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B_JEV_v1_0/J1_Review_Package/Step2B_JEV_v1.0_Leakage_Audit.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 10
- Column names: status; feature_timestamps_lte_t; normalization_fit_train_only; weights_fit_train_only; tau_d_fit_train_only; validation_losses_not_used_for_fit; test_split_status; test_rows_loaded; future_target_not_selector_input; oracle_fields_not_selector_input
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_J1_JEV_Candidate_Scores.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B_JEV_v1_0/smoke/Step2B_J1_JEV_Candidate_Scores.csv`
- Dataset role: 04_experiment_results
- Rows: 855
- Columns: 12
- Column names: split; target_station; timestamp; sample_id; candidate_station; candidate_rank; Q; S; D; C; jev_score; predicted_rank
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; candidate_station:int64; candidate_rank:int64; Q:float64; S:float64; D:float64; C:float64; jev_score:float64; predicted_rank:int64
- Units if known: Not automatically verified
- Date/time column: timestamp; candidate_station; candidate_rank
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-27 23:55:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_J1_JEV_Evidence.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B_JEV_v1_0/smoke/Step2B_J1_JEV_Evidence.csv`
- Dataset role: 04_experiment_results
- Rows: 3040
- Columns: 12
- Column names: split; target_station; timestamp; sample_id; candidate_station; Q; S; D; C; relative_utility; all_candidate_tie; jev_score
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; candidate_station:int64; Q:float64; S:float64; D:float64; C:float64; relative_utility:float64; all_candidate_tie:object; jev_score:float64
- Units if known: Not automatically verified
- Date/time column: timestamp; candidate_station; all_candidate_tie
- Date range: 2026-01-01 23:30:00-08:00 to 2026-06-27 23:55:00-07:00
- Missing values: 3895
- Unique identifiers: 
- Notes: 

## Step2B_J1_JEV_Predictions.csv

- Relative path: `09_model_outputs/predictions/training_data/results/Step2B_JEV_v1_0/smoke/Step2B_J1_JEV_Predictions.csv`
- Dataset role: 09_model_outputs
- Rows: 171
- Columns: 21
- Column names: split; target_station; timestamp; sample_id; method; selected_source; oracle_source; selected_loss; oracle_loss; worst_loss; raw_regret_mph; normalized_regret; all_candidate_tie; exact_top1_hit; near_oracle_hit_0p5; top2_hit; jev_top1_score; jev_top2_score; jev_margin; jev_selected_Q; jev_raw_confidence
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; method:object; selected_source:int64; oracle_source:int64; selected_loss:float64; oracle_loss:float64; worst_loss:float64; raw_regret_mph:float64; normalized_regret:float64; all_candidate_tie:bool; exact_top1_hit:bool; near_oracle_hit_0p5:bool; top2_hit:bool; jev_top1_score:float64; jev_top2_score:float64; jev_margin:float64; jev_selected_Q:float64; jev_raw_confidence:float64
- Units if known: Not automatically verified
- Date/time column: timestamp; all_candidate_tie
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-27 23:55:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2B_J1_JEV_Weights.json

- Relative path: `09_model_outputs/checkpoints/training_data/results/Step2B_JEV_v1_0/smoke/Step2B_J1_JEV_Weights.json`
- Dataset role: 09_model_outputs
- Rows: JSON object
- Columns: 5
- Column names: version; freeze_hash; weights; tau_d; optimizer
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_J1_Runtime.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2B_JEV_v1_0/smoke/Step2B_J1_Runtime.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 10
- Column names: start_utc; end_utc; elapsed_seconds; python; numpy; pandas; cpu; logical_cpu_count; raw_days_read; test_rows_loaded
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2B_J1_Smoke_Method_Summary.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2B_JEV_v1_0/smoke/Step2B_J1_Smoke_Method_Summary.csv`
- Dataset role: 04_experiment_results
- Rows: 7
- Columns: 9
- Column names: method; validation_samples; mean_normalized_regret; median_normalized_regret; mean_raw_regret_mph; median_raw_regret_mph; exact_top1_accuracy; near_oracle_hit_rate_0p5; top2_hit_rate
- Data types: method:object; validation_samples:int64; mean_normalized_regret:float64; median_normalized_regret:float64; mean_raw_regret_mph:float64; median_raw_regret_mph:float64; exact_top1_accuracy:float64; near_oracle_hit_rate_0p5:float64; top2_hit_rate:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2C_Calibration_Predictions__production.csv

- Relative path: `09_model_outputs/predictions/training_data/results/Step2C/production/Step2C_Calibration_Predictions__production.csv`
- Dataset role: 09_model_outputs
- Rows: 1300
- Columns: 13
- Column names: method; sample_id; target_station; timestamp; timestamp_utc; selected_source; raw_regret_mph; y_near_oracle; exact_top1_hit; jev_raw_confidence; predicted_probability; calibration_split; development_only
- Data types: method:object; sample_id:object; target_station:int64; timestamp:object; timestamp_utc:object; selected_source:int64; raw_regret_mph:float64; y_near_oracle:int64; exact_top1_hit:bool; jev_raw_confidence:float64; predicted_probability:float64; calibration_split:object; development_only:bool
- Units if known: Not automatically verified
- Date/time column: timestamp; timestamp_utc
- Date range: 2026-06-14 23:35:00-07:00 to 2026-06-28 23:55:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2C_Calibration_Split__production.csv

- Relative path: `05_metrics/05_calibration/training_data/results/Step2C/production/Step2C_Calibration_Split__production.csv`
- Dataset role: 05_metrics
- Rows: 1431
- Columns: 11
- Column names: sample_id; target_station; timestamp; timestamp_utc; selected_source; raw_regret_mph; exact_top1_hit; jev_raw_confidence; y_near_oracle; calibration_split; development_only
- Data types: sample_id:object; target_station:int64; timestamp:object; timestamp_utc:object; selected_source:int64; raw_regret_mph:float64; exact_top1_hit:bool; jev_raw_confidence:float64; y_near_oracle:int64; calibration_split:object; development_only:bool
- Units if known: Not automatically verified
- Date/time column: timestamp; timestamp_utc
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-28 23:55:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2C_Isotonic_Model__production.json

- Relative path: `04_experiment_results/07_confidence_calibration/training_data/results/Step2C/production/Step2C_Isotonic_Model__production.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 10
- Column names: method; implementation; y_min; y_max; increasing; out_of_bounds; fit_split; fit_n; x_thresholds; y_thresholds
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2C_Leakage_Audit.json

- Relative path: `04_experiment_results/07_confidence_calibration/training_data/results/Step2C/production/Step2C_Leakage_Audit.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 11
- Column names: status; selector_training_data_changed; jev_weights_refit; calibration_fit_split; calibration_evaluation_split; cal_fit_precedes_cal_eval; same_timestamp_cross_split; test_loaded; test_target_samples; test_statistics_used; future_test_information_used
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2C_Platt_Model__production.json

- Relative path: `04_experiment_results/07_confidence_calibration/training_data/results/Step2C/production/Step2C_Platt_Model__production.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 12
- Column names: method; implementation; penalty; solver; max_iter; a; b; converged; iterations; fit_split; fit_n; feature
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2C_Previous_Attempt_Status.json

- Relative path: `04_experiment_results/07_confidence_calibration/training_data/results/Step2C/production/Step2C_Previous_Attempt_Status.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 5
- Column names: status; formal_calibration_started; scientific_results_generated; reason; preserved_log
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## STEP2C_PRODUCTION_COMPLETE.json

- Relative path: `04_experiment_results/07_confidence_calibration/training_data/results/Step2C/production/STEP2C_PRODUCTION_COMPLETE.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 8
- Column names: status; completed_at_utc; qc_status; leakage_status; qc_sha256; selected_method_sha256; test_target_samples; test_split_status
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2C_QC__production.json

- Relative path: `04_experiment_results/07_confidence_calibration/training_data/results/Step2C/production/Step2C_QC__production.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 9
- Column names: status; checks; critical_failures; validation_input_n; split_summary; test_target_samples; test_split_status; development_only; full_step2c_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2C_Results.xlsx

- Relative path: `04_experiment_results/07_confidence_calibration/training_data/results/Step2C/production/Step2C_Results.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; SPLIT:None rows x None columns; METHOD_SUMMARY:None rows x None columns; RELIABILITY_BINS:None rows x None columns; PREDICTIONS_PREVIEW:None rows x None columns; PLATT:None rows x None columns; ISOTONIC:None rows x None columns; QC:None rows x None columns; LEAKAGE:None rows x None columns; RUNTIME:None rows x None columns
- Columns: Workbook
- Column names: README; SPLIT; METHOD_SUMMARY; RELIABILITY_BINS; PREDICTIONS_PREVIEW; PLATT; ISOTONIC; QC; LEAKAGE; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2C_Runtime__production.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2C/production/Step2C_Runtime__production.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 9
- Column names: input_and_split_seconds; platt_fit_seconds; isotonic_fit_seconds; total_seconds_excluding_workbook; python; numpy; pandas; scipy; sklearn
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2C_Selected_Method.json

- Relative path: `04_experiment_results/06_selective_prediction/training_data/results/Step2C/production/Step2C_Selected_Method.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 6
- Column names: selected_method; eligible_methods; selection_rule; selection_split; development_only; future_test_rule
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2C_Calibration_Method_Summary__smoke.csv

- Relative path: `05_metrics/05_calibration/training_data/results/Step2C/smoke/Step2C_Calibration_Method_Summary__smoke.csv`
- Dataset role: 05_metrics
- Rows: 4
- Columns: 11
- Column names: method; cal_eval_n; mean_predicted_probability; observed_success_prevalence; brier_score; nll; ece; eligible_for_final_family; development_only; raw_pearson_with_y; raw_spearman_with_y
- Data types: method:object; cal_eval_n:int64; mean_predicted_probability:float64; observed_success_prevalence:float64; brier_score:float64; nll:float64; ece:float64; eligible_for_final_family:bool; development_only:bool; raw_pearson_with_y:float64; raw_spearman_with_y:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 6
- Unique identifiers: 
- Notes: 

## Step2C_Calibration_Predictions__smoke.csv

- Relative path: `09_model_outputs/predictions/training_data/results/Step2C/smoke/Step2C_Calibration_Predictions__smoke.csv`
- Dataset role: 09_model_outputs
- Rows: 312
- Columns: 13
- Column names: method; sample_id; target_station; timestamp; timestamp_utc; selected_source; raw_regret_mph; y_near_oracle; exact_top1_hit; jev_raw_confidence; predicted_probability; calibration_split; development_only
- Data types: method:object; sample_id:object; target_station:int64; timestamp:object; timestamp_utc:object; selected_source:int64; raw_regret_mph:float64; y_near_oracle:int64; exact_top1_hit:bool; jev_raw_confidence:float64; predicted_probability:float64; calibration_split:object; development_only:bool
- Units if known: Not automatically verified
- Date/time column: timestamp; timestamp_utc
- Date range: 2026-06-11 23:45:00-07:00 to 2026-06-27 23:55:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2C_Calibration_Split__smoke.csv

- Relative path: `05_metrics/05_calibration/training_data/results/Step2C/smoke/Step2C_Calibration_Split__smoke.csv`
- Dataset role: 05_metrics
- Rows: 171
- Columns: 11
- Column names: sample_id; target_station; timestamp; timestamp_utc; selected_source; raw_regret_mph; exact_top1_hit; jev_raw_confidence; y_near_oracle; calibration_split; development_only
- Data types: sample_id:object; target_station:int64; timestamp:object; timestamp_utc:object; selected_source:int64; raw_regret_mph:float64; exact_top1_hit:bool; jev_raw_confidence:float64; y_near_oracle:int64; calibration_split:object; development_only:bool
- Units if known: Not automatically verified
- Date/time column: timestamp; timestamp_utc
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-27 23:55:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2C_Isotonic_Model__smoke.json

- Relative path: `04_experiment_results/07_confidence_calibration/training_data/results/Step2C/smoke/Step2C_Isotonic_Model__smoke.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 10
- Column names: method; implementation; y_min; y_max; increasing; out_of_bounds; fit_split; fit_n; x_thresholds; y_thresholds
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2C_Platt_Model__smoke.json

- Relative path: `04_experiment_results/07_confidence_calibration/training_data/results/Step2C/smoke/Step2C_Platt_Model__smoke.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 12
- Column names: method; implementation; penalty; solver; max_iter; a; b; converged; iterations; fit_split; fit_n; feature
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2C_QC__smoke.json

- Relative path: `04_experiment_results/07_confidence_calibration/training_data/results/Step2C/smoke/Step2C_QC__smoke.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 9
- Column names: status; checks; critical_failures; validation_input_n; split_summary; test_target_samples; test_split_status; development_only; full_step2c_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2C_Reliability_Bins__smoke.csv

- Relative path: `05_metrics/05_calibration/training_data/results/Step2C/smoke/Step2C_Reliability_Bins__smoke.csv`
- Dataset role: 05_metrics
- Rows: 40
- Columns: 8
- Column names: method; bin_id; bin_lower; bin_upper; n; mean_probability; observed_success_rate; absolute_gap
- Data types: method:object; bin_id:int64; bin_lower:float64; bin_upper:float64; n:int64; mean_probability:float64; observed_success_rate:float64; absolute_gap:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 87
- Unique identifiers: 
- Notes: 

## Step2C_Reliability_Diagram_SourceData__smoke.csv

- Relative path: `05_metrics/05_calibration/training_data/results/Step2C/smoke/Step2C_Reliability_Diagram_SourceData__smoke.csv`
- Dataset role: 05_metrics
- Rows: 40
- Columns: 8
- Column names: method; bin_id; bin_lower; bin_upper; n; mean_probability; observed_success_rate; absolute_gap
- Data types: method:object; bin_id:int64; bin_lower:float64; bin_upper:float64; n:int64; mean_probability:float64; observed_success_rate:float64; absolute_gap:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 87
- Unique identifiers: 
- Notes: 

## Step2C_Runtime__smoke.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2C/smoke/Step2C_Runtime__smoke.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 9
- Column names: input_and_split_seconds; platt_fit_seconds; isotonic_fit_seconds; total_seconds_excluding_workbook; python; numpy; pandas; scipy; sklearn
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2C_Smoke_Summary.xlsx

- Relative path: `04_experiment_results/07_confidence_calibration/training_data/results/Step2C/smoke/Step2C_Smoke_Summary.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; SPLIT:None rows x None columns; METHOD_SUMMARY:None rows x None columns; RELIABILITY_BINS:None rows x None columns; PREDICTIONS_PREVIEW:None rows x None columns; PLATT:None rows x None columns; ISOTONIC:None rows x None columns; QC:None rows x None columns; LEAKAGE:None rows x None columns; RUNTIME:None rows x None columns
- Columns: Workbook
- Column names: README; SPLIT; METHOD_SUMMARY; RELIABILITY_BINS; PREDICTIONS_PREVIEW; PLATT; ISOTONIC; QC; LEAKAGE; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2D_Bootstrap_Comparisons__production.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2D/production/Step2D_Bootstrap_Comparisons__production.csv`
- Dataset role: 04_experiment_results
- Rows: 50
- Columns: 10
- Column names: comparison; metric; requested_coverage; estimate_mean; ci_p2_5; ci_p97_5; repetitions; cluster; seed; development_only
- Data types: comparison:object; metric:object; requested_coverage:float64; estimate_mean:float64; ci_p2_5:float64; ci_p97_5:float64; repetitions:int64; cluster:object; seed:int64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 5
- Unique identifiers: 
- Notes: 

## Step2D_Confidence_Baselines__production.csv

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2D/production/Step2D_Confidence_Baselines__production.csv`
- Dataset role: 05_metrics
- Rows: 6
- Columns: 6
- Column names: system; status; n; candidate_k; selected_source_matches_rank1; platt_raw_rank_equivalent
- Data types: system:object; status:object; n:int64; candidate_k:float64; selected_source_matches_rank1:object; platt_raw_rank_equivalent:object
- Units if known: Not automatically verified
- Date/time column: candidate_k
- Date range: 1970-01-01 00:00:00.000000005 to 1970-01-01 00:00:00.000000005
- Missing values: 11
- Unique identifiers: 
- Notes: 

## Step2D_Fixed_Coverage_Summary__production.csv

- Relative path: `05_metrics/02_fixed_coverage_metrics/training_data/results/Step2D/production/Step2D_Fixed_Coverage_Summary__production.csv`
- Dataset role: 05_metrics
- Rows: 63
- Columns: 11
- Column names: ranking; system; requested_coverage; retained_n; realized_coverage; mean_normalized_regret; mean_raw_regret_mph; near_oracle_failure_rate; top1_error_rate; selective_gain; coverage_boundary_tie
- Data types: ranking:object; system:object; requested_coverage:float64; retained_n:int64; realized_coverage:float64; mean_normalized_regret:float64; mean_raw_regret_mph:float64; near_oracle_failure_rate:float64; top1_error_rate:float64; selective_gain:float64; coverage_boundary_tie:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2D_Leakage_Audit.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2D/production/Step2D_Leakage_Audit.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 12
- Column names: status; input_split; cal_fit_rows_used_for_primary_evaluation; test_loaded; test_target_samples; jev_refit; platt_refit; baseline_selectors_refit; future_information_used; coverage_levels_predefined; risk_metric_predefined; aurc_definition_predefined
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## STEP2D_PRODUCTION_COMPLETE.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2D/production/STEP2D_PRODUCTION_COMPLETE.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 6
- Column names: status; completed_at_utc; qc_status; leakage_status; test_target_samples; test_split_status
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2D_QC__production.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2D/production/Step2D_QC__production.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 12
- Column names: status; checks; critical_failures; platt_raw_rank_equivalent; platt_raw_aurc_equivalent; input_n; stations; timestamp_first; timestamp_last; test_target_samples; test_split_status; formal_step2d_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2D_Random_Reference__production.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2D/production/Step2D_Random_Reference__production.csv`
- Dataset role: 04_experiment_results
- Rows: 4
- Columns: 7
- Column names: system; repetitions; seed; random_aurc_mean; random_aurc_p2_5; random_aurc_p97_5; development_only
- Data types: system:object; repetitions:int64; seed:int64; random_aurc_mean:float64; random_aurc_p2_5:float64; random_aurc_p97_5:float64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2D_Results.xlsx

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2D/production/Step2D_Results.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; AURC:None rows x None columns; FIXED_COVERAGE:None rows x None columns; RC_CURVE:None rows x None columns; CONFIDENCE_BASELINES:None rows x None columns; RANDOM_REFERENCE:None rows x None columns; BOOTSTRAP:None rows x None columns; QC:None rows x None columns; LEAKAGE:None rows x None columns; RUNTIME:None rows x None columns
- Columns: Workbook
- Column names: README; AURC; FIXED_COVERAGE; RC_CURVE; CONFIDENCE_BASELINES; RANDOM_REFERENCE; BOOTSTRAP; QC; LEAKAGE; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2D_Risk_Coverage_Curve__production.csv

- Relative path: `05_metrics/03_risk_coverage/training_data/results/Step2D/production/Step2D_Risk_Coverage_Curve__production.csv`
- Dataset role: 05_metrics
- Rows: 2275
- Columns: 8
- Column names: ranking; system; rank_k; coverage; mean_normalized_regret; mean_raw_regret_mph; near_oracle_failure_rate; top1_error_rate
- Data types: ranking:object; system:object; rank_k:int64; coverage:float64; mean_normalized_regret:float64; mean_raw_regret_mph:float64; near_oracle_failure_rate:float64; top1_error_rate:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2D_Runtime__production.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2D/production/Step2D_Runtime__production.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 7
- Column names: total_seconds_excluding_workbook; random_repetitions; bootstrap_repetitions; seed; python; numpy; pandas
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2D_AURC_Summary__smoke.csv

- Relative path: `05_metrics/04_AURC/training_data/results/Step2D/smoke/Step2D_AURC_Summary__smoke.csv`
- Dataset role: 05_metrics
- Rows: 7
- Columns: 11
- Column names: ranking; system; N; aurc; full_coverage_risk; minimum_observed_curve_risk; maximum_observed_curve_risk; confidence_tie_count; coverage_boundary_tie_count; monotonic_violation_count; development_only
- Data types: ranking:object; system:object; N:int64; aurc:float64; full_coverage_risk:float64; minimum_observed_curve_risk:float64; maximum_observed_curve_risk:float64; confidence_tie_count:int64; coverage_boundary_tie_count:int64; monotonic_violation_count:int64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2D_Bootstrap_Comparisons__smoke.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2D/smoke/Step2D_Bootstrap_Comparisons__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 50
- Columns: 10
- Column names: comparison; metric; requested_coverage; estimate_mean; ci_p2_5; ci_p97_5; repetitions; cluster; seed; development_only
- Data types: comparison:object; metric:object; requested_coverage:float64; estimate_mean:float64; ci_p2_5:float64; ci_p97_5:float64; repetitions:int64; cluster:object; seed:int64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 5
- Unique identifiers: 
- Notes: 

## Step2D_Confidence_Baselines__smoke.csv

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2D/smoke/Step2D_Confidence_Baselines__smoke.csv`
- Dataset role: 05_metrics
- Rows: 6
- Columns: 6
- Column names: system; status; n; candidate_k; selected_source_matches_rank1; platt_raw_rank_equivalent
- Data types: system:object; status:object; n:int64; candidate_k:float64; selected_source_matches_rank1:object; platt_raw_rank_equivalent:object
- Units if known: Not automatically verified
- Date/time column: candidate_k
- Date range: 1970-01-01 00:00:00.000000005 to 1970-01-01 00:00:00.000000005
- Missing values: 11
- Unique identifiers: 
- Notes: 

## Step2D_Fixed_Coverage_Summary__smoke.csv

- Relative path: `05_metrics/02_fixed_coverage_metrics/training_data/results/Step2D/smoke/Step2D_Fixed_Coverage_Summary__smoke.csv`
- Dataset role: 05_metrics
- Rows: 63
- Columns: 11
- Column names: ranking; system; requested_coverage; retained_n; realized_coverage; mean_normalized_regret; mean_raw_regret_mph; near_oracle_failure_rate; top1_error_rate; selective_gain; coverage_boundary_tie
- Data types: ranking:object; system:object; requested_coverage:float64; retained_n:int64; realized_coverage:float64; mean_normalized_regret:float64; mean_raw_regret_mph:float64; near_oracle_failure_rate:float64; top1_error_rate:float64; selective_gain:float64; coverage_boundary_tie:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2D_QC__smoke.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2D/smoke/Step2D_QC__smoke.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 12
- Column names: status; checks; critical_failures; platt_raw_rank_equivalent; platt_raw_aurc_equivalent; input_n; stations; timestamp_first; timestamp_last; test_target_samples; test_split_status; formal_step2d_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2D_Random_Reference__smoke.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2D/smoke/Step2D_Random_Reference__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 4
- Columns: 7
- Column names: system; repetitions; seed; random_aurc_mean; random_aurc_p2_5; random_aurc_p97_5; development_only
- Data types: system:object; repetitions:int64; seed:int64; random_aurc_mean:float64; random_aurc_p2_5:float64; random_aurc_p97_5:float64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2D_Risk_Coverage_Curve__smoke.csv

- Relative path: `05_metrics/03_risk_coverage/training_data/results/Step2D/smoke/Step2D_Risk_Coverage_Curve__smoke.csv`
- Dataset role: 05_metrics
- Rows: 546
- Columns: 8
- Column names: ranking; system; rank_k; coverage; mean_normalized_regret; mean_raw_regret_mph; near_oracle_failure_rate; top1_error_rate
- Data types: ranking:object; system:object; rank_k:int64; coverage:float64; mean_normalized_regret:float64; mean_raw_regret_mph:float64; near_oracle_failure_rate:float64; top1_error_rate:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2D_Runtime__smoke.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2D/smoke/Step2D_Runtime__smoke.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 7
- Column names: total_seconds_excluding_workbook; random_repetitions; bootstrap_repetitions; seed; python; numpy; pandas
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2D_Smoke_Summary.xlsx

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2D/smoke/Step2D_Smoke_Summary.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; AURC:None rows x None columns; FIXED_COVERAGE:None rows x None columns; RC_CURVE:None rows x None columns; CONFIDENCE_BASELINES:None rows x None columns; RANDOM_REFERENCE:None rows x None columns; BOOTSTRAP:None rows x None columns; QC:None rows x None columns; LEAKAGE:None rows x None columns; RUNTIME:None rows x None columns
- Columns: Workbook
- Column names: README; AURC; FIXED_COVERAGE; RC_CURVE; CONFIDENCE_BASELINES; RANDOM_REFERENCE; BOOTSTRAP; QC; LEAKAGE; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## JEV_v1_0_timing_clone__benchmark_models.json

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/production/benchmark_models/JEV_v1_0_timing_clone__benchmark_models.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 13
- Column names: version; freeze_hash; feature_evidence_definitions; normalization; degenerate_features; tau_d; weights; optimizer; software_versions; fitting_timestamp_utc; train_candidate_rows; train_target_times; test_status
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2E_Fitting_Time.csv

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/production/Step2E_Fitting_Time.csv`
- Dataset role: 04_experiment_results
- Rows: 17
- Columns: 6
- Column names: method; repeat; fit_seconds; baseline_rss_bytes; peak_rss_bytes; incremental_peak_rss_bytes
- Data types: method:object; repeat:int64; fit_seconds:float64; baseline_rss_bytes:int64; peak_rss_bytes:int64; incremental_peak_rss_bytes:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Integrity_Audit__production.json

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/production/Step2E_Integrity_Audit__production.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 2
- Column names: status; files
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2E_Memory.csv

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/production/Step2E_Memory.csv`
- Dataset role: 04_experiment_results
- Rows: 204
- Columns: 7
- Column names: method; operation; repeat; baseline_rss_bytes; peak_rss_bytes; incremental_peak_rss_bytes; sampling_interval_ms
- Data types: method:object; operation:object; repeat:int64; baseline_rss_bytes:int64; peak_rss_bytes:int64; incremental_peak_rss_bytes:int64; sampling_interval_ms:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## STEP2E_PRODUCTION_COMPLETE.json

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/production/STEP2E_PRODUCTION_COMPLETE.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 4
- Column names: status; qc; test_target_samples; test_split_status
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2E_QC.json

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/production/Step2E_QC.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 5
- Column names: step; mode; status; checks; full_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2E_Results.xlsx

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/production/Step2E_Results.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; CONFIG:None rows x None columns; ENVIRONMENT:None rows x None columns; FAIRNESS_PROTOCOL:None rows x None columns; METHOD_SUMMARY:None rows x None columns; FITTING_TIME:None rows x None columns; INFERENCE_LATENCY:None rows x None columns; THROUGHPUT:None rows x None columns; MEMORY:None rows x None columns; MODEL_SIZE:None rows x None columns
- Columns: Workbook
- Column names: README; CONFIG; ENVIRONMENT; FAIRNESS_PROTOCOL; METHOD_SUMMARY; FITTING_TIME; INFERENCE_LATENCY; THROUGHPUT; MEMORY; MODEL_SIZE; REGRET_LATENCY; PARETO; QC; INTEGRITY; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2E_Runtime.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2E/production/Step2E_Runtime.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 4
- Column names: status; feature_preparation_seconds_excluded_from_primary_latency; elapsed_seconds_before_workbook; full_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2E_Speedup_Ratios.csv

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/production/Step2E_Speedup_Ratios.csv`
- Dataset role: 04_experiment_results
- Rows: 7
- Columns: 4
- Column names: method; median_latency_ms; latency_ratio_method_over_jev; jev_speedup_vs_method
- Data types: method:object; median_latency_ms:float64; latency_ratio_method_over_jev:float64; jev_speedup_vs_method:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## JEV_v1_0_timing_clone__benchmark_models.json

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/smoke/benchmark_models/JEV_v1_0_timing_clone__benchmark_models.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 13
- Column names: version; freeze_hash; feature_evidence_definitions; normalization; degenerate_features; tau_d; weights; optimizer; software_versions; fitting_timestamp_utc; train_candidate_rows; train_target_times; test_status
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2E_Integrity_Audit__smoke.json

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/smoke/Step2E_Integrity_Audit__smoke.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 9
- Column names: status; test_loaded; scientific_selector_models_changed; selector_hyperparameters_changed; JEV_definition_changed; validation_regret_source; timing_benchmark_does_not_replace_scientific_predictions; raw_data_io_excluded_from_primary_latency; reporting_time_excluded_from_primary_latency
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2E_Smoke_Efficiency_Report.xlsx

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/smoke/Step2E_Smoke_Efficiency_Report.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; CONFIG:None rows x None columns; ENVIRONMENT:None rows x None columns; FAIRNESS_PROTOCOL:None rows x None columns; FITTING_TIME:None rows x None columns; INFERENCE_LATENCY:None rows x None columns; THROUGHPUT:None rows x None columns; MEMORY:None rows x None columns; MODEL_SIZE:None rows x None columns; REGRET_LATENCY:None rows x None columns
- Columns: Workbook
- Column names: README; CONFIG; ENVIRONMENT; FAIRNESS_PROTOCOL; FITTING_TIME; INFERENCE_LATENCY; THROUGHPUT; MEMORY; MODEL_SIZE; REGRET_LATENCY; PARETO_FRONTIER; SPEEDUP_RATIOS; QC; ISSUES
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2E_Smoke_Fitting_Time.csv

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/smoke/Step2E_Smoke_Fitting_Time.csv`
- Dataset role: 04_experiment_results
- Rows: 7
- Columns: 6
- Column names: method; repeat; fit_seconds; baseline_rss_bytes; peak_rss_bytes; incremental_peak_rss_bytes
- Data types: method:object; repeat:int64; fit_seconds:float64; baseline_rss_bytes:int64; peak_rss_bytes:int64; incremental_peak_rss_bytes:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Smoke_Inference_Latency.csv

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2E/smoke/Step2E_Smoke_Inference_Latency.csv`
- Dataset role: 05_metrics
- Rows: 33
- Columns: 8
- Column names: method; timing_view; repeat; execution_order; validation_target_times; total_seconds; latency_ms_per_target; throughput_target_times_per_second
- Data types: method:object; timing_view:object; repeat:int64; execution_order:object; validation_target_times:int64; total_seconds:float64; latency_ms_per_target:float64; throughput_target_times_per_second:float64
- Units if known: Not automatically verified
- Date/time column: validation_target_times; throughput_target_times_per_second
- Date range: 1970-01-01 00:00:00.000000171 to 1970-01-01 00:00:00.000000171
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Smoke_Integrity_Check.json

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/smoke/Step2E_Smoke_Integrity_Check.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 2
- Column names: status; files
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2E_Smoke_Memory.csv

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/smoke/Step2E_Smoke_Memory.csv`
- Dataset role: 04_experiment_results
- Rows: 25
- Columns: 7
- Column names: method; operation; repeat; baseline_rss_bytes; peak_rss_bytes; incremental_peak_rss_bytes; sampling_interval_ms
- Data types: method:object; operation:object; repeat:int64; baseline_rss_bytes:int64; peak_rss_bytes:int64; incremental_peak_rss_bytes:int64; sampling_interval_ms:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Smoke_Memory_Profile.csv

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/smoke/Step2E_Smoke_Memory_Profile.csv`
- Dataset role: 04_experiment_results
- Rows: 25
- Columns: 7
- Column names: method; operation; repeat; baseline_rss_bytes; peak_rss_bytes; incremental_peak_rss_bytes; sampling_interval_ms
- Data types: method:object; operation:object; repeat:int64; baseline_rss_bytes:int64; peak_rss_bytes:int64; incremental_peak_rss_bytes:int64; sampling_interval_ms:int64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Smoke_Pareto_Frontier.csv

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2E/smoke/Step2E_Smoke_Pareto_Frontier.csv`
- Dataset role: 05_metrics
- Rows: 7
- Columns: 5
- Column names: method; validation_samples; mean_normalized_regret; median_latency_ms; pareto_nondominated
- Data types: method:object; validation_samples:int64; mean_normalized_regret:float64; median_latency_ms:float64; pareto_nondominated:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Smoke_QC.json

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/smoke/Step2E_Smoke_QC.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 10
- Column names: step; mode; status; checks; train_target_times; validation_target_times; candidate_k; test_target_samples; test_split_status; full_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2E_Smoke_Regret_Latency_Source_Data.csv

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2E/smoke/Step2E_Smoke_Regret_Latency_Source_Data.csv`
- Dataset role: 05_metrics
- Rows: 7
- Columns: 5
- Column names: method; validation_samples; mean_normalized_regret; median_latency_ms; pareto_nondominated
- Data types: method:object; validation_samples:int64; mean_normalized_regret:float64; median_latency_ms:float64; pareto_nondominated:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Smoke_Regret_Latency_SourceData.csv

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2E/smoke/Step2E_Smoke_Regret_Latency_SourceData.csv`
- Dataset role: 05_metrics
- Rows: 7
- Columns: 10
- Column names: method; validation_samples; mean_normalized_regret; median_latency_ms; p95_latency_ms; throughput; fitting_time_seconds; peak_inference_ram_mb; model_size_kb; pareto_efficient
- Data types: method:object; validation_samples:int64; mean_normalized_regret:float64; median_latency_ms:float64; p95_latency_ms:float64; throughput:float64; fitting_time_seconds:float64; peak_inference_ram_mb:float64; model_size_kb:float64; pareto_efficient:bool
- Units if known: Not automatically verified
- Date/time column: fitting_time_seconds
- Date range: 1970-01-01 00:00:00 to 1970-01-01 00:00:00.000000009
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Smoke_Runtime.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2E/smoke/Step2E_Smoke_Runtime.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 4
- Column names: status; feature_preparation_seconds_excluded_from_primary_latency; elapsed_seconds_before_workbook; full_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2E_Smoke_Speedup_Ratios.csv

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/smoke/Step2E_Smoke_Speedup_Ratios.csv`
- Dataset role: 04_experiment_results
- Rows: 7
- Columns: 4
- Column names: method; median_latency_ms; latency_ratio_method_over_jev; jev_speedup_vs_method
- Data types: method:object; median_latency_ms:float64; latency_ratio_method_over_jev:float64; jev_speedup_vs_method:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2E_Smoke_Summary.xlsx

- Relative path: `04_experiment_results/08_runtime_efficiency/training_data/results/Step2E/smoke/Step2E_Smoke_Summary.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; METHOD_SUMMARY:None rows x None columns; FITTING_TIME:None rows x None columns; INFERENCE_LATENCY:None rows x None columns; THROUGHPUT:None rows x None columns; MEMORY:None rows x None columns; MODEL_SIZE:None rows x None columns; REGRET_LATENCY:None rows x None columns; PARETO:None rows x None columns; QC:None rows x None columns
- Columns: Workbook
- Column names: README; METHOD_SUMMARY; FITTING_TIME; INFERENCE_LATENCY; THROUGHPUT; MEMORY; MODEL_SIZE; REGRET_LATENCY; PARETO; QC; INTEGRITY; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2E_Smoke_Throughput.csv

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2E/smoke/Step2E_Smoke_Throughput.csv`
- Dataset role: 05_metrics
- Rows: 7
- Columns: 3
- Column names: method; mean_throughput; median_throughput
- Data types: method:object; mean_throughput:float64; median_throughput:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## .step2f_gru_candidate_cache__production.csv

- Relative path: `04_experiment_results/01_baselines/training_data/results/Step2F/production/.step2f_gru_candidate_cache__production.csv`
- Dataset role: 04_experiment_results
- Rows: 7155
- Columns: 5
- Column names: sample_id; target_station; candidate_station; target_speed; prediction_GRU
- Data types: sample_id:object; target_station:int64; candidate_station:int64; target_speed:float64; prediction_GRU:float64
- Units if known: Not automatically verified
- Date/time column: candidate_station
- Date range: 1970-01-01 00:00:00.000715938 to 1970-01-01 00:00:00.000777767
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2F_Downstream_Predictions.csv

- Relative path: `09_model_outputs/predictions/training_data/results/Step2F/production/Step2F_Downstream_Predictions.csv`
- Dataset role: 09_model_outputs
- Rows: 11448
- Columns: 16
- Column names: split; target_station; timestamp; sample_id; method; selected_source; actual_target_speed; predicted_target_speed; forecast_error; absolute_error; squared_error; smape_component; oracle_source; oracle_absolute_error; selected_loss; raw_regret_mph
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; method:object; selected_source:int64; actual_target_speed:float64; predicted_target_speed:float64; forecast_error:float64; absolute_error:float64; squared_error:float64; smape_component:float64; oracle_source:int64; oracle_absolute_error:float64; selected_loss:float64; raw_regret_mph:float64
- Units if known: Not automatically verified
- Date/time column: timestamp
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-28 23:55:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2F_Error_Tail_Summary.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2F/production/Step2F_Error_Tail_Summary.csv`
- Dataset role: 04_experiment_results
- Rows: 9
- Columns: 5
- Column names: method; N; median_absolute_error; p90_absolute_error; p95_absolute_error
- Data types: method:object; N:int64; median_absolute_error:float64; p90_absolute_error:float64; p95_absolute_error:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2F_Independent_Evaluator_Sensitivity__production.csv

- Relative path: `04_experiment_results/04_sensitivity/training_data/results/Step2F/production/Step2F_Independent_Evaluator_Sensitivity__production.csv`
- Dataset role: 04_experiment_results
- Rows: 8
- Columns: 8
- Column names: method; N; MAE; RMSE; sMAPE; median_absolute_error; p90_absolute_error; p95_absolute_error
- Data types: method:object; N:int64; MAE:float64; RMSE:float64; sMAPE:float64; median_absolute_error:float64; p90_absolute_error:float64; p95_absolute_error:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2F_Integrity_Audit.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2F/production/Step2F_Integrity_Audit.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 12
- Column names: status; test_loaded; selector_models_refit; JEV_changed; primary_downstream_predictor_refit; downstream_predictor_tuned; selected_sources_changed; primary_metric_predefined; H30_horizon_unchanged; candidate_substitution_protocol_unchanged; primary_evaluation_split; same_denominator
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2F_Method_Summary.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2F/production/Step2F_Method_Summary.csv`
- Dataset role: 04_experiment_results
- Rows: 9
- Columns: 11
- Column names: method; N; MAE; RMSE; sMAPE; median_absolute_error; p90_absolute_error; p95_absolute_error; mae_improvement_vs_nearest_pct; mae_improvement_vs_historical_best_pct; delta_MAE_JEV_minus_method
- Data types: method:object; N:int64; MAE:float64; RMSE:float64; sMAPE:float64; median_absolute_error:float64; p90_absolute_error:float64; p95_absolute_error:float64; mae_improvement_vs_nearest_pct:float64; mae_improvement_vs_historical_best_pct:float64; delta_MAE_JEV_minus_method:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 2
- Unique identifiers: 
- Notes: 

## Step2F_Paired_Development_Comparisons.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2F/production/Step2F_Paired_Development_Comparisons.csv`
- Dataset role: 04_experiment_results
- Rows: 15
- Columns: 10
- Column names: comparison; metric; observed_difference; bootstrap_mean; ci95_lower; ci95_upper; cluster; repetitions; seed; development_only
- Data types: comparison:object; metric:object; observed_difference:float64; bootstrap_mean:float64; ci95_lower:float64; ci95_upper:float64; cluster:object; repetitions:int64; seed:int64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## STEP2F_PRODUCTION_COMPLETE.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2F/production/STEP2F_PRODUCTION_COMPLETE.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 5
- Column names: status; qc; integrity; test_target_samples; test_split_status
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2F_QC.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2F/production/Step2F_QC.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 9
- Column names: step; mode; status; checks; mae_selected_loss_max_abs_difference; mae_minus_oracle_raw_regret_max_abs_difference; test_target_samples; test_split_status; formal_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2F_Results.xlsx

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2F/production/Step2F_Results.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; METHOD_SUMMARY:None rows x None columns; PREDICTIONS_PREVIEW:None rows x None columns; PAIRED_COMPARISONS:None rows x None columns; STATION_SUMMARY:None rows x None columns; ERROR_TAILS:None rows x None columns; DOWNSTREAM_MODEL:None rows x None columns; INDEPENDENT_EVALUATOR:None rows x None columns; QC:None rows x None columns; INTEGRITY:None rows x None columns
- Columns: Workbook
- Column names: README; METHOD_SUMMARY; PREDICTIONS_PREVIEW; PAIRED_COMPARISONS; STATION_SUMMARY; ERROR_TAILS; DOWNSTREAM_MODEL; INDEPENDENT_EVALUATOR; QC; INTEGRITY; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2F_Runtime.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2F/production/Step2F_Runtime.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 6
- Column names: status; elapsed_seconds_before_workbook; prediction_source; independent_gru_predictions_regenerated_from_frozen_model; test_loaded; formal_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2F_Station_Level_Summary.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2F/production/Step2F_Station_Level_Summary.csv`
- Dataset role: 04_experiment_results
- Rows: 1368
- Columns: 9
- Column names: method; target_station; N; MAE; RMSE; sMAPE; median_absolute_error; p90_absolute_error; p95_absolute_error
- Data types: method:object; target_station:int64; N:int64; MAE:float64; RMSE:float64; sMAPE:float64; median_absolute_error:float64; p90_absolute_error:float64; p95_absolute_error:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## .step2f_gru_candidate_cache__smoke.csv

- Relative path: `04_experiment_results/01_baselines/training_data/results/Step2F/smoke/.step2f_gru_candidate_cache__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 855
- Columns: 5
- Column names: sample_id; target_station; candidate_station; target_speed; prediction_GRU
- Data types: sample_id:object; target_station:int64; candidate_station:int64; target_speed:float64; prediction_GRU:float64
- Units if known: Not automatically verified
- Date/time column: candidate_station
- Date range: 1970-01-01 00:00:00.000717951 to 1970-01-01 00:00:00.000776019
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2F_Independent_Evaluator_Sensitivity__smoke.csv

- Relative path: `04_experiment_results/04_sensitivity/training_data/results/Step2F/smoke/Step2F_Independent_Evaluator_Sensitivity__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 8
- Columns: 8
- Column names: method; N; MAE; RMSE; sMAPE; median_absolute_error; p90_absolute_error; p95_absolute_error
- Data types: method:object; N:int64; MAE:float64; RMSE:float64; sMAPE:float64; median_absolute_error:float64; p90_absolute_error:float64; p95_absolute_error:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2F_Smoke_Method_Summary.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2F/smoke/Step2F_Smoke_Method_Summary.csv`
- Dataset role: 04_experiment_results
- Rows: 9
- Columns: 11
- Column names: method; N; MAE; RMSE; sMAPE; median_absolute_error; p90_absolute_error; p95_absolute_error; mae_improvement_vs_nearest_pct; mae_improvement_vs_historical_best_pct; delta_MAE_JEV_minus_method
- Data types: method:object; N:int64; MAE:float64; RMSE:float64; sMAPE:float64; median_absolute_error:float64; p90_absolute_error:float64; p95_absolute_error:float64; mae_improvement_vs_nearest_pct:float64; mae_improvement_vs_historical_best_pct:float64; delta_MAE_JEV_minus_method:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 2
- Unique identifiers: 
- Notes: 

## Step2F_Smoke_Paired_Comparisons.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2F/smoke/Step2F_Smoke_Paired_Comparisons.csv`
- Dataset role: 04_experiment_results
- Rows: 15
- Columns: 10
- Column names: comparison; metric; observed_difference; bootstrap_mean; ci95_lower; ci95_upper; cluster; repetitions; seed; development_only
- Data types: comparison:object; metric:object; observed_difference:float64; bootstrap_mean:float64; ci95_lower:float64; ci95_upper:float64; cluster:object; repetitions:int64; seed:int64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2F_Smoke_Predictions.csv

- Relative path: `09_model_outputs/predictions/training_data/results/Step2F/smoke/Step2F_Smoke_Predictions.csv`
- Dataset role: 09_model_outputs
- Rows: 1368
- Columns: 16
- Column names: split; target_station; timestamp; sample_id; method; selected_source; actual_target_speed; predicted_target_speed; forecast_error; absolute_error; squared_error; smape_component; oracle_source; oracle_absolute_error; selected_loss; raw_regret_mph
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; method:object; selected_source:int64; actual_target_speed:float64; predicted_target_speed:float64; forecast_error:float64; absolute_error:float64; squared_error:float64; smape_component:float64; oracle_source:int64; oracle_absolute_error:float64; selected_loss:float64; raw_regret_mph:float64
- Units if known: Not automatically verified
- Date/time column: timestamp
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-27 23:55:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2F_Smoke_QC.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2F/smoke/Step2F_Smoke_QC.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 9
- Column names: step; mode; status; checks; mae_selected_loss_max_abs_difference; mae_minus_oracle_raw_regret_max_abs_difference; test_target_samples; test_split_status; formal_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2F_Smoke_Runtime.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2F/smoke/Step2F_Smoke_Runtime.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 6
- Column names: status; elapsed_seconds_before_workbook; prediction_source; independent_gru_predictions_regenerated_from_frozen_model; test_loaded; formal_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2F_Smoke_Summary.xlsx

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2F/smoke/Step2F_Smoke_Summary.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; METHOD_SUMMARY:None rows x None columns; PREDICTIONS_PREVIEW:None rows x None columns; PAIRED_COMPARISONS:None rows x None columns; STATION_SUMMARY:None rows x None columns; ERROR_TAILS:None rows x None columns; DOWNSTREAM_MODEL:None rows x None columns; INDEPENDENT_EVALUATOR:None rows x None columns; QC:None rows x None columns; INTEGRITY:None rows x None columns
- Columns: Workbook
- Column names: README; METHOD_SUMMARY; PREDICTIONS_PREVIEW; PAIRED_COMPARISONS; STATION_SUMMARY; ERROR_TAILS; DOWNSTREAM_MODEL; INDEPENDENT_EVALUATOR; QC; INTEGRITY; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2G_Integrity_Audit.json

- Relative path: `04_experiment_results/03_ablation/training_data/results/Step2G/production/Step2G_Integrity_Audit.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 13
- Column names: status; test_loaded; JEV_v1_0_changed; full_JEV_refit; ablation_variants_diagnostic_only; ablation_not_eligible_to_replace_frozen_JEV; selection_ablation_fit_split; selection_ablation_eval_split; confidence_ablation_source; Platt_refit; downstream_models_refit; candidate_pool_changed; metric_definition_changed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## STEP2G_PRODUCTION_COMPLETE.json

- Relative path: `04_experiment_results/03_ablation/training_data/results/Step2G/production/STEP2G_PRODUCTION_COMPLETE.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 5
- Column names: status; qc; integrity; test_target_samples; test_split_status
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2G_QC.json

- Relative path: `04_experiment_results/03_ablation/training_data/results/Step2G/production/Step2G_QC.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 12
- Column names: step; mode; status; selection_checks; confidence_checks; train_target_times; validation_target_times; candidate_k; minus_q_q_tiebreak_count; test_target_samples; test_split_status; formal_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2G_Results.xlsx

- Relative path: `04_experiment_results/03_ablation/training_data/results/Step2G/production/Step2G_Results.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; SELECTION_SUMMARY:None rows x None columns; ABLATION_WEIGHTS:None rows x None columns; PREDICTIONS_PREVIEW:None rows x None columns; STATION_SUMMARY:None rows x None columns; PAIRED_COMPARISONS:None rows x None columns; CONFIDENCE_ABLATION:None rows x None columns; CONFIDENCE_PROVENANCE:None rows x None columns; QC:None rows x None columns; INTEGRITY:None rows x None columns
- Columns: Workbook
- Column names: README; SELECTION_SUMMARY; ABLATION_WEIGHTS; PREDICTIONS_PREVIEW; STATION_SUMMARY; PAIRED_COMPARISONS; CONFIDENCE_ABLATION; CONFIDENCE_PROVENANCE; QC; INTEGRITY; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2G_Runtime.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2G/production/Step2G_Runtime.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 6
- Column names: status; elapsed_seconds_before_workbook; selection_bootstrap_repetitions; bootstrap_cluster; test_loaded; formal_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2G_Selection_Ablation_Predictions__production.csv

- Relative path: `09_model_outputs/predictions/training_data/results/Step2G/production/Step2G_Selection_Ablation_Predictions__production.csv`
- Dataset role: 09_model_outputs
- Rows: 10017
- Columns: 16
- Column names: split; target_station; timestamp; sample_id; variant; selected_source; oracle_source; selected_loss; oracle_loss; worst_loss; raw_regret_mph; normalized_regret; exact_top1_hit; top2_hit; near_oracle_hit_0p5; ablation_score
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; variant:object; selected_source:int64; oracle_source:int64; selected_loss:float64; oracle_loss:float64; worst_loss:float64; raw_regret_mph:float64; normalized_regret:float64; exact_top1_hit:bool; top2_hit:bool; near_oracle_hit_0p5:bool; ablation_score:float64
- Units if known: Not automatically verified
- Date/time column: timestamp
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-28 23:55:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2G_Ablation_Weights__smoke.csv

- Relative path: `09_model_outputs/model_summaries/training_data/results/Step2G/smoke/Step2G_Ablation_Weights__smoke.csv`
- Dataset role: 09_model_outputs
- Rows: 7
- Columns: 12
- Column names: variant; components; fit_type; optimizer_success; objective; iterations; weight_Q; weight_S; weight_D; weight_C; optimizer_status; optimizer_message
- Data types: variant:object; components:object; fit_type:object; optimizer_success:bool; objective:float64; iterations:int64; weight_Q:float64; weight_S:float64; weight_D:float64; weight_C:float64; optimizer_status:float64; optimizer_message:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 5
- Unique identifiers: 
- Notes: 

## Step2G_Paired_Development_Comparisons__smoke.csv

- Relative path: `04_experiment_results/03_ablation/training_data/results/Step2G/smoke/Step2G_Paired_Development_Comparisons__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 12
- Columns: 10
- Column names: comparison; metric; observed_difference; bootstrap_mean; ci95_lower; ci95_upper; repetitions; cluster; seed; development_only
- Data types: comparison:object; metric:object; observed_difference:float64; bootstrap_mean:float64; ci95_lower:float64; ci95_upper:float64; repetitions:int64; cluster:object; seed:int64; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2G_Selection_Ablation_Predictions__smoke.csv

- Relative path: `09_model_outputs/predictions/training_data/results/Step2G/smoke/Step2G_Selection_Ablation_Predictions__smoke.csv`
- Dataset role: 09_model_outputs
- Rows: 1197
- Columns: 16
- Column names: split; target_station; timestamp; sample_id; variant; selected_source; oracle_source; selected_loss; oracle_loss; worst_loss; raw_regret_mph; normalized_regret; exact_top1_hit; top2_hit; near_oracle_hit_0p5; ablation_score
- Data types: split:object; target_station:int64; timestamp:object; sample_id:object; variant:object; selected_source:int64; oracle_source:int64; selected_loss:float64; oracle_loss:float64; worst_loss:float64; raw_regret_mph:float64; normalized_regret:float64; exact_top1_hit:bool; top2_hit:bool; near_oracle_hit_0p5:bool; ablation_score:float64
- Units if known: Not automatically verified
- Date/time column: timestamp
- Date range: 2026-06-02 23:30:00-07:00 to 2026-06-27 23:55:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2G_Selection_Ablation_Summary__smoke.csv

- Relative path: `09_model_outputs/selections/training_data/results/Step2G/smoke/Step2G_Selection_Ablation_Summary__smoke.csv`
- Dataset role: 09_model_outputs
- Rows: 7
- Columns: 12
- Column names: variant; N; mean_normalized_regret; median_normalized_regret; mean_raw_regret_mph; median_raw_regret_mph; exact_top1_accuracy; top2_hit_rate; near_oracle_hit_rate_0p5; development_smoke_only; delta_nr_vs_full; relative_degradation_pct
- Data types: variant:object; N:int64; mean_normalized_regret:float64; median_normalized_regret:float64; mean_raw_regret_mph:float64; median_raw_regret_mph:float64; exact_top1_accuracy:float64; top2_hit_rate:float64; near_oracle_hit_rate_0p5:float64; development_smoke_only:bool; delta_nr_vs_full:float64; relative_degradation_pct:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2G_Smoke_QC.json

- Relative path: `04_experiment_results/03_ablation/training_data/results/Step2G/smoke/Step2G_Smoke_QC.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 12
- Column names: step; mode; status; selection_checks; confidence_checks; train_target_times; validation_target_times; candidate_k; minus_q_q_tiebreak_count; test_target_samples; test_split_status; formal_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2G_Smoke_Runtime.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2G/smoke/Step2G_Smoke_Runtime.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 6
- Column names: status; elapsed_seconds_before_workbook; selection_bootstrap_repetitions; bootstrap_cluster; test_loaded; formal_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2G_Smoke_Summary.xlsx

- Relative path: `04_experiment_results/03_ablation/training_data/results/Step2G/smoke/Step2G_Smoke_Summary.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; SELECTION_SUMMARY:None rows x None columns; ABLATION_WEIGHTS:None rows x None columns; PREDICTIONS_PREVIEW:None rows x None columns; STATION_SUMMARY:None rows x None columns; PAIRED_COMPARISONS:None rows x None columns; CONFIDENCE_ABLATION:None rows x None columns; CONFIDENCE_PROVENANCE:None rows x None columns; QC:None rows x None columns; INTEGRITY:None rows x None columns
- Columns: Workbook
- Column names: README; SELECTION_SUMMARY; ABLATION_WEIGHTS; PREDICTIONS_PREVIEW; STATION_SUMMARY; PAIRED_COMPARISONS; CONFIDENCE_ABLATION; CONFIDENCE_PROVENANCE; QC; INTEGRITY; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2G_Station_Level_Ablation__smoke.csv

- Relative path: `04_experiment_results/03_ablation/training_data/results/Step2G/smoke/Step2G_Station_Level_Ablation__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 35
- Columns: 6
- Column names: variant; target_station; N; mean_normalized_regret; near_oracle_hit_rate_0p5; exact_top1_accuracy
- Data types: variant:object; target_station:int64; N:int64; mean_normalized_regret:float64; near_oracle_hit_rate_0p5:float64; exact_top1_accuracy:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2H_Bootstrap_Comparisons__production.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/production/Step2H_Bootstrap_Comparisons__production.csv`
- Dataset role: 04_experiment_results
- Rows: 126
- Columns: 13
- Column names: boundary_dimension; stratum; baseline; N; unique_stations; DeltaNR_JEV_minus_baseline; bootstrap_status; ci95_lower; ci95_upper; bootstrap_mean; repetitions; cluster; development_only
- Data types: boundary_dimension:object; stratum:object; baseline:object; N:int64; unique_stations:int64; DeltaNR_JEV_minus_baseline:float64; bootstrap_status:object; ci95_lower:float64; ci95_upper:float64; bootstrap_mean:float64; repetitions:int64; cluster:object; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2H_Boundary_Thresholds__production.csv

- Relative path: `04_experiment_results/05_robustness/training_data/results/Step2H/production/Step2H_Boundary_Thresholds__production.csv`
- Dataset role: 04_experiment_results
- Rows: 6
- Columns: 7
- Column names: boundary_dimension; variable; fit_split; p33_333; p66_667; labels; engineering_smoke_only
- Data types: boundary_dimension:object; variable:object; fit_split:object; p33_333:float64; p66_667:float64; labels:object; engineering_smoke_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 1
- Unique identifiers: 
- Notes: 

## Step2H_Context_Correlations__production.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/production/Step2H_Context_Correlations__production.csv`
- Dataset role: 04_experiment_results
- Rows: 5
- Columns: 5
- Column names: context_variable; N; spearman_rho; p_value_descriptive_only; use
- Data types: context_variable:object; N:int64; spearman_rho:float64; p_value_descriptive_only:float64; use:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2H_Evaluator_Sensitivity__production.csv

- Relative path: `04_experiment_results/04_sensitivity/training_data/results/Step2H/production/Step2H_Evaluator_Sensitivity__production.csv`
- Dataset role: 04_experiment_results
- Rows: 105
- Columns: 11
- Column names: boundary_dimension; stratum; baseline; N; unique_stations; DeltaMAE_XGBEvaluator; DeltaMAE_GRUEvaluator; direction_XGB; direction_GRU; direction_consistent; evaluator_sensitive
- Data types: boundary_dimension:object; stratum:object; baseline:object; N:int64; unique_stations:int64; DeltaMAE_XGBEvaluator:float64; DeltaMAE_GRUEvaluator:float64; direction_XGB:object; direction_GRU:object; direction_consistent:bool; evaluator_sensitive:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2H_Failure_Profile__production.csv

- Relative path: `04_experiment_results/05_robustness/training_data/results/Step2H/production/Step2H_Failure_Profile__production.csv`
- Dataset role: 04_experiment_results
- Rows: 5
- Columns: 11
- Column names: profile; N; station_count; near_tie_rate; high_spread_rate; low_quality_rate; high_quality_heterogeneity_rate; high_volatility_rate; far_distance_rate; peak_rate; weekend_rate
- Data types: profile:object; N:int64; station_count:int64; near_tie_rate:float64; high_spread_rate:float64; low_quality_rate:float64; high_quality_heterogeneity_rate:float64; high_volatility_rate:float64; far_distance_rate:float64; peak_rate:float64; weekend_rate:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2H_HighConfidence_Failures__production.csv

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2H/production/Step2H_HighConfidence_Failures__production.csv`
- Dataset role: 05_metrics
- Rows: 160
- Columns: 16
- Column names: sample_id; target_station; timestamp; predicted_probability; normalized_regret; severe_failure; high_confidence_severe_failure; SPREAD; QUALITY_LEVEL; QUALITY_HETEROGENEITY; VOLATILITY; DISTANCE; TIE_SEPARATION; PEAK_OFFPEAK; PEAK_DETAIL; WEEKDAY_WEEKEND
- Data types: sample_id:object; target_station:int64; timestamp:object; predicted_probability:float64; normalized_regret:float64; severe_failure:bool; high_confidence_severe_failure:bool; SPREAD:object; QUALITY_LEVEL:object; QUALITY_HETEROGENEITY:object; VOLATILITY:object; DISTANCE:object; TIE_SEPARATION:object; PEAK_OFFPEAK:object; PEAK_DETAIL:object; WEEKDAY_WEEKEND:object
- Units if known: Not automatically verified
- Date/time column: timestamp
- Date range: 2026-06-15 23:30:00-07:00 to 2026-06-28 23:55:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2H_Integrity_Audit.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/production/Step2H_Integrity_Audit.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 13
- Column names: status; test_loaded; JEV_changed; baseline_models_refit; Platt_refit; downstream_evaluators_rerun; context_threshold_fit_split; validation_outcomes_used_for_threshold_definition; high_confidence_threshold_source; high_confidence_failure_eval_split; difficulty_variables_used_as_selector_features; boundary_analysis_is_explanatory_only; no_posthoc_stratum_merging
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## STEP2H_PRODUCTION_COMPLETE.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/production/STEP2H_PRODUCTION_COMPLETE.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 5
- Column names: status; qc; integrity; test_target_samples; test_split_status
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2H_QC.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/production/Step2H_QC.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 12
- Column names: step; mode; status; checks; train_target_times; validation_target_times; cal_eval_target_times; primary_targets; candidate_k; test_target_samples; test_split_status; formal_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2H_Results.xlsx

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/production/Step2H_Results.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; THRESHOLDS:None rows x None columns; STRATIFIED_PERFORMANCE:None rows x None columns; DELTA_NR:None rows x None columns; FAILURE_PROFILE:None rows x None columns; HIGH_CONF_FAILURE:None rows x None columns; EVALUATOR_SENSITIVITY:None rows x None columns; BOOTSTRAP:None rows x None columns; CORRELATIONS:None rows x None columns; QC:None rows x None columns
- Columns: Workbook
- Column names: README; THRESHOLDS; STRATIFIED_PERFORMANCE; DELTA_NR; FAILURE_PROFILE; HIGH_CONF_FAILURE; EVALUATOR_SENSITIVITY; BOOTSTRAP; CORRELATIONS; QC; INTEGRITY; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2H_Results.xlsx.bounds.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/production/Step2H_Results.xlsx.bounds.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 12
- Column names: README; THRESHOLDS; STRATIFIED_PERFORMANCE; DELTA_NR; FAILURE_PROFILE; HIGH_CONF_FAILURE; EVALUATOR_SENSITIVITY; BOOTSTRAP; CORRELATIONS; QC; INTEGRITY; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2H_Runtime.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2H/production/Step2H_Runtime.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 7
- Column names: status; elapsed_seconds_before_workbook; bootstrap_repetitions; bootstrap_cluster; eligible_bootstrap_comparisons; test_loaded; formal_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2H_Stratified_DeltaNR__production.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/production/Step2H_Stratified_DeltaNR__production.csv`
- Dataset role: 04_experiment_results
- Rows: 138
- Columns: 13
- Column names: boundary_dimension; stratum; baseline; N; unique_stations; DeltaNR_JEV_minus_baseline; bootstrap_status; ci95_lower; ci95_upper; bootstrap_mean; repetitions; cluster; development_only
- Data types: boundary_dimension:object; stratum:object; baseline:object; N:int64; unique_stations:int64; DeltaNR_JEV_minus_baseline:float64; bootstrap_status:object; ci95_lower:float64; ci95_upper:float64; bootstrap_mean:float64; repetitions:int64; cluster:object; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 48
- Unique identifiers: 
- Notes: 

## Step2H_Stratified_Performance__production.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/production/Step2H_Stratified_Performance__production.csv`
- Dataset role: 04_experiment_results
- Rows: 23
- Columns: 19
- Column names: boundary_dimension; stratum; N; unique_stations; descriptive_status; JEV_mean_NR; QualityRule_mean_NR; XGBoost_mean_NR; GRU_mean_NR; Nearest_mean_NR; HistoricalBest_mean_NR; Ridge_mean_NR; Delta_JEV_vs_Quality; Delta_JEV_vs_XGB; Delta_JEV_vs_GRU; JEV_mean_raw_regret_mph; JEV_near_oracle_rate; JEV_top1_rate; JEV_severe_failure_rate
- Data types: boundary_dimension:object; stratum:object; N:int64; unique_stations:int64; descriptive_status:object; JEV_mean_NR:float64; QualityRule_mean_NR:float64; XGBoost_mean_NR:float64; GRU_mean_NR:float64; Nearest_mean_NR:float64; HistoricalBest_mean_NR:float64; Ridge_mean_NR:float64; Delta_JEV_vs_Quality:float64; Delta_JEV_vs_XGB:float64; Delta_JEV_vs_GRU:float64; JEV_mean_raw_regret_mph:float64; JEV_near_oracle_rate:float64; JEV_top1_rate:float64; JEV_severe_failure_rate:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 28
- Unique identifiers: 
- Notes: 

## Step2H_Bootstrap_Comparisons__smoke.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/smoke/Step2H_Bootstrap_Comparisons__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 0
- Columns: 13
- Column names: boundary_dimension; stratum; baseline; N; unique_stations; DeltaNR_JEV_minus_baseline; bootstrap_status; ci95_lower; ci95_upper; bootstrap_mean; repetitions; cluster; development_only
- Data types: boundary_dimension:object; stratum:object; baseline:object; N:object; unique_stations:object; DeltaNR_JEV_minus_baseline:object; bootstrap_status:object; ci95_lower:object; ci95_upper:object; bootstrap_mean:object; repetitions:object; cluster:object; development_only:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2H_Boundary_Thresholds__smoke.csv

- Relative path: `04_experiment_results/05_robustness/training_data/results/Step2H/smoke/Step2H_Boundary_Thresholds__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 6
- Columns: 7
- Column names: boundary_dimension; variable; fit_split; p33_333; p66_667; labels; engineering_smoke_only
- Data types: boundary_dimension:object; variable:object; fit_split:object; p33_333:float64; p66_667:float64; labels:object; engineering_smoke_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 1
- Unique identifiers: 
- Notes: 

## Step2H_Context_Correlations__smoke.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/smoke/Step2H_Context_Correlations__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 5
- Columns: 5
- Column names: context_variable; N; spearman_rho; p_value_descriptive_only; use
- Data types: context_variable:object; N:int64; spearman_rho:float64; p_value_descriptive_only:float64; use:object
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2H_Evaluator_Sensitivity__smoke.csv

- Relative path: `04_experiment_results/04_sensitivity/training_data/results/Step2H/smoke/Step2H_Evaluator_Sensitivity__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 95
- Columns: 11
- Column names: boundary_dimension; stratum; baseline; N; unique_stations; DeltaMAE_XGBEvaluator; DeltaMAE_GRUEvaluator; direction_XGB; direction_GRU; direction_consistent; evaluator_sensitive
- Data types: boundary_dimension:object; stratum:object; baseline:object; N:int64; unique_stations:int64; DeltaMAE_XGBEvaluator:float64; DeltaMAE_GRUEvaluator:float64; direction_XGB:object; direction_GRU:object; direction_consistent:bool; evaluator_sensitive:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2H_Failure_Profile__smoke.csv

- Relative path: `04_experiment_results/05_robustness/training_data/results/Step2H/smoke/Step2H_Failure_Profile__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 5
- Columns: 11
- Column names: profile; N; station_count; near_tie_rate; high_spread_rate; low_quality_rate; high_quality_heterogeneity_rate; high_volatility_rate; far_distance_rate; peak_rate; weekend_rate
- Data types: profile:object; N:int64; station_count:int64; near_tie_rate:float64; high_spread_rate:float64; low_quality_rate:float64; high_quality_heterogeneity_rate:float64; high_volatility_rate:float64; far_distance_rate:float64; peak_rate:float64; weekend_rate:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2H_HighConfidence_Failures__smoke.csv

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2H/smoke/Step2H_HighConfidence_Failures__smoke.csv`
- Dataset role: 05_metrics
- Rows: 13
- Columns: 16
- Column names: sample_id; target_station; timestamp; predicted_probability; normalized_regret; severe_failure; high_confidence_severe_failure; SPREAD; QUALITY_LEVEL; QUALITY_HETEROGENEITY; VOLATILITY; DISTANCE; TIE_SEPARATION; PEAK_OFFPEAK; PEAK_DETAIL; WEEKDAY_WEEKEND
- Data types: sample_id:object; target_station:int64; timestamp:object; predicted_probability:float64; normalized_regret:float64; severe_failure:bool; high_confidence_severe_failure:bool; SPREAD:object; QUALITY_LEVEL:object; QUALITY_HETEROGENEITY:object; VOLATILITY:object; DISTANCE:object; TIE_SEPARATION:object; PEAK_OFFPEAK:object; PEAK_DETAIL:object; WEEKDAY_WEEKEND:object
- Units if known: Not automatically verified
- Date/time column: timestamp
- Date range: 2026-06-17 11:15:00-07:00 to 2026-06-26 23:45:00-07:00
- Missing values: 0
- Unique identifiers: 
- Notes: 

## Step2H_Smoke_QC.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/smoke/Step2H_Smoke_QC.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 12
- Column names: step; mode; status; checks; train_target_times; validation_target_times; cal_eval_target_times; primary_targets; candidate_k; test_target_samples; test_split_status; formal_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2H_Smoke_Runtime.json

- Relative path: `05_metrics/01_overall_metrics/training_data/results/Step2H/smoke/Step2H_Smoke_Runtime.json`
- Dataset role: 05_metrics
- Rows: JSON object
- Columns: 7
- Column names: status; elapsed_seconds_before_workbook; bootstrap_repetitions; bootstrap_cluster; eligible_bootstrap_comparisons; test_loaded; formal_production_executed
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2H_Smoke_Summary.xlsx

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/smoke/Step2H_Smoke_Summary.xlsx`
- Dataset role: 04_experiment_results
- Rows: README:None rows x None columns; THRESHOLDS:None rows x None columns; STRATIFIED_PERFORMANCE:None rows x None columns; DELTA_NR:None rows x None columns; FAILURE_PROFILE:None rows x None columns; HIGH_CONF_FAILURE:None rows x None columns; EVALUATOR_SENSITIVITY:None rows x None columns; BOOTSTRAP:None rows x None columns; CORRELATIONS:None rows x None columns; QC:None rows x None columns
- Columns: Workbook
- Column names: README; THRESHOLDS; STRATIFIED_PERFORMANCE; DELTA_NR; FAILURE_PROFILE; HIGH_CONF_FAILURE; EVALUATOR_SENSITIVITY; BOOTSTRAP; CORRELATIONS; QC; INTEGRITY; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.

## Step2H_Smoke_Summary.xlsx.bounds.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/smoke/Step2H_Smoke_Summary.xlsx.bounds.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 12
- Column names: README; THRESHOLDS; STRATIFIED_PERFORMANCE; DELTA_NR; FAILURE_PROFILE; HIGH_CONF_FAILURE; EVALUATOR_SENSITIVITY; BOOTSTRAP; CORRELATIONS; QC; INTEGRITY; RUNTIME
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## Step2H_Stratified_DeltaNR__smoke.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/smoke/Step2H_Stratified_DeltaNR__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 126
- Columns: 13
- Column names: boundary_dimension; stratum; baseline; N; unique_stations; DeltaNR_JEV_minus_baseline; bootstrap_status; ci95_lower; ci95_upper; bootstrap_mean; repetitions; cluster; development_only
- Data types: boundary_dimension:object; stratum:object; baseline:object; N:int64; unique_stations:int64; DeltaNR_JEV_minus_baseline:float64; bootstrap_status:object; ci95_lower:float64; ci95_upper:float64; bootstrap_mean:float64; repetitions:int64; cluster:object; development_only:bool
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 390
- Unique identifiers: 
- Notes: 

## Step2H_Stratified_Performance__smoke.csv

- Relative path: `04_experiment_results/02_JEV/training_data/results/Step2H/smoke/Step2H_Stratified_Performance__smoke.csv`
- Dataset role: 04_experiment_results
- Rows: 21
- Columns: 19
- Column names: boundary_dimension; stratum; N; unique_stations; descriptive_status; JEV_mean_NR; QualityRule_mean_NR; XGBoost_mean_NR; GRU_mean_NR; Nearest_mean_NR; HistoricalBest_mean_NR; Ridge_mean_NR; Delta_JEV_vs_Quality; Delta_JEV_vs_XGB; Delta_JEV_vs_GRU; JEV_mean_raw_regret_mph; JEV_near_oracle_rate; JEV_top1_rate; JEV_severe_failure_rate
- Data types: boundary_dimension:object; stratum:object; N:int64; unique_stations:int64; descriptive_status:object; JEV_mean_NR:float64; QualityRule_mean_NR:float64; XGBoost_mean_NR:float64; GRU_mean_NR:float64; Nearest_mean_NR:float64; HistoricalBest_mean_NR:float64; Ridge_mean_NR:float64; Delta_JEV_vs_Quality:float64; Delta_JEV_vs_XGB:float64; Delta_JEV_vs_GRU:float64; JEV_mean_raw_regret_mph:float64; JEV_near_oracle_rate:float64; JEV_top1_rate:float64; JEV_severe_failure_rate:float64
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 28
- Unique identifiers: 
- Notes: 

## Final_Results_Archive_Status.json

- Relative path: `04_experiment_results/02_JEV/training_data/results/最终结果/00_README_AND_INDEX/Final_Results_Archive_Status.json`
- Dataset role: 04_experiment_results
- Rows: JSON object
- Columns: 9
- Column names: archive_status; Stats Freeze; Final Test; technical_recovery_provenance; test_open_count; scientific_rerun; stats_freeze_changed; scientific_outputs_changed; updated_utc
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: JSON inspected in read-only mode.

## JEV_Paper_Tables_and_TableData_FINAL_20260927.xlsx

- Relative path: `08_table_data/Supplementary_Tables/processed_data/表数据/JEV_Paper_Tables_and_TableData_FINAL_20260927.xlsx`
- Dataset role: 08_table_data
- Rows: README:None rows x None columns; Table1_Protocol:None rows x None columns; Table2_FinalTest:None rows x None columns; Table3_Confidence:None rows x None columns; Source_Fig4a_Exact:None rows x None columns; Supp_Boundary_Failure:None rows x None columns; Supp_Downstream:None rows x None columns; Evidence_Register:None rows x None columns
- Columns: Workbook
- Column names: README; Table1_Protocol; Table2_FinalTest; Table3_Confidence; Source_Fig4a_Exact; Supp_Boundary_Failure; Supp_Downstream; Evidence_Register
- Data types: 
- Units if known: Not automatically verified
- Date/time column: 
- Date range: 
- Missing values: 
- Unique identifiers: 
- Notes: Workbook metadata inspected in read-only mode.
