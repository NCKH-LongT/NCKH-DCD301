# Paper 04 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Tóm tắt dựa trên abstract và ghi chú trong `M5_papers_baseline_gap.xlsx`. Cần đọc toàn văn để bổ sung số liệu chi tiết.

## Citation

Tên bài: Algorithmic Transparency in Forecasting Support Systems
Tác giả: Leif Feddersen
Năm: 2024
Nguồn: arXiv:2411.00699
DOI/Link: https://arxiv.org/abs/2411.00699

## Problem

Người dùng trong doanh nghiệp thường chỉnh tay dự báo. Thiết kế giao diện hệ thống hỗ trợ dự báo (FSS) thế nào để khuyến khích chỉnh sửa có lợi và hạn chế chỉnh sửa có hại?

## Method

Thí nghiệm người dùng với 3 thiết kế FSS có mức độ minh bạch khác nhau, dựa trên phân rã chuỗi thời gian (mô hình kiểu Prophet).

## Dataset

Theo ghi chú của nhóm: subset nhỏ của M5 (nhóm FOODS).

## Evaluation

Phương sai và tần suất các chỉnh sửa có hại, mức độ hài lòng tự báo cáo.

## Results

Minh bạch giảm được các chỉnh sửa có hại. Tuy nhiên, cho phép người dùng chỉnh trực tiếp các thành phần của thuật toán lại dẫn tới chỉnh sửa tệ nhất, và người dùng hài lòng nhất với hệ thống *không* minh bạch.

## Limitations

Chỉ một subset nhỏ và một mô hình. Minh bạch có thể làm người dùng quá tải nếu không được đào tạo.

## Relevance to our topic

**Trung bình.** Liên quan tới thiết kế dashboard khuyến nghị (người quản lý kho sẽ xem và có thể chỉnh khuyến nghị).

## Possible improvement

Dashboard của nhóm hiển thị lý do khuyến nghị ở mức vừa đủ (khoảng dự báo, số ngày tồn kho còn lại), không cho chỉnh trực tiếp tham số mô hình.
