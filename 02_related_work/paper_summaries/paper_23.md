# Paper 23 Summary

**Nhóm:** AI model / method + Domain (inventory) — **nguồn thứ cấp kiểm chứng cho bài 15, 16, 18**
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn** (PDF open access CC BY trong `papers_pdf/applsci-15-12030-v3.pdf`, 35 trang).

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: A New Approach to Forecast Intermittent Demand and Stock-Keeping-Unit Level Optimization for Spare Parts Management
Tác giả: Dimitrios S. Sfiris, Dimitrios E. Koulouriotis
Năm: 2025
Nguồn: Applied Sciences (MDPI), 15(22), 12030
DOI/Link: https://doi.org/10.3390/app152212030

## Problem

- Nhu cầu phụ tùng rời rạc và lumpy đòi hỏi chọn đúng mô hình dự báo cho từng mặt hàng (abstract).

## Method

- Tổng quan họ Croston (tr. 1–2, Bảng tr. 4): Croston bị **lệch dương** nên có SBA sửa lệch; **TSB** thay khoảng cách giữa các lần có nhu cầu bằng **xác suất xảy ra nhu cầu** giảm dần theo hàm mũ, xử lý vấn đề **lỗi thời** (end-of-lifecycle).
- Đề xuất phương pháp **SK** (ước lượng xác suất xảy ra nhu cầu không tham số) và biến thể SK–SSA; thước đo sSPEC; cơ chế chọn mô hình theo từng SKU (MCOST) (tr. 2).
- Phân loại theo ADI–CV² với **4 nhóm: Smooth (ADI ≤ 1,32 và CV² ≤ 0,49), Intermittent (ADI > 1,32 và CV² ≤ 0,49), Erratic (ADI ≤ 1,32 và CV² > 0,49), Lumpy (ADI > 1,32 và CV² > 0,49)** (tr. 10, mục 2.5).
- Tồn kho: chính sách **(R, Q)** xem xét liên tục, cho phép backorder; nhu cầu trong lead time mô hình hóa bằng phân phối negative binomial–Bernoulli; **lead time cố định 3 ngày** (tr. 10–11, mục 2.6).

## Dataset

- Dữ liệu thực **2.050 SKU phụ tùng ô tô**, mỗi SKU 104 tuần (Bảng 5, tr. 14); dữ liệu **không công khai** (tr. 27).

## Evaluation

- sSPEC, MASE, sAPIS (tr. 2); safety stock, mức phục vụ, backorder (tr. 26).

## Results

- Cải thiện độ chính xác và giảm safety stock, backorder so với các baseline mạnh; **SK–SSA cho safety stock thấp nhất ở cùng mức phục vụ** (tr. 26).
- Tối ưu toàn bộ 2.050 SKU mất dưới 15 phút trên CPU thường (tr. 21).

## Limitations

- Tác giả nêu (tr. 25): lead time cố định (nên mở rộng sang lead time ngẫu nhiên); chưa mô hình hóa lịch và sự kiện; chỉ một ngành (ô tô) và dữ liệu theo tuần.

## Relevance to our topic

[Nhận định nhóm] **Cao.** (1) Làm **nguồn thứ cấp đã kiểm chứng** cho mô tả Croston, SBA, TSB và 4 nhóm ADI–CV². (2) Ví dụ về việc nối dự báo nhu cầu rời rạc với chính sách tồn kho và safety stock.

## Possible improvement

[Nhận định nhóm] Bài làm trên phụ tùng (không phải bán lẻ), không có biến ngoại sinh, không có thanh lý. Đề tài làm trên bán lẻ M5 với giá và sự kiện.
