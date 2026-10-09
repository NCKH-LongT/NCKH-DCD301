# Baseline

Có hai loại baseline:

- **baseline dự báo**, so với LightGBM quantile;
- **baseline chính sách thanh lý**, so với quy tắc thanh lý theo phân vị.

Mọi phương pháp dùng **cùng panel, cùng origin, cùng mốc huấn luyện lại, cùng Decision Engine và cùng kịch bản**. Cài đặt: `code/f2d/models.py`.

## 1. Baseline dự báo

| Mã | Nhóm | Mô tả | Lý do đưa vào |
|---|---|---|---|
| `empirical` | Thống kê | Phân vị thực nghiệm của các tổng h tuần trượt trong 104 tuần gần nhất của chuỗi | Mốc tối thiểu, không có mô hình |
| `ets` | Thống kê | ETS(A,N,N) / SES; phân phối chuẩn cho tổng h tuần | Exponential smoothing vẫn cạnh tranh ở cấp sản phẩm–cửa hàng (bài 02, tr. 2) |
| `tsb` | Thống kê | TSB (Teunter–Syntetos–Babai) + Poisson cho tổng h tuần | Chuẩn cho nhu cầu rời rạc và hàng lỗi thời (bài 16, abstract; bài 23, tr. 2) |
| `tsb_nb` | Thống kê | TSB + negative binomial | Poisson cho khoảng quá hẹp khi nhu cầu lumpy |
| `lgb_tweedie` | ML | LightGBM-Tweedie dự báo điểm + safety stock chuẩn | Cách của đội thắng M5 Accuracy (bài 02, tr. 9) + safety stock truyền thống. **Ablation chính**: phân vị trực tiếp so với dự báo điểm + safety stock |
| `lgb_conformal` | ML | Cùng mô hình Tweedie + split conformal theo nhóm ADI–CV² | Khoảng dự báo từ mô hình điểm mà không giả định phân phối chuẩn |
| `hgb_quantile` | ML | scikit-learn HistGradientBoosting, `loss="quantile"` | Kiểm tra kết quả không phụ thuộc riêng vào thư viện LightGBM |
| **`lgb_quantile`** | **ML (chính)** | LightGBM quantile regression | Lời giải hạng nhất M5 Uncertainty dùng LightGBM theo từng phân vị (bài 03, tr. 14) |

## 2. Chi tiết cài đặt

**Mô hình thống kê** (vector hóa bằng numpy/scipy):

- Tham số được chọn **cho từng chuỗi** tại mỗi mốc cắt, bằng tổng bình phương sai số dự báo 1 bước trong mẫu. Sai số được tính từ tuần thứ 14 của chuỗi (`WARM_WEEKS = 13`) đến trước mốc cắt.
  - TSB: α_d, α_p ∈ {0,05; 0,1; 0,2; 0,3} (16 tổ hợp).
  - SES: α ∈ {0,02; 0,05; 0,1; 0,2; 0,3; 0,5}.
- Khởi tạo: mức trung bình, cỡ đơn trung bình và xác suất có bán trên giai đoạn trước mốc cắt.
- Trạng thái được cập nhật mỗi tuần đến origin.
- ETS: σ = căn bậc hai của MSE 1 bước trong mẫu; phương sai tổng h tuần = σ²·Σ_{j=0}^{h−1}(1 + jα)².
- TSB Poisson: tổng h tuần ~ Poisson(h·p·z).
- TSB NB: var_z là phương sai cỡ đơn trên các tuần có bán trước mốc cắt.
  - Nếu phương sai của tổng > trung bình: dùng negative binomial khớp hai moment.
  - Ngược lại: dùng Poisson.

**Mô hình ML** (cùng đặc trưng, `methodology.md` mục 5):

| | `lgb_quantile` | `lgb_tweedie` | `lgb_conformal` | `hgb_quantile` |
|---|---|---|---|---|
| Mục tiêu | D_h / s, cắt ở phân vị 99,9 | D_h | D_h | D_h / s, cắt ở phân vị 99,9 |
| Hàm mất mát | quantile (5 mô hình) | Tweedie, power 1,1 | Tweedie, power 1,1 | quantile (5 mô hình) |
| Tham số | `LGB_PARAMS` (lr 0,05; 63 lá; ≥ 200 mẫu/lá; fraction 0,8; λ₂ 1) | Như cột 1 | Như cột 1 | lr 0,1; 63 lá; ≥ 200 mẫu/lá; L2 1; tối đa 300 vòng |
| Early stopping | 50 vòng trên 13 origin validation | Như cột 1 | Như cột 1 | 30 vòng trên 10% dữ liệu huấn luyện |
| Dữ liệu huấn luyện | ≤ 3 triệu dòng | ≤ 3 triệu dòng | ≤ 3 triệu dòng | **≤ 300.000 dòng** (mẫu ngẫu nhiên) |
| Phân vị | Trực tiếp | μ + z_q·σ_i | μ + s·F⁻¹_g(q) | Trực tiếp |
| Horizon đã chạy | Mọi horizon của lưới | Mọi horizon | Mọi horizon | Chỉ h = 3, 13 |

Ghi chú cho bảng:

- **`lgb_tweedie`:** σ_i = căn bậc hai của trung bình bình phương phần dư validation của chuỗi i. Nếu chuỗi không có dòng validation thì σ_i = √μ.
- **`lgb_conformal`:** phần dư validation (D_h − μ) / s được gộp theo nhóm ADI–CV² g. Nhóm được tính trên giai đoạn trước mốc cắt. Nhóm có dưới 200 phần dư dùng phân phối gộp của tất cả nhóm.
- **`hgb_quantile`** khác ba mô hình LightGBM ở bốn điểm: dữ liệu huấn luyện, learning rate, early stopping và horizon đã chạy. Vì vậy nó là **kiểm tra độ vững**, không phải so sánh "cùng điều kiện" tuyệt đối với `lgb_quantile`.
- Không tinh chỉnh siêu tham số cho mô hình nào.

## 3. Baseline chính sách thanh lý

| Chính sách | Quy tắc | Vai trò |
|---|---|---|
| `none` | Không thanh lý | Mốc gốc |
| `fixed` | Thanh lý phần vị trí tồn kho vượt k × trung bình tuần của 26 tuần trước (k = 26 mặc định) | Quy tắc "số tuần cung ứng" thường dùng trong thực tế [Nhận định nhóm] |
| `quantile` (đề xuất) | Thanh lý phần vị trí tồn kho vượt Q_{q_L}(D_H) | Dùng chính dự báo xác suất |

## 4. Không đưa vào

- **Deep learning** (TiDE, DeepAR): ngoài phạm vi vì chi phí tính toán và vì trọng tâm là tầng quyết định (`04_proposed_system/ai_model_integration.md` mục 4). Đây là hạn chế cần nêu: bài 12 (tr. 19) cho thấy TiDE với đầu ra Tweedie tốt nhất trong các mô hình global trên dữ liệu rời rạc.
- **Croston gốc:** TSB là phiên bản cải tiến cho hàng lỗi thời (bài 16), nên chỉ giữ TSB.
- **Seasonal naive / moving average:** `empirical` đóng vai trò mốc đơn giản và cho sẵn phân vị.
- **Foundation model (Chronos…):** chưa thử; có thể là hướng mở rộng.
