# Paper 09 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Tóm tắt dựa trên abstract và ghi chú trong `M5_papers_baseline_gap.xlsx`. Cần đọc toàn văn để bổ sung số liệu chi tiết.

## Citation

Tên bài: Hierarchical Time Series Forecasting Via Latent Mean Encoding
Tác giả: Alessandro Salatiello, Stefan Birr, Manuel Kunz
Năm: 2025
Nguồn: arXiv:2506.19633
DOI/Link: https://arxiv.org/abs/2506.19633

## Problem

Tạo dự báo nhất quán (coherent) giữa nhiều mức tổng hợp thời gian.

## Method

Kiến trúc mạng phân cấp mới, mỗi module xử lý một mức tổng hợp thời gian, học mã hóa giá trị trung bình của biến mục tiêu trong lớp ẩn.

## Dataset

M5, chia train/validation/test = 1886/28/28 ngày.

## Evaluation

Sai số dự báo (abstract không nêu cụ thể).

## Results

Vượt các phương pháp đã có như TSMixer trên M5.

## Limitations

Abstract không nêu hạn chế và không có số liệu cụ thể; cần đọc toàn văn.

## Relevance to our topic

**Trung bình.** Tham khảo cách chia dữ liệu chuẩn 1886/28/28.

## Possible improvement

Nhóm dùng cùng cách chia để so sánh được với các bài khác.
