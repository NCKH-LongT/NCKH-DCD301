# Experimental Setup

Phương pháp: `05_methodology/methodology.md`. Bảng và hình trong file này lấy trực tiếp từ `code/outputs/` (bản sao: `tables/`, `figures/`).

## 1. Môi trường

| Thành phần | Giá trị |
|---|---|
| CPU | Intel Core i5-12450H (12 luồng) |
| RAM | 16 GB |
| GPU | RTX 3050 Laptop (4 GB), **không dùng** |
| Hệ điều hành | Windows 11 |
| Python | 3.12.10 |
| Thư viện | lightgbm 4.7.0; scikit-learn 1.8.0; pandas 2.3.3; numpy 2.2.6; scipy 1.17.1 (`code/requirements.txt`) |
| Seed | 2026 (`config.SEED`) |

## 2. Dữ liệu và chia tập

| | M5 | VN1 |
|---|---|---|
| Chuỗi trong panel / được đánh giá | 30.490 / **30.381** | 15.053 / **13.844** |
| Số tuần | 277 | 196 |
| Tuần kiểm thử (26) | 2015-11-21 → 2016-05-14 | 2023-10-09 → 2024-04-01 |
| Tuần tính KPI | 22 (bỏ 4 tuần khởi động) | 22 |
| Mốc huấn luyện lại | Đầu mỗi khối 13 tuần | Đầu Phase 1, đầu Phase 2 |
| Nhóm smooth / erratic / intermittent / lumpy | 16.102 / 1.777 / 10.285 / 2.217 | 2.596 / 1.901 / 6.539 / 2.808 |

## 3. Thí nghiệm đã chạy

| Thí nghiệm | M5 | VN1 |
|---|---|---|
| 8 phương pháp, kịch bản mặc định (τ = 0,9; L = 2; H = 13; q_L = 0,95; k = 26) | ✅ | ✅ |
| Lưới τ ∈ {0,8; 0,9; 0,95} (đường đánh đổi) | ✅ 8 phương pháp | ✅ 8 phương pháp |
| Lưới L ∈ {1, 2, 4}, H ∈ {8, 13, 26} | ❌ chưa chạy (chi phí: LightGBM quantile M5 mất khoảng 21 phút cho h = 3) | ✅ 7 phương pháp (không có `hgb_quantile`) |
| Lưới q_L ∈ {0,9; 0,95; 0,99}, k ∈ {13, 26, 52} | ❌ | ✅ 8 phương pháp |
| Ngưỡng hòa vốn thanh lý (kịch bản mặc định) | ✅ | ✅ |
| Bootstrap 95% (200 lần) cho fill rate, tồn kho | ✅ | ✅ |
| Kiểm định Friedman–Nemenyi / Wilcoxon theo chuỗi (`stat_tests.py`) | ✅ | ✅ |

Lệnh tái lập (dự báo được cache trong `data/cache/forecasts/<D>/`, nên lần chạy lại chỉ mất vài phút):

```bash
python -u code/run_pipeline.py --dataset VN1 --grid full --boot 200
```

```bash
python -u code/run_pipeline.py --dataset M5 --grid tau --boot 200
```

```bash
python code/liquidation_breakeven.py --dataset M5
```

```bash
python code/liquidation_breakeven.py --dataset VN1
```

```bash
python code/analyze_results.py
```

```bash
python code/stat_tests.py
```

Log: `code/outputs/logs/`:

- `run_M5.log`, `run_M5_v2.log`, `run_M5_tau.log`;
- `run_VN1.log`, `run_VN1_v2.log`;
- `breakeven_*.log`, `analyze.log`.

## 4. Thời gian chạy (một horizon, 2 khối, 26 origin)

| Mô hình | M5 h = 3 | M5 h = 13 | VN1 h = 3 | VN1 h = 13 |
|---|---|---|---|---|
| TSB negative binomial | 68 s | 55 s | 30 s | 27 s |
| LightGBM-Tweedie | 240 s | 147 s | 42 s | 44 s |
| LightGBM-conformal | 131 s | 114 s | 39 s | 38 s |
| HistGradientBoosting quantile (≤ 300.000 dòng) | 105 s | 126 s | 85 s | 99 s |
| LightGBM quantile (5 phân vị) | 1.251 s | 686 s | 146 s | 314 s |

Ghi chú:

- Empirical, TSB Poisson và ETS đã được cache từ lần chạy trước nên không có thời gian cho h = 3, 13. Ở các horizon khác của VN1, chúng mất 1–38 s.
- Mô phỏng + KPI cho lưới τ của M5 (8 mô hình × 3 τ × 3 chính sách, bootstrap 200): 65 s.

## 5. Sai lệch so với kế hoạch ban đầu

| Kế hoạch (`01_topic_proposal`, bản v1.x) | Thực tế | Lý do |
|---|---|---|
| M5 theo ngày, 3 cửa hàng, 28 ngày | M5 theo tuần, toàn bộ 10 cửa hàng, 26 tuần | Tần suất tuần phù hợp quyết định nhập hàng và giới hạn bộ nhớ |
| TiDE / DeepAR | Bỏ; thay bằng 2 baseline ML | Phần cứng; `04_proposed_system/ai_model_integration.md` mục 4 |
| Tổng chi phí với c_u, c_o giả định | KPI không đơn vị tiền + ngưỡng hòa vốn | Không có chi phí thực; giả định không đủ tin cậy |
| Dashboard FastAPI + Streamlit | Chưa cài đặt | Ưu tiên benchmark |
| Kiểm định Friedman–Nemenyi | Đã chạy cho SQL và KPI theo chuỗi | `results.md` mục 1b |
