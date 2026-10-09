# 3. Methodology and 4. Experimental Setup

> Draft v0.1, English. Sources: `05_methodology/{methodology,dataset,baseline,evaluation_metrics}.md`, `06_experiment_results/experimental_setup.md` [ES], code in `code/f2d/`. Tag conventions: `paper_outline.md`. Remove tags before submission.

## 3. Methodology

### 3.1 Design of the benchmark

This study does not propose a new forecasting model. It is a forecast-to-decision benchmark: eight probabilistic forecasting methods supply quantile forecasts to one common decision layer (replenishment plus liquidation), which is run in a multi-period inventory simulation on two public retail datasets. All methods share the same weekly panel, forecast origins, retraining cut-offs, decision rules and scenarios, so that differences in inventory outcomes can be attributed to the forecasts alone.

The pipeline has six steps (Fig. X — to be drawn from `04_proposed_system/diagrams/architecture.mmd`):

1. Build a weekly panel from the raw data.
2. Assign each series to an ADI–CV² demand class.
3. Build features.
4. Forecast quantiles of cumulative demand over the replenishment horizon and the liquidation horizon.
5. Turn the quantiles into order and liquidation decisions.
6. Simulate inventory under lost sales and compute key performance indicators (KPIs) by demand class.

Neither dataset contains inventory positions, lead times or unit costs. We therefore treat the lead time, target service level and liquidation parameters as **scenarios** rather than assumptions about reality. We also report only inventory KPIs that carry no monetary unit, plus a break-even salvage ratio that does not require choosing a single cost value (Section 3.6).

### 3.2 Data and demand classes

**M5** (Makridakis et al., 2022a) contains daily unit sales of 3,049 Walmart products in 10 stores in three US states, at 30,490 product–store series [P01 p. 6]. We aggregate daily sales to Walmart weeks and drop the last, incomplete week, which leaves 277 full weeks (2011-01-29 to 2016-05-14). Weekly prices come from the competition price file; missing prices are carried forward. A series starts in the first week in which the product has a price, i.e. is on the shelf. Weeks before that are treated as missing, not as zero demand. Calendar features are the number of events and the number of SNAP days of the store's state in each week.

**VN1** (Vandeput, 2024) is a weekly e-commerce dataset with 15,053 client × warehouse × product series, used in prior work for accuracy benchmarking (Zanotti, 2025) [P08 p. 7]. It covers 46 vendors and 328 warehouses [DP]. We concatenate Phase 0, Phase 1 and the official Phase 2 answers into 196 weeks (2020-07-06 to 2024-04-01). Prices exist only in Phase 0–1 and only in weeks with sales (29.3% of cells) [DP]; they are carried forward. A series starts at its first sale. Despite its name, VN1 is **not** Vietnamese data.

A series is evaluated if it starts at least 13 weeks before the test period and has at least one sale in the training period. Demand classes are computed on the pre-test history of each series, from its start week, using the thresholds ADI = 4/3 and CV² = 0.5 (Syntetos et al., 2005; thresholds as reported in Makridakis et al., 2022a [P01 p. 7–8]). Following Damato et al. (2026) [P12 p. 10], we use these thresholds as a conventional way to group series, not as a definition of intermittency.

**Table 1.** Datasets used in the benchmark.

| | M5 | VN1 |
|---|---|---|
| Setting | One retailer, 10 physical stores (US) | Multi-vendor e-commerce, 46 vendors, 328 warehouses |
| Series level | product × store | client × warehouse × product |
| Series in panel / evaluated | 30,490 / 30,381 | 15,053 / 13,844 |
| Weeks | 277 | 196 |
| Share of zero weeks | 39.7% | 69.9% |
| Exogenous information | price, events, SNAP, product hierarchy | price (partial) |
| Test window (main) | 2015-11-21 → 2016-05-14 | 2023-10-09 → 2024-04-01 |
| Smooth / erratic / intermittent / lumpy | 16,102 / 1,777 / 10,285 / 2,217 | 2,596 / 1,901 / 6,539 / 2,808 |
| Same, % | 53.0 / 5.8 / 33.9 / 7.3 | 18.8 / 13.7 / 47.2 / 20.3 |

