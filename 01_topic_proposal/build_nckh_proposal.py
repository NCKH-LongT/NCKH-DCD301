"""Build the NCKH FA26 research proposal (FPTU HCM template structure) as a Word file.

Template requirements (official proposal template): English, A4, single column, Times New Roman 11, at most 10 pages
excluding references and appendices, IEEE citations for the IT sub-committee, followed by the Commitment on
Responsible AI Usage. Citations are written as {key} and numbered in order of first appearance (IEEE).

Usage:
    python 01_topic_proposal/build_nckh_proposal.py 01_topic_proposal/NCKH_FA26_Proposal.docx
"""
import re
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

OUT = sys.argv[1]
TITLE = ("Beyond Forecast Accuracy: Comparing Probabilistic Demand Forecasts by the Inventory They Require across "
         "Retail Settings and Periods")

REFS = {
    "m5": 'S. Makridakis, E. Spiliotis, and V. Assimakopoulos, "The M5 competition: Background, organization, and implementation," Int. J. Forecast., vol. 38, no. 4, pp. 1325–1336, 2022, doi: 10.1016/j.ijforecast.2021.07.007.',
    "m5acc": 'S. Makridakis, E. Spiliotis, and V. Assimakopoulos, "M5 accuracy competition: Results, findings, and conclusions," Int. J. Forecast., vol. 38, no. 4, pp. 1346–1364, 2022, doi: 10.1016/j.ijforecast.2021.11.013.',
    "m5unc": 'S. Makridakis et al., "The M5 uncertainty competition: Results, findings and conclusions," Int. J. Forecast., vol. 38, no. 4, pp. 1365–1385, 2022, doi: 10.1016/j.ijforecast.2021.10.009.',
    "vn1": 'N. Vandeput, "VN1 Forecasting – Accuracy Challenge," DataSource.ai, 2024.',
    "zanotti": 'M. Zanotti, "The cost of ensembling: Is it always worth combining?" arXiv:2506.04677, 2025.',
    "wang26": 'S. Wang, Y. Kang, E. Spiliotis, and F. Petropoulos, "Multi-objective probabilistic forecast combination for inventory demand," arXiv:2606.04900, 2026.',
    "goltsos": 'T. E. Goltsos, A. A. Syntetos, C. H. Glock, and G. Ioannou, "Inventory–forecasting: Mind the gap," Eur. J. Oper. Res., vol. 299, no. 2, pp. 397–419, 2022, doi: 10.1016/j.ejor.2021.07.040.',
    "theodorou": 'E. Theodorou, E. Spiliotis, and V. Assimakopoulos, "Forecast accuracy and inventory performance: Insights on their relationship from the M5 competition data," Eur. J. Oper. Res., vol. 322, no. 2, pp. 414–426, 2025, doi: 10.1016/j.ejor.2024.12.033.',
    "spiliotis": 'E. Spiliotis, S. Makridakis, A. Kaltsounis, and V. Assimakopoulos, "Product sales probabilistic forecasting: An empirical evaluation using the M5 competition data," Int. J. Prod. Econ., vol. 240, Art. no. 108237, 2021, doi: 10.1016/j.ijpe.2021.108237.',
    "petropoulos": 'F. Petropoulos, X. Wang, and S. M. Disney, "The inventory performance of forecasting methods: Evidence from the M3 competition data," Int. J. Forecast., vol. 35, pp. 251–265, 2019, doi: 10.1016/j.ijforecast.2018.01.004.',
    "mohammed": 'Z. Mohammed, C. Anas, and M. El Hammoumi, "A hybrid learning framework for forecasting uncertainty and adaptive inventory planning in retail supply chains," Supply Chain Anal., vol. 13, Art. no. 100180, 2026, doi: 10.1016/j.sca.2025.100180.',
    "zabraoui": 'O. Zabraoui, Y. Hmamou, A. Chafi, and S. Kammouri Alami, "A comparative study of multi-algorithm optimization for inventory analytics in supply chains," Supply Chain Anal., vol. 12, Art. no. 100154, 2025, doi: 10.1016/j.sca.2025.100154.',
    "kourentzes": 'N. Kourentzes, J. R. Trapero, and D. K. Barrow, "Optimising forecasting models for inventory planning," Int. J. Prod. Econ., vol. 225, Art. no. 107597, 2020, doi: 10.1016/j.ijpe.2019.107597.',
    "vdhaar": 'J. F. van der Haar, A. P. Wellens, R. N. Boute, and R. J. I. Basten, "Supervised learning for integrated forecasting and inventory control," Eur. J. Oper. Res., vol. 319, no. 2, pp. 573–586, 2024, doi: 10.1016/j.ejor.2024.07.004.',
    "tsb": 'R. H. Teunter, A. A. Syntetos, and M. Z. Babai, "Intermittent demand: Linking forecasting to inventory obsolescence," Eur. J. Oper. Res., vol. 214, no. 3, pp. 606–615, 2011, doi: 10.1016/j.ejor.2011.05.018.',
    "syntetos": 'A. A. Syntetos, J. E. Boylan, and J. D. Croston, "On the categorization of demand patterns," J. Oper. Res. Soc., vol. 56, no. 5, pp. 495–503, 2005, doi: 10.1057/palgrave.jors.2601841.',
    "babai": 'M. Z. Babai, M. M. Ali, and K. Nikolopoulos, "Impact of temporal aggregation on stock control performance of intermittent demand estimators: Empirical analysis," Omega, vol. 40, pp. 713–721, 2012, doi: 10.1016/j.omega.2011.09.004.',
    "damato": 'S. Damato, N. Rubattu, D. Azzimonti, and G. Corani, "Intermittent time series forecasting: Local vs global models," arXiv:2601.14031, 2026.',
    "combreview": 'X. Wang, R. J. Hyndman, F. Li, and Y. Kang, "Forecast combinations: An over 50-year review," Int. J. Forecast., vol. 39, no. 4, pp. 1518–1547, 2023, doi: 10.1016/j.ijforecast.2022.11.005.',
    "fforma": 'P. Montero-Manso, G. Athanasopoulos, R. J. Hyndman, and T. S. Talagala, "FFORMA: Feature-based forecast model averaging," Int. J. Forecast., vol. 36, no. 1, pp. 86–92, 2020.',
    "lightgbm": 'G. Ke et al., "LightGBM: A highly efficient gradient boosting decision tree," in Proc. Adv. Neural Inf. Process. Syst. 30, 2017.',
    "koenker": 'R. Koenker and G. Bassett, "Regression quantiles," Econometrica, vol. 46, no. 1, pp. 33–50, 1978, doi: 10.2307/1913643.',
    "conformal": 'J. Lei, M. G\'Sell, A. Rinaldo, R. J. Tibshirani, and L. Wasserman, "Distribution-free predictive inference for regression," J. Amer. Statist. Assoc., vol. 113, no. 523, pp. 1094–1111, 2018, doi: 10.1080/01621459.2017.1307116.',
    "ets": 'R. Hyndman, A. Koehler, K. Ord, and R. Snyder, Forecasting with Exponential Smoothing. Berlin, Germany: Springer, 2008, doi: 10.1007/978-3-540-71918-2.',
    "sklearn": 'F. Pedregosa et al., "Scikit-learn: Machine learning in Python," J. Mach. Learn. Res., vol. 12, pp. 2825–2830, 2011.',
    "nhits": 'C. Challu, K. G. Olivares, B. N. Oreshkin, F. Garza, M. Mergenthaler-Canseco, and A. Dubrawski, "N-HiTS: Neural hierarchical interpolation for time series forecasting," in Proc. AAAI Conf. Artif. Intell., vol. 37, no. 6, 2023, doi: 10.1609/aaai.v37i6.25854.',
    "chronos": 'A. F. Ansari et al., "Chronos-2: From univariate to universal forecasting," arXiv:2510.15821, 2025.',
    "demsar": 'J. Demšar, "Statistical comparisons of classifiers over multiple data sets," J. Mach. Learn. Res., vol. 7, pp. 1–30, 2006.',
}

