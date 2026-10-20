# Paper 05 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn bản arXiv (ICML 2024 camera-ready, 20 trang).**

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: An Empirical Examination of Balancing Strategy for Counterfactual Estimation on Time Series
Tác giả: Qiang Huang, Chuizheng Meng, Defu Cao, Biwei Huang, Yi Chang, Yan Liu
Năm: 2024
Nguồn: ICML 2024 (arXiv:2408.08815)
DOI/Link: https://arxiv.org/abs/2408.08815

## Problem

- Trong ước lượng phản thực tế (counterfactual) trên chuỗi thời gian, hiệu quả của các chiến lược cân bằng (balancing) để giảm sai lệch do can thiệp vẫn là câu hỏi mở (abstract).

## Method

- Khảo sát thực nghiệm các chiến lược cân bằng **CDC, AGR, PCB** trên các mô hình **CT, CRN, RMSN, GNET, MSM**, so với biến thể ERM không có module cân bằng (Hình 3, tr. 4).

## Dataset

- 3 dataset: Tumor (mô phỏng), MIMIC-III (bán tổng hợp), **M5** (tr. 4).
- M5: 3.049 sản phẩm thuộc Hobbies, Foods, Household; không có nhãn phản thực tế nên chỉ đánh giá kết quả thực tế (factual), để ở phụ lục (tr. 4).
- M5 được tái cấu trúc với **giá sản phẩm là biến can thiệp (treatment)** (tr. 15, Phụ lục D.2).

## Evaluation

- Trên M5: RMNSE (mean ± std) với horizon τ = 1…6 (Bảng 8, tr. 16).

## Results

- Trên M5, các biến thể ERM **không có** module cân bằng nhìn chung tốt hơn biến thể có cân bằng; GNET và MSM bị loại vì không hội tụ trên dataset này (tr. 15, Phụ lục D.2).
- Trên MIMIC-III, module biểu diễn cân bằng không cải thiện kết quả (tr. 5).
- Kêu gọi xem xét lại chiến lược cân bằng trong bối cảnh chuỗi thời gian (abstract).

## Limitations

- M5 không có ground-truth phản thực tế nên chỉ đánh giá được kết quả thực tế (tr. 4).

## Relevance to our topic

[Nhận định nhóm] **Thấp.** Chỉ liên quan gián tiếp (giá → doanh số).

## Possible improvement

[Nhận định nhóm] Ngoài phạm vi; có thể nhắc trong Future Work (tác động của giảm giá tới thanh lý).
