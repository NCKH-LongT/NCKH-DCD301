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

**Title:** From Forecasts to Decisions: Benchmarking Probabilistic Demand Forecasts for Replenishment and Liquidation on Public Retail Data

**Short title:** Forecast-to-decision benchmark for retail replenishment and liquidation

**Keywords:** probabilistic forecasting; inventory management; intermittent demand; quantile regression; LightGBM; foundation models; liquidation; M5; VN1

**Target:** Q3–Q4 journal in operations / supply-chain analytics. Check on 10/10/2026: *Supply Chain Analytics* (journal of papers 21–22) is listed as Q1 (SJR 2024 = 0.896) by aggregator sites citing SCImago (resurchify.com, scijournal.org; SCImago itself not reached), so it is a stretch target, not Q3–Q4. Candidates whose scope includes demand forecasting and inventory control, quartile **[Chưa kiểm chứng]** on scimagojr.com: *Operations and Supply Chain Management: An International Journal* (ISSN 1979-3561; JCR Q3 per journalmetrics.org); *Journal of Industrial Engineering and Management* (ISSN 2013-0953; Q2 per resurchify.com). Final choice: group decision. Length target: 9,000–11,000 words with about 10 main tables/figures; long tables go to the Appendix.

**Positioning sentence** (`04_proposed_system/system_overview.md` §7):

> This study does not propose a new forecasting model. It benchmarks existing probabilistic forecasting models inside a common, transparent replenishment-and-liquidation decision layer across retail settings, and evaluates them with inventory KPIs by demand class.

## 1. Main messages (only results that hold across the three test windows)

Source: `06_experiment_results/results.md` §10–10.5 (Tables 11–14); draft `results.md` Table 8.

| # | Message | Evidence | Status |
|---|---|---|---|
| M1 | **M5:** LGB-Q is the most accurate method and needs the least inventory at equal fill rate in all three windows (P(best) = 1.00): 3–11% less than LGB-T, LGB-C, TSB-NB and ETS at fill rate 0.94, all bootstrap CIs excluding zero; HGB-Q within 0–1.5% | [R §10.1, §10.2] | Robust |
| M2 | **VN1 accuracy:** LGB-Q has the lowest **mean** SQL in every window, but the mean is unstable (0.336 / 0.539 / 2.008) while medians are stable; **per series** TSB-NB is on par at h = 3 and better at h = 13 in every window | [R §2, §10.1] | Robust |
| M3 | **VN1 aggregate inventory efficiency is period-dependent:** LGB-Q best in 2 of 3 windows (main-window lead not significant vs LGB-T, LGB-C, TSB-NB); TSB-NB significantly better in the second window | [R §10.1, §10.2] | Robust *as a finding of instability* |
| M4 | **VN1 by class:** LGB-Q is most inventory-efficient on lumpy series in every window and on intermittent series where rankable; smooth and erratic leaders change | [R §10.1 T12] | Robust (lumpy, intermittent) |
| M5 | **Mechanism:** on VN1 intermittent series LGB-Q has a lower pinball loss than TSB-NB on only 24–34% of series at every quantile, but a lower mean loss; its advantage is avoiding rare large errors | [R §2.1, §10.1] | Robust |
| M6 | **Liquidation:** the quantile rule costs about 0.02 pp fill rate in every window; fixed and dead-stock rules lose fill rate or add stockout weeks (dead13: +43% to +68% for VN1 intermittent); s\* ≈ 0.91–1.04 (VN1) and 0.90–1.01 with actual costs (VNF): **no economic benefit within 26 weeks** | [R §7, §10.1, §10.4] | Robust |
| M7 | **Foundation model:** zero-shot Chronos-2 is never best (accuracy or inventory), even on M5 (in its training data); 8–42 times slower on CPU | [R §10.5] | One M5 window, three VN1 windows, VNF |
| M8 | **Case study (VNF):** LGB-Q most inventory-efficient (P(best) = 0.91) although TSB-P has the lowest mean SQL; data caveats | [R §10.4] | Illustration only |
| M9 | **Cross-dataset consistency:** only the intermittent class has consistent rankings by fill rate between M5 and VN1 in every window (ρ = 0.83–0.93) | [R §6, §10, §10.1] | Robust (intermittent only) |

