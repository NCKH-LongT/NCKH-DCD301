# Topic Revision Log

| Version | Date | Change | Reason |
|---|---|---|---|
| v0.1 | 2026-05-21 | Đề tài cũ: Combinational Logic Design using Decoders (file `topic_proposal` không đuôi) | Bài tập khởi động |
| v1.0 | 2026-09-29 | Chuyển sang đề tài: Probabilistic demand forecasting → khuyến nghị nhập hàng / thanh lý trên M5 | Chọn lĩnh vực Quản lý kho theo Bước 1 README; có dataset công khai lớn (M5) và 13 bài báo nền |
| v1.1 | 2026-09-29 | Bổ sung 6 bài (model/method + domain); xác định bài 11 là đối thủ gần nhất và thêm 3 điểm khác biệt | Hoàn thành Bước 2–4 |
| v1.2 | 2026-09-29 | Kiểm tra toàn bộ 19 reference (Crossref, arXiv API, HTTP); sửa venue của bài 04, 06, 07, 15; sửa lại điểm khác biệt so với bài 11 sau khi đọc PDF | Đảm bảo reference chính xác, tránh phản biện bắt lỗi |
| v2.0 | 2026-10-08 | Chuyển hướng thành **benchmark "từ dự báo đến quyết định" trên 2 dataset** (M5 + giày dép Việt Nam, Vietnam Datathon 2023) ở **tần suất tuần**; cập nhật Bước 5–6; viết Bước 7 (thiết kế hệ thống); thêm `code/profile_datasets.py` | Định hướng tạp chí Q3–Q4; dữ liệu VN có giá vốn và tồn kho thực; tăng khả năng khái quát hóa ngoài M5 |
| v2.1 | 2026-10-08 | Dataset chính đổi thành **M5 + VN1** (VN1 Forecasting – Accuracy Challenge, 15.053 chuỗi tuần); dataset Datathon Việt Nam chuyển sang **phụ lục mô tả**; bỏ chi phí tuyệt đối, đánh giá bằng **KPI không đơn vị tiền**, đường đánh đổi tồn kho – fill rate và ngưỡng hòa vốn thanh lý | Không xác minh được độ đầy đủ và giấy phép của dữ liệu Datathon; giả định chi phí không đủ tin cậy cho tạp chí Q3–Q4; VN1 công khai, có đáp án chính thức, đã có tiền lệ học thuật (bài 08) |
| v2.2 | 2026-10-09 | **Bỏ deep learning** (TiDE/DeepAR); thêm baseline ML: LightGBM + conformal, HistGradientBoosting quantile; thêm TSB negative binomial; sửa lỗi đặc trưng `price_observed` của VN1; thêm phân tích ngưỡng hòa vốn thanh lý | Phần cứng (CPU, GPU 4 GB) không đủ cho mô hình sâu; LightGBM là lời giải mạnh nhất ở M5 (bài 02, 03); bài 12 cho thấy mô hình lớn không chắc tốt hơn |
| v2.3 | 2026-10-09 | Rà soát tài liệu Bước 1–7 theo code và kết quả: viết lại `topic_proposal.md`; sửa tỷ lệ nhóm nhu cầu của chuỗi được đánh giá, mô tả KPI, thứ tự mô phỏng, ngưỡng hòa vốn, thời gian chạy, trạng thái cài đặt; viết Bước 5 (`05_methodology/`) và Bước 6 (`06_experiment_results/`) từ kết quả đã chạy | Tài liệu phải khớp với những gì đã cài đặt và đo được |

## Việc cần làm tiếp

- [x] Bổ sung ≥ 3 bài về model/phương pháp AI (bài 14–17).
- [x] Bổ sung ≥ 2 bài về domain tồn kho (bài 18–19).
- [x] Kiểm tra năm, venue, DOI của bài 14–19 (Crossref).
- [x] Kiểm tra chính sách tồn kho và metric của bài 11 (newsvendor từng kỳ; total cost / holding / stockout).
- [ ] Đọc toàn văn bài 11 và bổ sung Goltsos et al. (2022) vào Related Work.
- [ ] Kiểm định thống kê, cửa sổ kiểm thử thứ hai, bất thường Tweedie VN1 h = 13 (`06_experiment_results/results.md` mục 9).
