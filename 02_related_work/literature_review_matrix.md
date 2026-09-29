# Literature Review Matrix

Chi tiết từng bài, kèm **số trang nguồn cho từng ý**, xem `paper_summaries/paper_XX.md`.

**Cột "Kiểm chứng":**

- ✅ = đã đọc toàn văn.
- ⚠️ = chỉ đọc được abstract. Các ô có dấu `*` là thông tin chưa kiểm chứng từ chính bài đó, xem file tóm tắt.
- Nội dung cột **Relevance** là **nhận định của nhóm**.
- `†` = lấy từ tóm tắt do người dùng cung cấp, **chưa đối chiếu PDF**.

| No | Paper Title | Year | Venue | Kiểm chứng | Domain | AI Method | Dataset | Metrics | Main Contribution | Limitation | Relevance to Our Topic |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | The M5 competition: Background… | 2022 | IJF | ✅ | Bán lẻ | Không đề xuất mô hình | 42.840 chuỗi / 12 cấp; 30.490 product–store; 73% intermittent, 17% lumpy, 3% erratic, 7% smooth | WRMSSE, WSPL | Mô tả tổ chức M5; phân loại ADI–CV² (ngưỡng 0,5 và 4/3) | Khó khái quát ngoài dữ liệu M5 (tác giả nêu) | Rất cao: dataset + tỷ lệ nhóm nhu cầu |
| 02 | M5 accuracy competition: Results… | 2022 | IJF | ✅ | Bán lẻ | LightGBM (cả top 50); đội thắng: 220 LightGBM + Tweedie | M5; 5.507 đội | WRMSSE | Đội thắng tốt hơn benchmark tốt nhất 22,4%; ES vẫn cạnh tranh ở cấp product–store | Chỉ phân tích top 50; ít đội chia sẻ chi tiết | Rất cao: căn cứ chọn LightGBM |
| 03 | M5 uncertainty competition: Results… | 2022 | IJF | ✅ | Bán lẻ | Đội thắng: **LightGBM riêng cho từng phân vị** (126 mô hình) | M5, 9 phân vị; 892 đội | WSPL | ML/LightGBM dẫn đầu cả nhánh Uncertainty; phân vị cao dùng cho safety stock (tr. 2) | **M5 không gắn với bài toán ra quyết định cụ thể** (tác giả nêu, tr. 2–3) | Rất cao: **ủng hộ LightGBM quantile** |
| 04 | Interpretability and Control in FSS | 2026 | HICSS | ✅ (arXiv) | Hệ thống hỗ trợ dự báo | Prophet + 3 thiết kế FSS | 10 chuỗi M5 FOODS; 230 người (arXiv) / 197 (HICSS) | Lượng chỉnh sửa, sai số, hài lòng | Minh bạch giảm chỉnh sửa có hại | Người dùng quá tải nếu thiếu đào tạo | TB: thiết kế dashboard |
| 05 | Balancing Strategy for Counterfactual… | 2024 | ICML | ✅ | Nhân quả | CT, CRN, RMSN, GNET, MSM + CDC/AGR/PCB | Tumor, MIMIC-III, M5 (giá = treatment) | RMNSE | Cân bằng không cải thiện trên M5 | Không có ground-truth phản thực tế | Thấp |
| 06 | Foundation Models … Dual-Strategy Ensembling | 2025 | KDD'25 WS | ✅ | Bán lẻ / supply chain | HE + AE trên LightGBM, DNN, DeepAR, PatchTST, TEMPO, Chronos | M5 + 3 dataset ngoài | WRMSSE | HE cải thiện mọi backbone (vd DeepAR 0,5556→0,5233) | Khó diễn giải ensemble; trọng số bằng nhau | TB–cao |
| 07 | The Forecast Critic | 2025 | AAAI'26 WS | ✅ | Giám sát dự báo | LLM | 1.000 chuỗi M5 + Chronos; dữ liệu tổng hợp | F1, sCRPS | LLM phát hiện dự báo kém (F1 0,88) | Kém người; khó với chu kỳ giãn/nén | Thấp–TB |
| 08 | The cost of ensembling | 2025 | arXiv | ✅ | Bán lẻ | 10 mô hình global, 8 ensemble | M5, VN1 | RMSSE, SQL/SMQL, chi phí | Ensemble 2–3 mô hình đã gần tối ưu | Chỉ 2 dataset; giả định không drift; trung bình đơn giản | TB–cao |
| 09 | Hierarchical TSF via Latent Mean Encoding | 2025 | arXiv | ✅ | Bán lẻ | Encoder–decoder phân cấp | M5 (1886/28/28) | WRMSSE, RMSE, MFEV, MAD | WRMSSE 0,620 so với TSMixer-Ext 0,640 | Baseline lấy lại từ bài khác; chỉ M5 | TB |
| 10 | CLEF | 2025 | ICLR'26 | ✅ | Y sinh (+ bán lẻ) | Controllable sequence editing | 8 dataset; M5 chia CA/TX/WI | MAE | MAE cải thiện TB 16,28% / 26,73%, tới 62,84% | Không có ground-truth nhân quả | Thấp |
| 11 | Multi-objective prob. forecast combination for inventory | 2026 | arXiv | ✅ | **Tồn kho** | MOO (NSGA-III) kết hợp WSS, ZV, Poisson, NB | M5 (28.903 chuỗi), RAF | DRPS, Cost, Holding, Stockout | Cân bằng độ chính xác & quyết định | **Tự nêu: newsvendor 1 kỳ, 1 sản phẩm**; tốn tính toán; cửa sổ cố định | **Rất cao: bài gần nhất** |
| 12 | Intermittent TSF: local vs global | 2026 | arXiv | ✅ | Nhu cầu rời rạc | Local vs global (TiDE, DeepAR, …, LightGBM distributional) | 5 dataset, >40k chuỗi | sQL (5 phân vị), RMSSE | TiDE + Tweedie tốt nhất; **LightGBM xác suất không cạnh tranh** | Chưa có kiến trúc chuẩn; chưa so foundation model | Rất cao, **phản biện lựa chọn LightGBM** |
| 13 | e2eTD probabilistic top-down | 2026 | arXiv | ✅ | Bán lẻ | ETS cho chuỗi tổng hợp + top-down sampling | M5, Favorita | WSPL, thời gian chạy | Hạng 11/892 M5-U; <5 phút trên laptop | Chọn chuỗi tổng hợp thủ công | Cao |
| 14 | LightGBM | 2017 | NeurIPS | ✅ | Tổng quát | GBDT (GOSS, EFB) | Allstate, Flight Delay, KDD10, KDD12 | Thời gian, độ chính xác | Nhanh hơn GBDT tới >20× | Không bàn chuỗi thời gian (nhận định) | Mô hình chính |
| 15 | Croston's method | 1972 | JORS (ORQ) | ⚠️ (+ bài 23) | Tồn kho | Ước lượng riêng kích thước & tần suất | * | * | Khắc phục SES với nhu cầu rời rạc | Lệch dương; không xử lý lỗi thời (theo bài 16) | Baseline |
| 16 | TSB – linking forecasting to obsolescence | 2011 | EJOR | ⚠️ (+ bài 23) | **Tồn kho** | TSB: cập nhật xác suất nhu cầu mỗi kỳ | **Mô phỏng** | * | Không lệch; nối dự báo với lỗi thời | Chỉ mô phỏng (theo abstract) | Rất cao: cơ sở cho THANH LÝ |
| 17 | DeepAR | 2020 | IJF | ✅ (arXiv) | Bán lẻ / tổng quát | RNN tự hồi quy toàn cục, xác suất | parts, electricity, traffic, ec, ec-sub | ρ-risk (quantile loss) | Cải thiện ~15% so với SOTA lúc đó | Không do tác giả nêu | Baseline nên thêm |
| 18 | Categorization of demand patterns | 2005 | JORS | ⚠️ (+ bài 01, 23) | **Tồn kho** | Phân loại theo ADI & CV²; EWMA, Croston, SBA | 3.000 chuỗi ô tô | MSE lý thuyết | Quy tắc chọn phương pháp theo ADI–CV² | Ngưỡng 1,32 không phải định nghĩa tính rời rạc (theo bài 12) | Rất cao: khung phân tích |
| 19 | Optimising forecasting models for inventory planning | 2020 | IJPE | ⚠️ (trang mô tả + tóm tắt người dùng†) | **Tồn kho** | Tối ưu tham số dự báo theo metric tồn kho qua vòng mô phỏng tồn kho† | 229 SKU hàng tiêu dùng, theo tuần, 173 quan sát/SKU, lead time 3–5 tuần† | Bias, mức phục vụ, tồn kho, độ chính xác† | Sai số tăng ~9% nhưng bias ngoài mẫu cải thiện ~62%†; MSE nhỏ nhất ≠ chi phí tồn kho nhỏ nhất† | * | Rất cao; **phải đối chiếu PDF trước khi trích số** |
| 20 | Forecast accuracy and inventory performance… M5 | 2025 | EJOR | ❌ | **Tồn kho + M5** | * | M5* | * | * | * | **Có thể trùng hướng, bắt buộc đọc** |
| 21 | Multi-algorithm optimization for inventory analytics | 2025 | SCA | ✅ | **Tồn kho + M5** | LSTM + GA–DQN; so với RL, GA, ML, heuristic | Tập con thực phẩm biến động mạnh của M5; mô phỏng 365 ngày | TIC, service level, stockout, bullwhip; MAE, RMSE, MAPE | Service level 61% → 94% | Lead time cố định; RL tốn kém, khó giải thích (tác giả nêu); không có thanh lý, không phân loại ADI–CV² | Rất cao: **đã có mô phỏng tồn kho nhiều kỳ trên M5** |
| 22 | Hybrid learning framework… adaptive inventory planning | 2026 | SCA | ✅ | Bán lẻ + M5 | XGBoost + LightGBM + LSTM-GRU stacking + GARCH | 8.000 chuỗi bán nhiều của M5 | R², RMSE, MAE, MAPE (theo ngành hàng) | R² 0,968; safety stock theo GARCH giảm chi phí tồn kho kỳ vọng 11,8% (1 phép tính minh họa, tr. 15) | **Không đánh giá chuỗi thưa/chậm, "điểm yếu chính"** (tác giả nêu, tr. 4, 18) | Cao: dẫn chứng cho gap chuỗi rời rạc |
| 23 | New approach to forecast intermittent demand… spare parts | 2025 | Appl. Sci. | ✅ | **Tồn kho** (phụ tùng) | Họ Croston (Croston, SBA, TSB…) + SK mới; chính sách (R, Q) | 2.050 SKU ô tô × 104 tuần (không công khai) | sSPEC, MASE, sAPIS; safety stock, backorder | Giảm safety stock ở cùng mức phục vụ | Lead time cố định; 1 ngành (tác giả nêu) | Cao: nguồn thứ cấp cho 15, 16, 18 |
| 24 | Feature engineering for intermittent demand (Z%, NZ%) | 2026 | J. Intell. Manuf. | ✅ | Nhu cầu rời rạc + M5 | GRU, LSTM, TCN + 20 chiến lược đặc trưng | 19 chuỗi M5 (3 mức ADI) | WMAPE, Z%, NZ%; tồn kho, thiếu hàng | Z% ↑ → tồn kho ↓ nhưng thiếu hàng ↑ | Chỉ dự báo điểm (tác giả nêu); 19 chuỗi | TB–cao: MAPE không dùng được; đánh đổi tồn kho–phục vụ |
| 25 | Forecasting critical spare parts… power plant | 2026 | Eng. Proc. | ✅ | Phụ tùng nhà máy điện | RF, XGBoost | 1 nhà máy, dữ liệu tháng 2020–2024 | RMSE, MAE, MAPE (bỏ kỳ bằng 0) | XGBoost tốt hơn RF; tồn cuối kỳ vượt xa safety stock → ước tính tiết kiệm ~2,6 tỷ IDR/năm (tr. 7) | Dữ liệu nhỏ, không phải bán lẻ; không mô phỏng chính sách (nhận định) | Thấp–TB: ví dụ tồn kho dư |

