# Paper 22 Summary

**Nhóm:** AI model / method + M5
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn** (PDF open access trong `papers_pdf/1-s2.0-S2949863525000809-main.pdf`, 20 trang).

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: A hybrid learning framework for forecasting uncertainty and adaptive inventory planning in retail supply chains
Tác giả: Zizi Mohammed, Chafi Anas, Mohammed El Hammoumi
Năm: 2026
Nguồn: Supply Chain Analytics, 13, 100180
DOI/Link: https://doi.org/10.1016/j.sca.2025.100180

## Problem

- Dự báo nhu cầu và lượng hóa độ bất định là nền tảng cho quyết định tồn kho dựa trên rủi ro; thiếu hệ thống lượng hóa bất định được thiết lập tốt (abstract; tr. 2).

## Method

- Stacked ensemble gồm XGBoost, LightGBM và mạng lai LSTM-GRU, cộng với **GARCH(1,1)** mô hình hóa phương sai có điều kiện của phần dư để tạo khoảng tin cậy 95% thích nghi (abstract; mục 3.5–3.7, tr. 6–8).
- Có đưa ra công thức safety stock theo lead time và newsvendor một kỳ dùng phương sai GARCH (công thức 19–21, tr. 9).

## Dataset

- M5, dùng **8.000 chuỗi sản phẩm bán nhiều (high-volume)**, 58 đặc trưng; chia train/test 75:25 (Bảng 2, tr. 4).
- Phân loại theo ADI/CV² (ngưỡng 1,32 và 0,49): 56,2% smooth, 22,8% erratic, 15,4% intermittent, 5,6% lumpy (tr. 4).

## Evaluation

- R², RMSE, MAE; phương sai có điều kiện; mức điều chỉnh dự báo giữa các ngày (abstract).

## Results

- Stacked ensemble: R² = 0,9681, RMSE = 1,48, MAE = 0,77 đơn vị, tốt hơn các mô hình cơ sở; phương sai có điều kiện trung bình 2,82 (abstract).
- Phần kết quả (mục 4) chủ yếu báo cáo metric dự báo; **không có bảng KPI tồn kho** (fill rate, chi phí) — nhóm đã tìm các từ khóa này trong mục 4.

## Limitations

- Tác giả tự nêu (tr. 4): chỉ dùng 8.000 mặt hàng bán nhiều, **không đánh giá mặt hàng bán thưa/chậm** (nhiều số 0), vốn cần kỹ thuật như Croston, SBA, TSB.
- Tác giả tự nêu (tr. 16–17): chi phí tính toán lớn (45–60 phút trên GPU cho 8.000 chuỗi); GARCH giả định phần dư dừng; chỉ thử nghiệm trên M5.

## Relevance to our topic

[Nhận định nhóm] **Cao.** Cùng hướng "dự báo bất định cho tồn kho" trên M5, nhưng **bỏ qua chuỗi rời rạc** (73% M5 theo bài 01) và không đánh giá KPI tồn kho — hai điểm nhóm làm được.

## Possible improvement

[Nhận định nhóm] Dẫn chứng trực tiếp cho gap: "các nghiên cứu dự báo bất định cho tồn kho trên M5 thường loại chuỗi rời rạc" (bài 22 tr. 4; bài 11 tr. 17 loại chuỗi không có lịch sử).
