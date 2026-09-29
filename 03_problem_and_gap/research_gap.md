# Research Gap

> Số trang `(tr. N)` và số bài theo `02_related_work/paper_list.md`; chi tiết trong `02_related_work/paper_summaries/` và `literature_review_matrix.md`. Bài 20 (Theodorou et al., 2025) **không dùng làm căn cứ** vì không đọc được toàn văn.

## 1. Các bài trước đã giải quyết như thế nào?

| Nhóm | Bài | Đã làm gì |
|---|---|---|
| Dự báo trên M5 | 02, 03, 06, 08, 09, 13 | Tối ưu độ chính xác (WRMSSE, WSPL). LightGBM được cả top 50 M5 Accuracy dùng (bài 02, tr. 1); lời giải hạng nhất M5 Uncertainty là LightGBM theo từng phân vị (bài 03, tr. 14). Hướng mới: foundation model và ensemble (06), đánh đổi chi phí (08), dự báo phân cấp (09, 13). |
| Nhu cầu rời rạc | 12, 15, 16, 18, 23, 24 | Croston/SBA/TSB, phân loại ADI–CV², phân phối phù hợp (Tweedie cho phân vị cao, bài 12). |
| Dự báo → tồn kho | 11, 16, 19, 21, 22, 23, 24 | **Bài 11:** kết hợp dự báo xác suất bằng tối ưu đa mục tiêu, đánh giá theo newsvendor. **Bài 21:** mô phỏng tồn kho 365 ngày trên tập con M5 bằng LSTM + GA–DQN. **Bài 22:** khoảng dự báo thích nghi (GARCH) cho safety stock. **Bài 23:** dự báo nhu cầu rời rạc + chính sách (R, Q) cho phụ tùng. **Bài 24:** độ chính xác ở các kỳ bằng 0 ảnh hưởng ngược chiều tới tồn kho và thiếu hàng. |

## 2. Các bài trước còn hạn chế gì?

1. **Tầng quyết định nằm ngoài phạm vi của M5.** Chính nhóm tổ chức M5 viết rằng cuộc thi không tập trung vào một bài toán ra quyết định cụ thể và không định nghĩa tham số của bài toán đó (bài 03, tr. 2–3). Các bài dự báo trên M5 (02, 03, 06, 08, 09, 13) vì vậy đánh giá bằng sai số dự báo.
2. **Chuỗi rời rạc bị chọn lọc bỏ trong các nghiên cứu gắn với tồn kho trên M5.**
   - Bài 22 chỉ dùng 8.000 chuỗi bán nhiều và tự nêu thiếu chuỗi thưa/chậm là "điểm yếu chính" (tr. 4, 18).
   - Bài 21 chỉ dùng tập con thực phẩm biến động mạnh (tr. 8).
   - Bài 24 chỉ dùng 19 chuỗi M5 (tr. 8).
   - Trong khi đó, 73% chuỗi M5 là intermittent (bài 01, tr. 8).
   - Lưu ý: bài 11 **giữ** chuỗi rời rạc (M5 có ~60,1% quan sát bằng 0, tr. 16), chỉ loại 1.587 chuỗi chưa có lịch sử bán (tr. 17).
3. **Không có quyết định thanh lý.** Đã tìm các từ khóa liquidation, markdown, clearance, salvage, disposal, write-off, obsolete trong toàn văn bài 11, 21, 22, 23, 24, 25: chỉ xuất hiện ở phần tài liệu tham khảo, không bài nào có quyết định thanh lý. Bài 16 liên hệ dự báo với tồn kho lỗi thời nhưng chỉ dùng thí nghiệm mô phỏng (abstract).
4. **Thiếu KPI tồn kho theo nhóm ADI–CV².**
   - Bài 01 phân loại M5 chỉ để mô tả dữ liệu (tr. 8).
   - Bài 22 báo cáo tỷ lệ các nhóm (tr. 4), nhưng phần tồn kho chỉ là **một phép tính chi phí tổng hợp** (safety stock theo GARCH giảm chi phí kỳ vọng 11,8%, tr. 15), không tách theo nhóm.
   - Bài 24 phân tích theo 3 mức ADI, nhưng chỉ có 19 chuỗi và dự báo điểm (tr. 8, 26).
