# Paper 15 Summary

**Nhóm:** AI model / method

> Bài bổ sung (không có trong file Excel ban đầu). Tên bài, tác giả, năm, tạp chí, tập/số/trang và DOI **đã được kiểm tra qua Crossref / trang NeurIPS (2026-09-29)**. Phần tóm tắt nội dung viết từ kiến thức chung, nên đọc bài gốc trước khi trích số liệu.

## Citation

Tên bài: Forecasting and stock control for intermittent demands
Tác giả: J. D. Croston
Năm: 1972
Nguồn: Journal of the Operational Research Society (lúc đó tên là Operational Research Quarterly), 23(3), 289–303
DOI/Link: https://doi.org/10.1057/jors.1972.50

## Problem

Làm mịn hàm mũ (SES) bị lệch khi nhu cầu rời rạc (nhiều kỳ bằng 0).

## Method

Tách chuỗi thành hai phần: kích thước nhu cầu khác 0 và khoảng cách giữa các lần có nhu cầu, rồi làm mịn riêng từng phần.

## Dataset

Dữ liệu tồn kho mô phỏng/thực tế (phân tích lý thuyết).

## Evaluation

Độ lệch và phương sai của dự báo; tác động tới tồn kho.

## Results

Cho dự báo ít lệch hơn SES đối với nhu cầu rời rạc, trở thành phương pháp chuẩn trong thực tế.

## Limitations

Vẫn còn lệch (sau này được sửa bởi SBA); không cập nhật khi sản phẩm ngừng bán (obsolescence).

## Relevance to our topic

**Cao.** Baseline chuẩn cho nhóm SKU rời rạc.

## Possible improvement

Dùng làm baseline thống kê trong thí nghiệm.
