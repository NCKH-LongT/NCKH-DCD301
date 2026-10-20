# Bàn giao: chạy baseline deep learning (N-HiTS)

Ngày 14/10/2026. Người giao: Anh Duy. Người nhận: một thành viên khác của nhóm SE1926_G01.

## 1. Bối cảnh

Bài báo so sánh 7 phương pháp dự báo xác suất bằng hiệu quả tồn kho trên hai bộ dữ liệu bán lẻ (M5, VN1). Mỗi bộ có ba cửa sổ kiểm thử:

- `main`: offset 0;
- `second`: offset 26;
- `third`: offset 52.

Reviewer và bài Theodorou et al. (2025) đều yêu cầu có một mô hình deep learning làm baseline. Script `code/run_neural.py` chạy **N-HiTS** (thư viện `neuralforecast`) theo **đúng giao thức** của các phương pháp khác:

- dự báo phân vị (0,5 / 0,8 / 0,9 / 0,95 / 0,99) của **tổng nhu cầu h tuần**;
- dự báo tại mỗi tuần trong 26 tuần kiểm thử;
- huấn luyện lại ở đầu mỗi khối 13 tuần.

Kết quả là một file `.npz` theo định dạng cache sẵn có. Script `code/member_run_neural.py` tự chạy, kiểm tra rồi commit và push các file này lên nhánh nhóm. Máy của Anh Duy sẽ dùng chúng để chấm điểm cùng 7 phương pháp kia.

**Không sửa script, siêu tham số hay dữ liệu.** Hai máy phải chạy giống hệt nhau thì kết quả mới gộp được.

## 2. Phân công

| Người | Dataset | Lệnh | Số lần chạy |
|---|---|---|---|
| **Thành viên B** | **M5** (30.490 chuỗi, nặng hơn) | `--dataset M5 --offset 0`, `26`, `52`, với `--h 3` | 3 |
| Anh Duy | VN1 (15.053 chuỗi) | `--dataset VN1 --offset 0`, `26`, `52`, với `--h 3` | 3 |

Thành viên B **chỉ cần dữ liệu M5**, không cần VN1.

Nếu máy B yếu (ít hơn 16 GB RAM), có thể đổi lại: B chạy VN1, Anh Duy chạy M5. Báo nhau trước khi đổi.

## 3. Chuẩn bị (khoảng 30–60 phút)

### 3.1. Lấy code

```bash
git clone https://github.com/NCKH-LongT/NCKH-DCD301.git
cd NCKH-DCD301
git checkout FA26_BDT301_SE1926_G01
```

Nếu đã có repo thì chỉ cần `git checkout FA26_BDT301_SE1926_G01` rồi `git pull`. Kiểm tra file `code/run_neural.py` có tồn tại; nếu không có, Anh Duy chưa push, hãy báo Anh Duy.

### 3.2. Lấy dữ liệu M5

1. Tải từ Kaggle, cuộc thi *M5 Forecasting – Accuracy*. Cần đăng nhập Kaggle và bấm chấp nhận luật cuộc thi.
2. Giải nén vào `data/m5-forecasting-accuracy/`. Cần đúng ba file sau (kiểm tra kích thước):

| File | Kích thước (byte) |
|---|---|
| `calendar.csv` | 103.469 |
| `sales_train_evaluation.csv` | 121.736.518 |
| `sell_prices.csv` | 203.395.785 |

**Lưu ý:** `sales_train_evaluation.csv` khác `sales_train_validation.csv`. Phải dùng bản *evaluation*.

### 3.3. Môi trường Python (3.12)

Đặt môi trường ảo ở ổ còn trống: cần khoảng 3 GB cho torch, ray và các thư viện kèm theo.

```bash
python -m venv D:/venvs/nf
D:/venvs/nf/Scripts/python.exe -m pip install numpy pandas neuralforecast==3.3.0
```

