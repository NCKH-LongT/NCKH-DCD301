# Giai đoạn 4 — Chi phí tính toán so với hiệu quả tồn kho (yêu cầu số 3 của reviewer)

Ngày 20/10/2026. Phần diễn giải gắn nhãn [Nhận định nhóm].

**Yêu cầu của reviewer:** thảo luận sự đánh đổi giữa chi phí tính toán, độ trễ và hiệu quả của các mô hình zero-shot hiện đại (như Chronos) trong bài toán lập kế hoạch tồn kho định kỳ.

Không chạy thêm thí nghiệm nào. Mọi con số lấy từ log và bảng kết quả đã có trong repo.

## Nguồn

| Số liệu | File |
|---|---|
| Thời gian dự báo các phương pháp thống kê và ML | `code/outputs/logs/run_<D>[_wN][_v2/_v24/_grid].log` (dòng "forecasting <model>, h=3 … done in Ns") |
| Thời gian Chronos-2 | `code/outputs/logs/run_M5_c2.log`, `run_VN1[_w26/_w52]_c2.log` |
| Thời gian N-HiTS | `code/outputs/neural/M5_run_info.json`, `VN1_run_info.json` |
| Tồn kho ở cùng fill rate (Chronos-2) | `code/outputs/equal_fill_ci_c2.md` (M5), `equal_fill_ci[_w26/_w52]_c2m7.md` (VN1) |
| Tồn kho ở cùng fill rate (N-HiTS, TSB-NB, C2) | `code/outputs/neural_eval.md` |

## Cách đo

- Thời gian là **thời gian dự báo** cho chân trời đặt hàng h = 3, trên **một cửa sổ kiểm thử 26 tuần** và **mọi chuỗi được đánh giá**. Với các mô hình học, con số gồm huấn luyện ở 2 mốc cắt (mỗi khối 13 tuần một lần) và dự báo 26 origin. Không gồm thời gian mô phỏng kho (vài giây).
- Mỗi mô hình có nhiều lần chạy (ba cửa sổ, các phiên bản code), và thời gian thay đổi theo tải của máy. Vì vậy bảng ghi **khoảng** thời gian, không phải một con số.
- **Máy:** mọi phương pháp chạy trên máy phát triển (Intel i5-12450H, 12 luồng, 16 GB RAM, chỉ CPU), trừ N-HiTS trên M5, chạy trên máy thành viên B (Intel 20 luồng, 16 GB RAM, chỉ CPU). Không phương pháp nào dùng GPU.
- LGB-Q huấn luyện **5 mô hình** (một mô hình cho mỗi phân vị) ở mỗi mốc cắt, nên chậm hơn LGB-T và LGB-C (một mô hình Tweedie).

## 1. Thời gian dự báo (h = 3, một cửa sổ, chỉ CPU)

| Phương pháp | Loại | M5 (28.824–30.381 chuỗi) | VN1 (9.383–13.844 chuỗi) |
|---|---|---|---|
| ETS | thống kê | 4–19 giây | khoảng 1 giây |
| EMP | thống kê | 0,5–2,4 phút | khoảng 0,5 phút |
| TSB-NB | thống kê | 1,1–2,3 phút | khoảng 0,5 phút |
| LGB-T | ML toàn cục | 0,7–4,0 phút | 0,2–0,7 phút |
| LGB-C | ML toàn cục | 0,7–2,3 phút | 0,2–0,7 phút |
| HGB-Q | ML toàn cục (mẫu 300 nghìn dòng) | 1,3–3,6 phút | 1,3–1,4 phút |
| **LGB-Q** | ML toàn cục, 5 mô hình | **10–21 phút** | **2,4–4,4 phút** |
| N-HiTS | deep learning, huấn luyện | khoảng 7 phút (máy B) | 5,1–5,7 phút |
| **Chronos-2** | foundation model, zero-shot | **5,4 giờ** (19.324 giây, cửa sổ chính) | **32–45 phút** |

Chronos-2 với chân trời thanh lý h = 13 mất thêm 7,9 giờ trên M5, tức khoảng 13,4 giờ cho cả hai chân trời của một cửa sổ. Vì vậy Chronos-2 chỉ chạy ở chân trời mặc định và chỉ ở cửa sổ chính của M5.

## 2. Đặt cạnh hiệu quả tồn kho

