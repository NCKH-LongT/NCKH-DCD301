# Paper 11 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Tóm tắt dựa trên abstract và ghi chú trong `M5_papers_baseline_gap.xlsx`. Cần đọc toàn văn để bổ sung số liệu chi tiết.

## Citation

Tên bài: Multi-objective probabilistic forecast combination for inventory demand
Tác giả: Shengjie Wang, Yanfei Kang, Evangelos Spiliotis, Fotios Petropoulos
Năm: 2026
Nguồn: arXiv:2606.04900
DOI/Link: https://arxiv.org/abs/2606.04900

## Problem

Kết hợp dự báo xác suất thường chỉ tối ưu độ chính xác thống kê, trong khi độ chính xác cao hơn không nhất thiết dẫn tới quyết định tồn kho tốt hơn, nhất là khi chi phí phi tuyến và có nhiều mục tiêu mâu thuẫn.

## Method

Bài toán kết hợp dự báo được đặt thành tối ưu đa mục tiêu (độ chính xác + hiệu quả quyết định tồn kho), sinh ra tập Pareto các trọng số kết hợp.

## Dataset

Walmart (M5; theo ghi chú nhóm, còn 28.903/30.490 SKU sau khi loại các SKU toàn số 0) và dữ liệu phụ tùng Royal Air Force.

## Evaluation

Độ chính xác dự báo và hiệu quả quyết định tồn kho, so với mô hình đơn lẻ, trung bình đơn giản và tối ưu đơn mục tiêu.

## Results

Cách tiếp cận đa mục tiêu cho hiệu năng cân bằng và ổn định hơn các phương pháp so sánh.

## Limitations

Loại 1.587 SKU toàn số 0 khi ước lượng trọng số; cần nhiều mô hình cơ sở để kết hợp (tốn kém); chỉ tập trung vào phía nhập hàng, không có quyết định xử lý hàng dư.

## Relevance to our topic

**Rất cao. Đây là bài gần nhất với đề tài**, phải so sánh và phân biệt rõ trong Related Work.

## Possible improvement

Nhóm khác biệt ở chỗ: (1) một mô hình quantile duy nhất thay vì kết hợp nhiều mô hình; (2) quyết định **hai chiều** (nhập + thanh lý); (3) **giữ lại** SKU nhu cầu thưa và phân tích riêng theo nhóm ADI–CV².
