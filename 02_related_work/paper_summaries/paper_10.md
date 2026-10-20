# Paper 10 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn bản arXiv (43 trang, ghi "Published as a conference paper at ICLR 2026").**

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: Controllable Sequence Editing for Biological and Clinical Trajectories (CLEF)
Tác giả: Michelle M. Li, Kevin Li, Yasha Ektefaie, Ying Jin, Yepeng Huang, Shvat Messica, Tianxi Cai, Marinka Zitnik
Năm: 2025 (preprint); ICLR 2026
Nguồn: ICLR 2026 (arXiv:2502.03569)
DOI/Link: https://arxiv.org/abs/2502.03569

## Problem

- Mô hình sinh chuỗi có điều kiện thường không kiểm soát được thời điểm và phạm vi tác động của điều kiện (abstract).

## Method

- CLEF học các "temporal concept" mã hóa cách và thời điểm điều kiện làm thay đổi chuỗi, cho phép chỉnh sửa có mục tiêu (abstract).

## Dataset

- 8 dataset (tái lập trình tế bào, sức khỏe bệnh nhân, bán hàng); so với 9 baseline (abstract).
- M5: dự báo doanh số, **điều kiện là giá sản phẩm**; 1.942 mốc thời gian, 3.049 sản phẩm, 10 cửa hàng; chia theo bang: train California, validate Texas, test Wisconsin (tr. 24).

## Evaluation

- MAE (abstract).

## Results

- Cải thiện MAE **trung bình 16,28%** (chỉnh sửa tức thời) và **trung bình 26,73%** (chỉnh sửa trễ) so với phiên bản không có CLEF; **lên tới 62,84%** trong sinh chuỗi phản thực tế zero-shot (abstract). Các con số này tính trên nhiều dataset, không riêng M5.

## Limitations

- M5 không có ground-truth phản thực tế nên chỉ dùng để sinh có điều kiện chuỗi quan sát được (tr. 24).
- Tác giả tự nêu (tr. 43): concept chỉ ở mức từng biến; có thể cải thiện nếu có mô hình nhân quả thực tế; decoder nhân có thể áp đặt giả định tuyến tính.

## Relevance to our topic

[Nhận định nhóm] **Thấp.** Chỉ gợi ý cách chia dữ liệu theo bang.

## Possible improvement

[Nhận định nhóm] Có thể thêm thí nghiệm train CA, test TX/WI.
