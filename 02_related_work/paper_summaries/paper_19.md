# Paper 19 Summary

**Nhóm:** Domain (inventory)
**Mức kiểm chứng (cập nhật 10/10/2026):** ✅ đã đọc toàn văn bản accepted manuscript (xem mục cuối). Trước đó (29/09/2026): ⚠️ **Chỉ đọc được trang mô tả của kho Lancaster** (tóm tắt + keywords). Có thêm **bản tóm tắt do người dùng cung cấp** (29/09/2026); các ý lấy từ bản này được đánh dấu `[Theo tóm tắt người dùng cung cấp — CHƯA đối chiếu PDF]` và **cần đối chiếu PDF trước khi trích số liệu**. PDF mở: https://eprints.lancs.ac.uk/id/eprint/140119/

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

## Kiểm chứng toàn văn (10/10/2026)

Đã đọc bản accepted manuscript trên kho Lancaster (35 trang; số trang dưới đây theo file PDF đó: https://eprints.lancs.ac.uk/id/eprint/140119/).

- Phương pháp: tham số hóa mô hình dự báo bằng hàm chi phí lập từ chỉ số tồn kho và chính sách tồn kho hiện hành, thay vì tối ưu likelihood hoặc sai số (tr. 1); mô hình là exponential smoothing mức cục bộ (tr. 13).
- Dữ liệu: 229 mặt hàng của một nhà sản xuất hàng tiêu dùng (vệ sinh) ở châu Âu, 173 tuần mỗi mặt hàng, chu kỳ kế hoạch tuần, lead time 3–5 tuần; 52 tuần cuối là tập kiểm thử; đánh giá rolling origin (tr. 13, 17).
- Kết quả: giảm bias 25%–60% so với tối ưu theo MSE, đổi lại độ chính xác giảm tối đa 9% (tr. 21). **Con số "cải thiện bias khoảng 62%" trong tóm tắt người dùng cung cấp ở trên là không đúng; dùng 25–60%.**
- Bài nêu rằng nghiên cứu dự báo thường coi độ chính xác là đại diện hợp lý cho quyết định mà dự báo phục vụ, và nhiều tác giả đã đặt câu hỏi về giả định này (tr. 6).