5. **Chính sách khó giải thích.** Bài 21 dùng RL và tự nêu DRL/DL khó diễn giải (tr. 19); bài 06 nêu kết quả ensemble khó giải thích (tr. 7). Chính sách dựa trên phân vị dự báo (newsvendor/order-up-to) minh bạch hơn (nhận định của nhóm).
6. **Hạn chế của bài gần nhất (bài 11).** Tác giả tự nêu: bài chỉ xét **newsvendor một kỳ, một sản phẩm**, nên hạn chế khi áp dụng cho hệ nhiều kỳ hoặc nhiều cấp (tr. 26). Bài cũng tốn chi phí tính toán do NSGA-III, và dùng cửa sổ validation cố định (tr. 26).

## 3. Nhóm sẽ cải tiến điểm nào?

| Cải tiến | Gap tương ứng | Mức độ mới |
|---|---|---|
| Giữ lại **toàn bộ nhóm nhu cầu** (kể cả intermittent và lumpy) và báo cáo KPI tồn kho **theo từng nhóm ADI–CV²** | 2, 4 | **Điểm mới chính** |
| Bổ sung **quyết định thanh lý** dựa trên phân vị dự báo, bên cạnh quyết định nhập hàng | 3 | **Điểm mới chính** |
| Đánh giá chính sách ở tầng quyết định (KPI tồn kho), không chỉ sai số dự báo | 1 | Có tiền lệ (bài 11, 21), nhưng chưa làm trên toàn bộ các nhóm nhu cầu |
| Mô phỏng tồn kho **nhiều kỳ có lead time**, tồn kho mang sang kỳ sau | 6 | So với bài 11 là mới; **bài 21 đã có mô phỏng nhiều kỳ trên M5**, nên không phải điểm mới độc lập |
| Dùng **LightGBM quantile** (giống cách của lời giải hạng nhất M5 Uncertainty, bài 03, tr. 14), so với baseline thống kê (ETS, TSB) và mô hình sâu (TiDE/DeepAR), thay vì kết hợp nhiều mô hình | 5, 6 | Lựa chọn thiết kế; cần kiểm chứng vì bài 12 cho thấy LightGBM dạng distributional kém trên dữ liệu rời rạc (tr. 13, 19) |

## 4. Đóng góp dự kiến của nhóm

1. Một pipeline **minh bạch** từ dự báo phân vị (LightGBM) tới khuyến nghị **nhập hàng / giữ nguyên / thanh lý** cho từng SKU–store trên M5.
2. Đánh giá thực nghiệm bằng **KPI tồn kho** (fill rate, tỷ lệ hết hàng, tồn dư, chi phí) trong mô phỏng nhiều kỳ, **giữ lại toàn bộ chuỗi rời rạc**.
3. Phân tích **theo nhóm ADI–CV²**: nhóm nào dự báo xác suất mang lại lợi ích rõ nhất, nhóm nào baseline thống kê (TSB) vẫn đủ tốt.
4. Phân tích **độ nhạy** theo tỷ lệ chi phí c_u/c_o và lead time, vì M5 không có dữ liệu tồn kho thực.

## 5. Câu phát biểu gap (English)

> Existing studies on the M5 dataset mainly optimise point or probabilistic forecast accuracy, as the competition itself did not target a specific decision-making problem. The few works that link forecasts to inventory decisions either restrict the analysis to selected high-volume or volatile series, evaluate a single-period newsvendor setting, or omit liquidation decisions. Limited attention has been given to evaluating quantile-based replenishment and liquidation policies in a multi-period simulation that retains intermittent and lumpy demand and reports inventory KPIs by demand class.

Nguồn cho từng vế:

| Vế trong câu gap | Nguồn |
|---|---|
| "the competition itself did not target a specific decision-making problem" | Bài 03, tr. 2–3 |
| "selected high-volume or volatile series" | Bài 22 (tr. 4); bài 21 (tr. 8) |
| "single-period newsvendor setting" | Bài 11, tr. 26 |
| "omit liquidation decisions" | Tìm từ khóa trong toàn văn bài 11, 21–25 |
| "retains intermittent and lumpy demand" | 73% intermittent + 17% lumpy trong M5 (bài 01, tr. 8) |

## 6. Lưu ý khi viết bài

- Bài 08, 09, 11, 12, 13 mới chỉ có trên arXiv, chưa qua phản biện. Đặc biệt **bài 11 là bài gần nhất** nên khi nộp cần kiểm tra xem bài đã được xuất bản chính thức chưa.
- **Không** viết câu "no study has examined the relationship between forecast accuracy and inventory performance on M5", vì bài 20 (Theodorou et al., 2025) có thể đã làm việc này.
- Dùng "limited attention" hoặc "to the best of our knowledge" thay cho "no study".
