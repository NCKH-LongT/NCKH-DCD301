# CODE_GUIDE — Giải thích code của benchmark "From Forecasts to Decisions"

---

## 1. Tổng quan

### 1.1 Luồng chạy

```text
data.py (panel tuần) → classify.py (ADI–CV²) → features.py (đặc trưng)
   → models.py (dự báo phân vị) → policy.py (đặt hàng / thanh lý + mô phỏng)
   → evaluate.py (KPI) → CSV trong code/outputs/
```

`run_pipeline.py` chạy toàn bộ luồng này. Các script còn lại đọc kết quả đã lưu để phân tích tiếp (kiểm định, khoảng tin cậy, hòa vốn thanh lý, bảng cho bài báo).

Tất cả script nằm phẳng trong `code/` (không chia thư mục con) vì nhiều script import lẫn nhau (ví dụ `from equal_fill_ci import totals`) và đường dẫn `code/<script>.py` được dẫn trong tài liệu và trong bài báo. Mục 1.3 nhóm chúng theo vai trò.

### 1.2 Hai quy ước xuyên suốt

- **Origin `o`** là tuần ra quyết định. Dự báo tại `o` chỉ dùng dữ liệu của các tuần nhỏ hơn `o`.
- **Mục tiêu dự báo** là tổng nhu cầu `D_h = Y[o] + … + Y[o+h−1]`, và mọi mô hình dự báo trực tiếp **phân vị của tổng** này. Cách này tránh lỗi cộng phân vị từng tuần (phân vị của tổng khác tổng các phân vị).
- Hai horizon chính: `h = L + R = 3` (đặt hàng) và `h = H = 13` (thanh lý).

### 1.3 Cây thư mục

```text
code/
├── f2d/                        # gói chính (mục 3)
│   ├── config.py               # hằng số
│   ├── data.py                 # nạp M5, VN1, VNF
│   ├── classify.py             # ADI–CV²
│   ├── features.py             # đặc trưng cho mô hình ML
│   ├── series_features.py      # đặc trưng mô tả từng chuỗi (phân tích shift, phân cụm)
│   ├── models.py               # 9 phương pháp dự báo (bài báo dùng 7, mục 5)
│   ├── policy.py               # Decision Engine + mô phỏng lost-sales
│   └── evaluate.py             # SQL, RMSSE, KPI tồn kho
│
│   ── Tầng 1: dữ liệu và benchmark chính ─────────────────────────────
├── profile_datasets.py         # mô tả dữ liệu, tạo cache VNF          (4.7)
├── run_pipeline.py             # lệnh chính: dự báo + mô phỏng + KPI   (4.1)
├── leadtime_forecasts.py       # dự báo thêm h = 2, 5 cho cửa sổ sớm   (4.12)
│
│   ── Tầng 2: phân tích kết quả chính ────────────────────────────────
├── analyze_results.py          # bảng + đường đánh đổi                 (4.2)
├── stat_tests.py               # Friedman–Nemenyi, Wilcoxon–Holm       (4.3)
├── equal_fill_ci.py            # bootstrap tồn kho ở cùng fill rate    (4.4)
├── liquidation_breakeven.py    # giá thu hồi hòa vốn s*                (4.5)
├── per_quantile_loss.py        # pinball loss từng phân vị             (4.6)
│
│   ── Tầng 2: độ vững và khả năng so sánh (phản biện) ─────────────────
├── sync_check.py               # M5 và VN1 có được chuẩn bị như nhau?  (4.9)
├── dataset_shift.py            # M5 khác VN1 thế nào                   (4.9)
├── matched_comparison.py       # cân lại thành phần chuỗi giữa 2 bộ    (4.9)
├── robust_accuracy.py          # wQL, SQL trung vị / cắt đuôi          (4.9)
├── frontier_sensitivity.py     # độ nhạy theo tập mức fill rate        (4.9)
├── hparam_sensitivity.py       # độ nhạy theo siêu tham số LightGBM    (4.9)
├── drop_tsbp_effect.py         # bỏ TSB-P: 8 → 7 phương pháp           (4.9)
│
│   ── Tầng 2: vì sao VN1 phụ thuộc giai đoạn ──────────────────────────
├── demand_shift_analysis.py    # chuỗi tăng / ổn định / giảm           (4.10)
├── segment_series.py           # phân cụm không giám sát               (4.10)
├── segment_eval.py             # phân cụm có giúp chọn mô hình không   (4.10)
├── growth_rule.py              # chọn mô hình theo dự đoán tăng trưởng (4.10)
│
│   ── Tầng 2: tổ hợp, chi phí, lead time ─────────────────────────────
├── combination.py              # C2 = trung bình phân vị LGB-Q, TSB-NB (4.11)
├── combination_weights.py      # trọng số học được và trọng số đều     (4.11)
├── cost_view.py                # quy kết quả ra chi phí theo tỷ lệ r   (4.11)
├── leadtime_equal_fill.py      # độ nhạy theo lead time L = 1, 2, 4    (4.12)
│
│   ── Tầng 2: baseline deep learning ────────────────────────────────
├── run_neural.py               # N-HiTS (cần môi trường riêng)         (4.13)
├── member_run_neural.py        # chạy N-HiTS bằng một lệnh ở máy khác  (4.13)
├── neural_eval.py              # chấm điểm N-HiTS                      (4.13)
│
│   ── Tầng 2: dữ liệu (EDA, đứt hàng) ───────────────────────────────
├── censoring_check.py          # ước lượng tuần nghi hết hàng          (4.14)
├── eda_figures.py              # biểu đồ khám phá dữ liệu              (4.14)
│
│   ── Tầng 3: bài báo ───────────────────────────────────────────────
├── paper_tables_v3.py          # bảng của bài ICIIT (v3)               (4.8)
├── build_iciit_docx.py         # dựng file Word theo mẫu ICIIT         (4.8)
├── revise_iciit_paper.py       # áp các sửa đổi lên bản Word đã sửa tay(4.8)
├── assemble_paper.py           # ghép bản nháp cũ                      (4.8)
├── make_pipeline_figure.py     # vẽ hình pipeline                      (4.8)
├── paper_appendix_tables.py    # bảng phụ lục                          (4.8)
│
└── outputs/                    # kết quả, quy ước tên ở mục 4.15
```

---

## 2. Chuẩn bị và chạy

### 2.1 Cài đặt

```bash
pip install -r code/requirements.txt
```

Phiên bản trong `requirements.txt` được ghim theo máy phát triển (Python 3.12). Các thư viện chính: pandas, numpy, scipy, scikit-learn, lightgbm, matplotlib, pyarrow, python-calamine (đọc Excel nhanh), tabulate. Chronos-2 cần thêm `chronos-forecasting`, `torch`, `transformers`, `accelerate`, `einops`.

