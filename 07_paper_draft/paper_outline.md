# Paper Outline

> **Draft v0.1 (09/10/2026), English.** Step 11 of the course README. Each section is drafted in its own file, then merged into `08_final_submission/`.
>
> **Internal tags (remove before submission):**
>
> - `[P03 p. 2–3]` = paper 03 in `02_related_work/paper_list.md`, PDF page 2–3 (see `paper_summaries/paper_03.md`). `(abstract)` = taken from the abstract only.
> - `[R §4 T4]` = `06_experiment_results/results.md`, section 4, Table 4. `[CW26]` = `06_experiment_results/tables/comparison_w26.md`. `[CF]` = `tables/comparison_full.md`. `[ES]` = `06_experiment_results/experimental_setup.md`. `[DP]` = `code/outputs/data_profile.md`.
> - **[Nhận định nhóm]** = group interpretation, not a measured result or a claim of a cited paper.
> - **[Chưa kiểm chứng]** = not verified against a source we have read; must be checked before submission.
>
> **Writing rules:** numbers only from `06_experiment_results/` and `code/outputs/`; claims about other papers only with a page or "(abstract)"; Theodorou et al. (2025) and Li (2026) are cited **by title only** (full text not available); never write "no study has examined …" — use "limited attention" / "to the best of our knowledge".

## 0. Working title, keywords, target

**Title:** From Forecasts to Decisions: Benchmarking Probabilistic Demand Forecasts for Replenishment and Liquidation on Two Public Retail Datasets

**Short title:** Forecast-to-decision benchmark for retail replenishment and liquidation

**Keywords:** probabilistic forecasting; inventory management; intermittent demand; quantile regression; LightGBM; liquidation; M5; VN1

**Target:** Q3–Q4 journal in operations / supply-chain analytics. Length target: 8,000–10,000 words, 6–8 main tables/figures.

**Positioning sentence** (`04_proposed_system/system_overview.md` §7):

> This study does not propose a new forecasting model. It benchmarks existing probabilistic forecasting models inside a common, transparent replenishment-and-liquidation decision layer across two retail domains, and evaluates them with inventory KPIs by demand class.

## 1. Main messages (only results that hold in **both** test windows)

Source: `results.md` §0 and §10 (Table 11).

| # | Message | Evidence | Status |
|---|---|---|---|
| M1 | **M5:** LightGBM quantile regression (LGB-Q) is the most accurate method (mean SQL at h = 3: 0.208 / 0.215 in the two windows; best per-series mean rank) **and** needs the least inventory at equal fill rate: 4–13% less than the strong baselines at fill rate 0.94–0.96; HistGradientBoosting quantile (HGB-Q) is close behind | [R §1 T1], [R §2 T2], [R §4 T4–T5], [R §10 T11], [CW26] | Robust |
| M2 | **VN1 accuracy:** LGB-Q has the lowest **mean** SQL, but **per series** TSB with negative-binomial demand (TSB-NB) is on par (h = 3) or better (h = 13). The advantage of the ML models is robustness (fewer very large errors). Report mean **and** median / ranks | [R §2], [R §10 T11] | Robust |
| M3 | **VN1 aggregate inventory efficiency is period-dependent:** LGB-Q is best in the main window, TSB-NB in the second window. No method wins consistently | [R §4], [R §10] | Robust *as a finding of instability* |
| M4 | **VN1 by demand class (robust):** TSB-NB is most inventory-efficient for smooth series; LGB-Q for intermittent and lumpy series. Erratic: winner changes between windows | [R §5], [R §10 T11] | Robust (except erratic) |
| M5 | **Liquidation:** the quantile rule barely reduces fill rate; the fixed weeks-of-supply rule and the dead-stock rule lose fill rate or add stockout weeks (dead13: +61–67% stockout weeks for VN1 intermittent series). Break-even salvage ratio s\* ≈ 0.91–1.04 of unit cost for the quantile rule (VN1): within 26 weeks **no economic benefit of liquidation is demonstrated** | [R §7], [R §10] | Robust |
| M6 | **Cross-dataset consistency:** only the intermittent class has consistent method rankings between M5 and VN1 in both windows (ρ = 0.83–0.95). Do **not** claim that frontier-based rankings are more consistent in general | [R §6 T7], [R §10] | Robust (intermittent only) |

