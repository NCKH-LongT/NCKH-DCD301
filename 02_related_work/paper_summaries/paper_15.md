# Paper 15 Summary

**Nhóm:** AI model / method
**Mức kiểm chứng (29/09/2026):** ⚠️ **Chỉ đọc được abstract** (bài closed access, không có bản mở).

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: Forecasting and stock control for intermittent demands
Tác giả: J. D. Croston
Năm: 1972
Nguồn: Journal of the Operational Research Society (lúc đó tên là Operational Research Quarterly), 23(3), 289–303
DOI/Link: https://doi.org/10.1057/jors.1972.50

## Problem

- Làm mịn hàm mũ thường dùng trong hệ thống kiểm soát tồn kho; với nhu cầu rời rạc, nó gần như luôn cho mức tồn kho không phù hợp — nhu cầu cố định theo chu kỳ có thể sinh mức tồn tới gấp đôi mức cần (abstract).

## Method

- Dùng **ước lượng riêng** cho kích thước nhu cầu và tần suất nhu cầu (abstract).

## Dataset

- [Chưa kiểm chứng] Không có trong abstract.

## Evaluation

- [Chưa kiểm chứng] Không có trong abstract.

## Results

- Quy tắc đặt tồn kho an toàn cũng phải điều chỉnh để có mức bảo vệ nhất quán trước hết hàng (abstract).

## Limitations

- [Nguồn thứ cấp: bài 16, abstract] Phương pháp Croston không cập nhật sau các kỳ nhu cầu bằng 0 nên không phù hợp khi sản phẩm lỗi thời, và bị lệch dương (positively biased).

## Relevance to our topic

[Nhận định nhóm] **Cao.** Baseline chuẩn cho SKU nhu cầu rời rạc.

## Possible improvement

[Nhận định nhóm] Dùng làm baseline thống kê.
