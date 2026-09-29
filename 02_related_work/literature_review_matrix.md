# Literature Review Matrix

Chi tiết từng bài: xem `paper_summaries/paper_XX.md`.

| No | Paper Title | Year | Venue | Domain | AI Method | Dataset | Metrics | Main Contribution | Limitation | Relevance to Our Topic |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | The M5 competition: Background… | 2022 | IJF | Bán lẻ | 24 benchmark (thống kê + ML) | M5 | WRMSSE, WSPL | Định nghĩa benchmark M5 | Không có dữ liệu tồn kho/chi phí | Cao: nguồn dataset & metric |
| 02 | M5 accuracy competition: Results… | 2022 | IJF | Bán lẻ | LightGBM global, ensemble | M5 | WRMSSE | ML/LightGBM thắng áp đảo | Chỉ đánh giá sai số, khó tái lập | Rất cao: lý do chọn LightGBM |
| 03 | M5 uncertainty competition: Results… | 2022 | IJF | Bán lẻ | LightGBM quantile + thống kê | M5 | WSPL (9 phân vị) | Tổng kết dự báo xác suất | Không liên hệ quyết định tồn kho | Rất cao: phân vị → quyết định |
| 04 | Algorithmic Transparency in FSS | 2024 | arXiv | Hệ thống hỗ trợ dự báo | Prophet-like decomposition | Subset M5 (FOODS) | Chỉnh sửa có hại, hài lòng | Minh bạch giảm chỉnh sửa có hại | 1 mô hình, dữ liệu nhỏ | TB: thiết kế dashboard |
| 05 | Balancing Strategy for Counterfactual… | 2024 | ICML | Nhân quả | Balancing (ERM) | M5 (giá = treatment) | Factual error | Xem xét lại balancing cho chuỗi | Không có ground-truth phản thực tế | Thấp |
| 06 | Foundation Models … Dual-Strategy Ensembling | 2025 | KDD WS | Bán lẻ / supply chain | LightGBM, DeepAR, PatchTST, Chronos… + HE/AE | M5 + 3 dataset | Sai số phân cấp | Ensemble FM tăng khả năng tổng quát | Trọng số cố định, tốn kém, khó giải thích | TB–cao: baseline hiện đại |
| 07 | The Forecast Critic | 2025 | arXiv | Giám sát dự báo | LLM | 1.000 chuỗi M5 + synthetic | F1, sCRPS | LLM phát hiện dự báo kém (F1 0,88) | Ít chuỗi, 1 nguồn dự báo | Thấp–TB: future work |
| 08 | The cost of ensembling | 2025 | arXiv | Bán lẻ | 10 mô hình, 8 ensemble | M5, VN1 | Point & prob. accuracy, cost | Ensemble nhỏ 2–3 mô hình đã đủ | Không đánh giá tầng quyết định | TB–cao: lập luận mô hình gọn |
| 09 | Hierarchical TSF via Latent Mean Encoding | 2025 | arXiv | Bán lẻ | Mạng phân cấp mới | M5 (1886/28/28) | Sai số dự báo | Vượt TSMixer | Thiếu số liệu công khai | TB: cách chia dữ liệu |
| 10 | CLEF | 2025 | ICLR'26 | Y sinh (+ bán lẻ) | Controllable sequence editing | 8 dataset, M5 theo bang | MAE | Sinh chuỗi có điều kiện | Không có ground-truth nhân quả | Thấp |
| 11 | Multi-objective prob. forecast combination for inventory | 2026 | arXiv | **Tồn kho** | Kết hợp dự báo xác suất đa mục tiêu (Pareto) | Walmart (M5), RAF spare parts | Accuracy + inventory performance | Tối ưu đồng thời độ chính xác & quyết định | Loại SKU toàn 0; cần nhiều mô hình; chỉ phía nhập hàng | **Rất cao: bài gần nhất** |
| 12 | Intermittent TSF: local vs global | 2026 | arXiv | Tồn kho / nhu cầu rời rạc | Local (iETS, TweedieGP…) vs global (TiDE, DeepAR, GBT…) | 5 dataset, >40k chuỗi (có M5) | Quantile loss, cost | Global (TiDE) + Tweedie tốt nhất ở phân vị cao | Chưa có kiến trúc chuẩn; không có tầng quyết định | Rất cao |
| 13 | e2eTD probabilistic top-down | 2026 | arXiv | Bán lẻ | Probabilistic top-down sampling | M5, Favorita | WSPL | Hạng 11/892 M5-U, 5 phút trên laptop | Chỉ dự báo trực tiếp chuỗi tổng hợp | Cao |
| 14 | LightGBM | 2017 | NeurIPS | Tổng quát | GBDT (GOSS, EFB) | Nhiều dataset | Time, accuracy | GBDT nhanh hơn >20× | Cần tự tạo đặc trưng chuỗi | **Mô hình chính** |
| 15 | Croston's method | 1972 | ORQ | Tồn kho | Croston | Lý thuyết/mô phỏng | Bias, variance | Chuẩn cho nhu cầu rời rạc | Bị lệch; không xử lý lỗi thời | Baseline |
| 16 | TSB – linking forecasting to obsolescence | 2011 | EJOR | **Tồn kho** | TSB | Mô phỏng + thực tế | Error, inventory cost, obsolescence | Nối dự báo với tồn kho lỗi thời | Không dùng biến ngoại sinh | Rất cao: cơ sở cho THANH LÝ |
| 17 | DeepAR | 2020 | IJF | Bán lẻ | Global RNN xác suất | Amazon, điện, giao thông | Quantile loss, ND | Deep probabilistic global model | Cần GPU, khó giải thích | Baseline tùy chọn |
| 18 | Categorization of demand patterns | 2005 | JORS | **Tồn kho** | Phân loại ADI–CV² | Lý thuyết + thực tế | MSE | 4 nhóm nhu cầu, chọn phương pháp | Chỉ xét phương pháp thống kê | Rất cao: khung phân tích |
| 19 | Optimising forecasting models for inventory planning | 2020 | IJPE | **Tồn kho** | ETS tối ưu theo tiêu chí tồn kho | Bán lẻ + mô phỏng | Error + service level, stock | Accuracy ≠ inventory performance | Chỉ mô hình thống kê | Rất cao: luận điểm chính |

