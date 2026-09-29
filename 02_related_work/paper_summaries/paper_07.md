# Paper 07 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Metadata và link **đã được kiểm tra (2026-09-29)** qua Crossref / arXiv API; link mở được. Tóm tắt dựa trên abstract, ghi chú `M5_papers_baseline_gap.xlsx` và đối chiếu PDF ở các chi tiết về dataset. Cần đọc toàn văn để bổ sung số liệu kết quả.

## Citation

Tên bài: The Forecast Critic: Leveraging Large Language Models for Poor Forecast Identification
Tác giả: Luke Bhan, Hanyu Zhang, Andrew Gordon Wilson, Michael W. Mahoney, Chuck Arvin
Năm: 2025
Nguồn: AAAI 2026 Workshop AI4TS (và AABA4ET); arXiv:2512.12059
DOI/Link: https://arxiv.org/abs/2512.12059

## Problem

Doanh nghiệp bán lẻ cần tự động giám sát chất lượng dự báo. LLM có phát hiện được dự báo bất hợp lý mà không cần huấn luyện riêng không?

## Method

Dùng LLM (nhiều kích cỡ, có/không reasoning, đa phương thức) để chấm dự báo của Chronos là hợp lý hay không.

## Dataset

Dữ liệu tổng hợp + 1.000 chuỗi mẫu từ M5.

## Evaluation

F1-score; sCRPS.

## Results

LLM tốt nhất đạt F1 = 0,88 (con người 0,97); có ngữ cảnh khuyến mãi đạt F1 = 0,84. Trên M5, các dự báo bị đánh dấu bất hợp lý có sCRPS cao hơn ít nhất 10%.

## Limitations

Chỉ 1.000 chuỗi và một nguồn dự báo (Chronos); vẫn kém con người.

## Relevance to our topic

**Thấp–trung bình.** Gợi ý một bước giám sát chất lượng dự báo trước khi đưa ra khuyến nghị.

## Possible improvement

Future Work: thêm module kiểm tra dự báo bất thường trước khi phát lệnh nhập/thanh lý.
