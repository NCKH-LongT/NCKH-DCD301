# Paper 03 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ⚠️ **Chỉ đọc được abstract** (qua OpenAlex). Toàn văn open access trên ScienceDirect nhưng bị CAPTCHA khi truy cập tự động → nhóm cần tự mở bằng trình duyệt.

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: The M5 uncertainty competition: Results, findings and conclusions
Tác giả: Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos, Zhi Chen, Anil Gaba, Ilia Tsetlin, Robert L. Winkler
Năm: 2022
Nguồn: International Journal of Forecasting, 38(4), 1365–1385
DOI/Link: https://doi.org/10.1016/j.ijforecast.2021.10.009

## Problem

- Nhánh **Uncertainty** của M5: dự báo chính xác phân phối bất định của 42.840 chuỗi doanh số phân cấp của Walmart (abstract).

## Method

- Yêu cầu dự báo **9 phân vị**: 0,005; 0,025; 0,165; 0,250; 0,500; 0,750; 0,835; 0,975; 0,995 (abstract).
- Bài trình bày triển khai, kết quả, các phương pháp tốt nhất, phát hiện chính (abstract).
- [Chưa kiểm chứng] Phương pháp cụ thể của các đội thắng.

## Dataset

- M5 (Walmart), 42.840 chuỗi (abstract).
- [Nguồn thứ cấp: bài 13, tr. 1 và tr. 25] Có **892 đội** tham gia nhánh Uncertainty.

## Evaluation

- [Nguồn thứ cấp: bài 08, tr. 14; bài 13] Weighted scaled pinball loss (WSPL).

## Results

- [Chưa kiểm chứng] Kết quả chi tiết — cần đọc toàn văn.

## Limitations

- [Chưa kiểm chứng] Ghi chú trong Excel ban đầu ("giới hạn ở top 50 đội") — cần đọc toàn văn.
- [Nhận định nhóm] Không đánh giá việc dùng phân vị cho quyết định tồn kho.

## Relevance to our topic

[Nhận định nhóm] **Rất cao.** Dự báo phân vị là đầu vào của lớp quyết định newsvendor.

## Possible improvement

[Nhận định nhóm] Dùng phân vị dự báo làm mức order-up-to và ngưỡng thanh lý, đo bằng KPI tồn kho.
