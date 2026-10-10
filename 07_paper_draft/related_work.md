# 2. Related Work

> Draft v0.2, English. Sources: `02_related_work/literature_review_matrix.md`, `paper_summaries/`, `03_problem_and_gap/research_gap.md`. Every claim about another paper carries a page or "(abstract)". Papers 20 (Theodorou et al., 2025) and W3 (Li, 2026) are cited **by title only**. Tag conventions: `paper_outline.md`.

## 2.1 Probabilistic forecasting on public retail benchmarks

**M5.** The M5 competition released 42,840 hierarchical Walmart sales series, with 30,490 series at the product–store level [P01 p. 6]. It had an accuracy track scored by WRMSSE and an uncertainty track scored by WSPL [P01 p. 3].

- *Accuracy track:* LightGBM was used by all of the top 50 teams [P02 p. 1]. The winner averaged 220 LightGBM models trained with a Tweedie loss [P02 p. 9] and beat the best benchmark by 22.4% [P02 p. 5–6]. Simple exponential smoothing remained competitive at the product and product–store levels [P02 p. 2].
- *Uncertainty track:* participants forecast nine quantiles [P03 (abstract)]. The winning team trained a separate LightGBM model for each quantile and aggregation level, 126 models in total [P03 p. 14].

These results motivate our choice of LightGBM quantile regression as the main model and of LightGBM-Tweedie as a baseline.

**Later work** on M5 continued to optimise forecast accuracy:

- hierarchical and architectural ensembles of LightGBM, deep and foundation models (Yang et al., 2025) [P06 p. 3–4];
- temporal-hierarchy encoders (Salatiello et al., 2025) [P09 p. 4];
- end-to-end probabilistic top-down reconciliation with ETS on a few aggregate series (Zambon et al., 2026). This method would have ranked 11th of 892 teams in the uncertainty track and runs in under five minutes on a laptop [P13 p. 25].

**VN1.** VN1 is a weekly e-commerce dataset of 15,053 products [P08 p. 7]. Zanotti (2025) used M5 and VN1 to study the cost of ensembling ten global models with point and quantile losses. Small ensembles of two or three models were often near-optimal, and less frequent retraining cut cost with little loss of accuracy [P08 (abstract)]. That study evaluates accuracy (RMSSE, scaled quantile loss) and computational cost, not inventory outcomes [P08 p. 13–14].

**Foundation models.** Pretrained time-series models are now used in demand forecasting. Yang et al. (2025) include Chronos and TEMPO among the backbones of their ensembles on M5 and three other retail datasets [P06 p. 4]. They note that the interpretability of ensemble results remains an open challenge for decision making [P06 p. 7]. Damato et al. (2026) leave the comparison with pretrained models on intermittent data to future work [P12 p. 2]. Chronos-2 is a recent pretrained model with quantile outputs and native covariate support (Ansari et al., 2025; model card) **[Chưa kiểm chứng: technical report not read]**. To our knowledge, such models have not been evaluated inside an inventory decision layer on intermittent retail data [Nhận định nhóm].

In short, the main public retail benchmarks rank methods by forecast error. The M5 organisers note that the competition did not target a specific decision problem [P03 p. 2–3], and that its conclusions are limited in how far they generalise beyond the data it represents [P01 p. 11].

## 2.2 Intermittent demand and demand classification

**Classical methods.** Croston's method forecasts demand size and inter-demand interval separately (Croston, 1972) [P15 via P23 p. 1–2]. It is positively biased, which motivated the SBA correction [P16 (abstract)]. TSB (Teunter et al., 2011) replaces the interval with a demand probability that is updated every period. This makes it unbiased and lets it react to obsolescence [P16 (abstract)], [P23 p. 2].

