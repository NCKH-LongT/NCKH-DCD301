# Quy trình giai đoạn 5 — vòng review thứ 3, gộp phần của thành viên A, slide, LightGBM hai giai đoạn

Lập ngày 21/10/2026.

**Mốc cứng:** ICIIT 2027 nộp toàn văn **30/10/2026**; NCKH vòng loại 31/10–01/11.

**Bản bài hiện tại:** `08_final_submission/ICIIT2027_Paper_rev6.docx`, đúng **10 trang**. Đây là mức tối đa trong phí đăng ký; mỗi trang thêm 30 USD.

## 0. Hiện trạng các đầu việc

| Đầu việc | Đã có | Còn thiếu |
|---|---|---|
| R1. Nhấn mạnh C2 là thăm dò, post hoc | Mục 5.5, Discussion và Conclusion đã ghi "post hoc", "needs independent evaluation" | Rà mọi chỗ **tóm tắt** C2 (abstract, câu đầu các đoạn, chú thích bảng) để chỗ nào cũng kèm điều kiện |
| R2. Censoring | Đoạn "Censored demand" (rev6). Thành viên A: `code/censoring_check.py` ước lượng tuần nghi hết hàng: M5 7,4–9,0%, VN1 6,1–6,9% số tuần kiểm thử; nhu cầu ẩn M5 khoảng 7–8%, VN1 khoảng 2–3%; tập trung ở intermittent/lumpy | **Kiểm tra thứ hạng LGB-Q / TSB-NB / C2 có đổi không** (cần cache dự báo, máy Duy) |
| R3. Chi phí tính toán so với hiệu quả (Chronos, N-HiTS) | Thành viên A: `06_experiment_results/phase4_compute_cost.md`, có đoạn văn đề xuất | Đưa vào bài (rút gọn); kiểm lại số |
| R4. Hướng dẫn dùng s* | Công thức s* ở mục 3.4 (rev6) | Thêm quy tắc ra quyết định và ví dụ bằng số cho nhà quản lý |
| Slide trình bày | `Từ dự báo đến quyết định.html` (16 slide) | Bổ sung các phần mà bản mẫu của mentor có (mục 4) |
| LightGBM hai giai đoạn | — | Cần PDF bài báo; đánh giá rồi quyết định (mục 5) |

## 1. Gộp phần việc của thành viên A (ngày 21/10)

Nhánh `giahuy/censoring-check` tách ra từ bản rev4 (`2ef8207`), cũ hơn nhánh chính 4 commit (rev5, rev6, Proposal, infographic).

1. Lấy từng commit sang nhánh chính bằng cherry-pick:
   - `4c57ed8` censoring check;
   - `a73001f` code/README và thư mục kết quả;
   - `a155e8f` chi phí tính toán.
2. Giải quyết xung đột nếu có (dễ xảy ra ở `code/README.md`).
3. Chạy lại `code/censoring_check.py` trên máy Duy. Mục đích: xác nhận số liệu và fingerprint 6 lần chạy khớp.
4. Commit, không push cho đến khi xong mục 2.

## 2. R2 — Censoring có làm đổi thứ hạng không (21–23/10, máy Duy)

Dùng `flag_weeks()` của A (ngưỡng α = 0,01; thêm 0,05 để kiểm tra độ nhạy).

| Cách | Làm gì | Trả lời câu hỏi |
|---|---|---|
| **(a) Bỏ chuỗi nghi hết hàng** | Chấm lại tồn kho ở cùng fill rate **chỉ trên chuỗi không có tuần bị đánh dấu** trong kỳ kiểm thử. Giữ nguyên dự báo đã cache | Thứ hạng trên tập "sạch" có giống tập đầy đủ không |
| **(b) Bù nhu cầu khi đánh giá** | Ở tuần bị đánh dấu trong kỳ kiểm thử, thay nhu cầu bằng mức bán trung bình của chuỗi trước kỳ kiểm thử, rồi mô phỏng lại. Dự báo giữ nguyên | Nếu nhu cầu thật cao hơn doanh số, phương pháp nào bị ảnh hưởng nhiều hơn |
| **(c) Bù cả khi huấn luyện** (chỉ làm nếu còn thời gian) | Bù tuần bị đánh dấu trong lịch sử, huấn luyện lại LGB-Q và TSB-NB, chỉ cửa sổ chính | Mô hình học trên dữ liệu bị cắt có thiên lệch không |

