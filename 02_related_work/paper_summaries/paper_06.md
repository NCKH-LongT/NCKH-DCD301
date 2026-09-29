# Paper 06 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Tóm tắt dựa trên abstract và ghi chú trong `M5_papers_baseline_gap.xlsx`. Cần đọc toàn văn để bổ sung số liệu chi tiết.

## Citation

Tên bài: Foundation Models for Demand Forecasting via Dual-Strategy Ensembling
Tác giả: Wei Yang, Defu Cao, Yan Liu
Năm: 2025
Nguồn: KDD Workshop / arXiv:2507.22053
DOI/Link: https://arxiv.org/abs/2507.22053

## Problem

Foundation model cho dự báo nhu cầu gặp khó khăn với cấu trúc phân cấp, dịch chuyển miền (domain shift) và yếu tố ngoại sinh thay đổi.

## Method

Hierarchical Ensemble (chia theo store/category/department) + Architectural Ensemble (kết hợp LightGBM, DNN, DeepAR, PatchTST, TEMPO, Chronos).

## Dataset

M5 + 3 dataset bán lẻ khác (in-domain và zero-shot).

## Evaluation

Sai số dự báo trên các cấp phân cấp.

## Results

Vượt các baseline mạnh một cách nhất quán và cải thiện độ chính xác ở nhiều cấp phân cấp.

## Limitations

Trọng số kết hợp cố định, chưa thích ứng; khó diễn giải; chi phí tính toán lớn; không đánh giá tác động tới quyết định tồn kho.

## Relevance to our topic

**Trung bình–cao.** Đại diện hướng foundation model/ensemble trên M5; làm baseline hiện đại tham khảo (Chronos).

## Possible improvement

Nhóm chọn hướng mô hình gọn (một LightGBM quantile) và chứng minh bằng KPI tồn kho rằng mô hình gọn đã đủ tốt cho quyết định.