## Tổng hợp (Synthesis)

### 1. Các bài trước đã làm gì?

- **Nhóm M5 (01–03, 06, 08, 09, 13):** tối ưu **độ chính xác dự báo** (WRMSSE/WSPL). LightGBM global là lựa chọn mạnh và phổ biến nhất; xu hướng mới là foundation model và ensemble.
- **Nhóm nhu cầu rời rạc (12, 15, 16, 18):** nhu cầu nhiều số 0 cần phương pháp/phân phối riêng (Croston, TSB, Tweedie); phân vị cao khó ước lượng.
- **Nhóm dự báo → tồn kho (11, 16, 19):** chỉ ra rằng dự báo chính xác hơn **không đảm bảo** quyết định tồn kho tốt hơn.

### 2. Model thường dùng

LightGBM (Tweedie/quantile), ETS/ARIMA, Croston/SBA/TSB, DeepAR, TiDE/PatchTST, Chronos, và các ensemble.

### 3. Metric thường dùng

- Dự báo: WRMSSE, RMSSE, MAE, WSPL/pinball loss, sCRPS. **MAPE hầu như không dùng** vì dữ liệu có nhiều số 0.
- Tồn kho (ít bài dùng): service level/fill rate, lượng tồn, chi phí, lượng hàng lỗi thời.

### 4. Khoảng trống (gap) đầu vào cho Bước 5

1. Trên M5, **rất ít bài đánh giá bằng KPI tồn kho**; bài 11 là ngoại lệ gần nhất.
2. Bài 11 **loại bỏ SKU toàn số 0** và chỉ xét **phía nhập hàng**; chưa có bài nào trên M5 đưa ra **quyết định hai chiều nhập + thanh lý**.
3. Chưa có phân tích **theo nhóm nhu cầu ADI–CV²** về việc AI (LightGBM quantile) giúp quyết định tồn kho tốt hơn ở nhóm nào, và kém hơn baseline thống kê (TSB) ở nhóm nào.
4. Các hướng mạnh nhất (ensemble, foundation model) **tốn kém**; bài 08 và 13 gợi ý rằng mô hình gọn có thể đủ tốt, nhưng chưa được kiểm chứng ở tầng quyết định.
