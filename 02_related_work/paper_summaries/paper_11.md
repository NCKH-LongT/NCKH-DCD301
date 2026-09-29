# Paper 11 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Metadata và link **đã được kiểm tra (2026-09-29)** qua Crossref / arXiv API; link mở được. Tóm tắt dựa trên abstract, ghi chú `M5_papers_baseline_gap.xlsx` và đối chiếu PDF ở các chi tiết về dataset. Cần đọc toàn văn để bổ sung số liệu kết quả.

## Citation

Tên bài: Multi-objective probabilistic forecast combination for inventory demand
Tác giả: Shengjie Wang, Yanfei Kang, Evangelos Spiliotis, Fotios Petropoulos
Năm: 2026
Nguồn: arXiv:2606.04900
DOI/Link: https://arxiv.org/abs/2606.04900

## Problem

Kết hợp dự báo xác suất thường chỉ tối ưu độ chính xác thống kê, trong khi độ chính xác cao hơn không nhất thiết dẫn tới quyết định tồn kho tốt hơn, nhất là khi chi phí phi tuyến và có nhiều mục tiêu mâu thuẫn.

## Method

Bài toán kết hợp dự báo được đặt thành tối ưu đa mục tiêu (độ chính xác + hiệu quả quyết định tồn kho), sinh ra tập Pareto các trọng số kết hợp.

## Dataset

M5 (Walmart, ~60,1% quan sát bằng 0): loại 1.587 chuỗi **toàn số 0 trong giai đoạn tham chiếu nhưng có bán trong giai đoạn đánh giá** (không có lịch sử để dự báo), còn 28.903 chuỗi; và dữ liệu phụ tùng Royal Air Force. Horizon 28 ngày theo M5.

## Evaluation

Độ chính xác dự báo xác suất và 3 chỉ số tồn kho: tổng chi phí `c1·Holding + c2·Stockout`, tồn kho trung bình, lượng thiếu hàng. Mức order-up-to = phân vị τ của dự báo, τ = tỷ lệ tới hạn newsvendor. So sánh với mô hình đơn lẻ, trung bình đơn giản (SA) và tối ưu đơn mục tiêu.

## Results

Cách tiếp cận đa mục tiêu cho hiệu năng cân bằng và ổn định hơn các phương pháp so sánh.

## Limitations

Đánh giá tồn kho theo newsvendor **từng kỳ độc lập** (so phân vị với nhu cầu thực mỗi ngày), không có lead time và không mang tồn kho sang kỳ sau; không có quyết định xử lý hàng dư (thanh lý); không phân tích theo loại nhu cầu; loại 1.587 chuỗi không có lịch sử (cold-start); cần nhiều mô hình cơ sở để kết hợp.

## Relevance to our topic

**Rất cao. Đây là bài gần nhất với đề tài**, phải so sánh và phân biệt rõ trong Related Work.

## Possible improvement

Nhóm khác biệt ở chỗ: (1) **mô phỏng tồn kho nhiều kỳ** có lead time, chu kỳ đặt hàng và tồn kho mang sang; (2) quyết định **hai chiều** (nhập + thanh lý); (3) phân tích kết quả **theo nhóm nhu cầu ADI–CV²**; (4) một mô hình LightGBM quantile duy nhất thay vì kết hợp nhiều mô hình. Nhóm cũng nên trích dẫn Goltsos et al. (2022, EJOR) mà bài này dẫn.
