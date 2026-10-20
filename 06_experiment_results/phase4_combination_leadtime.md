# Giai đoạn 4 — Kết hợp dự báo (việc A) và lead time ở cùng fill rate (việc 3)

Ngày 14/10/2026. Phần diễn giải gắn nhãn [Nhận định nhóm].

Nguồn:

- `code/combination.py` → `code/outputs/combination.md`, `combination.csv`, `combination_regret.csv`;
- `code/leadtime_equal_fill.py` → `code/outputs/leadtime_equal_fill.md`, `.csv`;
- bản sao ở `06_experiment_results/tables/`.

Cả hai chỉ dùng dự báo đã có trong cache; không huấn luyện lại mô hình nào.

**Kiểm chứng:**

- Bảng regret của 7 phương pháp đơn tái lập đúng số trong bài: LGB-Q 9,4%, HGB-Q 11,4%, LGB-T 9,5%, TSB-NB 20,7%.
- Ở L = 2, kết quả lead time khớp Bảng 3: LGB-Q cần 1,38 tuần tồn kho tại fill rate 0,94 trên M5; TSB-NB cần thêm 10,0%.

## A. Kết hợp dự báo phân vị

### Thiết kế

Mỗi phân vị của tổ hợp là trung bình cộng các phân vị của các phương pháp thành viên. Hai tổ hợp được cố định trước khi xem kết quả:

- **C2** = trung bình (LGB-Q, TSB-NB): tổ hợp chính;
- **C3** = trung bình (LGB-Q, HGB-Q, TSB-NB): tổ hợp phụ.

Chính sách mặc định: h = 3, L = 2, không thanh lý. Chạy trên ba cửa sổ của cả hai dataset.

**Lưu ý về chọn lựa:** hai thành viên của C2 được chọn vì phân tích chính cho thấy chúng thắng xen kẽ trên VN1, trên **cùng** các cửa sổ này. Đây là lựa chọn hiển nhiên (mô hình ML tốt nhất + mô hình thống kê tốt nhất), nhưng vẫn là lựa chọn sau khi đã thấy dữ liệu, nên phải nói rõ trong bài.

### Kết quả

Tồn kho so với LGB-Q (%, khoảng tin cậy 95%; số âm = cần ít tồn kho hơn):

| Dataset | Cửa sổ | C2, fill 0,90 | C2, fill 0,92 | C2, fill 0,94 | TSB-NB, fill 0,94 |
|---|---|---|---|---|---|
| M5 | chính | +0,8 [+0,5; +1,1] | +0,4 [0,0; +0,7] | +0,9 [+0,5; +1,3] | +10,0 |
| M5 | thứ hai | +0,2 [−0,1; +0,5] | +0,1 [−0,2; +0,4] | −0,3 [−0,6; 0,0] | +7,5 |
| M5 | thứ ba | −1,0 [−1,5; −0,7] | −1,5 [−2,1; −1,1] | −1,1 [−1,6; −0,7] | +4,9 |
| VN1 | chính | **−5,8 [−9,7; −0,9]** | **−5,9 [−8,7; −2,2]** | **−8,1 [−10,8; −4,8]** | +10,5 |
| VN1 | thứ hai | **−9,0 [−10,9; −7,2]** | **−10,5 [−15,2; −8,0]** | **−11,2 [−13,0; −9,3]** | −8,8 |
| VN1 | thứ ba | **−5,5 [−8,8; −1,5]** | **−7,1 [−10,4; −3,0]** | −5,3 [−10,9; +4,9] | không đạt |

Regret: phần tồn kho dư so với phương pháp **đơn** tốt nhất trong mỗi lần chạy, lấy trung bình trên các mức fill 0,90–0,98 mà phương pháp đạt được. Số âm = tốt hơn mọi phương pháp đơn.

