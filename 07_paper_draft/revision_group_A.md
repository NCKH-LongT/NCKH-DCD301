# Sửa nhóm A cho `final_paper.docx` — đoạn thay thế

File làm việc, chưa commit.

**Nguồn đã đọc ngày 12/10/2026:**

- Chronos-2: toàn văn bản HTML arXiv:2510.15821v1.
- Theodorou et al. (2025): **chỉ tóm tắt** (RePEc/IDEAS). Bài đóng sau tường phí.

**Quy ước:**

- "TÌM" = đoạn đang có trong bài; "THAY" = đoạn mới.
- Số mục (Sec.) và số bảng của Chronos-2 lấy từ bản HTML v1. **Kiểm tra lại số trang trên PDF trước khi nộp.**

---

## A1. Chronos-2

### A1.1 Lỗi sự thật phải sửa: M5 KHÔNG thuộc dữ liệu huấn luyện của Chronos-2

Báo cáo kỹ thuật cho thấy:

- Bảng 6 ("Real univariate datasets used for pretraining") liệt kê đủ 23 bộ dữ liệu, **không có M5**: Electricity, KDD Cup 2018, M4 (Daily/Hourly/Monthly/Weekly), Mexico City Bikes, Pedestrian Counts, Solar, Taxi, Uber TLC, USHCN, Weatherbench, Wiki, Wind Farms, Temperature-Rain, London Smart Meters, Alibaba Cluster Trace, Azure VM Traces, Borg Cluster Data, LargeST, Q-Traffic, Buildings 900K.
- M5 chỉ xuất hiện ở Bảng 11 (Phụ lục B) như **bài đánh giá** thuộc fev-bench (tần suất M, W, D).
- Sec. 5.1 ghi về fev-bench: "None of these datasets or tasks were seen by Chronos-2 during training."

Kho Hugging Face `autogluon/chronos_datasets` chứa cả dữ liệu đánh giá. Vì vậy, có tên file M5 trong kho **không** chứng minh M5 được dùng để huấn luyện.

**Các chỗ phải sửa trong bài:**

| Vị trí | Việc cần làm |
|---|---|
| Sec. 3.4, gạch đầu dòng "According to the model card, the training data include subsets of … The M5 result is therefore not a clean zero-shot test…" | Thay bằng đoạn A1.2 |
| Sec. 5.8, câu "Because M5 is part of the Chronos-2 training corpora, the M5 result is not a clean zero-shot test" | Xóa |
| Table 9, chú thích "(*) M5 is part of the Chronos-2 training data." và dấu (*) ở dòng "M5, main" | Xóa |
| Sec. 5.8, "On M5, despite the possible overlap with its training data, Chronos-2 is only on par with ETS" | Sửa thành "On M5, Chronos-2 is only on par with ETS" |
| Sec. 6.1, "This holds even on M5, which is part of its training data." | Xóa |
| Sec. 7 (Extensions), "even on M5, which is part of its training data," | Xóa cụm này |

### A1.2 Đoạn thay thế cho Sec. 3.4 (mô tả Chronos-2)

**THAY toàn bộ đoạn "Chronos-2. Chronos-2 is a 120-million-parameter…" và các gạch đầu dòng bên dưới bằng:**

> **Chronos-2.** Chronos-2 is a pretrained encoder-only transformer with 120 million parameters that outputs 21 quantile levels between 0.01 and 0.99 and is trained with a quantile loss (Ansari et al., 2025, Sec. 3.2, 5.1). Its main additions over earlier pretrained models are support for past and known-future covariates and a group-attention mechanism that shares information across related series (Ansari et al., 2025, Sec. 3.2, 3.4). The authors report their largest gains on tasks with covariates (Ansari et al., 2025, Sec. 5.2).
>
> We use the model zero-shot on CPU in its most restricted configuration: univariate, without covariates, without grouping related series and without fine-tuning. This is a deliberate lower bound on what the model can do, not an assessment of its full capability.
>
> To forecast D_h directly, as all other methods do, the context of series i at origin o is the sequence of non-overlapping h-week totals ending at o, over at most 104 weeks, and the model predicts one step ahead. The context is therefore short: at most 34 points for h = 3 and 8 points for h = 13. All requested quantiles (0.5–0.99) are among the model's output levels, so no interpolation of quantiles is needed.
>
> M5 is not among the real datasets listed for pretraining (Ansari et al., 2025, Table 6); it appears only as an evaluation task (Ansari et al., 2025, Table 11). VN1 and VNF are not mentioned in the report. We therefore treat all three as zero-shot tests.
>
> Because of its runtime on CPU (Section 4.4), Chronos-2 was run on the main M5 window, the three VN1 windows and VNF. Its results are stored separately, so the ranks of the eight-method benchmark are not affected.

