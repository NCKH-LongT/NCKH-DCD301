# Paper 06 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn bản arXiv v1 (9 trang).**

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: Foundation Models for Demand Forecasting via Dual-Strategy Ensembling
Tác giả: Wei Yang, Defu Cao, Yan Liu
Năm: 2025
Nguồn: 1st Workshop on 'AI for Supply Chain: Today and Future' @ KDD 2025, Toronto (arXiv:2507.22053)
DOI/Link: https://arxiv.org/abs/2507.22053

## Problem

- Dự báo nhu cầu chuỗi cung ứng gặp khó do cấu trúc phân cấp, dịch chuyển miền và yếu tố ngoại sinh; foundation model còn cứng nhắc về kiến trúc và kém ổn định khi phân phối thay đổi (abstract).

## Method

- **Hierarchical Ensemble (HE)**: chia huấn luyện/suy luận theo cấp ngữ nghĩa (store, category, department); **Architectural Ensemble (AE)**: kết hợp nhiều backbone (abstract; tr. 3).
- Kết hợp bằng trung bình có trọng số; tác giả dùng **trọng số chuẩn hóa bằng nhau** cho đơn giản (tr. 3, mục 3.2).
- Backbone/baseline: LightGBM, DNN, DeepAR, PatchTST, TEMPO, Chronos (tr. 4, mục 4.1.3).

## Dataset

- M5 là dataset chính (30.490 sản phẩm Walmart) + 3 dataset ngoài: Walmart Promo (theo tuần), Store-Item Benchmark (5 năm theo ngày), Balkan Retail (7 năm theo tháng) (tr. 4, mục 4.1.1).

## Evaluation

- M5: **WRMSSE** trên 12 cấp phân cấp (tr. 4, mục 4.1.2).

## Results

- HE cải thiện mọi backbone trên M5, ví dụ DeepAR WRMSSE 0,5556 → 0,5233; PatchTST 0,6997 → 0,6210 (tr. 4, mục 4.2.1).

## Limitations

- Khả năng diễn giải/giải thích của kết quả ensemble vẫn là thách thức mở, nhất là trong môi trường ra quyết định (tr. 7, mục 4.6).
- [Nhận định nhóm] Trọng số kết hợp cố định (bằng nhau, tr. 3); không đánh giá tác động tới quyết định tồn kho.

## Relevance to our topic

[Nhận định nhóm] **Trung bình–cao.** Đại diện hướng foundation model/ensemble trên M5.

## Possible improvement

[Nhận định nhóm] Chứng minh bằng KPI tồn kho rằng mô hình gọn có đủ tốt cho quyết định hay không.
