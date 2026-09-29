# Paper 14 Summary

**Nhóm:** AI model / method

> Bài bổ sung (không có trong file Excel ban đầu). Tên bài, tác giả, năm, tạp chí, tập/số/trang và DOI **đã được kiểm tra qua Crossref / trang NeurIPS (2026-09-29)**. Phần tóm tắt nội dung viết từ kiến thức chung, nên đọc bài gốc trước khi trích số liệu.

## Citation

Tên bài: LightGBM: A Highly Efficient Gradient Boosting Decision Tree
Tác giả: Guolin Ke, Qi Meng, Thomas Finley, Taifeng Wang, Wei Chen, Weidong Ma, Qiwei Ye, Tie-Yan Liu
Năm: 2017
Nguồn: Advances in Neural Information Processing Systems 30 (NeurIPS 2017)
DOI/Link: https://papers.nips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html

## Problem

Gradient boosting decision tree chậm khi dữ liệu có nhiều mẫu và nhiều đặc trưng.

## Method

GOSS (Gradient-based One-Side Sampling) và EFB (Exclusive Feature Bundling), tăng trưởng cây theo lá (leaf-wise).

## Dataset

Nhiều dataset công khai lớn.

## Evaluation

Thời gian huấn luyện, AUC/NDCG/sai số tùy bài toán.

## Results

Huấn luyện nhanh hơn GBDT truyền thống tới hơn 20 lần với độ chính xác gần như tương đương.

## Limitations

Là thuật toán tổng quát, không dành riêng cho chuỗi thời gian; cần tự thiết kế đặc trưng lag/rolling.

## Relevance to our topic

**Rất cao.** Là mô hình AI chính của đề tài; hỗ trợ sẵn loss Tweedie và quantile.

## Possible improvement

Áp dụng với objective `quantile` (nhiều mức τ) và `tweedie` cho dữ liệu M5.
