# Paper 17 Summary

**Nhóm:** AI model / method
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn bản preprint arXiv 1704.04110** (12 trang). Bản in IJF 2020 có thể khác chi tiết — khi trích số liệu nên kiểm tra bản IJF.

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: DeepAR: Probabilistic forecasting with autoregressive recurrent networks
Tác giả: David Salinas, Valentin Flunkert, Jan Gasthaus, Tim Januschowski
Năm: 2020
Nguồn: International Journal of Forecasting, 36(3), 1181–1191
DOI/Link: https://doi.org/10.1016/j.ijforecast.2019.07.001 · arXiv: https://arxiv.org/abs/1704.04110

## Problem

- Dự báo xác suất (ước lượng phân phối tương lai) là yếu tố then chốt cho tối ưu vận hành, ví dụ tồn kho bán lẻ (abstract).

## Method

- DeepAR: mạng RNN tự hồi quy huấn luyện trên **nhiều chuỗi liên quan** (abstract); có thể dùng likelihood negative binomial cho dữ liệu đếm (tr. 3).

## Dataset

- 5 dataset: parts (1.046 chuỗi bán phụ tùng ô tô theo tháng), electricity (370 khách hàng), traffic (963 làn xe), ec và ec-sub (bán hàng theo tuần của Amazon) (tr. 6).

## Evaluation

- ρ-risk (quantile loss) ở 0,5 và 0,9 (tr. 8), cùng các metric khác trong bài.

## Results

- Cải thiện độ chính xác **khoảng 15%** so với các phương pháp tốt nhất lúc đó (abstract).

## Limitations

- [Nhận định nhóm] Cần huấn luyện mạng sâu, khó diễn giải — không phải hạn chế do tác giả nêu.

## Relevance to our topic

[Nhận định nhóm] **Trung bình–cao.** Baseline deep learning xác suất; bài 12 cho thấy DeepAR cạnh tranh hơn LightGBM ở dạng xác suất.

## Possible improvement

[Nhận định nhóm] Thêm DeepAR (GluonTS) làm baseline.