# ----------------------------------------------------------------------------------------- content
# ("h1"|"h2"|"p"|"b"|"plan"|"pre"), text
C = []
H1 = lambda t: C.append(("h1", t))
H2 = lambda t: C.append(("h2", t))
P = lambda t: C.append(("p", t))
B = lambda t: C.append(("b", t))

ABSTRACT = (
    "Public retail forecasting benchmarks rank methods by forecast error, although forecasts are used to decide how much "
    "stock to hold. This research asks which probabilistic demand forecasting method needs the least inventory to reach a "
    "target service level in a realistic replenishment policy, and whether the answer holds across retail settings and "
    "time periods. The problem is that studies linking forecasts to inventory decisions usually rely on one dataset, one "
    "test period, selected series and assumed cost parameters, so their conclusions may not transfer to other retailers "
    "or periods. We embed seven probabilistic forecasting methods (three statistical, four gradient-boosting) and a "
    "neural baseline in one order-up-to policy with lost sales and optional liquidation, and evaluate them on all "
    "eligible series of two public datasets, M5 (brick-and-mortar) and VN1 (multi-vendor e-commerce), across three "
    "26-week test windows. Methods are compared by the inventory they require at the same realised fill rate, with "
    "bootstrap confidence intervals, complemented by regret, a cost view over lost-sales penalties, and sensitivity "
    "analyses of lead time and hyper-parameters. Preliminary results show that LightGBM quantile regression is the most "
    "efficient single method on M5 in every window, whereas on VN1 the best method changes with the period; a post hoc "
    "equal-weight quantile combination of LightGBM and a negative-binomial TSB model is the most robust choice in the "
    "tested windows and will be validated on new periods.")
