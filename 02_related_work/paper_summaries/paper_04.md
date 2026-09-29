# Paper 04 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn bản preprint arXiv v1 (2024, 44 trang)** + abstract bản chính thức HICSS 2026 (ScholarSpace). Lưu ý: hai bản có tên và số liệu khác nhau (xem bên dưới).

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: Interpretability and Control in Forecasting Support Systems (bản HICSS 2026); preprint arXiv: "Algorithmic Transparency in Forecasting Support Systems"
Tác giả: Leif Feddersen, Catherine Cleophas (bản HICSS); bản arXiv chỉ có Leif Feddersen
Năm: 2026 (HICSS); preprint 2024
Nguồn: Proceedings of the 59th Hawaii International Conference on System Sciences (HICSS 2026)
DOI/Link: https://doi.org/10.24251/HICSS.2026.172 · arXiv: https://arxiv.org/abs/2411.00699

## Problem

- Các tổ chức thường chỉnh tay dự báo thống kê; giao diện hệ thống hỗ trợ dự báo (FSS) là đòn bẩy để khuyến khích chỉnh sửa có lợi, hạn chế chỉnh sửa có hại (abstract arXiv).

## Method

- Tổng quan tài liệu về dự báo phán đoán và thiết kế FSS; thử nghiệm **3 thiết kế FSS** khác nhau về mức minh bạch dựa trên phân rã chuỗi thời gian (abstract arXiv).
- Mô hình dự báo nền là **Prophet** (tr. 16–17, mục 4.1).
- Bản HICSS gọi 3 thiết kế là Opaque, Interpretable (hiển thị phân rã) và Control (cho người dùng chỉnh tham số thành phần) (abstract HICSS).

## Dataset

- Subset M5 tập trung vào nhóm **"foods"**; chọn **10 chuỗi thời gian**, horizon **14 ngày** (tr. 17, mục 4.3).
- Người tham gia tuyển qua mTurk, lọc người ở Mỹ có vai trò quản lý/bán hàng (tr. 17, mục 4.4).
- Bản arXiv: sau khi lọc còn **75 / 77 / 78** người cho 3 nhóm (Bảng 1, tr. 26). Bản HICSS: n = 197 (abstract HICSS).

## Evaluation

- Các chỉ số: Adjustment Volume và các chỉ số khác về chỉnh sửa, độ chính xác, mức hài lòng tự báo cáo (tr. 17–18, mục 4.6).

## Results

- Minh bạch làm giảm phương sai và lượng chỉnh sửa có hại; cho người dùng tự chỉnh các thành phần minh bạch dẫn tới chỉnh sửa biến động lớn và có hại nhất (abstract arXiv).
- Kết luận (tr. 33): minh bạch **không** làm dự báo chính xác hơn hay hài lòng hơn một cách có ý nghĩa thống kê, nhưng giảm số lần chỉnh sửa và cho phương sai sai số thấp nhất.

## Limitations

- Rủi ro làm người dùng quá tải khi thiếu đào tạo; cần đào tạo kèm theo (abstract arXiv; tr. 33).
- [Nhận định nhóm] Chỉ 10 chuỗi và 1 mô hình (Prophet).

## Relevance to our topic

[Nhận định nhóm] **Trung bình.** Liên quan tới thiết kế dashboard khuyến nghị.

## Possible improvement

[Nhận định nhóm] Dashboard hiển thị lý do khuyến nghị ở mức vừa đủ, không cho chỉnh trực tiếp tham số mô hình.
