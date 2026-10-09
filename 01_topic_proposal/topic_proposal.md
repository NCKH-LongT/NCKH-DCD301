# Topic Proposal

> Phiên bản v2.2 (09/10/2026). Lịch sử thay đổi: `topic_revision_log.md`. Thiết kế chi tiết: `05_methodology/`; kết quả: `06_experiment_results/`.

## 1. Group Information

- Class: SE1926 (nhánh `FA26_BDT301_SE1926_G01`)
- Group: G01
- Leader: <điền tên>
- Members: <điền tên các thành viên>

## 2. Proposed Title

English title:

**From Forecasts to Decisions: Benchmarking Probabilistic Demand Forecasts for Replenishment and Liquidation on Two Public Retail Datasets (M5 and VN1)**

Vietnamese title:

**Từ dự báo đến quyết định: Đánh giá các phương pháp dự báo nhu cầu xác suất cho quyết định nhập hàng và thanh lý trên hai bộ dữ liệu bán lẻ công khai (M5 và VN1)**

## 3. Application Domain

**Quản lý kho (Inventory Management) trong bán lẻ.**

Với mỗi chuỗi sản phẩm (M5: sản phẩm × cửa hàng; VN1: nhà bán × kho × sản phẩm), mỗi tuần hệ thống dự báo phân phối nhu cầu và đưa ra một trong ba khuyến nghị:

| Khuyến nghị | Điều kiện | Mục tiêu |
|---|---|---|
| **ĐẶT HÀNG (Order)** | Vị trí tồn kho thấp hơn mức order-up-to S = Q_τ(D_{L+R}) | Tránh hết hàng |
| **GIỮ (Hold)** | Vị trí tồn kho nằm giữa S và ngưỡng thanh lý | Không hành động |
| **THANH LÝ (Liquidate)** | Vị trí tồn kho vượt Q_{q_L}(D_H), phân vị cao của nhu cầu trong H tuần tới | Giảm tồn kho dư |

## 4. Problem Statement

Nhà bán lẻ phải cân bằng hai rủi ro ngược chiều: **hết hàng** và **tồn kho dư**. Phần lớn nghiên cứu trên các benchmark bán lẻ công khai (M5, VN1) chỉ tối ưu **độ chính xác dự báo**; câu hỏi "phương pháp dự báo nào cho **quyết định tồn kho** tốt hơn, và ở nhóm sản phẩm nào" ít được đánh giá trên cùng một chính sách và nhiều loại hình bán lẻ. Chi tiết: `03_problem_and_gap/problem_statement.md`.

## 5. Motivation

- Ở M5 Accuracy, LightGBM được cả 50 đội đứng đầu sử dụng (bài 02, tr. 1). Ở M5 Uncertainty, lời giải hạng nhất huấn luyện LightGBM riêng cho từng phân vị (bài 03, tr. 14). Cả hai cuộc thi chỉ đánh giá sai số dự báo.
- Muốn đặt mức tồn kho an toàn cần biết **độ bất định**, tức là cần dự báo phân vị.
- Phần lớn chuỗi bán lẻ có **nhu cầu rời rạc**: 39,7% tuần của M5 và 69,9% tuần của VN1 bằng 0 (`code/outputs/data_profile.md`). Bài 12 (tr. 2) cho rằng chưa có kiến trúc global model được thiết lập cho chuỗi rời rạc.
- Hai dataset không có chi phí hay tồn kho thực, nên kết quả phải được trình bày bằng **KPI không đơn vị tiền** và **kịch bản**, không dựa trên chi phí giả định.
- Pipeline cần **tái lập được, chạy trên máy tính thông thường** (CPU, RAM 16 GB), không cần GPU.

## 6. Target Users

| Người dùng | Nhu cầu |
|---|---|
| Nhân viên kế hoạch nhập hàng | Tuần này đặt chuỗi nào, bao nhiêu |
| Quản lý ngành hàng | Danh sách hàng tồn dư cần thanh lý |
| Quản lý cấp cao | KPI: fill rate, tỷ lệ hết hàng, tồn kho tính bằng tuần nhu cầu |
| Nhà nghiên cứu | Benchmark có thể tái lập trên hai dataset công khai |

## 7. Proposed AI Model / Method

**Mô hình chính:** LightGBM hồi quy phân vị (global model), dự báo **trực tiếp** phân vị {0,5; 0,8; 0,9; 0,95; 0,99} của tổng nhu cầu trong h tuần (h = L + R cho nhập hàng, h = H cho thanh lý).

**Baseline (7):**

- Thống kê: Empirical (phân vị thực nghiệm), ETS(A,N,N), TSB + Poisson, TSB + negative binomial.
- ML: LightGBM-Tweedie + safety stock chuẩn (ablation "dự báo điểm + safety stock"), LightGBM-Tweedie + split conformal theo nhóm nhu cầu, HistGradientBoosting quantile (scikit-learn).
- **Không dùng deep learning** (lý do: `04_proposed_system/ai_model_integration.md` mục 4).

**Phân loại nhu cầu** ADI–CV² với ngưỡng ADI = 4/3, CV² = 0,5 (bài 01, tr. 7–8; bài 18).

**Lớp quyết định** (quy tắc minh bạch, không phải AI): order-up-to S = Q_τ(D_{L+R}); thanh lý phần vị trí tồn kho vượt Q_{q_L}(D_H); so sánh với thanh lý theo ngưỡng cố định k tuần bán trung bình. Mô tả đầy đủ: `05_methodology/methodology.md`.

## 8. System Features

