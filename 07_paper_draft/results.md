# 5. Results

> Draft v0.1, English. Every number comes from `06_experiment_results/results.md` [R], `tables/comparison_full.md` [CF], `tables/comparison_w26.md` [CW26] or `tables/stat_tests*.md`. Percentages marked "computed" are simple ratios of values in those tables. Tag conventions: `paper_outline.md`. Method labels: Table 2 (EMP, ETS, TSB-P, TSB-NB, LGB-T, LGB-C, HGB-Q, LGB-Q).

Unless stated otherwise, results refer to the main test window and the default scenario (τ = 0.9, L = 2, R = 1, H = 13, q_L = 0.95, k = 26). Inventory is expressed in weeks of demand. Section 5.7 repeats the analysis on a second test window and determines which findings are reported as robust.

## 5.1 Forecast accuracy (RQ1)

**Table 3.** Mean scaled quantile loss (SQL), RMSSE of the median and coverage of the 0.9 quantile, all evaluated series. Lower is better, except coverage (ideal 0.9). Bold = best per column. Source: [R §1 T1].

| Method | M5 SQL h=3 | M5 SQL h=13 | M5 RMSSE h=3 | M5 cov₀.₉ h=3 | VN1 SQL h=3 | VN1 SQL h=13 | VN1 RMSSE h=3 | VN1 cov₀.₉ h=3 |
|---|---|---|---|---|---|---|---|---|
| EMP | 0.340 | 0.347 | 0.765 | 0.855 | 0.522 | 0.557 | 0.799 | 0.909 |
| TSB-P | 0.283 | 0.361 | 0.596 | 0.793 | 0.454 | 0.506 | 0.645 | 0.849 |
| TSB-NB | 0.251 | 0.317 | 0.610 | 0.881 | 0.411 | 0.458 | 0.650 | 0.903 |
| ETS | 0.246 | 0.254 | 0.601 | 0.890 | 0.431 | 0.445 | 0.654 | 0.912 |
| LGB-T | 0.229 | 0.223 | **0.565** | 0.858 | 0.439 | 0.575 | 0.651 | 0.913 |
| LGB-C | 0.232 | 0.241 | 0.572 | 0.901 | 0.405 | 0.507 | 0.633 | 0.906 |
| HGB-Q | 0.211 | 0.201 | 0.572 | 0.872 | 0.338 | 0.423 | **0.593** | 0.917 |
| **LGB-Q** | **0.208** | **0.198** | 0.570 | 0.883 | **0.336** | **0.410** | 0.594 | 0.921 |

LGB-Q has the lowest mean SQL in all four SQL columns. HGB-Q is within 0.002–0.013 even though it is trained on at most 300,000 rows, so the result does not depend on the LightGBM library alone. The ranking by mean SQL also holds in every demand class of both datasets [R §5 T6]. For point accuracy (RMSSE), the four ML models are close on M5 (0.565–0.572), with LGB-T best.

Calibration of the 0.9 quantile differs between methods and datasets:

- On M5, most methods under-cover (0.79–0.89); only LGB-C reaches 0.901.
- On VN1, most methods cover 0.90–0.92, but TSB-P covers only 0.849 because Poisson intervals are too narrow.

These calibration differences are why inventory efficiency is compared at equal fill rate (Section 5.3) rather than at equal τ.

## 5.2 Per-series comparison

Mean SQL can be dominated by a few series with very large errors. We therefore also rank the methods series by series. The Friedman test rejects equal performance (p < 0.001) for every dataset, class and metric [R §2].

**Table 4.** Mean rank by per-series SQL (1 = best; top three per column, Nemenyi CD in brackets) and median per-series SQL on VN1. Sources: [R §2 T2] and the median table in [R §2].

| Rank | M5 h = 3 (CD 0.06) | M5 h = 13 (CD 0.06) | VN1 h = 3 (CD 0.09) | VN1 h = 13 (CD 0.09) |
|---|---|---|---|---|
| 1 | LGB-Q 3.40 | HGB-Q 3.72 | TSB-NB 3.62 | TSB-NB 3.36 |
| 2 | HGB-Q 3.66 | LGB-Q 3.81 | LGB-Q 3.68 | TSB-P 3.74 |
| 3 | LGB-T 4.23 | LGB-T 3.99 | HGB-Q 3.73 | HGB-Q 4.50 |

