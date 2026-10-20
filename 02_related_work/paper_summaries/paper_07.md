# Paper 07 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn bản arXiv (18 trang).**

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: The Forecast Critic: Leveraging Large Language Models for Poor Forecast Identification
Tác giả: Luke Bhan, Hanyu Zhang, Andrew Gordon Wilson, Michael W. Mahoney, Chuck Arvin
Năm: 2025
Nguồn: AAAI 2026 Workshop AI4TS (và AABA4ET) (arXiv:2512.12059)
DOI/Link: https://arxiv.org/abs/2512.12059

## Problem

- Giám sát hệ thống dự báo trong bán lẻ quy mô lớn; đánh giá liệu LLM có phát hiện được dự báo bất hợp lý hay không (abstract).

## Method

- Dùng LLM (nhiều kích cỡ, có/không reasoning, đa phương thức) đọc biểu đồ + chỉ dẫn để đánh giá dự báo là hợp lý hay không (abstract; tr. 6).

## Dataset

- Dữ liệu tổng hợp và dữ liệu thực M5 (abstract).
- M5: ở cấp sản phẩm, **lấy ngẫu nhiên 1.000 chuỗi** cùng dự báo của **Chronos**; đưa cho LLM 120 ngày lịch sử + 28 ngày dự báo (tr. 5).

## Evaluation

- F1-score (thí nghiệm tổng hợp); sCRPS (thí nghiệm M5) (abstract; tr. 5).

## Results

- Mô hình tốt nhất đạt F1 = 0,88 (con người 0,97); với ngữ cảnh khuyến mãi đạt F1 = 0,84 (abstract).
- Trên M5, dự báo bị đánh giá là bất hợp lý có sCRPS cao hơn ít nhất 10% so với dự báo hợp lý (abstract).

## Limitations

- LLM phát hiện tốt lệch xu hướng, dịch chuyển dọc nhưng khó phát hiện chu kỳ bị kéo giãn/nén; vẫn kém chuyên gia (tr. 6, Conclusion).
- [Nhận định nhóm] Chỉ 1.000 chuỗi và 1 nguồn dự báo (Chronos).

## Relevance to our topic

[Nhận định nhóm] **Thấp–trung bình.** Gợi ý bước giám sát dự báo.

## Possible improvement

[Nhận định nhóm] Future Work: kiểm tra dự báo bất thường trước khi phát lệnh nhập/thanh lý.
