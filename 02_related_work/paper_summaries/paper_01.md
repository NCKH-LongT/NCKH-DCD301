# Paper 01 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Metadata và link **đã được kiểm tra (2026-09-29)** qua Crossref / arXiv API; link mở được. Tóm tắt dựa trên abstract, ghi chú `M5_papers_baseline_gap.xlsx` và đối chiếu PDF ở các chi tiết về dataset. Cần đọc toàn văn để bổ sung số liệu kết quả.

## Citation

Tên bài: The M5 competition: Background, organization, and implementation
Tác giả: Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos
Năm: 2022
Nguồn: International Journal of Forecasting, 38(4), 1325–1336
DOI/Link: https://doi.org/10.1016/j.ijforecast.2021.07.007 (ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0169207021001187)

## Problem

Mô tả bối cảnh, mục tiêu và cách tổ chức cuộc thi M5: dự báo doanh số bán lẻ phân cấp (hierarchical) của Walmart, gồm cả dự báo điểm (Accuracy) và dự báo xác suất (Uncertainty).

## Method

Không đề xuất mô hình mới. Định nghĩa bộ dữ liệu, cấu trúc phân cấp 12 cấp độ, thước đo đánh giá và 24 benchmark chuẩn (Naive, sNaive, SES, MA, Croston, SBA, TSB, ES, ARIMA, MLP/RF...).

## Dataset

M5 (Walmart): 3.049 sản phẩm × 10 cửa hàng = 30.490 chuỗi SKU–store ở cấp thấp nhất, tổng 42.840 chuỗi qua 12 cấp; 1.941 ngày (2011–2016); kèm `calendar` (sự kiện, SNAP) và `sell_prices`.

## Evaluation

WRMSSE (Weighted Root Mean Squared Scaled Error) cho Accuracy; WSPL (Weighted Scaled Pinball Loss) trên 9 phân vị cho Uncertainty. Horizon 28 ngày.

## Results

Cung cấp một benchmark công khai, lớn, có nhiều chuỗi nhu cầu rời rạc (intermittent), trở thành chuẩn so sánh cho dự báo bán lẻ.

## Limitations

Chỉ mô tả thiết kế cuộc thi. Dữ liệu **không có thông tin tồn kho, lead time, chi phí**, và doanh số bằng 0 có thể là do hết hàng chứ không phải do không có nhu cầu (censored demand).

## Relevance to our topic

**Cao.** Đây là nguồn chính thức mô tả dataset và metric mà nhóm sẽ dùng (phần Dataset, Evaluation Metrics).

## Possible improvement

Bổ sung lớp mô phỏng tồn kho có tham số (lead time, chi phí) để biến M5 thành bài toán ra quyết định, không chỉ bài toán dự báo.
