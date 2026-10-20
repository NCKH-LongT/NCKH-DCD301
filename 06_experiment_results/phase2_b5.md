# Giai đoạn 2 — B5: bỏ TSB-P, chuyển Chronos-2 xuống phụ lục

Ngày 13/10/2026. Quy trình: `07_paper_draft/phase2_workflow.md`.

Nguồn số liệu:

- `code/outputs/drop_tsbp_effect.md` (script `code/drop_tsbp_effect.py`);
- các kết quả 7 phương pháp có đuôi `_m7` (script `code/outputs/logs/rerun_m7.sh`);
- `code/outputs/robust_accuracy_m7.md`.

Ký hiệu: "8" = EMP, TSB-P, TSB-NB, ETS, LGB-T, LGB-C, HGB-Q, LGB-Q; "7" = như trên, không có TSB-P.

Các kết quả 8 phương pháp vẫn được giữ nguyên trong repo để đối chiếu.

## 1. Kết luận nào đổi khi bỏ TSB-P?

**Không đổi** (không phụ thuộc tập phương pháp):

- tồn kho ở cùng fill rate;
- chênh lệch so với LGB-Q và khoảng tin cậy;
- độ phủ, wQL;
- mọi kết quả thanh lý.

**Có thể đổi:** những gì tính bằng **hạng** hoặc **tương quan hạng**.

| Kết luận | Với 8 phương pháp | Với 7 phương pháp | Đổi? |
|---|---|---|---|
| M5: hạng theo chuỗi tốt nhất, h = 3 (ba cửa sổ) | LGB-Q / LGB-Q / LGB-Q | LGB-Q / LGB-Q / LGB-Q | Không |
| M5: h = 13 | HGB-Q / LGB-Q / HGB-Q (sát nhau) | HGB-Q / LGB-Q / HGB-Q | Không |
| VN1: hạng theo chuỗi tốt nhất, h = 3 | TSB-NB / LGB-Q / LGB-Q | **LGB-Q** / LGB-Q / LGB-Q | Chỉ cửa sổ chính; hai phương pháp vẫn chênh dưới CD (3,18 so với 3,25; CD 0,077) |
| VN1: h = 13 | TSB-NB ở cả ba | TSB-NB ở cả ba | Không |
| VN1 theo nhóm, h = 3 | intermittent: TSB-NB; erratic, lumpy: LGB-Q | Như cũ | Không |
| Dẫn đầu đường đánh đổi, M5 | LGB-Q ở cả ba, P(dẫn đầu) = 1,00 | Như cũ | Không |
| Dẫn đầu đường đánh đổi, VN1 | LGB-Q / TSB-NB / LGB-Q | Như cũ | Không |
| Dẫn đầu theo nhóm (M5 và VN1, mọi nhóm, mọi cửa sổ) | — | Giống hệt | Không |
| SQL trung vị tốt nhất, VN1 intermittent | TSB-P ở cả ba | **TSB-NB** ở cả ba | Tên phương pháp đổi; nhận định giữ nguyên |
| wQL tốt nhất | LGB-Q ở 30/30 tổ hợp | LGB-Q ở 30/30 | Không |

**Nhận định "phương pháp thống kê chính xác hơn trên chuỗi rời rạc điển hình của VN1" vẫn đứng được** sau khi bỏ TSB-P: TSB-NB thay vào vị trí có SQL trung vị tốt nhất trên nhóm intermittent ở cả ba cửa sổ.

## 2. Điểm cần lưu ý: độ nhất quán giữa M5 và VN1 yếu đi

Spearman ρ giữa thứ hạng các phương pháp trên M5 và trên VN1, ba cửa sổ main / w26 / w52:

