# Topic Proposal

## 1. Group Information

- Class: SE1930
- Group: G06
- Leader: <điền tên>
- Members: <điền tên các thành viên>

## 2. Proposed Title

English title:

**From Forecasts to Decisions: A Probabilistic Demand Forecasting Framework for Replenishment and Liquidation Recommendations in Retail Inventory Management — Evidence from the M5 Dataset**

Vietnamese title:

**Từ dự báo đến quyết định: Khung dự báo nhu cầu xác suất hỗ trợ khuyến nghị nhập hàng và thanh lý nhằm giảm tồn kho và hết hàng trong quản lý kho bán lẻ — thực nghiệm trên bộ dữ liệu M5**

## 3. Application Domain

**Quản lý kho (Inventory / Warehouse Management) trong bán lẻ.**

Bài toán cụ thể: với mỗi sản phẩm tại mỗi cửa hàng (SKU–store), hệ thống dự báo nhu cầu trong tương lai và đưa ra một trong ba khuyến nghị:

| Khuyến nghị | Điều kiện | Mục tiêu |
|---|---|---|
| **NHẬP HÀNG (Replenish)** | Tồn kho dự kiến không đủ đáp ứng nhu cầu trong thời gian chờ hàng (lead time) | Tránh hết hàng (stockout) |
| **GIỮ NGUYÊN (Hold)** | Tồn kho nằm trong vùng an toàn | Không phát sinh chi phí |
| **THANH LÝ / GIẢM GIÁ (Liquidate / Markdown)** | Tồn kho vượt xa nhu cầu dự báo ở mức cao trong một khoảng thời gian dài | Giảm tồn kho dư thừa (overstock) và chi phí lưu kho |

## 4. Problem Statement

Các nhà bán lẻ thường phải đối mặt cùng lúc với hai rủi ro ngược chiều: **hết hàng** (mất doanh thu và khách hàng) và **tồn kho dư thừa** (tốn chi phí lưu kho, hàng quá hạn, phải giảm giá). Nguyên nhân chính là nhu cầu biến động mạnh theo mùa vụ, giá bán, sự kiện, chương trình SNAP. Ngoài ra, rất nhiều sản phẩm có **nhu cầu rời rạc (intermittent demand)**: nhiều ngày liên tiếp không bán được cái nào, rồi bất ngờ bán được vài cái.

Bộ dữ liệu M5 (Walmart, 42.840 chuỗi thời gian phân cấp, 30.490 SKU–store, 1.941 ngày) đã trở thành benchmark chuẩn cho dự báo bán lẻ. Tuy vậy, **phần lớn nghiên cứu trên M5 chỉ tối ưu độ chính xác dự báo** (WRMSSE, WSPL), còn câu hỏi "độ chính xác cao hơn có thực sự giúp **quyết định nhập/thanh lý tốt hơn** hay không" thì ít được đánh giá. Bài này nhằm lấp khoảng trống giữa **dự báo** và **quyết định tồn kho**.

## 5. Motivation

- Theo tổng kết cuộc thi M5 (Makridakis et al., 2022), các mô hình dạng LightGBM thắng áp đảo về độ chính xác. Tuy nhiên, đánh giá chỉ dừng ở sai số dự báo, chưa gắn với chi phí vận hành kho.
- Dự báo điểm (point forecast) chỉ cho một con số. Muốn quyết định lượng tồn kho an toàn thì cần biết **độ bất định**, tức là cần dự báo xác suất / phân vị (quantile).
- Các nghiên cứu gần đây (bài 12 trong `paper_list.md`) chỉ ra rằng **SKU có nhu cầu thưa/bằng 0** (khoảng 60% quan sát của M5 là số 0) vẫn là bài toán mở. Trong khi đó, đây chính là nhóm dễ gây tồn kho chết nhất.
- Doanh nghiệp vừa và nhỏ cần một pipeline **đơn giản, tái lập được, chạy được trên máy thường**, không cần ensemble hàng chục mô hình (bài 8: ensemble không phải lúc nào cũng đáng chi phí).

## 6. Target Users

| Người dùng | Nhu cầu |
|---|---|
| Nhân viên / quản lý kho cửa hàng | Biết hôm nay cần đặt thêm SKU nào, bao nhiêu |
| Bộ phận mua hàng (Procurement / Replenishment planner) | Lập kế hoạch đặt hàng theo lead time |
| Quản lý ngành hàng / Marketing | Danh sách hàng tồn cần giảm giá hoặc thanh lý |
| Quản lý cấp cao | Dashboard KPI: fill rate, tỷ lệ hết hàng, giá trị tồn kho dư |