## Tổng hợp (Synthesis)

> Mỗi ý bên dưới ghi rõ bài làm căn cứ. Xem file tóm tắt tương ứng để có số trang.

### 1. Các bài trước đã làm gì?

- **Nhóm M5 (02, 03, 06, 08, 09, 13):** tối ưu **độ chính xác dự báo** (WRMSSE, WSPL, quantile loss). Hướng mới là foundation model và ensemble (06), đánh đổi chi phí (08), dự báo phân cấp (09, 13).
- **Nhóm nhu cầu rời rạc (12, 15, 16, 18, 23, 24):** dữ liệu nhiều số 0 cần phương pháp riêng (Croston, TSB) và phân phối phù hợp (Tweedie cho phân vị cao, bài 12).
- **Nhóm dự báo → tồn kho (11, 16, 19, 20, 21, 22):** bài 21 mô phỏng tồn kho nhiều kỳ trên M5 bằng RL/GA; bài 22 tạo khoảng dự báo cho safety stock; bài 20 nghiên cứu trực tiếp quan hệ độ chính xác–tồn kho trên M5 (chưa đọc được). bài 11 cho thấy tối ưu theo sai số thống kê không đồng nghĩa với quyết định tồn kho tốt nhất (abstract bài 11). Bài 16 nối dự báo với tồn kho lỗi thời. Bài 19 đưa metric tồn kho vào việc tối ưu mô hình dự báo (chỉ từ trang mô tả).

