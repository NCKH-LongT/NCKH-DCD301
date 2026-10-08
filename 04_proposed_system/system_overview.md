# System Overview

## 1. Tên hệ thống

**F2D-Retail** — *Forecast-to-Decision benchmark & recommender for retail replenishment and liquidation*.

Hệ thống có hai vai trò:

1. **Công cụ nghiên cứu (benchmark):** chạy nhiều phương pháp dự báo trên hai dataset công khai (M5, VN1), đưa dự báo qua cùng một lớp quyết định, mô phỏng tồn kho và tính KPI để trả lời RQ1–RQ4.
2. **Hệ thống hỗ trợ ra quyết định (prototype):** mỗi tuần đưa ra khuyến nghị **ĐẶT HÀNG / GIỮ / THANH LÝ** cho từng chuỗi sản phẩm, kèm số lượng và rủi ro hết hàng, hiển thị trên dashboard.

## 2. Người dùng chính

| Người dùng | Nhu cầu | Chức năng dùng |
|---|---|---|
| Nhân viên kế hoạch nhập hàng (replenishment planner) | Đặt bao nhiêu, khi nào | Danh sách đề xuất đặt hàng tuần này, xác suất hết hàng |
| Quản lý ngành hàng / marketing | Hàng nào tồn dư cần giảm giá, thanh lý | Danh sách đề xuất thanh lý, giá trị tồn dư |
| Quản lý cửa hàng / chuỗi | Tình hình chung | KPI: fill rate, mức phục vụ đạt được, số tuần hết hàng, tồn kho tính bằng tuần nhu cầu |
| Nhóm nghiên cứu | So sánh phương pháp | Bảng benchmark và đường đánh đổi tồn kho – fill rate theo dataset × phương pháp × nhóm ADI–CV² |

## 3. Chức năng chính

1. **Nạp và chuẩn hóa dữ liệu** từ hai nguồn khác cấu trúc (M5: dữ liệu ngày + bảng giá riêng; VN1: dữ liệu tuần dạng bảng rộng theo phase) về **một bảng panel theo tuần** dùng chung.
2. **Phân loại nhu cầu ADI–CV²** cho từng chuỗi (smooth / erratic / intermittent / lumpy).
3. **Dự báo xác suất**: phân vị của tổng nhu cầu trong L + R tuần (cho nhập hàng) và trong H tuần (cho thanh lý), bằng nhiều phương pháp.
4. **Engine quyết định**: tính mức đặt hàng tối đa (order-up-to) và lượng thanh lý từ phân vị dự báo.
5. **Mô phỏng tồn kho nhiều kỳ** (backtest) theo các kịch bản mức phục vụ, lead time, tầm nhìn thanh lý; tính KPI **không phụ thuộc chi phí tuyệt đối**.
6. **Báo cáo và dashboard**: bảng benchmark, biểu đồ, danh sách khuyến nghị; xuất JSON qua API.

## 4. Dữ liệu đầu vào

| | M5 (Walmart) | VN1 Forecasting (Vandeput, 2024) |
|---|---|---|
| Loại hình | 1 nhà bán lẻ, 10 cửa hàng vật lý (Mỹ) | 46 nhà bán hàng TMĐT, 328 kho, chủ yếu Mỹ (bài 08, tr. 7) |
| Doanh số | Theo ngày → gộp theo tuần; 30.490 chuỗi item × cửa hàng | Theo tuần; 15.053 chuỗi client × kho × sản phẩm; 196 tuần |
| Giá | `sell_prices.csv` theo tuần | Giá tuần (có ở 29,3% số ô) |
| Lịch / sự kiện | Sự kiện, SNAP | Không có |
| Thuộc tính | Ngành, phòng ban, cửa hàng, bang | Chỉ mã client, kho (ẩn danh) |
| Tồn kho, giá vốn | Không có | Không có |

Phụ lục: dataset giày dép Việt Nam (Vietnam Datathon 2023), chỉ để mô tả. Số liệu chi tiết: `code/outputs/data_profile.md`.

## 5. Mô hình AI

- **Mô hình chính:** LightGBM hồi quy phân vị (global model, mỗi phân vị một mô hình).
- **Baseline thống kê:** Empirical, ETS, TSB (Poisson và negative binomial).
- **Baseline ML:** LightGBM-Tweedie dự báo điểm + safety stock chuẩn (cách của đội thắng M5 Accuracy, bài 02, tr. 9); LightGBM-Tweedie + conformal; HistGradientBoosting quantile (scikit-learn).
- **Không dùng deep learning** (lý do: `ai_model_integration.md` mục 4).
- Chi tiết: `ai_model_integration.md`.

## 6. Output

- **Theo chuỗi × tuần:** phân vị dự báo; hành động (ĐẶT HÀNG / GIỮ / THANH LÝ); lượng đặt; lượng thanh lý; xác suất hết hàng; lý do (vị trí tồn kho so với các phân vị).
- **Theo phương pháp × dataset × nhóm nhu cầu:** sai số dự báo và KPI tồn kho.

## 7. Câu định vị (theo README mục 18)

> This study does not propose a new forecasting model. It benchmarks existing probabilistic forecasting models inside a common, transparent replenishment-and-liquidation decision layer across two retail domains, and evaluates them with inventory KPIs by demand class.
