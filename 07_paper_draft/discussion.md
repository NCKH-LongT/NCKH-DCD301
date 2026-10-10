# 6. Discussion

> Draft v0.2, English. Interpretation of the results in `results.md`. Most statements here are group interpretation and are tagged [Nhận định nhóm]; numbers keep their source tags. Tag conventions: `paper_outline.md`.

## 6.1 What the benchmark shows

**Accuracy and inventory efficiency agree on M5 but not reliably on VN1.**

- *M5:* the method with the lowest forecast error (LGB-Q) also needs the least inventory at every fill target, in all three windows, and the bootstrap intervals exclude zero (Table 5). Ranking by error would lead to the same choice as ranking by inventory outcome.
- *VN1:* LGB-Q again has the lowest mean SQL in every window, but it is the most inventory-efficient method in only two of three windows. In the main window its lead over LGB-T, LGB-C and TSB-NB is not statistically significant; in the second window TSB-NB needs significantly less inventory (Table 5).

On intermittent e-commerce data, therefore, a lower average forecast error is not a reliable guide to inventory performance [Nhận định nhóm]. We state this as an observation on our datasets and windows, not as a general law. The general relationship between accuracy and inventory performance on M5 has been examined by Theodorou et al. (2025), whose results we could not read.

**The ML advantage on intermittent data is robustness, not typical-case accuracy.** On VN1, TSB-NB is as accurate per series as LGB-Q at h = 3 and more accurate at h = 13 in every window (Table 4). The per-quantile analysis sharpens this: on intermittent series, LGB-Q has a lower pinball loss than TSB-NB on only 24–34% of the series at every quantile, including q = 0.99, while it has the lower mean loss (Section 5.4). LGB-Q nevertheless needs less inventory on lumpy series in all windows, and on intermittent series where the class can be ranked. With unit-weighted KPIs, avoiding rare but very large errors appears to matter more for aggregate inventory than being accurate on the typical series [Nhận định nhóm; mechanism not tested].

The practical lesson is to report mean errors together with medians, per-series ranks and win shares. On VN1 the mean SQL of the same model ranges from 0.336 to 2.008 across windows while its median hardly moves (Section 5.1); a benchmark that reports only means would give an unstable and partly misleading picture [Nhận định nhóm].

**Equal-τ comparisons are misleading.** At τ = 0.9, the methods reach fill rates between 0.891 and 0.967 on M5 [R §3 T3], because each calibrates its quantiles differently (Table 3). Comparing inventory at equal τ would reward under-covering methods such as TSB-P, which holds less stock than LGB-Q on 97% of the series but has the lowest fill rate [R §2]. Trade-off curves and the inventory needed at a target fill rate remove this calibration effect, need no cost assumption, and—with series bootstrapping—come with confidence intervals [Nhận định nhóm].

**Direct quantiles beat point forecast plus safety stock where tails matter.** LGB-T and LGB-Q share data, features and training.

- On M5, LGB-T needs 5.1%, 6.8% and 3.3% more inventory than LGB-Q at fill rate 0.94 in the three windows, with intervals excluding zero (Table 5).
- On VN1, LGB-T cannot exceed fill rate 0.952 even at τ = 0.99 in the main window [R §4], and does not reach 0.94 in the third window.

The normal safety stock is adequate at moderate service levels but fails at high ones on intermittent data, where only learned or over-dispersed tails reach fill rates of 0.96–0.98 [Nhận định nhóm].

**A general-purpose foundation model does not replace a simple global model here.** Zero-shot Chronos-2 is less accurate than LGB-Q on 64–79% of the series and never the most inventory-efficient method (Table 9). This holds even on M5, which is part of its training data. It is also 8–42 times slower on CPU. Within the setting we tested (zero-shot, no covariates, h-week totals as context; Section 3.4), a pretrained model did not change the conclusions [Nhận định nhóm]. Other ways of using it—weekly series with covariates, cross-series learning or fine-tuning—may perform differently **[Chưa kiểm chứng]**.

## 6.2 Practical implications

The following recommendations are [Nhận định nhóm], conditional on the scenarios studied:

1. **Brick-and-mortar retail with mostly smooth demand (M5-like).** A global LightGBM quantile model is a safe default: it is the most accurate and the most inventory-efficient method in all three windows. HistGradientBoosting quantile regression is a close substitute (within 0–1.5% inventory at fill rate 0.94) that trains on a 300,000-row sample [R §1, §10.2].
2. **Intermittent e-commerce data (VN1-like): validate on several periods and by class, not on mean error.**
   - The most efficient method changed between windows, and the smooth-class leader was not stable.
   - LGB-Q was consistently best only on lumpy series.
   - TSB-NB is cheap to run (27–30 s on VN1 vs. 146–314 s for LGB-Q per horizon [ES §4]) and was best in one window, so a class-based or period-validated choice between the two is a low-cost option. **[Chưa kiểm chứng]:** such a selection rule was not simulated.