Các gói `duckdb`, `fastapi`, `uvicorn`, `streamlit` trong file là cho "prototype app" dự kiến. Hiện chưa có code nào dùng chúng.

**N-HiTS cần một môi trường ảo riêng** (không có trong `requirements.txt`), vì `neuralforecast` kéo theo torch, ray và khoảng 3 GB thư viện:

```bash
python -m venv C:/venvs/nf
C:/venvs/nf/Scripts/python.exe -m pip install numpy pandas neuralforecast==3.3.0 torch==2.12.0 tabulate matplotlib
```

Hai máy chạy N-HiTS dùng neuralforecast 3.3.0 với torch 2.12.0 (CPU). Môi trường này cũng chạy được `censoring_check.py` và `eda_figures.py` (chỉ cần numpy, pandas, scipy, matplotlib, tabulate), nhưng **không** có LightGBM, nên không chạy được `run_pipeline.py`.

### 2.2 Dữ liệu (không có trong git)

Đặt dữ liệu vào `data/` ở gốc repo. Thư mục này nằm trong `.gitignore`.

```text
data/
├── m5-forecasting-accuracy/            # calendar.csv, sales_train_evaluation.csv, sell_prices.csv
├── Vn1 forcasting/                     # Phase 0/1 - Sales/Price.csv, Phase 2 - Sales.csv
├── vietnamsaleandinventory/InventoryAndSale_snapshot_data/   # chỉ cho case study VNF
│   ├── Sales_snapshot_data/  Inventory_snapshot_data/  MasterData/
└── models/chronos-2/                   # trọng số amazon/chronos-2 (tùy chọn)
```

Tên thư mục `Vn1 forcasting` (có chữ "forcasting" viết sai) là tên mà code đang dùng, nên cần giữ nguyên. Nếu giải nén ra tên khác (ví dụ `VN1`), hãy đổi tên thư mục; tương tự, dữ liệu VNF phải nằm trong `vietnamsaleandinventory/`.

### 2.3 Thứ tự chạy gợi ý

```bash
# 0. Mô tả dữ liệu; đồng thời tạo cache VNF (data/cache/vn_sales.parquet)
python code/profile_datasets.py

# 1. Benchmark chính (cửa sổ kiểm thử cuối)
python -u code/run_pipeline.py --dataset VN1 --boot 200
python -u code/run_pipeline.py --dataset M5  --boot 200

# 2. Lưới kịch bản đầy đủ (độ nhạy L, H, q_L, k) hoặc chỉ lưới τ (đường đánh đổi)
python -u code/run_pipeline.py --dataset M5 --grid full --boot 200
python -u code/run_pipeline.py --dataset M5 --grid tau

# 3. Cửa sổ kiểm thử sớm hơn (bỏ 26 hoặc 52 tuần cuối của panel)
python -u code/run_pipeline.py --dataset VN1 --offset 26

# 4. Phân tích
python code/analyze_results.py                 # thêm --tag w26 cho cửa sổ w26
python code/stat_tests.py
python code/equal_fill_ci.py
python code/liquidation_breakeven.py --dataset VN1
python code/per_quantile_loss.py

# 5. Phân tích mở rộng (cần cache dự báo của bước 1–3 cho cả ba cửa sổ)
python code/combination.py                     # C2
python code/cost_view.py
python code/leadtime_forecasts.py --datasets VN1,M5 --offsets 26,52
python code/leadtime_equal_fill.py --offsets 0,26,52

# 6. N-HiTS (môi trường riêng, mục 2.1), rồi chấm điểm ở môi trường chính
C:/venvs/nf/Scripts/python.exe code/member_run_neural.py --dataset M5
python code/neural_eval.py

# 7. Dữ liệu: tuần nghi hết hàng và biểu đồ EDA (không cần cache dự báo)
python code/censoring_check.py
python code/eda_figures.py

# 8. Bảng và file Word của bài báo
python code/paper_tables_v3.py
```

Các lệnh chạy lại đúng như kết quả đã báo cáo được lưu thành script shell trong `code/outputs/logs/rerun_*.sh` (ví dụ `rerun_m7.sh` cho bộ 7 phương pháp, `rerun_w26.sh`, `rerun_w52.sh` cho hai cửa sổ sớm).

Chạy nhanh để thử: `python code/run_pipeline.py --dataset M5 --stores CA_1 --models empirical,tsb --tag smoke`.

> ⚠️ **Luôn kèm `--tag` khi dùng `--stores`.** Thư mục cache dự báo chỉ phụ thuộc vào dataset và `--tag`, không phụ thuộc `--stores`. Nếu thiếu `--tag`, dự báo của tập con một cửa hàng sẽ được lưu vào `data/cache/forecasts/M5/` và các lần chạy đầy đủ sau đó sẽ đọc nhầm file thiếu dữ liệu này.

Dự báo được cache trong `data/cache/forecasts/<DATASET>[_wN]/<model>_h<h>.npz`. Muốn tính lại một mô hình thì xóa file tương ứng.

**Lưu ý thời gian chạy:** `hgb_quantile` chậm hơn LightGBM nhiều, còn Chronos-2 mất khoảng 13 giờ trên CPU cho một cửa sổ M5. Vì vậy cả hai chỉ chạy ở các horizon mặc định (tham số `--default-only-models`).

---

## 3. Gói `f2d/`

### 3.1 `config.py`

File này chỉ chứa hằng số. Muốn đổi kịch bản thì sửa ở đây.

| Hằng số | Giá trị | Ý nghĩa |
|---|---|---|
| `QUANTILES` | 0,5; 0,8; 0,9; 0,95; 0,99 | Các mức phân vị mọi mô hình phải dự báo |
| `ADI_CUT`, `CV2_CUT` | 4/3, 0,5 | Ngưỡng phân nhóm ADI–CV² |
| `TEST_WEEKS` | 26 | 26 tuần cuối làm kiểm thử |
| `BLOCK_WEEKS` | 13 | Huấn luyện lại mô hình mỗi 13 tuần |
| `VALID_WEEKS` | 13 | Số origin validation ngay trước mỗi mốc cắt |
| `WARMUP_WEEKS` | 4 | Số tuần đầu mô phỏng không tính KPI |
| `DEFAULT` | R=1, L=2, τ=0,9, H=13, q_liq=0,95, k_fixed=26 | Kịch bản mặc định |
| `TAU_GRID` | 0,5; 0,8; 0,9; 0,95; 0,99 | Lưới τ cho đường đánh đổi |
| `DEAD_WEEKS` | (13, 26) | Ngưỡng của quy tắc hàng tồn chết |
| `SEED` | 2026 | Hạt giống ngẫu nhiên |

