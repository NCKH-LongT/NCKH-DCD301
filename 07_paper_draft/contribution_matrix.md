# Contribution matrix — how this study differs from the closest work

Every cell on prior work was checked against the paper itself on 26/10/2026 (PDFs in `papers_pdf/`; Wang et al. from
the arXiv full text). "—" = not part of that study's design.

| Aspect | Petropoulos et al. 2019 (IJF 35) [24] | Spiliotis et al. 2021 (IJPE 240) [23] | Theodorou et al. 2025 (EJOR 322) [7] | Wang et al. 2026 (arXiv 2606.04900) [5] | This study |
|---|---|---|---|---|---|
| Data | M3 monthly industry series | M5, 30,490 daily product–store series, 21 methods | M5, product–state level, 7,783 series (series with < 2.5 years dropped) | M5, 30,490 daily series; RAF spare parts | M5 (30,490 weekly product–store series), VN1 (15,053, multi-vendor e-commerce); all eligible series; independent footwear panel (909) |
| Inventory model | order-up-to, rolling simulation, several lead times | order-up-to with lost sales, review period and lead time of one day | order-up-to, 3 target service levels, 4 review periods, 2 lead times; holding, ordering and lost-sales costs | single-period, single-item newsvendor | weekly order-up-to with lost sales (L = 2), optional liquidation; lead times 1, 2, 4 |
| Test periods | rolling origins on M3 | one 28-day test set (last four weeks) | one 365-day simulation period | final 28 days (one holdout) | three 26-week windows per main dataset; one window for the footwear panel |
| Quantile construction | statistical methods (exponential smoothing, ARIMA, Theta, temporal aggregation) | empirical and model-based quantiles | from point forecasts and past forecast errors | linear pool of probabilistic forecasts | direct quantile models (LGB-Q, HGB-Q) alongside point + safety stock, conformal, statistical |
| Comparison basis | holding and backlog costs, order amplification, customer service levels | realised service levels and costs | costs and realised service at nominal targets | Pareto front of accuracy vs inventory cost | inventory at matched realised fill (retrospective) **and** with τ fixed before the test or calibrated weekly from past fill only (prospective) |
| Combination | combinations perform best | — | — | multi-objective weights, fixed validation window | pre-specified mean/median of seven methods, leave-one-out ablation, subset chosen on an earlier window |
| Validation of the combination | — | — | — | Walmart and RAF data, one holdout each | past-only calibration, cluster and full-policy bootstraps, independent panel; **not confirmed** |

## Core claims of this study and the evidence behind each

1. **Rankings by accuracy and by inventory agree in one setting and not in another, and the latter changes with the
   period.** Not shown before across two retail settings and three periods each: Theodorou et al. use one M5
   period; Wang et al. one holdout. Evidence: Tables 2–3 (M5: LGB-Q leads accuracy and inventory in every window;
   VN1: leader changes between windows), Section 5.3.
2. **Retrospective inventory savings need not survive deployment-style evaluation.** The matched-realised-fill
   comparison (as in [7, 25]) sets τ with test outcomes; we add past-only τ selection and calibration, paired
   full-policy bootstraps and an independent panel. Evidence: the 7–8 % VN1 saving of the pre-specified median at
   matched fill (Section 5.5) is not confirmed under these checks (Section 5.8, Table 7); M5 conclusions hold.

Supporting findings (robustness, not claimed as novel methods): demand classes and clusters do not select the
method in advance (Section 5.4); censoring scenarios (Section 6); break-even salvage ratio (Section 5.6).

What we do **not** claim: combining forecasts for inventory (shown by [24] and studied by [5]); evaluating forecasts
by inventory trade-off curves or at matched service (in [7, 25]); direct quantile LightGBM (M5 uncertainty
winner [3]).
