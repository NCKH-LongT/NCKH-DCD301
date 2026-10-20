# Outline v3 — 10-page version (seven methods)

Ngày 13/10/2026. File này thay cho `paper_outline.md` (bản 8 phương pháp, viết cho tạp chí).

- Bảng số liệu: `v3_tables.md`, sinh bởi `code/paper_tables_v3.py`. Không gõ lại số bằng tay.
- Căn cứ: `06_experiment_results/phase2_b1_b2.md`, `phase2_b3_b4.md`, `phase2_b5.md`.

## 0. Quyết định đã chốt

| Mục | Quyết định |
|---|---|
| Phương pháp | 7: EMP, TSB-NB, ETS, LGB-T, LGB-C, HGB-Q, LGB-Q. TSB-P bị bỏ |
| Chronos-2 | Chỉ ở phụ lục, trên VN1 và VNF |
| VNF (giày dép Việt Nam) | Phụ lục; trong thân bài chỉ một câu |
| Thước đo độ chính xác chính | wQL và hạng theo chuỗi. SQL trung bình chỉ nêu để giải thích vì sao không dùng |
| Độ dài | Tối đa 10 trang A4 một cột, không tính tài liệu tham khảo và phụ lục |
| Mẫu | **Chưa chốt** (IEEE Word của cuộc thi hay ACM của ICIIT). Nội dung viết không phụ thuộc mẫu |

## 1. Ba thông điệp

1. **Phải so sánh ở cùng mức phục vụ và qua nhiều giai đoạn.**
   - Ở cùng τ, các phương pháp đạt fill rate khác nhau.
   - Ở cùng fill rate, kết luận trên M5 vững qua ba cửa sổ; trên VN1 thì đổi theo cửa sổ.
2. **Trên dữ liệu thương mại điện tử, phương pháp hiệu quả nhất phụ thuộc vào biến động nhu cầu sắp tới, thứ mà phân loại theo lịch sử không nắm được.**
   - TSB-NB cần ít tồn kho hơn 13–16% trên chuỗi ổn định ở cả ba cửa sổ.
   - Chỉ LGB-Q phục vụ được chuỗi tăng mạnh.
   - Cả ADI–CV² lẫn phân cụm không giám sát đều không tách được hai loại chuỗi này.
   - Quy tắc chọn phương pháp theo nhóm không hơn việc luôn dùng một phương pháp.
3. **LGB-Q là lựa chọn có tổn thất tệ nhất nhỏ nhất; thanh lý theo phân vị an toàn nhưng chưa chứng minh được lợi ích kinh tế trong 26 tuần.**

Những gì **không** được khẳng định:

- phân khúc mới tốt hơn ADI–CV²;
- thứ hạng các phương pháp nhất quán giữa M5 và VN1;
- foundation model kém hơn nói chung;
- LGB-Q đứng đầu trong các mô hình ML trên VN1 (thứ hạng giữa LGB-Q, LGB-C, HGB-Q không vững).

## 2. Cấu trúc và ngân sách trang

| # | Mục | Trang | Bảng / hình | Nội dung chính |
|---|---|---|---|---|
| — | Title, abstract, keywords | 0,4 | — | Abstract ≤ 200 từ, ba thông điệp |
| 1 | Introduction | 1,0 | — | Vấn đề; khoảng trống; 4 đóng góp; không còn danh sách RQ dài |
| 2 | Related work | 1,0 | — | Ba đoạn: benchmark công khai; nhu cầu rời rạc; từ dự báo đến tồn kho (Wang 2026, Theodorou 2025 theo abstract, Zabraoui, Mohammed). Bỏ bảng định vị |
| 3 | Method | 2,0 | T1 (dữ liệu), F1 (pipeline) | Dữ liệu và kiểm tra đồng bộ (2 câu); mục tiêu dự báo; 7 phương pháp trong một bảng gọn; lớp quyết định; thước đo (wQL, hạng, tồn kho ở cùng fill rate, bootstrap, s\*) |
| 4 | Experimental setup | 0,5 | — | Rolling origin; 3 cửa sổ; kịch bản; môi trường |
| 5 | Results | 3,6 | T2–T7, F2 | Xem mục 3 dưới đây |
| 6 | Discussion and limitations | 1,0 | — | Hàm ý thực tiễn; so với Theodorou và Wang; hạn chế |
| 7 | Conclusion | 0,5 | — | |
| — | References | — | — | Khoảng 25; bỏ các bài không còn trích |
| A | Appendix | — | T8, A1, … | Kiểm tra khả năng so sánh; Chronos-2; VNF; lưới kịch bản; bảng theo nhóm |