**Demand classes.** Syntetos et al. (2005) derived a classification by the average inter-demand interval (ADI) and the squared coefficient of variation of demand sizes (CV²) to guide method selection [P18 (abstract)]. Makridakis et al. (2022a) report the thresholds ADI = 4/3 and CV² = 0.5 and use them to describe M5 [P01 p. 7–8]. They also note that the thresholds were originally meant to compare specific methods [P01 p. 8]. Damato et al. (2026) likewise stress that the thresholds are not a definition of intermittency [P12 p. 10]. Inventory studies on M5 report class shares [P22 p. 4] but evaluate inventory only in aggregate [P22 p. 15].

**Global models.** Damato et al. (2026) compared local and global probabilistic models on five intermittent datasets with more than 40,000 series [P12 (abstract)].

- TiDE was the most accurate global model, and a Tweedie output gave the best high quantiles [P12 p. 19].
- Gradient-boosted trees used in a *distributional* form, predicting distribution parameters rather than quantiles [P12 p. 6], were not competitive and were dropped from the analysis [P12 p. 13, 19].
- The authors conclude that no global architecture is established for intermittent series [P12 p. 2].

Our main model differs from theirs: it uses LightGBM *quantile regression*, as the M5 uncertainty winner did [P03 p. 14]. Their finding is nevertheless a reason to check the main model against TSB and against a second gradient-boosting implementation.

**Metrics.** For intermittent data, MAPE is undefined when demand is zero [P24 p. 4]. El-Meehy et al. (2026) further show that forecasting zero periods well is associated with lower inventory but more shortages [P24 p. 21]. This is a first sign that accuracy and inventory outcomes can pull in different directions.

## 2.3 From forecasts to inventory decisions

**Reviews and integrated approaches.**

- *Review.* A structured review of the inventory–forecasting interface proposes four levels of integration and observes that most forecasting studies ignore the step from forecast to replenishment decision (Goltsos et al., 2022) [G22 (abstract)].
- *Inventory-based parameter tuning.* Kourentzes et al. (2020) optimise the parameters of forecasting models with inventory metrics instead of statistical error measures [P19 (repository description)].
- *End-to-end learning.* van der Haar et al. (2024) learn order quantities directly with a supervised, end-to-end loss, for settings including lost sales [W1 (abstract)].

In contrast, we keep forecast and decision separate and use a transparent quantile-based policy. This lets one decision layer be fed by any probabilistic forecast.

**Studies on M5.**

- *Wang et al. (2026)* is the closest study. It combines four probabilistic models (two bootstrap, Poisson and negative binomial) with multi-objective optimisation [P11 p. 9–10, 14]. It sets the order-up-to level at the critical-ratio quantile of a newsvendor problem [P11 p. 11], with cost ratios equivalent to service levels of 80%, 90% and 95% [P11 p. 16]. It evaluates on 28,903 M5 series after removing 1,587 series without history [P11 p. 17]. No single method dominated in every scenario [P11 p. 18]. The authors list the single-period, single-product setting as a limitation [P11 p. 26].
- *Zabraoui et al. (2025)* simulate 365 days of inventory on a selected subset of volatile M5 food items. They compare reinforcement learning, genetic algorithms, deep learning and heuristics, and their GA–DQN hybrid raises the service level to 94% [P21 p. 8, 16]. The authors note the training cost and the low interpretability of deep reinforcement learning, and assume fixed lead times [P21 p. 19].
- *Mohammed et al. (2026)* build a stacked ensemble with GARCH-based intervals on 8,000 high-volume M5 series [P22 p. 4]. Their inventory evaluation is one illustrative calculation: a 11.8% lower expected cost than a fixed-quantile policy [P22 p. 15]. They name the omission of intermittent, slow-moving items as the main weakness and suggest quantile regression on intermittent series as future work [P22 p. 18–19].

**Related benchmarks we could not read.** Theodorou et al. (2025) studied the relationship between forecast accuracy and inventory performance on the M5 data [P20 (title only)]. Li (2026) proposed a decision-regret benchmark for perishability-aware multi-echelon replenishment on M5 [W3 (title only)]. Because we could not read either paper, we do not make claims about their methods or findings. We also do not pose the general accuracy–inventory relationship as a research question.

