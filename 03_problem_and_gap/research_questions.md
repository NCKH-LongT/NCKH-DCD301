# Research Questions

> Gap và đóng góp: `research_gap.md` (mục 2 và 4). `[DP]` = `code/outputs/data_profile.md`.

## 1. Main Research Question

**How do probabilistic demand forecasting methods compare when their forecasts drive a common, transparent replenishment-and-liquidation policy in two public retail benchmarks with different settings (M5: a brick-and-mortar retailer; VN1: multi-vendor e-commerce), and how do the results differ across demand classes?**

(Các phương pháp dự báo nhu cầu xác suất so với nhau thế nào khi dự báo của chúng điều khiển cùng một chính sách nhập hàng + thanh lý minh bạch, trên hai dataset bán lẻ công khai thuộc hai loại hình khác nhau, và kết quả khác nhau ra sao giữa các nhóm nhu cầu?)

## 2. Sub Research Questions

### RQ1 — Benchmark trên hai dataset

**Under a common multi-period quantile-based replenishment policy, how do LightGBM quantile regression, the M5-winning LightGBM-Tweedie point approach with normal safety stock or with conformal calibration, a second gradient-boosting implementation (HistGradientBoosting quantile), TSB (Poisson and negative binomial), ETS and an empirical baseline compare in forecast accuracy and in cost-free inventory KPIs on M5 and VN1, and do their rankings hold across the two datasets?**

Mục tiêu:

- Đưa cả hai dataset về tần suất tuần: M5 có 30.490 chuỗi item × cửa hàng; VN1 có 15.053 chuỗi client × kho × sản phẩm [DP].
- Dự báo phân vị tổng nhu cầu trong L + R tuần, đưa vào chính sách order-up-to giống nhau cho mọi phương pháp.
- Đo:
  - (a) dự báo: RMSSE, scaled quantile loss, độ phủ khoảng. **Không dùng MAPE** vì không xác định khi nhu cầu bằng 0 (bài 24, tr. 4).
  - (b) tồn kho, không có đơn vị tiền: fill rate, mức phục vụ đạt được so với mục tiêu, tỷ lệ tuần hết hàng, tồn kho trung bình tính bằng số tuần nhu cầu.
- Vẽ **đường đánh đổi tồn kho – fill rate** khi τ thay đổi; so sánh xếp hạng giữa hai dataset (tương quan hạng).

Căn cứ: LightGBM được cả top 50 M5 Accuracy dùng (bài 02, tr. 1); lời giải hạng nhất M5 Uncertainty là LightGBM theo phân vị (bài 03, tr. 14). Ngược lại, bài 12 thấy LightGBM dạng distributional kém trên dữ liệu rời rạc (tr. 13, 19); vì vậy có thêm hai đối chứng ML (conformal, HistGradientBoosting). Mô hình sâu (TiDE, DeepAR) nằm ngoài phạm vi vì lý do chi phí tính toán (`04_proposed_system/ai_model_integration.md` mục 4). Gap 1, 5.

### RQ2 — Theo nhóm nhu cầu

**How does the relative forecasting and inventory performance of these methods vary across ADI–CV² demand classes (smooth, erratic, intermittent, lumpy), and are the class-level patterns consistent between M5 and VN1?**

Mục tiêu:

- Phân loại theo ADI–CV² với ngưỡng **ADI = 4/3, CV² = 0,5** (bài 01, tr. 7–8).
- Phân bố nhóm hai dataset khác nhau rõ: M5 có 30% smooth, 10% lumpy; VN1 có 6% smooth, **31% lumpy** [DP]. Điều này cho phép kiểm tra kết luận theo nhóm có lặp lại không.
- Xác định nhóm nào dự báo xác suất bằng ML có lợi rõ nhất, nhóm nào baseline thống kê (TSB) vẫn đủ tốt.

Căn cứ: gap 2, 4.

### RQ3 — Thanh lý

**How much excess inventory does a quantile-based liquidation rule remove compared with no liquidation and with a fixed weeks-of-supply rule, at what cost in additional stockouts, and above which salvage-value ratio does liquidation become worthwhile for each demand class?**

Mục tiêu:

- Quy tắc: thanh lý phần tồn vượt Q_q của tổng nhu cầu trong H tuần tới.
- Baseline: không thanh lý; thanh lý theo ngưỡng cố định (tồn > k tuần bán trung bình).
- Đo: số đơn vị và số tuần tồn kho được giảm; số tuần hết hàng tăng thêm.
- **Ngưỡng giá thu hồi hòa vốn**: tỷ lệ giá thu hồi / giá trị hàng tối thiểu để thanh lý có lợi hơn việc giữ lại. Ngưỡng được trình bày dưới dạng **đường cong theo chi phí lưu kho**, không chọn một con số cố định.

Căn cứ: gap 3. Giả định: không mô hình hóa phản ứng của nhu cầu khi giảm giá (`problem_statement.md`, mục 6).

### RQ4 — Độ nhạy theo kịch bản

**How sensitive are method rankings and replenishment/liquidation recommendations to the target service level, the lead time and the liquidation horizon?**

Mục tiêu:

- Lưới kịch bản: τ ∈ {0,8; 0,9; 0,95} (tương đương c_o = 1, c_u ∈ {4, 9, 19} như bài 11, tr. 16); L ∈ {1, 2, 4} tuần; H ∈ {8, 13, 26} tuần.
- Kiểm tra độ ổn định qua nhiều mốc dự báo (rolling origin) và giữa hai dataset.

Căn cứ: cả hai dataset không có lead time hay chi phí thực, nên chúng được trình bày là **kịch bản**, không phải giả định về thực tế (`problem_statement.md`, mục 5).

## 3. Liên kết RQ – gap – đóng góp

| RQ | Gap (`research_gap.md`, mục 2) | Đóng góp (`research_gap.md`, mục 4) |
|---|---|---|
| RQ1 | 1, 5, 6 | 1, 2, 4 |
| RQ2 | 2, 4, 5 | 3 |
| RQ3 | 3 | 2, 4 |
| RQ4 | 1, 7 | 4 |
| (phụ lục: dataset Việt Nam) | — | 5 |

---

**Ghi chú:**

- **Không** đặt RQ dạng "độ chính xác dự báo có tương quan với hiệu quả tồn kho trên M5 không", vì có thể trùng bài 20 và W3, hai bài nhóm chưa đọc được.
- Dataset giày dép Việt Nam chỉ được mô tả ở phụ lục, **không** dùng để trả lời RQ1–RQ4.
