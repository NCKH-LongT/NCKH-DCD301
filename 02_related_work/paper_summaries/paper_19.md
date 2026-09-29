# Paper 19 Summary

**Nhóm:** Domain (inventory)
**Mức kiểm chứng (29/09/2026):** ⚠️ **Chỉ đọc được trang mô tả của kho Lancaster** (tóm tắt + keywords). Có thêm **bản tóm tắt do người dùng cung cấp** (29/09/2026); các ý lấy từ bản này được đánh dấu `[Theo tóm tắt người dùng cung cấp — CHƯA đối chiếu PDF]` và **cần đối chiếu PDF trước khi trích số liệu**. PDF mở: https://eprints.lancs.ac.uk/id/eprint/140119/

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: Optimising forecasting models for inventory planning
Tác giả: Nikolaos Kourentzes, Juan R. Trapero, Devon K. Barrow
Năm: 2020
Nguồn: International Journal of Production Economics, 225, 107597
DOI/Link: https://doi.org/10.1016/j.ijpe.2019.107597 · bản mở: https://eprints.lancs.ac.uk/id/eprint/140119/

## Problem

- Dự báo không chính xác gây hết hàng, mất doanh thu hoặc tồn kho quá mức; tài liệu dự báo thường ưu tiên metric thống kê thay vì kết quả tồn kho (trang mô tả Lancaster).

## Method

- Tối ưu tham số mô hình dự báo bằng cách **đưa trực tiếp các metric tồn kho và chính sách tồn kho hiện có** vào hàm mục tiêu; cân bằng nhiều mục tiêu (đáp ứng nhu cầu vs giảm tồn dư) qua hàm chi phí (trang mô tả Lancaster).
- [Theo tóm tắt người dùng cung cấp — CHƯA đối chiếu PDF] Nhúng mô hình dự báo vào **vòng mô phỏng tồn kho**: sinh dự báo với bộ tham số ứng viên → mô phỏng tồn kho → đo KPI tồn kho → điều chỉnh tham số (simulation–optimization).
- [Chưa kiểm chứng] Họ mô hình dự báo cụ thể (exponential smoothing?) — cần mở toàn văn.

## Dataset

- So sánh với các cách tiếp cận có sẵn trên **dữ liệu thực** (trang mô tả Lancaster); keywords có "simulation".
- [Theo tóm tắt người dùng cung cấp — CHƯA đối chiếu PDF] Dữ liệu thực của một nhà sản xuất ở Anh: **229 SKU**, dữ liệu **theo tuần**, **173 quan sát/SKU**, lead time điển hình **3–5 tuần**; hàng tiêu dùng (chất tẩy rửa gia dụng, chăm sóc cá nhân).

## Evaluation

- [Theo tóm tắt người dùng cung cấp — CHƯA đối chiếu PDF] Độ chính xác dự báo (MSE/MAE…), độ lệch (bias), mức phục vụ, tồn kho/chi phí lưu kho.

## Results

- Bài xem xét liệu độ chính xác dự báo có phải chỉ báo đáng tin cho hiệu quả tồn kho hay không (trang mô tả Lancaster).
- [Theo tóm tắt người dùng cung cấp — CHƯA đối chiếu PDF] Dự báo tối ưu theo mục tiêu tồn kho thường **kém chính xác hơn về thống kê** (sai số tăng tới khoảng **9%**) nhưng **cải thiện độ lệch ngoài mẫu tới khoảng 62%** và cho kết quả mức phục vụ/tồn kho tốt hơn.
- [Theo tóm tắt người dùng cung cấp — CHƯA đối chiếu PDF] Mô hình có MSE nhỏ nhất thường **không** phải mô hình cho chi phí tồn kho nhỏ nhất.

## Limitations

- [Chưa kiểm chứng].

## Relevance to our topic

[Nhận định nhóm] **Rất cao** cho luận điểm "độ chính xác dự báo ≠ hiệu quả tồn kho" — nhưng chỉ trích sau khi đọc toàn văn.

## Possible improvement

[Nhận định nhóm] Mở rộng luận điểm sang mô hình ML trên M5.