**Other domains.**

- Sfiris and Koulouriotis (2025) link intermittent-demand forecasts to an (R, Q) policy for 2,050 automotive spare parts. They report lower safety stock at the same service level [P23 p. 14, 26], with a fixed lead time as a stated limitation [P23 p. 25].
- de Sousa (2026) simulates replenishment from LightGBM/XGBoost forecasts for one fashion retailer [W2 (abstract)].

## 2.4 Excess inventory and liquidation

Excess stock is a recurring practical problem. For example, Putra and Purnomo (2026) report average end-of-period stock far above safety stock for many power-plant spare parts [P25 p. 7]. TSB was motivated partly by obsolescence [P16 (abstract)]. However, we searched the full texts of papers 11 and 21–25 for "liquidation", "markdown", "clearance", "salvage", "disposal", "write-off" and "obsolete". The terms appear only in reference lists or overview tables; none of these studies includes a liquidation decision (`research_gap.md` §2.3). The abstracts of W1 and W2 do not mention one either. Within the literature we reviewed, the reverse decision of clearing stock has thus received little attention alongside replenishment [Nhận định nhóm].

## 2.5 Positioning

**Table A.** Positioning against the closest studies. ✓ = yes, ✗ = no, "—" = not applicable. Entries for papers 11, 21 and 22 are based on full texts. Papers 20 and W3 are omitted because they were not read.

| | Wang et al. (2026) [P11] | Zabraoui et al. (2025) [P21] | Mohammed et al. (2026) [P22] | Zanotti (2025) [P08] | This study |
|---|---|---|---|---|---|
| Datasets | M5 + RAF spare parts | M5 subset | M5, 8,000 high-volume series | M5 + VN1 | M5 + VN1 |
| Intermittent series retained | ✓ (excl. 1,587 without history) | ✗ (selected volatile items) | ✗ | ✓ | ✓ (all classes) |
| Inventory evaluation | newsvendor, single period | 365-day simulation | one illustrative calculation | ✗ (accuracy only) | multi-period simulation with lead time |
| Liquidation decision | ✗ | ✗ | ✗ | — | ✓ (quantile, fixed, dead-stock) |
| Results by ADI–CV² class | ✗ | ✗ | ✗ (shares only) | — | ✓ |
| Cost-free KPIs / trade-off | cost ratios ↔ τ | costs | costs | — | ✓ (frontier, break-even salvage) |
| Policy transparency | quantile policy | RL (low interpretability, p. 19) | quantile + GARCH | — | quantile policy |
| Test periods | one evaluation period (28 days) | 365-day simulation | one 75/25 split | — (accuracy only) | three 26-week windows, rolling weekly origins |
| Foundation model in the comparison | ✗ | ✗ | ✗ | ✗ | ✓ (Chronos-2, zero-shot) |
| Actual unit costs from data | ✗ (cost ratios) | ✗ (assumed cost parameters) | ✗ (assumed cost parameters) | — | ✓ in the case study (VNF) |

Sources: [P11 p. 11, 16, 17, 26], [P21 p. 5, 8, 19], [P22 p. 4, 15, 18], [P08 p. 4, 13–14]. Test periods: P11 p. 16 (evaluation on the last 28 days), P22 p. 4 (75:25 split), P21 p. 8 (365-day simulation). Cost parameters: P21 p. 5 (cost function), P22 p. 15 (holding 0.50, shortage 5.00), P11 p. 16 (c₂ ∈ {4, 9, 19}).

Multi-period simulation alone is not new (Zabraoui et al., 2025; van der Haar et al., 2024), nor is decision-level evaluation (Wang et al., 2026). Our contribution lies in combining the following elements [Nhận định nhóm]:

- two public retail settings;
- all demand classes, reported by class;
- a two-sided decision layer (replenishment and liquidation);
- a cost-free evaluation with bootstrap uncertainty;
- three test windows;
- a foundation-model check;
- a case study with actual unit costs.
