# Giai đoạn 2 — B1 (đồng bộ) và B2 (khác biệt giữa M5 và VN1)

Ngày 13/10/2026. Quy trình: `07_paper_draft/phase2_workflow.md`.

Nguồn số liệu:

- `code/outputs/sync_check.md` (script `code/sync_check.py`);
- `code/outputs/dataset_shift.md` (script `code/dataset_shift.py`);
- bản sao trong `tables/`, hình trong `figures/fig_dataset_shift.png`.

Mọi đặc trưng theo chuỗi chỉ tính từ lịch sử **trước** giai đoạn kiểm thử, trên các chuỗi được đánh giá.

## B1 — Hai bộ dữ liệu đã đồng bộ chưa?

**Kết luận: đã đồng bộ ở mọi điểm ảnh hưởng tới so sánh.** Các khác biệt còn lại thuộc về bản chất dữ liệu.

| Tiêu chí | M5 | VN1 | Đánh giá |
|---|---|---|---|
| Độ dài tuần | 7 ngày | 7 ngày | Giống |
| Ngày đầu tuần | Thứ Bảy | Thứ Hai | Khác, không ảnh hưởng (hai bảng không ghép theo thời gian) |
| Thiếu doanh số sau điểm bắt đầu | 0 | 0 | Giống |
| Doanh số âm | 0 | 0 | Giống |
| Điều kiện chọn chuỗi; chia tập; mốc huấn luyện lại | Cùng một đoạn code | Cùng | Giống |
| Định nghĩa điểm bắt đầu chuỗi | Tuần đầu có giá (lên kệ) | Tuần bán đầu tiên | Khác về định nghĩa, **không khác về kết quả** (xem dưới) |
| Giá quan sát được sau điểm bắt đầu | 100% số ô | 44,6% số ô | Khác; giá VN1 được điền tiếp từ tuần trước. Kiểm tra bằng thử nghiệm bỏ đặc trưng giá (B0) |
| Đặc trưng của mô hình ML | 27 | 21 | 21 đặc trưng của VN1 đều có ở M5; M5 thêm 6 (sự kiện, SNAP, 4 thuộc tính) |
| Đơn vị chuỗi | sản phẩm × cửa hàng | nhà bán × kho × sản phẩm | Khác về bản chất; đã nêu trong bài |

**Về định nghĩa điểm bắt đầu chuỗi:**

- 99,5% chuỗi M5 có tuần lên kệ trùng với tuần bán đầu tiên.
- Tính lại M5 theo định nghĩa của VN1: tỷ lệ tuần bằng 0 giữ nguyên (24,4%), tỷ lệ các nhóm ADI–CV² đổi tối đa 0,1 điểm %, số chuỗi được đánh giá đổi 2–5 chuỗi.
- Điều này đúng ở cả ba cửa sổ.
- Vì vậy **không cần chạy thêm phiên bản M5 nào**.

**Lỗi phát hiện trong bài:** `final_paper_revA.docx` mục 3.4 ghi "M5 27, VN1 and VNF 21, 19 shared". Con số đúng là **21 đặc trưng chung**.

## B2 — Hai bộ dữ liệu khác nhau ở đâu?

### Mức khác biệt tổng thể

Một bộ phân loại "chuỗi này thuộc M5 hay VN1?" (5-fold, mẫu cân bằng):

| Đặc trưng dùng | AUC cửa sổ chính | Cửa sổ thứ hai | Cửa sổ thứ ba |
|---|---|---|---|
| Chỉ ADI và CV² | 0,865 | 0,866 | 0,855 |
| 9 đặc trưng chung (không phụ thuộc độ dài lịch sử hay giá) | 0,913 | 0,908 | 0,893 |
| Tất cả (thêm độ dài lịch sử, giá, mùa vụ) | 0,994 | 0,993 | 0,992 |

- AUC = 0,5 nghĩa là hai bộ giống nhau; AUC = 1 nghĩa là tách biệt hoàn toàn.
- Hai bộ dữ liệu **khác nhau rõ rệt** ngay cả khi chỉ nhìn hành vi nhu cầu, và mức khác biệt ổn định qua ba cửa sổ.
- ADI và CV² đã bắt được phần lớn khác biệt; các đặc trưng còn lại thêm khoảng 0,04–0,05 AUC.

### Khác ở đặc trưng nào (cửa sổ chính)

