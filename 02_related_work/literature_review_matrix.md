# Literature Review Matrix

Chi tiết từng bài, kèm **số trang nguồn cho từng ý**, xem `paper_summaries/paper_XX.md`.

**Cột "Kiểm chứng":**

- ✅ = đã đọc toàn văn.
- ⚠️ = chỉ đọc được abstract. Các ô có dấu `*` là thông tin chưa kiểm chứng từ chính bài đó, xem file tóm tắt.
- Nội dung cột **Relevance** là **nhận định của nhóm**.

| No | Paper Title | Year | Venue | Kiểm chứng | Domain | AI Method | Dataset | Metrics | Main Contribution | Limitation | Relevance to Our Topic |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | The M5 competition: Background… | 2022 | IJF | ⚠️ | Bán lẻ | Không đề xuất mô hình | M5: 42.840 chuỗi Walmart | WRMSSE, WSPL* | Mô tả tổ chức cuộc thi M5 (Accuracy + Uncertainty) | Dataset không có tồn kho/chi phí (nhận định nhóm) | Cao: nguồn mô tả dataset |
| 02 | M5 accuracy competition: Results… | 2022 | IJF | ⚠️ | Bán lẻ | Phương pháp các đội thắng*; LightGBM phổ biến* | M5, nộp 30.490 dự báo điểm | WRMSSE* | Tổng kết kết quả nhánh Accuracy | Chưa kiểm chứng* | Rất cao: phải đọc toàn văn trước khi trích |
| 03 | M5 uncertainty competition: Results… | 2022 | IJF | ⚠️ | Bán lẻ | Phương pháp các đội thắng* | M5, 9 phân vị; 892 đội* | WSPL* | Tổng kết nhánh Uncertainty | Chưa kiểm chứng* | Rất cao: phân vị → quyết định |
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
| 15 | Croston's method | 1972 | JORS (ORQ) | ⚠️ | Tồn kho | Ước lượng riêng kích thước & tần suất | * | * | Khắc phục SES với nhu cầu rời rạc | Lệch dương; không xử lý lỗi thời (theo bài 16) | Baseline |
| 16 | TSB – linking forecasting to obsolescence | 2011 | EJOR | ⚠️ | **Tồn kho** | TSB: cập nhật xác suất nhu cầu mỗi kỳ | **Mô phỏng** | * | Không lệch; nối dự báo với lỗi thời | Chỉ mô phỏng (theo abstract) | Rất cao: cơ sở cho THANH LÝ |
| 17 | DeepAR | 2020 | IJF | ✅ (arXiv) | Bán lẻ / tổng quát | RNN tự hồi quy toàn cục, xác suất | parts, electricity, traffic, ec, ec-sub | ρ-risk (quantile loss) | Cải thiện ~15% so với SOTA lúc đó | Không do tác giả nêu | Baseline nên thêm |
| 18 | Categorization of demand patterns | 2005 | JORS | ⚠️ | **Tồn kho** | Phân loại theo ADI & CV²; EWMA, Croston, SBA | 3.000 chuỗi ô tô | MSE lý thuyết | Quy tắc chọn phương pháp theo ADI–CV² | Ngưỡng 1,32 không phải định nghĩa tính rời rạc (theo bài 12) | Rất cao: khung phân tích |
| 19 | Optimising forecasting models for inventory planning | 2020 | IJPE | ⚠️ | **Tồn kho** | Tối ưu tham số dự báo theo metric tồn kho* | Dữ liệu thực* | * | Đưa metric tồn kho vào tối ưu dự báo | * | Rất cao, sau khi đọc toàn văn |

## Tổng hợp (Synthesis)

> Mỗi ý bên dưới ghi rõ bài làm căn cứ. Xem file tóm tắt tương ứng để có số trang.

### 1. Các bài trước đã làm gì?

- **Nhóm M5 (06, 08, 09, 13):** tối ưu **độ chính xác dự báo** (WRMSSE, WSPL, quantile loss). Hướng mới là foundation model và ensemble (06), đánh đổi chi phí (08), dự báo phân cấp (09, 13).
- **Nhóm nhu cầu rời rạc (12, 15, 16, 18):** dữ liệu nhiều số 0 cần phương pháp riêng (Croston, TSB) và phân phối phù hợp (Tweedie cho phân vị cao, bài 12).
- **Nhóm dự báo → tồn kho (11, 16, 19):** bài 11 cho thấy tối ưu theo sai số thống kê không đồng nghĩa với quyết định tồn kho tốt nhất (abstract bài 11). Bài 16 nối dự báo với tồn kho lỗi thời. Bài 19 đưa metric tồn kho vào việc tối ưu mô hình dự báo (chỉ từ trang mô tả).

### 2. Model thường dùng

- Thống kê: ETS (13), Croston/SBA/TSB (15, 16, 18), mô hình phân phối Poisson/NB (11).
- Machine learning / deep learning: LightGBM (06, 08, 12), DeepAR (06, 09, 12, 17), TiDE, DLinear, PatchTST (06, 12), foundation model Chronos, TEMPO (06, 07).

### 3. Metric thường dùng

- Dự báo điểm: WRMSSE, RMSSE (06, 08, 09, 12).
- Dự báo xác suất: WSPL / scaled quantile loss (08, 12, 13), DRPS (11), sCRPS (07).
- Tồn kho: total cost, holding, stockout (11). **Rất ít bài trong danh sách dùng metric tồn kho.**
- MAPE không được bài nào trong danh sách dùng. [Nhận định nhóm] Lý do là M5 có ~60,1% quan sát bằng 0 (bài 11, tr. 16), nên MAPE không xác định.

### 4. Khoảng trống (gap), đầu vào cho Bước 5

1. Trong 13 bài dùng M5, **chỉ bài 11** đánh giá bằng metric tồn kho.
2. Bài 11 **tự thừa nhận** giới hạn ở newsvendor **một kỳ, một sản phẩm**, chưa áp dụng cho hệ nhiều kỳ (bài 11, tr. 26). Bài này cũng không có quyết định thanh lý (nhận định nhóm sau khi đọc toàn văn).
3. Chưa bài nào trong danh sách phân tích hiệu quả **tồn kho** theo nhóm ADI–CV² trên M5 (nhận định nhóm).
4. ⚠️ **Rủi ro cần xử lý:** bài 12 (tr. 13, 19) cho thấy LightGBM **dạng xác suất (distributional)** không cạnh tranh trên dữ liệu rời rạc, và TiDE + Tweedie tốt hơn. Đề tài dùng LightGBM **quantile regression**, là cách khác. Nhóm cần nêu rõ khác biệt này và nên thêm TiDE hoặc DeepAR làm baseline.
