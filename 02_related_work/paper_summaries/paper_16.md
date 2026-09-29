# Paper 16 Summary

**Nhóm:** AI model / method (+ domain)
**Mức kiểm chứng (29/09/2026):** ⚠️ **Chỉ đọc được abstract** (qua OpenAlex). Bản mở có trên kho Salford và Groningen nhưng bị chặn khi tải tự động → nhóm có thể tự tải bằng trình duyệt.

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: Intermittent demand: Linking forecasting to inventory obsolescence
Tác giả: Ruud H. Teunter, Aris A. Syntetos, M. Zied Babai
Năm: 2011
Nguồn: European Journal of Operational Research, 214(3), 606–615
DOI/Link: https://doi.org/10.1016/j.ejor.2011.05.018

## Problem

- Croston là phương pháp chuẩn cho nhu cầu rời rạc nhưng có 2 nhược điểm: (1) không cập nhật sau các kỳ nhu cầu bằng 0 → không phù hợp với vấn đề **lỗi thời (obsolescence)**; (2) bị lệch dương. SBA đã xử lý (2) (abstract).

## Method

- Phương pháp mới (thường gọi là TSB): **không lệch** và cập nhật **xác suất có nhu cầu** thay vì khoảng cách giữa các lần có nhu cầu, cập nhật **mỗi kỳ** (abstract).

## Dataset

- **Thí nghiệm mô phỏng** quy mô lớn (abstract).

## Evaluation

- [Chưa kiểm chứng] Metric cụ thể không có trong abstract.

## Results

- Phương pháp mới cho hiệu năng vượt trội và giúp hiểu mối liên hệ giữa dự báo nhu cầu và lỗi thời (abstract).

## Limitations

- [Nhận định nhóm] Chỉ có bằng chứng mô phỏng (theo abstract); mô hình thống kê cục bộ, không dùng biến ngoại sinh.

## Relevance to our topic

[Nhận định nhóm] **Rất cao.** Cơ sở lý thuyết nối dự báo với tồn kho lỗi thời → khuyến nghị THANH LÝ.

## Possible improvement

[Nhận định nhóm] Dùng TSB làm baseline mạnh cho nhóm SKU rời rạc.