| VN1 median SQL (h = 3 / h = 13) | All series | Intermittent |
|---|---|---|
| LGB-Q | 0.152 / 0.175 | 0.133 / 0.181 |
| TSB-NB | 0.152 / 0.107 | 0.112 / 0.080 |
| TSB-P | 0.151 / 0.110 | 0.111 / 0.079 |

On **M5**, the per-series results agree with the means:

- At h = 3, LGB-Q has the best mean rank and beats HGB-Q on 57.3% of the series.
- At h = 13, HGB-Q ranks 0.09 better than LGB-Q, slightly above the CD, but the Wilcoxon test gives p = 0.055 and HGB-Q wins on only 53% of the series, so the two are practically tied.
- LGB-Q and HGB-Q are also best by median SQL in every class and at both horizons [R §2].

On **VN1**, the picture is different:

- At h = 3, TSB-NB, LGB-Q and HGB-Q are within the CD of each other.
- At h = 13, TSB-NB ranks first and LGB-Q only 4.67; LGB-Q is worse than TSB-NB on 69% of the series [R §2].
- By median SQL, TSB-NB and TSB-P match LGB-Q at h = 3 and are clearly better at h = 13 (0.107–0.110 vs. 0.175), especially on intermittent series.
- By class (h = 3), LGB-Q ranks best on erratic and lumpy series, TSB-NB on intermittent series (3.11 vs. 4.02), and HGB-Q on smooth series [R §2].

Thus, on VN1 the global ML models are **not** more accurate than TSB for a typical intermittent series. Their lower mean SQL comes from robustness: they rarely make very large errors [Nhận định nhóm]. This agrees with the observation of Damato et al. (2026) that no global architecture is established for intermittent series [P12 p. 2]. We therefore report both means and per-series ranks/medians throughout.

## 5.3 Inventory efficiency at equal fill rate (RQ1)

At τ = 0.9 the methods do not reach the same fill rate. For example, on M5 the fill rate ranges from 0.891 (TSB-P) to 0.967 (LGB-C) [R §3 T3]. Per-series KPI tests at τ = 0.9 are significant but mostly reflect these different service levels; for instance, TSB-P holds less inventory than LGB-Q on 97% of the series but has the lowest fill rate [R §2]. The default-scenario KPIs are therefore given in the Appendix, and the comparison below uses the trade-off curves.

![Figure 1a](../06_experiment_results/figures/fig_tradeoff_M5.png)
![Figure 1b](../06_experiment_results/figures/fig_tradeoff_VN1.png)

**Figure 1.** Inventory (weeks of demand) vs. fill rate as τ varies from 0.5 to 0.99, main test window. (a) M5, (b) VN1. Curves further up and to the left are better.

**Table 5.** Inventory (weeks of demand) needed to reach a target fill rate, all series, linear interpolation along the τ curve. "—" = target outside the range reached with τ ∈ [0.5, 0.99]. Bold = least inventory. Sources: [CF] (main window), [CW26] (second window).

*Panel A — M5*

| Method | Main 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Second 0.90 | 0.92 | 0.94 | 0.96 | 0.98 |
|---|---|---|---|---|---|---|---|---|---|---|
| EMP | 1.41 | 1.62 | 1.88 | 2.31 | 3.14 | 1.57 | 1.81 | 2.11 | 2.58 | 3.48 |
| TSB-P | 1.08 | 1.32 | — | — | — | 1.15 | 1.39 | — | — | — |
| TSB-NB | 1.09 | 1.24 | 1.51 | 1.92 | 2.91 | 1.18 | 1.31 | 1.60 | 1.99 | 2.95 |
| ETS | 1.20 | 1.32 | 1.52 | 1.87 | 2.67 | 1.29 | 1.43 | 1.60 | 1.99 | 2.79 |
| LGB-T | 1.07 | 1.19 | 1.45 | 1.83 | — | 1.19 | 1.31 | 1.59 | 1.98 | — |
| LGB-C | 1.14 | 1.26 | 1.44 | 1.91 | 2.82 | 1.26 | 1.38 | 1.61 | 2.07 | 3.01 |
| HGB-Q | 1.03 | 1.15 | 1.39 | 1.74 | 2.60 | **1.13** | 1.25 | 1.51 | 1.85 | 2.72 |
| LGB-Q | **1.02** | **1.12** | **1.38** | **1.69** | **2.49** | **1.13** | **1.24** | **1.49** | **1.80** | **2.59** |

