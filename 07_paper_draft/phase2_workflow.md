# Quy trình giai đoạn 2 — đồng bộ dữ liệu, phân khúc không giám sát, tinh gọn phương pháp

Phiên bản 13/10/2026. File làm việc; cập nhật trạng thái sau mỗi bước.

## 0. Mục tiêu và các quyết định đã chốt

| # | Yêu cầu | Cách hiểu để thực hiện |
|---|---|---|
| Y1 | Hai bộ dữ liệu phải đồng bộ | Kiểm tra M5 và VN1 dùng cùng định nghĩa: tuần, điểm bắt đầu chuỗi, đặc trưng, điều kiện chọn chuỗi, cách chia tập. Ghi lại mọi chỗ khác nhau. |
| Y2 | Phân tích sự khác nhau của hai bộ dữ liệu | So sánh phân phối đặc trưng của chuỗi và lượng hóa mức khác biệt. |
| Y3 | Dùng học không giám sát để ra "bộ dữ liệu mới" | Phân cụm chuỗi trên đặc trưng **chỉ tính từ lịch sử trước giai đoạn kiểm thử**. Kết quả là một **phân khúc chuỗi mới**, dùng chung cho M5 và VN1. |
| Y4 | So sánh ngược lại với hiện tại, chỉ ra cải tiến | So phân khúc mới với phân loại ADI–CV² hiện tại theo các tiêu chí định trước (mục 4). |
| Y5 | Bỏ TSB-P | Còn 7 phương pháp. Tính lại mọi hạng, bảng và hình. |
| Y6 | Chronos-2 chỉ ở phụ lục, cho VN1 và VNF | Bỏ kết quả M5 của Chronos-2 khỏi bài; chuyển mục 5.8 xuống phụ lục. |

**Ghi chú về Y6 (cần biết trước khi viết):**

- Báo cáo kỹ thuật Chronos-2 liệt kê 23 bộ dữ liệu thực dùng để huấn luyện (Bảng 6), **không có M5**; M5 chỉ là bài đánh giá (Bảng 11).
- Tuy vậy, báo cáo cũng nói mô hình dùng "một số" bộ từ các kho dữ liệu huấn luyện lớn hơn, nên người ngoài không tự kiểm chứng được hoàn toàn.
- Cách viết an toàn: **không** khẳng định M5 có trong dữ liệu huấn luyện, **không** khẳng định là không. Chỉ viết: "để tránh mọi nghi vấn về rò rỉ dữ liệu, Chronos-2 chỉ được báo cáo trên VN1 và VNF".
- Bản `final_paper_revA.docx` đang viết "M5 là zero-shot". Câu này sẽ được thay khi làm bước 6.

**Ghi chú về Y5:**

- TSB-P là phương pháp có SQL **trung vị** tốt nhất trên nhóm intermittent của VN1 ở cả ba cửa sổ (`code/outputs/robust_accuracy.md`).
- Bỏ TSB-P thì nhận định "phương pháp thống kê đơn giản chính xác hơn trên chuỗi rời rạc điển hình" sẽ dựa hoàn toàn vào TSB-NB.
- Việc này cần được kiểm tra lại ở bước 5.

## 1. Mốc thời gian phải khớp

**Cuộc thi NCKH FA26 (FPTU HCM)** — nguồn: `THÔNG TIN CUỘC THI NCKH FA26.pdf`

| Mốc | Nội dung |
|---|---|
| 01/10 – **20/10/2026** | Đăng ký và nộp Proposal |
| 31/10 – 01/11/2026 | Vòng loại |
| 28/11 – **07/12/2026** | Nộp toàn văn |
| Dự kiến 20/12/2026 | Chung kết (trình bày 10 phút + phản biện 20 phút, bằng tiếng Anh) |

Yêu cầu bài dự thi:

- mẫu IEEE dạng Word, **một cột, tối đa 10 trang A4** (không tính tài liệu tham khảo và phụ lục);
- Turnitin ≤ 25%;
- đề tài chưa từng công bố ở tạp chí hoặc hội nghị.

**Hội nghị ICIIT 2027** — nguồn: iciit.org, xem ngày 13/10/2026

| Mốc | Nội dung |
|---|---|
| **30/10/2026** | Hạn nộp toàn văn |
| 05/11/2026 | Hạn nộp tóm tắt (chỉ trình bày, không đăng bài) |
| 20/11/2026 | Thông báo kết quả |
| 10/12/2026 | Hạn đăng ký |
| 04–07/03/2027 | Hội nghị, TP.HCM |

**Cần hỏi giảng viên hướng dẫn hoặc ban tổ chức:** thể lệ cuộc thi không nhận đề tài "đã được công bố trên các tạp chí, hội nghị trước đây". Nếu nộp ICIIT trước chung kết, cần xác nhận điều này không vi phạm thể lệ.

