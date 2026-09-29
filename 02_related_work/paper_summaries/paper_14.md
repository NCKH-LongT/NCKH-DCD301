# Paper 14 Summary

**Nhóm:** AI model / method
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn** (bản PDF chính thức trên trang NeurIPS, 9 trang).

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: LightGBM: A Highly Efficient Gradient Boosting Decision Tree
Tác giả: Guolin Ke, Qi Meng, Thomas Finley, Taifeng Wang, Wei Chen, Weidong Ma, Qiwei Ye, Tie-Yan Liu
Năm: 2017
Nguồn: Advances in Neural Information Processing Systems 30 (NeurIPS 2017)
DOI/Link: https://papers.nips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html

## Problem

- Các cài đặt GBDT (XGBoost, pGBRT) kém hiệu quả khi số đặc trưng lớn và dữ liệu lớn, do phải duyệt mọi mẫu để ước lượng information gain (abstract).

## Method

- **GOSS** (Gradient-based One-Side Sampling): bỏ phần lớn mẫu có gradient nhỏ; **EFB** (Exclusive Feature Bundling): gộp các đặc trưng loại trừ nhau (abstract).

## Dataset

- Các dataset công khai lớn, gồm Allstate Insurance Claim, Flight Delay, KDD CUP 2010, KDD CUP 2012 (tr. 6).

## Evaluation

- Thời gian huấn luyện và độ chính xác (abstract; mục 5).

## Results

- Tăng tốc huấn luyện so với GBDT truyền thống **lên tới hơn 20 lần** với độ chính xác gần như tương đương (abstract; tr. 2).

## Limitations

- [Nhận định nhóm] Thuật toán tổng quát, không dành riêng cho chuỗi thời gian; bài gốc không bàn về dự báo xác suất hay Tweedie/quantile loss.

## Relevance to our topic

[Nhận định nhóm] **Rất cao.** Trích dẫn gốc cho mô hình chính.

## Possible improvement

[Nhận định nhóm] Áp dụng với objective quantile và tweedie (tính năng của thư viện, không phải nội dung bài báo).
