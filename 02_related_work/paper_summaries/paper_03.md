# Paper 03 Summary

## Citation

Tên bài: Hierarchical Parallel Evaluation of a Hamming Code  
Tác giả: Francisco García-Carballeira, Javier Carretero, Fernando Pérez-Costeira  
Năm: 2017  
Nguồn: Algorithms (MDPI)  
DOI/Link: https://www.mdpi.com/1999-4893/10/2/50

## Problem

Bài báo giải quyết vấn đề tốc độ xử lý chậm của thuật toán Hamming truyền thống khi xử lý dữ liệu lớn hoặc yêu cầu thời gian thực.

## Method

Bài báo đề xuất phương pháp xử lý song song (parallel processing) cho thuật toán Hamming nhằm tăng tốc độ mã hóa và giải mã lỗi.

## Dataset

Bài báo sử dụng các tập dữ liệu nhị phân được tạo ngẫu nhiên để kiểm tra hiệu suất của thuật toán song song.

## Evaluation

Bài báo đánh giá:
- Execution time
- Speedup
- Hiệu suất xử lý song song

## Results

Phiên bản parallel Hamming cho tốc độ xử lý nhanh hơn đáng kể so với phiên bản tuần tự truyền thống.

## Limitations

- Chủ yếu đánh giá trên hệ thống tính toán hiệu năng cao
- Chưa triển khai trên vi điều khiển nhúng
- Chưa đánh giá mức tiêu thụ năng lượng

## Relevance to our topic

Bài báo cung cấp hướng tối ưu tốc độ cho hệ thống phát hiện và sửa lỗi bộ nhớ bằng Hamming Code.

## Possible improvement

Nhóm có thể:
- Triển khai parallel decoding trên ESP32 dual-core
- So sánh sequential và parallel execution
- Đánh giá power consumption
- Áp dụng cho hệ thống IoT realtime