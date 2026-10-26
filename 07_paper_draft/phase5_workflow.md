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

---

## Kết quả bước 2 (21/10/2026) — censoring có làm đổi thứ hạng không

Nguồn: `code/censoring_rank_check.py` → `code/outputs/censoring/censoring_rank_check.md`. Script dùng `flag_weeks()` của thành viên A; tỷ lệ tuần bị đánh dấu khớp đúng số của A.

**(a) Chỉ chuỗi không có tuần nghi hết hàng** (72–82% số chuỗi):

- phương pháp dẫn đầu ở **cả 6 cửa sổ không đổi**;
- C2 vẫn có regret lớn nhất thấp nhất (−0,2% ở α = 0,01; −0,1% ở α = 0,05).

→ **Thứ hạng giữ nguyên** theo tiêu chí đặt trước.

**(b) Bù nhu cầu** bằng mức bán trung bình trước kỳ kiểm thử, ở mọi tuần bị đánh dấu. Đây là kịch bản khắt khe nhất: coi mọi chuỗi tuần bán bằng 0 bị đánh dấu là hết hàng.

- **TSB-NB:** cần thêm 17,0–26,5% tồn kho so với LGB-Q trên M5 ở fill rate 0,92, và 28,2–40,3% ở 0,94.
  - [Nhận định nhóm] Lý do hợp lý: TSB giảm xác suất có bán trong các chuỗi tuần bán bằng 0, nên dự báo thấp đi đúng lúc nhu cầu được bù.
- **LGB-Q:** regret trên M5 ≤ 4,2%.
- **C2:**
  - trên VN1 vẫn cần ít hơn LGB-Q 6,9–10,7% ở fill rate 0,92;
  - regret lớn nhất tăng lên 9,8% (M5, cửa sổ chính), cao hơn LGB-T (8,3%).
- **Phương pháp dẫn đầu** đổi ở 3/6 cửa sổ:

  | Cửa sổ | Dẫn đầu khi bù nhu cầu | Thay cho |
  |---|---|---|
  | M5 chính | HGB-Q (hạng 2,0) | LGB-Q (hạng 2,2) |
  | M5 thứ ba | ETS | LGB-Q |
  | VN1 thứ hai | LGB-T | TSB-NB |

→ **Kết luận:** thứ hạng vững khi bỏ các chuỗi nghi hết hàng, nhưng **nhạy với giả định về nhu cầu bị ẩn**. TSB-NB chịu ảnh hưởng nhiều nhất, nên lợi thế của C2 trên M5 phụ thuộc vào tỷ lệ chuỗi tuần bán bằng 0 thực sự là hết hàng. Trên VN1, C2 vẫn hơn LGB-Q trong mọi kịch bản. Trong bài phải nói đúng như vậy.

## 7. Kết hợp cả 7 phương pháp và ablation (theo góp ý của thầy, ghi trước khi chạy — 22/10/2026)

Mục đích: xem kết hợp nhiều phương pháp có cải thiện so với LGB-Q và C2 không, và phương pháp nào thật sự đóng góp.
Dùng dự báo đã lưu (h = 3, chính sách mặc định L = 2, không thanh lý), cả M5 và VN1, ba cửa sổ. Không huấn luyện lại.

**Các kết hợp** (trung bình phân vị, mỗi phân vị là trung bình hoặc trung vị của các thành viên):
- E7 = trung bình 7 phương pháp (chính, theo góp ý của thầy); E7-med = trung vị 7 phương pháp (biến thể chống ngoại lai).
- Ablation loại từng phương pháp: E7 − m, cho 7 phương pháp m.
- Theo họ phương pháp: STAT3 (EMP, ETS, TSB-NB), GBM4 (LGB-T, LGB-C, HGB-Q, LGB-Q), DQ2 (LGB-Q, HGB-Q); C2 để đối chiếu.
- Toàn bộ 127 tập con: tập con tốt nhất trong từng lần chạy = cận trên hồi cứu (không dùng được để triển khai).
- Chọn tập con prospective: chọn tập con có regret thấp nhất trên cửa sổ trước, áp dụng nguyên cho cửa sổ sau (thứ ba → thứ hai, thứ hai → chính).

**Thước đo:** wQL; tồn kho so với LGB-Q ở fill 0,92 và 0,94 (khoảng tin cậy bootstrap 95%, 200 lần); regret so với phương pháp đơn tốt nhất (trung bình fill 0,90–0,98), lấy giá trị lớn nhất qua 6 lần chạy.

