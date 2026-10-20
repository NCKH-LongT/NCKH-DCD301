# 7. Conclusion and Future Work

> Draft v0.2, English. Summarises only findings that hold across the test windows (`results.md` Table 8), plus the two extensions. Tag conventions: `paper_outline.md`.

This study benchmarked eight probabilistic demand forecasting methods inside one transparent replenishment-and-liquidation policy on two public retail datasets, M5 (brick-and-mortar) and VN1 (multi-vendor e-commerce). All series were retained, results were reported by ADI–CV² demand class, and the whole benchmark was repeated on three 26-week test windows. The evaluation used inventory KPIs without monetary units, comparisons at equal fill rate with bootstrap confidence intervals, and a break-even salvage ratio for liquidation. A zero-shot foundation model (Chronos-2) and a Vietnamese footwear case study with actual costs extended the benchmark.

**Answers to the research questions.**

- **RQ1 (accuracy and inventory KPIs across datasets and periods).**
  - *M5:* LightGBM quantile regression was both the most accurate method and the most inventory-efficient in all three windows. At a fill rate of 0.94 it needed 3–11% less inventory than the other strong baselines, with all bootstrap intervals excluding zero; HistGradientBoosting quantile regression was close behind [R §10.2].
  - *VN1:* the same model had the lowest mean error, but TSB with negative-binomial demand was as accurate per series at h = 3 and more accurate at h = 13 in every window. LightGBM quantile was the most inventory-efficient method in two of three windows, and TSB-NB in the other. Rankings therefore did not transfer fully from M5 to VN1, nor across periods within VN1.
- **RQ2 (demand classes).**
  - On VN1, LightGBM quantile regression was the most inventory-efficient method for lumpy series in every window, and for intermittent series in the two windows where the class could be ranked. The smooth and erratic leaders changed between windows.
  - On intermittent series, the advantage of LightGBM quantile came from fewer very large errors, not from better forecasts for a typical series.
  - Between M5 and VN1, only the intermittent class had consistent method rankings by fill rate in every window (ρ = 0.83–0.93) [R §10.1].
- **RQ3 (liquidation).**
  - A quantile-based liquidation rule reduced inventory at almost no loss of fill rate in every window.
  - The fixed weeks-of-supply and dead-stock rules lost fill rate or raised stockout weeks; the 13-week dead-stock rule raised them by 43–68% for intermittent VN1 series.
  - Within 26 weeks, liquidation paid off only at salvage prices near unit cost: s\* ≈ 0.91–1.04 for the quantile rule on VN1, and 0.90–1.01 with actual costs in the case study [R §7.2, §10.4].
- **RQ4 (sensitivity).**
  - On both datasets, fill-rate rankings were stable across lead times (ρ ≥ 0.96), and inventory grew roughly with L + R [R §8].
  - The quantile liquidation rule stayed the safer rule across the H, q_L, k and L grids.
  - The steep end of the trade-off curve dominates inventory: on VN1, raising the fill rate from 0.971 to 0.992 more than doubled inventory.

**Extensions.**

- Zero-shot Chronos-2 was never the most accurate or the most inventory-efficient method, even on M5, which is part of its training data, and it was 8–42 times slower on CPU.
- In the Vietnamese footwear case study, LightGBM quantile was the most inventory-efficient method although TSB with Poisson demand had the lowest mean error.

**Implications.** The most accurate forecast is not always the most inventory-efficient one. On intermittent data, methods should be compared at equal service level, by demand class, with per-series statistics and over more than one period [Nhận định nhóm].

**Future work.**

- Use pretrained models with weekly context, covariates or fine-tuning, and add deep global models such as TiDE.
- Simulate a class-based or period-validated selection between TSB-NB and LightGBM quantile.
- Identify the cause of the period dependence on VN1.
- Extend the scenario grid to the earlier test windows.
- Use longer horizons, product-discontinuation data and price-responsive demand to assess the economic case for liquidation.
- Validate the case-study findings on complete company data with actual inventory.