KEYWORDS = ("probabilistic forecasting; inventory management; intermittent demand; quantile regression; forecast "
            "combination; M5; VN1")

H1("1. Introduction")
H2("1.1 Literature Review")
P("Retail demand forecasting has been driven by public competitions. In the M5 accuracy track, LightGBM {lightgbm} was "
  "used by all of the top 50 teams and the winning solution combined LightGBM models trained with a Tweedie loss {m5acc}; "
  "the winner of the uncertainty track trained a separate LightGBM model for each quantile {m5unc}. These competitions "
  "score forecasts by error measures such as the weighted scaled pinball loss {m5}, and their organisers state that they "
  "did not target a specific decision problem {m5unc}. The more recent VN1 e-commerce dataset {vn1} has likewise been "
  "used to study accuracy and computational cost {zanotti}. Forecast accuracy, however, is not the quantity a retailer "
  "pays for: a structured review observes that most forecasting studies ignore the step from forecast to replenishment "
  "decision {goltsos}.")
P("A growing body of work evaluates forecasts by their inventory consequences. Kourentzes et al. tune exponential "
  "smoothing with an inventory-based cost function {kourentzes}; van der Haar et al. learn order quantities end to end "
  "{vdhaar}; Petropoulos et al. simulate an order-up-to policy over rolling origins on M3 data and find that forecast "
  "combinations perform best {petropoulos}. On M5, Spiliotis et al. compare 21 probabilistic methods in a 28-day daily "
  "simulation and find that simple empirical quantile methods outperform machine learning in inventory terms {spiliotis}; "
  "Wang et al. study probabilistic combinations with a single-period newsvendor rule {wang26}; Zabraoui et al. simulate "
  "reinforcement-learning policies on selected items {zabraoui}; and Mohammed et al. evaluate safety stock on 8,000 "
  "high-volume series {mohammed}. The closest study, by Theodorou et al. {theodorou}, simulates one year of an "
  "order-up-to policy with lost sales on 7,783 daily product–state series of M5 for 13 methods whose quantiles are "
  "point forecasts plus empirical error quantiles. Trade-off curves broadly follow accuracy, but total costs that weight "
  "lost sales heavily favour less accurate methods, and the authors call for replications on online retail data.")
P("Two further strands are relevant. For intermittent demand, the TSB method updates a demand probability every period "
  "{tsb}, demand is classified by the average inter-demand interval and the squared coefficient of variation (ADI–CV²) "
  "{syntetos}, the negative binomial is a common distribution for stock control {babai}, and no global architecture is "
  "established for such series {damato}. For model choice, forecast combinations hedge against model uncertainty, and the "
  "\"forecast combination puzzle\" states that equal weights often beat estimated weights {combreview}; feature-based "
  "meta-learning such as FFORMA learns combination weights from series features {fforma}. Neural and foundation models "
  "such as N-HiTS {nhits} and Chronos-2 {chronos} are increasingly used as global forecasters.")
