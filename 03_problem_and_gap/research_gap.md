# Research Gap

> Quy ước nguồn: `(bài X, tr. N)` theo `02_related_work/paper_list.md`; `[DP]` = `code/outputs/data_profile.md`. Bài 20 (Theodorou et al., 2025) và bài W3 (mục 1.2) **không dùng làm căn cứ** vì không đọc được nội dung.

## 1. Các bài trước đã giải quyết như thế nào?

### 1.1. Các bài trong danh sách chính thức

| Nhóm | Bài | Đã làm gì |
|---|---|---|
| Dự báo trên M5 (và VN1) | 02, 03, 06, 08, 09, 13 | Tối ưu độ chính xác (WRMSSE, WSPL). Bài 08 dùng cả **M5 và VN1** nhưng chỉ đánh giá độ chính xác và chi phí tính toán của ensemble (tr. 4, 13–14). LightGBM được cả top 50 M5 Accuracy dùng (bài 02, tr. 1); lời giải hạng nhất M5 Uncertainty là LightGBM theo từng phân vị (bài 03, tr. 14). Hướng mới: foundation model, ensemble (06), đánh đổi chi phí (08), dự báo phân cấp (09, 13). |
| Nhu cầu rời rạc | 12, 15, 16, 18, 23, 24 | Croston/SBA/TSB, phân loại ADI–CV², phân phối phù hợp (Tweedie cho phân vị cao, bài 12). |
| Dự báo → tồn kho | 11, 16, 19, 21, 22, 23, 24 | **Bài 11:** kết hợp dự báo xác suất, đánh giá theo newsvendor. **Bài 21:** mô phỏng tồn kho 365 ngày trên tập con M5 (LSTM + GA–DQN). **Bài 22:** khoảng dự báo GARCH cho safety stock. **Bài 23:** dự báo nhu cầu rời rạc + chính sách (R, Q) cho phụ tùng. **Bài 24:** độ chính xác ở kỳ bằng 0 ảnh hưởng ngược chiều tới tồn kho và thiếu hàng. |

### 1.2. Các nghiên cứu gần hướng, tìm thêm khi làm Bước 5 (29/09–08/10/2026)

| Mã | Công trình | Mức đã đọc | Khác biệt với đề tài |
|---|---|---|---|
| W1 | van der Haar, Wellens, Boute, Basten (2024). *Supervised learning for integrated forecasting and inventory control*. EJOR. doi:10.1016/j.ejor.2024.07.004 | Abstract + phần mở đầu (bản preprint KU Leuven) | Học **trực tiếp** quyết định đặt hàng bằng hàm mất mát tùy chỉnh (end-to-end), thử trên lost sales, hàng dễ hỏng, dual sourcing. Đề tài dùng hướng **dự báo → chính sách** minh bạch và có thanh lý; W1 có thể làm baseline nâng cao |
| W2 | de Sousa, A. G. P. (2026). *From Demand Forecasting to Replenishment Simulation: A Data-Driven Machine Learning Approach for Fashion Retail*. Luận văn, Đại học Porto | Abstract | Bối cảnh vận hành của **một** nhà bán lẻ phụ kiện thời trang toàn cầu; XGBoost/LightGBM (hurdle) + safety factor; mô phỏng nhập hàng so với hệ thống đang chạy. Theo abstract: không nhắc tới thanh lý, không so sánh nhiều dataset (chưa đọc toàn văn để khẳng định) |
| W3 | Li, P. (2026). *Forecasting for Inventory Decisions: A Decision-regret Benchmark for Perishability-aware Multi-Echelon Retail Replenishment using the M5/Walmart Data*. SSRN. doi:10.2139/ssrn.7051299 | ⛔ **Chỉ tên bài** (SSRN chặn, OpenAlex không có abstract) | Theo **tên bài**: benchmark quyết định trên M5, có xét hàng dễ hỏng và **nhiều cấp**. Không dùng làm căn cứ; khi viết chỉ trích ở mức tên bài |

## 2. Các bài trước còn hạn chế gì?

