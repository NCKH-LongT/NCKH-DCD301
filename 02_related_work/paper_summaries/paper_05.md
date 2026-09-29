# Paper 05 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Metadata và link **đã được kiểm tra (2026-09-29)** qua Crossref / arXiv API; link mở được. Tóm tắt dựa trên abstract, ghi chú `M5_papers_baseline_gap.xlsx` và đối chiếu PDF ở các chi tiết về dataset. Cần đọc toàn văn để bổ sung số liệu kết quả.

## Citation

Tên bài: An Empirical Examination of Balancing Strategy for Counterfactual Estimation on Time Series
Tác giả: Qiang Huang, Chuizheng Meng, Defu Cao, Biwei Huang, Yi Chang, Yan Liu
Năm: 2024
Nguồn: ICML 2024 (arXiv:2408.08815)
DOI/Link: https://arxiv.org/abs/2408.08815

## Problem

Các chiến lược cân bằng (balancing) dùng để giảm sai lệch do can thiệp (treatment bias) có thực sự hiệu quả với dữ liệu chuỗi thời gian không?

## Method

Khảo sát thực nghiệm các phương pháp cân bằng dựa trên ERM trong ước lượng phản thực tế (counterfactual) theo thời gian.

## Dataset

Nhiều dataset; M5 được tái cấu trúc với giá là biến can thiệp và doanh số là kết quả.

## Evaluation

Sai số trên kết quả quan sát được (factual outcome).

## Results

Chiến lược cân bằng không phải lúc nào cũng cải thiện ước lượng trên chuỗi thời gian; cần xem xét lại việc áp dụng mặc định.

## Limitations

Dữ liệu thật không có ground-truth phản thực tế nên không kiểm chứng đầy đủ được.

## Relevance to our topic

**Thấp.** Chỉ liên quan gián tiếp: cho thấy giá có tác động nhân quả tới doanh số, điều liên quan đến quyết định giảm giá/thanh lý.

## Possible improvement

Ngoài phạm vi. Có thể nhắc ở Future Work: ước lượng tác động của giảm giá tới lượng hàng thanh lý được.
