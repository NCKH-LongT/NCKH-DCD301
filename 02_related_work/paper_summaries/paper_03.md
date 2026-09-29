# Paper 03 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Tóm tắt dựa trên abstract và ghi chú trong `M5_papers_baseline_gap.xlsx`. Cần đọc toàn văn để bổ sung số liệu chi tiết.

## Citation

Tên bài: The M5 uncertainty competition: Results, findings and conclusions
Tác giả: Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos, Zhi Chen, Anil Gaba, Ilia Tsetlin, Robert L. Winkler
Năm: 2022 (online 2021)
Nguồn: International Journal of Forecasting, 38(4)
DOI/Link: https://www.sciencedirect.com/science/article/pii/S0169207021001722

## Problem

Tổng kết phần thi dự báo xác suất: ước lượng 9 phân vị của phân phối nhu cầu.

## Method

Phân tích phương pháp của các đội đứng đầu: kết hợp mô hình ML (LightGBM, quantile regression) và thống kê để sinh các phân vị.

## Dataset

M5 (Walmart); 892 đội tham gia.

## Evaluation

WSPL, phân vị τ ∈ {0.005, 0.025, 0.165, 0.25, 0.5, 0.75, 0.835, 0.975, 0.995}.

## Results

Dự báo xác suất ở cấp SKU–store (cấp thấp, nhiều số 0) khó hơn nhiều so với cấp tổng hợp; các mô hình dựa trên ML và phân phối phù hợp với dữ liệu đếm cho kết quả tốt nhất.

## Limitations

Giới hạn ở top 50 đội; ít đội chia sẻ chi tiết. Không đánh giá phân vị dự báo được dùng thế nào cho quyết định tồn kho.

## Relevance to our topic

**Rất cao.** Dự báo phân vị chính là đầu vào của lớp quyết định newsvendor trong đề tài.

## Possible improvement

Dùng trực tiếp phân vị dự báo làm mức order-up-to và ngưỡng thanh lý, rồi đo hiệu quả bằng KPI tồn kho.
