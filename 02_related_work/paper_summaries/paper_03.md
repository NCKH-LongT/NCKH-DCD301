# Paper 03 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn** (PDF open access trong `papers_pdf/1-s2.0-S0169207021001722-main.pdf`, 21 trang).

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
- Phần lớn phương pháp thắng dùng **LightGBM**; các đội còn lại chủ yếu dùng LSTM (tr. 14).
- Đội hạng nhất (Everyday Low SPLices; Lainder & Wolfinger) **huấn luyện mô hình gradient boosting riêng cho từng phân vị và từng cấp tổng hợp**, tổng **126 mô hình**, siêu tham số tìm trong không gian cấu hình LightGBM; đặc trưng gồm ngày trong tuần/tháng, SNAP, ngày lễ, rolling mean/median/quantile, tỷ lệ số 0; **không dùng giá**; có hiệu chỉnh nhất quán giữa các cấp (reconciliation) (tr. 14).

## Dataset

- M5, 42.840 chuỗi (abstract).
- **1.137 người, 892 đội, 94 quốc gia** (tr. 5).

## Evaluation

- WSPL (xem bài 01, tr. 3).

## Results

- Các kết luận chính của nhánh Accuracy cũng đúng cho nhánh Uncertainty; nhấn mạnh hiệu năng của ML, đặc biệt **LightGBM được đại đa số top 50 sử dụng** (tr. 19).

## Limitations

- [Nhận định nhóm] Không đánh giá việc dùng phân vị cho quyết định tồn kho.

## Relevance to our topic

[Nhận định nhóm] **Rất cao.** Bằng chứng trực tiếp rằng **LightGBM huấn luyện theo từng phân vị** — đúng cách tiếp cận của nhóm — là lời giải hạng nhất của M5 Uncertainty. Điều này cân bằng với kết quả bất lợi của bài 12 (vốn dùng LightGBM dạng distributional, cách khác).

## Possible improvement

[Nhận định nhóm] Dùng phân vị dự báo làm mức order-up-to và ngưỡng thanh lý, đo bằng KPI tồn kho.
