# Paper 18 Summary

**Nhóm:** Domain (inventory)

> Bài bổ sung (không có trong file Excel ban đầu). Tên bài, tác giả, năm, tạp chí, tập/số/trang và DOI **đã được kiểm tra qua Crossref / trang NeurIPS (2026-09-29)**. Phần tóm tắt nội dung viết từ kiến thức chung, nên đọc bài gốc trước khi trích số liệu.

## Citation

Tên bài: On the categorization of demand patterns
Tác giả: Aris A. Syntetos, John E. Boylan, J. D. Croston
Năm: 2005
Nguồn: Journal of the Operational Research Society, 56(5), 495–503
DOI/Link: https://doi.org/10.1057/palgrave.jors.2601841

## Problem

Nên chọn phương pháp dự báo nào cho từng loại mẫu nhu cầu trong tồn kho?

## Method

Phân loại nhu cầu theo ADI (khoảng cách trung bình giữa các lần có nhu cầu) và CV² (độ biến thiên kích thước nhu cầu), ngưỡng ADI = 1,32 và CV² = 0,49, cho ra 4 nhóm: smooth, erratic, intermittent, lumpy.

## Dataset

Phân tích lý thuyết + dữ liệu thực.

## Evaluation

MSE lý thuyết của các phương pháp dự báo.

## Results

Đưa ra quy tắc chọn phương pháp (SES/Croston/SBA) theo nhóm nhu cầu; trở thành chuẩn phân loại trong ngành.

## Limitations

Ngưỡng được suy ra cho các phương pháp thống kê cụ thể; không bao gồm ML.

## Relevance to our topic

**Rất cao.** Là khung để nhóm phân tích kết quả theo loại nhu cầu (đóng góp số 2).

## Possible improvement

Áp dụng phân loại ADI–CV² cho 30.490 SKU M5 và báo cáo KPI tồn kho theo từng nhóm.