Ký hiệu: `R` là chu kỳ xem xét, `L` là lead time, `τ` là mức phục vụ mục tiêu, `H` là tầm nhìn thanh lý, `q_liq` là phân vị thanh lý, `k` là ngưỡng thanh lý cố định (số tuần bán).

### 3.2 `data.py`

File này đưa mọi dataset về cùng một dạng **panel tuần**, là một dict gồm:

| Khóa | Ý nghĩa |
|---|---|
| `Y` | Doanh số tuần, ma trận [chuỗi × tuần], NaN trước khi chuỗi bắt đầu |
| `P` | Giá tuần, điền bằng giá gần nhất trước đó |
| `Pobs` | True ở các ô giá thực sự được quan sát |
| `weeks` | Ngày đầu tuần |
| `start` | Chỉ số tuần hoạt động đầu tiên của mỗi chuỗi |
| `attrs` | Thuộc tính tĩnh của chuỗi |
| `events` | Biến lịch biết trước (có thể rỗng) |

**Các hàm**

- `_ffill_rows`: điền giá bằng giá gần nhất trước đó theo từng chuỗi. Hàm vector hóa bằng `maximum.accumulate`.
- `load_m5`
  - Cộng doanh số ngày thành tuần Walmart (`wm_yr_wk`).
  - Tuần cuối chỉ có 2 ngày (d_1940–d_1941) nên bị bỏ, còn 277 tuần.
  - Tạo biến lịch theo tuần: số sự kiện và số ngày SNAP của bang tương ứng.
  - Ghép giá từ `sell_prices.csv`.
  - `start` là tuần đầu tiên có giá (sản phẩm lên kệ). Các tuần trước đó là NaN, không phải 0.
  - Kết quả được cache dạng `.npz`.
- `load_vn1`
  - Nối Phase 0, 1, 2 theo khóa (Client, Warehouse, Product). Phase 2 không có giá nên giá là NaN.
  - `start` là tuần có bán đầu tiên.
- `load_vnf` (case study giày dép Việt Nam)
  - Lọc kênh "Bán lẻ" và các dòng có số lượng dương, rồi ghép với `Productmaster`.
  - Sửa mã tuần sai ở ranh giới năm: bỏ 202153 và 202331, gộp 202352 vào 202252.
  - Chuỗi là **mẫu–màu × toàn chuỗi cửa hàng**.
  - Lưu giá bán ròng và giá vốn trung vị của từng chuỗi vào `attrs` để tính hòa vốn bằng tiền.
  - Cần chạy `profile_datasets.py` trước để có `data/cache/vn_sales.parquet`.
- `truncate(panel, T)`: giữ T tuần đầu để tạo cửa sổ kiểm thử sớm hơn.
- `load(name)`: chọn loader theo tên (`M5`, `VN1`, `VNF`).

### 3.3 `classify.py`

- `adi_cv2(Y, start, end)`
  - ADI = số tuần hoạt động / số tuần có bán.
  - CV² = (độ lệch chuẩn / trung bình)², chỉ tính trên các tuần có bán.
  - Chỉ dùng các tuần từ `start` đến `end`.
- `classify(Y, start, end)`
  - Gán `smooth` (ADI < 4/3, CV² < 0,5), `erratic` (ADI < 4/3, CV² ≥ 0,5), `intermittent` (ADI ≥ 4/3, CV² < 0,5) hoặc `lumpy` (ADI ≥ 4/3, CV² ≥ 0,5).
  - Chuỗi không có tuần bán nào được gán `none`.

`end` là tuần bắt đầu kiểm thử, nên việc phân loại không thấy dữ liệu tương lai.

### 3.4 `features.py`

Lớp `Builder` tạo hàng đặc trưng cho cặp (chuỗi i, origin o).

**Cách làm nhanh**
`__init__` tính trước các tổng cộng dồn (`C` cho doanh số, `C2` cho bình phương, `A` cho số tuần hoạt động, `NZ` cho số tuần có bán). Nhờ đó mọi thống kê theo cửa sổ chỉ cần một phép trừ.

**Quy mô `s`**
`s` là doanh số tuần trung bình của 52 tuần hoạt động gần nhất, có sàn 0,1. Các đặc trưng mức (lag, trung bình, độ lệch) được chia cho `s`, để một mô hình toàn cục xử lý được cả chuỗi bán nhiều lẫn bán ít. Chính `s` cũng là một đặc trưng.

**Danh sách đặc trưng**

| Nhóm | Đặc trưng |
|---|---|
| Lag | 1, 2, 3, 4, 8, 13, 26, 52 |
| Cửa sổ trượt | trung bình và độ lệch chuẩn 4/13/26 tuần |
| Độ thưa | tỷ lệ tuần bằng 0 trong 13 tuần; số tuần từ lần bán gần nhất |
| Lịch | tuần trong năm, tháng |
| Sự kiện (chỉ M5) | số sự kiện và số ngày SNAP **trong đúng cửa sổ mục tiêu** (biết trước nên không rò rỉ) |
| Giá | giá tuần trước; thay đổi giá so với 4 tuần trước |
| Tĩnh (chỉ M5) | dept, cat, store, state (biến phân loại) |
| Quy mô | `s` |

**Design notes** (được dẫn từ chú thích trong `features.py`)

- VN1 không dùng `Client` (46 mức) và `Warehouse` (328 mức) làm biến phân loại. Đây là mã ẩn danh; khi đưa vào LightGBM như biến categorical, mô hình overfit và một số phân vị bị phình rất lớn.
- Biến "giá có được quan sát" bị bỏ. Ở VN1 giá chỉ được ghi ở tuần có bán, nên khi huấn luyện biến này trùng với `lag_1 > 0`; và Phase 2 không có giá, nên ở khối kiểm thử thứ hai biến này bằng 0 cho mọi chuỗi (lệch train/test).
- Mô hình Tweedie được huấn luyện trên mục tiêu đã chia quy mô `D_h/s` (giống mô hình phân vị). Huấn luyện trên `D_h` thô cho dự báo rất lớn ở các chuỗi VN1 gần như ngừng bán (`06_experiment_results/results.md`, mục 1).

**Các phương thức chính**

- `target(o, h)`: tổng nhu cầu h tuần.
- `since_sale(o)`: số tuần từ lần bán gần nhất.
- `rows(origins, h, ...)`: gộp nhiều origin thành một bảng. Bỏ chuỗi chưa đủ 13 tuần lịch sử (`min_history`).

### 3.4b `series_features.py`

Đặc trưng **mô tả một chuỗi** (một dòng cho mỗi chuỗi), tính trên các tuần trước mốc cắt nên không rò rỉ kỳ kiểm thử. Khác với `features.py` (một dòng cho mỗi cặp chuỗi × origin, dùng để huấn luyện). Được dùng bởi `dataset_shift.py`, `segment_series.py`, `matched_comparison.py`, `growth_rule.py`.