**Do not claim:** (i) LGB-Q is uniformly best on VN1; (ii) "better SQL implies less inventory" or its negation as a general law (may overlap with Theodorou et al., 2025, unread); (iii) liquidation is profitable; (iv) frontier rankings are more consistent across datasets; (v) TSB-NB is best on smooth VN1 series; (vi) foundation models in general are worse (one model, one usage design); (vii) case-study results generalise.

## 2. Research questions

From `03_problem_and_gap/research_questions.md`, with "and test periods" added to RQ1.

- **Main RQ:** How do probabilistic demand forecasting methods compare when their forecasts drive a common, transparent replenishment-and-liquidation policy in public retail benchmarks with different settings, and how do the results differ across demand classes?
- **RQ1:** accuracy and cost-free inventory KPIs on M5 and VN1; do rankings hold across datasets and test periods?
- **RQ2:** variation across ADI–CV² classes; consistency of class-level patterns between M5 and VN1.
- **RQ3:** how much excess inventory a quantile-based liquidation rule removes vs. no liquidation, a fixed weeks-of-supply rule and a dead-stock rule; cost in stockouts; break-even salvage ratio.
- **RQ4:** sensitivity to τ, lead time L and liquidation horizon H (L, H, q_L, k grid on the main window of M5 and VN1).

## 3. Contributions (as stated in the Introduction)

1. A reproducible **forecast-to-decision benchmark** on two public retail datasets of different settings, with one transparent replenishment-and-liquidation layer; CPU-only, open code.
2. A **cost-free evaluation protocol with uncertainty**: trade-off curves, inventory at target fill rate, frontier rank, bootstrap CIs, break-even salvage ratio.
3. **Robustness evidence**: all series retained, results by demand class with per-series tests, three test windows.
4. **Two extensions**: a zero-shot foundation model (Chronos-2) and a Vietnamese footwear case study with actual costs.

## 4. Section plan

| § | File | Content | Main tables/figures |
|---|---|---|---|
| — | `abstract.md` | About 250 words | — |
| 1 | `introduction.md` | Problem; accuracy-focused benchmarks; foundation models; three difficulties; gap; RQs; contributions; findings | — |
| 2 | `related_work.md` | 2.1 Benchmarks and foundation models; 2.2 Intermittent demand; 2.3 Forecasts to inventory; 2.4 Liquidation; 2.5 Positioning | Table A |
| 3 | `methodology.md` §3 | Design; data (M5, VN1, VNF); target; methods incl. Chronos-2; decision layer; measures incl. bootstrap and actual-cost s\* | Tables 1, 2 |
| 4 | `methodology.md` §4 | Rolling origin; scenarios; three windows; environment; runtime; reproducibility | Table 2b |
| 5 | `results.md` | 5.1–5.6 main benchmark; 5.7 robustness; 5.8 Chronos-2; 5.9 case study | Tables 3–10, Figs. 2–3 |
| 6 | `discussion.md` | Findings; implications; comparison with papers 11, 12, 21, 22; limitations | — |
| 7 | `conclusion.md` | Answers to RQs; extensions; future work | — |
| App. | (to write) | A1 default-scenario KPIs (τ = 0.9); A2 Tweedie fix; A3 per-quantile loss tables; A4 full inventory-at-fill-rate tables by class and window; A5 value-weighted CIs; A6 VNF data preparation | — |

## 5. Main tables and figures

| No. | Content | Source | Section |
|---|---|---|---|
| Fig. 1 | Benchmark pipeline (`code/make_pipeline_figure.py`) | `06_experiment_results/figures/fig_pipeline.png` | 3.1 |
| Table 1 | Datasets incl. VNF and three test windows | `05_methodology/dataset.md`, [ES §2], [R §10.1, §10.4] | 3.2 |
| Table 2 | Forecasting methods (8 + Chronos-2) | `05_methodology/baseline.md`, `code/f2d/models.py` | 3.4 |
| Table 2b | Runtime | [ES §4], [R §10.5] | 4.4 |
| Table 3 | Accuracy, main window | [R §1 T1] | 5.1 |
| Table 4 | Per-series ranks, three windows | `code/outputs/*/stat_tests.csv` | 5.2 |
| Fig. 2 | Trade-off curves, main window | `06_experiment_results/figures/fig_tradeoff_{M5,VN1}.png` | 5.3 |
| Table 5 | Inventory at fill 0.94 with bootstrap CIs, three windows | [R §10.2], `equal_fill_ci*.csv` | 5.3 |
| Table 6 | Frontier rank by class, three windows | `equal_fill_ci*.csv` | 5.4 |
| Table 7 | Liquidation policies | [R §7] | 5.5 |
| Table 8 | Robustness summary | [R §10, §10.1] | 5.7 |
| Fig. 3 | Trade-off curves, second and third windows | `fig_tradeoff_*_w26.png`, `code/outputs/fig_tradeoff_*_w52.png` | 5.7 |
| Table 9 | Chronos-2 vs LGB-Q | [R §10.5] | 5.8 |
| Table 10 | VNF case study | [R §10.4] | 5.9 |

