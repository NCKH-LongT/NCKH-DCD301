# AI Model Integration

## 1. Trả lời các câu hỏi của README (Bước 8)

| Nội dung | Trả lời |
|---|---|
| **Model dùng là gì?** | **LightGBM hồi quy phân vị** (global model). Baseline: 4 phương pháp thống kê (Empirical, ETS, TSB với Poisson, TSB với negative binomial) và 3 phương pháp machine learning (LightGBM-Tweedie + safety stock chuẩn, LightGBM-Tweedie + conformal, HistGradientBoosting quantile). **Không dùng deep learning** (mục 4) |
| **Vì sao chọn?** | LightGBM được cả top 50 M5 Accuracy dùng (bài 02, tr. 1). Lời giải hạng nhất M5 Uncertainty huấn luyện LightGBM **riêng cho từng phân vị** (bài 03, tr. 14). Mô hình nhẹ, chạy trên CPU, dùng được đặc trưng ngoại sinh (giá, sự kiện, thuộc tính) |
| **Model lấy từ đâu?** | Thư viện mã nguồn mở `lightgbm` và `scikit-learn`; các phương pháp thống kê được cài đặt vector hóa bằng numpy/scipy trong `code/f2d/models.py`. Không có model đóng hay API trả phí |
| **Input?** | Bảng đặc trưng theo chuỗi × tuần: 27 đặc trưng (M5), 21 (VN1), 19 đặc trưng chung (`data_flow.md` mục 5) |
| **Output?** | Phân vị {0,5; 0,8; 0,9; 0,95; 0,99} của **tổng nhu cầu trong L + R tuần** và **trong H tuần** |
| **Tích hợp vào app?** | Đã cài đặt: Python batch (`code/run_pipeline.py`) → dự báo (NPZ) và KPI (CSV). Thiết kế, chưa cài đặt: ghi khuyến nghị vào Parquet/DuckDB → FastAPI trả JSON → Streamlit hiển thị |
| **Có baseline không?** | Có, 7 baseline (mục 3); tất cả đi qua **cùng một Decision Engine** để so sánh công bằng |

## 2. Mô hình chính: LightGBM quantile

- **Dự báo trực tiếp tổng nhu cầu** D_h = Σ qty(o … o+h−1) với h = L + R (nhập hàng) và h = H (thanh lý). **Không cộng phân vị theo tuần**, vì phân vị của tổng khác tổng các phân vị.
- **Một mô hình cho mỗi (dataset, horizon, phân vị, khối huấn luyện)**; hàm mục tiêu `objective="quantile"`, `alpha` = phân vị. Mục tiêu được chuẩn hóa D_h / `scale` và cắt ở phân vị 99,9 của tập huấn luyện (`data_flow.md` mục 5).
- **Chống chồng chéo phân vị:** sắp xếp lại các phân vị của mỗi dự báo cho tăng dần.
- **Siêu tham số cố định** (`LGB_PARAMS` trong `code/f2d/models.py`: learning rate 0,05; 63 lá; tối thiểu 200 mẫu mỗi lá; feature/bagging fraction 0,8; λ₂ = 1), tối đa 1.000 vòng với **early stopping** 50 vòng trên 13 origin validation ngay trước mốc cắt. LightGBM-Tweedie và LightGBM-conformal dùng cùng tham số, cùng đặc trưng, cùng các origin huấn luyện/validation. HistGradientBoosting dùng cùng đặc trưng và mục tiêu nhưng khác ở bốn điểm (dữ liệu huấn luyện, learning rate, early stopping, horizon đã chạy; mục 3). Không tinh chỉnh siêu tham số riêng cho mô hình nào.
- **Rủi ro đã biết:** bài 12 (tr. 13, 19) cho thấy LightGBM **dạng distributional** kém trên dữ liệu rời rạc. Đề tài dùng **quantile regression** (cách khác), và kiểm chứng bằng hai đối chứng ML: conformal (dự báo điểm + hiệu chỉnh phân phối) và HistGradientBoosting (một thư viện boosting khác).

## 3. Baseline

| Nhóm | Baseline | Cách tạo phân vị D_{L+R}, D_H | Lý do đưa vào |
|---|---|---|---|
| Thống kê | **Empirical** | Phân vị thực nghiệm của các tổng h tuần trong 104 tuần gần nhất của chuỗi | Mốc tối thiểu |
| Thống kê | **ETS(A,N,N)** (α chọn theo từng chuỗi trên lưới) | Phân phối chuẩn quanh tổng dự báo; phương sai của tổng h tuần theo công thức ETS(A,N,N) | Exponential smoothing vẫn cạnh tranh ở cấp product–store (bài 02, tr. 2) |
| Thống kê | **TSB + Poisson** | Trung bình tuần p·z từ TSB → Poisson cho tổng | Chuẩn cho nhu cầu rời rạc, xử lý hàng lỗi thời (bài 16, abstract; bài 23, tr. 2) |
| Thống kê | **TSB + negative binomial** (`tsb_nb`) | Tổng h tuần có trung bình h·p·z, phương sai h·(p·(var_z + z²) − (p·z)²) với var_z là phương sai cỡ đơn trên các tuần có bán trước mốc cắt → negative binomial (Poisson nếu không quá phân tán) | Poisson cho khoảng dự báo quá hẹp với nhu cầu lumpy |
| ML | **LightGBM-Tweedie + safety stock chuẩn** | Dự báo điểm (mục tiêu D_h / s như mô hình quantile, từ v2.4) → μ + z_q·σ, σ từ phần dư validation của từng chuỗi | Cách của đội thắng M5 Accuracy (bài 02, tr. 9) + safety stock truyền thống. **Ablation chính**: phân vị so với dự báo điểm + safety stock |
| ML | **LightGBM-Tweedie + conformal** (`lgb_conformal`) | μ + scale · phân vị của phần dư chuẩn hóa trên validation, tách theo nhóm ADI–CV² | Cách hiện đại để có khoảng dự báo từ mô hình điểm, không giả định phân phối chuẩn |
| ML | **HistGradientBoosting quantile** (`hgb_quantile`, scikit-learn) | Cùng mục tiêu chuẩn hóa như LightGBM quantile; huấn luyện trên mẫu ngẫu nhiên **tối đa 300.000 dòng**, learning rate 0,1, tối đa 300 vòng, early stopping trên 10% dữ liệu huấn luyện (không phải 13 origin validation); chỉ chạy ở horizon mặc định (h = 3, 13) | Kiểm tra kết quả **không phụ thuộc riêng vào LightGBM** |

