# Paper 21 Summary

**Nhóm:** Domain (inventory) + M5
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn** (PDF open access CC BY trong `papers_pdf/1-s2.0-S2949863525000548-main.pdf`, 22 trang).

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: A comparative study of multi-algorithm optimization for inventory analytics in supply chains
Tác giả: Oussama Zabraoui, Yahya Hmamou, Anas Chafi, Salaheddine Kammouri Alami
Năm: 2025
Nguồn: Supply Chain Analytics, 12, 100154
DOI/Link: https://doi.org/10.1016/j.sca.2025.100154

## Problem

- Chiến lược tồn kho truyền thống dựa trên giả định cứng nhắc hoặc một kỹ thuật duy nhất, không đáp ứng được nhu cầu biến động, lead time bất định, gián đoạn cung ứng (abstract).
- Tác giả cho rằng việc áp dụng các phương pháp này trên dữ liệu bán lẻ lớn như M5, nhất là tối ưu các KPI tồn kho, còn ít được khai thác (tr. 2).

## Method

- So sánh RL (DQN, PPO), GA, DL (LSTM), ML (XGBoost, RF) và heuristic ((s, S), Min–Max) (Bảng 2, tr. 6).
- Đề xuất **GA–DQN**: GA tối ưu tham số tĩnh (điểm đặt hàng lại, safety stock, lượng đặt Q); DQN học chính sách đặt hàng thích nghi; LSTM dự báo nhu cầu (abstract; tr. 2).
- Hàm mục tiêu: tổng chi phí tồn kho + chi phí hết hàng + chi phí đặt hàng theo thời gian (công thức (1), tr. 5).

## Dataset

- M5 (3 file sales, calendar, sell_prices; 10 cửa hàng ở CA, TX, WI) (tr. 8).
- Thực nghiệm trên **một nhóm được chọn lọc gồm các mặt hàng thực phẩm biến động mạnh** (theo độ biến động nhu cầu, hệ số biến thiên, tần suất hết hàng) (tr. 8).
- Môi trường RL xây từ **kết hợp dữ liệu thực và dữ liệu sinh tổng hợp**; mô phỏng **365 ngày** cho mỗi mặt hàng/cửa hàng (tr. 8).
- Tiền xử lý: làm mượt ngoại lai (1,5 × IQR), chuẩn hóa z-score (tr. 8).

## Evaluation

- Tồn kho: Total Inventory Cost (TIC), Service Level, Stockout Rate, Order Frequency, Bullwhip Effect; dự báo: MAE, RMSE, MAPE, R² (Bảng 2, tr. 6).
- 5 lần mô phỏng độc lập cho mỗi cấu hình (tr. 8).

## Results

- GA–DQN nâng mức phục vụ từ **61% (DQN đơn lẻ) lên 94%** và giảm chi phí (abstract); so với GA–PPO: mức phục vụ 94% so với 91%, tỷ lệ hết hàng 6% so với 25,9% (tr. 16).
- Heuristic có TIC thấp hơn GA (~8,91 triệu USD so với ~11,18 triệu USD), nhưng GA giảm mạnh hiệu ứng bullwhip (2,69 so với 9,86) (tr. 14).

## Limitations

- Tác giả tự nêu (tr. 19): chi phí huấn luyện RL lớn; DRL/DL khó diễn giải; **giả định lead time cố định** và hành vi nhà cung cấp đơn giản.
- So sánh heuristic–GA giả định lead time và giá không đổi (tr. 14).
- [Nhận định nhóm] Chỉ dùng tập con thực phẩm biến động mạnh, không phải toàn bộ M5; không có quyết định thanh lý; không phân tích theo nhóm ADI–CV²; dùng MAPE, vốn khó áp dụng khi dữ liệu có nhiều số 0.

## Relevance to our topic

[Nhận định nhóm] **Rất cao — làm yếu gap cũ.** Bài này **đã** mô phỏng tồn kho nhiều kỳ trên M5, nên nhóm không thể nói "chưa có mô phỏng tồn kho nhiều kỳ trên M5".

## Possible improvement

[Nhận định nhóm] Khác biệt còn lại: (1) quyết định **thanh lý**; (2) toàn bộ hoặc đại diện M5 **gồm cả chuỗi rời rạc**, phân tích theo nhóm ADI–CV²; (3) dự báo **xác suất (phân vị)** dẫn trực tiếp tới quyết định, thay vì RL hộp đen; (4) chính sách minh bạch, dễ giải thích cho người quản lý kho.
