# Research Gap

## 1. Các bài trước đã giải quyết như thế nào?

| Nhóm | Bài | Đã làm gì |
|---|---|---|
| Dự báo trên M5 | 02, 03, 06, 08, 09, 13 | Tối ưu độ chính xác (WRMSSE, WSPL). Đội thắng M5 dùng LightGBM; hướng mới gồm foundation model, ensemble, dự báo phân cấp. |
| Nhu cầu rời rạc | 12, 15, 16, 18, 23, 24 | Croston/TSB, phân loại ADI–CV², mô hình phân phối phù hợp (Tweedie). |
| Dự báo → tồn kho | 11, 16, 19, 21, 22 | Bài 11: kết hợp dự báo xác suất theo newsvendor (một kỳ). Bài 21: mô phỏng tồn kho 365 ngày bằng LSTM + GA–DQN. Bài 22: khoảng dự báo thích nghi cho safety stock. |

## 2. Các bài trước còn hạn chế gì?

1. **Chuỗi rời rạc bị bỏ hoặc chọn lọc.** Bài 22 chỉ dùng 8.000 chuỗi bán nhiều và tự nêu thiếu chuỗi thưa/chậm; bài 21 chỉ dùng tập con thực phẩm biến động mạnh; bài 11 loại 1.587 chuỗi không có lịch sử. Trong khi 73% chuỗi M5 là intermittent (bài 01).
2. **Không có quyết định thanh lý.** Các bài 11, 21, 22 không xét quyết định xử lý hàng dư. Bài 16 liên hệ dự báo với tồn kho lỗi thời nhưng chỉ dùng dữ liệu mô phỏng.
3. **Thiếu KPI tồn kho theo nhóm ADI–CV².** Bài 01 phân loại M5 chỉ để mô tả dữ liệu; bài 22 báo cáo tỷ lệ các nhóm nhưng không có KPI tồn kho.
4. **Chính sách khó giải thích.** Bài 21 dùng RL và tự nêu DRL/DL khó diễn giải; chính sách dựa trên phân vị dự báo (newsvendor/order-up-to) minh bạch hơn (nhận định của nhóm).
5. **Hạn chế phương pháp của bài gần nhất (bài 11):** đánh giá từng kỳ độc lập, không có lead time và không mang tồn kho sang kỳ sau.

## 3. Nhóm sẽ cải tiến điểm nào?

- Giữ lại **toàn bộ nhóm nhu cầu** (kể cả intermittent và lumpy) và báo cáo kết quả **theo từng nhóm ADI–CV²**.
- Mô phỏng tồn kho **nhiều kỳ có lead time**, tồn kho mang sang kỳ sau.
- Bổ sung **quyết định thanh lý** dựa trên phân vị dự báo, bên cạnh quyết định nhập hàng.
- Dùng một mô hình **LightGBM quantile** gọn, so sánh với baseline thống kê và một mô hình sâu (TiDE/DeepAR), thay vì kết hợp nhiều mô hình.

## 4. Câu phát biểu gap (English)

> Existing studies on the M5 dataset mainly optimise point or probabilistic forecast accuracy, while the few works linking forecasts to inventory decisions either restrict the analysis to selected, high-volume or volatile series, evaluate a single period, or omit liquidation decisions. Limited attention has been given to evaluating quantile-based replenishment and liquidation policies in a multi-period simulation that retains intermittent and lumpy demand and reports inventory KPIs by demand class.


- Các bài 08, 09, 11, 12, 13 mới chỉ có trên arXiv (chưa qua phản biện).