KS = khoảng cách Kolmogorov–Smirnov (0 = cùng phân phối, 1 = tách rời).

| Đặc trưng | Trung vị M5 [Q25–Q75] | Trung vị VN1 [Q25–Q75] | KS | Diễn giải |
|---|---|---|---|---|
| Độ dài lịch sử (tuần) | 230 [143–251] | 103 [50–160] | 0,68 | Chuỗi VN1 ngắn hơn một nửa |
| Biến động giá (CV) | 0,023 [0–0,049] | 0,082 [0,027–0,156] | 0,45 | Giá VN1 dao động mạnh hơn |
| ADI | 1,25 [1,08–1,59] | 2,18 [1,16–6,80] | 0,40 | VN1 rời rạc hơn nhiều; một phần tư số chuỗi bán chưa tới 1 tuần trong 7 |
| Tỷ lệ tuần bằng 0 | 19,8% [7,7–37,1] | 54,2% [14,1–85,3] | 0,40 | Như trên |
| Mức bán (log) | 1,65 | 0,89 | 0,34 | VN1 bán ít hơn |
| Số tuần từ lần bán gần nhất | 0 [0–0] | 1 [0–15] | 0,33 | Một phần tư chuỗi VN1 không bán ≥ 15 tuần trước kiểm thử |
| CV² cỡ đơn | 0,32 [0,24–0,41] | 0,34 [0,12–0,63] | 0,23 | Trung vị gần bằng; VN1 phân tán rộng hơn hẳn |
| Xu hướng 26 tuần (log) | 0,07 [−0,21–0,37] | −0,04 [−0,63–0,25] | 0,22 | VN1 biến động xu hướng mạnh hơn, lệch về giảm |
| Đỉnh bán so với cỡ đơn (52 tuần) | 0,84 [0,69–1,00] | 0,85 [0,47–1,16] | 0,21 | Trung vị bằng nhau; VN1 phân tán hơn |
| Mùa vụ (tự tương quan trễ 52) | 0,04 | 0,06 | 0,11 | Gần như giống; cả hai yếu |

Trong 9 đặc trưng chung, các đặc trưng đóng góp nhiều nhất vào khả năng phân biệt (độ quan trọng hoán vị): ADI (0,099), CV² (0,079), xu hướng 26 tuần (0,046), cỡ đơn (0,034), đỉnh bán (0,025).

**Ghi chú phương pháp:** đặc trưng "tỷ trọng tuần bán lớn nhất trên toàn lịch sử" (KS 0,62) bị loại khỏi bộ đặc trưng chung. Lý do: nó giảm một cách cơ học khi lịch sử dài hơn, nên không so sánh được giữa hai bộ dữ liệu. Nó được thay bằng "đỉnh bán so với cỡ đơn trong 52 tuần gần nhất".

### Hình

![PCA](figures/fig_dataset_shift.png)

Trên hai thành phần chính đầu tiên (71% phương sai):

- M5 tập trung trong một vùng (chuỗi bán đều, ADI thấp).
- VN1 phủ vùng đó **và** kéo dài sang vùng ADI cao / lâu không bán, nơi M5 gần như không có chuỗi nào.

### Ý nghĩa cho các bước sau

[Nhận định nhóm]

1. Vùng nhu cầu của M5 gần như là **tập con** của VN1. Kết luận rút từ M5 có thể chuyển sang phần "giống M5" của VN1, nhưng không chắc chuyển sang phần đuôi.
2. Ba đặc trưng mà ADI–CV² **không** chứa — xu hướng, độ gần của lần bán cuối, đỉnh bán — khác nhau rõ giữa hai bộ. Phân tích dịch chuyển nhu cầu (`code/outputs/demand_shift.md`) đã cho thấy chuỗi "tăng mạnh" và "ổn định" có phương pháp tốt nhất khác nhau. Đây là cơ sở để thử phân cụm trên bộ đặc trưng rộng hơn ở B3.
3. Bước B3 dùng 9 đặc trưng chung. Không dùng độ dài lịch sử và giá, vì hai đặc trưng này chủ yếu nhận diện "đây là dataset nào" chứ không mô tả hành vi nhu cầu.

## B2b — Khắc phục: làm cho hai bộ dữ liệu so sánh được

**Nguyên tắc:**

