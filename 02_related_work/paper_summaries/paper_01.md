# Paper 01 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ⚠️ **Chỉ đọc được abstract** (qua OpenAlex). Toàn văn trên ScienceDirect là open access nhưng trang yêu cầu CAPTCHA khi truy cập tự động → **nhóm cần tự mở bằng trình duyệt để kiểm tra các mục [Chưa kiểm chứng]**.

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: The M5 competition: Background, organization, and implementation
Tác giả: Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos
Năm: 2022
Nguồn: International Journal of Forecasting, 38(4), 1325–1336
DOI/Link: https://doi.org/10.1016/j.ijforecast.2021.07.007

## Problem

- Cuộc thi M5 tập trung vào dự báo doanh số bán lẻ: tạo dự báo điểm chính xác nhất cho **42.840 chuỗi thời gian** doanh số phân cấp của Walmart, đồng thời ước lượng độ bất định của dự báo (abstract).

## Method

- Bài **không đề xuất mô hình**; mô tả bối cảnh, cách tổ chức và triển khai cuộc thi, gồm 2 nhánh song song: **Accuracy** và **Uncertainty** (abstract).
- M5 mở rộng các cuộc thi M trước ở 5 điểm: (a) nhiều phương pháp tham gia hơn, đặc biệt là machine learning; (b) đánh giá cả phân phối bất định; (c) có biến ngoại sinh/giải thích; (d) chuỗi thời gian phân nhóm, tương quan; (e) tập trung vào chuỗi có tính **rời rạc (intermittency)** (abstract).
- [Chưa kiểm chứng] Con số "24 benchmark" ghi trong file Excel ban đầu — cần mở toàn văn.

## Dataset

- 42.840 chuỗi doanh số phân cấp của Walmart (abstract).
- Cấp thấp nhất gồm 30.490 chuỗi (3.049 sản phẩm × 10 cửa hàng, 1.941 ngày) [Nguồn thứ cấp: bài 11, tr. 16]; 3 ngành hàng Hobbies, Foods, Household [Nguồn thứ cấp: bài 05, tr. 4].

## Evaluation

- [Nguồn thứ cấp: bài 08, tr. 13–14] RMSSE (dạng có trọng số — WRMSSE) là thước đo chính thức của nhánh Accuracy; scaled multi-quantile loss dạng có trọng số (WSPL) là thước đo chính của nhánh Uncertainty.

## Results

- Bài mang tính giới thiệu, làm tài liệu nền để hiểu kết quả hai nhánh thi (abstract). Kết quả nằm ở bài 02 và 03.

## Limitations

- [Nhận định nhóm] Bộ dữ liệu M5 gồm doanh số, lịch và giá bán — **không có tồn kho, lead time, chi phí**. Doanh số bằng 0 có thể do hết hàng (nhu cầu bị che khuất). Điều này kiểm chứng được bằng cách mở các file dữ liệu M5 trên Kaggle, không phải nội dung bài báo.

## Relevance to our topic

[Nhận định nhóm] **Cao.** Nguồn chính thức để mô tả dataset trong phần Dataset.

## Possible improvement

[Nhận định nhóm] Bổ sung lớp mô phỏng tồn kho có tham số để dùng M5 cho bài toán ra quyết định.
