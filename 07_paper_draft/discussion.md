# 6. Discussion

> Draft v0.1, English. Interpretation of the results in `results.md`. Most statements here are group interpretation and are tagged [Nhận định nhóm]; numbers keep their source tags. Tag conventions: `paper_outline.md`.

## 6.1 What the benchmark shows

**Accuracy and inventory efficiency agree on M5 but not on VN1.** On M5, the method with the lowest forecast error (LGB-Q) also needs the least inventory at every fill target, in both test windows (Table 5). Ranking by error would therefore lead to the same choice as ranking by inventory outcome. On VN1, LGB-Q again has the lowest mean SQL in both windows. However, the most inventory-efficient method switches between windows: LGB-Q in the main window, TSB-NB in the second. TSB-NB is also as accurate per series as LGB-Q at h = 3 and more accurate at h = 13 (Table 4). On intermittent e-commerce data, therefore, a lower average forecast error is not a reliable guide to inventory performance [Nhận định nhóm]. We state this as an observation on our two datasets and two windows, not as a general law. The general relationship between accuracy and inventory performance on M5 has been examined by Theodorou et al. (2025), whose results we could not read.

**Mean errors hide what happens to a typical series.** The VN1 results show how mean SQL and per-series ranks can disagree: the global ML models avoid very large errors, while TSB-NB is better on a typical intermittent series (Section 5.2). A benchmark that reports only mean scaled errors would conclude that LGB-Q dominates VN1. Reporting medians, ranks and win shares alongside means changes that conclusion [Nhận định nhóm].

**Equal-τ comparisons are misleading.** At τ = 0.9, the methods reach fill rates between 0.891 and 0.967 on M5 [R §3 T3], because each calibrates its quantiles differently (Table 3). Comparing inventory at equal τ would reward under-covering methods such as TSB-P, which holds the least stock on 97% of the series but has the lowest fill rate [R §2]. Trade-off curves and the inventory needed at a target fill rate remove this calibration effect. Neither requires a cost assumption [Nhận định nhóm].

**Direct quantiles beat point forecast plus safety stock where tails matter.** LGB-T and LGB-Q share data, features and training. On M5, LGB-Q needs 4.8% (main) and 6.3% (second window) less inventory than LGB-T at fill rate 0.94 (computed from Table 5). On VN1, LGB-T cannot exceed fill rate 0.952 even at τ = 0.99 [R §4]. The normal safety stock is adequate at moderate service levels but fails at high ones on intermittent data, where only learned or over-dispersed tails reach fill rates of 0.96–0.98 [Nhận định nhóm].

## 6.2 Practical implications

The following recommendations are [Nhận định nhóm], conditional on the scenarios studied:

1. **Brick-and-mortar retail with mostly smooth demand (M5-like).** A global LightGBM quantile model is a safe default: it is the most accurate and the most inventory-efficient method in both windows. HistGradientBoosting quantile regression is a close substitute that trains on a 300,000-row sample [R §1, §4].
2. **Intermittent e-commerce data (VN1-like): choose by demand class and target service level, not by mean error.** TSB-NB was the most efficient method for smooth series in both windows. LGB-Q was the most efficient for intermittent and lumpy series and at high fill targets. TSB-NB is cheap to run (27–30 s on VN1 vs. 146–314 s for LGB-Q per horizon [ES §4]), so a class-based combination of the two is a low-cost option. **[Chưa kiểm chứng]:** such a combination was not simulated.
3. **Service targets should be set with the steep end of the trade-off curve in view.** On VN1, moving the fill rate from 0.971 to 0.992 more than doubles inventory (4.77 → 10.37 weeks) [R §8].
4. **Liquidation rules should be forecast-based and conservative.** Two rules lose service:
   - the fixed weeks-of-supply rule clears stock that is later re-ordered or would have been sold;
   - the dead-stock rule raises stockout weeks for intermittent series by 61–67% and loses fill rate on M5, where "dormant" items often sell again [R §7.1, §10].

   The quantile rule loses almost no fill rate. Even so, within 26 weeks it pays off only if stock can be salvaged near unit cost (s\* ≈ 0.91–1.04 on VN1) [R §7.2]. Liquidation should therefore be justified by factors outside this simulation, such as obsolescence, space or product discontinuation, not by holding cost alone.
