# Giai đoạn 2 — B3 (phân cụm), B4 (so với ADI–CV²) và thử nghiệm bỏ đặc trưng giá

Ngày 13/10/2026. Quy trình: `07_paper_draft/phase2_workflow.md`. Phần trước: `phase2_b1_b2.md`.

Nguồn số liệu:

- `code/outputs/segmentation.md` (script `code/segment_series.py`);
- `code/outputs/segment_eval.md` (script `code/segment_eval.py`);
- `code/outputs/equal_fill_ci*_nop.md` (thử nghiệm giá).

Mọi phân tích dùng 7 phương pháp (không có TSB-P). Phần diễn giải gắn nhãn [Nhận định nhóm].

## 0. Tóm tắt

1. **Phân cụm cho ra một phân khúc 3 nhóm, ổn định**, mang thông tin khác với ADI–CV². Tuy vậy, cấu trúc cụm yếu: dữ liệu là một dải liên tục.
2. **So với ADI–CV², phân khúc mới không phải là một cải tiến rõ ràng:**
   - giải thích khác biệt về độ chính xác giữa các phương pháp tốt hơn một phần;
   - **không** cho "phương pháp tốt nhất theo nhóm" ổn định hơn;
   - **không** tạo ra quy tắc chọn phương pháp tốt hơn việc luôn dùng LightGBM quantile.
3. **Lý do sâu hơn:** trong cùng một cửa sổ, phương pháp tốt nhất gần như giống nhau ở mọi nhóm. Thứ thay đổi là **giai đoạn**, không phải nhóm chuỗi. Vì vậy không cách chia nhóm nào dựa trên lịch sử giúp chọn phương pháp tốt hơn.
4. **Giá không giải thích được sự phụ thuộc giai đoạn trên VN1:** bỏ đặc trưng giá, kết quả gần như không đổi ở cả ba cửa sổ.

## 1. B3 — Phân cụm

### Thiết kế (định trước)

- **Đặc trưng (8):** mức bán, cỡ đơn, ADI, CV², số tuần từ lần bán gần nhất, xu hướng 26 tuần, mức 13 tuần gần nhất so với lịch sử, đỉnh bán 52 tuần. Tất cả chỉ từ lịch sử trước kiểm thử. Tỷ lệ tuần bằng 0 bị bỏ, vì nó là hàm của ADI.
- **Khớp** trên cửa sổ sớm nhất (w52), mẫu cân bằng 9.000 chuỗi mỗi dataset; áp dụng nguyên trạng cho hai cửa sổ sau.
- **Ứng viên:** K-means và Gaussian mixture với k = 3…8; HDBSCAN để kiểm tra cấu trúc.
- **Tiêu chí chọn:** độ ổn định bootstrap (ARI ≥ 0,70); mỗi cụm ≥ 3% số chuỗi ở cả hai dataset; sau đó lấy silhouette cao nhất.

### Kết quả chọn mô hình

| Mô hình | Silhouette | Ổn định (ARI) | Cụm nhỏ nhất ở M5 | Đạt tiêu chí |
|---|---|---|---|---|
| K-means k = 3 | 0,364 | 0,983 | 2,9% | Không (thiếu 0,1 điểm % ở tiêu chí cỡ cụm) |
| K-means k = 4…8 | 0,21–0,24 | 0,72–0,96 | 1,0–2,5% | Không |
| **Gaussian mixture k = 3** | 0,209 | 0,944 | 6,7% | **Có — được chọn** |
| Gaussian mixture k = 4 | 0,091 | 0,936 | 3,2% | Có |
| Gaussian mixture k = 5…8 | 0,04–0,12 | 0,65–0,90 | 0,1–2,1% | Không |