## 3. Mục 5 (Results) — thứ tự và bảng

| Mục | Câu hỏi | Bảng / hình (`v3_tables.md`) | Câu kết luận |
|---|---|---|---|
| 5.1 | Phương pháp nào chính xác nhất? | Table 2 | LGB-Q có wQL thấp nhất ở mọi dataset và cửa sổ. Theo chuỗi: M5 rõ ràng; VN1 hòa với TSB-NB ở h = 3, TSB-NB hơn ở h = 13 |
| 5.2 | Phương pháp nào cần ít tồn kho nhất ở cùng fill rate? | Figure 2, Table 3 | M5: LGB-Q, ba cửa sổ, P(best) = 1,00. VN1: LGB-Q / TSB-NB / LGB-Q |
| 5.3 | Kết luận có khác theo nhóm nhu cầu không? | Table 4 | M5: LGB-Q ở hầu hết nhóm. VN1: chỉ lumpy ổn định |
| 5.4 | Vì sao VN1 phụ thuộc giai đoạn? | Table 5 | Chuỗi ổn định: TSB-NB hơn 13–16% ở cả ba cửa sổ. Chuỗi tăng mạnh: chỉ LGB-Q đạt. Kết quả tổng thể theo tỷ trọng chuỗi tăng mạnh (31,5 / 22,8 / 40,4%) |
| 5.5 | Chia nhóm tốt hơn có giúp chọn phương pháp không? | Table 6 | Không: quy tắc theo ADI–CV² hay theo phân cụm đều không hơn LGB-Q một cách đáng tin; ngay cả "tiên tri" theo nhóm cũng không hơn phương pháp đơn tốt nhất |
| 5.6 | Thanh lý | Table 7 | Quy tắc phân vị: mất 0,02 điểm % fill rate. Fixed và dead13: tăng tuần hết hàng 5–23%. s\* gần hoặc trên 1 |
| 5.7 | Các khác biệt giữa hai dataset có phải do cách xử lý? | Một đoạn; chi tiết ở phụ lục (Table 8) | Không phải do thành phần chuỗi; không phải do giá; **(c) lượng thông tin của mô hình — chờ kết quả** |

## 4. Chỗ còn chờ số liệu

- [x] **Table 8 (c):** M5 chỉ dùng 21 đặc trưng chung — đã có: tồn kho LGB-Q đổi dưới 1% ở cả ba cửa sổ, LGB-Q vẫn dẫn đầu. Đã điền vào `v3_draft.md` mục 5.6; không câu nào khác phải sửa.
- [x] **Table A1:** Chronos-2 so với 7 phương pháp trên VN1 và VNF — đã có.

## 5. Chỗ phải sửa so với `final_paper_revA.docx`

1. "eight" → "seven"; bỏ TSB-P ở mọi bảng và mọi câu ví dụ (`06_experiment_results/phase2_b5.md` mục 4).
2. "19 shared features" → "21".
3. Thay "the cause of the VN1 reversal has not been identified" bằng kết quả mục 5.4, 5.5 và 5.7.
4. Thay Table 3 (SQL trung bình) bằng Table 2 mới (wQL, trung vị, hạng).
5. Bỏ các RQ; thay bằng 4 đóng góp gắn với ba thông điệp.
6. Câu về độ nhất quán M5–VN1: dùng số 7 phương pháp (nhóm intermittent ρ = 0,75–0,89 theo fill rate) và hạ xuống thành xu hướng.
7. Chronos-2: bỏ mọi kết quả M5; lý do ghi là "để tránh mọi nghi vấn về trùng dữ liệu huấn luyện".

## 6. Việc tiếp theo

1. Viết toàn văn tiếng Anh theo cấu trúc mục 2 vào `v3_draft.md` (khoảng 5.000–5.500 từ thân bài).
2. Điền Table 8 (c) khi lượt chạy xong.
3. Đổ vào mẫu Word đã chọn; kiểm tra số trang.
4. Kiểm tra Turnitin (≤ 25%).