**Do not claim:** (i) LGB-Q is uniformly best on VN1; (ii) "better SQL implies less inventory" or its negation as a general law (may overlap with Theodorou et al., 2025, unread); (iii) liquidation is profitable; (iv) frontier rankings are more consistent across datasets.

## 2. Research questions

From `03_problem_and_gap/research_questions.md` (unchanged wording).

- **Main RQ:** How do probabilistic demand forecasting methods compare when their forecasts drive a common, transparent replenishment-and-liquidation policy in two public retail benchmarks with different settings, and how do the results differ across demand classes?
- **RQ1:** accuracy and cost-free inventory KPIs of 8 methods on M5 and VN1; do rankings hold across datasets?
- **RQ2:** variation across ADI–CV² classes; consistency of class-level patterns between M5 and VN1.
- **RQ3:** how much excess inventory a quantile-based liquidation rule removes vs. no liquidation, a fixed weeks-of-supply rule and a dead-stock rule; cost in stockouts; break-even salvage ratio.
- **RQ4:** sensitivity to τ, lead time L and liquidation horizon H (L, H grid on VN1 only).

## 3. Contributions (to be stated in the Introduction)

1. A reproducible **forecast-to-decision benchmark** on two public retail datasets of different settings (brick-and-mortar M5, multi-vendor e-commerce VN1) at weekly frequency, with 8 probabilistic methods feeding the same multi-period replenishment-and-liquidation policy; CPU-only, open code.
2. **All demand classes retained** and results reported by ADI–CV² class, including per-series statistical tests (Friedman–Nemenyi, Wilcoxon–Holm).
3. A **cost-free evaluation** protocol: inventory–fill-rate trade-off curves, inventory needed to reach a target fill rate, frontier rank, and a break-even salvage ratio for liquidation.
4. **Robustness evidence from two test windows**, which shows which conclusions are stable (M5; VN1 per-series accuracy; VN1 class-level results; liquidation) and which are period-dependent (VN1 aggregate efficiency).

## 4. Section plan

| § | File | Content | Approx. words | Main tables/figures |
|---|---|---|---|---|
| — | `abstract.md` | 200–250 words; written last | 250 | — |
| 1 | `introduction.md` | Problem; accuracy-focused benchmarks; intermittent demand; liquidation; gap; RQs; contributions; positioning sentence; paper structure | 1,200 | — |
| 2 | `related_work.md` | 2.1 Forecasting on M5/VN1; 2.2 Intermittent demand and demand classification; 2.3 Linking forecasts to inventory decisions; 2.4 Excess inventory and liquidation; 2.5 Positioning (comparison table) | 1,500 | Table A (positioning) |
| 3 | `methodology.md` §3 | Design; data and demand classes; forecasting target; 8 methods; decision layer; evaluation measures | 2,000 | Table 1 (datasets), Table 2 (methods) |
| 4 | `methodology.md` §4 | Rolling-origin design; scenarios; second test window; statistics; environment; runtime | 700 | (Table 2 cont.) |
| 5 | `results.md` | 5.1 Accuracy; 5.2 Per-series tests; 5.3 Trade-off and inventory at equal fill rate; 5.4 Demand classes; 5.5 Liquidation; 5.6 Sensitivity; 5.7 Robustness (second window) | 2,500 | Table 3–7, Fig. 1–2 |
| 6 | `discussion.md` | Practical implications; comparison with papers 11, 12, 21, 22; limitations | 1,300 | — |
| 7 | `conclusion.md` | Answers to RQs; future work | 500 | — |
| — | References | Below (§6) | — | — |
| App. | (later) | Default-scenario KPIs at τ = 0.9 ([R §3 T3]); full trade-off tables ([CF], [CW26]); Vietnamese footwear dataset (description only) | — | — |

## 5. Main tables and figures (8)