| Phương pháp | M5 chính | M5 thứ hai | M5 thứ ba | VN1 chính | VN1 thứ hai | VN1 thứ ba | **Lớn nhất** |
|---|---|---|---|---|---|---|---|
| C3 | −0,3 | −1,3 | −2,2 | −6,7 | +0,2 | −6,5 | **0,2** |
| C2 | +0,9 | −0,6 | −1,4 | −7,7 | −1,4 | −5,3 | **0,9** |
| LGB-Q | 0 | 0 | 0 | +0,7 | +9,4 | +0,2 | 9,4 |
| LGB-T | +6,0 | +7,1 | +3,8 | +0,3 | +5,8 | +9,5 | 9,5 |
| HGB-Q | +2,3 | +2,0 | +0,9 | +5,9 | +11,4 | +2,4 | 11,4 |
| TSB-NB | +11,5 | +8,4 | +6,5 | +10,4 | +3,7 | +20,7 | 20,7 |

Độ chính xác (wQL) của C2 kém LGB-Q một chút ở mọi lần chạy: ví dụ VN1 cửa sổ chính 0,108 so với 0,103.

### Kết luận

1. **Trên VN1, C2 cần ít tồn kho hơn LGB-Q ở cả ba cửa sổ** (5–11%; khoảng tin cậy không chứa 0, trừ một ô). Ở cửa sổ thứ hai, nơi TSB-NB thắng, C2 ngang TSB-NB (chênh −2,6% đến +0,9%, không có ý nghĩa).
2. **Trên M5, C2 nằm trong khoảng ±1,5% so với LGB-Q.** Thêm TSB-NB không làm hỏng kết quả.
3. **Regret lớn nhất của C2 chỉ 0,9%, so với 9,4% của LGB-Q.** Tổ hợp chính là lựa chọn ít hối tiếc nhất, tốt hơn bất kỳ phương pháp đơn nào. Kết quả này **thay thế** kết luận cũ của bài "LGB-Q is the minimax-regret choice".
4. C2 kém LGB-Q về wQL nhưng tốt hơn về tồn kho, thêm một ví dụ cho luận điểm "độ chính xác ≠ hiệu quả tồn kho".
5. So với quy tắc tăng trưởng (`phase3_q3_extensions.md` mục 2), C2 đơn giản hơn, không cần dự đoán, và ổn định ở cả ba cửa sổ. Quy tắc tăng trưởng chỉ có ý nghĩa ở một cửa sổ.
6. Kết quả khớp với Petropoulos et al. [24]: kết hợp dự báo cho kết quả tồn kho tốt nhất.
7. [Nhận định nhóm] Cách giải thích hợp lý: hai thành viên sai theo hướng khác nhau. TSB-NB phủ thiếu với chuỗi tăng mạnh; LGB-Q dư tồn kho với chuỗi ổn định. Trung bình hai bên giảm cả hai lỗi. Chưa kiểm chứng trực tiếp bằng phân tích theo nhóm chuỗi ổn định / tăng mạnh.

## 3. Độ nhạy theo lead time ở cùng fill rate

### Thiết kế

- L = 1, 2, 4 tuần (R = 1).
- Dùng dự báo đã cache của cửa sổ chính cho h = L + 1, tức h = 2, 3, 5.
- HGB-Q không có trong phân tích vì không có dự báo ở h = 2 và h = 5.

### Kết quả

Δ so với LGB-Q tại fill rate 0,94 (%; số dương = LGB-Q cần ít tồn kho hơn):

| Dataset | L | LGB-T | LGB-C | TSB-NB | ETS | C2 |
|---|---|---|---|---|---|---|
| M5 | 1 | +6,5* | +6,5* | +14,8* | +9,8* | +1,7* |
| M5 | 2 | +5,1* | +4,5* | +10,0* | +10,6* | +0,9* |
| M5 | 4 | +6,3* | +8,6* | +9,6* | +13,4* | −0,6* |
| VN1 | 1 | +0,2 | +2,5 | +16,0* | +21,0* | −4,1* |
| VN1 | 2 | +0,9 | +1,7 | +10,5* | +12,0* | −8,1* |
| VN1 | 4 | +3,7 (không có CI) | −0,5 | +4,8 (không có CI) | +7,9 | −5,4* |

