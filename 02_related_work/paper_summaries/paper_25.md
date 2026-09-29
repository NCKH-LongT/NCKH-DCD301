# Paper 25 Summary

**Nhóm:** Domain (spare parts) — tham khảo phụ
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn** (PDF open access trong `papers_pdf/engproc-143-00030.pdf`, 9 trang).

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: Forecasting Critical Spare Parts Demand in Combined Cycle Power Plant Using Ensemble Learning
Tác giả: Brian Qaedi Laksono Putra, Jerry Dwi Trijoyo Purnomo
Năm: 2026
Nguồn: Engineering Proceedings (MDPI), 143, 30 — kỷ yếu hội nghị ETLTC 2026
DOI/Link: https://doi.org/10.3390/engproc2026143030

## Problem

- Nhu cầu phụ tùng quan trọng ở nhà máy điện chu trình hỗn hợp thưa, rời rạc, phi tuyến; dự báo sai gây tồn kho dư hoặc thiếu hàng (abstract).

## Method

- Random Forest và XGBoost (có tinh chỉnh) (abstract; tr. 2).

## Dataset

- Dữ liệu mua và sử dụng phụ tùng 2020–2024 của một nhà máy, gộp theo tháng; nhiều mặt hàng chọn theo lấy mẫu có chủ đích dựa trên độ đầy đủ dữ liệu (tr. 2).

## Evaluation

- RMSE, MAE, MAPE; **loại các kỳ thực tế bằng 0 khỏi MAPE** (abstract).

## Results

- XGBoost tốt hơn Random Forest: RMSE 0,831 so với 1,032; MAE 0,106 so với 0,139; MAPE 9,25 so với 9,91 (Bảng 1, tr. 5).

## Limitations

- [Nhận định nhóm] Một nhà máy, số mặt hàng nhỏ, không phải bán lẻ; không đánh giá KPI tồn kho; phải loại số 0 khỏi MAPE, cho thấy MAPE không phù hợp với dữ liệu rời rạc.

## Relevance to our topic

[Nhận định nhóm] **Thấp.** Chỉ dùng làm ví dụ phụ; không nên dùng làm trụ cột. Đây là kỷ yếu hội nghị nên mức uy tín thấp hơn các tạp chí như IJF, EJOR, JORS.

## Possible improvement

[Nhận định nhóm] —