Ghi chú:

- Số điểm ngữ cảnh: 104 // 3 = 34 và 104 // 13 = 8. **Kiểm tra lại với code** (`rerun_c2.sh` và hàm tạo ngữ cảnh) trước khi dùng hai con số này.
- Xóa câu "The facts used here come from the model card and configuration of amazon/chronos-2; the technical report was not read."

### A1.3 Sec. 2.1 (Related Work, đoạn Foundation models)

**TÌM:** "Chronos-2 is a recent pretrained model with quantile outputs and native covariate support (Ansari et al., 2025; model card)."

**THAY:**

> Chronos-2 is a recent pretrained model with quantile outputs, covariate support and a group-attention mechanism for related series; it was trained on real univariate datasets and on synthetic data (Ansari et al., 2025, Sec. 3–4). Its report includes retail tasks, among them M5, and evaluates forecast accuracy only (Ansari et al., 2025, Sec. 5.3, Table 11).

### A1.4 Sec. 6.1 (đoạn về foundation model) — giảm mức khẳng định

**TÌM:** tiêu đề đoạn "A general-purpose foundation model does not replace a simple global model here." và các câu sau nó.

**THAY:**

> **A zero-shot univariate foundation model did not change the conclusions.** Used without covariates or cross-series information, Chronos-2 was less accurate than LGB-Q on 64–79% of the series and never the most inventory-efficient method (Table 9). It was also 8–42 times slower on CPU. This result concerns one restricted configuration: the model's reported strengths are covariates and related series (Ansari et al., 2025, Sec. 5.2), which we did not use, and our contexts of h-week totals are short (Section 3.4). The result should therefore not be read as evidence against foundation models in general.

**Sửa tương ứng:**

- **Tóm tắt (Abstract):** thay "Chronos-2 is never the best method and is 8–42 times slower." bằng "A zero-shot, univariate use of Chronos-2 is never the best method and is 8–42 times slower on CPU."
- **Main findings:** thay "Foundation model: zero-shot Chronos-2 is never…" bằng "Foundation model: used zero-shot and without covariates, Chronos-2 is never…".

---

## A2. Theodorou et al. (2025) — chỉ đọc được tóm tắt

**Nội dung tóm tắt** (RePEc; diễn giải, không trích nguyên văn):

- Dữ liệu M5; mô phỏng với các phương pháp tạo dự báo phân vị.
- Nhiều thiết lập của chính sách order-up-to, cho các chuỗi có kiểu nhu cầu khác nhau.
- Chi phí lưu kho, đặt hàng và mất doanh số.
- Độ chính xác quan trọng hơn khi chi phí lưu kho ngang hoặc cao hơn chi phí mất doanh số.
- Khi chi phí mất doanh số cao hơn, phương pháp chính xác nhất có thể không phải tốt nhất, nhất là với chu kỳ xem xét và lead time ngắn và với sản phẩm rời rạc.

**Hệ quả:** không được coi "mô phỏng order-up-to nhiều kỳ trên M5 theo kiểu nhu cầu" là điểm mới. Khác biệt còn đứng được:

1. dataset thứ hai (VN1) và ba cửa sổ kiểm thử;
2. so sánh ở cùng fill rate, không cần giả định chi phí;
3. quyết định thanh lý;
4. kết quả theo chuỗi (hạng, trung vị).

**Không** viết gì về tên phương pháp, số chuỗi hay con số của họ, vì tóm tắt không nêu.