**Tiêu chí kết luận, chốt trước:**
- E7 được coi là cải thiện nếu: regret lớn nhất qua 6 lần chạy thấp hơn của LGB-Q (9,4%), VÀ trên VN1 cần ít hàng hơn LGB-Q với khoảng tin cậy không chứa 0 ở ít nhất 2/3 cửa sổ, VÀ trên M5 không kém LGB-Q quá 1% ở cửa sổ nào.
- Chọn tập con prospective được coi là hiệu quả nếu ở cả 4 lần chuyển (2 bộ × 2 lần chuyển) không kém LGB-Q, và ít nhất ở 2 lần chuyển tốt hơn với khoảng tin cậy không chứa 0.
- Báo cáo mọi kết quả, kể cả khi không đạt.

## 8. Các điểm hoàn thiện P0–P1 (ghi trước khi chạy — 23/10/2026)

Dùng dự báo h = 3 đã lưu, chính sách mặc định (L = 2, không thanh lý). Phương pháp: 7 phương pháp đơn, C2, E7-med.

**P0-1 · τ chọn trước (prospective), thay cho so sánh ex-post.** Mức order-up-to cho τ liên tục được nội suy tuyến tính giữa các phân vị đã lưu. Với mỗi phương pháp, tìm τ* (chia đôi trên [0,5; 0,99]) sao cho fill thực tế ở **cửa sổ trước** bằng mục tiêu 0,92 hoặc 0,94; áp dụng nguyên τ* cho **cửa sổ sau** (thứ ba → thứ hai, thứ hai → chính). Báo cáo fill đạt được, sai lệch so với mục tiêu và tồn kho ở cửa sổ sau. Tiêu chí: kết luận ex-post "giữ" nếu ở cửa sổ sau, phương pháp dẫn đầu ex-post có fill đạt được không thấp hơn đối thủ quá 0,005 và cần ít tồn kho hơn (thống trị hoặc gần thống trị).

**P0-2 · Bootstrap.** 1.000 lần lặp cho mỗi kiểu: (a) theo chuỗi (như bài, đối chứng); (b) cluster: M5 theo sản phẩm (3.049) và theo cửa hàng (10 cụm, ít nên chỉ để tham khảo); VN1 theo kho (328) và theo nhà bán (46); (c) block bootstrap theo tuần (khối 4 tuần, vòng tròn, trên 22 tuần đánh giá). Các so sánh kiểm tra: các khẳng định "khoảng tin cậy không chứa 0" trong bài (M5: LGB-Q so với LGB-T, LGB-C, TSB-NB, ETS ở fill 0,94; VN1 cửa sổ thứ hai: TSB-NB so với LGB-Q; VN1: E7-med và C2 so với LGB-Q ở fill 0,92). Tiêu chí: một khẳng định "giữ" nếu khoảng tin cậy vẫn không chứa 0 dưới mọi kiểu bootstrap (trừ cụm cửa hàng M5, chỉ báo cáo).

**P1-4 · Hết hàng.** α ∈ {0,001; 0,01; 0,05; 0,1} × ba cách bù cho tuần bị gắn cờ: mean (mức bán TB trước kiểm thử, như bài), half (một nửa mức đó), pos (TB các tuần có bán, kịch bản mạnh). Báo cáo: người dẫn đầu, LGB-Q so với TSB-NB trên M5, E7-med so với LGB-Q, regret lớn nhất của E7-med, C2, LGB-Q.

**P1-3 · Kiểm chứng độc lập:** không làm được với M5/VN1 (đã dùng hết dữ liệu); để cho bản tạp chí với bộ VNF. Ghi là giới hạn.

## 9. Hiệu chỉnh τ theo quá khứ (P0) và kiểm chứng độc lập trên VNF (P1) — ghi trước khi chạy, 23/10/2026

**P0 · Rolling calibration.** Trong cửa sổ đích, τ được cập nhật mỗi tuần chỉ bằng dữ liệu đã quan sát:
τ_{k+1} = clip(τ_k + η·(mục tiêu − F_k), 0,5, 0,99), với F_k = fill của toàn danh mục từ đầu cửa sổ đến hết tuần k.
- τ_0 = τ* chọn ở cửa sổ trước (M5, VN1: thứ ba → thứ hai, thứ hai → chính); η = 0,5 là cấu hình chính; η = 0,25 và 1,0 chỉ để kiểm tra độ nhạy.
- Mục tiêu fill 0,92 và 0,94. Phương pháp: 7 đơn, C2, E7-med.
- Báo cáo cùng lúc: fill đạt được trên 22 tuần đánh giá; |fill − mục tiêu|; vi phạm mục tiêu (fill cả cửa sổ < mục tiêu − 0,005; tỷ lệ tuần có fill 4 tuần gần nhất < mục tiêu); tồn kho; Δ tồn kho so với LGB-Q, kèm khoảng tin cậy bootstrap theo kho (VN1) / theo sản phẩm (M5), giữ nguyên đường đi của τ.
- Tiêu chí: hiệu chỉnh được coi là "khắc phục" nếu với LGB-Q, HGB-Q, C2 và E7-med, |fill − mục tiêu| ≤ 1 điểm ở cả hai lần chuyển của VN1. E7-med được coi là "tốt hơn prospective" trên một lần chuyển nếu fill ≥ fill của LGB-Q − 0,5 điểm và tồn kho thấp hơn với khoảng tin cậy theo kho không chứa 0.

