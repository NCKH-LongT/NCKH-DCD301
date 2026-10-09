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
| Lưới τ ∈ {0,5; 0,8; 0,9; 0,95; 0,99} (đường đánh đổi) | ✅ 8 phương pháp | ✅ 8 phương pháp |
| Lưới L ∈ {1, 2, 4}, H ∈ {8, 13, 26} | ❌ chưa chạy (chi phí: LightGBM quantile M5 mất khoảng 21 phút cho h = 3) | ✅ 7 phương pháp (không có `hgb_quantile`) |
| Lưới q_L ∈ {0,9; 0,95; 0,99}, k ∈ {13, 26, 52} | ❌ | ✅ 8 phương pháp |
| Chính sách thanh lý none / quantile / fixed / dead13 / dead26 | ✅ | ✅ |
| Ngưỡng hòa vốn thanh lý + phân rã (kịch bản mặc định) | ✅ | ✅ |
| Bootstrap 95% (200 lần) cho fill rate, tồn kho | ✅ | ✅ |
| Kiểm định Friedman–Nemenyi / Wilcoxon theo chuỗi (`stat_tests.py`) | ✅ | ✅ |
| Cửa sổ kiểm thử thứ hai (`--offset 26`, lưới τ, 5 chính sách; không có lưới L/H và ngưỡng hòa vốn) | ✅ 29.917 chuỗi, 2015-05-23 → 2015-11-14 | ✅ 11.442 chuỗi, 2023-04-10 → 2023-10-02 |

**Lịch sử chạy:**

| Phiên bản | Thay đổi | Log |
|---|---|---|
| v2.2–v2.3 | 8 mô hình; lưới τ {0,8; 0,9; 0,95}; Tweedie học D_h chưa chuẩn hóa | `run_M5.log`, `run_M5_v2.log`, `run_M5_tau.log`, `run_VN1.log`, `run_VN1_v2.log` |
| **v2.4 (kết quả hiện tại)** | Tweedie/conformal học D_h / s (dự báo lại); lưới τ 5 mức; thêm dead13/dead26; hạng theo đường đánh đổi; kiểm định theo chuỗi | `rerun_v24.sh` → `run_M5_v24.log`, `run_VN1_v24.log`, `breakeven_*.log`, `stat_tests.log`, `analyze.log` |
| v2.4, cửa sổ thứ hai | Bỏ 26 tuần cuối, chạy lại 8 mô hình ở h = 3, 13 với lưới τ | `rerun_w26.sh` → `run_M5_w26.log`, `run_VN1_w26.log`, `stat_tests_w26.log`, `analyze_w26.log` |

Lệnh tái lập toàn bộ kết quả v2.4. Dự báo được cache trong `data/cache/forecasts/<D>/`, nên khi đã có cache, mỗi script chỉ mất vài phút.

```bash
sh code/outputs/logs/rerun_v24.sh
```

```bash
sh code/outputs/logs/rerun_w26.sh
```

## 4. Thời gian chạy (một horizon, 2 khối, 26 origin)

| Mô hình | M5 h = 3 | M5 h = 13 | VN1 h = 3 | VN1 h = 13 |
|---|---|---|---|---|
| TSB negative binomial | 68 s | 55 s | 30 s | 27 s |
| LightGBM-Tweedie (v2.4) | 133 s | 50 s | 10 s | 7 s |
| LightGBM-conformal (v2.4) | 98 s | 35 s | 9 s | 8 s |
| HistGradientBoosting quantile (≤ 300.000 dòng) | 105 s | 126 s | 85 s | 99 s |
| LightGBM quantile (5 phân vị) | 1.251 s | 686 s | 146 s | 314 s |

Ghi chú:

- Empirical, TSB Poisson và ETS đã được cache từ lần chạy trước nên không có thời gian cho h = 3, 13. Ở các horizon khác của VN1, chúng mất 1–38 s.
- Tweedie v2.4 nhanh hơn v2.3 (M5 h = 3: 240 s → 133 s), vì với mục tiêu chuẩn hóa, early stopping dừng sớm hơn.
- Mô phỏng + KPI (5 chính sách, bootstrap 200): lưới τ của M5 khoảng 2 phút; lưới đầy đủ của VN1 khoảng 3 phút.

## 5. Sai lệch so với kế hoạch ban đầu

| Kế hoạch (`01_topic_proposal`, bản v1.x) | Thực tế | Lý do |
|---|---|---|
| M5 theo ngày, 3 cửa hàng, 28 ngày | M5 theo tuần, toàn bộ 10 cửa hàng, 26 tuần | Tần suất tuần phù hợp quyết định nhập hàng và giới hạn bộ nhớ |
| TiDE / DeepAR | Bỏ; thay bằng 2 baseline ML | Phần cứng; `04_proposed_system/ai_model_integration.md` mục 4 |
| Tổng chi phí với c_u, c_o giả định | KPI không đơn vị tiền + ngưỡng hòa vốn | Không có chi phí thực; giả định không đủ tin cậy |
| Dashboard FastAPI + Streamlit | Chưa cài đặt | Ưu tiên benchmark |
| Kiểm định Friedman–Nemenyi | Đã chạy cho SQL và KPI theo chuỗi | `results.md` mục 2 |
| Một cửa sổ kiểm thử | Hai cửa sổ | Kiểm tra độ vững (`results.md` mục 10) |
