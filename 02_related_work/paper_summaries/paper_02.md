# Paper 02 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn** (PDF open access trong `papers_pdf/1-s2.0-S0169207021001874-main.pdf`, 19 trang).

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: M5 accuracy competition: Results, findings, and conclusions
Tác giả: Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos
Năm: 2022
Nguồn: International Journal of Forecasting, 38(4), 1346–1364
DOI/Link: https://doi.org/10.1016/j.ijforecast.2021.11.013

## Problem

- Trình bày kết quả nhánh **Accuracy** của M5: dự báo chính xác 42.840 chuỗi doanh số phân cấp của Walmart (abstract).

## Method

- Yêu cầu nộp **30.490 dự báo điểm** ở cấp thấp nhất, cộng dồn lên các cấp trên (abstract).
- **LightGBM được tất cả 50 đội đứng đầu sử dụng** (tr. 1).
- Đội hạng nhất (YJ_STU) dùng trung bình cộng có trọng số bằng nhau của nhiều mô hình LightGBM (gộp dữ liệu theo store, store–category, store–department; cả cách đệ quy và không đệ quy), tổng **220 mô hình**, tối ưu theo **negative log-likelihood của phân phối Tweedie** (tr. 9).

## Dataset

- 3.049 sản phẩm Walmart, 42.840 chuỗi ở 12 cấp tổng hợp (tr. 2).
- **7.092 người, 5.507 đội, 101 quốc gia** (tr. 4).

## Evaluation

- WRMSSE (tr. 3); so sánh với các benchmark thống kê và benchmark khác (tr. 2).

## Results

- Đội thắng tốt hơn benchmark tốt nhất (**ES_bu**) **22,4%**; 5 đội đầu cải thiện hơn 20% (tr. 5–6). WRMSSE của đội thắng: 0,520 (bảng, tr. 7).
- Các phương pháp đơn giản, rẻ như **exponential smoothing vẫn cạnh tranh**, đặc biệt ở cấp product và product–store (tr. 2).

## Limitations

- Các bảng phân tích chỉ tập trung vào **top 50 đội**, vì không thể phân tích hết và **rất ít đội chia sẻ chi tiết phương pháp** (tr. 5).
- [Nhận định nhóm] Đánh giá bằng sai số dự báo, không gắn với chi phí tồn kho.

## Relevance to our topic

[Nhận định nhóm] **Rất cao.** Bằng chứng trực tiếp cho việc chọn LightGBM + Tweedie. Đồng thời, nhận định "exponential smoothing vẫn cạnh tranh ở cấp product–store" (tr. 2) ủng hộ việc giữ ETS làm baseline.

## Possible improvement

[Nhận định nhóm] Kiểm tra xem lợi thế 22,4% về WRMSSE có chuyển thành lợi thế về KPI tồn kho hay không.