### A2.1 Sec. 1 (Introduction)

**TÌM:** "Theodorou et al. (2025) examined the relationship between forecast accuracy and inventory performance on the M5 data (Theodorou et al., 2025)."

**THAY:**

> On the M5 data, Theodorou et al. (2025) simulate an order-up-to policy with quantile forecasts and report that the most accurate method may not be the best choice when lost-sales costs exceed holding costs, especially for intermittent products and short lead times (Theodorou et al., 2025, abstract).

### A2.2 Sec. 2.3 — thay đoạn "Related benchmarks we could not read."

**THAY toàn bộ đoạn bằng:**

> **Accuracy and inventory performance on M5.** Theodorou et al. (2025) study the relationship between forecast accuracy and inventory performance on M5. According to the abstract, they simulate several set-ups of an order-up-to policy with quantile forecasts for series with different demand patterns, and consider holding, ordering and lost-sales costs. They find that accuracy matters more when holding costs are similar to or higher than lost-sales costs, and that the most accurate method may not be the best choice when lost-sales costs dominate, especially for short review periods and lead times and for intermittent products (Theodorou et al., 2025, abstract). We had access to the abstract only, so we do not comment on their methods or numerical results. Our study is complementary in four respects: a second retail dataset (VN1) and three test windows; a comparison at equal fill rate that needs no cost assumption; a liquidation decision; and per-series evidence (ranks, medians and win shares) in addition to aggregate KPIs.

**Về Li (2026, SSRN):** bài chưa phản biện và chưa đọc được. Đề xuất **xóa** khỏi bài (cả ở Sec. 2.3, Table A, Sec. 6.4 và References). Nếu muốn giữ, chỉ để một câu: "A decision-regret benchmark on M5 for perishable, multi-echelon replenishment has also been proposed (Li, 2026, preprint)."

### A2.3 Sec. 2.5 (Positioning)

- **Table A:** thêm một cột "Theodorou et al. (2025)†" với chú thích "† based on the abstract only". Điền:
  - Datasets: M5;
  - Inventory evaluation: order-up-to simulation;
  - Results by demand pattern: ✓ (demand patterns);
  - Cost-free KPIs: costs;
  - các ô còn lại: "n/s" (not stated in the abstract).
- **Chú thích bảng:**
  - TÌM: "Entries for papers 11, 21 and 22 are based on full texts. Papers 20 and W3 are omitted because they were not read."
  - THAY: "Entries are based on full texts, except Theodorou et al. (2025), which is based on its abstract."
- **Câu sau bảng:**
  - TÌM: "Multi-period simulation alone is not new (Zabraoui et al., 2025; van der Haar et al., 2024), nor is decision-level evaluation (Wang et al., 2026)."
  - THAY: "Multi-period simulation is not new (Zabraoui et al., 2025; van der Haar et al., 2024; Theodorou et al., 2025), nor is decision-level evaluation (Wang et al., 2026) or the observation that the most accurate method need not be the best for inventory (Theodorou et al., 2025)."

### A2.4 Sec. 6.1

**TÌM:** "We state this as an observation on our datasets and windows, not as a general law. The general relationship between accuracy and inventory performance on M5 has been examined by Theodorou et al. (2025), whose results we could not read."

**THAY:**

> This is consistent with Theodorou et al. (2025), who report on M5 that the most accurate method may not be the best choice for intermittent products when lost-sales costs dominate (abstract). Our results add that, on VN1, the divergence also depends on the test period, and that on M5 we observe no divergence at the service levels studied. We state this as an observation on our datasets and windows, not as a general law.

### A2.5 Sec. 6.4 (Limitations, "Literature coverage")

**THAY:**

> **Literature coverage.** Theodorou et al. (2025) was available to us as an abstract only. Several cited studies are preprints.

---

## A3. Dấu vết bản nháp — tìm và sửa (Ctrl+H trong Word)