Tồn kho cần để đạt fill rate 0,92, so với LGB-Q (dương = cần nhiều hàng hơn LGB-Q), qua các cửa sổ có kết quả:

| Phương pháp | Thời gian / cửa sổ (M5) | M5 | VN1 |
|---|---|---|---|
| LGB-Q | 10–21 phút | mốc so sánh | mốc so sánh |
| C2 (= LGB-Q + TSB-NB) | khoảng thời gian LGB-Q + TSB-NB | −1,5% đến +0,4% | −5,9% đến −10,5% (`combination.md`) |
| TSB-NB | 1–2 phút | +5,5% đến +10,4% | −11,3% đến +25,1% |
| N-HiTS | khoảng 7 phút | +2,6% đến +8,9% | −2,1% đến +8,3% |
| Chronos-2 | 5,4 giờ | +14,7% (chỉ cửa sổ chính) | +1,2% đến +48,1% |

## Nhận xét

1. **Mọi phương pháp, trừ Chronos-2, chạy xong một cửa sổ trong vài phút đến khoảng 20 phút trên CPU laptop.** Chu kỳ đặt hàng là mỗi tuần, nên thời gian này không phải ràng buộc thực tế.
2. **Chi phí tính toán không đi kèm hiệu quả.** Chronos-2 chậm nhất (khoảng 15 lần LGB-Q ở cùng cửa sổ chính M5: 19.324 so với 1.251 giây) nhưng cũng cần nhiều tồn kho nhất trong nhóm mô hình học (+15% trên M5, tới +48% trên VN1). N-HiTS tốn thời gian tương đương LGB-Q nhưng kém hơn trên M5.
3. **Lựa chọn tốt nhất về cả hai mặt** là LGB-Q (M5) và C2 (VN1). C2 chỉ tốn thêm thời gian của TSB-NB, khoảng 1–2 phút.
4. **Về độ trễ:** quyết định theo tuần chấp nhận được độ trễ vài giờ, nên ngay cả 13,4 giờ của Chronos-2 trên CPU vẫn nằm trong một chu kỳ tuần. Điểm yếu thật của Chronos-2 là **chi phí so với lợi ích**: tốn nhiều tài nguyên nhất (muốn nhanh thì cần GPU) mà tồn kho lại kém nhất. Thời gian dự báo tăng theo số chuỗi, nên với danh mục lớn hơn M5 nhiều lần, khoảng cách này còn lớn hơn.
5. [Nhận định nhóm] Chronos-2 ở đây chạy **zero-shot, không fine-tune, không biến ngoại sinh**, với ngữ cảnh là chuỗi tổng h tuần không chồng lấn. N-HiTS là mô hình **đơn biến, không tinh chỉnh**. Kết quả chỉ cho thấy hai baseline tiêu chuẩn này không vượt được mô hình phân vị toàn cục có biến giá và lịch. Đây không phải giới hạn trên của deep learning hay foundation model.
6. **Giới hạn của phép so sánh:** thời gian đo trên hai máy khác nhau (N-HiTS M5 trên máy B), và các lần chạy khác nhau dùng các phiên bản code khác nhau. Các con số chỉ đúng ở mức độ lớn, không dùng để so sánh chính xác vài chục giây.

## Đoạn văn đề xuất cho bài (tiếng Anh)

Đặt ở Discussion, sau đoạn về N-HiTS và Chronos-2, hoặc ở Limitations:

> **Computational cost.** All methods except Chronos-2 forecast one 26-week window in minutes on a laptop CPU (Intel i5-12450H, 16 GB, no GPU): about 1–2 minutes for TSB-NB, 10–21 minutes for LGB-Q on M5 (five quantile models per cutoff) and about 7 minutes for N-HiTS. Zero-shot Chronos-2 needs no training, but its CPU inference took 5.4 hours per window on M5 at the replenishment horizon and 32–45 minutes on VN1, while requiring 15% (M5) and up to 48% (VN1) more inventory than LGB-Q at a fill rate of 0.92. For a weekly review cycle, computation is therefore not the binding constraint for the gradient-boosting and statistical methods, and the additional cost of the foundation model and the neural network did not buy inventory efficiency in our setting. Both were run without fine-tuning or covariates, so this is a statement about standard baselines rather than an upper bound for these model classes.
