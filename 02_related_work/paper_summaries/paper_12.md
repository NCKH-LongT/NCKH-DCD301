# Paper 12 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Metadata và link **đã được kiểm tra (2026-09-29)** qua Crossref / arXiv API; link mở được. Tóm tắt dựa trên abstract, ghi chú `M5_papers_baseline_gap.xlsx` và đối chiếu PDF ở các chi tiết về dataset. Cần đọc toàn văn để bổ sung số liệu kết quả.

## Citation

Tên bài: Intermittent time series forecasting: local vs global models
Tác giả: Stefano Damato, Nicolò Rubattu, Dario Azzimonti, Giorgio Corani
Năm: 2026
Nguồn: arXiv:2601.14031 (nộp Journal of the Operational Research Society)
DOI/Link: https://arxiv.org/abs/2601.14031

## Problem

Dự báo xác suất cho chuỗi nhu cầu rời rạc (nhiều số 0), vốn rất quan trọng cho quản lý tồn kho.

## Method

So sánh mô hình local (iETS, GAS-NB, TweedieGP, Markov Walk) với global (FFNN, DeepAR, DLinear, TiDE, PatchTST, Autoformer, GBT) với các đầu ra phân phối negative binomial, hurdle-shifted NB và Tweedie.

## Dataset

5 dataset, hơn 40.000 chuỗi thực tế (có M5).

## Evaluation

Độ chính xác dự báo xác suất (các phân vị), chi phí tính toán.

## Results

TiDE (global) chính xác nhất, vượt các mô hình local và tính toán rẻ hơn. Mô hình global lớn vừa chậm vừa kém hơn. Phân phối **Tweedie** ước lượng tốt nhất các phân vị cao.

## Limitations

Chưa có kiến trúc global chuẩn cho nhu cầu rời rạc; không đánh giá ở tầng quyết định tồn kho.

## Relevance to our topic

**Rất cao.** Củng cố lựa chọn global model + Tweedie, và cho thấy phân vị cao (dùng làm mức tồn kho an toàn) cần mô hình phù hợp.

## Possible improvement

Nhóm kiểm tra phân vị cao của LightGBM trong vai trò quyết định (fill rate) theo từng nhóm nhu cầu.
