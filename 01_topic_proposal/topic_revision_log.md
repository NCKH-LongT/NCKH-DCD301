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
| v2.4 | 2026-10-09 | Kiểm định Friedman–Nemenyi/Wilcoxon theo chuỗi; xếp hạng theo đường đánh đổi (τ mở rộng thành {0,5; …; 0,99}); sửa LightGBM-Tweedie/conformal để học mục tiêu D_h / s; thêm quy tắc thanh lý dead-stock (13/26 tuần); thêm cửa sổ kiểm thử thứ hai; cập nhật Bước 5–6 | Rà soát độ vững trước khi viết bài: SQL trung bình che khuất kết quả theo chuỗi trên VN1; Tweedie học mục tiêu chưa chuẩn hóa cho dự báo sai lớn trên VN1 |
| v2.5 | 2026-10-09 | Viết bản nháp bài báo tiếng Anh (Bước 11, `07_paper_draft/`); thêm phân tích loss theo từng phân vị (`code/per_quantile_loss.py`, `results.md` mục 2.1), qua đó sửa diễn giải "phân vị trên của LightGBM quantile tốt hơn ở chuỗi intermittent"; kiểm tra lại toàn bộ reference; rà soát nhất quán các tài liệu Bước 1–11 với kết quả và sửa sai số làm tròn | Chuẩn bị viết bài: mọi số liệu và nhận định trong bản nháp phải khớp với kết quả đã chạy |

## Việc cần làm tiếp

- [x] Bổ sung ≥ 3 bài về model/phương pháp AI (bài 14–17).
- [x] Bổ sung ≥ 2 bài về domain tồn kho (bài 18–19).
- [x] Kiểm tra năm, venue, DOI của bài 14–19 (Crossref).
- [x] Kiểm tra chính sách tồn kho và metric của bài 11 (newsvendor từng kỳ; total cost / holding / stockout).
- [x] Đọc toàn văn bài 11 (bản arXiv) và bổ sung Goltsos et al. (2022) vào Related Work (mức abstract).
- [x] Kiểm định thống kê, cửa sổ kiểm thử thứ hai, sửa Tweedie, dead-stock (`06_experiment_results/results.md`).
- [x] Bản nháp bài báo tiếng Anh (`07_paper_draft/`).
- [ ] Đọc toàn văn Goltsos et al. (2022) và Kourentzes et al. (2020) trước khi trích sâu hơn mức abstract/trang mô tả.
- [ ] (Tùy chọn) lưới L, H cho M5; ngưỡng hòa vốn cho cửa sổ thứ hai; đọc W3 và bài 20.
- [ ] Weekly reports (`weekly_reports/`) chưa phản ánh đề tài hiện tại.
- [ ] Điền tên leader/thành viên trong `topic_proposal.md` mục 1.