P("Quality and gaps. The reviewed sources are peer-reviewed journals and proceedings (IJF, EJOR, IJPE, AAAI) or "
  "preprints from established groups; the preprints are marked as such. Four gaps and inconsistencies emerge. (1) Studies "
  "on M5 often keep only selected series, such as high-volume items {mohammed}, food items {zabraoui} or series with at "
  "least 2.5 years of history {theodorou}. (2) Most use one dataset and one test period {wang26}, {theodorou}, "
  "{spiliotis}, so it is unknown whether conclusions transfer across settings and periods; Theodorou et al. themselves "
  "caution that one simulated year gives no guarantee for the next {theodorou}. (3) Cost-based evaluations depend on "
  "assumed parameters, and cost-based and cost-free conclusions can disagree {theodorou}. (4) Results conflict: simple "
  "methods win in daily simulations {theodorou}, {spiliotis}, whereas LightGBM dominates the M5 competitions "
  "{m5acc}, {m5unc}. Our literature search has not yet identified studies by Vietnamese researchers that evaluate "
  "probabilistic retail forecasts by inventory decisions; the search will be extended in local journals and conferences "
  "during the project.")
P("Applications and implications. Decision-based evaluation matters for retailers who must choose a forecasting method "
  "without cost data or a data-science team. The implication for research is that benchmarks should report inventory at "
  "equal service level over several periods; for practice, that a method choice should be robust when the best method "
  "cannot be known in advance.")

H2("1.2 Necessity of the Research")
P("Problem. A retailer needs to know which forecasting method keeps the least stock for a required service level, but "
  "public benchmarks answer a different question (which method has the lowest error), and decision-based studies are "
  "limited to one setting and one period. The research tests three hypotheses: H1 – the ranking of methods by inventory "
  "at equal realised fill rate differs from the ranking by forecast error; H2 – the most inventory-efficient method "
  "depends on the retail setting and on the test period; H3 – a combination of complementary methods is more robust "
  "(smaller worst-case regret) than any single method.")
P("Originality and significance. The research combines, for the first time to our knowledge, (i) two public retail "
  "settings, brick-and-mortar and e-commerce, (ii) all eligible series including intermittent ones, (iii) three test "
  "periods, (iv) comparison at equal realised fill rate rather than at equal nominal service target, and (v) a test of "
  "whether demand classes, unsupervised segmentation or a growth predictor can choose the method in advance. The "
  "scientific value lies in evidence on when forecast accuracy translates into inventory efficiency; the practical "
  "value lies in a simple, reproducible recommendation for small retailers.")

H2("1.3 Feasibility of Research")
P("Research question. Which probabilistic forecasting method, or combination, needs the least inventory to reach a "
  "target fill rate in an order-up-to policy with lost sales, and does the answer hold across retail settings and test "
  "periods? Sub-questions: RQ1 – how do statistical, gradient-boosting and neural methods compare at equal realised fill "
  "rate on M5 and VN1; RQ2 – why does the best method change between periods, and can demand classes, unsupervised "
  "segmentation or a growth predictor anticipate it; RQ3 – is a quantile combination robust, and how does the answer "
  "depend on the cost of a lost sale; RQ4 – does liquidation reduce inventory without losing service, and at which "
  "salvage price does it break even under assumed costs.")
P("Research design. An empirical benchmark with rolling-origin forecasting and multi-period inventory simulation. Each "
  "method forecasts quantiles {0.5, 0.8, 0.9, 0.95, 0.99} of cumulative demand over the protection interval directly; "
  "the policy orders up to the τ-quantile; the inventory needed at each fill target is interpolated along the "
  "inventory–fill-rate curve; statistical significance uses bootstrap intervals over series and the Friedman–Nemenyi "
  "test {demsar}.")
P("Sample size and population. The population is retail SKU–location demand series. Sample: M5 contains 30,490 "
  "product–store series over 277 weeks; VN1 contains 15,053 client–warehouse–product series over 196 weeks. Inclusion "
  "criterion: a series starts at least 13 weeks before the test window and has at least one sale before it, giving "
  "30,381 / 29,917 / 28,824 eligible M5 series and 13,844 / 11,442 / 9,383 eligible VN1 series in the three windows. No "
  "further sampling is applied.")