## 7. Proposed AI Model / Method

**Lý do cần AI:** mỗi ngày có hàng chục nghìn SKU–store, mỗi SKU chịu tác động phi tuyến của giá, ngày lễ, SNAP, thứ trong tuần. Làm quy tắc thủ công hoặc dùng trung bình động không nắm bắt được các tác động này và cũng không định lượng được độ bất định.

**Mô hình chính (AI):**

- **LightGBM global model** (Ke et al., 2017), cùng loại mô hình đã thắng M5 Accuracy:
  - Dự báo điểm với hàm mất mát **Tweedie** (phù hợp dữ liệu nhiều số 0).
  - Dự báo **phân vị (quantile regression)** ở các mức τ ∈ {0.5, 0.75, 0.9, 0.95, 0.99}. Các phân vị này dùng làm đầu vào cho lớp ra quyết định.
- **Phân loại nhu cầu theo ADI–CV²** (Syntetos–Boylan): smooth / erratic / intermittent / lumpy. Dùng để phân tích kết quả theo từng nhóm và chọn chiến lược phù hợp.

**Lớp ra quyết định (Decision layer), không phải model mới mà là chính sách tồn kho cổ điển được "cấp dữ liệu" bởi dự báo xác suất:**

- Mức đặt hàng tối đa (order-up-to) theo **newsvendor**: `S = Q_τ*(nhu cầu trong L + R ngày)`, với `τ* = c_u / (c_u + c_o)` (c_u: chi phí thiếu hàng, c_o: chi phí thừa hàng).
- Lượng nhập = `max(0, S − tồn kho hiện tại)` → **NHẬP HÀNG**.
- Nếu tồn kho > `Q_0.95(nhu cầu trong H ngày)` → phần dư được đề xuất **THANH LÝ / GIẢM GIÁ**.

**Baseline để so sánh:**

- Seasonal Naive (tuần trước), Moving Average 28 ngày, ETS.
- Croston / TSB (chuẩn cho nhu cầu rời rạc).
- LightGBM dự báo điểm + safety stock giả định phân phối chuẩn. Đây là ablation quan trọng nhất: trả lời câu hỏi dự báo xác suất có tốt hơn cách truyền thống hay không.
- *(Tùy chọn)* Chronos zero-shot, đại diện cho foundation model (bài 6, 7).

## 8. System Features

1. **Nạp & xử lý dữ liệu:** đọc `sales_train`, `calendar`, `sell_prices` của M5, tạo đặc trưng (lag, rolling mean, giá, sự kiện, SNAP).
2. **Dự báo nhu cầu xác suất** 28 ngày cho từng SKU–store (các phân vị + giá trị kỳ vọng).
3. **Engine khuyến nghị** NHẬP / GIỮ / THANH LÝ, kèm số lượng và mức độ rủi ro hết hàng.
4. **Mô phỏng tồn kho (inventory simulator):** chạy lại lịch sử (rolling-origin backtest) để đo chi phí và fill rate của từng chính sách.
5. **Dashboard:** danh sách SKU cần nhập, danh sách SKU tồn dư cần thanh lý, KPI tổng hợp. Có thể làm bằng Streamlit + FastAPI.

## 9. Expected Contribution

1. **Khung "forecast-to-decision"** trên M5: nối dự báo phân vị bằng LightGBM với chính sách nhập hàng và thanh lý trong một **mô phỏng tồn kho nhiều kỳ** (có lead time và tồn kho mang sang), đánh giá bằng **KPI tồn kho** (fill rate, stockout, overstock, tổng chi phí) thay vì chỉ sai số dự báo.
2. **Phân tích thực nghiệm theo loại nhu cầu (ADI–CV²):** chỉ ra ở nhóm SKU nào thì AI mang lại lợi ích rõ nhất, và ở nhóm nào baseline thống kê (TSB) vẫn đủ tốt.
3. **Phân tích độ nhạy theo tỷ lệ chi phí** c_u/c_o: cho thấy khuyến nghị thay đổi thế nào theo chiến lược doanh nghiệp (ưu tiên không hết hàng hay ưu tiên ít tồn kho).
4. Pipeline và mã nguồn **mở, tái lập được** (khắc phục hạn chế "khó tái lập" của bài 2 và 3).