## 6. References (draft)

Format to be adapted to the target journal. **Status 09/10/2026:** every entry below was checked against Crossref, the arXiv abstract page, or the publisher page (JMLR, NeurIPS). The source of each check is given in brackets; entries without brackets were checked earlier (`02_related_work/paper_list.md`).

- [P01] Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022a). The M5 competition: Background, organization, and implementation. *International Journal of Forecasting, 38*(4), 1325–1336. https://doi.org/10.1016/j.ijforecast.2021.07.007
- [P02] Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022b). M5 accuracy competition: Results, findings, and conclusions. *International Journal of Forecasting, 38*(4), 1346–1364. https://doi.org/10.1016/j.ijforecast.2021.11.013
- [P03] Makridakis, S., Spiliotis, E., Assimakopoulos, V., Chen, Z., Gaba, A., Tsetlin, I., & Winkler, R. L. (2022c). The M5 uncertainty competition: Results, findings and conclusions. *International Journal of Forecasting, 38*(4), 1365–1385. https://doi.org/10.1016/j.ijforecast.2021.10.009
- [P04] Feddersen, L., & Cleophas, C. (2026). Interpretability and control in forecasting support systems. In *Proceedings of the 59th Hawaii International Conference on System Sciences*. https://doi.org/10.24251/HICSS.2026.172 [Crossref]
- [P06] Yang, W., Cao, D., & Liu, Y. (2025). Foundation models for demand forecasting via dual-strategy ensembling. KDD 2025 Workshop "AI for Supply Chain: Today and Future". arXiv:2507.22053. [arXiv, v1 only, no journal-ref]
- [P08] Zanotti, M. (2025). The cost of ensembling: Is it always worth combining? arXiv:2506.04677. [arXiv v2, 9 Jul 2025, no journal-ref]
- [P09] Salatiello, A., Birr, S., & Kunz, M. (2025). Hierarchical time series forecasting via latent mean encoding. arXiv:2506.19633. [arXiv, v1 only, no journal-ref]
- [P11] Wang, S., Kang, Y., Spiliotis, E., & Petropoulos, F. (2026). Multi-objective probabilistic forecast combination for inventory demand. arXiv:2606.04900. [arXiv, v1 only, no journal-ref]
- [P12] Damato, S., Rubattu, N., Azzimonti, D., & Corani, G. (2026). Intermittent time series forecasting: Local vs global models. arXiv:2601.14031. [arXiv v2, 10 Jun 2026; comment "Submitted to the Journal of the Operational Research Society"]
- [P13] Zambon, L., Azzimonti, D., & Corani, G. (2026). End-to-end probabilistic hierarchical forecasting of large hierarchies via probabilistic top-down. arXiv:2606.26774. [arXiv v2, 30 Jul 2026, no journal-ref]
- [P14] Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T.-Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. In *Advances in Neural Information Processing Systems 30* (NIPS 2017). [NeurIPS proceedings page]
- [P15] Croston, J. D. (1972). Forecasting and stock control for intermittent demands. *Operational Research Quarterly, 23*(3), 289–303. https://doi.org/10.1057/jors.1972.50
- [P16] Teunter, R. H., Syntetos, A. A., & Babai, M. Z. (2011). Intermittent demand: Linking forecasting to inventory obsolescence. *European Journal of Operational Research, 214*(3), 606–615. https://doi.org/10.1016/j.ejor.2011.05.018
- [P17] Salinas, D., Flunkert, V., Gasthaus, J., & Januschowski, T. (2020). DeepAR: Probabilistic forecasting with autoregressive recurrent networks. *International Journal of Forecasting, 36*(3), 1181–1191. https://doi.org/10.1016/j.ijforecast.2019.07.001 [Crossref]
- [P18] Syntetos, A. A., Boylan, J. E., & Croston, J. D. (2005). On the categorization of demand patterns. *Journal of the Operational Research Society, 56*(5), 495–503. https://doi.org/10.1057/palgrave.jors.2601841
- [P19] Kourentzes, N., Trapero, J. R., & Barrow, D. K. (2020). Optimising forecasting models for inventory planning. *International Journal of Production Economics, 225*, 107597. https://doi.org/10.1016/j.ijpe.2019.107597
- [P20] Theodorou, E., Spiliotis, E., & Assimakopoulos, V. (2025). Forecast accuracy and inventory performance: Insights on their relationship from the M5 competition data. *European Journal of Operational Research, 322*(2), 414–426. https://doi.org/10.1016/j.ejor.2024.12.033 *(cited by title only)*
- [P21] Zabraoui, O., Hmamou, Y., Chafi, A., & Kammouri Alami, S. (2025). A comparative study of multi-algorithm optimization for inventory analytics in supply chains. *Supply Chain Analytics, 12*, 100154. https://doi.org/10.1016/j.sca.2025.100154
- [P22] Mohammed, Z., Anas, C., & El Hammoumi, M. (2026). A hybrid learning framework for forecasting uncertainty and adaptive inventory planning in retail supply chains. *Supply Chain Analytics, 13*, 100180. https://doi.org/10.1016/j.sca.2025.100180
- [P23] Sfiris, D. S., & Koulouriotis, D. E. (2025). A new approach to forecast intermittent demand and stock-keeping-unit level optimization for spare parts management. *Applied Sciences, 15*(22), 12030. https://doi.org/10.3390/app152212030
- [P24] El-Meehy, A. O., El-Kharbotly, A. K., & El-Beheiry, M. M. (2026). Feature engineering for intermittent demand forecasting: Zero-detection and forecast performance across GRU, LSTM, and TCN architectures. *Journal of Intelligent Manufacturing*. https://doi.org/10.1007/s10845-026-02964-7
- [P25] Putra, B. Q. L., & Purnomo, J. D. T. (2026). Forecasting critical spare parts demand in combined cycle power plant using ensemble learning. *Engineering Proceedings, 143*, 30. https://doi.org/10.3390/engproc2026143030 [Crossref: authors, title, article 30, ETLTC 2026; volume 143 from `paper_list.md`]
- [W1] van der Haar, J. F., Wellens, A. P., Boute, R. N., & Basten, R. J. I. (2024). Supervised learning for integrated forecasting and inventory control. *European Journal of Operational Research, 319*(2), 573–586. https://doi.org/10.1016/j.ejor.2024.07.004 [Crossref]
- [W2] de Sousa, A. G. P. (2026). *From demand forecasting to replenishment simulation: A data-driven machine learning approach for fashion retail* (Master's thesis). University of Porto.
- [W3] Li, P. (2026). Forecasting for inventory decisions: A decision-regret benchmark for perishability-aware multi-echelon retail replenishment using the M5/Walmart data. SSRN. https://doi.org/10.2139/ssrn.7051299 *(cited by title only; not peer-reviewed)*
- [G22] Goltsos, T. E., Syntetos, A. A., Glock, C. H., & Ioannou, G. (2022). Inventory–forecasting: Mind the gap. *European Journal of Operational Research, 299*(2), 397–419. https://doi.org/10.1016/j.ejor.2021.07.040 *(abstract only)*
- [S1] Turgay, S., Demir, R., & Kavacık, M. (2026). A Monte Carlo-based approach to demand forecasting and stochastic optimization in supply chains. *Supply Chain Analytics, 14*, 100210. https://doi.org/10.1016/j.sca.2026.100210 [OpenAlex metadata and abstract; full text not read]
- [C2] Ansari, A. F., Shchur, O., Küken, J., Auer, A., Han, B., Mercado, P., Rangapuram, S. S., Shen, H., Stella, L., Zhang, X., Goswami, M., Kapoor, S., Maddix, D. C., Guerron, P., Hu, T., Yin, J., Erickson, N., Desai, P. M., Wang, H., Rangwala, H., Karypis, G., Wang, Y., & Bohlke-Schneider, M. (2025). Chronos-2: From univariate to universal forecasting. arXiv:2510.15821. [arXiv page, v1 17 Oct 2025, no journal-ref; technical report not read — cited only for the model]
- [VNF] Hoang Tien Anh (2023). *sales_and_inventory_snapshot_data: Sales and inventory data of Vietnam retailers — Dataset 2, Vietnam Datathon 2023* (version 1) [Data set]. Kaggle. https://www.kaggle.com/datasets/tienanh2003/sales-and-inventory-snapshot-data [Kaggle API: creator "Hoang Tien Anh", last updated 2023-11-13, licence "Unknown". Author name order (family name) to confirm with the owner]
- [VN1] Vandeput, N. (2024). *VN1 Forecasting – Accuracy Challenge*. DataSource.ai. https://www.datasource.ai/en/home/data-science-competitions-for-startups/phase-2-vn1-forecasting-accuracy-challenge/description [entry as given by Zanotti (2025), P08 p. 31]

Method references (not in `02_related_work/`; cited in `methodology.md`):

- Demšar, J. (2006). Statistical comparisons of classifiers over multiple data sets. *Journal of Machine Learning Research, 7*, 1–30. [JMLR page]
- Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics, 6*(2), 65–70. [Not in Crossref. Volume, issue and pages agree across several catalogues found by web search. The DOI 10.2307/4615733 that they give returns 404 at doi.org, so no DOI is listed.]
- Hyndman, R., Koehler, A., Ord, K., & Snyder, R. (2008). *Forecasting with exponential smoothing*. Springer Series in Statistics. Springer. https://doi.org/10.1007/978-3-540-71918-2 [Crossref. The subtitle "The state space approach" is not in Crossref and is omitted.]
- Koenker, R., & Bassett, G. (1978). Regression quantiles. *Econometrica, 46*(1), 33–50. https://doi.org/10.2307/1913643 [Crossref; pages 33–50 from the Econometric Society page. The Econometric Society page lists Bassett first, while Crossref and JSTOR list Koenker first; we follow Crossref.]
- Lei, J., G'Sell, M., Rinaldo, A., Tibshirani, R. J., & Wasserman, L. (2018). Distribution-free predictive inference for regression. *Journal of the American Statistical Association, 113*(523), 1094–1111. https://doi.org/10.1080/01621459.2017.1307116 [Crossref]
- Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830. [JMLR page]

## 7. Open items before submission

- [ ] Read Li (2026) and Theodorou et al. (2025). If either already covers liquidation or demand-class KPIs, re-position contributions 2–3.
- [x] Check whether arXiv papers 06, 08, 09, 11, 12, 13 have been formally published. As of 09/10/2026 none has a journal-ref; recheck just before submission.
- [x] Verify the references previously marked [Chưa kiểm chứng] (09/10/2026, see §6).
- [ ] Read Goltsos et al. (2022) and Kourentzes et al. (2020) in full before citing beyond the abstract / repository description.
- [~] Papers from the target journal: one recent *Supply Chain Analytics* paper added ([S1], abstract level); an OpenAlex search of the journal (2024–2026) found no other close match beyond papers 21–22. Revisit once the target journal is chosen.
- [x] [C2] verified on arXiv (10/10/2026). [VNF] citation completed from the Kaggle API; the licence is "Unknown" — **ask the owner (Hoang Tien Anh) or the Datathon organiser for permission before submission**.
- [ ] Re-check against the PDFs: P21/P22 cost parameters (Table A) and that P11, P21 and P22 use a single test period (Introduction, difficulty 3).
- [x] Pipeline figure drawn (`code/make_pipeline_figure.py`, Figure 1) and figures renumbered.
- [x] Appendix written (`appendix.md`, A1–A6; tables from `code/paper_appendix_tables.py`).
- [x] Cross-check of all draft numbers against `06_experiment_results/tables/` (09/10/2026). Five rounding errors were corrected in `06_experiment_results/results.md` (and in the draft where used): M5 fixed s\* lower end 1.06; VN1 fixed lost sales 0.12–0.23; VN1 dead13 re-orders 0.01–0.12; VN1 dead13 stockout +68% and inventory −19.4%. The "TSB-P 97%" statement now says "less inventory than LGB-Q", and the fixed-rule range is restricted to the ML forecasts.
- [x] Optional experiments run on 10/10/2026: L/H/q_L/k grid for M5 (main window); break-even for the second and third windows. Not run (cost): Chronos-2 on the earlier M5 windows (about 13 CPU hours each); Chronos-2 with weekly context or covariates.
