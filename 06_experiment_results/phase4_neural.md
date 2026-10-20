# Giai đoạn 4 — Baseline deep learning (N-HiTS)

Ngày 14/10/2026. Phần diễn giải gắn nhãn [Nhận định nhóm].

Nguồn:

- `code/run_neural.py` và `code/member_run_neural.py`: chạy mô hình;
- `code/neural_eval.py` → `code/outputs/neural_eval.md` (bản sao ở `tables/`): chấm điểm.

Dự báo nằm ở `code/outputs/neural/`.

| Phần | Máy | Trạng thái |
|---|---|---|
| VN1, ba cửa sổ | Anh Duy (i5-12450H, 16 GB) | ✅ xong; mỗi cửa sổ 5–6 phút |
| M5, ba cửa sổ | Thành viên B (20 luồng CPU, 16 GB) | ✅ xong; mỗi cửa sổ khoảng 7 phút; fingerprint khớp cả ba cửa sổ |

## Thiết kế

- **Mô hình:** N-HiTS (`neuralforecast` 3.3.0), loss đa phân vị.
- **Mục tiêu:** dự báo trực tiếp phân vị của tổng h tuần (h = 3).
  - Mô hình được huấn luyện trên chuỗi tổng h tuần dịch tới, Z[t] = Y[t] + … + Y[t+h−1].
  - Giá trị cần dự báo là bước thứ h của dự báo trên chuỗi Z.
- **Cấu hình huấn luyện:**
  - huấn luyện lại ở đầu mỗi khối 13 tuần;
  - lịch sử đầu vào 52 tuần;
  - 1.500 bước huấn luyện;
  - mô hình đơn biến (không dùng giá hay lịch);
  - siêu tham số cố định, một seed.

## Kết quả VN1

| | Cửa sổ chính | Cửa sổ thứ hai | Cửa sổ thứ ba |
|---|---|---|---|
| wQL N-HiTS / LGB-Q / TSB-NB | 0,107 / **0,103** / 0,129 | 0,079 / **0,078** / 0,088 | 0,104 / **0,102** / 0,138 |
| Tồn kho N-HiTS so với LGB-Q, fill 0,92 | +8,3% [+3,6; +12,7] | −2,1% [−8,3; +0,4] | +2,6% [−1,8; +10,8] |
| Hạng đường đánh đổi của N-HiTS (8 phương pháp) | 4,4 | 2,8 | 3,8 |
| Regret của N-HiTS | 9,5% | 5,9% | 7,8% |

Regret lớn nhất qua ba cửa sổ VN1, so với phương pháp đơn tốt nhất trong 8:

| C2 | N-HiTS | LGB-T | LGB-Q | HGB-Q | TSB-NB |
|---|---|---|---|---|---|
| **−0,7%** | 9,5% | 9,5% | 10,2% | 12,3% | 20,7% |

Lưu ý: regret của LGB-Q ở cửa sổ thứ hai tăng từ 9,4% lên 10,2%, vì N-HiTS thắng LGB-Q ở một số mức fill rate trong cửa sổ đó, nên mốc "phương pháp đơn tốt nhất" thay đổi.

## Nhận xét (VN1)

1. **Độ chính xác:** N-HiTS đứng thứ hai hoặc thứ ba về wQL, sau LGB-Q, ngang HGB-Q, và tốt hơn TSB-NB rõ rệt. Độ phủ ở các phân vị cao gần mức danh nghĩa (ví dụ 0,99 → 0,986–0,992).
2. **Tồn kho:** N-HiTS không dẫn đầu ở cửa sổ nào; hạng đường đánh đổi 2,8–4,4.
   - Ở cửa sổ thứ hai (nơi TSB-NB thắng), N-HiTS nhỉnh hơn LGB-Q một chút.
   - Ở cửa sổ chính, N-HiTS kém LGB-Q 3,5–8,8%.
3. **Kết luận chính không đổi khi thêm N-HiTS:**
   - LGB-Q vẫn là phương pháp đơn tốt nhất ở cửa sổ chính và cửa sổ thứ ba;
   - C2 vẫn có regret thấp nhất, và vẫn tốt hơn mọi phương pháp đơn kể cả khi tính N-HiTS.
4. [Nhận định nhóm] N-HiTS ở đây là mô hình đơn biến, không tinh chỉnh. Một mô hình neural có dùng biến ngoại sinh và được tinh chỉnh có thể làm tốt hơn. Khi viết bài cần nói rõ đây là một baseline deep learning tiêu chuẩn, không phải giới hạn trên của deep learning.

## Kết quả M5 (thêm 14/10/2026, từ máy thành viên B)

| | Cửa sổ chính | Cửa sổ thứ hai | Cửa sổ thứ ba |
|---|---|---|---|
| wQL N-HiTS / LGB-Q / TSB-NB | 0,078 / **0,076** / 0,088 | 0,083 / **0,080** / 0,091 | 0,089 / **0,086** / 0,098 |
| Tồn kho N-HiTS so với LGB-Q, fill 0,92 | +7,5% [+6,7; +8,3] | +2,6% [+2,3; +3,1] | +8,9% [+6,7; +11,2] |
| Hạng đường đánh đổi (8 phương pháp) | 3,8 | 2,6 | 5,8 |
| Regret của N-HiTS | 5,0% | 3,0% | 9,2% |

Regret lớn nhất qua **6 lần chạy** (2 dataset × 3 cửa sổ, 8 phương pháp đơn):

| C2 | N-HiTS | LGB-T | LGB-Q | HGB-Q | TSB-NB |
|---|---|---|---|---|---|
| **0,9%** | 9,5% | 9,5% | 10,2% | 12,3% | 20,7% |

### Nhận xét M5

1. Trên M5, N-HiTS kém LGB-Q rõ rệt ở mọi cửa sổ: cần thêm 2,6–10,0% tồn kho, mọi khoảng tin cậy đều nằm trên 0. Nó kém HGB-Q nhưng tốt hơn TSB-NB ở 2 trên 3 cửa sổ.
2. [Nhận định nhóm] Trên M5, LGB-Q dùng giá, sự kiện và phân cấp sản phẩm; N-HiTS đơn biến không có các thông tin này. Phù hợp với cách giải thích đó, trên M5 N-HiTS kém LGB-Q **nhất quán** ở cả ba cửa sổ, còn trên VN1 thì lẫn lộn (cửa sổ thứ hai N-HiTS còn nhỉnh hơn LGB-Q). Đây chỉ là giả thuyết; bài không kiểm tra N-HiTS có biến ngoại sinh.
3. **Kết luận chính của bài không đổi:** LGB-Q là phương pháp đơn tốt nhất trên M5; C2 có regret lớn nhất thấp nhất (0,9%).

## Việc tiếp theo

- Khi B push phần M5: `git pull`, rồi chạy `python code/neural_eval.py`. Script tự nhận các file mới và cập nhật bảng.
