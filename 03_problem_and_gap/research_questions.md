# Research Questions

## 2. Research Questions

### RQ1

**In a multi-period inventory simulation on M5, does quantile forecasting with LightGBM achieve better inventory performance (fill rate, total cost) than point forecasts with normal-approximation safety stock, and than Seasonal Naive, TSB and a deep global model (TiDE/DeepAR)?**

Mục tiêu:

- Xây dựng pipeline dự báo xác suất 28 ngày trên dữ liệu M5 bằng LightGBM quantile.
- Xây mô phỏng tồn kho nhiều kỳ có lead time, dùng phân vị dự báo làm mức đặt hàng tối đa (order-up-to).
- Xây các baseline để so sánh: Seasonal Naive, TSB, LightGBM dự báo điểm + safety stock chuẩn, TiDE/DeepAR.
- Đánh giá bằng fill rate, tỷ lệ ngày hết hàng và tổng chi phí, kèm WRMSSE, WSPL cho phần dự báo.

### RQ2

**How does the relative performance of these methods differ across ADI–CV² demand classes (smooth, erratic, intermittent, lumpy)?**

Mục tiêu:

- Phân loại SKU theo ADI–CV² (ngưỡng ADI = 4/3, CV² = 0,5).
- Báo cáo KPI tồn kho và sai số dự báo riêng cho từng nhóm nhu cầu.
- Xác định nhóm nào AI mang lại lợi ích rõ nhất và nhóm nào baseline thống kê (TSB) vẫn đủ tốt.

### RQ3

**Does a quantile-based liquidation rule reduce overstock and holding cost compared with no liquidation and with a fixed-threshold rule, and at what cost in stockouts?**

Mục tiêu:

- Định nghĩa quy tắc thanh lý dựa trên phân vị (tồn kho vượt Q0.95 của nhu cầu trong H ngày) và mô hình chi phí thanh lý (giá thu hồi, chi phí lưu kho).
- Xây các baseline: không thanh lý và thanh lý theo ngưỡng cố định.
- Đo lượng tồn dư, chi phí lưu kho, giá trị hàng đề xuất thanh lý và số ngày hết hàng phát sinh thêm.

### RQ4

**How sensitive are the recommendations and results to the assumed cost ratio c_u/c_o and lead time?**

Mục tiêu:

- Chạy phân tích độ nhạy theo tỷ lệ chi phí c_u/c_o và lead time.
- Cho thấy khuyến nghị nhập hàng và thanh lý thay đổi thế nào theo chiến lược doanh nghiệp (ưu tiên không hết hàng hay ưu tiên ít tồn kho).
- Kiểm tra độ ổn định của kết quả qua rolling-origin backtest và giữa các cửa hàng (CA_1, TX_1, WI_1).

---

**Ghi chú:** câu hỏi "độ chính xác dự báo (WRMSSE) có dự đoán được hiệu quả tồn kho không" chưa đưa vào vì có thể trùng bài 20 (Theodorou et al., 2025). Nếu sau khi đọc bài 20 vẫn còn khoảng trống, có thể thêm thành RQ5. Mọi kết luận về chi phí phụ thuộc vào các giả định mô phỏng (lead time, c_u, c_o), vì M5 không có dữ liệu tồn kho thực.