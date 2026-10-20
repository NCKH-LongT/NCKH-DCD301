# Dataset

`[DP]` = `code/outputs/data_profile.md` (sinh bởi `code/profile_datasets.py`). Số chuỗi được đánh giá và nhóm nhu cầu lấy từ `code/outputs/<D>/summary.md`.

## 1. Tổng quan

| | M5 | VN1 | Phụ lục: giày dép Việt Nam |
|---|---|---|---|
| Nguồn | Kaggle *M5 Forecasting – Accuracy* (Walmart) | *VN1 Forecasting – Accuracy Challenge*, Vandeput (2024), DataSource.ai | Kaggle `tienanh2003/sales-and-inventory-snapshot-data` (Vietnam Datathon 2023) |
| Loại hình | 1 nhà bán lẻ, 10 cửa hàng vật lý ở 3 bang (Mỹ) | 46 nhà bán hàng thương mại điện tử, 328 kho [DP]; chủ yếu Mỹ (bài 08, tr. 7) | Dữ liệu bán lẻ giày dép Việt Nam, 4 thương hiệu ẩn danh, 221 điểm bán |
| Cấp chuỗi | sản phẩm × cửa hàng | client × kho × sản phẩm | mẫu–màu × toàn chuỗi |
| Số chuỗi | 30.490 | 15.053 | 1.006 |
| Tần suất gốc → dùng | Ngày → tuần Walmart | Tuần | Giao dịch → tuần |
| Số tuần dùng (ngày đầu tuần) | 277 (2011-01-29 → 2016-05-14, tuần đủ 7 ngày) | 196 (2020-07-06 → 2024-04-01) | 84 |
| Tỷ lệ tuần bằng 0 | 39,7% [DP] | 69,9% [DP] | 47,9% [DP] |
| Giá | `sell_prices.csv` theo tuần | Phase 0–1, chỉ ở tuần có bán (29,3% số ô) [DP] | Có giá bán và giá vốn |
| Sự kiện / thuộc tính | Sự kiện, SNAP; ngành, phòng ban, cửa hàng, bang | Không (mã client, kho ẩn danh) | Nhóm sản phẩm, kênh |
| Tồn kho, giá vốn | Không có | Không có | Có ảnh chụp tồn kho cuối tháng 2022 |
| Vai trò | **Benchmark chính** | **Benchmark chính** | **Chỉ mô tả** |

Lưu ý: "VN1" là tên cuộc thi, **không phải dữ liệu Việt Nam**.

## 2. Tiền xử lý (`code/f2d/data.py`)

**M5**

- Cộng doanh số ngày theo tuần Walmart `wm_yr_wk`. Tuần cuối (11618) chỉ có 2 ngày (d_1940–d_1941) nên bị bỏ → 277 tuần.
- Lịch: số sự kiện (`event_name_1`, `event_name_2`) và số ngày SNAP của bang của cửa hàng, theo tuần.
- Giá: `sell_price` theo tuần, chỉ lấy các tuần trong panel (bỏ 28 ngày ẩn sau d_1941); giá thiếu được điền bằng giá gần nhất trước đó.
- **Tuần bắt đầu của chuỗi** = tuần đầu có giá trong `sell_prices.csv` (sản phẩm lên kệ); các tuần trước đó là NaN, không tính là 0.

**VN1**

- Ghép Phase 0 (170 tuần) + Phase 1 (13 tuần) + Phase 2 (13 tuần, đáp án chính thức) theo `Client`, `Warehouse`, `Product`.
- Giá: Phase 0–1, điền bằng giá gần nhất trước đó; Phase 2 không có giá.
- **Tuần bắt đầu** = tuần có bán đầu tiên.

