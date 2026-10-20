# From Forecasts to Decisions: Benchmarking Probabilistic Demand Forecasts for Retail Replenishment and Liquidation Across Settings and Periods

> Draft v3 (13/10/2026) for ICIIT 2027 — single column, at most 10 pages including figures, tables and references.
> Tables are generated in `v3_tables.md`; the numbers quoted in the text come from that file and from `06_experiment_results/phase2_*.md`.
> All runs are complete; no passage is pending.
> Author names, affiliations and the repository link are to be added.

## Abstract

Public retail forecasting benchmarks rank methods by forecast error, although forecasts are used to decide how much to stock. We benchmark seven probabilistic forecasting methods, three statistical and four based on gradient boosting, inside one transparent order-up-to policy with optional liquidation. The benchmark uses two public datasets from different retail settings, M5 (brick-and-mortar) and VN1 (multi-vendor e-commerce), keeps every eligible series and repeats all experiments on three 26-week test windows. Because the datasets contain no costs, methods are compared at equal fill rate along inventory–fill-rate trade-off curves, with bootstrap confidence intervals. On M5, LightGBM quantile regression is the most accurate method and needs 3–11% less inventory than point forecasts with safety stock, conformal quantiles, TSB and exponential smoothing in every window. On VN1 the most inventory-efficient method changes between windows. We trace this to demand dynamics: a negative-binomial TSB model needs 13–16% less inventory on series with stable demand in every window, whereas only the quantile model serves series whose demand grows sharply. Neither the ADI–CV² classes nor an unsupervised segmentation separates these series in advance, so group-wise method selection does not help. In a post hoc analysis, averaging the quantiles of LightGBM and TSB-NB hedges between the two: it needs 6–11% less inventory than LightGBM on VN1 at a fill rate of 0.92 in all three windows, stays within 1.5% of it on M5, and has the smallest worst-case regret (0.9% against 9.4%). A quantile-based liquidation rule costs almost no service, but under the assumed costs no rule pays off within 26 weeks.

**Keywords:** probabilistic forecasting; inventory management; intermittent demand; quantile regression; demand segmentation; liquidation; M5; VN1

## 1 Introduction

Retailers face two opposite risks. With too little stock they lose sales; with too much they tie up capital and eventually have to clear products at a loss. Setting stock levels requires the uncertainty of demand, not only its expected value, so quantile forecasts are the natural input to inventory decisions [3].

Public benchmarks have driven progress in probabilistic demand forecasting, but they score forecasts, not decisions [24]. The M5 competition used the weighted RMSSE and the weighted scaled pinball loss [1], and its organisers state that it did not target a specific decision problem [3]. Studies on the more recent VN1 e-commerce data also compare accuracy and computational cost [4]. Yet higher accuracy does not necessarily give better inventory decisions [5, 6, 23]. On M5, Theodorou et al. [7] report that the most accurate method may not be the best choice when lost-sales costs dominate, especially for intermittent products and short review periods and lead times, and call for replications on online retail data.

Three gaps remain. First, studies that link forecasts to inventory on M5 often keep only selected series, such as 8,000 high-volume series [8], a subset of volatile food items [9] or series with at least 2.5 years of history [7], although most retail series are intermittent. Second, they rely on one dataset and one test period [5, 7, 8, 9, 23], so it is unknown whether their conclusions transfer to another retail setting or another period. Third, public datasets contain neither costs nor inventory positions, so cost-based evaluations depend on assumed parameters, and cost-based and cost-free conclusions can disagree [7].

This paper addresses these gaps with a forecast-to-decision benchmark. It does not propose a new forecasting model. Our contributions are:

1. A reproducible benchmark of seven probabilistic forecasting methods inside one transparent replenishment-and-liquidation policy, on two public retail datasets from different settings, with all eligible series retained. It runs on a laptop CPU.
2. A cost-free evaluation protocol: methods are compared at equal realised fill rate along their trade-off curves, with bootstrap confidence intervals, and liquidation is summarised by a break-even salvage ratio.
3. Evidence on robustness. Everything is repeated on three test windows, which separates findings that hold in every window from period-dependent ones.
4. An explanation of the period dependence on e-commerce data. We show that it is associated with how much demand grows in the test period, that neither the standard demand classes nor an unsupervised segmentation anticipates this, and that group-wise method selection therefore does not help.
5. A simple hedge, identified post hoc: the average of the quantiles of the global quantile model and TSB-NB has the smallest worst-case regret in the six runs tested.

## 2 Related Work

**Retail forecasting benchmarks.** In the M5 accuracy track, LightGBM was used by all of the top 50 teams, and the winner combined LightGBM models trained with a Tweedie loss [2]. The winner of the uncertainty track trained a separate LightGBM model for each quantile [3]. These results motivate our main model and our point-forecast baseline. Zanotti [4] used M5 and VN1 to study the cost of ensembling global models; that study evaluates accuracy and computational cost, not inventory outcomes.

**Intermittent demand.** The TSB method updates a demand probability every period, which lets it react to obsolescence [10]. Demand is commonly classified by the average inter-demand interval (ADI) and the squared coefficient of variation of demand sizes (CV²) [11]; the thresholds 4/3 and 0.5 are used to describe M5 [1]. Damato et al. [12] compared local and global probabilistic models on intermittent data and concluded that no global architecture is established for such series.

**From forecasts to inventory decisions.** A structured review observes that most forecasting studies ignore the step from forecast to replenishment decision [6]. Kourentzes et al. [13] tune exponential smoothing with an inventory-based cost function and question whether forecast accuracy is a reasonable proxy for the decisions it supports. van der Haar et al. [14] learn order quantities end to end. Petropoulos et al. [24] simulate an order-up-to policy over rolling origins on M3 series and find that forecast combinations perform best. On M5, Spiliotis et al. [23] simulate one 28-day period with daily review and find that simple empirical quantile methods give better inventory performance than machine-learning methods; Wang et al. [5] evaluate probabilistic forecast combinations with a newsvendor rule in a single-period setting, which they list as a limitation; Zabraoui et al. [9] simulate inventory with reinforcement-learning policies on selected items; Mohammed et al. [8] evaluate safety stock with one illustrative cost calculation on high-volume series. The closest study is Theodorou et al. [7]. They simulate one year of an order-up-to policy with lost sales on 7,783 daily product–state series of M5, for 13 methods whose quantiles are point forecasts plus empirical quantiles of past errors, under 24 combinations of service level, review period and lead time. Trade-off curves broadly follow accuracy, but total costs that weight lost sales more than holding favour less accurate methods.

Our study differs from these works in combining two retail settings, all demand classes, a liquidation decision and three test windows. Compared with [7], we also use direct quantile models, and compare methods at equal realised fill rate rather than at equal target service level, at which [7] observe different realised service levels. Multi-period simulation [7, 9, 14] and decision-level evaluation [5, 7] are not new in themselves.

## 3 Method

### 3.1 Data

M5 [1] contains daily unit sales of 3,049 products in 10 Walmart stores (30,490 product–store series). We aggregate them to 277 complete weeks. VN1 [21] is a weekly e-commerce dataset with 15,053 client–warehouse–product series over 196 weeks; despite its name it is not Vietnamese data. A series is evaluated if it starts at least 13 weeks before the test period and has at least one sale before it.

**Table 1.** Datasets. Class shares and zero weeks refer to the history before the main test window.

| | M5 | VN1 |
|---|---|---|
| Setting | one retailer, 10 physical stores | multi-vendor e-commerce, 46 vendors, 328 warehouses |
| Series in panel / evaluated (main, second, third window) | 30,490 / 30,381, 29,917, 28,824 | 15,053 / 13,844, 11,442, 9,383 |
| Weeks | 277 | 196 |
| Zero weeks since series start | 24.4% | 49.1% |
| Smooth / erratic / intermittent / lumpy | 53.0 / 5.8 / 33.9 / 7.3% | 18.8 / 13.7 / 47.2 / 20.3% |
| Exogenous information | price, events, SNAP days, product hierarchy | price in weeks with sales only |

