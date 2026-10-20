# Paper 24 Summary

**Nhóm:** AI model / method + M5
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn** (PDF open access trong `papers_pdf/s10845-026-02964-7.pdf`, 29 trang).

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: Feature engineering for intermittent demand forecasting: zero-detection and forecast performance across GRU, LSTM, and TCN architectures
Tác giả: Ahmed O. El-Meehy, Amin K. El-Kharbotly, Mohammed M. El-Beheiry
Năm: 2026
Nguồn: Journal of Intelligent Manufacturing (Springer)
DOI/Link: https://doi.org/10.1007/s10845-026-02964-7

## Problem

- Thước đo sai số thông thường không phản ánh được khả năng dự báo đúng các kỳ **nhu cầu bằng 0** (abstract).
- MAPE không xác định khi nhu cầu thực bằng 0 nên không phù hợp với chuỗi rời rạc; WMAPE khắc phục được, nhưng vẫn trộn lẫn phần dự báo số 0 và phần khác 0 (tr. 4).

## Method

- Đề xuất 2 thước đo **Z%** (tỷ lệ dự báo đúng kỳ bằng 0) và **NZ%** (kỳ khác 0) (abstract).
- So sánh GRU, LSTM, TCN với 20 chiến lược tạo đặc trưng (lag, zero-pattern); tổng khoảng 1.140 kịch bản (abstract).

## Dataset

- Chọn chuỗi từ **M5** theo 3 mức ADI (1,32; 1,60; 2,00), mỗi mức 7 chuỗi ngẫu nhiên; loại 2 chuỗi toàn 0 ở horizon → **19 chuỗi sản phẩm** (tr. 8).

## Evaluation

- WMAPE%, Z%, NZ%; tương quan với mức tồn kho và lượng thiếu hàng (abstract; tr. 21).

## Results

- Kết hợp đặc trưng lag và zero-pattern là cấu hình ổn định nhất; GRU và LSTM tốt hơn TCN (abstract; tr. 26).
- Z% tương quan âm với WMAPE%, mạnh hơn khi mức rời rạc tăng (r = −0,495 ở ADI ≈ 2,00) (abstract).
- **Z% cao hơn gắn với tồn kho thấp hơn nhưng rủi ro thiếu hàng cao hơn; NZ% thì ngược lại** — đánh đổi tồn kho–mức phục vụ (abstract; tr. 21–24).

## Limitations

- Tác giả nêu: chỉ dự báo điểm; dự báo xác suất và so sánh chi phí tính toán nằm ngoài phạm vi (tr. 26); chuỗi có ADI rất cao (tới 20) để lại cho nghiên cứu sau (tr. 9).
- [Nhận định nhóm] Chỉ 19 chuỗi M5.

## Relevance to our topic

[Nhận định nhóm] **Trung bình–cao.** (1) Dẫn chứng mới (2026, Springer) rằng **MAPE không dùng được** với dữ liệu nhiều số 0. (2) Cho thấy độ chính xác dự báo ở các kỳ bằng 0 tác động ngược chiều lên tồn kho và thiếu hàng, ủng hộ việc đánh giá bằng KPI tồn kho.

## Possible improvement

[Nhận định nhóm] Đề tài dùng dự báo **xác suất** (bài này để ngoài phạm vi) và toàn bộ M5 thay vì 19 chuỗi; có thể báo cáo thêm Z% như một chỉ số phụ.