**Hệ quả cho bài:** bản hiện tại dài khoảng 13.700 từ. Phải rút xuống 10 trang, nên bước 5–6 dưới đây cũng là dịp cắt gọn.

## 2. Tổng quan quy trình

```text
B0 Dọn dẹp ─► B1 Đồng bộ ─► B2 Khác biệt ─► B3 Phân cụm ─► B4 So sánh với hiện tại
                                                                    │
                    B6 Viết lại bài ◄─ B5 Bỏ TSB-P, Chronos-2 xuống phụ lục
```

Mỗi bước có **đầu ra** và **điều kiện qua cổng**. Không qua cổng thì không làm bước sau.

## 3. Các bước

### B0 — Dọn dẹp việc dở (0,5 ngày)

| Việc | Đầu ra |
|---|---|
| Commit các phân tích nhóm B đã xong | `robust_accuracy.py`, `demand_shift_analysis.py`, `frontier_sensitivity.py` và kết quả |
| Chạy lại thử nghiệm bỏ đặc trưng giá trên VN1, 3 cửa sổ (đã bị dừng giữa chừng) | `sh code/outputs/logs/rerun_nop.sh` → `outputs/VN1*_nop/` |
| Ghi kết quả nhóm B vào `06_experiment_results/results.md` | Mục mới về độ vững |

**Cổng:** thử nghiệm giá chạy xong cả ba cửa sổ. Kết luận ghi rõ một trong hai: "giá giải thích sự đảo chiều" hoặc "giá không giải thích".

### B1 — Kiểm tra đồng bộ hai bộ dữ liệu (0,5 ngày)

Script mới `code/sync_check.py` → `outputs/sync_check.md`. Mỗi dòng: tiêu chí, M5, VN1, khớp hay lệch, cách xử lý.

| Tiêu chí | Điều cần kiểm tra | Đã biết |
|---|---|---|
| Tần suất, ngày đầu tuần | Cả hai là tuần đủ 7 ngày | M5: tuần Walmart bắt đầu thứ Bảy; VN1: thứ Hai. Lệch nhưng không ảnh hưởng, vì hai bộ không ghép theo thời gian |
| Điểm bắt đầu chuỗi | Cùng định nghĩa | **Lệch:** M5 = tuần đầu có giá (lên kệ); VN1 = tuần bán đầu tiên. Ảnh hưởng tới ADI và tỷ lệ tuần bằng 0 |
| Giá trị thiếu, âm | Không có NaN sau điểm bắt đầu; không âm | Cần xác nhận lại bằng số |
| Đặc trưng | Cùng công thức, cùng tên | 19 đặc trưng chung; M5 thêm sự kiện, SNAP, thuộc tính |
| Giá | Cùng cách xử lý | VN1: chỉ có ở tuần có bán, Phase 2 không có giá |
| Điều kiện chọn chuỗi | Giống nhau | Giống (≥ 13 tuần trước kiểm thử, có bán) |
| Chia tập, mốc huấn luyện lại | Giống nhau | Giống |
| Đơn vị | Đơn vị bán | M5: sản phẩm × cửa hàng; VN1: sản phẩm × kho × nhà bán. Khác cấp gộp |

**Việc phải quyết ở bước này:** có chạy thêm phiên bản M5 với điểm bắt đầu = tuần bán đầu tiên (giống VN1) hay không. Phiên bản này đo xem khác biệt giữa hai dataset có phải do định nghĩa hay không.

**Cổng:** mọi dòng "lệch" đều có quyết định xử lý, hoặc chấp nhận kèm lý do.

### B2 — Phân tích khác biệt giữa hai bộ dữ liệu (1 ngày)

Script mới `code/dataset_shift.py` → `outputs/dataset_shift.md` và hình.

1. **Bảng đặc trưng theo chuỗi** — một dòng mỗi chuỗi, mỗi cửa sổ, **chỉ từ lịch sử trước kiểm thử**:
   - mức bán trung bình (log); ADI; CV²; tỷ lệ tuần bằng 0; số tuần từ lần bán gần nhất;
   - độ dài lịch sử;
   - xu hướng 26 tuần gần nhất so với 26 tuần trước đó;
   - độ mạnh mùa vụ (tự tương quan trễ 52, nếu đủ dữ liệu);
   - độ biến động giá;
   - tỷ trọng tuần lớn nhất (dấu hiệu đơn hàng sỉ).
2. **So sánh từng đặc trưng:** trung vị, tứ phân vị, khoảng cách Kolmogorov–Smirnov, chỉ số PSI.
3. **Mức tách biệt tổng thể:**
   - huấn luyện một bộ phân loại "chuỗi này thuộc M5 hay VN1" trên các đặc trưng chung;
   - AUC gần 0,5 = hai bộ giống nhau; gần 1 = khác hẳn;
   - độ quan trọng đặc trưng cho biết khác ở đâu.