1. **Tầng quyết định nằm ngoài phạm vi của M5.** Nhóm tổ chức M5 viết rằng cuộc thi không tập trung vào một bài toán ra quyết định cụ thể (bài 03, tr. 2–3). Các bài dự báo trên M5 (02, 03, 06, 08, 09, 13) đánh giá bằng sai số dự báo.
2. **Chuỗi rời rạc bị chọn lọc bỏ trong các nghiên cứu gắn với tồn kho trên M5.** Bài 22 chỉ dùng 8.000 chuỗi bán nhiều, tự nêu là "điểm yếu chính" (tr. 4, 18); bài 21 chỉ dùng tập con thực phẩm biến động mạnh (tr. 8); bài 24 chỉ dùng 19 chuỗi (tr. 8). Trong khi đó, 73% chuỗi M5 là intermittent (bài 01, tr. 8). *(Bài 11 giữ chuỗi rời rạc, chỉ loại 1.587 chuỗi chưa có lịch sử, tr. 17.)*
3. **Không có quyết định thanh lý.** Tìm các từ khóa liquidation, markdown, clearance, salvage, disposal, write-off, obsolete trong toàn văn bài 11, 21, 22, 23, 24, 25: chỉ xuất hiện ở phần tài liệu tham khảo, không bài nào có quyết định thanh lý. W1, W2 (theo abstract) cũng không đề cập. Bài 16 liên hệ dự báo với tồn kho lỗi thời nhưng chỉ dùng mô phỏng (abstract).
4. **Thiếu KPI tồn kho theo nhóm ADI–CV².** Bài 01 phân loại M5 chỉ để mô tả (tr. 8); bài 22 báo cáo tỷ lệ các nhóm (tr. 4) nhưng phép tính chi phí tồn kho là tổng hợp (tr. 15); bài 24 phân tích theo mức ADI nhưng chỉ 19 chuỗi và dự báo điểm (tr. 8, 26).
5. **Đánh giá tầng quyết định chỉ trên một loại hình bán lẻ.** Các bài gắn với tồn kho trên M5 (11, 21, 22, 24) chỉ dùng dữ liệu Walmart (bài 11 thêm phụ tùng Không quân Anh, không phải bán lẻ). Bài 22 tự nêu chỉ thử trên M5, một môi trường bán lẻ ở Mỹ (tr. 17); nhóm tổ chức M5 cũng thừa nhận giới hạn khái quát hóa (bài 01, tr. 11). Bài 08 có dùng M5 + VN1 nhưng **chỉ đánh giá độ chính xác**; bài chỉ nhắc rằng phân vị cao quan trọng cho safety stock (tr. 14), không mô phỏng tồn kho.
6. **Chính sách khó giải thích.** Bài 21 dùng RL và tự nêu DRL/DL khó diễn giải (tr. 19); bài 06 nêu ensemble khó giải thích (tr. 7). Chính sách dựa trên phân vị dự báo minh bạch hơn (nhận định nhóm).
7. **Hạn chế của bài gần nhất (bài 11):** chỉ xét **newsvendor một kỳ, một sản phẩm** (tác giả tự nêu, tr. 26).

## 3. Nhóm sẽ cải tiến điểm nào?

| Cải tiến | Gap | Mức độ mới |
|---|---|---|
| **Benchmark tầng quyết định trên hai loại hình bán lẻ** (M5: cửa hàng vật lý; VN1: TMĐT nhiều nhà bán) với cùng một quy trình | 5 | **Điểm mới chính** (bài 08 đã dùng cặp dataset này nhưng chỉ cho độ chính xác) |
| Giữ lại **toàn bộ nhóm nhu cầu** và báo cáo KPI tồn kho **theo nhóm ADI–CV²** | 2, 4 | **Điểm mới chính** |
| Bổ sung **quyết định thanh lý** dựa trên phân vị dự báo | 3 | **Điểm mới chính** |
| **Đánh giá không phụ thuộc chi phí tuyệt đối**: theo mức phục vụ mục tiêu, đường đánh đổi tồn kho – fill rate, ngưỡng giá thu hồi hòa vốn của thanh lý | 1, 3 | Điểm cộng phương pháp (giảm phụ thuộc vào giả định) |
| Đánh giá ở tầng quyết định (KPI tồn kho) | 1 | Có tiền lệ (bài 11, 21; W1–W3), không phải điểm mới độc lập |
| Mô phỏng nhiều kỳ có lead time | 7 | So với bài 11 là mới; bài 21 và W1 đã có, **không** phải điểm mới độc lập |
| Phương pháp dự báo: LightGBM quantile + baseline thống kê + mô hình sâu | 6 | Lựa chọn thiết kế, **không** phải thuật toán mới |