| TÌM | Xử lý |
|---|---|
| `[Author names and affiliations to be added]` | Điền tên và đơn vị |
| `papers 11 and 21–25` (Sec. 2.4) | "the full texts of Wang et al. (2026), Zabraoui et al. (2025), Mohammed et al. (2026), Sfiris and Koulouriotis (2025), El-Meehy et al. (2026) and Putra and Purnomo (2026)" — **đối chiếu lại số 23–25 với `02_related_work/paper_list.md`** |
| `The abstracts of W1 and W2 do not mention one either.` | "The abstracts of van der Haar et al. (2024) and de Sousa (2026) do not mention one either." |
| `RL (low interpretability, p. 19)` (Table A) | "RL (low interpretability)" |
| `(not tested) (not tested)` và các "(not tested)" lẻ | Giữ một lần, viết thành câu: "We did not test this." |
| `main window,.` (Table 2b) | "main window." |
| `analyses:.` (Sec. 4.5) | Điền tên script (`analyze_results.py`, `stat_tests.py`, `liquidation_breakeven.py`) hoặc xóa dòng |
| `[link to be added]` | Điền link repo |
| `reported for transparency,:` | "reported for transparency:" |
| `are, conditional on` (Sec. 6.2) | "are conditional on" |
| `(Table 10;).` | "(Table 10)." |
| `“Unknown”,.` | "“Unknown”." |
| Trích dẫn lặp: `X et al. (YYYY) … (X et al., YYYY)` trong cùng một câu | Xóa cái trong ngoặc ở cuối câu (hàng chục chỗ; tìm chuỗi `) (` và `, 2026) (`) |
| `Table A`, `Table 2b`, bảng chính sách không số | Đánh số lại liên tục: Table 1…N |
| Chú thích Figure 1 lặp ("Figure 1" + "Figure 1. Benchmark pipeline…") | Giữ một |

## A4. Giả thuyết H2, H3 chưa được phát biểu

Thêm vào cuối Sec. 1, sau các câu hỏi nghiên cứu (hoặc đầu Sec. 3.6):

> Before running the benchmark we stated four working hypotheses. H1: LightGBM quantile regression has the lowest quantile loss on both datasets. H2: at equal fill rate, direct quantile forecasts need less inventory than a point forecast with normal safety stock. H3: machine-learning models help most on smooth and erratic series, whereas TSB suffices for intermittent series. H4: a quantile-based liquidation rule removes excess inventory at a smaller loss of fill rate than a fixed weeks-of-supply rule.

Lưu ý trung thực: trong repo, các giả thuyết này được ghi ở `05_methodology/evaluation_metrics.md` mục 7 **sau** lượt chạy đầu tiên. Nếu không chắc chúng có trước khi chạy, hãy đổi "Before running the benchmark we stated" thành "We organise the results around four working hypotheses".

## A5. Tài liệu tham khảo không được trích

- **Feddersen & Cleophas (2026):** có trong References nhưng không được trích trong bài. Hoặc xóa, hoặc trích ở Sec. 6.2 (Transparency), với điều kiện nội dung khớp với tóm tắt bài 04 trong `02_related_work/`.
- Sau khi sửa A2: nếu xóa Li (2026) thì xóa luôn khỏi References.

## A6. Case study giày dép (VNF) — hạ mức khẳng định

| TÌM | THAY |
|---|---|
| Abstract: "…liquidation pays off only at salvage prices near unit cost, which the case study confirms." | "…near unit cost; a case study with actual costs points the same way." |
| Sec. 1 (findings): "…which the case study confirms with actual costs." | "…and a case study with actual costs gives a similar range." |
| Sec. 5.5: "The case study with actual unit costs (Section 5.9) confirms this." | "The case study with actual unit costs (Section 5.9) gives a similar range, subject to its data caveats." |
| Sec. 5.9: "The case study thus repeats the M5/VN1 pattern…" | "The case study shows the same pattern in one window…" |

Đề xuất thêm:

- Chuyển Sec. 5.9 xuống Phụ lục và chỉ để 3–4 câu tóm tắt trong thân bài.
- Kiểm tra điều khoản của tạp chí về dữ liệu có giấy phép "Unknown". Nếu tạp chí không chấp nhận, bỏ case study.
