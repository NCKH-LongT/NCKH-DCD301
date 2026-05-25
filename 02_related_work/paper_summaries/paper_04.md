# Paper 04 Summary

## Citation

Tên bài: Análisis del impacto de la inclusión de Códigos Correctores de Errores en un Sistema Empotrado basado en Arduino  
Tác giả: Carlos Andrés Hernández Suárez và cộng sự  
Năm: 2022  
Nguồn: ResearchGate Conference Paper  
DOI/Link: https://www.researchgate.net/publication/363791708_Analisis_del_impacto_de_la_inclusion_de_Codigos_Correctores_de_Errores_en_un_Sistema_Empotrado_basado_en_Arduino

## Problem

Bài báo nghiên cứu ảnh hưởng của việc tích hợp Error Correction Codes vào hệ thống nhúng Arduino đối với hiệu suất và độ tin cậy dữ liệu.

## Method

Bài báo triển khai cơ chế ECC trên nền tảng Arduino để phát hiện và sửa lỗi dữ liệu trong hệ thống nhúng.

## Dataset

Sử dụng dữ liệu nhị phân và các mẫu lỗi được giả lập trong quá trình truyền và lưu trữ dữ liệu.

## Evaluation

Bài báo đánh giá:
- Tỷ lệ lỗi dữ liệu
- Độ chính xác sửa lỗi
- Hiệu năng hệ thống sau khi tích hợp ECC

## Results

ECC giúp tăng độ tin cậy dữ liệu và giảm lỗi trong hệ thống nhúng Arduino.

## Limitations

- Hiệu suất hệ thống bị giảm khi thêm ECC
- Chưa tối ưu cho hệ thống realtime
- Chưa phân tích sâu mức tiêu thụ năng lượng

## Relevance to our topic

Bài báo liên quan trực tiếp đến đề tài Memory & Error Detection vì đánh giá tác động của cơ chế sửa lỗi trên hệ thống nhúng Arduino.

## Possible improvement

Nhóm có thể:
- Tối ưu thuật toán ECC cho realtime
- Triển khai trên ESP32 dual-core
- Đo power consumption
- Thêm web dashboard giám sát lỗi