Sources: `05_methodology/dataset.md` §1, §4; [ES §2]; [DP].

The two datasets differ clearly in class composition: M5 is mostly smooth, VN1 mostly intermittent and lumpy. This difference lets us check whether class-level conclusions transfer between retail settings (RQ2). 109 M5 series and 1,209 VN1 series were excluded by the start-date and history conditions.

### 3.3 Forecasting target

Let y_{i,t} be the sales of series i in week t, used as demand. Censoring caused by real stockouts cannot be detected (Section 4.7). At each origin o (the decision week), a forecast may use only weeks before o. The target is the cumulative demand over h weeks,

  D_h(i, o) = y_{i,o} + … + y_{i,o+h−1},

and every method forecasts the quantiles Q_q(D_h) for q ∈ {0.5, 0.8, 0.9, 0.95, 0.99} **directly**. We do not sum weekly quantiles, because the quantile of a sum is not the sum of quantiles. Two horizons are needed: h = L + R for replenishment (default L = 2, R = 1, so h = 3) and h = H for liquidation (default H = 13). Common post-processing for all methods clips negative values to zero and sorts the quantiles so that they do not cross.

### 3.4 Forecasting methods

**Table 2.** Forecasting methods. s = scale of the series (mean weekly demand over its last 52 active weeks, floor 0.1).

| Label | Family | How the quantiles of D_h are produced | Role |
|---|---|---|---|
| EMP | Statistical | Empirical quantiles of rolling h-week sums over the last 104 weeks | Model-free floor |
| ETS | Statistical | ETS(A,N,N) (Hyndman et al., 2008): normal with mean h·ℓ and variance σ²·Σ_{j=0}^{h−1}(1 + jα)² | Exponential smoothing remains competitive at product–store level [P02 p. 2] |
| TSB-P | Statistical | TSB (Teunter et al., 2011); Poisson(h·p·z) | Standard method for intermittent demand and obsolescence [P16 (abstract)] |
| TSB-NB | Statistical | TSB; negative binomial matched to mean h·p·z and variance h·(p(var_z + z²) − (pz)²); Poisson if not over-dispersed | Wider intervals for lumpy demand |
| LGB-T | ML | LightGBM-Tweedie point forecast μ + normal safety stock: μ + z_q·σ_i | Approach of the M5 Accuracy winner [P02 p. 9] + classical safety stock; main ablation |
| LGB-C | ML | Same Tweedie model + split conformal (Lei et al., 2018): μ + s·F⁻¹_g(q), residuals pooled by demand class g | Intervals from a point model without a normal assumption |
| HGB-Q | ML | scikit-learn HistGradientBoosting, quantile loss, one model per q | Checks that results do not depend on one library |
| **LGB-Q** | ML (main) | LightGBM quantile regression (Koenker & Bassett, 1978), one global model per q | The M5 Uncertainty winner trained LightGBM per quantile [P03 p. 14] |

*Statistical models.* Parameters are chosen per series at each cut-off by the in-sample sum of squared one-step errors, computed from the 14th week of the series: TSB α_d, α_p ∈ {0.05, 0.1, 0.2, 0.3}; SES α ∈ {0.02, 0.05, 0.1, 0.2, 0.3, 0.5}. States are updated every week up to the origin. For ETS, σ is the root of the in-sample one-step MSE. For TSB-NB, var_z is the variance of non-zero demand sizes before the cut-off.

