# Problem Statement

> Quy ước nguồn: `(bài X, tr. N)` theo `02_related_work/paper_list.md`; `[DP]` = số liệu nhóm tự tính, tái lập được bằng `code/profile_datasets.py` (báo cáo: `code/outputs/data_profile.md`).

## 1. Vấn đề thực tế

Nhà bán lẻ phải cân bằng hai rủi ro ngược chiều:

- **Hết hàng (stockout):** mất doanh thu và khách hàng.
- **Tồn kho dư thừa (overstock):** tốn chi phí lưu kho, đọng vốn, hàng phải giảm giá hoặc thanh lý. Ví dụ thực tế ở bài 25 (tr. 7): tồn cuối kỳ của nhiều phụ tùng vượt xa mức safety stock trong thời gian dài.

Bài toán khó vì nhu cầu bán lẻ có ba đặc điểm:

1. **Biến động theo giá, sự kiện, mùa vụ.** Ví dụ, trong M5 chương trình SNAP chiếm khoảng 33% số ngày (bài 01, tr. 6); với dữ liệu Việt Nam, lịch có cờ Tết Nguyên đán [DP].
2. **Nhu cầu rời rạc và lumpy chiếm đa số.**
   - M5 theo ngày: 73% intermittent và 17% lumpy (bài 01, tr. 8).
   - M5 theo tuần: 39,7% số tuần bằng 0, 56,7% chuỗi intermittent [DP].
   - Dataset giày dép Việt Nam theo tuần: cấp SKU × cửa hàng có **98,5% số tuần bằng 0**; ở cấp mẫu–màu toàn chuỗi vẫn còn 47,9% [DP].
3. **Sản phẩm có vòng đời và mùa ra mắt** (đặc biệt trong thời trang/giày dép). Hàng cuối mùa cần được xử lý chứ không chỉ nhập thêm.

Với mỗi chuỗi sản phẩm, người quản lý cần quyết định mỗi kỳ: **nhập thêm bao nhiêu**, **giữ nguyên**, hay **thanh lý/giảm giá** phần tồn dư.

## 2. Vì sao vấn đề này quan trọng

- **Cần dự báo xác suất, không chỉ dự báo điểm.** Quyết định tồn kho an toàn cần biết độ bất định; trong bán lẻ, các phân vị cao (0,925–0,995) thường dùng để xác định safety stock (bài 03, tr. 2).
- **Độ chính xác dự báo chưa phải mục tiêu cuối.**
  - M5 đánh giá bằng WRMSSE và WSPL (bài 01, tr. 3), và **không gắn với một bài toán ra quyết định cụ thể** (bài 03, tr. 2–3).
  - Trong tồn kho, độ chính xác cao hơn không nhất thiết cho quyết định tốt hơn (bài 11, abstract); dự báo đúng các kỳ bằng 0 làm giảm tồn kho nhưng tăng thiếu hàng (bài 24, tr. 21).
- **Chuỗi rời rạc thường bị chọn lọc bỏ** trong các nghiên cứu gắn với tồn kho trên M5: bài 22 chỉ dùng 8.000 chuỗi bán nhiều và tự nêu đây là "điểm yếu chính" (tr. 4, 18); bài 21 chỉ dùng tập con thực phẩm biến động mạnh (tr. 8).
- **Quyết định thanh lý chưa được xét cùng quyết định nhập hàng** trong các bài đã đọc toàn văn (11, 21–25; kết quả tìm từ khóa, xem `research_gap.md`).
- **Kết quả trên M5 chưa chắc đúng cho thị trường khác.** Chính nhóm tổ chức M5 thừa nhận kết luận của M5 có giới hạn khi khái quát hóa ngoài dữ liệu đó (bài 01, tr. 11). M5 là dữ liệu thực phẩm/gia dụng ở Mỹ; dữ liệu Việt Nam là giày dép, đa kênh, có giá vốn và tồn kho thực [DP].

## 3. Phát biểu bài toán

> Xây dựng một **benchmark "từ dự báo đến quyết định"** trên **hai miền bán lẻ** — M5 (Walmart, Mỹ) và dữ liệu giày dép Việt Nam (Vietnam Datathon 2023) — ở **tần suất tuần**. Benchmark so sánh nhiều phương pháp dự báo xác suất khi đưa vào **cùng một lớp quyết định nhập hàng + thanh lý** trong mô phỏng tồn kho nhiều kỳ có lead time, **giữ lại toàn bộ các nhóm nhu cầu**, và báo cáo KPI tồn kho **theo từng nhóm ADI–CV²** và **theo từng dataset**.

## 4. Phạm vi

| | M5 | Việt Nam |
|---|---|---|
| Chuỗi dự báo | Item × cửa hàng, **30.490 chuỗi**, 278 tuần Walmart [DP] | **Mẫu–màu × toàn chuỗi**, kênh bán lẻ, **1.006 chuỗi**, 84 tuần [DP] |
| Lý do chọn cấp | Cấp gốc của M5; theo tuần còn 39,7% số 0 | Cấp SKU × cửa hàng có 98,5% số 0, không dự báo được; cấp mẫu–màu × chuỗi có đủ 4 nhóm ADI–CV² (35/33/22/10%) [DP] |
| Đặc trưng ngoại sinh | Giá bán, sự kiện, SNAP | Giá bán thực, giá niêm yết, **giá vốn**, Tết, thuộc tính sản phẩm (nhóm, giới tính, phong cách, mùa ra mắt) |
| Tham số chi phí | **Giả định** + phân tích độ nhạy | Ước lượng từ **giá vốn và giá bán thực** (giá vốn ≈ 69% giá niêm yết, trung vị [DP]) |

## 5. Giả định và hạn chế dữ liệu

- **M5 không có tồn kho thực.** Tồn kho ban đầu, lead time, chu kỳ đặt hàng và chi phí là tham số giả định, kèm phân tích độ nhạy.
- **Doanh số không hoàn toàn bằng nhu cầu**: khi hết hàng, doanh số bằng 0 dù nhu cầu khác 0 (nhận định nhóm).
- **Dữ liệu Việt Nam:**
  - Chỉ có **tuần**, không có ngày; **84 tuần** sau khi loại tuần bất thường 202352 (2.583 dòng) [DP].
  - Có **26.432 dòng trả hàng** (số lượng âm) cần xử lý [DP].
  - Tồn kho chỉ chụp cuối tháng **năm 2022**; chỉ **10 cửa hàng (1201–1210)** có đủ 12 tháng [DP].
  - Tồn kho tháng 01/2022 tại 10 cửa hàng này bằng **216–485 tuần bán** [DP]. Nghi ngờ file doanh số (`*_split_1.xlsx`) **chỉ chứa một phần giao dịch** → tồn kho thực **chỉ dùng để mô tả**, không dùng để kiểm chứng mô phỏng, cho tới khi xác minh với ban tổ chức.
  - Giấy phép trên Kaggle ghi "Unknown" → trích dẫn nguồn và xin phép ban tổ chức trước khi công bố.
- **Không mô hình hóa phản ứng của nhu cầu khi giảm giá**; quyết định thanh lý chỉ được so sánh giữa các chính sách trong mô phỏng.
