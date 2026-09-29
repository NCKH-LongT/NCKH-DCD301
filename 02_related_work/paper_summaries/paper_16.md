# Paper 16 Summary

**Nhóm:** AI model / method (+ domain)

> Bài bổ sung (không có trong file Excel ban đầu). Tên bài, tác giả, năm, tạp chí, tập/số/trang và DOI **đã được kiểm tra qua Crossref / trang NeurIPS (2026-09-29)**. Phần tóm tắt nội dung viết từ kiến thức chung, nên đọc bài gốc trước khi trích số liệu.

## Citation

Tên bài: Intermittent demand: Linking forecasting to inventory obsolescence
Tác giả: Ruud H. Teunter, Aris A. Syntetos, M. Zied Babai
Năm: 2011
Nguồn: European Journal of Operational Research, 214(3), 606–615
DOI/Link: https://doi.org/10.1016/j.ejor.2011.05.018

## Problem

Croston không cập nhật dự báo trong các kỳ không có nhu cầu, nên phản ứng chậm khi sản phẩm sắp lỗi thời, dẫn tới tồn kho chết.

## Method

Phương pháp TSB: cập nhật **xác suất có nhu cầu** mỗi kỳ (kể cả kỳ bằng 0) thay vì khoảng cách giữa các lần có nhu cầu.

## Dataset

Dữ liệu mô phỏng và thực tế.

## Evaluation

Sai số dự báo, chi phí tồn kho và lượng hàng lỗi thời.

## Results

TSB giảm rủi ro tồn kho lỗi thời so với Croston/SBA khi nhu cầu suy giảm.

## Limitations

Mô hình thống kê cục bộ, không dùng biến ngoại sinh (giá, sự kiện).

## Relevance to our topic

**Rất cao.** Nối trực tiếp dự báo với **tồn kho lỗi thời**, là cơ sở lý thuyết cho khuyến nghị THANH LÝ.

## Possible improvement

Dùng TSB làm baseline mạnh cho nhóm SKU rời rạc/lumpy.