*Panel B — VN1*

| Method | Main 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Second 0.90 | 0.92 | 0.94 | 0.96 | 0.98 |
|---|---|---|---|---|---|---|---|---|---|---|
| EMP | 3.16 | 3.73 | 4.67 | — | — | 2.10 | 2.46 | 3.03 | 4.05 | — |
| TSB-P | — | — | — | — | — | — | — | — | — | — |
| TSB-NB | 2.21 | 2.67 | 3.50 | 4.79 | — | **1.10** | **1.22** | **1.63** | 2.27 | 4.10 |
| ETS | 2.38 | 2.83 | 3.54 | — | — | 1.28 | 1.49 | 1.78 | 2.40 | — |
| LGB-T | **2.05** | **2.48** | 3.19 | — | — | 1.21 | 1.37 | 1.65 | **2.13** | — |
| LGB-C | 2.10 | 2.55 | 3.22 | 4.72 | 8.94 | 1.19 | 1.30 | 1.71 | 2.23 | **3.67** |
| HGB-Q | 2.17 | 2.68 | 3.31 | 4.36 | 7.61 | 1.21 | 1.38 | 1.77 | 2.37 | 4.19 |
| LGB-Q | 2.07 | 2.54 | **3.17** | **4.13** | **7.24** | 1.20 | 1.38 | 1.79 | 2.33 | 3.87 |

**M5.** LGB-Q needs the least inventory at every fill target in both windows; HGB-Q is second or tied. At fill rate 0.94, LGB-Q needs (computed from Table 5) the following amounts less inventory than the other baselines:

| Baseline | Main window | Second window |
|---|---|---|
| LGB-C | 4.2% | 7.5% |
| LGB-T | 4.8% | 6.3% |
| TSB-NB | 8.6% | 6.9% |
| ETS | 9.2% | 6.9% |

At fill rate 0.96 the savings against these four baselines are 7.7–12.0% (main) and 9.1–13.0% (second). Its frontier rank is 1.0 (main) and 1.2 (second); HGB-Q follows with 2.0 and 1.8 [R §4 T5], [CW26]. The direct-quantile model therefore dominates the point-forecast-plus-safety-stock ablation (LGB-T) on M5, which supports hypothesis H2 for this dataset [R §9].

**VN1.** The results depend on the test window.

- *Main window:* LGB-T needs slightly less inventory at fill rates 0.90–0.92 (2.05 vs. 2.07; 2.48 vs. 2.54), and LGB-Q is best from 0.94 upwards. LGB-T cannot exceed a fill rate of 0.952 even at τ = 0.99 [R §4]. We attribute this to the thin tail of the normal safety-stock distribution on intermittent data [Nhận định nhóm]. Only methods with a learned or over-dispersed tail (LGB-Q, HGB-Q, LGB-C, and TSB-NB up to 0.96) reach fill rates of 0.96–0.98. Frontier ranks: LGB-Q 1.4, LGB-C 3.0, LGB-T 3.3, TSB-NB 4.8.
- *Second window:* TSB-NB needs the least inventory at fill rates 0.90–0.94, LGB-T at 0.96, and LGB-C at 0.98. Frontier ranks: TSB-NB 1.8, LGB-C 2.0, LGB-T 3.5, LGB-Q 3.8 [CW26].

In the main window TSB-NB needs 5–10% more inventory than LGB-Q at fill rates 0.92–0.94; in the second window LGB-Q needs 10–13% more than TSB-NB [R §10]. Hence, on VN1 no method is the most inventory-efficient in both windows, and the lowest mean SQL (LGB-Q in both windows) does not reliably translate into the lowest inventory [Nhận định nhóm]. Section 5.7 discusses this further.

## 5.4 Results by demand class (RQ2)

**Table 6.** Frontier rank by demand class (mean rank of required inventory over fill targets 0.90–0.98; 1 = least inventory). Sources: [R §4 T5] (main), [CW26] (second).