## 4. Đóng góp dự kiến

1. **Benchmark công khai, tái lập được** "từ dự báo đến quyết định" trên **hai dataset bán lẻ công khai** (M5, VN1) ở cùng tần suất tuần, với mã nguồn mở.
2. **Lớp quyết định minh bạch** gồm nhập hàng (order-up-to theo phân vị) và **thanh lý** (theo phân vị dài hạn), đánh giá bằng KPI tồn kho.
3. **Phân tích theo nhóm ADI–CV²** trên cả hai dataset: phương pháp nào hiệu quả ở nhóm nào, và xếp hạng có giữ nguyên khi đổi miền không.
4. **Cách đánh giá không phụ thuộc chi phí tuyệt đối** (mức phục vụ mục tiêu, đường đánh đổi, ngưỡng hòa vốn thanh lý) và phân tích theo kịch bản lead time.
5. (Phụ lục) Mô tả một **dataset bán lẻ giày dép Việt Nam** ít được khai thác, kèm cảnh báo về tính đầy đủ của dữ liệu.

## 5. Câu phát biểu gap (English)

> Most studies on public retail benchmarks such as M5 and VN1 optimise forecast accuracy, as the M5 competition itself did not target a specific decision-making problem. The few works that link forecasts to inventory decisions restrict the analysis to selected high-volume or volatile series, consider a single-period newsvendor setting, omit liquidation decisions, or use a single retail setting. Limited attention has been given to benchmarking probabilistic forecasting methods under a common, transparent replenishment-and-liquidation policy across different retail settings, while retaining intermittent and lumpy demand and reporting cost-free inventory KPIs by demand class.

| Vế trong câu gap | Nguồn |
|---|---|
| "competition itself did not target a specific decision-making problem" | Bài 03, tr. 2–3 |
| "selected high-volume or volatile series" | Bài 22 (tr. 4); bài 21 (tr. 8) |
| "single-period newsvendor setting" | Bài 11, tr. 26 |
| "omit liquidation decisions" | Tìm từ khóa trong toàn văn bài 11, 21–25 |
| "use a single retail setting" | Bài 22 (tr. 17); bài 21, 24 chỉ dùng M5; bài 01 (tr. 11) |
| "M5 and VN1 … optimise forecast accuracy" | Bài 02, 03 (M5); bài 08 dùng M5 + VN1, chỉ đánh giá độ chính xác (tr. 13–14) |
| "retaining intermittent and lumpy demand" | M5: 73% intermittent + 17% lumpy theo ngày (bài 01, tr. 8); theo tuần: M5 và VN1 [DP] |

## 6. Lưu ý khi viết bài

- **Không** viết "no study has examined…". Bài 20 và W3 có thể đã làm một phần (benchmark quyết định trên M5). Dùng "limited attention" / "to the best of our knowledge".
- Trước khi nộp, **cố đọc W3** (SSRN) và bài 20; nếu W3 đã có thanh lý hoặc phân tích theo nhóm nhu cầu thì phải định vị lại.
- Bài 08, 09, 11, 12, 13 và W3 chưa qua phản biện; kiểm tra xem đã được xuất bản chính thức chưa trước khi nộp.
- VN1: trích dẫn Vandeput (2024), *VN1 Forecasting – Accuracy Challenge*, DataSource.ai (như bài 08). Lưu ý "VN1" **không** phải dữ liệu Việt Nam.
- Dataset Việt Nam (phụ lục): nêu rõ nghi ngờ dữ liệu doanh số chưa đầy đủ ("split_1") và giấy phép chưa rõ. Tìm "Vietnam Datathon 2023" trên OpenAlex (06/10/2026) không ra bài nào dùng dataset này.