Both datasets pass through the same code; the one definitional difference, the series start, coincides for 99.5% of the M5 series. The datasets nevertheless contain different kinds of series: a classifier separates them with an AUC of 0.91 from nine demand features alone (see Section 5.7).

### 3.2 Forecasting target and methods

At each weekly origin, every method forecasts the quantiles q ∈ {0.5, 0.8, 0.9, 0.95, 0.99} of the cumulative demand over h weeks directly, with h = 3 for replenishment and h = 13 for liquidation. Weekly quantiles are not summed, because the quantile of a sum is not the sum of quantiles.

- **EMP**: empirical quantiles of rolling h-week sums over the last 104 weeks.
- **ETS**: simple exponential smoothing with a normal distribution for the h-week total [18].
- **TSB-NB**: TSB [10] with a negative-binomial distribution, a common choice for intermittent demand [25], matched to the mean and variance of the h-week total.
- **LGB-T**: a global LightGBM [15] point model with a Tweedie loss plus a normal safety stock from each series' validation residuals. This is the common "point forecast plus safety stock" practice.
- **LGB-C**: the same point model with split-conformal quantiles [17] pooled by demand class.
- **HGB-Q**: histogram gradient boosting [19] with a quantile loss, trained on a 300,000-row sample; a check that the results do not depend on one library.
- **LGB-Q**: LightGBM quantile regression [16], one global model per quantile (main model).

Section 5.5 adds **C2**, the mean of the LGB-Q and TSB-NB quantiles.

The four global models share features (lags, rolling means and standard deviations, zero share, weeks since the last sale, calendar, price, and a scale) and a target scaled by the series level. M5 adds events, SNAP days and the product hierarchy. Hyper-parameters are fixed; no model is tuned.

### 3.3 Decision layer

Each week, for every series: (1) the order placed L weeks earlier arrives; (2) the inventory position IP is on-hand plus on-order stock; (3) stock above a liquidation threshold T is liquidated; (4) an order max(S − IP, 0) is placed, with S the τ-quantile of demand over L + 1 weeks, unless stock was liquidated; (5) demand occurs and unmet demand is lost. The default lead time is L = 2 weeks.

Four liquidation policies use the same replenishment forecasts: none; **quantile** (T is the 0.95-quantile of 13-week demand from the same method); **fixed** (T is 26 times the mean weekly sales of the last 26 weeks); and **dead13** (a series without a sale in 13 weeks is liquidated completely and not replenished until it sells again).

### 3.4 Evaluation

*Accuracy.* The usual scaled quantile loss divides each series' pinball loss by its in-sample naive error. Its mean is unstable on VN1 (Section 5.1). We therefore report the volume-weighted quantile loss wQL (total pinball loss divided by total demand), the median per-series scaled loss, and mean per-series ranks with the Friedman test and the Nemenyi critical difference [20].

*Inventory.* Over the 22 test weeks after a 4-week warm-up we compute the fill rate (units sold / units demanded) and inventory in weeks of demand. At a fixed τ the methods reach different fill rates, so we run τ over the five quantile levels, draw each method's trade-off curve, a standard tool in inventory evaluations [7, 25], and interpolate the inventory needed to reach a target fill rate. The frontier rank is a method's mean rank of required inventory over the targets 0.90–0.98. Confidence intervals come from resampling series (200 resamples).

*Liquidation.* For each policy we compute the break-even salvage ratio s*, the minimum salvage price per unit cost at which liquidating is at least as profitable as holding, over holding costs of 10–40% per year and gross margins of 30–100%.

## 4 Experimental Setup