| Method | M5 all (main / 2nd) | VN1 smooth | VN1 erratic | VN1 intermittent | VN1 lumpy | VN1 all |
|---|---|---|---|---|---|---|
| EMP | 7.2 / 7.2 | 6.8 / 7.2 | 6.1 / 6.9 | 6.7 / 6.6 | 5.9 / 6.9 | 6.7 / 6.9 |
| TSB-P | 6.7 / 6.5 | 7.6 / 6.6 | 6.9 / 7.7 | 7.1 / 7.2 | 6.3 / 7.7 | 7.3 / 7.7 |
| TSB-NB | 5.0 / 4.0 | **2.4 / 2.0** | 5.3 / 2.8 | 3.2 / 4.4 | 5.2 / 2.4 | 4.8 / **1.8** |
| ETS | 5.4 / 5.2 | 4.0 / 2.6 | 5.9 / 5.7 | 5.2 / 5.2 | 6.3 / 6.1 | 6.1 / 5.9 |
| LGB-T | 4.1 / 4.5 | 3.4 / 3.6 | 4.3 / 2.5 | 4.4 / 3.6 | 6.3 / 3.3 | 3.3 / 3.5 |
| LGB-C | 4.6 / 5.6 | 3.0 / 4.0 | 3.7 / **2.2** | 4.8 / 4.8 | 2.8 / 4.4 | 3.0 / 2.0 |
| HGB-Q | 2.0 / 1.8 | 5.4 / 4.8 | 2.6 / 4.2 | 3.2 / 2.2 | 2.2 / 3.2 | 3.4 / 4.4 |
| LGB-Q | **1.0 / 1.2** | 3.4 / 5.2 | **1.2** / 4.0 | **1.4 / 2.0** | **1.0 / 2.0** | **1.4** / 3.8 |

VN1 cells show main / second window.

**M5.** The direct quantile models have the lowest SQL in all four classes [R §5 T6] and the best frontier ranks in all classes, except erratic in the main window, where LGB-C ranks first (1.6) [R §4 T5].

**VN1.** Three class-level results hold in both windows:

- *Smooth:* TSB-NB is the most inventory-efficient method (frontier rank 2.4 and 2.0). In the main window it needs 1.19 weeks at fill rate 0.90 vs. 1.28 for ETS, LGB-Q and LGB-T [R §5].
- *Intermittent:* LGB-Q ranks first (1.4 and 2.0). In the main window TSB-NB needs less inventory at moderate service levels (2.12 vs. 2.47 weeks at fill rate 0.90). LGB-Q is better from 0.94 upwards, and TSB-NB cannot reach 0.96 [R §5].
- *Lumpy:* LGB-Q ranks first (1.0 and 2.0). In the main window only five methods reach fill rate 0.90 on lumpy series, and LGB-Q needs 6.06 weeks against 8.99 for TSB-NB and 12.8 for EMP [R §5].

The erratic class changes leader between windows (LGB-Q in the main window, LGB-C in the second).

This contradicts our initial hypothesis H3, which expected ML to help most on smooth and erratic series and TSB to suffice for intermittent ones. On VN1 the opposite holds for the frontier: TSB-NB is best on smooth series and LGB-Q on intermittent and lumpy series. However, per-series SQL still favours TSB-NB on intermittent series (Section 5.2) [R §9].

To see whether the frontier advantage of LGB-Q on intermittent series comes from better upper quantiles, we computed the scaled pinball loss separately for each quantile (h = 3) [R §2.1], `tables/per_quantile_loss.csv`. On VN1 intermittent series:

- LGB-Q beats TSB-NB on only 24–33% of the series at every quantile in the main window, and on 29–34% in the second window.
- TSB-NB's per-series advantage is **largest** at the highest quantile. At q = 0.99 the median loss is 0.025 vs. 0.064 in the main window, and 0.027 vs. 0.052 in the second.
- By the mean, LGB-Q is better at every quantile (q = 0.99: 0.206 vs. 0.321 main; 0.678 vs. 1.241 second), because TSB-NB occasionally makes very large errors.

The frontier advantage of LGB-Q on intermittent series therefore does not come from a better upper tail on a typical series. It matches the pattern of a smaller *mean* loss: fewer very large errors [Nhận định nhóm]. One possible mechanism is that unit-weighted KPIs are dominated by the series on which TSB-NB fails badly; this link was not tested **[Chưa kiểm chứng]**.

**Cross-dataset consistency.** The Spearman correlation between the rankings of the 8 methods on M5 and on VN1 is unstable:

- by frontier rank it is 0.88 (p = 0.004) in the main window but 0.50 (p = 0.21) in the second;
- by fill rate at τ = 0.9 it is 0.69 and 0.93 [R §6 T7], [R §10 T11];
- only the **intermittent** class is consistent in both windows and under both ranking criteria (ρ = 0.83–0.95).