5. **Transparency.** Every recommendation (ORDER / HOLD / LIQUIDATE) follows from comparing the inventory position with two forecast quantiles, so it can be explained to a planner. This contrasts with reinforcement-learning policies, whose authors note limited interpretability [P21 p. 19].

## 6.3 Comparison with closely related studies

- **Wang et al. (2026) [P11].** Like them, we set the order-up-to level at a quantile of the forecast distribution and map service levels 0.8/0.9/0.95 to cost ratios 4/9/19 [P11 p. 11, 16]. They found that no single method dominated every scenario [P11 p. 18]. Our VN1 results point the same way: the most efficient method depends on the window, the class and the service target. M5 is the exception, where LGB-Q dominated in both windows. Our setting extends theirs in four ways:
  - multi-period simulation with lead time and lost sales, addressing the single-period limitation they state [P11 p. 26];
  - a liquidation decision;
  - results by demand class;
  - a second retail dataset.

  Their methods (forecast combinations of statistical models) and ours (single models including ML) differ, so the numbers are not directly comparable [Nhận định nhóm].
- **Damato et al. (2026) [P12].** They found distributional LightGBM not competitive on intermittent data and found no established global architecture [P12 p. 2, 13, 19]. Our LGB-Q is a quantile-regression model. Two of our results are consistent with their caution: on intermittent VN1 series it is not more accurate per series than TSB-NB, and its mean-SQL advantage comes from fewer large errors. Its upper quantiles, however, were the most inventory-efficient on intermittent and lumpy VN1 series in both windows. The decision layer thus rewards a different property than the median-centred error measures [Nhận định nhóm]. TiDE, their best model [P12 p. 19], was not included here (Section 6.4).
- **Zabraoui et al. (2025) [P21].** They also simulate inventory over many periods on M5, but on a selected subset of volatile food items with RL-based policies [P21 p. 8]. We retain all series and use a transparent policy. The two studies answer different questions: which policy-learning algorithm (theirs) versus which forecast to feed a fixed, interpretable policy (ours) [Nhận định nhóm].
- **Mohammed et al. (2026) [P22].** They suggest intermittent series and quantile regression as future work [P22 p. 18–19]; this study does both. Their safety-stock evaluation is a single illustrative cost calculation on high-volume series [P22 p. 15]. Our results add a caution: with intermittent series included, the normal safety-stock model (LGB-T) cannot reach high fill rates on VN1 [R §4].

## 6.4 Limitations

1. **Two test windows of 26 weeks.** VN1 aggregate inventory efficiency changed between them, and we have not identified why. Seasonal differences and the missing Phase 2 prices are untested hypotheses [R §10]. A third window would be needed for firmer conclusions [R §11].
2. **Liquidation horizon.** Twenty-six weeks are too short to observe the benefits of clearing obsolete stock. The break-even analysis covers holding cost and lost margin only [R §7.2].
3. **No equal-fill-rate significance test.** Per-series tests were run for SQL and for KPIs at fixed τ. Inventory at equal fill rate is not tested, because per-series fill rates are discrete and cannot be interpolated reliably [R §11].
4. **Incomplete scenario grid.** The L and H grid was run on VN1 only. The break-even analysis was not repeated for the second window [ES §3], [R §10].
5. **Censored demand and no price response.** Sales are used as demand, so historical stockouts bias demand downward. Liquidation does not change demand in the simulation [`05_methodology/methodology.md` §9].
6. **Fixed hyper-parameters.** No model was tuned. HGB-Q uses a smaller sample and a different early-stopping scheme, so it is a robustness check rather than a like-for-like competitor [`05_methodology/baseline.md` §2].
7. **Unit-weighted KPIs.** Aggregate KPIs are dominated by high-volume series. Per-series tests give an unweighted view [R §11]. KPIs are not value-weighted because unit costs are unavailable.
8. **Scope of models.** Deep global models (TiDE, DeepAR) and foundation models were excluded for computational reasons, although TiDE was the strongest global model in Damato et al. (2026) [P12 p. 19].
9. **Literature coverage.** Two closely related works were available to us by title only (Theodorou et al., 2025; Li, 2026). Several cited studies are preprints [`02_related_work/paper_list.md`].