- `FEATURES`: 13 đặc trưng, gồm mức bán (`log_mean`), cỡ đơn (`log_size`), `adi`, `cv2`, `zero_share`, số tuần từ lần bán cuối, độ dài lịch sử, xu hướng 26 tuần, tỷ lệ gần đây so với lịch sử, tự tương quan 52 tuần, tỷ trọng tuần lớn nhất, đỉnh 52 tuần, độ dao động giá.
- `SHARED`: 9 đặc trưng không phụ thuộc thông tin riêng của từng dataset (không giá, không độ dài panel), dùng khi so sánh hoặc phân cụm chung M5 và VN1.

### 3.5 `models.py`

Mọi hàm có cùng chữ ký `(b, origins, h, qs, series)` và trả về mảng `Q[chuỗi, origin, phân vị]` (NaN cho chuỗi không được đánh giá). Mô hình được huấn luyện lại tại mỗi mốc cắt `c`, 13 tuần một lần. Giữa hai mốc cắt, mô hình thống kê cập nhật trạng thái mỗi tuần, còn mô hình ML giữ nguyên tham số nhưng áp lên đặc trưng mới nhất.

| Mã | Cách hoạt động |
|---|---|
| `empirical` | Phân vị thực nghiệm của các tổng h tuần trượt trong 104 tuần gần nhất. |
| `tsb` | Làm mượt riêng xác suất có bán `p` và kích thước đơn `z`. Tham số chọn theo từng chuỗi trên lưới 4×4 bằng cách tối thiểu hóa SSE trong mẫu. Tổng h tuần ~ Poisson(h·p·z). |
| `tsb_nb` | Cùng trung bình như TSB, phương sai h·(p·(var_z + z²) − (p·z)²). Dùng nhị thức âm nếu phương sai lớn hơn trung bình, ngược lại dùng Poisson. |
| `ets` | ETS(A,N,N) (làm mượt mũ đơn). Khoảng chuẩn với σ từ MSE một bước và hệ số Σ(1+jα)². |
| `lgb_tweedie` | LightGBM Tweedie (variance power 1,1) trên `D_h/s`, nhân lại `s`. Phân vị = μ + z_q·σ, với σ từng chuỗi lấy từ phần dư validation. Đây là kiểu "dự báo điểm + safety stock chuẩn". |
| `lgb_conformal` | Cùng mô hình Tweedie. Phần dư validation (chia cho `s`) được gom theo nhóm ADI–CV² để lấy phân vị phần dư. |
| `hgb_quantile` | scikit-learn `HistGradientBoostingRegressor(loss="quantile")`, một mô hình mỗi phân vị, huấn luyện trên tối đa 300 nghìn dòng. |
| **`lgb_quantile`** | **Mô hình chính.** Một mô hình LightGBM `objective="quantile"` cho mỗi mức q, mục tiêu `D_h/s` bị cắt ở phân vị 99,9, early stopping 50 vòng. |
| `chronos2` | Foundation model dùng zero-shot. Ngữ cảnh là chuỗi các tổng h tuần không chồng lấn, dự báo một bước, không biến ngoài. |

**Tên trong bài báo:** `empirical` = EMP, `ets` = ETS, `tsb_nb` = TSB-NB, `lgb_quantile` = LGB-Q, `lgb_tweedie` = LGB-T, `lgb_conformal` = LGB-C, `hgb_quantile` = HGB-Q. Bài báo dùng **7 phương pháp** này; `tsb` (TSB-P, Poisson) được bỏ khỏi bài ở giai đoạn 2 (`06_experiment_results/phase2_b5.md`; ảnh hưởng của việc bỏ được kiểm tra bằng `drop_tsbp_effect.py`), còn `chronos2` chỉ ở phụ lục. Kết quả 7 phương pháp có hậu tố `_m7`. N-HiTS không nằm trong `MODELS` mà ở script riêng `run_neural.py`.

**Tham số LightGBM (cố định, không tinh chỉnh):** learning rate 0,05; 63 lá; tối thiểu 200 mẫu mỗi lá; feature fraction và bagging fraction 0,8; λ₂ = 1; tối đa 1.000 vòng.

**Các hàm hỗ trợ**

- `block_cutoffs`: chia origin thành các khối 13 tuần.
- `_train_valid`: chọn origin huấn luyện và validation sao cho mục tiêu kết thúc trước `c`, tránh rò rỉ. Giới hạn tối đa 3 triệu dòng, lấy mẫu ngẫu nhiên nếu vượt.
- `_sort`: cắt giá trị âm về 0 và sắp xếp phân vị tăng dần để chúng không chồng chéo.
- `_grid_sse`, `_run_per_series`: chạy bộ làm mượt vector hóa cho mọi chuỗi và mọi tham số trong lưới cùng lúc.
- `MODELS`: từ điển tên → hàm. `run_pipeline.py` dùng nó để gọi mô hình.

### 3.6 `policy.py`

**`simulate(D, S, T_liq, L)`** chạy mô phỏng nhiều kỳ, vector hóa trên các chuỗi. Mỗi tuần diễn ra theo thứ tự:

1. Nhận hàng đã đặt L tuần trước.
2. Tính vị trí tồn kho `IP = tồn hiện có + hàng đang về`.
3. **Thanh lý:** `x = min(max(IP − T_liq, 0), tồn hiện có)`.
4. **Đặt hàng:** `q = max(S − IP, 0)`, bằng 0 nếu tuần đó đã thanh lý (tránh vừa thanh lý vừa mua lại).
5. Nhu cầu của tuần xảy ra: `bán = min(tồn, nhu cầu)`. Phần thiếu **mất luôn** (lost sales, không bù sau).

`S` và `T_liq` được làm tròn lên số nguyên. Tồn ban đầu bằng `S` của tuần xem xét đầu tiên.

**Các hàm khác**

- `stockout_risk(Q, qs, ip)`: nội suy tuyến tính CDF qua các phân vị để ước tính P(D > IP). Chỉ dùng cho đầu ra khuyến nghị, không dùng trong KPI.
- `deadstock(S, since_sale, N)`: nếu chuỗi không bán trong N tuần thì thanh lý toàn bộ tồn và đặt `S = 0` (ngừng đặt hàng) cho đến khi bán lại.

**Năm chính sách thanh lý** (được `run_pipeline.py` dựng từ các hàm trên):

| Chính sách | Ngưỡng `T_liq` |
|---|---|
| `none` | ∞ (không thanh lý) |
| `quantile` (đề xuất) | `Q_{q_liq}(D_H)` của chính mô hình dự báo |
| `fixed` | `k × doanh số tuần trung bình của 26 tuần trước` |
| `dead13`, `dead26` | 0 nếu chuỗi không bán N tuần, ngược lại ∞ |