### 2. Model thường dùng

- Thống kê: ETS (13), Croston/SBA/TSB (15, 16, 18), mô hình phân phối Poisson/NB (11).
- Machine learning / deep learning: LightGBM (02, 03, 06, 08, 12), DeepAR (06, 09, 12, 17), TiDE, DLinear, PatchTST (06, 12), foundation model Chronos, TEMPO (06, 07).

### 3. Metric thường dùng

- Dự báo điểm: WRMSSE, RMSSE (02, 06, 08, 09, 12).
- Dự báo xác suất: WSPL / scaled quantile loss (03, 08, 12, 13), DRPS (11), sCRPS (07).
- Tồn kho:
  - **Mô phỏng/đánh giá chính sách có hệ thống:** bài 11 (total cost, holding, stockout), bài 21 (TIC, service level, stockout rate, bullwhip), bài 23 (safety stock, backorder ở mức phục vụ cho trước).
  - **Chỉ phân tích phụ/minh họa:** bài 22 (một phép tính chi phí kỳ vọng, tr. 15), bài 24 (tương quan Z%/NZ% với mức tồn kho và thiếu hàng, tr. 21), bài 25 (ước tính tiết kiệm chi phí lưu kho, tr. 7).
- **Không dùng MAPE.** MAPE không xác định khi nhu cầu thực bằng 0 (bài 24, tr. 4); M5 có ~60,1% quan sát bằng 0 (bài 11, tr. 16). Bài 25 phải loại các kỳ bằng 0 khỏi MAPE (abstract), còn bài 21 (Bảng 2, tr. 6) và bài 22 (tr. 13) vẫn dùng MAPE, là điểm yếu có thể phê bình.