P("Data sources. Existing public datasets only: M5 (Kaggle competition data) and VN1 (DataSource.ai). No surveys or "
  "interviews are needed. The datasets are used under their terms and are not redistributed.")
P("Budget and funding. No direct cost: data are public and all experiments run on the authors' laptops (Intel Core "
  "i5-12450H, 16 GB RAM, CPU only). A possible conference registration fee for the accompanying paper is outside this "
  "proposal.")
P("Timeframe. October to December 2026, aligned with the competition milestones (Section 5). The core benchmark and "
  "robustness analyses are already running and reproducible from a public repository "
  "(https://github.com/anhduyBA/forecast-to-decision-benchmark).")
P("Potential challenges and risks. (1) Sales are used as demand, so historical stock-outs are invisible – mitigated by "
  "stating the limitation and by comparing methods under identical data. (2) The combination was specified after the "
  "main analysis – mitigated by validating it on new periods before claiming it. (3) Bootstrap intervals resample series, "
  "not periods – mitigated by three separate test windows. (4) Long computation on M5 – mitigated by caching forecasts "
  "and splitting runs across two machines with data fingerprints. (5) Dataset differences may confound comparisons – "
  "mitigated by re-weighting, price ablation and shared-feature checks.")

H1("2. Research Objectives")
B("O1 – Build a reproducible benchmark that embeds probabilistic forecasting methods in one order-up-to policy with "
  "optional liquidation, on all eligible series of M5 and VN1, repeated on three 26-week test windows.")
B("O2 – Define and apply a cost-free evaluation protocol: inventory at equal realised fill rate with bootstrap confidence "
  "intervals, frontier rank and regret, complemented by a cost view over lost-sales penalties.")
B("O3 – Explain differences between settings and periods, and test demand classes, an unsupervised segmentation, a "
  "growth-prediction rule and quantile combinations as ways to choose a method.")
B("O4 – Check robustness to lead time, hyper-parameters, price features, feature parity and a neural baseline.")
B("O5 – Validate the recommended combination on periods not used to select it, and publish code and results.")

H1("3. Research Scope")
P("Included: weekly demand of SKU–location series in two public retail datasets; seven probabilistic forecasting methods "
  "(empirical quantiles, exponential smoothing, TSB with a negative-binomial distribution, LightGBM with Tweedie loss plus "
  "safety stock, LightGBM with conformal quantiles, histogram gradient boosting and LightGBM quantile regression), a "
  "univariate N-HiTS baseline and quantile combinations; an order-up-to policy with weekly review, lead times of one, two "
  "and four weeks and lost sales; four liquidation rules evaluated over 26 weeks.")
P("Excluded: price-response (promotion) modelling, multi-echelon inventory, pack-size and minimum-order constraints, "
  "hyper-parameter tuning beyond the sensitivity analysis, and deployment at a real company. Conclusions are limited to "
  "the tested datasets, windows and policy settings.")

H1("4. Approach and Method")
P("RQ1 – Benchmark. Each method forecasts quantiles of the h-week total D_h(o) = Y[o] + … + Y[o+h−1] directly (h = 3 "
  "for replenishment, h = 13 for liquidation), using a rolling origin over the last 26 weeks in two 13-week blocks with "
  "refits. The global models (LightGBM {lightgbm}, quantile regression {koenker}, conformal quantiles {conformal}, "
  "scikit-learn {sklearn}) share lag, rolling, calendar and price features; the statistical models follow {ets}, {tsb}. "
  "Accuracy: volume-weighted quantile loss, coverage and per-series ranks with Friedman–Nemenyi {demsar}. Inventory: "
  "the policy orders max(S − IP, 0) with S the τ-quantile; τ runs over the five quantile levels, and the inventory needed "
  "at fill targets 0.90–0.98 is interpolated along each method's curve, with 200 bootstrap resamples of series.")
P("RQ2 – Period dependence. Series are split ex post into stable and growing demand to explain rankings; prospective "
  "selection is then tested with ADI–CV² classes {syntetos}, a Gaussian-mixture segmentation chosen by pre-defined "
  "stability criteria, and a classifier that predicts growth from pre-test features, each learned on an earlier window "
  "and applied to the next. Comparability between datasets is checked by inverse-propensity re-weighting, price "
  "ablation and refits with shared features only.")