## 10. Evaluation Plan

- **Dataset:** M5 Forecasting (Kaggle/Walmart), gồm 3 bang, 10 cửa hàng, 3 ngành hàng, 30.490 SKU–store, 1.941 ngày. Giai đoạn thử nghiệm: dùng 3 cửa hàng đại diện (CA_1, TX_1, WI_1 ≈ 9.147 chuỗi), sau đó mở rộng ra toàn bộ nếu tài nguyên cho phép. Chia dữ liệu theo đúng thiết kế gốc (28 ngày validation, 28 ngày test) và thêm rolling-origin backtest.
- **Baseline:** Seasonal Naive, MA(28), ETS, Croston/TSB, LightGBM point + normal safety stock.
- **Metrics:**
  - *Dự báo:* RMSSE / WRMSSE, MAE, RMSE, Pinball loss / WSPL. Không dùng MAPE vì dữ liệu có nhiều số 0 nên MAPE không xác định.
  - *Tồn kho (quan trọng nhất):* Fill rate, tỷ lệ ngày hết hàng, số lượng tồn dư, chi phí lưu kho, tổng chi phí (thiếu + thừa), giá trị hàng đề xuất thanh lý.
  - *Hệ thống:* thời gian huấn luyện, thời gian suy luận cho toàn bộ SKU.
- **Kiểm định thống kê:** Diebold–Mariano hoặc kiểm định Friedman–Nemenyi giữa các phương pháp.
- **Expert evaluation:** *(tùy chọn)* nhờ 2–3 người làm vận hành bán lẻ đánh giá tính hợp lý của danh sách khuyến nghị.
- **User survey:** *(tùy chọn)* SUS cho dashboard.
- **Giả định mô phỏng (phải ghi rõ trong bài):** M5 **không có dữ liệu tồn kho thực**. Vì vậy tồn kho ban đầu, lead time (ví dụ L = 7 ngày), chu kỳ đặt hàng (R = 7 ngày) và chi phí c_u, c_o được **giả lập có tham số** và phân tích độ nhạy.

## 11. Related Papers

Danh sách đầy đủ gồm 19 bài, xem `02_related_work/paper_list.md`. Các bài trụ cột (đánh số theo `paper_list.md`):

| No | Title | Year | Source | Link / DOI |
|---|---|---|---|---|
| 02 | M5 accuracy competition: Results, findings, and conclusions | 2022 | Int. J. Forecasting | https://doi.org/10.1016/j.ijforecast.2021.11.013 |
| 03 | The M5 uncertainty competition: Results, findings and conclusions | 2022 | Int. J. Forecasting | https://doi.org/10.1016/j.ijforecast.2021.10.009 |
| 11 | Multi-objective probabilistic forecast combination for inventory demand | 2026 | arXiv | https://arxiv.org/abs/2606.04900 |
| 12 | Intermittent time series forecasting: local vs global models | 2026 | arXiv | https://arxiv.org/abs/2601.14031 |
| 16 | Intermittent demand: Linking forecasting to inventory obsolescence | 2011 | EJOR | https://doi.org/10.1016/j.ejor.2011.05.018 |
| 18 | On the categorization of demand patterns | 2005 | JORS | https://doi.org/10.1057/palgrave.jors.2601841 |
| 19 | Optimising forecasting models for inventory planning | 2020 | IJPE | https://doi.org/10.1016/j.ijpe.2019.107597 |

> **Lưu ý định vị:** Bài 11 (Wang, Kang, Spiliotis & Petropoulos, 2026) là bài gần nhất: cũng dùng M5, cũng đặt mức order-up-to bằng phân vị τ theo newsvendor, và cũng đo chi phí tồn/thiếu hàng. Đã kiểm tra PDF: họ đánh giá **từng kỳ độc lập** (không lead time, không mang tồn kho sang kỳ sau), **không có thanh lý**, **không phân tích theo loại nhu cầu** và **không dùng LightGBM**. Đề tài của nhóm khác biệt ở bốn điểm: (1) mô phỏng tồn kho nhiều kỳ có lead time; (2) quyết định **hai chiều** nhập hàng + thanh lý; (3) phân tích theo nhóm ADI–CV²; (4) một mô hình LightGBM quantile gọn thay vì kết hợp nhiều mô hình.