\* = khoảng tin cậy 95% không chứa 0.

### Kết luận

1. **Kết luận về M5 không đổi với L = 1, 2 và 4.** LGB-Q cần ít tồn kho hơn LGB-T, LGB-C, TSB-NB và ETS ở cả ba lead time, mọi khoảng tin cậy không chứa 0. Regret lớn nhất của LGB-Q qua sáu lần chạy (2 dataset × 3 lead time) là 1,0% (không tính HGB-Q).
2. **VN1, cửa sổ chính:**
   - LGB-Q, LGB-T và LGB-C không khác nhau có ý nghĩa ở mọi lead time, giống kết quả chính.
   - Lợi thế của LGB-Q so với TSB-NB giảm khi lead time dài: +16% ở L = 1, +10,5% ở L = 2, không còn ý nghĩa ở L = 4.
3. **C2 tốt nhất trên VN1 ở cả ba lead time** (−4 đến −8% so với LGB-Q).
4. Câu Limitations trong bài ICIIT ("only the fill-rate ranking at τ = 0.9 was checked") giờ có thể thay bằng kết quả ở cùng fill rate.
5. **Giới hạn:** chỉ cửa sổ chính. Hai cửa sổ còn lại cần dự báo h = 2 và h = 5, phải huấn luyện lại.

## Đưa vào bài ICIIT (14/10/2026)

Người dùng đồng ý đưa C2 vào bản ICIIT.

**Thêm hoặc thay:**

- Abstract: câu "LightGBM quantile regression is the minimax-regret choice" → kết quả C2 (6–11% ít tồn kho hơn trên VN1 tại fill rate 0,92; ±1,5% trên M5; regret lớn nhất 0,9% so với 9,4%).
- Đóng góp 5 (mới): "A simple hedge".
- Mục 3.2: định nghĩa C2.
- Mục 5.5 (mới): kết quả C2, nói rõ cặp thành viên được chọn sau khi xem kết quả. Các mục Liquidation và Artefacts dời thành 5.6 và 5.7.
- Discussion:
  - đoạn regret đổi thành "C2 is the minimax-regret choice";
  - đoạn quy tắc tăng trưởng rút còn hai câu, chi tiết để trong repo.
- Limitations: thay câu về lead time bằng kết quả ở cùng fill rate.
- Conclusion: thêm câu về C2.

**Rút gọn để giữ 10 trang** (các nội dung này vẫn có trong repo):

- mục 5.1: bỏ các hạng trung bình ở h = 13;
- mục 5.3: bỏ câu về mức tăng 3,2 lần ở cửa sổ thứ ba;
- mục 5.4: rút phần mô tả phân cụm;
- mục 5.6: bỏ câu "factors outside this simulation";
- mục 5.7: gộp kiểm tra giá và kiểm tra đặc trưng chung;
- bỏ vài câu lặp ý ở mục 5.2 và Discussion.

Bài hiện **vừa khít 10 trang, không còn dòng trống**.

## B. Góc nhìn chi phí (14/10/2026)

Nguồn: `code/cost_view.py` → `code/outputs/cost_view.md` (bản sao ở `tables/`).

**Câu hỏi:** Theodorou et al. [7] cho thấy kết luận theo đường đánh đổi và theo chi phí có thể ngược nhau. Kết luận của nhóm có đứng vững khi tính bằng chi phí không?

### Cách tính

- Chi phí trên mỗi đơn vị nhu cầu, quy ra "tuần giữ hàng":
  - C(r) = tồn kho (tuần nhu cầu) + r × (1 − fill rate);
  - r = phạt mất doanh số / chi phí giữ hàng mỗi tuần.