4. **Hình:** PCA 2 chiều, tô màu theo dataset.

**Cổng:** bảng xếp hạng đặc trưng theo mức khác biệt, và một đoạn kết luận "hai bộ khác nhau chủ yếu ở …".

### B3 — Phân cụm không giám sát (1,5 ngày)

Script mới `code/segment_series.py` → `outputs/segments_<D>[_wN].csv`, `outputs/segmentation.md`.

**Nguyên tắc bắt buộc:**

- Đặc trưng **chỉ từ lịch sử trước kiểm thử**. Không dùng nhu cầu của giai đoạn kiểm thử.
- **Một** mô hình phân cụm, khớp trên M5 + VN1 gộp lại, để cụm có cùng ý nghĩa ở hai dataset.
- Chuẩn hóa trước khi phân cụm: biến lệch lấy log, rồi chuẩn hóa theo trung vị và khoảng tứ phân vị.
- Lấy mẫu cân bằng hai dataset khi khớp, để M5 (nhiều chuỗi gấp đôi) không lấn át.
- Mô hình khớp trên cửa sổ sớm nhất, rồi **áp dụng nguyên trạng** cho hai cửa sổ còn lại. Cách này kiểm tra được độ ổn định.

**Thuật toán** (chạy cả ba, chọn theo tiêu chí định trước):

| Thuật toán | Vai trò |
|---|---|
| K-means, k = 3…8 | Mốc đơn giản, dễ giải thích |
| Gaussian mixture, k = 3…8 | Cho cụm hình elip; chọn k theo BIC |
| HDBSCAN | Không cần chọn k; tách được nhóm "bất thường" (chuỗi bùng nổ, đơn sỉ) |

**Tiêu chí chọn** (định trước, không nhìn kết quả tồn kho):

- hệ số silhouette;
- BIC (với GMM);
- độ ổn định: chỉ số Rand hiệu chỉnh (ARI) giữa các lần khớp trên mẫu bootstrap ≥ 0,7;
- mỗi cụm ≥ 3% số chuỗi ở cả hai dataset;
- cụm mô tả được bằng lời.

**Đầu ra — "bộ dữ liệu mới":**

- bảng chuỗi kèm nhãn cụm;
- bảng mô tả từng cụm: tâm cụm, tỷ trọng ở M5 và VN1, tên gọi.

**Cổng:** chọn được một cách phân cụm đạt mọi tiêu chí trên. Nếu không có cách nào đạt độ ổn định, dừng lại và báo cáo: kết quả âm tính cũng là kết quả.

### B4 — So sánh phân khúc mới với ADI–CV² hiện tại (1,5 ngày)

Script mới `code/segment_eval.py` → `outputs/segment_eval.md`. Bốn tiêu chí, định trước:

| Tiêu chí | Cách đo | Thế nào là "cải tiến" |
|---|---|---|
| C1. Mức trùng với ADI–CV² | Bảng chéo, ARI | Chỉ mô tả. ARI thấp = phân khúc mới mang thông tin khác |
| C2. Giải thích khác biệt giữa phương pháp | Tỷ lệ phương sai của chênh lệch SQL theo chuỗi (LightGBM quantile − TSB-NB) được giải thích bởi phân khúc (η²) | η² của phân khúc mới cao hơn ADI–CV² ở **cả ba** cửa sổ |
| C3. Độ ổn định của "phương pháp tốt nhất theo nhóm" | Số nhóm có cùng phương pháp dẫn đầu (theo đường đánh đổi) ở cả ba cửa sổ | Nhiều nhóm ổn định hơn ADI–CV² (hiện tại: lumpy ổn định; smooth và erratic không) |
| C4. Giá trị cho quyết định | Quy tắc "chọn phương pháp theo nhóm": học trên cửa sổ sớm, áp dụng cho cửa sổ sau; đo tồn kho ở cùng fill rate | Cần ít tồn kho hơn (a) một phương pháp duy nhất tốt nhất và (b) quy tắc tương tự dựa trên ADI–CV², với khoảng tin cậy bootstrap không chứa 0 |

Bối cảnh cho C4: phân tích dịch chuyển nhu cầu (`outputs/demand_shift.md`) đã cho thấy:

- trên chuỗi VN1 ổn định, TSB-NB cần ít tồn kho hơn LightGBM quantile 13–16% ở cả ba cửa sổ;
- trên chuỗi tăng mạnh, chỉ LightGBM quantile phục vụ được.

Phân tích đó chia nhóm **sau khi biết kết quả**. Câu hỏi của B4 là: phân khúc **biết trước** (từ lịch sử) có bắt được khác biệt này không.

