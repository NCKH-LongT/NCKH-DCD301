# 1. Introduction

> Draft v0.2, English. Sources: `01_topic_proposal/topic_proposal.md`, `03_problem_and_gap/{problem_statement,research_gap,research_questions}.md`, `02_related_work/`, `06_experiment_results/results.md`. Tag conventions: `paper_outline.md`. Remove tags before submission.

Retailers face two opposite risks every week. With too little stock they lose sales and customers; with too much they tie up capital, pay holding costs and eventually have to discount or liquidate products. Deciding how much to order, and when to clear excess stock, requires knowing not only the expected demand but also its uncertainty. High quantiles of the demand distribution are commonly used to set safety stock [P03 p. 2]. Probabilistic forecasts are therefore the natural input to inventory decisions.

Public retail benchmarks have driven much of the recent progress in probabilistic demand forecasting, but they evaluate forecasts rather than decisions:

- The M5 competition measured accuracy with the weighted RMSSE and the weighted scaled pinball loss [P01 p. 3]. Its organisers state that it did not target a specific decision-making problem, so any quantile could be useful [P03 p. 2–3].
- LightGBM was used by all of the top 50 teams in the accuracy track [P02 p. 1], and the winner of the uncertainty track trained a separate gradient-boosting model for each quantile [P03 p. 14].
- Studies on the more recent VN1 e-commerce dataset also compare methods by accuracy and computational cost (Zanotti, 2025) [P08 p. 13–14].

Yet, in inventory settings, higher forecast accuracy does not necessarily lead to better decisions (Wang et al., 2026) [P11 (abstract)]. A structured review notes that much forecasting research treats the forecast as an end in itself rather than as an input to replenishment (Goltsos et al., 2022) [G22 (abstract)]. Theodorou et al. (2025) examined the relationship between forecast accuracy and inventory performance on the M5 data [P20 (title only)]. Meanwhile, pretrained time-series foundation models are entering demand forecasting (e.g. Yang et al., 2025) [P06 p. 4], but evidence on whether they improve inventory decisions on intermittent retail data is scarce [Nhận định nhóm].

Three features of retail data make the step from forecast to decision difficult.

1. **Most retail series are intermittent or lumpy.** In M5, 73% of the product–store series are intermittent and 17% lumpy at daily frequency [P01 p. 8]. Even at weekly frequency, 39.7% of M5 weeks and 69.9% of VN1 weeks have zero sales [DP]. Yet studies that link forecasts to inventory decisions on M5 often restrict themselves to selected series:
   - 8,000 high-volume series, which the authors call the main weakness of their study (Mohammed et al., 2026) [P22 p. 4, 18];
   - a subset of highly volatile food items (Zabraoui et al., 2025) [P21 p. 8].
2. **Excess stock must be handled, not only avoided.** Products reach the end of their life, and stock above any plausible future demand has to be cleared. To our knowledge, the forecast-to-inventory studies we reviewed in full text do not include a liquidation decision [Nhận định nhóm, based on a keyword search of papers 11 and 21–25; `03_problem_and_gap/research_gap.md` §2.3]. The TSB method links intermittent-demand forecasting to obsolescence, but was evaluated by simulation (Teunter et al., 2011) [P16 (abstract)].
3. **Conclusions from one dataset or one period may not transfer.**
   - The M5 organisers acknowledge limits to generalising beyond the data it represents [P01 p. 11].
   - The decision-oriented M5 studies cited above use only Walmart data; Mohammed et al. (2026) name testing on a single US retail setting as a limitation [P22 p. 17].
   - The closest study evaluates probabilistic forecast combinations in a single-period, single-product newsvendor setting, which its authors list as a limitation [P11 p. 26].
   - These studies evaluate a single test period [P11 p. 16], [P22 p. 4], [P21 p. 8] **[Chưa kiểm chứng: check that none of the three uses rolling or multiple test windows]**.

Limited attention has therefore been given to benchmarking probabilistic forecasting methods under a common, transparent replenishment-and-liquidation policy across different retail settings and periods, while retaining intermittent and lumpy demand and reporting inventory KPIs by demand class (`research_gap.md` §5). A further practical obstacle is that public datasets contain neither inventory positions nor unit costs, so cost-based evaluations depend on assumed cost parameters.