- **HDBSCAN:** tìm thấy 3 cụm, nhưng gán **43,4% số chuỗi là nhiễu**.
- Silhouette thấp (0,21) và tỷ lệ nhiễu cao cho thấy các chuỗi tạo thành một dải liên tục, không có ranh giới tự nhiên. Phân khúc là một cách **chia** dải đó, không phải phát hiện các nhóm tách biệt.
- Phần lớn ứng viên bị loại vì M5 gần như không có chuỗi ở vùng "thưa" (dưới 3%). Điều này khớp với B2: vùng nhu cầu của M5 gần như là tập con của VN1.

### Ba nhóm

| Nhóm | Mô tả | ADI | Mức 13 tuần gần nhất so với lịch sử (log) | Tuần từ lần bán cuối | M5 (3 cửa sổ) | VN1 (3 cửa sổ) |
|---|---|---|---|---|---|---|
| S1 | Bán đều, ổn định | 1,12 | −0,04 | 0 | 68–70% | 35–38% |
| S2 | Đang hụt so với lịch sử | 1,74 | −0,54 | 2 | 24–26% | 26–27% |
| S3 | Thưa, mức bán thấp | 5,44 | −0,22 | 5 | 6–7% | 36–38% |

### Quan hệ với ADI–CV² (tiêu chí C1)

- ARI giữa hai cách chia: 0,19–0,22 trên M5; 0,39–0,41 trên VN1. Hai cách chia mang thông tin khác nhau.
- Nhóm S2 "đang hụt" cắt ngang cả bốn nhóm ADI–CV². Ví dụ trên M5, 41% chuỗi intermittent và 51% chuỗi lumpy rơi vào S2.
- **Độ bền của nhãn** (tỷ lệ chuỗi giữ nguyên nhóm sau 26 tuần):

| | Phân khúc mới | ADI–CV² |
|---|---|---|
| M5 | 75–76% | 91–92% |
| VN1 | 83–84% | 87–89% |

Phân khúc mới kém bền hơn, vì nó dùng đặc trưng về trạng thái gần đây.

## 2. B4 — So với ADI–CV² theo các tiêu chí định trước

### C2. Giải thích khác biệt độ chính xác giữa LGB-Q và TSB-NB

η² = tỷ lệ phương sai được giải thích bởi cách chia nhóm (%), ba cửa sổ w52 / w26 / main.

| Thước đo | Dataset, h | ADI–CV² | Phân khúc mới | Kết hợp cả hai |
|---|---|---|---|---|
| Log tỷ số SQL | VN1, h = 3 | 10,4 / 12,4 / 14,3 | **10,8 / 15,3 / 18,2** | 13,5 / 17,2 / 19,4 |
| Log tỷ số SQL | VN1, h = 13 | 7,0 / 8,3 / 13,8 | **7,7 / 11,3 / 19,2** | 10,2 / 12,4 / 19,9 |
| Log tỷ số SQL | M5, h = 3 | 1,2 / 1,1 / 2,0 | 2,0 / 0,6 / 6,0 | 3,5 / 1,6 / 8,2 |
| Log tỷ số SQL | M5, h = 13 | 0,0 / 0,1 / 0,4 | **3,7 / 0,3 / 9,5** | 4,8 / 0,6 / 10,5 |
| Chỉ báo "LGB-Q thắng" | VN1, h = 3 | 5,3 / 5,9 / 7,6 | 3,0 / 4,9 / 8,5 | 6,2 / 7,0 / 9,7 |
| Chỉ báo "LGB-Q thắng" | VN1, h = 13 | 2,9 / 2,5 / 4,2 | 1,7 / 1,7 / 5,5 | 3,7 / 2,9 / 6,2 |

**Đánh giá: cải tiến một phần.**

- Theo log tỷ số SQL, phân khúc mới giải thích nhiều hơn ở 11 trên 12 ô.
- Theo chỉ báo thắng/thua, nó kém hơn trên VN1 ở 2 trên 3 cửa sổ.
- Trong mọi trường hợp, phần giải thích được đều nhỏ (dưới 20%).
- Kết hợp cả hai cách chia luôn tốt nhất.

### C3. Độ ổn định của phương pháp dẫn đầu theo nhóm