The last 26 weeks of a panel form the test period, in two 13-week blocks; models are retrained at the start of each block and every test week is a forecast origin. To test robustness we drop the last 26 and the last 52 weeks and repeat everything, including model training, on the preceding 26 weeks. This gives three test windows per dataset (main, second, third). All experiments ran on a laptop CPU (Intel Core i5-12450H, 16 GB RAM). Code and result files are available at [link to be added].

## 5 Results

### 5.1 Accuracy

*[Table 2 here — `v3_tables.md`]*

By volume-weighted loss, LGB-Q is the most accurate method in both datasets and all three windows, with HGB-Q within 0.002 (Table 2). It is also the best method in every demand class of both datasets and every window. On M5, per-series ranks agree: LGB-Q ranks first at h = 3 in every window, ahead of HGB-Q by more than the critical difference.

On VN1 the per-series view differs. At h = 3, LGB-Q, HGB-Q and TSB-NB are within 0.17 mean ranks, and LGB-Q and HGB-Q differ by less than the critical difference. At h = 13, TSB-NB ranks first in all three windows. The global models are thus not more accurate than TSB-NB for a typical VN1 series; their advantage in total loss comes from avoiding rare, very large errors. The mean scaled loss hides this: for LGB-Q on VN1 it is 0.336, 0.539 and 2.008 in the three windows, driven by a few series with a tiny naive error, whereas wQL is 0.103, 0.078 and 0.102.

### 5.2 Inventory at equal fill rate

**M5.** LGB-Q has the best frontier rank in every resample of every window. At a fill rate of 0.94 it needs 3.3–10.6% less inventory than LGB-T, LGB-C, TSB-NB and ETS, and every interval excludes zero (Table 3). HGB-Q is within 0.2–1.4%.

**VN1.** The answer depends on the window. In the main window LGB-Q has the best frontier rank, but its lead over LGB-T, LGB-C and TSB-NB at a fill rate of 0.94 is not significant. In the second window TSB-NB leads, and TSB-NB, LGB-T and LGB-C need 4.1–8.8% less inventory than LGB-Q. In the third window LGB-Q leads again, and TSB-NB, ETS and LGB-T cannot reach a fill rate of 0.94 at any τ. The lowest loss (LGB-Q in every window) does not reliably give the lowest inventory.

*[Figure 2 here — trade-off curves, main window: (a) M5, (b) VN1]*

*[Table 3 here]*

By demand class, LGB-Q leads on M5 in the smooth, intermittent and lumpy classes in every window. On VN1 only the lumpy class has the same leader (LGB-Q) in all three windows; the smooth class is led by TSB-NB in two windows and by LGB-C in the third.

### 5.3 Why VN1 depends on the period

*[Table 5 here]*

We split the series of each window by how their demand changed between the 26 weeks before the test period and the test period itself: stable (0.67–1.5 times) or growing (more than 1.5 times). This split uses realised demand, so it is descriptive and cannot guide decisions.

The pattern is the same in all three windows (Table 5). On VN1 series with stable demand, TSB-NB needs 13.3–15.6% less inventory than LGB-Q. On series whose demand grows, TSB-NB fails to reach a fill rate of 0.92 in two windows, whereas LGB-Q reaches it. The aggregate result follows the share of demand that comes from growing series: 31.5% and 40.4% in the windows where LGB-Q leads, and 22.8% in the window where TSB-NB leads. On M5, LGB-Q needs less inventory in both strata in every window.

### 5.4 Can a better grouping of series anticipate this?

*[Table 6 here]*

If growth were predictable from a series' history, a method could be chosen per group of series. Besides the ADI–CV² classes, we clustered the series of both datasets on eight pre-test features (level, order size, ADI, CV², weeks since the last sale, trend, recent relative level, peak size), fitted on the earliest window and applied unchanged later. A three-component Gaussian mixture (regular, fading and sparse segments) was selected among K-means and mixture models by criteria fixed in advance. It is stable (adjusted Rand index 0.94 between refits) but not well separated (silhouette 0.21).