Thus, whether a method ranking transfers from M5 to VN1 depends on the class and the period. We do not find a ranking criterion that is consistent in general.

## 5.5 Liquidation (RQ3)

**Table 7.** Liquidation policies with LGB-Q forecasts, default scenario, all series, main window. Inventory in weeks of demand; % liq. = liquidated units / demand; stockout = stockout weeks / weeks with demand. s\* = break-even salvage ratio (upper bound), range over holding cost 10–40%/year × margin 30–100%, four ML models. Sources: [CF], [R §7 T8], [R §7.1], [R §7.2].

| Dataset | Policy | Inventory | % liq. | Fill rate | Stockout rate | s\* range |
|---|---|---|---|---|---|---|
| M5 | none | 1.581 | 0 | 0.956 | 0.072 | — |
| M5 | quantile | 1.579 | 0.02 | 0.956 | 0.072 | unstable (\*) |
| M5 | fixed (k = 26) | 1.545 | 0.79 | 0.953 | 0.077 | 1.06–1.32 |
| M5 | dead13 | 1.542 | 0.67 | 0.949 | 0.081 | 1.35–2.08 |
| VN1 | none | 3.405 | 0 | 0.948 | 0.066 | — |
| VN1 | quantile | 3.261 | 1.18 | 0.948 | 0.066 | 0.91–1.04 |
| VN1 | fixed (k = 26) | 3.198 | 2.76 | 0.941 | 0.079 | 1.00–1.22 |
| VN1 | dead13 | 3.269 | 1.21 | 0.947 | 0.081 | 1.03–1.37 |

(\*) Fewer than 1,200 units are liquidated on the whole of M5, so s\* is not stable.

**Quantile rule.** On M5 the rule almost never triggers for the ML models, ETS and EMP (≤ 0.02% of demand). It triggers only for TSB-P and TSB-NB (about 1.1% of demand) and then costs about 0.5 percentage points (pp) of fill rate [R §7]. On VN1, with the ML models, it reduces inventory by 0.6–12%, costs at most 0.1 pp of fill rate, and touches 2–12% of the series [R §7].

**Fixed rule.** On VN1, with the four ML forecasts, the fixed rule costs 0.2–0.7 pp of fill rate and touches 42–51% of the series [R §7].

**Lumpy series** show the largest effects (VN1, LGB-Q):

| Policy | Inventory | Change | Fill rate |
|---|---|---|---|
| none | 7.52 weeks | — | 0.928 |
| quantile | 6.73 weeks | −10.5% | 0.926 |
| fixed | 6.40 weeks | −14.9% | 0.877 |
| dead13 | 7.02 weeks | −6.6% | 0.923 |

**Dead-stock rule.** We added the dead-stock rule because 28.2% of VN1 series have no demand in the 22 KPI weeks, while the quantile rule touches only 5.4% of the series [R §7.1].

- On VN1 intermittent series, dead13 cuts inventory more than the quantile rule (−19.4% vs. −5.9%) but raises the stockout rate from 0.081 to 0.135 (+68%).
- On M5, products that have not sold for 13 weeks usually sell again, so dead13 costs 0.66 pp of fill rate [R §7.1].

**Break-even salvage ratio.** For every rule and both datasets, s\* is close to or above 1. Liquidation pays off within the 26-week window only if stock is sold at roughly unit cost or more [R §7.2]. The decomposition per liquidated unit explains why [R §7.2 T10]:

- *Fixed rule:* 0.35–0.63 (VN1) and 0.57–0.63 (M5) of each liquidated unit is ordered again later, and 0.12–0.32 becomes lost sales.
- *Dead13 on VN1* targets truly unsold stock: 0.93–1.05 of each liquidated unit would still be on hand at the end. Yet 8–13 units of sales are lost per 100 liquidated, and within 26 weeks the holding cost saved does not cover this loss.
- *Dead13 on M5* is wrong most of the time: 0.86–0.97 of each liquidated unit becomes a lost sale.
- *Quantile rule:* has the lowest s\*, but still needs a salvage price close to cost.

Benefits such as avoiding obsolescence or freeing space would require a horizon longer than 26 weeks, or data on discontinued products, to be assessed [Nhận định nhóm].

## 5.6 Sensitivity (RQ4)

**Target service level** (LGB-Q, fill rate / inventory) [R §8]:

| τ | 0.5 | 0.8 | 0.9 | 0.95 | 0.99 |
|---|---|---|---|---|---|
| M5 | 0.816 / 0.59 | 0.921 / 1.13 | 0.956 / 1.58 | 0.974 / 2.05 | 0.992 / 3.32 |
| VN1 | 0.797 / 0.97 | 0.907 / 2.16 | 0.948 / 3.41 | 0.971 / 4.77 | 0.992 / 10.37 |

On VN1, raising the fill rate from 0.971 to 0.992 more than doubles inventory (4.77 → 10.37 weeks). TSB-P hardly reacts to τ on VN1 (fill rate 0.793 → 0.843 for τ from 0.5 to 0.99) [R §8].

**Lead time** (VN1 only) [R §8]:

- Fill-rate rankings are stable across L: the Spearman correlation between L = 2 and L = 1 is 0.96, and between L = 2 and L = 4 it is 1.00 (7 methods).
- Inventory grows roughly in proportion to L + R; for LGB-Q it is 2.07, 3.41 and 6.01 weeks at L = 1, 2 and 4.
- TSB-NB loses fill rate fastest as L grows (−2.2 pp from L = 2 to L = 4).

**Liquidation parameters** (VN1, LGB-Q) [R §8]:

- H = 8 / 13 / 26 gives a liquidated share of 3.1 / 1.2 / 0.2% with fill rate 0.946 / 0.948 / 0.948.
- q_L = 0.9 / 0.95 / 0.99 gives 2.8 / 1.2 / 0.2%.
- The fixed rule with k = 13 / 26 / 52 liquidates 7.1 / 2.8 / 1.2% with fill rate 0.929 / 0.941 / 0.946.
- At L = 4, the quantile rule liquidates 5.0% and loses 0.1 pp of fill rate, whereas the fixed rule liquidates 8.6% and loses 1.9 pp.

Across the grid, the quantile rule is the safer liquidation rule in terms of fill rate [Nhận định nhóm].

## 5.7 Robustness: second test window

![Figure 2a](../06_experiment_results/figures/fig_tradeoff_M5_w26.png)
![Figure 2b](../06_experiment_results/figures/fig_tradeoff_VN1_w26.png)

**Figure 2.** Inventory–fill-rate trade-off curves in the second test window (M5: 2015-05-23 to 2015-11-14; VN1: 2023-04-10 to 2023-10-02).

The comparison of the two windows [R §10 T11] separates robust from period-dependent findings.

**Robust in both windows:**

- LGB-Q has the lowest mean SQL at h = 3 on both datasets: M5 0.208 / 0.215, VN1 0.336 / 0.539.
- M5 per-series ranks: LGB-Q leads at h = 3 (3.40 / 3.50, vs. HGB-Q 3.66 / 3.72); LGB-Q and HGB-Q are tied at h = 13.
- VN1 per-series ranks: TSB-NB, LGB-Q and HGB-Q are within the CD at h = 3; TSB-NB leads at h = 13 (3.36 / 3.45).
- M5 frontier ranks: LGB-Q 1.0 / 1.2, HGB-Q 2.0 / 1.8.
- VN1 frontier leaders by class: TSB-NB on smooth series; LGB-Q on intermittent and lumpy series.
- Liquidation: the quantile rule loses almost no fill rate (VN1, LGB-Q: inventory −4.2% / −1.7%, Δfill −0.02 pp in both windows). Dead13 raises the stockout rate of VN1 intermittent series (0.081 → 0.135 and 0.087 → 0.140, i.e. +61% to +68%) and always costs fill rate on M5 (−0.66 / −0.46 pp).
- Cross-dataset consistency of the intermittent class (ρ = 0.90 / 0.95 by frontier rank).

**Not robust:**

- The VN1 aggregate frontier ranking: LGB-Q leads in the main window (1.4), TSB-NB in the second (1.8; LGB-Q 3.8).
- The VN1 erratic-class leader.
- The cross-dataset Spearman correlation of all-series rankings (frontier: 0.88 → 0.50; fill rate: 0.69 → 0.93).

The cause of the VN1 reversal has not been identified. Two candidate explanations are seasonal differences between the windows and missing prices in Phase 2, where the main window uses carried-forward prices [R §10] — **[Chưa kiểm chứng]**. We therefore report VN1 aggregate inventory efficiency as period-dependent and base our conclusions on the robust findings above.
