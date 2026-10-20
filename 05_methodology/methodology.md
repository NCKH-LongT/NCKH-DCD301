# Methodology

> Mô tả đúng những gì đã cài đặt trong `code/f2d/` và `code/*.py` (commit hiện tại). Tham số lấy từ `code/f2d/config.py` và `code/f2d/models.py`. Dữ liệu: `dataset.md`; baseline: `baseline.md`; metric: `evaluation_metrics.md`.

## 1. Tổng quan

Nghiên cứu **không đề xuất mô hình dự báo mới**. Đây là một **benchmark "từ dự báo đến quyết định"**: 8 phương pháp dự báo xác suất cùng cấp dự báo cho **một lớp quyết định chung** (đặt hàng + thanh lý). Lớp quyết định chạy trong **mô phỏng tồn kho nhiều kỳ**, và kết quả được đo bằng KPI không có đơn vị tiền, trên hai dataset bán lẻ công khai (M5, VN1).

```text
CSV gốc ─► panel tuần ─► phân loại ADI–CV² ─► đặc trưng ─► dự báo phân vị D_{L+R}, D_H (8 phương pháp)
                                                                 │
             KPI theo nhóm ◄─ mô phỏng lost-sales nhiều kỳ ◄─ Decision Engine (order-up-to + thanh lý)
```

| Bước | Cài đặt |
|---|---|
| Panel tuần | `f2d/data.py` |
| Phân loại ADI–CV² | `f2d/classify.py` |
| Đặc trưng | `f2d/features.py` |
| Dự báo | `f2d/models.py` |
| Decision Engine + mô phỏng | `f2d/policy.py` |
| KPI | `f2d/evaluate.py` |
| Chạy toàn bộ | `run_pipeline.py`; phân tích: `analyze_results.py`, `liquidation_breakeven.py` |

## 2. Ký hiệu

| Ký hiệu | Ý nghĩa |
|---|---|
| y_{i,t} | Doanh số tuần t của chuỗi i (dùng làm nhu cầu; xem hạn chế "censored demand" ở mục 9) |
| o | Mốc dự báo (origin) = tuần ra quyết định; dự báo tại o chỉ dùng tuần < o |
| D_h(i, o) | Tổng nhu cầu h tuần: y_{i,o} + … + y_{i,o+h−1} |
| Q_q(D_h) | Phân vị mức q của D_h |
| R, L | Chu kỳ xem xét (1 tuần), lead time (tuần) |
| τ | Mức phục vụ mục tiêu (phân vị dùng để đặt hàng) |
| H, q_L | Tầm nhìn thanh lý (tuần), phân vị thanh lý |
| k | Ngưỡng của quy tắc thanh lý cố định (số tuần bán trung bình) |

## 3. Mục tiêu dự báo

- Mọi phương pháp dự báo **trực tiếp** các phân vị q ∈ {0,5; 0,8; 0,9; 0,95; 0,99} của **tổng nhu cầu** D_h, với h = L + R (đặt hàng) và h = H (thanh lý). Không cộng phân vị của từng tuần, vì phân vị của tổng khác tổng các phân vị.
- Kịch bản mặc định: L = 2, R = 1 → h = 3; H = 13.
- Hậu xử lý chung cho mọi phương pháp: cắt giá trị âm về 0 và sắp xếp lại các phân vị theo thứ tự tăng dần (tránh phân vị chồng chéo).

## 4. Thiết kế đánh giá theo thời gian (rolling origin)

| Thành phần | Giá trị | Nguồn |
|---|---|---|
| Giai đoạn kiểm thử | 26 tuần cuối (`TEST_WEEKS`) | `config.py` |
| Khối huấn luyện lại | 2 khối × 13 tuần (`BLOCK_WEEKS`); mốc cắt c = tuần đầu của mỗi khối | `config.py`, `models.block_cutoffs` |
| Origin dự báo | Mỗi tuần kiểm thử (26 origin) | `run_pipeline.py` |
| Validation (ML) | 13 origin cuối cùng có mục tiêu kết thúc trước c (`VALID_WEEKS`) | `models._train_valid` |
| Huấn luyện (ML) | Tối đa 104 origin trước validation (`TRAIN_ORIGINS`); tối đa 3 triệu dòng, lấy mẫu ngẫu nhiên nếu vượt | `models.py` |
| Khởi động mô phỏng | 4 tuần đầu không tính KPI (`WARMUP_WEEKS`) | `config.py` |