Neither grouping helps to choose a method (Table 6). A rule that assigns each group the method that was most inventory-efficient for it in the previous window stays within 0.3% of LGB-Q on M5. On VN1 it saves 5.6% and then costs 5.1% with the classes, and saves nothing and then costs 10.5% with the segments. Even an oracle that knows the best method of each segment in the test window does no better than the best single method of that window, because within a window the same method leads in every segment. The reason is that the share of series that will grow is almost the same in every group: 18–31% in the three segments and 14–39% in the four ADI–CV² classes on VN1.

### 5.5 A combination hedges between the leaders

LGB-Q and TSB-NB fail on different series of VN1, so we average their quantiles (C2). This needs no prediction of growth. The pair was chosen after observing that the two methods alternate as leaders, so the analysis is not fully out of sample. At a fill rate of 0.92, C2 needs 5.9%, 10.5% and 7.1% less inventory than LGB-Q on VN1 in the three windows, and every interval excludes zero; in the second window it matches TSB-NB. On M5 it stays within 1.5% of LGB-Q. Its wQL is slightly higher than that of LGB-Q. In the main window C2 also needs 4.1% and 5.4% less inventory than LGB-Q on VN1 at a fill rate of 0.94 with lead times of one and four weeks.

### 5.6 Liquidation

*[Table 7 here]*

With LGB-Q forecasts, the quantile rule costs 0.02 percentage points of fill rate or less in every window and dataset (Table 7). On M5 it almost never triggers; on VN1 it reduces inventory by 1.7–7.4%. The fixed rule and the dead-stock rule lose more service: they raise the stockout rate by 5–20% and 10–23%.

Under our cost model, which is assumed rather than observed, no rule shows an economic benefit within 26 weeks. The break-even salvage ratio of the quantile rule on VN1 is 0.91–1.21 of unit cost, and that of the other rules is at or above 0.97.

### 5.7 Are the differences between the datasets artefacts?

We checked three possible artefacts (details in the repository). Re-weighting the VN1 series to match the feature distribution of M5 (mean standardised difference 0.32–0.39 reduced to 0.02–0.03) leaves the VN1 conclusions unchanged. Refitting the global models without price features on VN1, where prices are observed in less than half of the weeks, or on M5 with only the 21 features shared with VN1, changes the inventory needed by LGB-Q by less than 1% in every window. We therefore attribute the difference between the datasets to the retail settings rather than to data preparation.

## 6 Discussion

**Compare at equal service level and over several periods.** At τ = 0.9 the methods reach fill rates between 0.935 and 0.967 on M5, because each calibrates its quantiles differently. Comparing at equal τ rewards methods that under-cover. A single test period would have given a confident but wrong answer on VN1 in either direction, which bears out the caution of [7] that a simulated year gives no guarantee for the next.

**On e-commerce data the best method depends on what demand will do.** A well-specified statistical model is the more economical choice for series that continue as before, and a global quantile model is the only one that copes with series that take off. This is consistent with [7], who find on M5 that the most accurate method need not be the best when lost-sales costs dominate, especially for intermittent products; our results add that the divergence depends on the period and that it is not visible on M5 at the service levels we studied. With perfect knowledge of which series grow, using a global model for them and TSB-NB for the others would need 5.6–9.8% less inventory than LGB-Q on VN1; a rule that predicts growth from pre-test features recovers part of this but is unstable (details in the repository). The combination C2 obtains similar savings without any prediction.

**Direct quantiles matter.** Many studies, including [7], derive quantiles from point forecasts and past errors. On M5 this costs 3.3–8.2% more inventory at a fill rate of 0.94 than direct quantiles from the same LightGBM model (LGB-T and LGB-C in Table 3), which, besides the daily product–state level, may explain why [7] found LightGBM less accurate than simpler methods except at the longest horizon.