Máy của Anh Duy dùng neuralforecast 3.3.0 với torch 2.12.0 (bản CPU).

## 4. Chạy bằng một lệnh

Script `code/member_run_neural.py` làm trọn quy trình. Nó tự động:

1. kiểm tra nhánh git, phiên bản neuralforecast (3.3.0) và kích thước từng file dữ liệu;
2. chạy thử một lần và so **fingerprint** dữ liệu với máy của Anh Duy; lệch bất kỳ con số nào là dừng ngay;
3. chạy thật từng cửa sổ kiểm thử (offset 0, 26, 52) và ghi log;
4. kiểm tra log: không thiếu dự báo, file đã được ghi;
5. chép kết quả vào `code/outputs/neural/`, gồm file `.npz`, log, thời gian chạy và cấu hình máy;
6. **commit riêng thư mục `code/outputs/neural/`**, `git pull --rebase`, rồi `git push` lên nhánh nhóm.

Script commit và push **sau mỗi cửa sổ**. Nếu máy tắt giữa chừng, chỉ cần chạy lại đúng lệnh cũ: các cửa sổ đã xong sẽ được bỏ qua.

Script không sửa code, không sửa dữ liệu, và không commit gì ngoài `code/outputs/neural/`.

### Bước 1 — Kiểm tra máy (vài phút, không commit)

```bash
D:/venvs/nf/Scripts/python.exe code/member_run_neural.py --check-only
```

Kết quả đúng kết thúc bằng `Check-only mode: everything is ready for the full run.` Nếu gặp dòng `STOP: ...`, đọc lý do rồi xem mục 6.

### Bước 2 — Chạy thật

```bash
D:/venvs/nf/Scripts/python.exe code/member_run_neural.py
```

- Lệnh này mặc định chạy M5, ba cửa sổ, h = 3.
- **Thời gian:** chưa đo trên M5. Log in thời gian huấn luyện của từng khối; báo con số của khối đầu tiên cho Anh Duy.
- **Không để máy ngủ hoặc tắt** trong khi chạy. Lần đầu chạy M5, script tạo `data/cache/panel_m5.npz`, mất vài phút.

Nếu không có quyền push lên nhánh nhóm, script vẫn commit ở máy và in thông báo. Khi đó gửi thư mục `code/outputs/neural/` cho Anh Duy qua Drive hoặc Zalo. Cũng có thể chạy với `--no-push` rồi tự push sau.

### Fingerprint đúng (script tự kiểm tra; bảng để tham khảo)

| Lần chạy | Fingerprint |
|---|---|
| M5, offset 0 | `30490 series x 277 weeks, evaluated 30381, total sales of evaluated series 66793704` |
| M5, offset 26 | `30490 series x 251 weeks, evaluated 29917, total sales of evaluated series 59390858` |
| M5, offset 52 | `30490 series x 225 weeks, evaluated 28824, total sales of evaluated series 52145075` |
| VN1, offset 0 | `15053 series x 196 weeks, evaluated 13844, total sales of evaluated series 39234029` |
| VN1, offset 26 | `15053 series x 170 weeks, evaluated 11442, total sales of evaluated series 31620787` |
| VN1, offset 52 | `15053 series x 144 weeks, evaluated 9383, total sales of evaluated series 24659310` |

## 5. Kết quả sau khi chạy xong

Trên nhánh nhóm sẽ có:

- `code/outputs/neural/M5_w0_nhits_h3.npz`, `M5_w26_nhits_h3.npz`, `M5_w52_nhits_h3.npz`: mỗi file khoảng 10–20 MB;
- `code/outputs/neural/logs/`: log của bản chạy thử và từng cửa sổ;
- `code/outputs/neural/M5_run_info.json`: cấu hình máy và thời gian chạy từng cửa sổ.

**Không** commit thư mục `data/` hay bất kỳ file nào khác.

## 6. Nếu gặp lỗi

