# Paper 02 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Tóm tắt dựa trên abstract và ghi chú trong `M5_papers_baseline_gap.xlsx`. Cần đọc toàn văn để bổ sung số liệu chi tiết.

## Citation

Tên bài: M5 accuracy competition: Results, findings, and conclusions
Tác giả: Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos
Năm: 2022
Nguồn: International Journal of Forecasting, 38(4)
DOI/Link: https://www.sciencedirect.com/science/article/pii/S0169207021001874

## Problem

Tổng kết kết quả phần thi dự báo điểm M5 Accuracy: phương pháp nào thắng và vì sao.

## Method

Phân tích phương pháp của các đội đứng đầu so với 24 benchmark. Các đội thắng chủ yếu dùng **LightGBM global model** (huấn luyện chung trên nhiều chuỗi), kết hợp ensemble, đặc trưng lag/rolling/giá/lịch và hàm mất mát Tweedie/Poisson.

## Dataset

M5 (Walmart).

## Evaluation

WRMSSE trên 12 cấp phân cấp, horizon 28 ngày.

## Results

Các phương pháp ML (đặc biệt LightGBM) vượt trội rõ rệt so với các benchmark thống kê. Mô hình global học từ nhiều chuỗi và việc tận dụng biến ngoại sinh (giá, sự kiện) là yếu tố then chốt.

## Limitations

Chỉ phân tích top 50 đội; nhiều đội không công bố đầy đủ chi tiết nên khó tái lập. Đánh giá **chỉ bằng sai số dự báo**, không gắn với chi phí tồn kho.

## Relevance to our topic

**Rất cao.** Là căn cứ để chọn LightGBM làm mô hình chính và chọn các đặc trưng.

## Possible improvement

Kiểm tra xem lợi thế về WRMSSE của LightGBM có chuyển thành lợi thế về fill rate / chi phí tồn kho hay không.
