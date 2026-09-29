# Research Questions

## 1. Main Research Question

**How can probabilistic (quantile) demand forecasts be translated into transparent replenishment and liquidation decisions for retail SKU–store series on the M5 dataset, including intermittent and lumpy demand, and how do these decisions perform in terms of inventory KPIs?**

(Làm thế nào để chuyển dự báo nhu cầu dạng phân vị thành quyết định nhập hàng và thanh lý minh bạch cho từng SKU–store trên M5, kể cả nhu cầu rời rạc và lumpy, và các quyết định này đạt hiệu quả tồn kho ra sao?)

## 2. Sub Research Questions

### RQ1

**In a multi-period inventory simulation on M5, does quantile forecasting with LightGBM achieve better inventory performance (fill rate, total cost) than point forecasts with normal-approximation safety stock, and than Seasonal Naive, TSB and a deep global model (TiDE/DeepAR)?**

Mục tiêu:

- Xây dựng pipeline dự báo xác suất 28 ngày trên dữ liệu M5 bằng LightGBM quantile.
- Xây mô phỏng tồn kho nhiều kỳ có lead time, dùng phân vị dự báo làm mức đặt hàng tối đa (order-up-to).
- Xây các baseline để so sánh: Seasonal Naive, TSB, LightGBM dự báo điểm + safety stock chuẩn, TiDE/DeepAR.
- Đánh giá bằng fill rate, tỷ lệ ngày hết hàng và tổng chi phí; kèm WRMSSE và WSPL cho phần dự báo (không dùng MAPE, vì MAPE không xác định khi nhu cầu bằng 0, bài 24, tr. 4).

Căn cứ:

- LightGBM được cả top 50 M5 Accuracy dùng (bài 02, tr. 1). Lời giải hạng nhất M5 Uncertainty huấn luyện LightGBM theo từng phân vị (bài 03, tr. 14).
- Ngược lại, bài 12 cho thấy LightGBM dạng distributional kém trên dữ liệu rời rạc, còn TiDE + Tweedie tốt nhất (tr. 13, 19). Vì vậy cần TiDE/DeepAR làm baseline.

### RQ2

**How does the relative performance of these methods differ across ADI–CV² demand classes (smooth, erratic, intermittent, lumpy)?**

Mục tiêu:

- Phân loại SKU theo ADI–CV², dùng ngưỡng **ADI = 4/3 và CV² = 0,5** như bài 01 (tr. 7–8), để so sánh được với tỷ lệ nhóm của M5 (73% intermittent, 17% lumpy, 3% erratic, 7% smooth).
- Báo cáo KPI tồn kho và sai số dự báo riêng cho từng nhóm nhu cầu.
- Xác định nhóm nào dự báo xác suất bằng AI mang lại lợi ích rõ nhất, và nhóm nào baseline thống kê (TSB) vẫn đủ tốt.

Căn cứ: gap 2 và 4 trong `research_gap.md`.

### RQ3

**Does a quantile-based liquidation rule reduce overstock and holding cost compared with no liquidation and with a fixed-threshold rule, and at what cost in stockouts?**

Mục tiêu:

- Định nghĩa quy tắc thanh lý dựa trên phân vị (tồn kho vượt Q0.95 của nhu cầu trong H ngày) và mô hình chi phí thanh lý (giá thu hồi, chi phí lưu kho).
- Xây các baseline: không thanh lý, và thanh lý theo ngưỡng cố định.
- Đo lượng tồn dư, chi phí lưu kho, giá trị hàng đề xuất thanh lý và số ngày hết hàng phát sinh thêm.

Căn cứ: gap 3 trong `research_gap.md`. Giả định: không mô hình hóa phản ứng của nhu cầu khi giảm giá (`problem_statement.md`, mục 4).

### RQ4

**How sensitive are the recommendations and results to the assumed cost ratio c_u/c_o and lead time?**

Mục tiêu:

- Chạy phân tích độ nhạy theo tỷ lệ chi phí c_u/c_o và lead time.
- Cho thấy khuyến nghị nhập hàng và thanh lý thay đổi thế nào theo chiến lược doanh nghiệp (ưu tiên không hết hàng hay ưu tiên ít tồn kho).
- Kiểm tra độ ổn định của kết quả qua rolling-origin backtest và giữa các cửa hàng (CA_1, TX_1, WI_1).

Căn cứ: M5 không có dữ liệu tồn kho thực nên chi phí và lead time là tham số giả định (`problem_statement.md`, mục 4). Bài 11 cũng thử nhiều mức chi phí c1 = 1, c2 ∈ {4, 9, 19} (tr. 16).

## 3. Liên kết RQ – gap – đóng góp

| RQ | Gap (`research_gap.md`, mục 2) | Đóng góp (`research_gap.md`, mục 4) |
|---|---|---|
| RQ1 | 1, 5, 6 | 1, 2 |
| RQ2 | 2, 4 | 3 |
| RQ3 | 3 | 1, 2 |
| RQ4 | (giả định mô phỏng) | 4 |

---

**Ghi chú:**

- Câu hỏi "độ chính xác dự báo (WRMSSE) có dự đoán được hiệu quả tồn kho không" **không đưa vào**, vì có thể trùng bài 20 (Theodorou et al., 2025). Bài này không đọc được toàn văn nên nhóm quyết định không đặt RQ theo hướng này (xem `02_related_work/paper_summaries/paper_20.md`).
- Mọi kết luận về chi phí phụ thuộc vào các giả định mô phỏng (lead time, c_u, c_o), vì M5 không có dữ liệu tồn kho thực.