- Mỗi phương pháp được chọn mức τ có chi phí thấp nhất cho mình.
- r chạy từ 10 đến 1.000. Hai mốc tham chiếu:
  - giữ hàng 20%/năm, mất 30% biên lợi nhuận → r ≈ 78;
  - bộ chi phí của [7] → r ≈ 650.

### Kết quả

Regret lớn nhất qua 6 lần chạy (%, so với phương pháp đơn rẻ nhất):

| r | 10 | 20 | 50 | 100 | 200 | 500 | 1.000 |
|---|---|---|---|---|---|---|---|
| C2 | **0,6** | **0,7** | **1,2** | **3,1** | 1,0 | 16,9 | 28,7 |
| LGB-Q | 7,3 | 5,7 | 3,8 | 8,1 | **0** | **0** | **0** |
| HGB-Q | 7,1 | 5,0 | 6,3 | 13,6 | 7,8 | 16,2 | 23,2 |
| TSB-NB | 6,9 | 7,4 | 15,4 | 26,0 | 49,3 | 108,3 | 147,2 |

Phương pháp đơn rẻ nhất: LGB-Q ở mọi lần chạy M5 và mọi r. Trên VN1, với r nhỏ, phương pháp rẻ nhất có thể là LGB-C, TSB-NB hoặc LGB-T (cửa sổ thứ hai).

### Kết luận

1. **Với r ≤ 200**, tức phần lớn tình huống bán lẻ hợp lý, C2 vẫn là lựa chọn an toàn nhất: regret lớn nhất 3,1%, trong khi LGB-Q tới 8,1%.
2. **Với r ≥ 500** (mất doanh số rất đắt, như bộ chi phí của [7]), mọi phương pháp đều chọn τ = 0,99.
   - Khi đó thắng là phương pháp đạt fill rate cao nhất ở τ = 0,99, tức LGB-Q (ví dụ VN1 cửa sổ thứ ba: 0,977 so với 0,966 của C2).
   - C2 đắt hơn tới 29%, vì phân vị 0,99 của TSB-NB phủ thiếu (độ phủ 0,953–0,969).
3. **Ngược với [7]:** khi mất doanh số đắt, phương pháp **chính xác nhất** lại tốt nhất. [Nhận định nhóm] Lý do: trong [7], các phương pháp kém chính xác có phân vị bị phình ra nên tự động giữ nhiều hàng; ở đây TSB-NB phủ thiếu ở phân vị cao, nên bị phạt.
4. **Giới hạn:** lưới τ dừng ở 0,99. Nếu cho phép phân vị cao hơn, C2 có thể bù được một phần. Cần nói rõ điều này nếu viết chi tiết trong bản tạp chí.

### Đã đưa vào bài ICIIT

- Thêm vào đoạn "C2 is the minimax-regret choice" hai câu giới hạn: (a) với r ≤ 200, C2 lệch phương pháp rẻ nhất tối đa 3,1%; (b) với phạt lớn hơn, LGB-Q tốt nhất và C2 đắt hơn tới 29%, ngược với [7].
- Để giữ 10 trang, đã bỏ:
  - câu về thứ tự LGB-Q / LGB-C / HGB-Q khi bỏ giá;
  - câu "Unmet demand is lost…";
  - rút gọn câu Spearman ở Limitations và câu về so sánh ở cùng τ.

## Trọng số học được hay trọng số bằng nhau (15/10/2026)

Nguồn: `code/combination_weights.py` → `code/outputs/combination_weights.md`.

**Cách làm:**

- Tổ hợp C_w = w × LGB-Q + (1 − w) × TSB-NB, với w = 0; 0,1; …; 1.
- Chọn w trên cửa sổ huấn luyện sao cho tồn kho cần thiết trung bình tại fill 0,90–0,94 thấp nhất.
- Áp dụng w đó cho cửa sổ kế tiếp. Ba lần chuyển cửa sổ giống quy tắc tăng trưởng.