- **Đầu ra:** bảng Δ tồn kho so với LGB-Q (TSB-NB, LGB-T, C2) tại fill 0,92 / 0,94 cho (a) và (b), đủ 2 dataset × 3 cửa sổ; regret lớn nhất.
- **Tiêu chí kết luận** (đặt trước khi chạy):
  - Thứ hạng "giữ nguyên" nếu phương pháp dẫn đầu từng cửa sổ không đổi và C2 vẫn có regret lớn nhất thấp nhất.
  - Nếu đổi, báo cáo đúng như kết quả.
- **Viết vào bài:** 2–3 câu trong đoạn "Censored demand", nêu tỷ lệ tuần nghi hết hàng và kết quả (a)/(b). Nhấn mạnh đây là **cận trên** từ một bộ phát hiện chỉ dùng doanh số.

## 3. R1, R3, R4 — sửa bài (23–25/10), xuất rev7

| Việc | Nội dung | Chỗ sửa |
|---|---|---|
| R1 | Mỗi câu tóm tắt C2 đều kèm "post hoc" hoặc "exploratory"; chú thích bảng nào có C2 cũng ghi "post hoc, not independently validated" | Abstract, mục 1 (đóng góp 5), 5.5, 5.8, 6, 7 |
| R3 | Đoạn "Computational cost" rút từ bản của A còn 4–5 câu. Số liệu: LGB-Q 10–21 phút/cửa sổ trên M5; N-HiTS khoảng 7 phút; Chronos-2 5,4 giờ trên M5 với +14,7% tồn kho. Đối chiếu từng số với log trước khi đưa vào | Discussion, sau đoạn N-HiTS |
| R4 | Quy tắc: **thanh lý khi tỷ lệ thu hồi kỳ vọng r ≥ s\***. Ví dụ VN1, quy tắc phân vị: s\* = 0,91–1,21 → nếu kênh thứ cấp chỉ thu hồi 60% giá vốn thì không nên thanh lý trong 26 tuần. Nêu ba yếu tố làm s\* thấp hơn: lỗi thời, chi phí kho cao, horizon dài hơn. Có thể thêm 1 bảng nhỏ "r so với s\* → quyết định" | 3.4 hoặc 5.6, cạnh Bảng 6 |

**Ngân sách trang:** bài đã 10 trang. Thêm R2 + R3 + R4 khoảng 15–20 dòng. Hai cách:
- **(i)** rút các đoạn dài ở mục 5.4 và 5.7, giữ 10 trang;
- **(ii)** chấp nhận 11 trang, thêm 30 USD.

Cần nhóm quyết định trước ngày 23/10.

**Kiểm tra cuối rev7:**
- mọi con số đối chiếu với file kết quả;
- đếm trang bằng Word;
- cập nhật repo công khai (censoring, compute cost);
- commit rồi push.

## 4. Slide trình bày — theo khung bản mẫu của mentor (24–28/10)

Khung bản mẫu: **00 Mở đầu → 01 Khám phá dữ liệu → 02 Tiền xử lý & đặc trưng → 03 Distribution shift → 04 Mô hình & đánh giá → 05 Insight & kết luận**. Mỗi slide có dòng **"NGUỒN"** trỏ tới notebook hoặc file kết quả.