P("RQ3 – Robust choice. Equal-weight quantile averaging {combreview} of complementary methods is compared with single "
  "methods and with learned weights; regret is the excess inventory over the best single method per run. A cost view "
  "maps each curve to cost C(r) = inventory + r·(1 − fill rate) for lost-sales penalties r from 10 to 1,000 weeks of "
  "holding. Robustness: lead times of one, two and four weeks in every window, four LightGBM settings, and a neural "
  "baseline (N-HiTS {nhits}).")
P("RQ4 – Liquidation. Quantile-based, fixed and dead-stock rules are simulated with the same forecasts; the break-even "
  "salvage ratio is computed over holding rates of 10–40% per year and margins of 30–100%.")
P("Validation of the combination (O5). The combination will be re-evaluated on test windows that were not used to choose "
  "it, so that the robustness claim does not rest only on the windows in which it was specified.")

H1("5. Research Plan")
C.append(("plan", [
    ("15/09/2026 – 05/10/2026", "Literature review; data acquisition and harmonisation of M5 and VN1", "Literature matrix; weekly panels; data checks", "Bùi Anh Duy, Khổng Trần Gia Huy"),
    ("01/10/2026 – 12/10/2026", "Benchmark of seven methods on three test windows", "Forecasts, simulation results, accuracy and inventory tables", "Bùi Anh Duy"),
    ("10/10/2026 – 16/10/2026", "Robustness: hyper-parameters, lead time, N-HiTS baseline, cost view, dataset checks", "Sensitivity tables; neural baseline results", "Bùi Anh Duy, Khổng Trần Gia Huy"),
    ("13/10/2026 – 20/10/2026", "Research proposal and conference draft", "Proposal (this document); draft paper", "Bùi Anh Duy, Khổng Trần Gia Huy"),
    ("21/10/2026 – 30/10/2026", "Revise and submit the full paper to ICIIT 2027 (approved by the mentors)", "Submitted conference paper; public code repository", "Bùi Anh Duy, Khổng Trần Gia Huy"),
    ("31/10/2026 – 01/11/2026", "Qualifying round presentation", "Presentation slides", "Bùi Anh Duy, Khổng Trần Gia Huy"),
    ("02/11/2026 – 27/11/2026", "Validate the combination on unseen periods; extend the literature search; address review comments", "Validation results; revised manuscript", "Bùi Anh Duy, Khổng Trần Gia Huy"),
    ("28/11/2026 – 07/12/2026", "Full paper for the competition in the IEEE template", "Full research paper", "Bùi Anh Duy, Khổng Trần Gia Huy"),
    ("08/12/2026 – 20/12/2026", "Final presentation preparation and final round", "Slides; final presentation", "Bùi Anh Duy, Khổng Trần Gia Huy"),
]))
P("The mentors, Nguyễn Thị Cẩm Hương and Trương Long, review the design, results and manuscripts at each milestone.")

H1("6. Expected Results")
P("Theoretical implications. Evidence on when forecast accuracy translates into inventory efficiency, and on how the "
  "answer depends on the retail setting, the test period and the cost of lost sales. Preliminary results (Appendix A) "
  "indicate that LightGBM quantile regression is the most efficient single method on brick-and-mortar data in every "
  "window and lead time tested, whereas on e-commerce data the best method changes with demand growth.")
P("Methodological implications. A cost-free protocol, inventory at equal realised fill rate over several periods, that "
  "avoids rewarding methods whose quantiles under-cover, together with regret and cost-view summaries; and a negative "
  "result: demand classes and unsupervised segmentation do not choose the method reliably.")
P("Practical implications. A simple, reproducible recommendation for retailers without cost data: an equal-weight "
  "quantile average of a global quantile model and a statistical intermittent-demand model, used unless lost sales are "
  "very expensive, subject to the planned validation. The benchmark code and results are public.")
P("Plan to apply the research in practice. The recommended models will be served in RetailIQ, the team's capstone "
  "warehouse-management system, which computes replenishment suggestions from probabilistic forecasts with an "
  "order-up-to policy and requires human approval of every order.")