| No. | Content | Source | Section |
|---|---|---|---|
| Table 1 | Datasets: series, weeks, test window, zero share, demand-class counts | `05_methodology/dataset.md`, [ES §2] | 3.2 |
| Table 2 | The 8 forecasting methods and how each produces quantiles of D_h | `05_methodology/methodology.md` §5, `baseline.md` | 3.4 |
| Table 3 | Forecast accuracy: mean SQL (h = 3, 13), RMSSE, coverage of q = 0.9 | [R §1 T1] | 5.1 |
| Table 4 | Per-series mean ranks (SQL) and median SQL, M5 and VN1 | [R §2 T2] + median table | 5.2 |
| Fig. 1 | Inventory–fill-rate trade-off curves, M5 and VN1, main window | `06_experiment_results/figures/fig_tradeoff_M5.png`, `fig_tradeoff_VN1.png` | 5.3 |
| Table 5 | Inventory (weeks of demand) needed to reach fill rate 0.90–0.98, both windows | [R §4 T4], [CW26] | 5.3 |
| Table 6 | Frontier rank by demand class, VN1, both windows (+ M5 all) | [R §4 T5], [CW26] | 5.4 |
| Table 7 | Liquidation policies: inventory, liquidated share, Δfill, stockout weeks, s\* | [R §7 T8, §7.1, §7.2] | 5.5 |
| Fig. 2 | Trade-off curves, second window | `fig_tradeoff_M5_w26.png`, `fig_tradeoff_VN1_w26.png` | 5.7 |

## 6. References (draft)

Verified entries (Crossref / arXiv / publisher page, `02_related_work/paper_list.md`). Format to be adapted to the target journal.