### 3.7 `evaluate.py`

- `naive_scales`: tính mean|Δy| và mean Δy² của dự báo naive một bước, dùng để chuẩn hóa sai số.
- `forecast_metrics`: trả về bảng theo nhóm gồm
  - **SQL** = pinball loss trung bình / (h · mean|Δy|);
  - **RMSSE** tính trên phân vị 0,5;
  - **độ phủ** của từng phân vị.
- `series_kpis`: tính tổng theo từng chuỗi sau khi bỏ 4 tuần khởi động: nhu cầu, doanh số, hàng mất, số tuần hết hàng, tồn kho, lượng thanh lý, và **tồn dư ex-post** (tồn vượt nhu cầu thực của H tuần kế tiếp).
- `_agg`: gộp thành KPI cho cả nhóm.
- `kpi_table`: bảng KPI theo nhóm, tùy chọn bootstrap theo chuỗi cho khoảng tin cậy 95%.

**KPI chính**

| KPI | Cách tính |
|---|---|
| `fill_rate` | tổng bán / tổng nhu cầu |
| `csl` | 1 − số tuần hết hàng / số tuần |
| `stockout_rate_demand_weeks` | số tuần hết hàng / số tuần có nhu cầu |
| `inventory_weeks` | tồn kho trung bình / nhu cầu tuần trung bình (đơn vị: "tuần nhu cầu") |
| `excess_weeks_of_demand` | tồn dư ex-post, cũng tính bằng tuần nhu cầu |
| `liquidated_share` | lượng thanh lý / tổng nhu cầu |

---

## 4. Các script ở `code/`

### 4.1 `run_pipeline.py` (lệnh chính)

**Tham số**

| Tham số | Ý nghĩa |
|---|---|
| `--dataset` | `M5`, `VN1` hoặc `VNF` (bắt buộc) |
| `--models` | Danh sách mô hình, mặc định 8 mô hình (không có `chronos2`) |
| `--grid` | `default` (một kịch bản), `tau` (chỉ đổi τ), `full` (đổi từng tham số một) |
| `--boot` | Số lần bootstrap cho khoảng tin cậy KPI |
| `--stores` | Chỉ M5: lọc theo cửa hàng, ví dụ `CA_1` |
| `--offset` | Cửa sổ kiểm thử sớm hơn (bỏ N tuần cuối); thư mục kết quả mặc định có hậu tố `w<N>` |
| `--tag`, `--out-suffix` | Hậu tố thư mục kết quả (`--out-suffix` không ảnh hưởng cache dự báo) |
| `--default-only-models` | Mô hình chỉ dự báo ở horizon mặc định (mặc định `hgb_quantile,chronos2`) |

**Các bước**

1. Nạp panel và xác định 26 tuần cuối làm kiểm thử.
2. Chọn chuỗi được đánh giá: bắt đầu ít nhất 13 tuần trước kiểm thử và có ít nhất một tuần có bán trước đó.
3. Phân loại ADI–CV², tạo nhóm `all`, `smooth`, `erratic`, `intermittent`, `lumpy`.
4. Sinh các kịch bản bằng `scenarios()`.
5. Với mỗi (mô hình, horizon): dự báo (hoặc đọc cache), rồi tính SQL, RMSSE, độ phủ.
6. Với mỗi (mô hình, kịch bản, chính sách): chạy `simulate` rồi tính KPI.
7. Ghi kết quả.

**Đầu ra** (trong `code/outputs/<DATASET>[_tag]/`)

| File | Nội dung |
|---|---|
| `classes.csv` | ADI, CV² và nhóm của từng chuỗi được đánh giá |
| `forecast_metrics.csv` | SQL, RMSSE, độ phủ theo mô hình × horizon × nhóm |
| `kpi.csv` | KPI tồn kho theo mô hình × chính sách × kịch bản × nhóm |
| `summary.md` | Bảng tóm tắt ở kịch bản mặc định |

### 4.2 `analyze_results.py`

Đọc `kpi.csv` và `forecast_metrics.csv`, ghi `code/outputs/comparison*.md` và các hình `fig_tradeoff_<D>*.png`. Tham số: `--tag` (cửa sổ, ví dụ `w26`), `--datasets` (ví dụ `VNF`).

- **Đường đánh đổi:** tồn kho (tuần nhu cầu) so với fill rate khi τ thay đổi.
- **Lượng tồn kho cần để đạt fill rate** 0,90 / 0,92 / 0,94 / 0,96 / 0,98, nội suy tuyến tính trên đường τ, không ngoại suy.
- **Frontier rank:** hạng trung bình theo lượng tồn kho cần. Mô hình không đạt được mức nào thì chia nhau các hạng xấu nhất.
- Bảng thanh lý, độ nhạy L và H, và hệ số Spearman giữa thứ hạng trên M5 và VN1.

Hàm `frontier_rank` và hằng `TARGETS` được `equal_fill_ci.py` dùng lại.

### 4.3 `stat_tests.py`

Tính SQL và fill rate theo **từng chuỗi** từ dự báo đã cache, rồi kiểm định theo dataset × nhóm × metric.

- **Friedman** trên các mô hình (chỉ lấy chuỗi đủ dữ liệu cho mọi mô hình).
- **Nemenyi CD** = `q_α/√2 · √(k(k+1)/6N)`, với `q_α` từ phân phối studentized range.
- **Wilcoxon cặp** của từng mô hình so với `lgb_quantile`, hiệu chỉnh **Holm**.
- Báo cáo thêm hiệu trung vị và tỷ lệ chuỗi mà `lgb_quantile` thắng hoặc thua.

Với hàng chục nghìn chuỗi, p-value gần như luôn nhỏ. Vì vậy cần đọc cùng **độ lớn hiệu ứng** (chênh lệch hạng so với CD, tỷ lệ chuỗi thắng/thua). Tham số: `--offset`, `--models` (thêm `chronos2`), `--out-suffix`, `--datasets`.

### 4.4 `equal_fill_ci.py`

Bootstrap theo chuỗi (B = 200, seed 2026) cho lượng tồn kho cần ở cùng fill rate.

- Với mỗi lần lấy mẫu, dựng lại đường đánh đổi của từng phương pháp và nội suy như `analyze_results.py`.
- Báo cáo: lượng tồn kho cần (điểm và khoảng tin cậy 95%), chênh lệch tương đối so với `lgb_quantile`, xác suất `lgb_quantile` cần ít hơn, hạng frontier và P(best) của từng phương pháp.
- Tính cả theo đơn vị và theo giá trị (nhân giá bán theo tuần).

Các câu dạng "cần ít hơn 3–11% tồn kho" trong abstract đến từ file này.

### 4.5 `liquidation_breakeven.py`