# ----------------------------------------------------------------------------------------- appendix
APPX = [
    ("Single method with the lowest inventory at equal fill rate, M5", "LGB-Q in all three windows; 3.3–10.6% less inventory than LGB-T, LGB-C, TSB-NB and ETS at fill rate 0.94"),
    ("Same, VN1", "Changes with the window (LGB-Q, TSB-NB, LGB-Q)"),
    ("Lead times 1, 2 and 4 weeks (18 runs)", "M5: LGB-Q ahead of LGB-T, LGB-C, TSB-NB and ETS in all nine window × lead-time runs"),
    ("Quantile combination C2 (post hoc)", "VN1: 3.2–10.9% less inventory than LGB-Q at fill rate 0.92 across windows and lead times; maximum regret 2.0% vs 12.6% for LGB-Q"),
    ("Hyper-parameter settings", "M5 conclusions hold under four settings; VN1 under three of four"),
    ("Neural baseline (N-HiTS)", "Well calibrated; not the most inventory-efficient method in any run"),
    ("Liquidation", "Quantile rule costs ≤ 0.02 percentage points of fill rate; no economic benefit within 26 weeks under assumed costs"),
]

AI_RULES = [
    "AI may only assist with correcting grammar, structure, and phrasing in academic writing.",
    "AI must not create content, draft the paper, produce fake data, or synthesize literature.",
    "All authors must check and confirm AI use. Each author is fully responsible for the accuracy, transparency, and originality of their sections, including citations and references.",
    "All authors must disclose any use of generative AI or AI-assisted tools to co-authors, specifying where and how it was applied.",
]
AI_DISCLOSURE = (
    "Disclosure of AI use (rule 4). A generative AI assistant (Claude, Anthropic) was used in this project to write and "
    "debug analysis code, to run experiments on the public datasets, and to prepare drafts of this proposal and of the "
    "accompanying paper, including summaries of the cited literature prepared from full-text copies obtained by the "
    "authors. All numbers "
    "come from experiments that the authors can reproduce from the public repository. The authors have reviewed every "
    "section and take full responsibility for its accuracy. Because rule 2 restricts AI-generated content, the authors "
    "will confirm with the organising committee how this use should be handled before signing.")

# ----------------------------------------------------------------------------------------- numbering
order = []


def cite(text):
    def rep(m):
        k = m.group(1)
        if k not in order:
            order.append(k)
        return f"[{order.index(k) + 1}]"
    return re.sub(r"\{(\w+)\}", rep, text)


# ----------------------------------------------------------------------------------------- document
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
    setattr(sec, side, Cm(2.54))
st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
st.paragraph_format.space_after = Pt(4)
st.paragraph_format.line_spacing = 1.08