- **Không rò rỉ dữ liệu:** dòng huấn luyện/validation chỉ dùng origin có mục tiêu D_h quan sát xong trước c (origin cuối = c − h).
- Giữa hai mốc cắt: mô hình thống kê cập nhật trạng thái mỗi tuần; mô hình ML giữ nguyên tham số nhưng được áp dụng lên đặc trưng mới nhất.
- Theo bài 08, giảm tần suất huấn luyện lại tiết kiệm nhiều chi phí mà ít mất độ chính xác (abstract); vì vậy chỉ huấn luyện lại mỗi 13 tuần.

## 5. Phương pháp dự báo

Chi tiết và lý do chọn: `baseline.md`. Tóm tắt:

| Mã | Phương pháp | Phân vị của D_h |
|---|---|---|
| `empirical` | Phân vị thực nghiệm | Phân vị của các tổng h tuần trượt trong 104 tuần gần nhất |
| `ets` | ETS(A,N,N) | Chuẩn: h·ℓ ± z_q·σ·√Σ_{j=0}^{h−1}(1 + jα)² |
| `tsb` | TSB + Poisson | Poisson(h·p·z) |
| `tsb_nb` | TSB + negative binomial | NB khớp trung bình h·p·z và phương sai h·(p(var_z + z²) − (pz)²) |
| `lgb_tweedie` | LightGBM-Tweedie (mục tiêu D_h/s) + safety stock chuẩn | μ + z_q·σ_i |
| `lgb_conformal` | LightGBM-Tweedie + split conformal | μ + s·F⁻¹_class(q) |
| `hgb_quantile` | HistGradientBoosting quantile | Một mô hình mỗi phân vị, mục tiêu D_h/s |
| **`lgb_quantile`** | **LightGBM quantile (mô hình chính)** | Một mô hình mỗi phân vị, mục tiêu D_h/s |

**Mô hình chính — LightGBM quantile:**

- Một mô hình global cho mỗi (dataset, h, q, khối); `objective = "quantile"`, `alpha = q`.
- Mục tiêu chuẩn hóa D_h / s, với s = trung bình tuần của 52 tuần hoạt động gần nhất (sàn 0,1). Mục tiêu bị cắt ở phân vị 99,9 của tập huấn luyện. Dự báo được nhân lại với s; pinball loss bất biến theo tỷ lệ nên phép chuẩn hóa này không làm sai lệch mục tiêu phân vị.
- Tham số cố định, không tinh chỉnh: learning rate 0,05; 63 lá; tối thiểu 200 mẫu mỗi lá; feature fraction và bagging fraction 0,8; λ₂ = 1; tối đa 1.000 vòng, early stopping 50 vòng trên tập validation; seed 2026.

**Đặc trưng** (`f2d/features.py`; M5 27, VN1 21, 19 chung):

- Lag 1, 2, 3, 4, 8, 13, 26, 52.
- Trung bình và độ lệch chuẩn trượt 4/13/26 tuần.
- Tỷ lệ tuần bằng 0 trong 13 tuần; số tuần từ lần bán gần nhất.
- Tuần trong năm, tháng.
- M5: tổng số sự kiện và số ngày SNAP **trong đúng cửa sổ mục tiêu h tuần** (biết trước).
- Giá tuần trước, thay đổi giá so với 4 tuần trước.
- M5: dept, cat, store, state (categorical).
- s.

Các đặc trưng mức (lag, trung bình, độ lệch) được chia cho s. VN1 không dùng `Client`/`Warehouse` và không dùng cờ `price_observed` (lý do: `04_proposed_system/data_flow.md` mục 3, 5).

## 6. Decision Engine

Ở đầu mỗi tuần kiểm thử o (R = 1), với mỗi chuỗi (`f2d/policy.py`):

1. Nhận hàng đã đặt từ L tuần trước.
2. Vị trí tồn kho: **IP = tồn hiện có + hàng đang về**.
3. **Thanh lý:** x = min(max(IP − T_liq, 0), tồn hiện có).
4. **Đặt hàng:** q = 0 nếu x > 0; ngược lại q = max(S − IP, 0), với **S = Q_τ(D_{L+R})**.
5. Nhu cầu tuần o xảy ra: bán = min(tồn hiện có, nhu cầu); phần thiếu bị **mất** (lost sales, không bù sau).

Quy ước của bước 3–5:

- Ở bước 3, T_liq = ∞ khi không thanh lý.
- Ở bước 4, không đặt hàng trong tuần đã thanh lý, để tránh vừa thanh lý vừa mua lại.
- S và T_liq được làm tròn lên số nguyên.
- Tồn ban đầu = S của tuần kiểm thử đầu tiên, chưa có hàng đang về.

**Năm chính sách thanh lý**, chạy trên cùng dự báo đặt hàng:

| Chính sách | Ngưỡng T_liq | Ghi chú |
|---|---|---|
| `none` | ∞ | Chỉ đặt hàng |
| `quantile` (đề xuất) | Q_{q_L}(D_H) của cùng phương pháp dự báo | Mặc định q_L = 0,95, H = 13 |
| `fixed` (baseline) | k × trung bình tuần của 26 tuần trước o | Mặc định k = 26 |
| `dead13`, `dead26` (baseline hàng tồn chết) | 0 khi chuỗi không bán trong N = 13 / 26 tuần trước o; ngược lại ∞ | Khi "chết": thanh lý toàn bộ tồn hiện có **và** S = 0 (ngừng đặt hàng) cho đến khi bán lại (`policy.deadstock`) |

**Nhãn khuyến nghị:** THANH LÝ nếu x > 0; ĐẶT HÀNG nếu q > 0; ngược lại GIỮ. **Rủi ro hết hàng** P(D_{L+R} > IP) được nội suy tuyến tính từ các phân vị (`policy.stockout_risk`); hiện chỉ dùng cho đầu ra khuyến nghị, không dùng trong KPI.

## 7. Kịch bản

Hai dataset không có lead time, chi phí hay tồn kho thực, nên các tham số được trình bày là **kịch bản**, không phải giả định về thực tế.

| Tham số | Mặc định | Lưới (thay đổi từng tham số một) |
|---|---|---|
| τ | 0,9 | 0,5; 0,8; 0,9; 0,95; 0,99 (0,8 / 0,9 / 0,95 ≈ c_o = 1, c_u ∈ {4, 9, 19}; bài 11, tr. 16; 0,5 và 0,99 để kéo dài đường đánh đổi) |
| L | 2 | 1, 2, 4 |
| H | 13 | 8, 13, 26 |
| q_L | 0,95 | 0,9; 0,95; 0,99 |
| k | 26 | 13, 26, 52 |

Phạm vi đã chạy: `06_experiment_results/experimental_setup.md` mục 3.

## 8. Phân tích

1. **Độ chính xác dự báo** (SQL, RMSSE, độ phủ) theo mô hình × horizon × nhóm ADI–CV².
2. **KPI tồn kho** ở kịch bản mặc định, theo nhóm, kèm khoảng tin cậy bootstrap.
3. **Đường đánh đổi** tồn kho – fill rate khi τ thay đổi, **lượng tồn kho cần để đạt fill rate** 0,90/0,92/0,94/0,96/0,98 (nội suy tuyến tính trên đường τ), và **hạng theo đường đánh đổi** (hạng trung bình của lượng tồn kho cần trên các mức fill rate). So sánh theo cách này không phụ thuộc vào việc mỗi phương pháp hiệu chỉnh phân vị tốt hay kém ở một τ cụ thể.
4. **Thanh lý:** so sánh `none` / `quantile` / `fixed` / `dead13` / `dead26`; tính **ngưỡng giá thu hồi hòa vốn** s* và phân rã mỗi đơn vị thanh lý (`evaluation_metrics.md` mục 4).
5. **Độ nhạy** theo L, H, q_L, k.
6. **Độ nhất quán giữa dataset:** hệ số Spearman giữa thứ hạng của 8 phương pháp trên M5 và VN1, theo nhóm (theo fill rate ở τ = 0,9 và theo đường đánh đổi).
7. **Kiểm định theo chuỗi:** Friedman–Nemenyi và Wilcoxon–Holm (`code/stat_tests.py`).
8. **Cửa sổ kiểm thử thứ hai:** bỏ 26 tuần cuối của panel và chạy lại toàn bộ trên 26 tuần liền trước (`run_pipeline.py --offset 26`); mô hình không thấy dữ liệu sau điểm cắt.

## 9. Giả định và hạn chế của phương pháp

- **Nhu cầu bị kiểm duyệt (censored):** doanh số quan sát được dùng làm nhu cầu; tuần hết hàng thực tế trong dữ liệu gốc không nhận biết được. [Nhận định nhóm]
- **Không có phản ứng giá:** thanh lý không làm thay đổi nhu cầu trong mô phỏng.
- **Lost sales, không backorder; không giới hạn sức chứa; không có số lượng đặt tối thiểu.**
- **Siêu tham số cố định** cho mọi mô hình ML (không tinh chỉnh); HistGradientBoosting được huấn luyện trên mẫu con (`baseline.md`).
- **Hai cửa sổ kiểm thử** 26 tuần (kết quả chính + cửa sổ kiểm tra độ vững).
- KPI được cộng gộp theo đơn vị, nên chuỗi bán nhiều có trọng số lớn hơn.