| Xếp hạng theo | Nhóm | 8 phương pháp | 7 phương pháp |
|---|---|---|---|
| Fill rate ở τ = 0,9 | toàn bộ | 0,69 / 0,93 / 0,60 | 0,54 / 0,89 / 0,39 |
| Fill rate ở τ = 0,9 | intermittent | 0,83 / 0,93 / 0,83 | 0,75 / 0,89 / 0,79 |
| Fill rate ở τ = 0,9 | erratic | 0,19 / 0,83 / 0,05 | −0,21 / 0,75 / −0,43 |
| Đường đánh đổi | toàn bộ | 0,88 / 0,50 / 0,67 | 0,86 / 0,29 / 0,61 |
| Đường đánh đổi | intermittent | 0,90 / 0,95 / n/a | 0,79 / 0,96 / n/a |

- **Vì sao giảm:** TSB-P đứng gần cuối ở **cả hai** dataset. Một phương pháp luôn kém như vậy kéo tương quan hạng lên. Bỏ nó đi, tương quan phản ánh đúng hơn mức nhất quán giữa các phương pháp cạnh tranh.
- **Hệ quả cho bài:**
  - Câu "chỉ nhóm intermittent có thứ hạng nhất quán giữa M5 và VN1 ở mọi cửa sổ (ρ = 0,83–0,93)" phải sửa thành ρ = 0,75–0,89.
  - Với 7 phương pháp, ngưỡng ý nghĩa 5% vào khoảng 0,79, nên hai trong ba giá trị chỉ ở mức biên.
  - [Nhận định nhóm] Nên trình bày đây là xu hướng, không phải kết luận chắc chắn.

## 3. Chronos-2

- **Quyết định:** chỉ báo cáo Chronos-2 ở **phụ lục**, trên VN1 (ba cửa sổ) và VNF. Bỏ kết quả M5.
- **Cách viết trong bài:** "để tránh mọi nghi vấn về việc dữ liệu đánh giá trùng với dữ liệu huấn luyện của mô hình, Chronos-2 chỉ được báo cáo trên VN1 và VNF".
  - Không khẳng định M5 có trong dữ liệu huấn luyện. Báo cáo kỹ thuật không liệt kê M5 trong các bộ dữ liệu huấn luyện (Bảng 6).
- **Số liệu:** hạng của Chronos-2 so với 7 phương pháp đã được tính lại (`code/outputs/logs/rerun_c2m7.sh` → các file đuôi `_c2m7`); kèm bản 7 phương pháp của VNF (`_m7`).
- Kết quả M5 của Chronos-2 vẫn nằm trong repo (`code/outputs/M5_c2/`) nhưng không đưa vào bài.

## 4. Việc phải sửa trong bài (làm ở B6)

1. Mọi bảng: bỏ dòng TSB-P. "Eight methods" → "seven methods"; "four statistical" → "three statistical".
2. Table 4 (hạng theo chuỗi), Table 6 (hạng đường đánh đổi), Table 8 (độ vững): thay bằng số 7 phương pháp.
3. Các câu dùng TSB-P làm ví dụ, chẳng hạn "TSB-P holds less inventory than LGB-Q on 97% of the series but has the lowest fill rate", "TSB-P covers only 0.849": bỏ, hoặc thay bằng ví dụ khác.
4. Mục 5.4, độ nhất quán giữa dataset: dùng số ở mục 2 trên đây.
5. Mục 5.8 (Chronos-2) và 5.9 (VNF): chuyển xuống phụ lục; bỏ dòng M5 trong Table 9.
6. Case study VNF: TSB-P đang là phương pháp có SQL trung bình thấp nhất ở đó. Câu này phải viết lại theo bản 7 phương pháp.

## 5. Trạng thái

- [x] B5 Bỏ TSB-P: tính lại xong ba cửa sổ; bảng trước/sau ở `code/outputs/drop_tsbp_effect.md`.
- [x] Chronos-2 so với 7 phương pháp trên VN1 và VNF — xong (`07_paper_draft/v3_tables.md`, Table A1).
- [x] B2b (c) M5 chỉ dùng 21 đặc trưng chung — xong (cuối `phase2_b1_b2.md`).
