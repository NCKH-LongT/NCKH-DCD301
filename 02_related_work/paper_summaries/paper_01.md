# Paper 01 Summary

**Nhóm:** Direct (M5 / bán lẻ)
**Mức kiểm chứng (29/09/2026):** ✅ **Đã đọc toàn văn** (PDF open access trong `papers_pdf/1-s2.0-S0169207021001187-main.pdf`, 12 trang).

> **Quy ước nguồn** (để đối chiếu khi giảng viên hỏi):
> - `(tr. N)` = trang thứ N trong file PDF (đếm theo trang PDF, không phải số in trên trang); `(abstract)` = phần tóm tắt của bài.
> - `[Nguồn thứ cấp: bài X, tr. N]` = thông tin **không** đọc trực tiếp từ bài này mà từ một bài khác trích dẫn nó.
> - `[Chưa kiểm chứng]` = chưa tìm thấy trong phần đã đọc được; **không được dùng trong bài báo** cho tới khi mở toàn văn kiểm tra.
> - `[Nhận định nhóm]` = phân tích của nhóm, **không phải** nội dung bài báo.

## Citation

Tên bài: The M5 competition: Background, organization, and implementation
Tác giả: Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos
Năm: 2022
Nguồn: International Journal of Forecasting, 38(4), 1325–1336
DOI/Link: https://doi.org/10.1016/j.ijforecast.2021.07.007

## Problem

- Cuộc thi M5 tập trung vào dự báo doanh số bán lẻ: tạo dự báo điểm chính xác nhất cho **42.840 chuỗi thời gian** doanh số phân cấp của Walmart, đồng thời ước lượng độ bất định (abstract).

## Method

- Bài **không đề xuất mô hình**; mô tả bối cảnh, tổ chức và triển khai cuộc thi với 2 nhánh song song **Accuracy** và **Uncertainty** (abstract).
- Mở rộng so với các cuộc thi M trước ở 5 điểm, trong đó có biến ngoại sinh, chuỗi phân nhóm tương quan và chuỗi **rời rạc (intermittency)** (abstract; tr. 2).

## Dataset

- 3.049 sản phẩm, 42.840 chuỗi ở **12 cấp tổng hợp**; cấp thấp nhất product–store có **30.490 chuỗi** (bảng cấp tổng hợp, tr. 6).
- Chia dữ liệu: ngày 1–1913 (29/01/2011–24/04/2016) là tập huấn luyện ban đầu; ngày 1914–1941 là validation; 28 ngày cuối (1942–1969) là test (tr. 5).
- Có biến ngoại sinh: lịch, giá bán, hoạt động khuyến mãi (tr. 5); SNAP ở 3 bang CA, TX, WI, mỗi bang 10 ngày/tháng (~33% số ngày) (tr. 6).
- **Phân loại theo Syntetos–Boylan** (tr. 7–8): dùng CV² và ADI với ngưỡng **0,5 và 4/3**; 30.490 chuỗi gồm **22.339 intermittent (73%), 5.206 lumpy (17%), 883 erratic (3%), 2.062 smooth (7%)**. Tác giả lưu ý ngưỡng này ban đầu dùng để so sánh các phương pháp dự báo cụ thể, sau này mới được dùng rộng rãi để phân 4 nhóm chuỗi (tr. 8).
- Các chuỗi không có mùa vụ hay xu hướng mạnh (tr. 7).

## Evaluation

- Accuracy: **WRMSSE**; Uncertainty: **WSPL** (weighted scaled pinball loss) (tr. 3).

## Results

- Bài mang tính giới thiệu, làm tài liệu nền cho kết quả hai nhánh thi (abstract). Kết quả nằm ở bài 02 và 03.

## Limitations

- Tác giả thừa nhận kết luận của M5 có giới hạn khi khái quát hóa ra ngoài dữ liệu mà nó đại diện (tr. 11).
- [Nhận định nhóm] Dữ liệu M5 không có tồn kho, lead time, chi phí; doanh số bằng 0 có thể do hết hàng.

## Relevance to our topic

[Nhận định nhóm] **Rất cao.** Nguồn chính thức cho mô tả dataset, và cho **tỷ lệ 4 nhóm nhu cầu** dùng trong phân tích ADI–CV² của đề tài.

## Possible improvement

[Nhận định nhóm] Dùng đúng ngưỡng 0,5 và 4/3 như bài này để kết quả so sánh được; báo cáo KPI tồn kho riêng cho từng nhóm.