**P1 · Kiểm chứng độc lập trên VNF** (giày dép Việt Nam, 909 chuỗi mẫu × màu, một cửa sổ 26 tuần; chưa từng dùng để thiết kế E7-med hay C2). Cấu hình giữ nguyên (trung vị/trung bình phân vị, cùng chính sách, cùng thước đo).
- (a) Tồn kho ở cùng fill thực tế 0,92 và 0,94 so với LGB-Q, bootstrap theo chuỗi và theo mẫu giày (1.000 lần).
- (b) Rolling calibration như P0, với τ_0 = mục tiêu (không có cửa sổ trước).
- Tiêu chí: E7-med được coi là "kiểm chứng được" nếu ở fill 0,92 cần ít hàng hơn LGB-Q với khoảng tin cậy không chứa 0 dưới cả hai kiểu bootstrap. Nếu không đạt: giảm mức khẳng định về kết hợp trong Abstract và Conclusion.

## 10. Kế hoạch hoàn thiện cuối (26/10/2026) — ghi trước khi chạy

Baseline đã khoá: tag `rev18-baseline` (repo nhóm 525b1dc; repo công khai 859451a). Bảng 7 của rev18 khớp 25/25 ô với rolling_calibration.csv.

**Hạng mục 2 · Full-policy cluster bootstrap (P0).** Giữ nguyên dự báo, chính sách, lead time, warm-up và quy tắc
τ_{t+1} = clip(τ_t + 0,5·(0,92 − F_t), 0,5, 0,99), τ_0 như rev18. Mỗi lần lặp lấy mẫu lại cụm (M5 sản phẩm, VN1 kho, giày dép mẫu giày)
→ trọng số chuỗi = số lần cụm được chọn; F_t tính lại trên danh mục có trọng số; **đường đi τ được cập nhật lại** và tồn kho mô phỏng lại
trong từng lần lặp. Mọi phương pháp dùng cùng một mẫu (so sánh cặp). 1.000 lần lặp chính; 2.000 lần cho LGB-Q và E7-med để kiểm tra độ ổn định.
Báo cáo: fill đạt được, tồn kho, vi phạm mục tiêu, ΔI và Δfill so với LGB-Q, khoảng 95% percentile. Số liệu điểm (mẫu gốc) phải trùng rev18.
Nếu khoảng tin cậy chứa 0: ghi "không đủ bằng chứng", không ghi "không có hiệu ứng".

**Hạng mục 4 · Đánh đổi tồn kho – dịch vụ (P0).** Phân loại mỗi phép so sánh: đạt mục tiêu (|fill − 0,92| < 0,005) hay không;
so sánh được (|Δfill| < ngưỡng) hay không, với ngưỡng 0,25 / 0,5 / 1,0 điểm. Đếm số tiết kiệm có ý nghĩa / cần nhiều hàng hơn / không kết luận
theo từng ngưỡng, dùng khoảng tin cậy từ hạng mục 2. Không gọi là tiết kiệm khi fill không tương đương.

**Hạng mục 3 · Ranking reversal (P1, sau P0).** Đơn vị: kho của VN1. Kết quả: log tỷ số tồn kho TSB-NB / LGB-Q ở fill 0,92 trong từng kho
(chỉ kho đủ chuỗi và đạt mục tiêu). Biến giải thích, chỉ từ dữ liệu trước cửa sổ: tăng trưởng 13 tuần gần nhất so với 13 tuần trước đó,
ADI, CV², tỷ lệ tuần = 0, độ dài lịch sử, quy mô. Ước lượng trên cửa sổ thứ ba, kiểm tra dự báo trên cửa sổ thứ hai và chính (tương quan hạng
giữa dự báo và kết quả). Báo cáo cả khi không tìm thấy yếu tố dự báo đáng tin.