| Phần trong bản mẫu | Bản của nhóm | Cần thêm | Nguồn có sẵn |
|---|---|---|---|
| 00 Bối cảnh | Có (slide 1–3) | Đánh số chương; một slide "bối cảnh vận hành" (một tuần của người lập kế hoạch) | — |
| 1.1 Tải dữ liệu, kiểm tra cấu trúc (kích thước, giá trị thiếu, 5 dòng đầu) | **Thiếu** | Bảng kích thước, tuần thiếu, giá trị âm, ví dụ vài dòng của panel tuần | `sync_check.md`, `data_profile` |
| 1.2 Đặc điểm nhãn → chọn metric | **Thiếu** | Vì sao không dùng mean SQL (0,336 → 2,008 trên VN1) mà dùng wQL và so sánh ở cùng fill rate | Mục 3.4 và 5.1 của bài |
| 1.3 So sánh phân phối hai tập | Có một phần (slide 6) | Bảng KS theo đặc trưng | `dataset_shift.md` |
| 1.4 Ma trận tương quan | **Thiếu** | Hình tương quan | `code/outputs/eda/eda_6_correlation.png` (của A) |
| 2.1 Đặc trưng mới, có công thức | **Thiếu** | Danh sách đặc trưng: lag, rolling, since-sale, scale, giá, lịch; công thức mục tiêu D_h | `f2d/features.py`, mục 3.2 |
| 2.2 Chống rò rỉ dữ liệu (fit trên train, transform test) | Có một câu (slide 7) | Sơ đồ: dự báo tại tuần o chỉ dùng dữ liệu trước o; refit mỗi 13 tuần; phân cụm khớp trên cửa sổ sớm nhất | `models.py` |
| 3.1 Định lượng shift (PSI, KS) | **Thiếu** | Bảng KS + AUC 0,91 | `dataset_shift.md` |
| 3.2 Drift classifier | **Thiếu** | AUC 0,865 / 0,913 / 0,994 theo bộ đặc trưng | `phase2_b1_b2.md` |
| 3.3 Xử lý shift (cân lại mẫu) | **Thiếu** | Cân lại VN1 cho giống M5: SMD 0,32–0,39 → 0,02–0,03, kết luận không đổi | `matched_comparison.md` |
| 4.1 Huấn luyện + bảng siêu tham số | **Thiếu** | Bảng 4 cấu hình LightGBM và kết quả độ nhạy | `hparam_sensitivity.md` |
| 4.3 Bảng kết quả | Có (slide 10–12) | Bảng đủ phương pháp × cửa sổ | Bảng 2–3 của bài |
| 4.4 Đường cong | Có một phần | Hình đường đánh đổi tồn kho–fill rate | `fig1_tradeoff.png` |
| 5.1 Insight vận hành | Có (slide 16) | Thêm khuyến nghị theo tình huống: C2 hay LGB-Q tùy mức phạt mất khách; quy tắc dùng s\* | Mục 6 của bài |
| — | — | **Thêm mới:** slide censoring (R2), slide chi phí tính toán (R3) | Kết quả mục 2, 3 |

**Thứ tự làm:**
1. Dựng khung chương và dòng "NGUỒN" cho từng slide cũ.
2. Thêm 7–8 slide còn thiếu.
3. Chèn hình EDA của A.
4. Kiểm tra số liệu.

Lưu thành file mới, không ghi đè bản của nhóm.

## 5. LightGBM hai giai đoạn (bài ScienceDirect pii S2090447926004764)

**Chưa đọc được:** ScienceDirect chặn truy cập tự động, cần nhóm gửi PDF.

**Đánh giá sơ bộ, chờ đọc bài:** "LightGBM hai giai đoạn" thường có hai dạng.

| Dạng | Ý tưởng | Áp dụng cho bài này |
|---|---|---|
| **Hurdle / two-part** | Giai đoạn 1: phân loại có bán hay không. Giai đoạn 2: hồi quy lượng bán khi có bán | Rất hợp với nhu cầu gián đoạn: tương đương TSB-NB nhưng dùng ML và biến giá, lịch. Khó ở chỗ phải ghép thành **phân vị của tổng h tuần** (cần mô phỏng hoặc hỗn hợp phân phối) |
| **Dự báo điểm rồi hiệu chỉnh sai số** | Giai đoạn 1: dự báo điểm. Giai đoạn 2: mô hình hóa sai số hoặc phân vị | Gần LGB-T / LGB-C đã có; bài đã cho thấy cách này kém LGB-Q 3,3–8,2% |

**Đề xuất:**
- **Không** đưa vào bản ICIIT (còn 9 ngày, bài đã 10 trang, thêm phương pháp mới phải chạy lại toàn bộ đánh giá).
- Nếu là dạng hurdle, làm cho **bản tạp chí**: thêm phương pháp "LGB-H" và chạy đúng giao thức (3 cửa sổ, cùng fill rate).

## 6. Lịch và phân công

| Ngày | Việc | Người |
|---|---|---|
| 21/10 | Mục 1: gộp phần của A | Duy (AI hỗ trợ) |
| 21–23/10 | Mục 2: censoring (a), (b); (c) nếu kịp | Duy (cần cache) |
| 22/10 | Gửi PDF bài LightGBM hai giai đoạn | Nhóm |
| 23/10 | Quyết định 10 hay 11 trang | Nhóm và mentor |
| 23–25/10 | Mục 3: R1, R3, R4 → rev7 | Duy, A |
| 24–28/10 | Mục 4: slide | A, Duy |
| 26–28/10 | Mentor đọc rev7 và slide | Mentor |
| 29/10 | Sửa theo mentor; kiểm tra cuối (số liệu, trang, Turnitin, khai báo AI) | Nhóm |
| 30/10 | **Nộp ICIIT** | Duy |
| 31/10–01/11 | Vòng loại NCKH | Nhóm |
| Sau 30/10 | Mục 5 (LGB hai giai đoạn) cho bản tạp chí | Nhóm |