Trong cùng một dataset, mọi phương pháp dùng **cùng dữ liệu, cùng mốc chia, cùng Decision Engine và cùng các kịch bản (τ, L, H)**.

## 4. Vì sao không dùng deep learning

1. **Bằng chứng về độ chính xác:**
   - LightGBM được cả top 50 M5 Accuracy dùng (bài 02, tr. 1); lời giải hạng nhất M5 Uncertainty là LightGBM theo phân vị (bài 03, tr. 14).
   - Bài 12 thấy các mô hình lớn vừa tốn tính toán vừa kém chính xác hơn (tr. 19).
   - Bài 08 cho thấy chi phí tính toán là vấn đề thực tế khi triển khai (abstract).
2. **Định vị thực tiễn:** pipeline phải chạy được trên **máy tính thông thường không cần GPU mạnh** (CPU i5 12 luồng, RAM 16 GB), phù hợp với doanh nghiệp vừa và nhỏ. Thời gian chạy được báo cáo như một chỉ số.
3. **Trọng tâm của bài là tầng quyết định**, không phải thi đấu độ chính xác dự báo.
4. **Hạn chế cần nêu trong bài:** bài 12 (tr. 19) cho thấy TiDE với đầu ra Tweedie tốt nhất trong các mô hình global trên dữ liệu rời rạc. So sánh với mô hình sâu toàn cục (TiDE, DeepAR) là **hướng phát triển**.

## 5. Vị trí của AI trong hệ thống

```text
Panel tuần ──► Feature Builder ──► [AI] Forecasting Service ──► phân vị D_L+R, D_H
                                                                     │
                                                     Decision Engine ◄┘ (quy tắc minh bạch, không phải AI)
                                                                     │
                                         khuyến nghị ĐẶT HÀNG / GIỮ / THANH LÝ
```

AI chỉ nằm ở **tầng dự báo**. Tầng quyết định là **quy tắc minh bạch** (order-up-to, ngưỡng thanh lý), nên người quản lý hiểu được vì sao hệ thống khuyến nghị như vậy. Đây là gap 6 trong `research_gap.md`.

## 6. Ngân sách tính toán (đo thực tế, CPU i5-12450H)

Thời gian dự báo cho một horizon (2 khối huấn luyện, 26 origin), lấy từ `code/outputs/logs/`:

| Mô hình | M5, h = 3 | M5, h = 13 | VN1, h = 3 | VN1, h = 13 |
|---|---|---|---|---|
| Empirical | — (*) | — (*) | — (*) | — (*) |
| TSB Poisson | — (*) | — (*) | — (*) | — (*) |
| TSB negative binomial | 68 s | 55 s | 30 s | 27 s |
| ETS(A,N,N) | — (*) | — (*) | — (*) | — (*) |
| LightGBM-Tweedie (v2.4, mục tiêu D_h / s) | 133 s | 50 s | 10 s | 7 s |
| LightGBM-conformal (v2.4) | 98 s | 35 s | 9 s | 8 s |
| HistGradientBoosting quantile | 105 s | 126 s | 85 s | 99 s |
| **LightGBM quantile** (5 phân vị) | **1.251 s** | **686 s** | 146 s | 314 s |

(*) Dự báo đã được cache từ lần chạy trước nên log không ghi thời gian. Ở cửa sổ kiểm thử thứ hai (VN1, h = 3 / 13; `run_VN1_w26.log`): Empirical 28 / 17 s, TSB Poisson 14 / 13 s, ETS 1 / 1 s. Ở các horizon khác của VN1 (h = 2, 5, 8, 26): Empirical 24–38 s, TSB Poisson 12–15 s, ETS khoảng 1 s. Toàn bộ pipeline VN1 với lưới kịch bản đầy đủ: khoảng 30 phút (`run_VN1.log`) + 11 phút cho 3 baseline bổ sung (`run_VN1_v2.log`). Mô phỏng tồn kho và tính KPI cho lưới τ của M5: 65 s (`run_M5_tau.log`).

## 7. Phiên bản và tái lập

- Phiên bản thư viện trong `code/requirements.txt`; `random_state`/`seed` cố định (`config.SEED = 2026`).
- Cấu hình mỗi lần chạy nằm trong tham số dòng lệnh của `code/run_pipeline.py` (`--dataset`, `--models`, `--grid`, `--boot`) và log trong `code/outputs/logs/`.
- Dự báo được cache trong `data/cache/forecasts/<DATASET>/`; xóa file để tính lại.
