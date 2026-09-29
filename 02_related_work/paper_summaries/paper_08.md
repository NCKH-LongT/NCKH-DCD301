# Paper 08 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Metadata và link **đã được kiểm tra (2026-09-29)** qua Crossref / arXiv API; link mở được. Tóm tắt dựa trên abstract, ghi chú `M5_papers_baseline_gap.xlsx` và đối chiếu PDF ở các chi tiết về dataset. Cần đọc toàn văn để bổ sung số liệu kết quả.

## Citation

Tên bài: The cost of ensembling: is it always worth combining?
Tác giả: Marco Zanotti
Năm: 2025
Nguồn: arXiv:2506.04677
DOI/Link: https://arxiv.org/abs/2506.04677

## Problem

Ensemble có đáng với chi phí tính toán bỏ ra không?

## Method

10 mô hình cơ sở, 8 cấu hình ensemble, dự báo điểm và xác suất, với nhiều tần suất huấn luyện lại.

## Dataset

M5 và VN1.

## Evaluation

Độ chính xác dự báo điểm và xác suất; chi phí tính toán.

## Results

Ensemble cải thiện độ chính xác (đặc biệt với dự báo xác suất) nhưng tốn kém. Ensemble nhỏ 2–3 mô hình thường đã gần tối ưu, và giảm tần suất huấn luyện lại tiết kiệm nhiều chi phí mà ít mất độ chính xác.

## Limitations

Chỉ dữ liệu bán lẻ; không đánh giá ở tầng quyết định.

## Relevance to our topic

**Trung bình–cao.** Hỗ trợ lập luận chọn mô hình gọn, và cho biết có thể huấn luyện lại theo tuần thay vì theo ngày.

## Possible improvement

Báo cáo thời gian huấn luyện/suy luận như một metric hệ thống; thử tần suất huấn luyện lại hàng tuần.
