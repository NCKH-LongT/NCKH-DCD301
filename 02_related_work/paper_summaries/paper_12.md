# Paper 12 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn bản arXiv (28 trang).**

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: Intermittent time series forecasting: local vs global models
Tác giả: Stefano Damato, Nicolò Rubattu, Dario Azzimonti, Giorgio Corani
Năm: 2026
Nguồn: arXiv:2601.14031 (đã nộp Journal of the Operational Research Society, chưa qua phản biện)
DOI/Link: https://arxiv.org/abs/2601.14031

## Problem

- Dự báo xác suất cho chuỗi nhu cầu rời rạc (có số 0), quan trọng cho quản lý tồn kho (abstract).

## Method

- Local: in-sample quantiles (baseline), iETS, GAS-NB, TweedieGP, Markov Walk (tr. 2).
- Global: FNN, DeepAR, DLinear, TiDE, PatchTST, Autoformer và gradient boosted trees (LightGBM) (tr. 6).
- Đầu ra phân phối: negative binomial, hurdle-shifted NB, Tweedie (abstract).
- **LightGBM dùng dạng distributional GBT** (dự đoán tham số phân phối, tối thiểu negative log-likelihood), **không phải quantile regression** (tr. 6).

## Dataset

- 5 dataset: M5 (30.490 chuỗi theo ngày), UCI, Auto, Carparts, RAF (Bảng 2, tr. 10–11); tổng hơn 40.000 chuỗi (abstract).
- Tiêu chí rời rạc: ADI > 1 (có ít nhất một số 0) (tr. 10).

## Evaluation

- Scaled quantile loss ở q ∈ {0,50; 0,80; 0,90; 0,95; 0,99}; RMSSE; thời gian huấn luyện (tr. 11, mục 3.2).

## Results

- TiDE chính xác nhất trong các mô hình global, vượt local, chi phí tính toán thấp hơn; mô hình lớn vừa tốn kém vừa kém chính xác (abstract; tr. 19).
- Tweedie cho ước lượng tốt nhất ở phân vị cao nhất (abstract; tr. 19).
- ⚠️ **GBT/LightGBM "không cạnh tranh" ở dạng dự báo xác suất**, biến động lớn giữa các lần chạy, và bị loại khỏi phân tích tiếp theo; LightGBM + Tweedie **lỗi số học trên M5** (tr. 13 và 19).

## Limitations

- Chưa có kiến trúc global được thiết lập cho chuỗi rời rạc (tr. 2).
- Chưa so sánh với mô hình pre-trained (foundation model), để lại cho nghiên cứu sau (tr. 2).
- Dùng mô hình "off-the-shelf" với tinh chỉnh siêu tham số tối thiểu (tr. 19).

## Relevance to our topic

[Nhận định nhóm] **Rất cao — và là bằng chứng phản biện cho lựa chọn mô hình của nhóm.** Kết quả cho thấy LightGBM dạng xác suất (distributional) kém trên dữ liệu rời rạc. Nhóm dùng LightGBM **quantile regression** (cách khác), nên cần (a) nêu rõ khác biệt này, và (b) nên thêm TiDE hoặc DeepAR làm baseline để trả lời được phản biện.

## Possible improvement

[Nhận định nhóm] So sánh LightGBM-quantile với TiDE/DeepAR ở tầng quyết định tồn kho (fill rate, chi phí), không chỉ quantile loss.
