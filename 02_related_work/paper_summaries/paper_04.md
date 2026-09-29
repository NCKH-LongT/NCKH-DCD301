# Paper 04 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Metadata và link **đã được kiểm tra (2026-09-29)** qua Crossref / arXiv API; link mở được. Tóm tắt dựa trên abstract, ghi chú `M5_papers_baseline_gap.xlsx` và đối chiếu PDF ở các chi tiết về dataset. Cần đọc toàn văn để bổ sung số liệu kết quả.

## Citation

Tên bài: Interpretability and Control in Forecasting Support Systems (bản chính thức HICSS; bản preprint arXiv có tên "Algorithmic Transparency in Forecasting Support Systems", tác giả Leif Feddersen)
Tác giả: Leif Feddersen, Catherine Cleophas
Năm: 2026
Nguồn: Proceedings of the 59th Hawaii International Conference on System Sciences (HICSS 2026), tr. 1445 (10 trang); preprint arXiv:2411.00699 (2024)
DOI/Link: https://doi.org/10.24251/HICSS.2026.172 (arXiv: https://arxiv.org/abs/2411.00699)

## Problem

Người dùng trong doanh nghiệp thường chỉnh tay dự báo. Thiết kế giao diện hệ thống hỗ trợ dự báo (FSS) thế nào để khuyến khích chỉnh sửa có lợi và hạn chế chỉnh sửa có hại?

## Method

Thí nghiệm người dùng (n = 197) với 3 thiết kế FSS: Opaque (không minh bạch), Interpretable (hiển thị phân rã chuỗi thời gian) và Control (cho người dùng chỉnh tham số các thành phần).

## Dataset

Subset M5: 10 chuỗi thuộc nhóm FOODS (đã kiểm tra trong PDF, mục 4.2–4.3); người tham gia dự báo 14 ngày tới.

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