Số nhóm có cùng phương pháp dẫn đầu đường đánh đổi ở cả ba cửa sổ:

| | ADI–CV² | Phân khúc mới |
|---|---|---|
| M5 | 3 trên 4 | 2 trên 3 |
| VN1 | 1 trên 4 (lumpy) | 0 trên 3 |

**Đánh giá: không cải tiến.** Trên VN1, cả ba nhóm mới đều đổi phương pháp dẫn đầu giữa các cửa sổ. Riêng nhóm S3 chỉ xếp hạng được ở cửa sổ chính.

### C4. Giá trị cho quyết định

**Cách đo:** quy tắc "với mỗi nhóm, dùng phương pháp hiệu quả nhất của nhóm đó ở cửa sổ trước" được học trên cửa sổ t−1 và áp dụng cho cửa sổ t.

Bảng dưới ghi chênh lệch tồn kho so với việc luôn dùng LGB-Q, ở fill rate 0,94, kèm khoảng tin cậy 95%. Số âm = cần ít tồn kho hơn.

| Quy tắc | M5 w52→w26 | M5 w26→main | VN1 w52→w26 | VN1 w26→main |
|---|---|---|---|---|
| Luôn dùng TSB-NB | +7,5% | +10,0% | **−8,8%** [−12,6; −5,1] | +10,5% [+1,9; +20,4] |
| Phương pháp tốt nhất của cửa sổ trước | 0,0% | 0,0% | 0,0% | +10,5% [+1,9; +20,4] |
| Quy tắc theo ADI–CV² | +0,1% | 0,0% | **−5,6%** [−8,1; −3,9] | +5,1% [−0,3; +10,2] |
| Quy tắc theo phân khúc mới | +0,1% | 0,0% | −0,1% [−0,7; +0,5] | +10,5% [+1,9; +20,4] |
| Quy tắc theo ADI–CV² × phân khúc | +0,1% | 0,0% | −5,6% [−8,1; −3,8] | +4,8% [−0,1; +12,0] |
| "Tiên tri" theo phân khúc (biết trước kết quả) | 0,0% | 0,0% | −8,9% | 0,0% |

**Đánh giá: không cải tiến.**

- **M5:** không quy tắc nào hơn việc luôn dùng LGB-Q; chênh lệch ≤ 0,3%.
- **VN1:** quy tắc học từ cửa sổ trước **không đáng tin**.
  - Quy tắc theo ADI–CV² giúp ở một lần chuyển (−5,6%) và có xu hướng hại ở lần kia (+5,1%; khoảng tin cậy [−0,3; +10,2], chứa 0).
  - Quy tắc theo phân khúc mới không giúp ở lần chuyển thứ nhất và hại ở lần thứ hai (+10,5%).
- **Dòng "tiên tri" là kết quả quan trọng nhất:** ngay cả khi biết trước phương pháp tốt nhất cho từng nhóm, quy tắc theo nhóm cũng **không hơn phương pháp đơn tốt nhất của cửa sổ đó**. Nghĩa là trong một cửa sổ, cùng một phương pháp thắng ở mọi nhóm.

### Vì sao phân khúc không giúp được

[Nhận định nhóm, dựa trên các số đo dưới đây]

1. Phân tích dịch chuyển nhu cầu (`code/outputs/demand_shift.md`) đã cho thấy thứ quyết định phương pháp nào thắng là chuỗi **sẽ** tăng mạnh hay ổn định trong giai đoạn kiểm thử.
2. Tỷ lệ chuỗi "sẽ tăng mạnh" gần như **bằng nhau giữa các nhóm**:
   - trên VN1, ba nhóm S1/S2/S3 có 29% / 31% / 31% (cửa sổ w52) và 25% / 26% / 23% (cửa sổ chính);
   - các nhóm ADI–CV² cũng chỉ chênh nhau 14–39%.
   - Cách chia nhóm, cả cũ lẫn mới, không tách được chuỗi sắp tăng khỏi chuỗi sẽ ổn định.
