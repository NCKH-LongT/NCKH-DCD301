# Paper 18 Summary

**Nhóm:** Domain (inventory)
**Mức kiểm chứng (29/09/2026):** ⚠️ **Chỉ đọc được abstract** (qua OpenAlex). Bản mở trên kho Salford bị chặn khi tải tự động.

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: On the categorization of demand patterns
Tác giả: A. A. Syntetos, J. E. Boylan, J. D. Croston
Năm: 2005
Nguồn: Journal of the Operational Research Society, 56(5), 495–503
DOI/Link: https://doi.org/10.1057/palgrave.jors.2601841

## Problem

- Phân loại mẫu nhu cầu giúp chọn phương pháp dự báo; thực tế ngành phần mềm tồn kho thường phân loại tùy ý (abstract).

## Method

- So sánh trực tiếp các phương pháp dựa trên sai số lý thuyết (MSE) để xác định vùng vượt trội, rồi định nghĩa mẫu nhu cầu; xét **EWMA, Croston và phương pháp thay thế của hai tác giả đầu** (tức SBA) (abstract).
- Quy tắc phân loại theo **khoảng cách trung bình giữa các lần có nhu cầu (ADI)** và **bình phương hệ số biến thiên kích thước nhu cầu (CV²)** (abstract).

## Dataset

- Kiểm chứng trên **3.000 chuỗi nhu cầu rời rạc thực** từ ngành ô tô (abstract).

## Evaluation

- MSE lý thuyết (abstract).

## Results

- Đề xuất quy tắc phân loại theo ADI và CV² (abstract).
- Ngưỡng ADI = 1,32: [Nguồn thứ cấp: bài 12, tr. 10] gọi là "ngưỡng phổ biến ADI > 1,32".
- [Chưa kiểm chứng] Ngưỡng CV² = 0,49 và tên 4 nhóm (smooth/erratic/intermittent/lumpy) — cần mở toàn văn.

## Limitations

- [Nguồn thứ cấp: bài 12, tr. 10] Ngưỡng ADI > 1,32 chỉ được đưa ra để phân biệt giữa các phương pháp dự báo đơn giản, **không** phải định nghĩa tính rời rạc.

## Relevance to our topic

[Nhận định nhóm] **Rất cao.** Khung phân tích kết quả theo loại nhu cầu.

## Possible improvement

[Nhận định nhóm] Khi dùng, nêu rõ ngưỡng là quy ước chọn phương pháp, không phải định nghĩa (theo phản biện ở bài 12).