1. Nạp M5 và VN1, đưa về **panel tuần** dùng chung (đã cài đặt, `code/f2d/data.py`).
2. Phân loại ADI–CV² và tạo đặc trưng (đã cài đặt).
3. Dự báo phân vị bằng 8 phương pháp (đã cài đặt).
4. Decision Engine ĐẶT HÀNG / GIỮ / THANH LÝ, kèm rủi ro hết hàng (đã cài đặt, `code/f2d/policy.py`).
5. Mô phỏng tồn kho nhiều kỳ, mất doanh số khi hết hàng (đã cài đặt).
6. Báo cáo benchmark, đường đánh đổi, ngưỡng hòa vốn thanh lý (đã cài đặt, `code/analyze_results.py`, `code/liquidation_breakeven.py`).
7. API + dashboard (FastAPI, Streamlit): **mới ở mức thiết kế** (`04_proposed_system/system_architecture.md`).

## 9. Expected Contribution

1. **Benchmark "từ dự báo đến quyết định"** trên hai dataset bán lẻ công khai khác loại hình (cửa hàng vật lý và thương mại điện tử), với cùng một chính sách nhập hàng + thanh lý trong **mô phỏng nhiều kỳ có lead time**.
2. **Giữ toàn bộ chuỗi rời rạc** và báo cáo kết quả **theo nhóm ADI–CV²**.
3. **Đánh giá không phụ thuộc chi phí**: fill rate, tồn kho tính bằng tuần nhu cầu, đường đánh đổi theo τ, lượng tồn kho cần để đạt một fill rate, và **ngưỡng giá thu hồi hòa vốn** của thanh lý.
4. Mã nguồn mở, tái lập được trên CPU.

## 10. Evaluation Plan

- **Dataset:** M5 (30.490 chuỗi, 277 tuần đủ 7 ngày) và VN1 (15.053 chuỗi, 196 tuần, Phase 2 là đáp án chính thức). Dataset giày dép Việt Nam chỉ ở **phụ lục mô tả**.
- **Chia dữ liệu:** 26 tuần cuối là kiểm thử (2 khối 13 tuần, huấn luyện lại mỗi khối); 13 tuần validation ngay trước mỗi mốc cắt; dự báo mỗi tuần (rolling origin).
- **Metric dự báo:** scaled quantile loss (SQL), RMSSE, độ phủ của từng phân vị. Không dùng MAPE (nhiều số 0; bài 24, tr. 4).
- **Metric tồn kho (không đơn vị tiền):** fill rate, tỷ lệ tuần hết hàng, tồn kho trung bình tính bằng tuần nhu cầu, tồn dư, tỷ lệ thanh lý; khoảng tin cậy bootstrap 95%.
- **Kịch bản:** τ ∈ {0,8; 0,9; 0,95}; L ∈ {1, 2, 4}; H ∈ {8, 13, 26}; q_L ∈ {0,9; 0,95; 0,99}; k ∈ {13, 26, 52}.
- **Kiểm định thống kê:** Friedman–Nemenyi hoặc Wilcoxon trên kết quả theo chuỗi (**chưa chạy**, `06_experiment_results/results.md` mục 9).
- **Hệ thống:** thời gian chạy của từng mô hình.

## 11. Related Papers

Danh sách đầy đủ: `02_related_work/paper_list.md` (24 bài chính thức + bài 20 và W1–W3 ở danh sách theo dõi). Các bài trụ cột:

| No | Title | Year | Source | Link / DOI |
|---|---|---|---|---|
| 01 | The M5 competition: Background, organization, and implementation | 2022 | Int. J. Forecasting | https://doi.org/10.1016/j.ijforecast.2021.07.007 |
| 02 | M5 accuracy competition: Results, findings, and conclusions | 2022 | Int. J. Forecasting | https://doi.org/10.1016/j.ijforecast.2021.11.013 |
| 03 | The M5 uncertainty competition: Results, findings and conclusions | 2022 | Int. J. Forecasting | https://doi.org/10.1016/j.ijforecast.2021.10.009 |
| 08 | The cost of ensembling: is it always worth combining? (dùng M5 + VN1) | 2025 | arXiv | https://arxiv.org/abs/2506.04677 |
| 11 | Multi-objective probabilistic forecast combination for inventory demand | 2026 | arXiv | https://arxiv.org/abs/2606.04900 |
| 12 | Intermittent time series forecasting: local vs global models | 2026 | arXiv | https://arxiv.org/abs/2601.14031 |
| 16 | Intermittent demand: Linking forecasting to inventory obsolescence | 2011 | EJOR | https://doi.org/10.1016/j.ejor.2011.05.018 |
| 18 | On the categorization of demand patterns | 2005 | JORS | https://doi.org/10.1057/palgrave.jors.2601841 |
| 19 | Optimising forecasting models for inventory planning | 2020 | IJPE | https://doi.org/10.1016/j.ijpe.2019.107597 |

> **Định vị:** bài 11 gần nhất (M5, order-up-to theo phân vị, newsvendor từng kỳ, không thanh lý, không phân tích theo nhóm nhu cầu). Bài 21 đã mô phỏng tồn kho nhiều kỳ trên tập con M5, nên "mô phỏng nhiều kỳ" **không** phải điểm mới riêng. Điểm khác biệt của đề tài: hai dataset khác loại hình, giữ toàn bộ chuỗi rời rạc, quyết định thanh lý và ngưỡng hòa vốn, KPI theo nhóm ADI–CV². Bài 20 và W3 chưa đọc được toàn văn, nên không đặt RQ "độ chính xác có tương quan với hiệu quả tồn kho" (`03_problem_and_gap/research_gap.md` mục 6).