| Thông báo | Cách xử lý |
|---|---|
| `STOP: current branch is ...` | `git checkout FA26_BDT301_SE1926_G01`, rồi `git pull` |
| `STOP: neuralforecast ... required` | Cài đúng `neuralforecast==3.3.0` trong môi trường ảo |
| `STOP: ... has N bytes, expected ...` hoặc `missing data file` | Sai file hoặc thiếu file dữ liệu. Thường là dùng nhầm `sales_train_validation.csv` (xem mục 3.2) |
| `STOP: data fingerprint does not match` | Dữ liệu khác máy Anh Duy. Không chạy tiếp; báo Anh Duy |
| `STOP: run failed ...` | Gửi file log được nêu trong thông báo cho Anh Duy |
| `MemoryError` hoặc máy treo | Đóng các ứng dụng khác rồi chạy lại. Nếu vẫn lỗi, báo Anh Duy để đổi phân công. **Không** tự giảm siêu tham số |
| `push failed` | Kết quả đã commit ở máy. Gửi thư mục `code/outputs/neural/` cho Anh Duy |

## 7. Prompt cho AI của thành viên B

Dán nguyên đoạn sau vào trợ lý AI (Claude Code, Cursor…) đang mở trong thư mục repo:

```text
Tôi là thành viên nhóm nghiên cứu SE1926_G01. Nhiệm vụ: chạy baseline deep learning N-HiTS trên bộ dữ liệu M5 rồi
push kết quả lên nhánh nhóm, theo đúng file 07_paper_draft/handoff_neural_baseline.md của repo này. Hãy đọc toàn
bộ file đó trước, rồi làm lần lượt:
1. git checkout FA26_BDT301_SE1926_G01 và git pull.
2. Mục 3.2: kiểm tra 3 file M5 trong data/m5-forecasting-accuracy/ đúng kích thước. Nếu chưa có, hướng dẫn tôi tải
   từ Kaggle; đừng tự tải.
3. Mục 3.3: tạo môi trường ảo ở ổ còn trống (ít nhất 3 GB) và cài numpy, pandas, neuralforecast==3.3.0. Hỏi tôi
   trước khi cài.
4. Mục 4, bước 1: chạy  <python của môi trường ảo> code/member_run_neural.py --check-only
5. Nếu bước 4 thành công, chạy  <python của môi trường ảo> code/member_run_neural.py  ở chế độ nền và theo dõi
   log; báo cho tôi thời gian của từng khối và khi mỗi cửa sổ được push.

Quy tắc bắt buộc:
- KHÔNG sửa bất kỳ file nào trong code/ hay data/, kể cả khi gặp lỗi. Gặp "STOP:" hoặc lỗi thì dừng lại, cho tôi
  xem thông báo và tra bảng ở mục 6.
- KHÔNG tự chạy git commit hoặc git push bằng tay; script tự commit đúng thư mục code/outputs/neural/. Không đưa
  thư mục data/ lên git.
- Không đổi tham số --dataset, --offsets hay --h nếu tôi chưa yêu cầu.
```

## 8. Việc của Anh Duy sau khi B push

1. `git pull`, rồi chép `code/outputs/neural/M5_w{0,26,52}_nhits_h3.npz` vào `data/cache/forecasts/M5{,_w26,_w52}/nhits_h3.npz`.
2. Chạy VN1 trên máy này bằng cùng script: `D:/venvs/nf/Scripts/python.exe code/member_run_neural.py --dataset VN1`.
3. Chấm điểm:

   ```bash
   python code/equal_fill_ci.py --models empirical,tsb_nb,ets,lgb_tweedie,lgb_conformal,hgb_quantile,lgb_quantile,nhits --out-suffix nn
   ```

   Chạy thêm với `--offset 26` và `--offset 52`. Sau đó tính độ chính xác (wQL) và regret có N-HiTS và C2.
4. Ghi kết quả vào `06_experiment_results/` (bản tạp chí).