This study addresses this gap with a forecast-to-decision benchmark on two public retail datasets of different settings, both at weekly frequency:

- **M5:** one brick-and-mortar retailer, 30,490 product–store series;
- **VN1:** multi-vendor e-commerce, 15,053 client–warehouse–product series.

Eight probabilistic forecasting methods feed the same multi-period order-up-to policy with an optional liquidation rule. Four are statistical (empirical quantiles, ETS, and TSB with Poisson or negative-binomial demand). Four use gradient boosting (LightGBM quantile regression, LightGBM-Tweedie with normal safety stock or with conformal intervals, and HistGradientBoosting quantile regression).

We evaluate the methods without monetary units:

- KPIs: fill rate, stockout rate and inventory in weeks of demand;
- comparisons at equal fill rate along each method's inventory–fill-rate trade-off curve, with bootstrap confidence intervals;
- a break-even salvage ratio to summarise the economics of liquidation.

All analyses are reported by ADI–CV² demand class and repeated on three 26-week test windows. Two extensions complete the benchmark:

- a pretrained foundation model (Chronos-2) as a ninth method;
- a case study on a Vietnamese footwear retail chain, whose actual costs and prices allow liquidation to be valued in money.

This study does not propose a new forecasting model. It benchmarks existing probabilistic forecasting models inside a common, transparent replenishment-and-liquidation decision layer across retail settings, and evaluates them with inventory KPIs by demand class.

We address the following research questions:

- **RQ1.** Under a common multi-period quantile-based replenishment policy, how do the methods compare in forecast accuracy and in cost-free inventory KPIs on M5 and VN1, and do their rankings hold across datasets and test periods?
- **RQ2.** How does their relative performance vary across ADI–CV² demand classes, and are the class-level patterns consistent between M5 and VN1?
- **RQ3.** How much excess inventory does a quantile-based liquidation rule remove compared with no liquidation, a fixed weeks-of-supply rule and a dead-stock rule, at what cost in stockouts, and above which salvage-value ratio does liquidation pay off?
- **RQ4.** How sensitive are the rankings and recommendations to the target service level, the lead time and the liquidation horizon?

The contributions are as follows:

1. **A reproducible forecast-to-decision benchmark** on two public retail datasets from different settings, with one transparent decision layer for replenishment and liquidation. It runs on a laptop CPU and the code is open.
2. **A cost-free evaluation protocol with uncertainty quantification.** It combines trade-off curves, the inventory needed at a target fill rate, a frontier rank, bootstrap confidence intervals, and a break-even salvage ratio for liquidation.
3. **Robustness evidence.** All series are retained, results are reported by demand class with per-series statistical tests, and the whole benchmark is repeated on three test windows. This separates robust findings from period-dependent ones.
4. **Two extensions.**
   - A zero-shot foundation model (Chronos-2) in the same decision layer.
   - A case study on a Vietnamese footwear chain with actual unit costs, which values liquidation in money and illustrates the benchmark in an emerging-market retail setting.

The main findings are as follows:

- **M5:** LightGBM quantile regression is both the most accurate method and the one that needs the least inventory at equal fill rate, in all three windows. At a fill rate of 0.94 it needs 3–11% less inventory than the other strong baselines, and all bootstrap intervals exclude zero.
- **VN1, accuracy:** the same model has the lowest mean error, but TSB with negative-binomial demand is as accurate per series at a 3-week horizon and more accurate at 13 weeks, in every window. The ML advantage is robustness to rare large errors, not better forecasts for a typical series.
- **VN1, inventory:** the most inventory-efficient method depends on the period (LightGBM quantile in two of three windows); only lumpy series favour LightGBM quantile in every window.
- **Foundation model:** zero-shot Chronos-2 is never the most accurate or the most inventory-efficient method, and is 8–42 times slower on CPU.
- **Liquidation:** a quantile-based rule costs almost no service, whereas fixed and dead-stock rules raise stockouts. Within 26 weeks, however, no rule shows an economic benefit unless stock is salvaged near unit cost, which the case study confirms with actual costs.

The paper is organised as follows. Section 2 reviews related work. Section 3 describes the data, methods, decision layer and evaluation measures, and Section 4 the experimental setup. Section 5 reports the results, Section 6 discusses implications and limitations, and Section 7 concludes.