**Cổng:** ghi rõ kết quả từng tiêu chí là "cải tiến", "ngang" hay "kém hơn". Không chọn lọc tiêu chí có lợi.

### B5 — Tinh gọn phương pháp (1 ngày)

| Việc | Chi tiết |
|---|---|
| Bỏ TSB-P | Sửa `MODELS` trong các script phân tích còn 7 phương pháp. Chạy lại `stat_tests.py`, `analyze_results.py`, `equal_fill_ci.py`, `robust_accuracy.py`, `frontier_sensitivity.py` cho 3 cửa sổ. Dự báo đã cache nên không phải dự báo lại; mỗi script vài phút |
| Kiểm tra hệ quả | Các kết luận trong Table 8 của bài có đổi không khi hạng tính trên 7 phương pháp thay vì 8 |
| Chronos-2 | Bỏ kết quả M5; giữ VN1 (3 cửa sổ) và VNF; chuyển thành phụ lục |

**Cổng:** bảng "trước và sau khi bỏ TSB-P" cho mọi kết luận chính.

### B6 — Viết lại bài theo mẫu 10 trang (3–4 ngày)

1. Chốt 3 thông điệp chính, lấy từ kết quả B0–B5.
2. Chuyển sang mẫu IEEE một cột; văn xuôi thay cho gạch đầu dòng.
3. Thân bài còn 6–7 bảng và 2–3 hình. Phần còn lại xuống phụ lục: Chronos-2, VNF, lưới kịch bản, bảng theo nhóm chi tiết.
4. Đổi thước đo độ chính xác chính sang wQL + hạng theo chuỗi. Lý do: SQL trung bình không ổn định; wQL ổn định qua ba cửa sổ.
5. Thay câu "nguyên nhân đảo chiều chưa xác định" bằng kết quả của B0 và B4.
6. Kiểm tra Turnitin.

## 4. Rủi ro và cách xử lý

| Rủi ro | Xử lý |
|---|---|
| Phân cụm không ổn định hoặc không hơn ADI–CV² | Báo cáo trung thực là kết quả âm tính; giữ ADI–CV². Khi đó đóng góp của bài vẫn là benchmark + phân tích dịch chuyển nhu cầu |
| Rò rỉ thông tin tương lai vào đặc trưng phân cụm | Mọi đặc trưng tính với mốc cắt = tuần đầu kiểm thử; có kiểm thử tự động trong script |
| Thêm phân khúc mới làm bài dài hơn trong khi phải cắt còn 10 trang | Phân khúc mới thay cho một phần phân tích ADI–CV² trong thân bài, không cộng thêm |
| Tiến trình chạy lâu bị dừng khi máy ngủ | Chạy dạng tiến trình độc lập; bật chế độ không ngủ khi cắm điện |
| Hạn ICIIT 30/10 quá gần | Quyết định sớm: nhắm ICIIT hay chỉ cuộc thi. Nếu nhắm ICIIT, B3–B4 phải xong trước 22/10 |

## 5. Lịch đề xuất

| Ngày | Việc |
|---|---|
| 13–14/10 | B0, B1 |
| 15/10 | B2 |
| 16–17/10 | B3 |
| 18–19/10 | B4; nộp Proposal cuộc thi trước 20/10 |
| 20/10 | B5 |
| 21–27/10 | B6 |
| 28–29/10 | Rà soát, Turnitin; nộp ICIIT (nếu quyết định nộp) |

## 6. Trạng thái

- [x] B0 Dọn dẹp, chạy lại thử nghiệm giá — xong cả ba cửa sổ
- [x] B1 Đồng bộ (06_experiment_results/phase2_b1_b2.md)
- [x] B2 Khác biệt hai bộ dữ liệu (06_experiment_results/phase2_b1_b2.md)
- [x] B2b Khả năng so sánh: (a) cân bằng thành phần; (b) bỏ đặc trưng giá VN1; (c) M5 chỉ dùng đặc trưng chung — cả ba đều không giải thích được khác biệt M5–VN1
- [x] B3 Phân cụm — GMM k = 3 (06_experiment_results/phase2_b3_b4.md)
- [x] B4 So sánh với ADI–CV² — kết quả phần lớn âm tính: C1 có, C2 một phần, C3 không, C4 không
- [x] B5 Bỏ TSB-P — kết luận gần như không đổi; tương quan hạng M5–VN1 yếu đi (06_experiment_results/phase2_b5.md). Chronos-2 trên VN1 và VNF: đã tính lại với 7 phương pháp
- [ ] B6 Viết lại bài — đã có `v3_draft.md` và bản theo mẫu ICIIT `08_final_submission/ICIIT2027_paper_v3.docx` (10 trang, dựng bằng `code/build_iciit_docx.py`); còn: tên tác giả, đơn vị, link kho mã, biểu mẫu Authors' Information, Turnitin