**C2 had the smallest worst-case regret.** We define the regret of a method in one run (dataset and window) as its excess inventory over the best single method, averaged over the fill targets it reaches. Over the six runs the largest regret is 0.9% for C2 and 9.4% for LGB-Q, the best single method, followed by LGB-T (9.5%, but it misses the highest targets in every run), HGB-Q (11.4%) and TSB-NB (20.7%). If a lost sale costs up to 200 weeks of holding, C2 stays within 3.1% of the cheapest single method in every run. For larger penalties all methods operate at τ = 0.99, where LGB-Q reaches the highest fill rate and C2 costs up to 29% more; unlike in [7], expensive lost sales then favour the most accurate method. As C2 was chosen after the main analysis, this is evidence from three windows, not a guarantee for deployment.

**Limitations.** Sales are used as demand, so historical stockouts are not visible. Hyper-parameters are not tuned, although the M5 conclusions hold under four LightGBM settings. At lead times of one and four weeks, checked in the main window only, the M5 conclusions hold at equal fill rate. The demand-shift analysis is ex post. Bootstrap intervals reflect variation across series, not across periods, so stability claims refer to the three windows tested; method rankings agree only weakly between the datasets. In the repository only, a zero-shot Chronos-2 [22] was less accurate than LGB-Q on 69–73% of the VN1 series and never the most inventory-efficient method.

## 7 Conclusion

We benchmarked seven probabilistic forecasting methods inside one replenishment-and-liquidation policy on two public retail datasets and three test windows. On brick-and-mortar data (M5) the conclusion holds in all three test windows: LightGBM quantile regression is the most accurate method and needs 3–11% less inventory than point forecasts with safety stock, conformal quantiles, TSB-NB and exponential smoothing at a fill rate of 0.94. On e-commerce data (VN1) the most inventory-efficient method changes with the period, because a statistical model is more economical for stable series while only the quantile model serves series whose demand grows sharply. Neither demand classes nor a segmentation anticipate this. Averaging the quantiles of LightGBM and TSB-NB hedges between them: in a post hoc analysis it needs 6–11% less inventory than LightGBM on VN1 at a fill rate of 0.92 in all three windows and stays within 1.5% of it on M5. A quantile-based liquidation rule is safe for service, but under the assumed costs liquidation pays off within 26 weeks only at salvage prices near unit cost. Future work should confirm the combination on new periods and datasets, extend the liquidation horizon, and test covariate-informed models.

## References

[1] S. Makridakis, E. Spiliotis, and V. Assimakopoulos. 2022. The M5 competition: Background, organization, and implementation. *International Journal of Forecasting* 38, 4, 1325–1336. https://doi.org/10.1016/j.ijforecast.2021.07.007

[2] S. Makridakis, E. Spiliotis, and V. Assimakopoulos. 2022. M5 accuracy competition: Results, findings, and conclusions. *International Journal of Forecasting* 38, 4, 1346–1364. https://doi.org/10.1016/j.ijforecast.2021.11.013

[3] S. Makridakis, E. Spiliotis, V. Assimakopoulos, Z. Chen, A. Gaba, I. Tsetlin, and R. L. Winkler. 2022. The M5 uncertainty competition: Results, findings and conclusions. *International Journal of Forecasting* 38, 4, 1365–1385. https://doi.org/10.1016/j.ijforecast.2021.10.009

[4] M. Zanotti. 2025. The cost of ensembling: Is it always worth combining? arXiv:2506.04677.

[5] S. Wang, Y. Kang, E. Spiliotis, and F. Petropoulos. 2026. Multi-objective probabilistic forecast combination for inventory demand. arXiv:2606.04900.

[6] T. E. Goltsos, A. A. Syntetos, C. H. Glock, and G. Ioannou. 2022. Inventory–forecasting: Mind the gap. *European Journal of Operational Research* 299, 2, 397–419. https://doi.org/10.1016/j.ejor.2021.07.040

[7] E. Theodorou, E. Spiliotis, and V. Assimakopoulos. 2025. Forecast accuracy and inventory performance: Insights on their relationship from the M5 competition data. *European Journal of Operational Research* 322, 2, 414–426. https://doi.org/10.1016/j.ejor.2024.12.033

