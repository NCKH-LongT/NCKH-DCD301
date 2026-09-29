# Paper 13 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn bản arXiv (32 trang).**

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: End-to-end probabilistic hierarchical forecasting of large hierarchies via probabilistic top-down
Tác giả: Lorenzo Zambon, Dario Azzimonti, Giorgio Corani
Năm: 2026
Nguồn: arXiv:2606.26774 (chưa qua phản biện)
DOI/Link: https://arxiv.org/abs/2606.26774

## Problem

- Dự báo xác suất nhất quán giữa các cấp phân cấp với chi phí tính toán chấp nhận được ở quy mô bán lẻ (abstract).

## Method

- e2eTD: chỉ dự báo trực tiếp một tập nhỏ chuỗi tổng hợp (~0,3% phân cấp, mượt hơn), rồi dùng thuật toán lấy mẫu top-down xác suất với tỷ lệ phân bổ lịch sử được mô hình hóa như phân phối đồng thời (abstract).
- Mô hình dự báo cho các chuỗi tổng hợp được chọn: **ETS** tự chọn mô hình (tr. 9).

## Dataset

- M5 và Favorita (abstract; tr. 1).

## Evaluation

- Weighted scaled pinball loss (WSPL) trên các cấp; chi phí tính toán (abstract; tr. 25).

## Results

- WSPL trung bình thấp nhất trên M5 và Favorita; nếu tham gia M5 Uncertainty sẽ xếp **11/892**; riêng cấp thấp nhất (L12) xếp thứ 7 trong top 50 (tr. 25).
- Chạy dưới 5 phút (M5) và dưới 20 phút (Favorita) trên laptop thường (tr. 25).

## Limitations

- Tác giả nêu hướng cần phát triển (tr. 25): chọn chuỗi tổng hợp để dự báo hiện làm **thủ công**; mô hình hóa tỷ lệ phân bổ đang dùng heuristic đơn giản.

## Relevance to our topic

[Nhận định nhóm] **Cao.** Baseline dự báo xác suất nhẹ, chạy được trên laptop.

## Possible improvement

[Nhận định nhóm] Nhóm tập trung vào cấp SKU–store — cấp mà bài này nhấn mạnh là cấp dẫn dắt quyết định tồn kho (tr. 25).