3. **Set service targets with the steep end of the trade-off curve in view.** On VN1, moving the fill rate from 0.971 to 0.992 more than doubles inventory (4.77 → 10.37 weeks) [R §8].
4. **Make liquidation rules forecast-based and conservative.** Two rules lose service:
   - the fixed weeks-of-supply rule clears stock that is later re-ordered or would have been sold;
   - the dead-stock rule raises stockout weeks for intermittent VN1 series by 43–68% across windows and loses fill rate on M5, where "dormant" items often sell again [R §7.1, §10.1].

   The quantile rule loses almost no fill rate in any window. Even so, within 26 weeks it pays off only if stock can be salvaged near unit cost: s\* ≈ 0.91–1.04 on VN1 with assumed margins, and 0.90–1.01 in the footwear case study with actual costs [R §7.2, §10.4]. Liquidation should therefore be justified by factors outside this simulation, such as obsolescence, space or product discontinuation, not by holding cost alone.
5. **Transparency.** Every recommendation (ORDER / HOLD / LIQUIDATE) follows from comparing the inventory position with two forecast quantiles, so it can be explained to a planner. This contrasts with reinforcement-learning policies, whose authors note limited interpretability [P21 p. 19].

## 6.3 Comparison with closely related studies

- **Wang et al. (2026) [P11].** Like them, we set the order-up-to level at a quantile of the forecast distribution and map service levels 0.8/0.9/0.95 to cost ratios 4/9/19 [P11 p. 11, 16]. They found that no single method dominated every scenario [P11 p. 18]. Our VN1 results point the same way: the most efficient method depends on the window, the class and the service target. M5 is the exception, where LGB-Q dominated in all windows. Our setting extends theirs in five ways:
  - multi-period simulation with lead time and lost sales, addressing the single-period limitation they state [P11 p. 26];
  - a liquidation decision;
  - results by demand class;
  - a second retail dataset;
  - several test periods.

  Their methods (forecast combinations of statistical models) and ours (single models including ML) differ, so the numbers are not directly comparable [Nhận định nhóm].
- **Damato et al. (2026) [P12].** They found distributional LightGBM not competitive on intermittent data and found no established global architecture [P12 p. 2, 13, 19]. Our LGB-Q is a quantile-regression model, and our results are consistent with their caution: on intermittent VN1 series LGB-Q is less accurate than TSB-NB for most series at every quantile [R §2.1, §10.1]. Its advantage is a lower *mean* loss. They also left pretrained models for future work [P12 p. 2]; our Chronos-2 check gives one data point (Section 5.8).
- **Zabraoui et al. (2025) [P21].** They also simulate inventory over many periods on M5, but on a selected subset of volatile food items with RL-based policies [P21 p. 8]. We retain all series and use a transparent policy. The two studies answer different questions: which policy-learning algorithm (theirs) versus which forecast to feed a fixed, interpretable policy (ours) [Nhận định nhóm].
- **Mohammed et al. (2026) [P22].** They suggest intermittent series and quantile regression as future work [P22 p. 18–19]; this study does both. Their safety-stock evaluation is a single illustrative cost calculation on high-volume series [P22 p. 15]. Our results add a caution: with intermittent series included, the normal safety-stock model (LGB-T) cannot reach high fill rates on VN1 [R §4].

## 6.4 Limitations

1. **Three test windows of 26 weeks.** VN1 aggregate inventory efficiency and the smooth- and erratic-class leaders changed between windows, and we have not identified why. Seasonal differences and the missing Phase 2 prices are untested hypotheses [R §10]. Chronos-2 was run on one M5 window only, because of its CPU cost.
2. **Liquidation horizon.** Twenty-six weeks are too short to observe the benefits of clearing obsolete stock. The break-even analysis covers holding cost and lost margin only [R §7.2].
3. **Equal-fill-rate uncertainty.** Confidence intervals come from a bootstrap over series of aggregate trade-off curves; there is no per-series test at equal fill rate, because per-series fill rates are discrete [R §10.2, §11].
4. **Scenario grid in one window.** The L, H, q_L and k grids were run on the main window of M5 and VN1 only; HGB-Q and Chronos-2 were run at the default horizons only [R §8].
5. **Censored demand and no price response.** Sales are used as demand, so historical stockouts bias demand downward. Liquidation does not change demand in the simulation [`05_methodology/methodology.md` §9].
6. **Fixed hyper-parameters.** No model was tuned. HGB-Q uses a smaller sample and a different early-stopping scheme, so it is a robustness check rather than a like-for-like competitor [`05_methodology/baseline.md` §2]. Chronos-2 was used zero-shot with one context design only.
7. **Weighting.** Aggregate KPIs are unit-weighted and thus dominated by high-volume series. Per-series tests give an unweighted view, and price-weighted KPIs give the same conclusions [R §10.3]. Margins and costs are assumed for M5 and VN1.
8. **Case-study data.** The Vietnamese data may be incomplete (inventory equal to 216–485 weeks of sales in ten stores), sales fall sharply just before the test window, only one window is available, and the licence is listed as "Unknown" [R §10.4], [DP].
9. **Scope of models.** Deep global models trained from scratch (TiDE, DeepAR) were excluded for computational reasons, although TiDE was the strongest global model in Damato et al. (2026) [P12 p. 19].
10. **Literature coverage.** Two closely related works were available to us by title only (Theodorou et al., 2025; Li, 2026). Several cited studies are preprints [`02_related_work/paper_list.md`].