**Phụ lục — giày dép Việt Nam:** giữ kênh "Bán lẻ"; bỏ tuần bất thường 202352; không trừ trả hàng; gộp lên mẫu–màu × toàn chuỗi. **Cập nhật 10/10/2026:** mã 202352 thực chất là ngày 1/1/2023 bị gán sai năm (thuộc tuần ISO 2022-W52), không phải tuần bất thường; case study (`f2d.data.load_vnf`, `06_experiment_results/results.md` mục 10.4) gộp nó vào 202252, bỏ 202153 (1–2/1/2022) và 202331 (chỉ có 31/7/2023). Dữ liệu gồm 4 thương hiệu ẩn danh (Brand1 khoảng 82% số đơn vị), 42 nhà cung cấp, 221 điểm bán ở kênh bán lẻ; "toàn chuỗi" ở đây là tổng trên mọi cửa hàng của bộ dữ liệu, không phải một chuỗi duy nhất.

## 3. Chia dữ liệu

| | M5 | VN1 |
|---|---|---|
| Kiểm thử (26 tuần) | 2015-11-21 → 2016-05-14 | 2023-10-09 → 2024-04-01 (= Phase 1 + Phase 2) |
| Khối 1 / khối 2 | 13 + 13 tuần | Phase 1 / Phase 2 |
| Validation | 13 origin ngay trước mỗi mốc cắt | Như M5 |
| Huấn luyện | Tối đa 104 origin trước validation | Như M5 |

## 4. Chuỗi được đánh giá và nhóm nhu cầu

Điều kiện để một chuỗi được đánh giá:

- chuỗi bắt đầu ít nhất 13 tuần trước giai đoạn kiểm thử;
- chuỗi có ít nhất một tuần có bán trong giai đoạn huấn luyện.

ADI–CV² được tính trên giai đoạn trước kiểm thử, từ tuần bắt đầu của chuỗi, với ngưỡng ADI = 4/3, CV² = 0,5 (bài 01, tr. 7–8).

| Nhóm | M5 | | VN1 | |
|---|---|---|---|---|
| | Số chuỗi | % | Số chuỗi | % |
| smooth | 16.102 | 53,0 | 2.596 | 18,8 |
| erratic | 1.777 | 5,8 | 1.901 | 13,7 |
| intermittent | 10.285 | 33,9 | 6.539 | 47,2 |
| lumpy | 2.217 | 7,3 | 2.808 | 20,3 |
| **Tổng** | **30.381** | 100 | **13.844** | 100 |

- Số chuỗi bị loại:
  - VN1 1.209 chuỗi: tất cả có lần bán đầu tiên muộn hơn 13 tuần trước giai đoạn kiểm thử.
  - M5 109 chuỗi: sản phẩm lên kệ quá muộn, hoặc không có tuần nào có bán trước giai đoạn kiểm thử.
- Phân bố trong [DP] khác bảng trên (M5: 56,7% intermittent; VN1: 31,1% lumpy), vì [DP] tính ADI trên **toàn bộ lưới thời gian**, kể cả các tuần trước khi sản phẩm bắt đầu bán. Benchmark dùng bảng trên.
- Hai dataset có cơ cấu nhóm khác nhau rõ: M5 chủ yếu smooth; VN1 chủ yếu intermittent và lumpy. Điều này cho phép kiểm tra kết luận theo nhóm có lặp lại giữa hai dataset không (RQ2).

## 5. Lý do chọn dataset

- **M5:** benchmark bán lẻ chuẩn, có giá và lịch sự kiện; có nhiều bài trước để so sánh (bài 01–03, 11, 21).
- **VN1:** công khai, có đáp án chính thức cho 13 tuần cuối, khác loại hình (thương mại điện tử nhiều nhà bán), đã được dùng trong nghiên cứu (bài 08, chỉ đánh giá độ chính xác).
- **Dataset Việt Nam chỉ ở phụ lục**, vì hai lý do:
  - tồn kho đầu năm 2022 bằng 216–485 tuần bán ở 10 cửa hàng có đủ dữ liệu [DP], nên nghi ngờ file doanh số (`*_split_1`) chỉ chứa một phần giao dịch;
  - giấy phép ghi "Unknown".

## 6. Giấy phép và trích dẫn

- M5: dùng theo điều khoản cuộc thi Kaggle; trích dẫn bài 01.
- VN1: trích dẫn Vandeput (2024), *VN1 Forecasting – Accuracy Challenge*, DataSource.ai, như bài 08.
- Dữ liệu **không** đưa lên git (`data/` nằm trong `.gitignore`); cách tải: `code/README.md`.