*ML models.* All four ML models are **global** models trained on the target D_h / s and clipped at the 99.9th percentile of the training set. Predictions are multiplied back by s. Because the pinball loss is scale-equivariant, scaling does not bias the quantile objective. LightGBM models (Ke et al., 2017) use fixed hyper-parameters with no tuning: learning rate 0.05, 63 leaves, at least 200 samples per leaf, feature and bagging fraction 0.8, λ₂ = 1, up to 1,000 rounds, early stopping after 50 rounds on the validation origins, seed 2026. The Tweedie models use power 1.1. For LGB-T, σ_i is the root mean squared validation residual of series i, or √μ if the series has no validation rows. For LGB-C, scaled validation residuals (D_h − μ)/s are pooled by demand class; classes with fewer than 200 residuals use the pooled distribution.

LGB-T, LGB-C and LGB-Q share features, target and training data and differ **only in how quantiles are produced**, which makes LGB-T vs. LGB-Q a clean ablation of "point forecast + safety stock" against "direct quantiles". In an earlier run, the Tweedie model was trained on unscaled D_h and produced very large forecasts for near-zero VN1 series; training it on D_h / s reduced these errors (VN1 RMSSE at h = 13 from 1.131 to 0.896). The remaining gap to EMP (0.64) comes mainly from bulk-order spikes that all models miss [R §1.1]. HGB-Q (Pedregosa et al., 2011) differs from LGB-Q in four respects: it is trained on a random sample of at most 300,000 rows (LGB models: at most 3 million), uses learning rate 0.1 and at most 300 rounds, stops early on 10% of the training data, and was run only for h = 3 and 13. It is therefore a **robustness check**, not a like-for-like comparison.

*Features* (M5 27, VN1 21, 19 shared): lags 1, 2, 3, 4, 8, 13, 26, 52; rolling mean and standard deviation over 4, 13 and 26 weeks; share of zero weeks in the last 13 weeks; weeks since the last sale; week of year and month; last week's price and price change over 4 weeks; the scale s. M5 adds the number of events and SNAP days inside the h-week target window (known in advance) and the categorical attributes dept, cat, store and state. Level features are divided by s. VN1 client and warehouse codes are not used.

*Excluded.* Deep global models (e.g. DeepAR, Salinas et al., 2020; TiDE) are outside the scope because of computational cost and because the focus is the decision layer. Damato et al. (2026) found TiDE with a Tweedie output to be the best global model on intermittent data [P12 p. 19], so this is a limitation (Section 6). Croston's method (Croston, 1972) is represented by its obsolescence-aware variant TSB.

### 3.5 Decision layer

At the start of each test week o, with review period R = 1 week, the following steps are applied to every series (`code/f2d/policy.py`):

1. Receive the order placed L weeks earlier.
2. Compute the inventory position IP = on-hand + on-order.
3. **Liquidate** x = min(max(IP − T_liq, 0), on-hand).
4. **Order** q = max(S − IP, 0) with S = Q_τ(D_{L+R}); no order is placed in a week with x > 0.
5. Demand occurs: sales = min(on-hand, demand). Unmet demand is lost.

S and T_liq are rounded up to integers. Initial on-hand equals S of the first test week, with nothing on order. Each series–week receives one of three transparent recommendations: LIQUIDATE if x > 0, ORDER if q > 0, otherwise HOLD.

Five liquidation policies are run on the same replenishment forecasts:

| Policy | Threshold T_liq | Note |
|---|---|---|
| none | ∞ | Replenishment only |
| quantile (proposed) | Q_{q_L}(D_H) from the same forecasting method | Default q_L = 0.95, H = 13 |
| fixed | k × mean weekly sales of the previous 26 weeks | Weeks-of-supply rule, default k = 26 |
| dead13 / dead26 | 0 if the series had no sale in the previous 13 / 26 weeks, else ∞ | When "dead": liquidate all on-hand **and** set S = 0 until the next sale |

The quantile rule uses the forecast distribution itself; the fixed and dead-stock rules need no forecast and act as practitioner-style baselines [Nhận định nhóm].

### 3.6 Evaluation measures

**Forecast accuracy** is computed per series over all test origins and averaged without weights within a group:

