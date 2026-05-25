# Paper 02 Summary

## Citation

Tên bài: Application of Hamming Code for Error Control in Memory  
Tác giả: Đỗ H. N. Tran và cộng sự  
Năm: 2022  
Nguồn: Journal of Technical Education Science  
DOI/Link: https://jte.edu.vn/index.php/jte/article/view/1141

## Problem

Bài báo giải quyết vấn đề lỗi bit trong bộ nhớ của hệ thống nhúng và IoT, có thể gây mất dữ liệu hoặc lỗi hệ thống.

## Method

Bài báo thiết kế hệ thống ECC sử dụng mã Hamming để mã hóa dữ liệu trước khi lưu vào bộ nhớ nhằm phát hiện và sửa lỗi bit đơn.

## Dataset

Bài báo sử dụng các mẫu dữ liệu nhị phân và giả lập lỗi bit trong bộ nhớ để kiểm tra khả năng sửa lỗi.

## Evaluation

Bài báo đánh giá:
- Khả năng phát hiện lỗi
- Khả năng sửa lỗi
- Độ chính xác của encoder và decoder

## Results

Hệ thống ECC hoạt động hiệu quả trong việc phát hiện và sửa lỗi bit đơn, giúp tăng độ tin cậy của bộ nhớ.

## Limitations

- Chỉ sửa được single-bit error
- Chưa đánh giá realtime performance
- Chưa triển khai trên phần cứng ESP32 hoặc Arduino

## Relevance to our topic

Đây là bài báo phù hợp trực tiếp với đề tài Memory & Error Detection vì tập trung vào ECC cho bộ nhớ bằng mã Hamming.

## Possible improvement

Nhóm có thể:
- Xây dựng hệ thống realtime monitoring
- Đo execution time và memory overhead
- Triển khai trên ESP32 hoặc Arduino
- Thêm visualization dashboard