# Paper 02 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ⚠️ **Chỉ đọc được abstract** (qua OpenAlex). Toàn văn open access trên ScienceDirect nhưng bị CAPTCHA khi truy cập tự động → nhóm cần tự mở bằng trình duyệt.

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: M5 accuracy competition: Results, findings, and conclusions
Tác giả: Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos
Năm: 2022
Nguồn: International Journal of Forecasting, 38(4), 1346–1364
DOI/Link: https://doi.org/10.1016/j.ijforecast.2021.11.013

## Problem

- Trình bày kết quả nhánh **Accuracy** của M5: dự báo chính xác 42.840 chuỗi doanh số phân cấp của Walmart (abstract).

## Method

- Cuộc thi yêu cầu nộp **30.490 dự báo điểm** ở cấp thấp nhất, sau đó cộng dồn để có dự báo cho các cấp cao hơn (abstract).
- Bài trình bày chi tiết triển khai, kết quả, các phương pháp tốt nhất và tổng kết phát hiện chính (abstract).
- [Nguồn thứ cấp: bài 12, tr. 6] LightGBM là một phần của các bài nộp thành công ở M5, ví dụ khi kết hợp với loss Tweedie. [Nguồn thứ cấp: bài 06, tr. 4] LightGBM được dùng rộng rãi trong các lời giải M5.
- [Chưa kiểm chứng] Nhận định "LightGBM/ML thắng áp đảo so với benchmark thống kê" — cần đọc toàn văn bài này để trích đúng.

## Dataset

- M5 (Walmart), 42.840 chuỗi (abstract).

## Evaluation

- [Nguồn thứ cấp: bài 06, tr. 4; bài 08, tr. 13] WRMSSE, horizon 28 ngày.

## Results

- [Chưa kiểm chứng] Thứ hạng, mức cải thiện so với benchmark, đặc điểm của các đội thắng — cần đọc toàn văn.

## Limitations

- [Chưa kiểm chứng] Ghi chú trong Excel ban đầu ("chỉ phân tích top 50 đội; nhiều đội không công bố chi tiết") — cần đọc toàn văn.
- [Nhận định nhóm] Đánh giá bằng sai số dự báo, không gắn với chi phí tồn kho.

## Relevance to our topic

[Nhận định nhóm] **Rất cao.** Cơ sở để chọn mô hình global dạng GBDT — nhưng phải trích từ toàn văn, không từ bản tóm tắt này.

## Possible improvement

[Nhận định nhóm] Kiểm tra xem độ chính xác dự báo có chuyển thành hiệu quả tồn kho hay không.