- **Không** biến đổi dữ liệu cho hai bộ giống nhau. Chúng khác nhau vì là hai loại hình bán lẻ khác nhau, và bài cần sự khác nhau đó để kiểm tra kết luận có chuyển được giữa các bối cảnh hay không.
- Thứ cần khắc phục là **khả năng so sánh**. Có ba nguồn khác biệt, mỗi nguồn một cách xử lý:

| Nguồn khác biệt | Cách xử lý | Trạng thái |
|---|---|---|
| (a) Thành phần chuỗi (VN1 nhiều chuỗi rời rạc hơn) | Đặt lại trọng số chuỗi để hai bộ có cùng phân phối đặc trưng, rồi so lại kết luận | ✅ xong (dưới đây) |
| (b) Giá: VN1 thiếu giá ở nhiều tuần và ở toàn bộ Phase 2 | Chạy lại 4 mô hình ML của VN1 không có đặc trưng giá | ✅ xong cả ba cửa sổ (`phase2_b3_b4.md` mục 3) |
| (c) Lượng thông tin của mô hình ML: M5 có thêm 6 đặc trưng (sự kiện, SNAP, 4 thuộc tính) | Chạy lại 4 mô hình ML của M5 chỉ với 21 đặc trưng chung | ✅ xong cả ba cửa sổ (cuối file này) |

### (a) So sánh sau khi cân bằng thành phần chuỗi

Nguồn: `code/outputs/matched_comparison.md` (script `code/matched_comparison.py`).

**Cách làm:**

- Trọng số nghịch đảo xác suất, lấy từ bộ phân loại "M5 hay VN1" trên 9 đặc trưng chung (xác suất ngoài mẫu).
- Trọng số được cắt ở phân vị 99.
- So sánh trên 7 phương pháp (không có TSB-P).

**Chất lượng cân bằng** (độ lệch chuẩn hóa trung bình của 9 đặc trưng; < 0,1 là cân bằng):

| | Gốc | VN1 → giống M5 | M5 → giống VN1 |
|---|---|---|---|
| Cửa sổ chính | 0,39 | **0,02** | 0,24 |
| Cửa sổ thứ hai | 0,32 | **0,03** | 0,15 |
| Cửa sổ thứ ba | 0,34 | **0,02** | 0,14 |

- Chiều VN1 → M5 cân bằng tốt. Cỡ mẫu hiệu dụng còn khoảng 1.700–2.000 chuỗi.
- Chiều M5 → VN1 chỉ cân bằng một phần, vì M5 gần như không có chuỗi ở vùng đuôi của VN1 (ADI cao, lâu không bán). Kết quả chiều này chỉ mang tính tham khảo.

**Kết quả:**

| | M5 gốc | VN1 → giống M5 | VN1 gốc |
|---|---|---|---|
| Tỷ lệ chuỗi mà LGB-Q chính xác hơn TSB-NB, h = 3 (ba cửa sổ) | 64 / 60 / 62% | 49 / 51 / 50% | 46 / 49 / 48% |
| Như trên, h = 13 | 59 / 58 / 57% | 35 / 41 / 45% | 31 / 39 / 41% |
| Phương pháp dẫn đầu đường đánh đổi (ba cửa sổ) | LGB-Q / LGB-Q / LGB-Q | LGB-Q / **TSB-NB** / LGB-Q | LGB-Q / **TSB-NB** / LGB-Q |
| Tồn kho của TSB-NB so với LGB-Q ở fill 0,92 (ba cửa sổ) | +10,4 / +5,5 / +6,1% | −0,9 / −5,7 / +9,6% | +5,0 / −11,3 / +25,1% |

**Kết luận:**

- Sau khi VN1 có cùng thành phần chuỗi với M5, kết luận của VN1 **vẫn không trở thành kết luận của M5**:
  - LGB-Q vẫn chỉ hơn TSB-NB trên khoảng một nửa số chuỗi;
  - TSB-NB vẫn dẫn đầu ở cửa sổ thứ hai.
- Khác biệt về thành phần chuỗi (đo bằng 9 đặc trưng) **không** giải thích được khác biệt giữa hai bộ dữ liệu.
- [Nhận định nhóm] Phần còn lại là hiệu ứng của bối cảnh, hoặc của những thứ 9 đặc trưng không đo được. Ứng viên rõ nhất là nguồn (c): mô hình ML trên M5 biết ngành hàng, cửa hàng và lịch sự kiện; trên VN1 thì không. Thử nghiệm (c) sẽ kiểm tra điều này.

