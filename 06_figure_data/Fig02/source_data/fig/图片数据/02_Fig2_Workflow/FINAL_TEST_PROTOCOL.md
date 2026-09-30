# Final one-shot Test protocol

Status: **FROZEN BEFORE TEST ACCESS**.

Do not run until the Stats Freeze is independently reviewed and the exact authorization `FINAL ONE-SHOT TEST — EXECUTE` is provided.

- Frozen station universe: 171; station 777316 is audit-only.
- Candidate K: 5. Selectors: Nearest, Historical Best, Quality Rule, Ridge, XGBoost, GRU, JEV v1.0.
- No selector refit on Validation. Final Platt parameters alone were refit on all 1,431 frozen Validation observations.
- FINAL_BASE_RATE: 0.41928721174004191. Validation raw-confidence Q75: 0.031266923959426346.
- Three separate Holm FWER .05 families: PRIMARY P1-P4, CONFIDENCE C1-C3, BOUNDARY_REPLICATION B1-B4.
- Inference clusters on target_station; 10,000 bootstrap/permutation/random-ranking replicates; seed 20260924.
- Test is opened once. The script atomically creates FINAL_TEST_OPENED.json immediately before the first Test-row read.
- After opening, scientific logic and frozen hashes cannot change. A technical rerun requires identical hashes and explicit TECHNICAL_RERUN_ONLY handling.
