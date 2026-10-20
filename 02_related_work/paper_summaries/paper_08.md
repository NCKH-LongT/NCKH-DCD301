# Paper 08 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn bản arXiv (44 trang).**

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: The cost of ensembling: is it always worth combining?
Tác giả: Marco Zanotti
Năm: 2025
Nguồn: arXiv:2506.04677 (chưa qua phản biện)
DOI/Link: https://arxiv.org/abs/2506.04677

## Problem

- Đánh đổi giữa độ chính xác và chi phí tính toán của ensemble trong dự báo chuỗi thời gian (abstract).

## Method

- **10 mô hình global** làm base learner (từ ML truyền thống tới deep learning) + **8 cấu hình ensemble**; dự báo điểm và xác suất; nhiều tần suất huấn luyện lại (abstract; tr. 4, 8).
- Hai triết lý ensemble: ENSACC (theo độ chính xác) và ENSTIME (theo hiệu quả tính toán) (tr. 25).

## Dataset

- **M5** và **VN1** (tr. 4). VN1 do Flieber, Syrup Tech và SupChains tổ chức từ 10/2024, gồm dữ liệu bán hàng theo tuần của 15.053 sản phẩm (tr. 7).

## Evaluation

- RMSSE cho dự báo điểm; scaled quantile loss (SQL) và scaled multi-quantile loss (SMQL) cho dự báo xác suất; chi phí tính toán (tr. 13–14, mục 3.4).

## Results

- Ensemble cải thiện hiệu năng một cách nhất quán, nhất là dự báo xác suất, nhưng tốn chi phí đáng kể; giảm tần suất huấn luyện lại giảm mạnh chi phí mà ít mất độ chính xác; ensemble nhỏ 2–3 mô hình thường đã gần tối ưu (abstract).
- Trên M5, lợi thế của ENSACC so với base model tốt nhất là rất nhỏ, trong khi chi phí cao hơn nhiều (tr. 21).

## Limitations

- Tác giả tự nêu (tr. 26): chỉ 2 dataset bán lẻ; giả định quá trình sinh dữ liệu ổn định (không concept drift); ensemble chỉ dùng trung bình đơn giản; giả định chi phí tính toán tĩnh.

## Relevance to our topic

[Nhận định nhóm] **Trung bình–cao.** Hỗ trợ lập luận chọn mô hình gọn và huấn luyện lại ít thường xuyên.

## Possible improvement

[Nhận định nhóm] Báo cáo thời gian huấn luyện/suy luận như một metric hệ thống.
