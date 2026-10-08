# Research Questions

> Gap và đóng góp: `research_gap.md` (mục 2 và 4). `[DP]` = `code/outputs/data_profile.md`.

## 1. Main Research Question

**How do probabilistic demand forecasting methods compare when their forecasts drive a common, transparent replenishment-and-liquidation policy across two retail domains (US grocery/household — M5; Vietnamese footwear — Vietnam Datathon 2023), and how do the results differ across demand classes?**

(Các phương pháp dự báo nhu cầu xác suất so với nhau thế nào khi dự báo của chúng điều khiển cùng một chính sách nhập hàng + thanh lý minh bạch trên hai miền bán lẻ, và kết quả khác nhau ra sao giữa các nhóm nhu cầu?)

## 2. Sub Research Questions

### RQ1 — Benchmark trên hai miền

**Under a common multi-period quantile-based replenishment policy, how do LightGBM quantile regression, the M5-winning LightGBM-Tweedie point approach with normal safety stock, TSB, ETS/Seasonal Naive, and a deep global model (TiDE or DeepAR) compare in forecast accuracy and inventory performance on M5 and on the Vietnamese dataset, and do their rankings hold across the two domains?**

Mục tiêu:

- Đưa cả hai dataset về tần suất tuần: M5 item × cửa hàng (30.490 chuỗi), Việt Nam mẫu–màu × toàn chuỗi (1.006 chuỗi) [DP].
- Dự báo phân vị tổng nhu cầu trong L + R tuần, đưa vào chính sách order-up-to giống nhau cho mọi phương pháp.
- Đo: (a) dự báo — RMSSE, scaled quantile loss, độ phủ khoảng; (b) tồn kho — fill rate, tỷ lệ tuần hết hàng, tồn trung bình, tổng chi phí. **Không dùng MAPE** (không xác định khi nhu cầu bằng 0, bài 24, tr. 4).
- So sánh xếp hạng giữa hai dataset (ví dụ hệ số tương quan hạng).

Căn cứ: LightGBM được cả top 50 M5 Accuracy dùng (bài 02, tr. 1), lời giải hạng nhất M5 Uncertainty là LightGBM theo phân vị (bài 03, tr. 14); ngược lại bài 12 thấy LightGBM dạng distributional kém trên dữ liệu rời rạc (tr. 13, 19). Gap 1, 5.

### RQ2 — Theo nhóm nhu cầu

**How does the relative forecasting and inventory performance of these methods vary across ADI–CV² demand classes (smooth, erratic, intermittent, lumpy), and are these class-level patterns consistent between the two datasets?**

Mục tiêu:

- Phân loại theo ADI–CV² với ngưỡng **ADI = 4/3, CV² = 0,5** (bài 01, tr. 7–8).
- Báo cáo KPI và sai số theo từng nhóm cho từng dataset. Phân bố nhóm hai dataset khác nhau: M5 theo tuần có 57% intermittent, 30% smooth; Việt Nam có 35% intermittent, 33% lumpy, 22% erratic, 10% smooth [DP].
- Xác định nhóm nào dự báo xác suất bằng ML có lợi rõ nhất, nhóm nào baseline thống kê (TSB) vẫn đủ tốt.

Căn cứ: gap 2, 4.

### RQ3 — Thanh lý

**Does a quantile-based liquidation rule reduce overstock and total cost compared with no liquidation and with a fixed weeks-of-supply rule, and how many additional stockouts does it cause, in each dataset?**

Mục tiêu:

- Quy tắc: thanh lý phần tồn vượt Q_q của tổng nhu cầu trong H tuần tới, với giá thu hồi s.
- Baseline: không thanh lý; thanh lý theo ngưỡng cố định (ví dụ tồn > k tuần bán trung bình).
- Đo: lượng và giá trị hàng thanh lý, tồn trung bình, chi phí lưu kho, lỗ thanh lý, số tuần hết hàng phát sinh thêm.
- Với dữ liệu Việt Nam, đặt giá thu hồi và chi phí lưu kho theo giá vốn/giá bán thực [DP].

Căn cứ: gap 3. Giả định: không mô hình hóa phản ứng của nhu cầu khi giảm giá (`problem_statement.md`, mục 5).

### RQ4 — Độ nhạy

**How sensitive are the method rankings and the replenishment/liquidation recommendations to the cost ratio c_u/c_o, the lead time, and the liquidation horizon?**

Mục tiêu:

- Lưới tham số: τ = c_u/(c_u + c_o) ∈ {0,8; 0,9; 0,95} (giống bài 11, tr. 16); L ∈ {1, 2, 4} tuần; H ∈ {8, 13, 26} tuần.
- Kiểm tra độ ổn định qua nhiều mốc dự báo (rolling origin) và giữa hai dataset.

Căn cứ: M5 không có dữ liệu tồn kho thực nên chi phí và lead time là giả định (`problem_statement.md`, mục 5).

## 3. Liên kết RQ – gap – đóng góp

| RQ | Gap (`research_gap.md`, mục 2) | Đóng góp (`research_gap.md`, mục 4) |
|---|---|---|
| RQ1 | 1, 5, 6 | 1, 2 |
| RQ2 | 2, 4, 5 | 3 |
| RQ3 | 3 | 2 |
| RQ4 | 1, 7 | 4 |
| (mô tả dataset Việt Nam) | 5 | 5 |

---

**Ghi chú:**

- **Không** đặt RQ dạng "độ chính xác dự báo có tương quan với hiệu quả tồn kho trên M5 không", vì có thể trùng bài 20 và W3, hai bài nhóm chưa đọc được.
- Kết luận về chi phí phụ thuộc giả định mô phỏng. Với dữ liệu Việt Nam, tồn kho thực chỉ dùng để mô tả cho tới khi xác minh tính đầy đủ của doanh số.