3. Việc một chuỗi có tăng mạnh hay không chỉ **dự đoán được một phần** từ lịch sử: một mô hình có giám sát đạt AUC 0,72–0,73 trên VN1 và 0,79–0,83 trên M5.

**Hệ quả cho bài:** đóng góp không nằm ở một phân khúc mới, mà ở chính nhận định này. Trên dữ liệu thương mại điện tử, phương pháp hiệu quả nhất phụ thuộc vào biến động nhu cầu sắp tới, thứ mà phân loại theo lịch sử không nắm được.

Vì vậy lựa chọn an toàn là phương pháp có tổn thất tệ nhất nhỏ nhất:

| Phương pháp | Trường hợp tệ nhất qua ba cửa sổ |
|---|---|
| LightGBM quantile | Cần nhiều tồn kho hơn phương pháp tốt nhất khoảng 9% |
| TSB-NB | Cần nhiều hơn khoảng 10–25%, và không đạt được các mức fill rate cao |

## 3. Thử nghiệm bỏ đặc trưng giá trên VN1 (B2b, nguồn b)

Bốn mô hình ML của VN1 được huấn luyện lại không có hai đặc trưng giá, ở cả ba cửa sổ.

| | Cửa sổ chính | Cửa sổ thứ hai | Cửa sổ thứ ba |
|---|---|---|---|
| SQL trung bình LGB-Q, h = 3: có giá → không giá | 0,336 → 0,336 | 0,539 → 0,540 | 2,008 → 1,995 |
| Tồn kho LGB-Q ở fill 0,94: có giá → không giá | 3,17 → 3,18 | 1,79 → 1,77 | 3,31 → 3,32 |
| Phương pháp dẫn đầu đường đánh đổi, có giá | LGB-Q (1,4) | TSB-NB (1,8) | LGB-Q (1,25) |
| Phương pháp dẫn đầu, không giá | LGB-Q và LGB-C (2,2) | TSB-NB (1,8) | HGB-Q (1,75) |

- Độ chính xác và lượng tồn kho của LGB-Q **gần như không đổi** (dưới 1%).
- TSB-NB vẫn dẫn đầu ở cửa sổ thứ hai, dù có hay không có giá.
- Ở cửa sổ chính và cửa sổ thứ ba, nhóm mô hình ML vẫn dẫn đầu. Thứ hạng **giữa các mô hình ML** thì đổi, vì chúng chỉ chênh nhau vài phần trăm.
- **Kết luận:**
  - Giá, kể cả việc Phase 2 không có giá, **không** giải thích được sự phụ thuộc giai đoạn trên VN1.
  - Thứ hạng giữa LGB-Q, LGB-C và HGB-Q trên VN1 không đủ vững để khẳng định mô hình nào đứng đầu.

## 4. Bảng tổng kết so với kế hoạch

| Tiêu chí định trước | Kết quả |
|---|---|
| C1. Phân khúc mới mang thông tin khác ADI–CV² | Có (ARI 0,2–0,4) |
| C2. Giải thích khác biệt giữa phương pháp tốt hơn ở cả ba cửa sổ | Một phần |
| C3. Phương pháp dẫn đầu theo nhóm ổn định hơn | Không |
| C4. Quy tắc chọn phương pháp tốt hơn | Không |
| Giá giải thích sự đảo chiều trên VN1 | Không |
| Thành phần chuỗi giải thích khác biệt M5–VN1 (B2b, a) | Không |

## 5. Còn lại

- [x] B2b (c): M5 chỉ dùng 21 đặc trưng chung — xong; kết quả ở cuối `phase2_b1_b2.md`.
- [x] B5: bỏ TSB-P; Chronos-2 chỉ trên VN1 và VNF (`phase2_b5.md`).
- [x] B6: bản theo mẫu ICIIT ở `08_final_submission/ICIIT2027_paper_v3.docx`.