Trả lời RQ3: giá thu hồi tối thiểu để thanh lý có lợi. Chạy mô phỏng có và không có thanh lý từ cùng tồn đầu kỳ, rồi tính:

```text
s* = [ΔĐặt hàng − ΔTồn cuối + h·ΔTồn-đơn-vị-tuần − (1+m)·ΔDoanh số] / Đơn vị thanh lý
```

- `h` là chi phí lưu kho tuần (tỷ lệ năm / 52), `m` là biên lợi nhuận gộp (giá bán = (1+m) × giá vốn).
- **Hai cận:** (a) tồn cuối kỳ định giá bằng giá vốn, cho **cận trên** của `s*`; (b) tồn cuối kỳ cũng được thanh lý cùng tỷ lệ, cho **cận dưới**.
- Quét chi phí lưu kho 10 / 25 / 40% mỗi năm và biên lợi nhuận 30 / 50 / 100%.
- Với VNF, tính thêm `s*_actual` bằng giá vốn và giá bán thực của từng chuỗi.
- Cách đọc: `s* ≈ 1` nghĩa là thanh lý chỉ có lợi khi bán gần bằng giá vốn. `s* > 1` nghĩa là chỉ có lợi khi bán được cao hơn giá vốn. `s* < 0` nghĩa là có lợi ngay cả khi thu hồi bằng 0.
- Ghi `breakeven.csv` và `series_inventory.csv` (số tuần tồn kho theo chuỗi).

Script yêu cầu dự báo đã được cache, nên phải chạy `run_pipeline.py` trước.

### 4.6 `per_quantile_loss.py`

Tính pinball loss **riêng từng phân vị** theo nhóm ADI–CV² (h = 3), so `lgb_quantile` với `tsb_nb`. Báo cáo trung bình, trung vị và tỷ lệ chuỗi mà `lgb_quantile` có loss thấp hơn. Mục đích là kiểm tra cách diễn giải "lợi thế của LightGBM quantile đến từ việc tránh sai nặng ở đuôi". Tham số `--runs` dạng `M5:0,VN1:0,M5:26,...`.

### 4.7 `profile_datasets.py`

Mô tả kích thước, độ thưa, phân nhóm ADI–CV² và so sánh tồn kho với doanh số cho M5, VN1 và bộ giày dép Việt Nam. Ghi `outputs/data_profile.md` và cache parquet. **Phải chạy trước khi dùng `--dataset VNF`.**

Số nhóm ADI–CV² trong `data_profile.md` khác bảng trong `05_methodology/dataset.md`, vì profile tính ADI trên toàn bộ lưới thời gian (kể cả các tuần trước khi sản phẩm bắt đầu bán). Benchmark dùng bảng trong `dataset.md`.

### 4.8 Script cho bài báo

**Bài ICIIT (bản đang dùng)**

- `paper_tables_v3.py` sinh mọi bảng của bài 10 trang (7 phương pháp) vào `07_paper_draft/v3_tables.md`, đọc thẳng từ các file kết quả (`*_m7`, `demand_shift.csv`, `segment_eval.csv`, `matched_comparison.csv`, `kpi.csv`, `breakeven.csv`...) nên không có con số nào phải gõ lại.
- `build_iciit_docx.py` dựng file Word theo mẫu ACM của ICIIT từ `v3_draft.md` và `v3_tables.md`. Mẫu không có trong repo, tải ở trang ICIIT rồi truyền bằng `--template`.
- `revise_iciit_paper.py` áp các sửa đổi theo phản biện lên **bản Word đã được sửa tay** (`08_final_submission/ICIIT2027_Paper.docx`) và ghi ra file mới (`_rev1`, `_rev2`...). File gốc không bị sửa. Mỗi thay đổi tìm đoạn văn theo các chữ mở đầu, nên nếu bản Word đổi thì script báo lỗi thay vì sửa nhầm chỗ.

**Script cũ (bản nháp trước v3)**

- `assemble_paper.py` ghép các file trong `07_paper_draft/` thành `full_draft.md`. Nó cố ý giữ các tag nguồn như `[P03 p. 2]`, `[Nhận định nhóm]`, nên các tag này phải xóa tay trước khi nộp.
- `make_pipeline_figure.py` vẽ hình pipeline (Hình 1 của bản tạp chí) vào `07_paper_draft/figures/fig_pipeline.png` và `.pdf`. Số chuỗi "30,490 / 15,053" được gõ cứng trong file này.
- `paper_appendix_tables.py` sinh các bảng phụ lục A1–A5 vào `07_paper_draft/_appendix_tables.md`.

### 4.9 Độ vững và khả năng so sánh giữa hai dataset

Các script này trả lời phản biện "M5 và VN1 có được so sánh công bằng không" và "kết luận có phụ thuộc lựa chọn của nhóm không". Tên mã B1–B7 trong docstring là mã ý kiến phản biện trong `07_paper_draft/phase2_workflow.md`.

| Script | Câu hỏi | Kết quả |
|---|---|---|
| `sync_check.py` | Hai dataset có được chuẩn bị giống nhau không? Định nghĩa ngày bắt đầu chuỗi khác nhau (M5: tuần có giá đầu tiên; VN1: tuần có bán đầu tiên) ảnh hưởng bao nhiêu? | `sync_check.md` |
| `dataset_shift.py` | M5 khác VN1 ở đâu? KS, PSI, AUC từng đặc trưng, classifier "M5 hay VN1?", hình PCA | `dataset_shift.md`, `fig_dataset_shift.png` |
| `matched_comparison.py` | Nếu cân lại để hai bộ có cùng thành phần chuỗi (trọng số nghịch xác suất), kết luận có hội tụ không? | `matched_comparison.md` |
| `robust_accuracy.py` | SQL trung bình không ổn định trên VN1; dùng wQL, SQL trung vị, SQL cắt 1% thì sao? | `robust_accuracy*.md` |
| `frontier_sensitivity.py` | Hạng frontier có phụ thuộc tập mức fill rate (0,90–0,98) không? | `frontier_sensitivity*.md` |
| `hparam_sensitivity.py` | Đổi siêu tham số LightGBM, kết luận có giữ không? | `hparam_sensitivity.md` |
| `drop_tsbp_effect.py` | Bỏ TSB-P (8 → 7 phương pháp) đổi những kết luận nào? | `drop_tsbp_effect.md` |

### 4.10 Vì sao kết quả VN1 phụ thuộc giai đoạn