### (b) Bỏ đặc trưng giá — kết quả cửa sổ thứ hai của VN1

Nguồn: `code/outputs/equal_fill_ci_w26_nop.md`.

| | Có giá | Không giá |
|---|---|---|
| Hạng đường đánh đổi: TSB-NB / LGB-Q | 1,8 / 3,8 | 1,8 / 3,2 |
| P(dẫn đầu) của TSB-NB | 0,90 | 0,93 |
| Tồn kho LGB-Q ở fill 0,94 | 1,787 | 1,774 |
| SQL trung bình LGB-Q, h = 3 | 0,539 | 0,540 |

Ở cửa sổ này, đặc trưng giá gần như không ảnh hưởng, và TSB-NB vẫn dẫn đầu. **Giá không giải thích được sự đảo chiều ở cửa sổ thứ hai.** Kết quả của hai cửa sổ còn lại, gồm cửa sổ chính (nơi Phase 2 không có giá), ở `phase2_b3_b4.md` mục 3: cũng không đổi.

## Trạng thái

- [x] B1 Đồng bộ
- [x] B2 Khác biệt hai bộ dữ liệu
- [x] B2b (a) So sánh sau khi cân bằng thành phần chuỗi
- [x] B2b (b) Thử nghiệm bỏ đặc trưng giá trên VN1 — xong cả ba cửa sổ; kết quả ở `phase2_b3_b4.md` mục 3
- [x] B2b (c) M5 chỉ dùng 21 đặc trưng chung — xong cả ba cửa sổ (kết quả ở cuối file)

## B2b (c) — M5 chỉ dùng 21 đặc trưng chung (kết quả)

Nguồn: `code/outputs/equal_fill_ci*_sf.md`, `07_paper_draft/v3_tables.md` (Table 8 c).

Bốn mô hình ML của M5 được huấn luyện lại không có 6 đặc trưng riêng (số sự kiện, số ngày SNAP, dept, cat, store, state), ở cả ba cửa sổ.

| | Cửa sổ chính | Cửa sổ thứ hai | Cửa sổ thứ ba |
|---|---|---|---|
| Tồn kho LGB-Q ở fill 0,94: 27 → 21 đặc trưng | 1,376 → 1,388 | 1,485 → 1,492 | 1,736 → 1,748 |
| TSB-NB cần nhiều hơn LGB-Q: 27 → 21 đặc trưng | +10,0% → +9,0% | +7,5% → +7,0% | +4,9% → +4,2% |
| LGB-T cần nhiều hơn LGB-Q | +5,1% → +4,8% | +6,8% → +6,6% | +3,3% → +2,7% |
| P(LGB-Q dẫn đầu), 21 đặc trưng | 1,00 | 1,00 | 1,00 |
| SQL trung bình LGB-Q, h = 3 | 0,208 → 0,210 | 0,215 → 0,217 | 0,222 → 0,223 |

**Kết luận:**

- Bỏ 6 đặc trưng riêng, tồn kho LGB-Q cần chỉ tăng dưới 1%, và mọi khoảng tin cậy của chênh lệch với TSB-NB, ETS, LGB-T, LGB-C vẫn không chứa 0.
- Lợi thế của LGB-Q trên M5 **không** đến từ việc mô hình có thêm thông tin về lịch sự kiện hay cấu trúc sản phẩm.
- Ở tần suất tuần, các đặc trưng này gần như không thêm giá trị dự báo.

## Tổng kết B2b

Cả ba nguồn khác biệt về xử lý đã được kiểm tra, và không nguồn nào giải thích được vì sao M5 và VN1 cho kết luận khác nhau:

| Nguồn | Kết quả |
|---|---|
| (a) Thành phần chuỗi | Cân bằng xong, kết luận VN1 không đổi |
| (b) Giá | Bỏ đặc trưng giá, tồn kho LGB-Q đổi dưới 1% |
| (c) Lượng thông tin của mô hình | Bỏ 6 đặc trưng riêng của M5, tồn kho LGB-Q đổi dưới 1% |

[Nhận định nhóm] Khác biệt còn lại thuộc về bản chất hai bối cảnh bán lẻ, không phải do cách chuẩn bị dữ liệu. Điểm khác rõ nhất đã đo được là mức biến động nhu cầu giữa lịch sử và giai đoạn kiểm thử (`code/outputs/demand_shift.md`).