- *Scaled quantile loss* SQL = mean_{o,q} ρ_q(D_h − Q_q) / (h · mean|Δy|), where ρ_q is the pinball loss and the denominator is h times the in-sample mean absolute one-step naive error.
- *RMSSE* of the median, scaled by the naive error.
- *Coverage* cov_q = share of origins with D_h ≤ Q_q (ideal value q).

MAPE is not used because it is undefined when demand is zero [P24 p. 4].

**Inventory KPIs** are computed over the 22 test weeks that follow 4 warm-up weeks. Units are summed over all series of a group before ratios are formed, so high-volume series carry more weight.

- Fill rate = Σ sales / Σ demand.
- Cycle service level (CSL) = 1 − (stockout weeks / weeks).
- Stockout rate = stockout weeks / weeks with positive demand.
- Inventory in **weeks of demand** = mean end-of-week on-hand / mean weekly demand.
- Liquidated share = liquidated units / demand.

95% confidence intervals use a bootstrap over series (200 resamples, seed 2026).

**Cost-free comparison.** At a fixed τ, the methods reach different fill rates, so inventory levels are not directly comparable. We therefore:

- run τ ∈ {0.5, 0.8, 0.9, 0.95, 0.99} and draw the inventory–fill-rate **trade-off curve** of each method;
- compute the **inventory needed to reach a target fill rate** (0.90, 0.92, 0.94, 0.96, 0.98) by linear interpolation along each curve, without extrapolation;
- summarise each method by its **frontier rank**: the mean rank of required inventory over the targets that at least two methods reach, where a method that misses a target shares the last ranks.

The levels τ = 0.8, 0.9 and 0.95 correspond to a normalised overage cost of 1 and underage costs of 4, 9 and 19, as in Wang et al. (2026) [P11 p. 16]. A curve that lies above and to the left of another is better for every cost ratio in this range [Nhận định nhóm].

**Break-even salvage ratio of liquidation.** For each policy, we simulate the 26 weeks with and without liquidation from the same initial state. All quantities are counted in units and valued at unit cost c = 1. Let:

- Δ = (with liquidation) − (without liquidation);
- X = units liquidated;
- h_w = weekly holding cost rate (annual rate / 52);
- m = gross margin, so the selling price is (1 + m)·c.

The break-even salvage ratio s\* is the minimum salvage price / unit cost at which liquidating beats keeping the stock. We report two bounds:

- (a) upper bound, ending position valued at cost: s\* = [ΔOrders − ΔEndPosition + h_w·ΔInventory(unit-weeks) − (1 + m)·ΔSales] / X;
- (b) lower bound, ending position eventually salvaged at the same ratio: s\* = [ΔOrders + h_w·ΔInventory − (1 + m)·ΔSales] / (X + ΔEndPosition).

s\* is computed on a grid of holding cost {10, 25, 40}% per year × margin {30, 50, 100}%. We also decompose each liquidated unit into the part re-ordered later (ΔOrders / X), the part that becomes lost sales (−ΔSales / X), and the part that would still have been in stock at the end (−ΔEndPosition / X).

**Per-series statistical tests.** For SQL and for per-series KPIs at τ = 0.9 we report:

- a Friedman test over the 8 methods;
- mean ranks compared with the Nemenyi critical difference (CD, α = 0.05; Demšar, 2006);
- pairwise Wilcoxon signed-rank tests against LGB-Q with Holm correction (Holm, 1979);
- the share of series on which each method wins.

With tens of thousands of series almost every difference has p < 0.001, so conclusions rest on effect sizes: rank differences relative to the CD and win shares.

**Cross-dataset consistency.** The Spearman correlation between the rankings of the 8 methods on M5 and on VN1 is computed by demand class, both for the fill rate at τ = 0.9 and for the frontier rank.

## 4. Experimental Setup

### 4.1 Rolling-origin design

The last 26 weeks of each panel form the test period. It is split into two blocks of 13 weeks; for VN1 the blocks coincide with Phase 1 and Phase 2. Models are retrained at the first week of each block (cut-off c). Every test week is a forecast origin (26 origins). Between cut-offs:

