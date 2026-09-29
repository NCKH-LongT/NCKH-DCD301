# Paper 19 Summary

**Nhóm:** Domain (inventory)

> Bài bổ sung (không có trong file Excel ban đầu). Tên bài, tác giả, năm, tạp chí, tập/số/trang và DOI **đã được kiểm tra qua Crossref / trang NeurIPS (2026-09-29)**. Phần tóm tắt nội dung viết từ kiến thức chung, nên đọc bài gốc trước khi trích số liệu.

## Citation

Tên bài: Optimising forecasting models for inventory planning
Tác giả: Nikolaos Kourentzes, Juan R. Trapero, Devon K. Barrow
Năm: 2020
Nguồn: International Journal of Production Economics, 225, 107597
DOI/Link: https://doi.org/10.1016/j.ijpe.2019.107597

## Problem

Mô hình dự báo thường được tối ưu và chọn theo sai số một bước (ví dụ MSE), trong khi mục tiêu thực là hiệu quả tồn kho.

## Method

Đề xuất các hàm mục tiêu/tiêu chí chọn mô hình hướng tới tồn kho (bao gồm độ chính xác của phân phối/khoảng dự báo trong lead time) thay vì chỉ sai số điểm.

## Dataset

Dữ liệu bán lẻ và mô phỏng.

## Evaluation

Sai số dự báo và chỉ số tồn kho (mức phục vụ đạt được, lượng tồn).

## Results

Tối ưu mô hình theo tiêu chí gắn với tồn kho cho kết quả tồn kho tốt hơn so với tối ưu thuần sai số dự báo.

## Limitations

Tập trung vào mô hình thống kê (họ exponential smoothing); chưa xét mô hình ML toàn cục.

## Relevance to our topic

**Rất cao.** Là bằng chứng kinh điển cho luận điểm "forecast accuracy ≠ inventory performance" của đề tài.

## Possible improvement

Mở rộng luận điểm sang mô hình ML global (LightGBM) trên dữ liệu lớn M5, với quyết định hai chiều nhập/thanh lý.