[8] Z. Mohammed, C. Anas, and M. El Hammoumi. 2026. A hybrid learning framework for forecasting uncertainty and adaptive inventory planning in retail supply chains. *Supply Chain Analytics* 13, 100180. https://doi.org/10.1016/j.sca.2025.100180

[9] O. Zabraoui, Y. Hmamou, A. Chafi, and S. Kammouri Alami. 2025. A comparative study of multi-algorithm optimization for inventory analytics in supply chains. *Supply Chain Analytics* 12, 100154. https://doi.org/10.1016/j.sca.2025.100154

[10] R. H. Teunter, A. A. Syntetos, and M. Z. Babai. 2011. Intermittent demand: Linking forecasting to inventory obsolescence. *European Journal of Operational Research* 214, 3, 606–615. https://doi.org/10.1016/j.ejor.2011.05.018

[11] A. A. Syntetos, J. E. Boylan, and J. D. Croston. 2005. On the categorization of demand patterns. *Journal of the Operational Research Society* 56, 5, 495–503. https://doi.org/10.1057/palgrave.jors.2601841

[12] S. Damato, N. Rubattu, D. Azzimonti, and G. Corani. 2026. Intermittent time series forecasting: Local vs global models. arXiv:2601.14031.

[13] N. Kourentzes, J. R. Trapero, and D. K. Barrow. 2020. Optimising forecasting models for inventory planning. *International Journal of Production Economics* 225, 107597. https://doi.org/10.1016/j.ijpe.2019.107597

[14] J. F. van der Haar, A. P. Wellens, R. N. Boute, and R. J. I. Basten. 2024. Supervised learning for integrated forecasting and inventory control. *European Journal of Operational Research* 319, 2, 573–586. https://doi.org/10.1016/j.ejor.2024.07.004

[15] G. Ke, Q. Meng, T. Finley, T. Wang, W. Chen, W. Ma, Q. Ye, and T.-Y. Liu. 2017. LightGBM: A highly efficient gradient boosting decision tree. In *Advances in Neural Information Processing Systems 30*.

[16] R. Koenker and G. Bassett. 1978. Regression quantiles. *Econometrica* 46, 1, 33–50. https://doi.org/10.2307/1913643

[17] J. Lei, M. G'Sell, A. Rinaldo, R. J. Tibshirani, and L. Wasserman. 2018. Distribution-free predictive inference for regression. *Journal of the American Statistical Association* 113, 523, 1094–1111. https://doi.org/10.1080/01621459.2017.1307116

[18] R. Hyndman, A. Koehler, K. Ord, and R. Snyder. 2008. *Forecasting with Exponential Smoothing*. Springer. https://doi.org/10.1007/978-3-540-71918-2

[19] F. Pedregosa et al. 2011. Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.

[20] J. Demšar. 2006. Statistical comparisons of classifiers over multiple data sets. *Journal of Machine Learning Research* 7, 1–30.

[21] N. Vandeput. 2024. VN1 Forecasting – Accuracy Challenge. DataSource.ai.

[22] A. F. Ansari et al. 2025. Chronos-2: From univariate to universal forecasting. arXiv:2510.15821.

[23] E. Spiliotis, S. Makridakis, A. Kaltsounis, and V. Assimakopoulos. 2021. Product sales probabilistic forecasting: An empirical evaluation using the M5 competition data. *International Journal of Production Economics* 240, 108237. https://doi.org/10.1016/j.ijpe.2021.108237

[24] F. Petropoulos, X. Wang, and S. M. Disney. 2019. The inventory performance of forecasting methods: Evidence from the M3 competition data. *International Journal of Forecasting* 35, 251–265. https://doi.org/10.1016/j.ijforecast.2018.01.004

[25] M. Z. Babai, M. M. Ali, and K. Nikolopoulos. 2012. Impact of temporal aggregation on stock control performance of intermittent demand estimators: Empirical analysis. *Omega* 40, 713–721. https://doi.org/10.1016/j.omega.2011.09.004