- statistical models update their states each week;
- ML models keep their parameters and are applied to the latest features.

Infrequent retraining follows the finding that reducing retraining frequency cuts computational cost with little loss of accuracy [P08 (abstract)]. ML validation uses the 13 last origins whose target ends before c. Training uses at most 104 earlier origins (at most 3 million rows, randomly sampled if exceeded). Only origins whose target D_h is fully observed before c (last origin c − h) are used, so no future information leaks into training.

### 4.2 Scenarios

| Parameter | Default | Grid (one parameter varied at a time) | Run on |
|---|---|---|---|
| τ | 0.9 | 0.5, 0.8, 0.9, 0.95, 0.99 | M5 and VN1, 8 methods |
| L (weeks) | 2 | 1, 2, 4 | VN1 only, 7 methods (no HGB-Q) |
| H (weeks) | 13 | 8, 13, 26 | VN1 only, 7 methods |
| q_L | 0.95 | 0.9, 0.95, 0.99 | VN1, 8 methods |
| k (weeks) | 26 | 13, 26, 52 | VN1, 8 methods |

The L and H grids were not run on M5 because LGB-Q would have to be retrained for each extra horizon (about 21 minutes for h = 3 on M5) [ES §3].

### 4.3 Second test window

To test robustness, we drop the last 26 weeks of each panel and rerun everything, including all 8 forecasting models from scratch, on the preceding 26 weeks:

- M5: 2015-05-23 to 2015-11-14, 29,917 series;
- VN1: 2023-04-10 to 2023-10-02, 11,442 series. This window lies entirely in Phase 0, so the official answers are not used.

The default scenario, the τ grid and the five liquidation policies were run; the L/H grid and the break-even analysis were not [R §10].

### 4.4 Environment and runtime

Experiments ran on a laptop CPU (Intel Core i5-12450H, 12 threads, 16 GB RAM, Windows 11); the GPU was not used. Software: Python 3.12.10, lightgbm 4.7.0, scikit-learn 1.8.0, pandas 2.3.3, numpy 2.2.6, scipy 1.17.1; seed 2026 [ES §1].

**Table 2b** (or text). Training + forecasting time for one horizon (2 blocks, 26 origins) [ES §4].

| Method | M5 h = 3 | M5 h = 13 | VN1 h = 3 | VN1 h = 13 |
|---|---|---|---|---|
| TSB-NB | 68 s | 55 s | 30 s | 27 s |
| LGB-T | 133 s | 50 s | 10 s | 7 s |
| LGB-C | 98 s | 35 s | 9 s | 8 s |
| HGB-Q (≤ 300k rows) | 105 s | 126 s | 85 s | 99 s |
| LGB-Q (5 quantiles) | 1,251 s | 686 s | 146 s | 314 s |

EMP, TSB-P and ETS were read from cache in this run; at the other VN1 horizons they took 1–38 s. Simulation and KPIs for the full τ grid with 5 policies and 200 bootstrap resamples took about 2 minutes (M5) and 3 minutes (VN1).

### 4.5 Reproducibility

Code, configuration and scripts that rerun all results (`code/outputs/logs/rerun_v24.sh`, `rerun_w26.sh`) are released with the paper **[link to be added]**. Data are not redistributed; download instructions are in `code/README.md`.

### 4.6 Changes made during the study

Three changes were made before the final runs and are reported for transparency [ES §5], [R §1.1]:

- the Tweedie and conformal models were moved to the scaled target;
- the τ grid was extended to five levels;
- dead-stock rules and the second test window were added.

### 4.7 Assumptions

- Observed sales are used as demand. Censoring by historical stockouts cannot be detected.
- Liquidation does not change demand (no price response).
- Unmet demand is lost (no backorders); there are no capacity or minimum-order constraints.
- Hyper-parameters are fixed for every ML model.
- KPIs are unit-weighted.