**Kết quả** (so với C2, tức w = 0,5):

| Dataset | w học được | Tồn kho so với C2 |
|---|---|---|
| M5 | 0,7–0,8 | ít hơn 0,6–1,7% |
| VN1 | 0,3–0,6 | kém C2 ở 2 trên 3 lần chuyển (+1,1% đến +3,5%); hòa ở lần còn lại |

**Độ nhạy theo w (VN1, fill 0,92):**

- Trọng số tốt nhất thay đổi giữa các cửa sổ: 0,3 / 0,5 / 0,6–0,7.
- Mọi w trong khoảng 0,4–0,6 lệch tối đa 2,3 điểm phần trăm so với w tốt nhất của từng cửa sổ.

**Kết luận:**

- Đây là "forecast combination puzzle" (Wang et al. 2023, [26]) ở cấp quyết định tồn kho: trên VN1, nơi cần phòng hộ, ước lượng trọng số tốn nhiều hơn lợi.
- Trọng số bằng nhau là lựa chọn an toàn.
- Đã đưa vào bản nháp tạp chí: Bảng 9b, mục 6.3 và mục 2.4.

**Ba tài liệu mới (đọc toàn văn ngày 15/10/2026):**

| Tài liệu | Dùng để trích dẫn |
|---|---|
| [26] Wang, Hyndman, Li, Kang (2023), IJF 39(4) | Quantile averaging (Vincentization) cho dự báo xác suất; "forecast combination puzzle" |
| [27] Montero-Manso và cs. (2020), IJF 36(1) | FFORMA: meta-model học trọng số kết hợp từ đặc trưng chuỗi; hạng 2 ở M4 |
| [28] Challu và cs. (2023), AAAI 37(6) | N-HiTS: mạng MLP với nội suy phân cấp và lấy mẫu đầu vào đa tần |

DOI của [27] cần chép từ bản xuất bản; bản đã đọc là working paper Monash 19/18.

## Lead time trên cả ba cửa sổ (16/10/2026, theo yêu cầu của reviewer)

Nguồn: `code/leadtime_forecasts.py` tạo dự báo h = 2 và h = 5 cho cửa sổ thứ hai và thứ ba; `code/leadtime_equal_fill.py --offsets 0,26,52` chấm điểm; kết quả ở `code/outputs/leadtime_equal_fill_all_windows.md`. HGB-Q vẫn không có trong phân tích này.

**Kết quả qua 18 lần chạy** (2 dataset × 3 cửa sổ × L = 1, 2, 4):

- **M5:** ở cả 9 tổ hợp cửa sổ × lead time, LGB-Q cần ít tồn kho hơn có ý nghĩa thống kê, tại fill rate 0,94, so với:
  - LGB-T: 2,5–7,4%;
  - LGB-C: 4,5–10,9%;
  - TSB-NB: 4,9–14,8%;
  - ETS: 5,9–13,4%.

  Regret của LGB-Q không vượt 0,2%.
- **VN1:** C2 cần ít tồn kho hơn LGB-Q 3,2–10,9% tại fill rate 0,92 ở cả 9 tổ hợp; khoảng tin cậy không chứa 0 ở 7 tổ hợp.
- **Regret lớn nhất** (so với phương pháp đơn tốt nhất trong 6 phương pháp):

  | C2 | LGB-Q | LGB-T | ETS | TSB-NB |
  |---|---|---|---|---|
  | **2,0%** | 12,6% (VN1, cửa sổ thứ hai, L = 4) | 20,2% | 32,3% | 36,3% |

**Đã đưa vào bài:** `08_final_submission/ICIIT2027_Paper_rev3.docx`, gồm abstract, mục 5.5, mục 5.8 ("Lead time") và Limitations. Bài 9 trang.
