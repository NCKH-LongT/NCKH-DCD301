# Paper 01 Summary

## Citation

Tên bài: Implementasi Deteksi Dan Koreksi Error Pada Komunikasi Serial Arduino Berbasis UART Dengan Metode Hamming Code  
Tác giả: Muhammad Rizki Maulana, Eko Setijadi, Gamantyo Hendrantoro  
Năm: 2018  
Nguồn: Jurnal Pengembangan Teknologi Informasi dan Ilmu Komputer (J-PTIIK)  
DOI/Link: https://j-ptiik.ub.ac.id/index.php/j-ptiik/article/view/3186

## Problem

Bài báo giải quyết vấn đề lỗi truyền dữ liệu trong giao tiếp nối tiếp UART giữa các thiết bị Arduino. Nhiễu trong quá trình truyền có thể làm đảo bit dữ liệu, gây sai lệch thông tin.

## Method

Bài báo sử dụng mã Hamming để phát hiện và sửa lỗi bit đơn trong quá trình truyền UART giữa các vi điều khiển Arduino.

## Dataset

Dữ liệu thử nghiệm là các chuỗi bit nhị phân được truyền giữa các Arduino thông qua giao tiếp UART và được chèn lỗi giả lập trong quá trình truyền.

## Evaluation

Bài báo đánh giá:
- Khả năng phát hiện lỗi
- Khả năng sửa lỗi
- Độ chính xác truyền dữ liệu

## Results

Hệ thống có thể phát hiện và sửa thành công lỗi bit đơn trong truyền dữ liệu UART bằng mã Hamming.

## Limitations

- Chỉ sửa được lỗi 1 bit
- Chưa hỗ trợ lỗi nhiều bit
- Chưa đánh giá hiệu năng thời gian thực

## Relevance to our topic

Bài báo liên quan trực tiếp đến đề tài Memory & Error Detection vì sử dụng Hamming Code để phát hiện và sửa lỗi dữ liệu trên hệ thống nhúng.

## Possible improvement

Nhóm có thể:
- Triển khai trên ESP32
- Thêm realtime monitoring
- Đo latency và memory usage
- So sánh hiệu suất sequential và parallel decoding