### 4. Khoảng trống (gap), đầu vào cho Bước 5 (**đã cập nhật sau khi đọc bài 21–22**)

Các gap cũ không còn đứng được:

- ~~"Chỉ bài 11 đánh giá bằng metric tồn kho trên M5"~~: bài 21 cũng làm.
- ~~"Chưa có mô phỏng tồn kho nhiều kỳ trên M5"~~: bài 21 đã mô phỏng 365 ngày với điểm đặt hàng lại và safety stock (tr. 8).
- ⚠️ Bài 20 (EJOR 2025) có tên bài trùng câu hỏi "độ chính xác dự báo ↔ hiệu quả tồn kho trên M5". **Chưa đọc được**, nên không thể khẳng định RQ này còn mới.

Các gap còn đứng được (đã có dẫn chứng):

1. **Tầng quyết định tồn kho vốn nằm ngoài phạm vi của M5.** Chính nhóm tổ chức M5 viết rằng cuộc thi không tập trung vào một bài toán ra quyết định cụ thể (bài 03, tr. 2–3).
2. **Chuỗi rời rạc bị loại hoặc chọn lọc bỏ.** Bài 22 chỉ dùng 8.000 chuỗi bán nhiều, tự nêu thiếu chuỗi thưa/chậm là "điểm yếu chính" (tr. 4, 18), và đề xuất hướng tương lai là chuỗi rời rạc cùng quantile regression (tr. 18–19), trùng với cách tiếp cận của đề tài. Bài 21 chỉ dùng tập con thực phẩm biến động mạnh (tr. 8). Bài 11 loại 1.587 chuỗi không có lịch sử (tr. 17). Trong khi đó, 73% chuỗi M5 là intermittent (bài 01, tr. 8).
3. **Không có quyết định thanh lý / xử lý hàng dư.** Đã tìm các từ khóa liquidation, markdown, clearance, salvage, disposal, write-off, obsolete trong toàn văn bài 11, 21, 22, 23, 24, 25: các từ này chỉ xuất hiện trong phần tài liệu tham khảo hoặc bảng tổng quan, **không bài nào có quyết định thanh lý**. Bài 25 ghi nhận tồn kho dư kéo dài (tr. 7) nhưng không đề xuất cách xử lý. Bài 16 (abstract) liên hệ dự báo với tồn kho lỗi thời nhưng chỉ dùng dữ liệu mô phỏng.
4. **Chưa có phân tích KPI tồn kho theo nhóm ADI–CV².** Bài 01 phân loại M5 nhưng chỉ nhằm mô tả dữ liệu (tr. 8). Bài 22 báo cáo tỷ lệ các nhóm (tr. 4) và sai số theo ngành hàng (tr. 13), nhưng phép tính chi phí tồn kho là tổng hợp (tr. 15). Bài 24 phân tích theo 3 mức ADI, nhưng chỉ có 19 chuỗi và dự báo điểm (tr. 8, 26).
5. **Minh bạch và dễ giải thích.** Bài 21 dùng RL và tự nêu DRL/DL khó diễn giải (tr. 19); bài 06 nêu ensemble khó giải thích (tr. 7). Chính sách dựa trên phân vị dự báo (newsvendor/order-up-to) thì minh bạch hơn. (Nhận định nhóm, cần lập luận thêm.)

Về mô hình, có hai bằng chứng trái chiều về LightGBM xác suất:

- Bài 03 (tr. 14): lời giải hạng nhất M5 Uncertainty là LightGBM **theo từng phân vị**.
- Bài 12 (tr. 13, 19): LightGBM **dạng distributional** không cạnh tranh; TiDE + Tweedie tốt nhất.
- Đề tài dùng cách giống bài 03, và nên có TiDE hoặc DeepAR làm baseline.
