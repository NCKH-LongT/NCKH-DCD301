# Paper 17 Summary

**Nhóm:** AI model / method

> Bài bổ sung (không có trong file Excel ban đầu). Thông tin được tóm tắt từ kiến thức chung, **cần mở bài gốc để kiểm tra lại** trước khi trích dẫn.

## Citation

Tên bài: DeepAR: Probabilistic forecasting with autoregressive recurrent networks
Tác giả: David Salinas, Valentin Flunkert, Jan Gasthaus, Tim Januschowski
Năm: 2020
Nguồn: International Journal of Forecasting, 36(3), 1181–1191
DOI/Link: https://doi.org/10.1016/j.ijforecast.2019.07.001

## Problem

Dự báo xác suất cho hàng nghìn chuỗi liên quan trong bán lẻ.

## Method

Mạng RNN tự hồi quy toàn cục, xuất ra tham số phân phối (ví dụ negative binomial cho dữ liệu đếm).

## Dataset

Dữ liệu bán lẻ Amazon, điện năng, giao thông...

## Evaluation

Quantile loss (ρ-risk), ND, RMSE.

## Results

Cải thiện khoảng 15% so với các phương pháp tốt nhất lúc đó; mô hình global học được từ nhiều chuỗi liên quan.

## Limitations

Cần GPU và điều chỉnh siêu tham số; khó diễn giải.

## Relevance to our topic

**Trung bình–cao.** Baseline deep learning xác suất tùy chọn.

## Possible improvement

Có thể thêm DeepAR (GluonTS) làm baseline nếu có GPU.
