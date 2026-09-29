# Paper 11 Summary

**Nhóm:** Direct (M5 / bán lẻ) — **bài gần nhất với đề tài**
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn bản arXiv (32 trang).**

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: Multi-objective probabilistic forecast combination for inventory demand
Tác giả: Shengjie Wang, Yanfei Kang, Evangelos Spiliotis, Fotios Petropoulos
Năm: 2026
Nguồn: arXiv:2606.04900 (chưa qua phản biện)
DOI/Link: https://arxiv.org/abs/2606.04900

## Problem

- Kết hợp dự báo xác suất thường chỉ tối ưu sai số thống kê; trong tồn kho, độ chính xác cao hơn không nhất thiết cho quyết định tốt hơn, nhất là khi chi phí phi tuyến và có nhiều mục tiêu mâu thuẫn (abstract).

## Method

- Đặt bài toán kết hợp dự báo thành **tối ưu đa mục tiêu** (MOO), sinh tập Pareto (abstract); dùng NSGA-III (tr. 14, 26).
- 4 mô hình thành phần: **WSS, ZV** (bootstrap/lấy mẫu lại) và **Poisson, Negative Binomial** (mô hình phân phối, trung bình động damped) (tr. 9–10).
- Chính sách tồn kho: mức order-up-to = **phân vị τ** của phân phối dự báo; τ = tỷ lệ tới hạn newsvendor (tr. 11).

## Dataset

- M5: 30.490 chuỗi, 3.049 sản phẩm × 10 cửa hàng, 1.941 ngày; ~60,1% quan sát bằng 0 (tr. 16, mục 5.1).
- Chia dữ liệu: base đến ngày 1857, reference ngày 1858–1913, evaluation 28 ngày cuối (1914–1941) (tr. 16).
- Loại **1.587 chuỗi** toàn 0 ở giai đoạn reference nhưng có bán ở giai đoạn evaluation, còn **28.903** chuỗi (tr. 17).
- Dataset thứ hai: phụ tùng Royal Air Force (abstract).

## Evaluation

- DRPS (độ chính xác dự báo); Cost = c1·Holding + c2·Stockout, Holding, Stockout (tr. 11; Bảng 1–3, tr. 18–19).
- Chi phí: c1 = 1, c2 ∈ {4, 9, 19} ↔ mức phục vụ τ ∈ {80%, 90%, 95%} (tr. 16).

## Results

- Ví dụ M5, (c1, c2) = (1, 4): trung bình đơn giản (SA) Cost = 65,6164; NSGA-III-c 65,3958; Cost-opt 65,1533; mô hình đơn lẻ tốt nhất (POIS) 64,5532 (Bảng 1, tr. 18).
- Không có phương pháp đơn lẻ nào vượt trội ở mọi kịch bản (tr. 18).
- Kết luận: kết hợp MOO cho cân bằng tốt hơn giữa độ chính xác và chất lượng quyết định; có trường hợp cải thiện cả hai (tr. 26).

## Limitations

- Tác giả tự nêu (tr. 26): (1) NSGA-III tốn chi phí tính toán; (2) dùng cửa sổ validation cố định để ước lượng trọng số; (3) **chỉ xét newsvendor một kỳ, một sản phẩm**, hạn chế áp dụng cho hệ nhiều kỳ/nhiều cấp.
- [Nhận định nhóm] Không có quyết định thanh lý; không phân tích theo loại nhu cầu; không dùng mô hình ML.

## Relevance to our topic

[Nhận định nhóm] **Rất cao — bài gần nhất.** Phải phân biệt rõ trong Related Work.

## Possible improvement

[Nhận định nhóm] Khác biệt: (1) mô phỏng tồn kho **nhiều kỳ** có lead time — đúng hạn chế (3) tác giả tự nêu; (2) quyết định hai chiều nhập + thanh lý; (3) phân tích theo nhóm ADI–CV²; (4) mô hình dự báo ML thay vì kết hợp 4 mô hình thống kê.
