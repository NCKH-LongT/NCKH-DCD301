# AI Model Integration

## 1. Trả lời các câu hỏi của README (Bước 8)

| Nội dung | Trả lời |
|---|---|
| **Model dùng là gì?** | **LightGBM hồi quy phân vị** (global model). Baseline: Seasonal Naive, ETS, TSB, LightGBM-Tweedie + safety stock chuẩn, TiDE/DeepAR |
| **Vì sao chọn?** | LightGBM được cả top 50 M5 Accuracy dùng (bài 02, tr. 1). Lời giải hạng nhất M5 Uncertainty huấn luyện LightGBM **riêng cho từng phân vị** (bài 03, tr. 14). Mô hình nhẹ, chạy trên CPU, dùng được đặc trưng ngoại sinh (giá, sự kiện, thuộc tính) |
| **Model lấy từ đâu?** | Thư viện mã nguồn mở: `lightgbm`, `statsforecast` (Nixtla), `neuralforecast` (Nixtla). Không có model đóng hay API trả phí |
| **Input?** | Bảng đặc trưng theo chuỗi × tuần (khoảng 26–28 đặc trưng, `data_flow.md` mục 5) |
| **Output?** | Phân vị {0,5; 0,8; 0,9; 0,95; 0,99} của **tổng nhu cầu trong L + R tuần** và **trong H tuần** |
| **Tích hợp vào app?** | Python batch job hằng tuần → ghi dự báo và khuyến nghị vào Parquet/DuckDB → FastAPI đọc và trả JSON → Streamlit hiển thị |
| **Có baseline không?** | Có, 5 baseline (mục 3); tất cả đi qua **cùng một Decision Engine** để so sánh công bằng |

## 2. Mô hình chính: LightGBM quantile

- **Mục tiêu dự báo trực tiếp tổng nhu cầu** D_{L+R} = Σ qty(t+1 … t+L+R) và D_H. **Không cộng phân vị theo tuần**, vì phân vị của tổng khác tổng các phân vị.
- **Một mô hình cho mỗi (dataset, horizon, phân vị)**: 2 dataset × 2 horizon × 5 phân vị = **20 mô hình** cho mỗi khối huấn luyện. Hàm mục tiêu `objective="quantile"`, `alpha` = phân vị.
- **Chống chồng chéo phân vị:** sắp xếp lại các phân vị của mỗi dự báo cho tăng dần.
- **Tinh chỉnh siêu tham số** trên tập validation, tìm ngẫu nhiên khoảng 30 cấu hình: `num_leaves`, `learning_rate`, `min_data_in_leaf`, `feature_fraction`, `lambda_l2`; dùng early stopping. Cùng ngân sách tinh chỉnh cho các baseline ML.
- **Rủi ro đã biết:** bài 12 (tr. 13, 19) cho thấy LightGBM **dạng distributional** kém trên dữ liệu rời rạc. Đề tài dùng **quantile regression**, cách khác, và kiểm chứng bằng so sánh với TiDE/DeepAR.

## 3. Baseline

| Baseline | Cách tạo phân vị D_{L+R}, D_H | Lý do đưa vào |
|---|---|---|
| **Seasonal Naive / thực nghiệm** | Phân vị thực nghiệm của các tổng (L + R) và H tuần trong lịch sử của chuỗi | Mốc tối thiểu |
| **ETS** (`statsforecast` AutoETS) | Phân phối chuẩn quanh tổng dự báo, phương sai từ phần dư | Phương pháp thống kê phổ biến; bài 02 (tr. 2): exponential smoothing vẫn cạnh tranh ở cấp product–store |
| **TSB** (`statsforecast`) | Trung bình mỗi tuần từ TSB → giả định phân phối Poisson cho tổng | Chuẩn cho nhu cầu rời rạc, xử lý hàng lỗi thời (bài 16, abstract; bài 23, tr. 2) |
| **LightGBM-Tweedie + safety stock chuẩn** | Dự báo điểm (Tweedie) → S = μ + z_τ·σ, với σ từ phần dư validation | Cách của đội thắng M5 Accuracy (bài 02, tr. 9) + cách tính safety stock truyền thống. **Ablation chính**: dự báo phân vị có hơn dự báo điểm + safety stock không |
| **TiDE hoặc DeepAR** (`neuralforecast`) | Hàm mất mát phân phối (negative binomial / Tweedie) → lấy mẫu đường đi → cộng theo horizon → phân vị | Mô hình sâu toàn cục; TiDE + Tweedie tốt nhất trong bài 12 (tr. 19) |

Trong cùng một dataset, mọi phương pháp dùng **cùng dữ liệu, cùng mốc chia, cùng Decision Engine và cùng tham số chi phí**.

## 4. Vị trí của AI trong hệ thống

```text
Panel tuần ──► Feature Builder ──► [AI] Forecasting Service ──► phân vị D_L+R, D_H
                                                                     │
                                                     Decision Engine ◄┘ (quy tắc minh bạch, không phải AI)
                                                                     │
                                         khuyến nghị ĐẶT HÀNG / GIỮ / THANH LÝ
```

AI chỉ nằm ở **tầng dự báo**. Tầng quyết định là **quy tắc minh bạch** (order-up-to, ngưỡng thanh lý), nên người quản lý hiểu được vì sao hệ thống khuyến nghị như vậy. Đây là gap 6 trong `research_gap.md`.

## 5. Ngân sách tính toán (ước lượng, cần đo lại khi chạy)

| Phần | Ước lượng |
|---|---|
| LightGBM, M5 (khoảng 8 triệu dòng × 26 đặc trưng, 20 mô hình × 2 khối) | Vài giờ trên CPU 12 luồng |
| LightGBM, VN (khoảng 85 nghìn dòng) | Vài phút |
| TiDE/DeepAR, M5 | Có thể lâu trên RTX 3050 (4 GB); nếu quá tải, chạy trên tập con 3 cửa hàng CA_1, TX_1, WI_1 và nêu rõ trong bài |
| Mô phỏng tồn kho | Nhanh (vector hóa theo chuỗi) |

## 6. Phiên bản và tái lập

- Ghi lại phiên bản thư viện trong `code/requirements.txt`.
- Cố định random seed; chạy mô hình sâu với 3 seed khác nhau.
- Lưu cấu hình mỗi lần chạy (YAML) cùng kết quả.
