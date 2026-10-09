# 7. Conclusion and Future Work

> Draft v0.1, English. Summarises only findings that hold in both test windows (`paper_outline.md` §1). Tag conventions: `paper_outline.md`.

This study benchmarked eight probabilistic demand forecasting methods inside one transparent replenishment-and-liquidation policy on two public retail datasets: M5 (brick-and-mortar) and VN1 (multi-vendor e-commerce). All series were retained, results were reported by ADI–CV² demand class, and the analysis was repeated on a second test window. Evaluation used inventory KPIs without monetary units, comparisons at equal fill rate, and a break-even salvage ratio for liquidation.

**Answers to the research questions.**

- **RQ1 (accuracy and inventory KPIs across datasets).**
  - *M5:* LightGBM quantile regression was both the most accurate method (mean SQL at h = 3 of 0.208 and 0.215 in the two windows, best per-series rank) and the most inventory-efficient. At fill rates 0.94–0.96 it needed 4–13% less inventory than the strong baselines, with HistGradientBoosting quantile regression close behind [R §10].
  - *VN1:* the same model had the lowest mean error, but TSB with negative-binomial demand was as accurate per series at h = 3 and more accurate at h = 13. The most inventory-efficient method overall changed between windows. Rankings therefore did not transfer fully from M5 to VN1.
- **RQ2 (demand classes).**
  - On VN1, TSB-NB was the most inventory-efficient method for smooth series, and LightGBM quantile regression for intermittent and lumpy series, in both windows. The erratic class was unstable.
  - Only the intermittent class had consistent method rankings between M5 and VN1 in both windows (ρ = 0.83–0.95) [R §10].
- **RQ3 (liquidation).**
  - A quantile-based liquidation rule reduced inventory at almost no loss of fill rate.
  - Fixed weeks-of-supply and dead-stock rules lost fill rate or raised stockout weeks; the 13-week dead-stock rule raised them by 61–67% for VN1 intermittent series.
  - Within 26 weeks, liquidation paid off only at salvage prices near or above unit cost (s\* ≈ 0.91–1.04 for the quantile rule on VN1) [R §7.2].
- **RQ4 (sensitivity).**
  - On VN1, fill-rate rankings were stable across lead times (ρ ≥ 0.96), and inventory grew roughly with L + R [R §8].
  - The quantile liquidation rule stayed the safer rule across the H, q_L, k and L grids.
  - The steep end of the trade-off curve dominates inventory: on VN1, raising the fill rate from 0.971 to 0.992 more than doubled inventory.

**Implications.** The most accurate forecast is not always the most inventory-efficient one. On intermittent e-commerce data, methods should be compared at equal service level, by demand class, and with per-series statistics as well as mean errors [Nhận định nhóm].

**Future work.**

- Add deep global models such as TiDE and DeepAR, and foundation models, to the same decision layer.
- Simulate a class-based selection of methods (e.g. TSB-NB for smooth series, LightGBM quantile for intermittent and lumpy series).
- Add further test windows and identify the cause of the VN1 period dependence.
- Extend the scenario grid and break-even analysis to M5 and to the second window.
- Use longer horizons, product-discontinuation data and price-responsive demand to assess the economic case for liquidation.
- Use value-weighted KPIs where unit costs are available.