| Script | Việc làm | Kết quả |
|---|---|---|
| `demand_shift_analysis.py` | Chia chuỗi thành giảm (< 0,67×), ổn định, tăng (> 1,5×) theo nhu cầu kỳ kiểm thử so với 26 tuần trước, rồi so sánh tồn kho từng nhóm. **Mô tả sau sự kiện**, không dùng để ra quyết định được | `demand_shift.md` |
| `segment_series.py` | Phân cụm không giám sát (K-means, GMM, HDBSCAN) trên đặc trưng `SHARED`, khớp trên cửa sổ sớm nhất rồi áp nguyên cho cửa sổ sau | `segmentation.md` |
| `segment_eval.py` | Phân cụm có tốt hơn ADI–CV² để chọn mô hình theo nhóm không (4 tiêu chí C1–C4 cố định trước) | `segment_eval.md` |
| `growth_rule.py` | Dự đoán chuỗi nào sẽ tăng trưởng từ đặc trưng trước kỳ kiểm thử, rồi chọn mô hình theo dự đoán; học trên cửa sổ trước, áp lên cửa sổ sau | `growth_rule.md` |

`segment_eval.py` cũng cung cấp các hàm `curve`, `inv_at`, `MODELS`, `TARGETS` được nhiều script khác import.

### 4.11 Tổ hợp dự báo và góc nhìn chi phí

- `combination.py`: **C2** = trung bình từng phân vị của LGB-Q và TSB-NB (C3 thêm HGB-Q). Báo cáo wQL, tồn kho ở fill 0,90 / 0,92 / 0,94 so với LGB-Q và TSB-NB (bootstrap), và **regret** = phần tồn kho dư so với phương pháp đơn tốt nhất trong lần chạy, trung bình qua các mức fill 0,90–0,98; lấy giá trị lớn nhất qua 6 lần chạy. Cung cấp `setup`, `add_combos`, `wql` cho các script khác. C2 được chọn **sau khi xem kết quả** (post hoc).
- `combination_weights.py`: C_w = w·LGB-Q + (1 − w)·TSB-NB với w = 0; 0,1; …; 1. Học w trên cửa sổ trước, áp lên cửa sổ sau, so với w = 0,5 (C2).
- `cost_view.py`: chi phí trên mỗi đơn vị nhu cầu tính bằng "tuần giữ hàng", C(r) = tồn kho (tuần) + r·(1 − fill rate), với r = phạt mất doanh số / chi phí giữ hàng mỗi tuần. Mỗi phương pháp được chọn mức τ rẻ nhất cho mình.

### 4.12 Lead time

- `leadtime_forecasts.py` tạo dự báo h = 2 và h = 5 (tức L = 1 và L = 4) cho cửa sổ thứ hai và thứ ba. Cửa sổ chính đã có sẵn từ `run_pipeline.py --grid full`. File cache có rồi thì bỏ qua, nên chạy lại được sau khi bị ngắt.
- `leadtime_equal_fill.py` mô phỏng L = 1, 2, 4 trên lưới τ và so sánh ở cùng fill rate, có C2. HGB-Q không có trong phân tích này vì không có dự báo h = 2, 5.

### 4.13 Baseline deep learning: N-HiTS

- `run_neural.py`: N-HiTS (`neuralforecast`) với loss đa phân vị, **cùng giao thức** với các phương pháp khác: dự báo trực tiếp phân vị của tổng h tuần (huấn luyện trên chuỗi tổng trượt Z[t] = Y[t] + … + Y[t+h−1]), huấn luyện lại mỗi khối 13 tuần, lịch sử 52 tuần, 1.500 bước, đơn biến, một seed. Ghi `data/cache/forecasts/<D>[_wN]/nhits_h3.npz`. `--quick` chạy thử 300 chuỗi, không ghi cache.
- `member_run_neural.py`: chạy N-HiTS bằng một lệnh trên máy thứ hai. Kiểm tra nhánh git, phiên bản neuralforecast, kích thước file dữ liệu và **fingerprint** dữ liệu; chạy thử; chạy thật từng cửa sổ; chép kết quả vào `code/outputs/neural/` rồi commit và push (`--no-push` để chỉ commit). Hướng dẫn: `07_paper_draft/handoff_neural_baseline.md`.
- `neural_eval.py`: chấm N-HiTS cùng 7 phương pháp và C2 (wQL, độ phủ, tồn kho ở cùng fill rate, hạng frontier, regret). Đọc dự báo từ `code/outputs/neural/`.

Thời gian chạy N-HiTS trên CPU: khoảng 5–6 phút mỗi cửa sổ VN1 (i5-12450H) và khoảng 7 phút mỗi cửa sổ M5 (20 luồng), xem `code/outputs/neural/*_run_info.json`.

### 4.14 Dữ liệu: tuần nghi hết hàng và biểu đồ EDA

Hai script này chỉ cần dữ liệu thô, **không cần cache dự báo**, và chạy được trong môi trường N-HiTS.

- `censoring_check.py` (phản biện: nhu cầu bị kiểm duyệt khi hết hàng). Không có dữ liệu tồn kho, nên script ước lượng từ doanh số: một khoảng k ≥ 2 tuần bán bằng 0 kẹp giữa hai tuần có bán bị đánh dấu "nghi hết hàng" khi (1 − p)^k < α, với p là tỷ lệ tuần có bán trước kỳ kiểm thử (α = 0,01; thử thêm 0,05 và 0,001). Báo cáo tỷ lệ chuỗi, tỷ lệ tuần và "nhu cầu ẩn" theo dataset × cửa sổ × giai đoạn × nhóm ADI–CV². Bộ phát hiện cũng bắt nhầm các khoảng nghỉ thật, nên con số là **cận trên**. Kết quả: `code/outputs/censoring/`.
- `eda_figures.py`: 6 biểu đồ khám phá dữ liệu M5 và VN1, nhãn tiếng Việt, dùng cho thuyết trình (doanh số theo thời gian với 3 cửa sổ, tỷ lệ nhóm ADI–CV², phân phối 6 đặc trưng, bản đồ ADI–CV², thay đổi nhu cầu khi vào cửa sổ kiểm thử, tương quan). Kết quả: `code/outputs/eda/` kèm `eda_summary.md` ghi các con số trên hình.

### 4.15 Quy ước tên trong `code/outputs/`

| Mẫu | Ý nghĩa |
|---|---|
| `<D>/` | Kết quả `run_pipeline.py` của dataset `D` (M5, VN1, VNF), cửa sổ chính |
| `<D>_w26/`, `<D>_w52/` | Cửa sổ thứ hai và thứ ba (`--offset 26 / 52`) |
| hậu tố `_m7` | 7 phương pháp (không có TSB-P), là bộ dùng trong bài |
| hậu tố `_nop` | Mô hình ML không dùng đặc trưng giá (`--no-price`) |
| hậu tố `_sf` | Chỉ dùng đặc trưng chung cho mọi dataset (`--shared-features`) |
| hậu tố `_c2`, `_c2m7` | Có thêm Chronos-2 (8 hoặc 7 phương pháp + Chronos-2) |
| `comparison*.md`, `fig_tradeoff_*.png` | Từ `analyze_results.py` |
| `equal_fill_ci*`, `stat_tests*` | Từ `equal_fill_ci.py`, `stat_tests.py` |
| `neural/` | Dự báo N-HiTS, log và cấu hình máy chạy |
| `censoring/`, `eda/` | Từ `censoring_check.py`, `eda_figures.py` |
| `logs/` | Log của từng lần chạy và các script `rerun_*.sh` để chạy lại kết quả đã báo cáo |