def para(text, bold=False, italic=False, size=None, align=None, space_before=0, indent_first=False, keep=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    if size:
        r.font.size = Pt(size)
    if align:
        p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    if keep:
        p.paragraph_format.keep_with_next = True
    return p


def body(text):
    """Body paragraph; a leading 'Label.' (up to ~6 words before the first full stop) is set in bold."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    m = re.match(r"^((?:[A-Z][\w–\-]*\s?){1,6}(?:[A-Z0-9]+)?\.)\s", text)
    lab = re.match(r"^(RQ\d – [^.]+\.|Validation of the combination \(O5\)\.|Research question\.|Research design\.|Sample size and population\.|Data sources\.|Budget and funding\.|Timeframe\.|Potential challenges and risks\.|Problem\.|Originality and significance\.|Quality and gaps\.|Applications and implications\.|Included:|Excluded:|Theoretical implications\.|Methodological implications\.|Practical implications\.|Plan to apply the research in practice\.)\s", text)
    if lab:
        r = p.add_run(lab.group(1) + " ")
        r.bold = True
        p.add_run(text[len(lab.group(0)):])
    else:
        p.add_run(text)
    return p


# cover
para("RESEARCH PROPOSAL", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER)
para("Student Research Competition FA26 – FPT University Ho Chi Minh City", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
para(TITLE, bold=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10)
cover = [("Research title", TITLE), ("Sub-committee", "Information Technology"), ("Group name", "[to be filled in by the group]"),
         ("Authors", "Bùi Anh Duy (SE193264, anhduy290605@gmail.com); Khổng Trần Gia Huy (SE180313, huyktgse180313@fpt.edu.vn)"),
         ("Mentor", "Nguyễn Thị Cẩm Hương (huongntc2@fpt.edu.vn); Trương Long (longt5@fpt.edu.vn)")]
t = doc.add_table(rows=len(cover), cols=2)
t.style = "Table Grid"
t.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, (k, v) in enumerate(cover):
    t.cell(i, 0).text, t.cell(i, 1).text = k, v
    t.cell(i, 0).paragraphs[0].runs[0].bold = True
    t.cell(i, 0).width, t.cell(i, 1).width = Cm(3.8), Cm(12.2)
para("Abstract", bold=True, size=12, space_before=10, keep=True)
pa = body(ABSTRACT)
kp = doc.add_paragraph()
kp.add_run("Keywords: ").bold = True
kp.add_run(KEYWORDS)

for kind, val in C:
    if kind == "h1":
        para(val, bold=True, size=12, space_before=10, keep=True)
    elif kind == "h2":
        para(val, bold=True, space_before=6, keep=True)
    elif kind == "p":
        body(cite(val))
    elif kind == "b":
        p = doc.add_paragraph(style="List Bullet")
        p.add_run(cite(val))
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    elif kind == "plan":
        tb = doc.add_table(rows=1 + len(val), cols=5)
        tb.style = "Table Grid"
        hdr = ["No.", "Date (dd/mm/yyyy – dd/mm/yyyy)", "Task", "Output", "Person in charge"]
        widths = [Cm(1.0), Cm(3.4), Cm(5.2), Cm(3.8), Cm(2.6)]
        for j, h in enumerate(hdr):
            c = tb.cell(0, j)
            c.text = h
            c.paragraphs[0].runs[0].bold = True
        for i, row in enumerate(val, 1):
            vals = [str(i)] + list(row)
            for j, v in enumerate(vals):
                tb.cell(i, j).text = v
        for row in tb.rows:
            for j, c in enumerate(row.cells):
                c.width = widths[j]
                for p in c.paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(10)

# references
para("References", bold=True, size=12, space_before=10, keep=True)
for i, k in enumerate(order, 1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.9)
    p.paragraph_format.first_line_indent = Cm(-0.9)
    r = p.add_run(f"[{i}]\t{REFS[k]}")
    r.font.size = Pt(10)

# appendix
para("Appendix A. Preliminary results (from the public repository)", bold=True, size=12, space_before=10, keep=True)
ta = doc.add_table(rows=1 + len(APPX), cols=2)
ta.style = "Table Grid"
ta.cell(0, 0).text, ta.cell(0, 1).text = "Analysis", "Preliminary finding"
for j in range(2):
    ta.cell(0, j).paragraphs[0].runs[0].bold = True
for i, (a, b) in enumerate(APPX, 1):
    ta.cell(i, 0).text, ta.cell(i, 1).text = a, b
for row in ta.rows:
    row.cells[0].width, row.cells[1].width = Cm(5.0), Cm(11.0)
    for c in row.cells:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.size = Pt(10)
para("These results come from three test windows; the combination was specified after the main analysis and is "
     "validated on unseen periods in the research plan.", italic=True, size=10)

# AI commitment
doc.add_page_break()
para("Commitment on Responsible AI Usage in Research", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER)
para(f"Paper title: {TITLE}", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
body("All members of the research team commit to complying with the regulations on AI use and the guidelines on research "
     "ethics, as follows:")
for k, rule in enumerate(AI_RULES, 1):
    p = doc.add_paragraph(style="List Number")
    p.add_run(rule)
body(AI_DISCLOSURE)
body("The authors take full responsibility for the accuracy and transparency of the information provided.")
sig = doc.add_table(rows=3, cols=2)
labels = ["Author 1", "Author 2"]
names = ["Bùi Anh Duy", "Khổng Trần Gia Huy"]
for j in range(2):
    sig.cell(0, j).text = labels[j]
    sig.cell(0, j).paragraphs[0].runs[0].bold = True
    sig.cell(1, j).text = "(Signature)\n\n\n"
    sig.cell(2, j).text = names[j]
    for i in range(3):
        sig.cell(i, j).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.core_properties.title = TITLE
doc.save(OUT)
print("written", OUT, "| references:", len(order), "| abstract words:", len(ABSTRACT.split()))
