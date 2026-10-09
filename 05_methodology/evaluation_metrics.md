# Evaluation Metrics

Cài đặt: `code/f2d/evaluate.py` (sai số dự báo, KPI), `code/analyze_results.py` (đường đánh đổi, Spearman), `code/liquidation_breakeven.py` (ngưỡng hòa vốn).

## 1. Mục tiêu đánh giá

1. **RQ1:** so sánh 8 phương pháp về độ chính xác dự báo và KPI tồn kho trên M5 và VN1, và kiểm tra thứ hạng có giữ nguyên giữa hai dataset không.
2. **RQ2:** so sánh theo nhóm ADI–CV².
3. **RQ3:** lượng tồn kho giảm được nhờ thanh lý, cái giá phải trả về fill rate, và ngưỡng giá thu hồi hòa vốn.
4. **RQ4:** độ nhạy theo τ, L, H, q_L, k.

Không dùng chi phí tuyệt đối: mọi KPI tồn kho đều **không có đơn vị tiền**.

## 2. Metric dự báo

Tính trên mọi origin kiểm thử, cho từng chuỗi, rồi lấy trung bình không trọng số giữa các chuỗi trong nhóm. Chuỗi có mẫu số bằng 0 bị bỏ.

| Metric | Công thức | Ý nghĩa | Lý do dùng |
|---|---|---|---|
| **SQL** (scaled quantile loss) | mean_{o,q} ρ_q(D_h − Q_q) / (h · mean\|Δy\|) | Pinball loss trung bình trên 5 phân vị, chia cho sai số của dự báo naive 1 bước (tính trên giai đoạn huấn luyện) nhân h | Đánh giá cả phân phối, không phụ thuộc quy mô chuỗi; thấp hơn là tốt hơn |
| **RMSSE** | √[ mean_o (D_h − Q_0,5)² / (h² · mean Δy²) ] | Sai số của trung vị, chuẩn hóa theo naive | Thước đo dự báo điểm quen thuộc của M5 |
| **Độ phủ** cov_q | mean_o 1{D_h ≤ Q_q} | Tỷ lệ thực tế nằm dưới phân vị q; lý tưởng = q | Kiểm tra hiệu chỉnh của phân vị dùng để đặt hàng (q = 0,9) |

Không dùng MAPE vì không xác định khi nhu cầu bằng 0 (bài 24, tr. 4).

## 3. KPI tồn kho (không đơn vị tiền)

Tính trên 22 tuần kiểm thử sau 4 tuần khởi động. Tổng được cộng theo đơn vị trên mọi chuỗi trong nhóm, rồi mới lấy tỷ lệ; vì vậy chuỗi bán nhiều có trọng số lớn hơn.

| KPI | Định nghĩa | Hướng tốt |
|---|---|---|
| **Fill rate** | Σ lượng bán / Σ nhu cầu | Cao |
| **CSL** (mức phục vụ đạt được) | 1 − Σ tuần hết hàng / Σ tuần | Cao; so với τ |
| **Tỷ lệ hết hàng** (`stockout_rate_demand_weeks`) | Σ tuần có thiếu hàng / Σ tuần có nhu cầu > 0 | Thấp |
| **Tồn kho (tuần nhu cầu)** (`inventory_weeks`) | (tồn cuối tuần trung bình) / (nhu cầu tuần trung bình) | Thấp, khi cùng fill rate |
| **Tồn dư hậu nghiệm** (`excess_weeks_of_demand`) | Phần tồn cuối tuần vượt **nhu cầu thực tế** H tuần tiếp theo, quy ra tuần nhu cầu; chỉ tính các tuần có đủ H tuần phía sau | Thấp |
| **Tỷ lệ thanh lý** (`liquidated_share`) | Σ đơn vị thanh lý / Σ nhu cầu | — (đọc cùng fill rate) |
| **Tỷ lệ chuỗi có thanh lý** (`liq_series_share`) | Số chuỗi có ≥ 1 lần thanh lý / số chuỗi | — |

- **Khoảng tin cậy 95%:** bootstrap theo chuỗi (200 lần, seed 2026) cho fill rate và tồn kho.
- **Phân bố theo chuỗi** (`series_inventory.csv`): trung vị, phân vị 75 và 90 của số tuần tồn kho của từng chuỗi; tỷ lệ chuỗi không có nhu cầu trong giai đoạn KPI.

## 4. Đánh giá không phụ thuộc chi phí