Bản sao các bảng đưa vào bài nằm ở `06_experiment_results/tables/`.

---

## 5. Điểm cần lưu ý khi giải thích hoặc dùng code

1. **`empirical` không phải Seasonal Naive.** Docstring ghi "Empirical (seasonal naive) baseline", nhưng code lấy phân vị của các tổng h tuần trượt trong 104 tuần. Không có mô hình lag-52 hay moving average nào. Nếu cần mốc tham chiếu chuẩn (ví dụ MA12 của VN1), phải thêm baseline.
2. **Nhu cầu chính là doanh số quan sát được.** `D` trong mô phỏng lấy từ `Y` thực, nên tuần hết hàng trong dữ liệu gốc không được nhận biết (nhu cầu bị kiểm duyệt). Đây là hạn chế đã ghi trong `methodology.md`. `censoring_check.py` ước lượng mức độ: trong kỳ kiểm thử, khoảng 7–9% số tuần của M5 và 6–7% của VN1 nằm trong khoảng nghi hết hàng (cận trên), tập trung gần gấp đôi ở nhóm intermittent và lumpy so với smooth.
3. **Không tinh chỉnh siêu tham số LightGBM.** Cách này công bằng với baseline, nhưng có thể chưa khai thác hết LightGBM.
4. **`lgb_conformal` dùng rất ít dữ liệu hiệu chỉnh:** phần dư lấy từ 13 origin validation, gom theo nhóm. Nó khác split conformal chuẩn, nên không nên gọi nó là conformal prediction "đầy đủ".
5. **`stockout_risk` chưa dùng trong KPI.** Nó chỉ phục vụ đầu ra khuyến nghị.
6. **Thanh lý không có phản ứng giá.** Nhu cầu không thay đổi khi thanh lý, và giá thu hồi chỉ xuất hiện trong phân tích hòa vốn.
7. **Lost sales, không backorder, không giới hạn sức chứa, không số lượng đặt tối thiểu.**
8. **Giá trị gõ cứng:** số chuỗi trong `make_pipeline_figure.py` (30.490 / 15.053, tức toàn bộ chuỗi) không tự cập nhật. Số chuỗi thực sự được đánh giá ở cửa sổ chính là M5 30.381, VN1 13.844, VNF 909. Script N-HiTS (`member_run_neural.py`) dùng đúng các con số này làm fingerprint.
9. **Chronos-2 chạy rất chậm** (khoảng 13 giờ trên CPU cho một cửa sổ M5), nên chỉ chạy ở các horizon mặc định và không phải mọi cửa sổ đều có kết quả.
10. **Kết quả không phụ thuộc môi trường nếu giữ nguyên seed và phiên bản thư viện.** Tuy vậy, phiên bản thư viện trong `requirements.txt` rất mới, nên khi cài ở máy khác có thể cần điều chỉnh.
11. **Cache dự báo không nằm trong git.** `data/cache/forecasts/` chỉ có trên máy đã chạy `run_pipeline.py`. Các script phân tích ở mục 4.9–4.13 (trừ `run_neural.py`) cần cache này; máy mới clone repo phải chạy lại bước 1–3 ở mục 2.3 (vài giờ cho M5). Riêng dự báo N-HiTS được commit trong `code/outputs/neural/`.
12. **`--stores` phải đi kèm `--tag`** (mục 2.3), nếu không cache dự báo dùng chung sẽ bị ghi đè bằng dự báo của tập con.
13. **C2 là tổ hợp được chọn sau khi xem kết quả** (post hoc), chưa kiểm chứng trên dữ liệu độc lập. Khi trích dẫn kết quả C2 cần nói rõ điều này.

---

## 6. Bảng tra nhanh: câu hỏi nghiên cứu → script → file kết quả

| Câu hỏi | Script | Kết quả |
|---|---|---|
| RQ1: độ chính xác dự báo | `run_pipeline.py` | `forecast_metrics.csv` |
| RQ1: hiệu quả tồn kho ở cùng fill rate | `analyze_results.py`, `equal_fill_ci.py` | `comparison*.md`, `equal_fill_ci*.md` |
| RQ1–RQ2: kiểm định theo chuỗi | `stat_tests.py` | `stat_tests*.md` |
| RQ2: theo nhóm ADI–CV² | `run_pipeline.py`, `analyze_results.py` | `kpi.csv`, `comparison*.md` |
| RQ3: thanh lý | `run_pipeline.py`, `liquidation_breakeven.py` | `kpi.csv`, `breakeven.csv` |
| RQ4: độ nhạy L, H, q_L, k | `run_pipeline.py --grid full` | `kpi.csv` |
| Độ vững qua cửa sổ | `run_pipeline.py --offset 26/52` | thư mục `<D>_w26`, `<D>_w52` |
| Foundation model | `run_pipeline.py --models ...,chronos2 --out-suffix c2` | thư mục `<D>_c2` |
| Deep learning (N-HiTS) | `run_neural.py`, `member_run_neural.py`, `neural_eval.py` | `neural/`, `neural_eval.md` |
| Tổ hợp C2, trọng số kết hợp | `combination.py`, `combination_weights.py` | `combination*.md` |
| Kết luận theo chi phí | `cost_view.py` | `cost_view.md` |
| Lead time L = 1, 2, 4 | `leadtime_forecasts.py`, `leadtime_equal_fill.py` | `leadtime_equal_fill*.md` |
| Vì sao VN1 đảo hạng | `demand_shift_analysis.py`, `segment_series.py`, `segment_eval.py`, `growth_rule.py` | `demand_shift.md`, `segmentation.md`, `segment_eval.md`, `growth_rule.md` |
| M5 và VN1 có so sánh được không | `sync_check.py`, `dataset_shift.py`, `matched_comparison.py` | `sync_check.md`, `dataset_shift.md`, `matched_comparison.md` |
| Nhu cầu bị kiểm duyệt (hết hàng) | `censoring_check.py` | `censoring/censoring_check.md` |
| Biểu đồ khám phá dữ liệu | `eda_figures.py` | `eda/*.png`, `eda/eda_summary.md` |
| Bảng và file Word của bài | `paper_tables_v3.py`, `build_iciit_docx.py`, `revise_iciit_paper.py` | `07_paper_draft/v3_tables.md`, `08_final_submission/*.docx` |