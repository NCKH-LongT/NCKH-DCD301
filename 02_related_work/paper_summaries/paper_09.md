# Paper 09 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn bản arXiv (7 trang).**

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: Hierarchical Time Series Forecasting Via Latent Mean Encoding
Tác giả: Alessandro Salatiello, Stefan Birr, Manuel Kunz
Năm: 2025
Nguồn: arXiv:2506.19633 (chưa qua phản biện)
DOI/Link: https://arxiv.org/abs/2506.19633

## Problem

- Dự báo nhất quán ở nhiều mức tổng hợp thời gian (temporal hierarchy) (abstract).

## Method

- Kiến trúc phân cấp dạng encoder–decoder với các module chuyên cho từng mức tổng hợp thời gian, học mã hóa hành vi trung bình trong lớp ẩn (abstract).
- So sánh với TSMixer dạng nguyên khối (Mono), TFT, DeepAR và baseline trung bình cửa sổ (tr. 4, mục 2.4).

## Dataset

- M5; dùng 1886 ngày đầu để train, 28 ngày validation, 28 ngày test; context window c = 35, horizon h = 28 (tr. 3).

## Evaluation

- WRMSSE, RMSE theo ngày/tuần, MFEV, MAD (Bảng 1, tr. 4).

## Results

- EncDecMSE đạt WRMSSE **0,620**, EncDecNB 0,634, so với TSMixer-Ext 0,640, TFT 0,670, DeepAR 0,789 (Bảng 1, tr. 4).
- Lưu ý: số liệu của DeepAR, TFT, TSMixer-Ext được **lấy lại từ Chen et al. (2023)**, huấn luyện tới 300 epoch, trong khi mô hình của tác giả chỉ 100 epoch (tr. 4).

## Limitations

- Bài không có mục hạn chế riêng (đã tìm trong toàn văn).
- [Nhận định nhóm] Chỉ thực nghiệm trên M5; một phần baseline lấy lại từ bài khác chứ không chạy lại.

## Relevance to our topic

[Nhận định nhóm] **Trung bình.** Tham khảo cách chia dữ liệu 1886/28/28.

## Possible improvement

[Nhận định nhóm] Dùng cùng cách chia để so sánh được.
