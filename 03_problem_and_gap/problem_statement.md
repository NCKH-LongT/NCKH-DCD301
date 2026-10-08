# Problem Statement

> Quy ước nguồn: `(bài X, tr. N)` theo `02_related_work/paper_list.md`; `[DP]` = số liệu nhóm tự tính, tái lập được bằng `code/profile_datasets.py` (báo cáo: `code/outputs/data_profile.md`).

## 1. Vấn đề thực tế

Nhà bán lẻ phải cân bằng hai rủi ro ngược chiều:

- **Hết hàng (stockout):** mất doanh thu và khách hàng.
- **Tồn kho dư thừa (overstock):** đọng vốn, tốn chi phí lưu kho, hàng phải giảm giá hoặc thanh lý. Ví dụ thực tế ở bài 25 (tr. 7): tồn cuối kỳ của nhiều phụ tùng vượt xa mức safety stock trong thời gian dài.

Bài toán khó vì:

1. **Nhu cầu biến động theo giá, sự kiện, mùa vụ.** Ví dụ, SNAP chiếm khoảng 33% số ngày trong M5 (bài 01, tr. 6).
2. **Nhu cầu rời rạc và lumpy chiếm đa số** [DP]:

   | Dataset (theo tuần) | Tỷ lệ tuần bằng 0 | Intermittent | Lumpy | Smooth | Erratic |
   |---|---|---|---|---|---|
   | M5 (Walmart, item × cửa hàng) | 39,7% | 56,7% | 10,1% | 29,6% | 3,6% |
   | VN1 (thương mại điện tử, client × kho × sản phẩm) | 69,9% | 57,6% | 31,1% | 5,9% | 5,4% |

3. **Sản phẩm có vòng đời.** Hàng bán chậm hoặc cuối vòng đời cần được xử lý, không chỉ nhập thêm.

Mỗi kỳ, với mỗi chuỗi sản phẩm, người quản lý cần quyết định: **nhập thêm bao nhiêu**, **giữ nguyên**, hay **thanh lý/giảm giá** phần tồn dư.

## 2. Vì sao vấn đề này quan trọng

- **Cần dự báo xác suất.** Quyết định tồn kho an toàn cần biết độ bất định; các phân vị cao (0,925–0,995) thường dùng để xác định safety stock (bài 03, tr. 2).
- **Độ chính xác dự báo chưa phải mục tiêu cuối.**
  - M5 đánh giá bằng WRMSSE và WSPL (bài 01, tr. 3), và không gắn với một bài toán ra quyết định cụ thể (bài 03, tr. 2–3).
  - Các nghiên cứu dùng VN1 tới nay cũng đánh giá bằng độ chính xác và chi phí tính toán (bài 08, tr. 13–14).
  - Trong tồn kho, độ chính xác cao hơn không nhất thiết cho quyết định tốt hơn (bài 11, abstract).
- **Chuỗi rời rạc thường bị chọn lọc bỏ** trong các nghiên cứu gắn với tồn kho trên M5 (bài 22, tr. 4, 18; bài 21, tr. 8).
- **Quyết định thanh lý chưa được xét cùng quyết định nhập hàng** trong các bài đã đọc toàn văn (11, 21–25; xem `research_gap.md`).
- **Kết luận trên một dataset khó khái quát.** Nhóm tổ chức M5 thừa nhận điều này (bài 01, tr. 11). M5 là một nhà bán lẻ với cửa hàng vật lý; VN1 gồm 46 nhà bán hàng thương mại điện tử qua 328 kho (bài 08, tr. 7) [DP].

## 3. Phát biểu bài toán

> Xây dựng một **benchmark "từ dự báo đến quyết định"** trên **hai dataset bán lẻ công khai** — **M5** (Walmart, cửa hàng vật lý) và **VN1** (thương mại điện tử nhiều nhà bán) — ở **tần suất tuần**. Benchmark so sánh nhiều phương pháp dự báo xác suất khi đưa vào **cùng một lớp quyết định nhập hàng + thanh lý** trong mô phỏng tồn kho nhiều kỳ, **giữ lại toàn bộ các nhóm nhu cầu**, và đánh giá bằng **KPI tồn kho không phụ thuộc chi phí tuyệt đối**, theo từng nhóm ADI–CV² và từng dataset.

## 4. Phạm vi

| | M5 | VN1 |
|---|---|---|
| Nguồn | Kaggle M5 Forecasting – Accuracy | VN1 Forecasting – Accuracy Challenge (Vandeput, 2024; DataSource.ai) |
| Chuỗi dự báo | Item × cửa hàng, **30.490 chuỗi** [DP] | Client × kho × sản phẩm, **15.053 chuỗi** [DP] |
| Độ dài | 278 tuần (2011–2016) [DP] | 196 tuần (07/2020–04/2024), gồm 13 tuần đáp án chính thức (Phase 2) [DP] |
| Đặc trưng ngoại sinh | Giá, sự kiện, SNAP, thuộc tính sản phẩm/cửa hàng | Giá (có ở 29,3% số ô, thường chỉ khi có bán) [DP]; mã client/kho |
| Thị trường | Mỹ, 1 nhà bán lẻ, 10 cửa hàng | Chủ yếu Mỹ, 46 nhà bán hàng TMĐT, 328 kho (bài 08, tr. 7) |

**Phụ lục (mô tả, không dùng để rút kết luận):** dataset giày dép Việt Nam (Vietnam Datathon 2023). Lý do chỉ để phụ lục: nghi ngờ doanh số chưa đầy đủ (tồn kho bằng 216–485 tuần bán ở 10 cửa hàng [DP]) và giấy phép ghi "Unknown".

## 5. Cách đánh giá không phụ thuộc chi phí tuyệt đối

Hai dataset đều **không có tồn kho, lead time hay giá vốn thực**. Thay vì giả định các con số chi phí, nghiên cứu:

1. **Chạy theo mức phục vụ mục tiêu** τ ∈ {0,8; 0,9; 0,95}. Cách này tương đương với tỷ lệ chi phí chuẩn hóa c_o = 1, c_u ∈ {4, 9, 19}, giống bài 11 (tr. 16).
2. **Báo cáo KPI không có đơn vị tiền:** fill rate, mức phục vụ đạt được so với mục tiêu, tỷ lệ tuần hết hàng, tồn kho trung bình tính bằng số tuần nhu cầu.
3. **Vẽ đường đánh đổi tồn kho – fill rate** của từng phương pháp. Phương pháp có đường tốt hơn thì tốt hơn với **mọi** mức chi phí.
4. **Thanh lý:** báo cáo lượng tồn dư giảm được so với số tuần hết hàng tăng thêm, và **ngưỡng giá thu hồi hòa vốn** theo từng nhóm nhu cầu, dưới dạng đường cong theo chi phí lưu kho, không chọn một con số cố định.
5. **Lead time** L ∈ {1, 2, 4} tuần được trình bày là **kịch bản**.

## 6. Giả định và hạn chế còn lại

- **Doanh số không hoàn toàn bằng nhu cầu**: khi hết hàng, doanh số bằng 0 dù nhu cầu khác 0 (nhận định nhóm). Áp dụng cho cả hai dataset.
- **VN1:** mã sản phẩm đã ẩn danh, không có thuộc tính sản phẩm hay lịch sự kiện; giá chỉ có ở 29,3% số ô [DP].
- **M5:** dùng giá bán để quy đổi KPI theo giá trị khi cần; không giả định giá vốn.
- **Không mô hình hóa phản ứng của nhu cầu khi giảm giá**; thanh lý chỉ so sánh giữa các chính sách trong mô phỏng.