- [P01] Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022a). The M5 competition: Background, organization, and implementation. *International Journal of Forecasting, 38*(4), 1325–1336. https://doi.org/10.1016/j.ijforecast.2021.07.007
- [P02] Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022b). M5 accuracy competition: Results, findings, and conclusions. *International Journal of Forecasting, 38*(4), 1346–1364. https://doi.org/10.1016/j.ijforecast.2021.11.013
- [P03] Makridakis, S., Spiliotis, E., Assimakopoulos, V., Chen, Z., Gaba, A., Tsetlin, I., & Winkler, R. L. (2022c). The M5 uncertainty competition: Results, findings and conclusions. *International Journal of Forecasting, 38*(4), 1365–1385. https://doi.org/10.1016/j.ijforecast.2021.10.009
- [P04] Feddersen, ?., & Cleophas, C. (2026). *(first author's initial to complete)* Interpretability and control in forecasting support systems. *Proceedings of HICSS 2026*. https://doi.org/10.24251/HICSS.2026.172
- [P06] Yang, Cao, & Liu (2025). Foundation models for demand forecasting via dual-strategy ensembling. KDD 2025 Workshop "AI for Supply Chain". arXiv:2507.22053. *(first names to complete)*
- [P08] Zanotti, M. (2025). The cost of ensembling: Is it always worth combining? arXiv:2506.04677.
- [P09] Salatiello, Birr, & Kunz (2025). Hierarchical time series forecasting via latent mean encoding. arXiv:2506.19633. *(first names to complete)*
- [P11] Wang, S., Kang, Y., Spiliotis, E., & Petropoulos, F. (2026). Multi-objective probabilistic forecast combination for inventory demand. arXiv:2606.04900.
- [P12] Damato, S., Rubattu, N., Azzimonti, D., & Corani, G. (2026). Intermittent time series forecasting: Local vs global models. arXiv:2601.14031.
- [P13] Zambon, Azzimonti, & Corani (2026). End-to-end probabilistic hierarchical forecasting of large hierarchies via probabilistic top-down. arXiv:2606.26774. *(first names to complete)*
- [P14] Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T.-Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems 30*. **[Chưa kiểm chứng: full author list — paper_list.md only gives "Ke et al."]**
- [P15] Croston, J. D. (1972). Forecasting and stock control for intermittent demands. *Operational Research Quarterly, 23*(3), 289–303. https://doi.org/10.1057/jors.1972.50
- [P16] Teunter, R. H., Syntetos, A. A., & Babai, M. Z. (2011). Intermittent demand: Linking forecasting to inventory obsolescence. *European Journal of Operational Research, 214*(3), 606–615. https://doi.org/10.1016/j.ejor.2011.05.018
- [P17] Salinas, D., Flunkert, V., Gasthaus, J., & Januschowski, T. (2020). DeepAR: Probabilistic forecasting with autoregressive recurrent networks. *International Journal of Forecasting, 36*(3), 1181–1191. https://doi.org/10.1016/j.ijforecast.2019.07.001 **[Chưa kiểm chứng: author list — paper_list.md only gives "Salinas et al."]**
- [P18] Syntetos, A. A., Boylan, J. E., & Croston, J. D. (2005). On the categorization of demand patterns. *Journal of the Operational Research Society, 56*(5), 495–503. https://doi.org/10.1057/palgrave.jors.2601841
- [P19] Kourentzes, N., Trapero, J. R., & Barrow, D. K. (2020). Optimising forecasting models for inventory planning. *International Journal of Production Economics, 225*, 107597. https://doi.org/10.1016/j.ijpe.2019.107597
- [P20] Theodorou, E., Spiliotis, E., & Assimakopoulos, V. (2025). Forecast accuracy and inventory performance: Insights on their relationship from the M5 competition data. *European Journal of Operational Research, 322*(2), 414–426. https://doi.org/10.1016/j.ejor.2024.12.033 *(cited by title only)*
- [P21] Zabraoui, O., Hmamou, Y., Chafi, A., & Kammouri Alami, S. (2025). A comparative study of multi-algorithm optimization for inventory analytics in supply chains. *Supply Chain Analytics, 12*, 100154. https://doi.org/10.1016/j.sca.2025.100154
- [P22] Mohammed, Z., Anas, C., & El Hammoumi, M. (2026). A hybrid learning framework for forecasting uncertainty and adaptive inventory planning in retail supply chains. *Supply Chain Analytics, 13*, 100180. https://doi.org/10.1016/j.sca.2025.100180
- [P23] Sfiris, D. S., & Koulouriotis, D. E. (2025). A new approach to forecast intermittent demand and stock-keeping-unit level optimization for spare parts management. *Applied Sciences, 15*(22), 12030. https://doi.org/10.3390/app152212030
- [P24] El-Meehy, A. O., El-Kharbotly, A. K., & El-Beheiry, M. M. (2026). Feature engineering for intermittent demand forecasting: Zero-detection and forecast performance across GRU, LSTM, and TCN architectures. *Journal of Intelligent Manufacturing*. https://doi.org/10.1007/s10845-026-02964-7
- [W1] van der Haar, J. F., Wellens, A. P., Boute, R. N., & Basten, R. J. I. (2024). Supervised learning for integrated forecasting and inventory control. *European Journal of Operational Research*. https://doi.org/10.1016/j.ejor.2024.07.004 **[Chưa kiểm chứng: author initials, volume/pages]**
- [W2] de Sousa, A. G. P. (2026). *From demand forecasting to replenishment simulation: A data-driven machine learning approach for fashion retail* (Master's thesis). University of Porto.
- [W3] Li, P. (2026). Forecasting for inventory decisions: A decision-regret benchmark for perishability-aware multi-echelon retail replenishment using the M5/Walmart data. SSRN. https://doi.org/10.2139/ssrn.7051299 *(cited by title only; not peer-reviewed)*
- [G22] Goltsos, T. E., Syntetos, A. A., Glock, C. H., & Ioannou, G. (2022). Inventory–forecasting: Mind the gap. *European Journal of Operational Research, 299*(2), 397–419. https://doi.org/10.1016/j.ejor.2021.07.040 *(abstract only)*
- [VN1] Vandeput, N. (2024). *VN1 Forecasting – Accuracy Challenge*. DataSource.ai. **[Chưa kiểm chứng: exact URL]**

Method references **not** in `02_related_work/` — all **[Chưa kiểm chứng]**, check on Crossref before use:

- Koenker, R., & Bassett, G. (1978). Regression quantiles. *Econometrica, 46*(1), 33–50.
- Hyndman, R. J., Koehler, A. B., Ord, J. K., & Snyder, R. D. (2008). *Forecasting with exponential smoothing: The state space approach*. Springer.
- Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830.
- Lei, J., G'Sell, M., Rinaldo, A., Tibshirani, R. J., & Wasserman, L. (2018). Distribution-free predictive inference for regression. *Journal of the American Statistical Association, 113*(523), 1094–1111.
- Demšar, J. (2006). Statistical comparisons of classifiers over multiple data sets. *Journal of Machine Learning Research, 7*, 1–30.
- Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics, 6*(2), 65–70.

## 7. Open items before submission

- [ ] Read Li (2026) and Theodorou et al. (2025). If either already covers liquidation or demand-class KPIs, re-position contributions 2–3.
- [ ] Check whether arXiv papers 08, 09, 11, 12, 13 have been formally published; cite the published version.
- [ ] Verify the [Chưa kiểm chứng] references above.
- [ ] Read Goltsos et al. (2022) and Kourentzes et al. (2020) in full before citing beyond the abstract / repository description.
- [ ] Add 2–3 papers from the target journal.
- [ ] Optional experiments (not run): L, H grid for M5; break-even for the second window; a third test window.
