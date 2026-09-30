# JEV v1.0 Method Specification

Version: 1.0  
Formal definition date: 2026-09-23  
Status before execution: `FORMALLY_DEFINED_NOT_YET_EXECUTED`

JEV v1.0 is a lightweight, interpretable source selector. It uses only causal candidate information available at decision time `t` or earlier. It is not a forecasting model and contains no XGBoost, GRU, MLP, attention, Transformer, ensemble, station-ID embedding, or learned confidence head.

## Frozen evidence components

All robust scalers use finite Train candidate rows only. For feature `x`, save `p05` and `p95` and define `r(x)=clip((x-p05)/(p95-p05),0,1)`. If `p95<=p05`, define `r(x)=0.5` and record the degenerate feature.

- Quality: `Q=(r(recent_observed_mean_60)+r(recent_observed_min_60)+(1-r(recent_missing_count_60))+r(train_candidate_observed_mean))/4`.
- Stability: `S=1-(r(speed_std_60)+r(speed_range_60)+r(abs(speed_slope_60))+r(abs(speed_delta_15))+r(abs(speed_delta_30)))/5`.
- Spatial relevance: `tau_d=median(abs_postmile_distance)` over Train candidate rows, requiring `tau_d>0`; `D=exp(-abs_postmile_distance/tau_d)`.
- Context consistency: with `epsilon=1e-6`, `z=abs(speed_lag00-speed_mean_60)/(speed_std_60+epsilon)`, `z_clipped=clip(z,0,10)`, and `C=exp(-z_clipped)`.

`Q`, `S`, and the final score are clipped to `[0,1]`. `D` is in `(0,1]`; `C` is in `[exp(-10),1]`.

## Train label and fitting

For each Train target-time, let `best=min(loss)`, `worst=max(loss)`, and `spread=worst-best`. When `spread>0`, relative utility is `U=1-(loss-best)/spread`; when `spread=0`, all candidates receive `U=1` and the sample is marked `all_candidate_tie=true`.

The four evidence weights are fitted by deterministic SLSQP from `[0.25,0.25,0.25,0.25]`, minimizing mean squared error between `U` and the additive score:

`JEV_score = w_Q*Q + w_S*S + w_D*D + w_C*C`

subject to `w_k>=0` and `sum(w)=1`. No Validation loss is used for fitting or tuning.

## Selection and raw confidence

Select the candidate with maximum score. Ties are resolved by larger `Q`, then smaller absolute postmile distance, then smaller deterministic candidate-station identifier. Candidate ranks follow the same ordering.

Let `score_1` and `score_2` be the top two scores and let `Q_selected` be the selected candidate's `Q`. Define `margin=score_1-score_2` and `JEV_raw_confidence=margin*Q_selected`. This value is uncalibrated. JEV v1.0 has no sigmoid, gamma, abstention threshold, or risk-coverage calibration.

## Immutability

After first smoke execution, the evidence components, formulas, robust-scaling percentiles, `tau_d` definition, relative-utility equation, fitting objective, optimizer, selection/tie-break rule, and confidence equation must not change in v1.0 because of observed performance. A code bug may be patched only with a versioned implementation audit. A methodological change requires a later version.

Test remains sealed and held out. Step 2B-J1 smoke results are development diagnostics only.
