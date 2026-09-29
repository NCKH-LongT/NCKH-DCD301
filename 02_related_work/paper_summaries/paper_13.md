# Paper 13 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Tóm tắt dựa trên abstract và ghi chú trong `M5_papers_baseline_gap.xlsx`. Cần đọc toàn văn để bổ sung số liệu chi tiết.

## Citation

Tên bài: End-to-end probabilistic hierarchical forecasting of large hierarchies via probabilistic top-down
Tác giả: Lorenzo Zambon, Dario Azzimonti, Giorgio Corani
Năm: 2026
Nguồn: arXiv:2606.26774
DOI/Link: https://arxiv.org/abs/2606.26774

## Problem

Tạo dự báo xác suất nhất quán giữa các cấp phân cấp mà vẫn tính toán hiệu quả ở quy mô bán lẻ (hàng trăm nghìn chuỗi).

## Method

e2eTD: chỉ dự báo các chuỗi tổng hợp cấp cao (~0,3% phân cấp, mượt hơn), rồi dùng thuật toán lấy mẫu top-down xác suất để phân bổ xuống cấp thấp.

## Dataset

M5 (~40.000 chuỗi) và Favorita (~300.000 chuỗi).

## Evaluation

Weighted scaled pinball loss trên các cấp.

## Results

WSPL thấp nhất trong các phương pháp so sánh; nếu tham gia M5 Uncertainty sẽ xếp hạng 11/892 đội. Chạy ~5 phút (M5) và ~20 phút (Favorita) trên laptop thường.

## Limitations

Chỉ dự báo trực tiếp một tập con chuỗi tổng hợp đủ mượt; chất lượng ở cấp SKU phụ thuộc vào tỷ lệ phân bổ lịch sử.

## Relevance to our topic

**Cao.** Baseline dự báo xác suất nhẹ và mạnh; cho thấy có thể làm tốt trên laptop.

## Possible improvement

Nhóm tập trung vào cấp SKU–store (cấp ra quyết định nhập/thanh lý) thay vì cấp tổng hợp.