**Đường đánh đổi tồn kho – fill rate.** Chạy τ ∈ {0,8; 0,9; 0,95} và vẽ (tồn kho, fill rate) của từng phương pháp. Phương pháp nằm phía trên – bên trái tốt hơn với mọi tỷ lệ chi phí trong khoảng này.

**Tồn kho cần để đạt fill rate mục tiêu** (0,90; 0,92; 0,94; 0,96):

- Được tính bằng nội suy tuyến tính trên đường τ của từng phương pháp.
- Bỏ trống ("—") nếu mục tiêu nằm ngoài khoảng fill rate đạt được với τ ∈ [0,8; 0,95]. Không ngoại suy.
- Cho phép so sánh ở **cùng mức phục vụ**, loại bỏ khác biệt do phương pháp phân vị lệch cao hoặc lệch thấp.

**Ngưỡng giá thu hồi hòa vốn s\*** của thanh lý (`liquidation_breakeven.py`):

- Mô phỏng có và không có thanh lý, xuất phát từ cùng trạng thái, trên toàn bộ 26 tuần (kể cả khởi động).
- Mọi đại lượng tính bằng đơn vị và định giá theo giá vốn c = 1.
- Gọi Δ = (có thanh lý) − (không thanh lý), X = số đơn vị thanh lý, h = chi phí lưu kho/tuần = tỷ lệ năm / 52, m = biên lợi nhuận gộp (giá bán = (1 + m)·c).

| Cận | Giả định về vị trí tồn kho cuối kỳ | Công thức |
|---|---|---|
| (a) cận trên | Định giá theo giá vốn (có lợi cho việc giữ hàng) | s\* = [ΔĐặt hàng − ΔVịTríCuối + h·ΔTồn(đơn vị·tuần) − (1 + m)·ΔBán] / X |
| (b) cận dưới | Cuối cùng cũng thanh lý với cùng tỷ lệ s | s\* = [ΔĐặt hàng + h·ΔTồn − (1 + m)·ΔBán] / (X + ΔVịTríCuối) |

Cách đọc s\*:

- s\* là tỷ lệ giá thu hồi / giá vốn tối thiểu để thanh lý có lợi hơn giữ lại.
- s\* < 0: thanh lý có lợi kể cả khi cho không.
- s\* > 1: chỉ có lợi khi bán thanh lý cao hơn giá vốn.
- s\* được tính trên lưới chi phí lưu kho {10, 25, 40}%/năm × biên lợi nhuận {30, 50, 100}%, không chọn một con số cố định.
- Khi X rất nhỏ, hoặc khi X + ΔVịTríCuối gần 0 ở cận (b), s\* không ổn định; kết quả này được đánh dấu khi báo cáo.

## 5. Độ nhất quán và kiểm định

| Phân tích | Cách làm | Trạng thái |
|---|---|---|
| Thứ hạng giữa dataset | Spearman ρ giữa fill rate (kịch bản mặc định, không thanh lý) của 8 phương pháp trên M5 và VN1, theo nhóm | ✅ đã chạy |
| Độ ổn định theo kịch bản | Spearman ρ giữa thứ hạng ở L = 2 và L = 1 hoặc 4 (VN1) | ✅ đã tính (`06_experiment_results/results.md`) |
| Kiểm định khác biệt giữa phương pháp | Friedman + Nemenyi trên SQL theo chuỗi; Wilcoxon theo cặp với hiệu chỉnh Holm cho KPI theo chuỗi | 🔲 **chưa chạy**; cần lưu kết quả theo chuỗi |

## 6. Metric hệ thống

Thời gian huấn luyện + dự báo của mỗi mô hình cho một horizon, đo trên CPU i5-12450H, RAM 16 GB (`code/outputs/logs/`; bảng: `04_proposed_system/ai_model_integration.md` mục 6).

## 7. Giả thuyết kiểm tra

| Giả thuyết | Đo bằng |
|---|---|
| H1: LightGBM quantile có SQL thấp nhất trên cả hai dataset | SQL theo nhóm |
| H2: Ở cùng fill rate, dự báo phân vị trực tiếp cần ít tồn kho hơn dự báo điểm + safety stock chuẩn | Tồn kho cần để đạt fill rate |
| H3: Lợi thế của ML lớn hơn ở nhóm smooth/erratic; TSB đủ tốt ở nhóm intermittent | KPI theo nhóm |
| H4: Thanh lý theo phân vị giảm tồn kho mà mất ít fill rate hơn quy tắc cố định | Bảng thanh lý, s\* |

Kết quả kiểm tra từng giả thuyết: `06_experiment_results/results.md` mục 8.
