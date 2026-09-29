# Paper List

Yêu cầu README (Bước 2): ≥ 5 bài liên quan trực tiếp, ≥ 3 bài về model/phương pháp AI, ≥ 2 bài về domain. Hiện có **13 + 4 + 2 = 19 bài**.

Mức liên quan: ★★★ = trụ cột, ★★ = hỗ trợ, ★ = tham khảo phụ.

## A. Liên quan trực tiếp (M5 / bán lẻ)

| No | Title | Authors | Year | Venue | Link | Mức |
|---|---|---|---|---|---|---|
| 01 | The M5 competition: Background, organization, and implementation | Makridakis, Spiliotis, Assimakopoulos | 2022 | Int. J. Forecasting 38(4):1325–1336 | [doi](https://doi.org/10.1016/j.ijforecast.2021.07.007) | ★★★ |
| 02 | M5 accuracy competition: Results, findings, and conclusions | Makridakis, Spiliotis, Assimakopoulos | 2022 | Int. J. Forecasting 38(4):1346–1364 | [doi](https://doi.org/10.1016/j.ijforecast.2021.11.013) | ★★★ |
| 03 | The M5 uncertainty competition: Results, findings and conclusions | Makridakis et al. | 2022 | Int. J. Forecasting 38(4):1365–1385 | [doi](https://doi.org/10.1016/j.ijforecast.2021.10.009) | ★★★ |
| 04 | Interpretability and Control in Forecasting Support Systems (preprint: "Algorithmic Transparency in Forecasting Support Systems") | Feddersen, Cleophas | 2026 | HICSS 2026 (preprint arXiv 2024) | [doi](https://doi.org/10.24251/HICSS.2026.172) · [arXiv](https://arxiv.org/abs/2411.00699) | ★★ |
| 05 | An Empirical Examination of Balancing Strategy for Counterfactual Estimation on Time Series | Huang et al. | 2024 | ICML | [2408.08815](https://arxiv.org/abs/2408.08815) | ★ |
| 06 | Foundation Models for Demand Forecasting via Dual-Strategy Ensembling | Yang, Cao, Liu | 2025 | KDD 2025 Workshop "AI for Supply Chain" | [2507.22053](https://arxiv.org/abs/2507.22053) | ★★ |
| 07 | The Forecast Critic: Leveraging LLMs for Poor Forecast Identification | Bhan et al. | 2025 | AAAI 2026 Workshop AI4TS | [2512.12059](https://arxiv.org/abs/2512.12059) | ★ |
| 08 | The cost of ensembling: is it always worth combining? | Zanotti | 2025 | arXiv | [2506.04677](https://arxiv.org/abs/2506.04677) | ★★ |
| 09 | Hierarchical Time Series Forecasting Via Latent Mean Encoding | Salatiello, Birr, Kunz | 2025 | arXiv | [2506.19633](https://arxiv.org/abs/2506.19633) | ★★ |
| 10 | Controllable Sequence Editing for Biological and Clinical Trajectories (CLEF) | Li et al. | 2025 | ICLR 2026 | [2502.03569](https://arxiv.org/abs/2502.03569) | ★ |
| 11 | Multi-objective probabilistic forecast combination for inventory demand | Wang, Kang, Spiliotis, Petropoulos | 2026 | arXiv | [2606.04900](https://arxiv.org/abs/2606.04900) | ★★★ (bài gần nhất) |
| 12 | Intermittent time series forecasting: local vs global models | Damato, Rubattu, Azzimonti, Corani | 2026 | arXiv (nộp JORS) | [2601.14031](https://arxiv.org/abs/2601.14031) | ★★★ |
| 13 | End-to-end probabilistic hierarchical forecasting of large hierarchies via probabilistic top-down | Zambon, Azzimonti, Corani | 2026 | arXiv | [2606.26774](https://arxiv.org/abs/2606.26774) | ★★ |

## B. Model / phương pháp AI

| No | Title | Authors | Year | Venue | Link | Mức |
|---|---|---|---|---|---|---|
| 14 | LightGBM: A Highly Efficient Gradient Boosting Decision Tree | Ke et al. | 2017 | NeurIPS 30 | [link](https://papers.nips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html) | ★★★ |
| 15 | Forecasting and stock control for intermittent demands | Croston | 1972 | JORS (Operational Research Quarterly) 23(3):289–303 | [doi](https://doi.org/10.1057/jors.1972.50) | ★★ |
| 16 | Intermittent demand: Linking forecasting to inventory obsolescence | Teunter, Syntetos, Babai | 2011 | EJOR 214(3):606–615 | [doi](https://doi.org/10.1016/j.ejor.2011.05.018) | ★★★ |
| 17 | DeepAR: Probabilistic forecasting with autoregressive recurrent networks | Salinas et al. | 2020 | Int. J. Forecasting 36(3):1181–1191 | [doi](https://doi.org/10.1016/j.ijforecast.2019.07.001) | ★★ |

## C. Domain quản lý kho

| No | Title | Authors | Year | Venue | Link | Mức |
|---|---|---|---|---|---|---|
| 18 | On the categorization of demand patterns | Syntetos, Boylan, Croston | 2005 | JORS 56(5):495–503 | [doi](https://doi.org/10.1057/palgrave.jors.2601841) | ★★★ |
| 19 | Optimising forecasting models for inventory planning | Kourentzes, Trapero, Barrow | 2020 | IJPE 225:107597 | [doi](https://doi.org/10.1016/j.ijpe.2019.107597) | ★★★ |

## Kiểm tra reference (2026-09-29)

Tất cả 19 link đã được kiểm tra tự động:

| Loại | Cách kiểm tra | Kết quả |
|---|---|---|
| 9 bài có DOI (01–03, 04, 15–19) | Crossref API (tên bài, tác giả, tạp chí, tập/số/trang); `doi.org` chuyển hướng đúng nhà xuất bản | ✅ Khớp. Link ScienceDirect (PII) của 01–03 trỏ đúng DOI |
| 10 bài arXiv (04–13) | arXiv API + HTTP (`/abs` và `/pdf` đều trả 200) | ✅ Đúng tên bài và tác giả |
| LightGBM (14) | Trang NeurIPS chính thức | ✅ Link cũ bị redirect nên đã thay bằng link chính thức |

Các chỉnh sửa sau kiểm tra:

- 04: đã xuất bản tại **HICSS 2026** với **tên mới** "Interpretability and Control in Forecasting Support Systems" và **thêm đồng tác giả Catherine Cleophas**. Khi trích dẫn phải dùng bản HICSS.
- 06: venue chính xác là Workshop "AI for Supply Chain: Today and Future" @ KDD 2025.
- 07: được trình bày tại **AAAI 2026 AI4TS workshop**.
- 15: DOI thuộc JORS; năm 1972 tạp chí còn tên *Operational Research Quarterly*.
- 11: 1.587 chuỗi bị loại là chuỗi **không có lịch sử** (toàn 0 ở giai đoạn tham chiếu), không phải mọi chuỗi nhu cầu thưa.

## Ghi chú

- Bài 08, 09, 11, 12, 13 vẫn **chưa qua phản biện** (chỉ có trên arXiv). Khi viết bài, nên ưu tiên trích dẫn bài tạp chí và kiểm tra xem bài arXiv đã có bản được xuất bản chính thức chưa.
- **Gợi ý đọc thêm (đã xác minh):** Goltsos, T. E., Syntetos, A. A., Glock, C. H., & Ioannou, G. (2022). Inventory–forecasting: Mind the gap. *European Journal of Operational Research*, 299(2), 397–419. https://doi.org/10.1016/j.ejor.2021.07.040. Theo abstract (OpenAlex): bài là **tổng quan có cấu trúc (structured review)** về tích hợp dự báo nhu cầu và kiểm soát tồn kho, đề xuất 4 mức tích hợp (từ bỏ qua đến hiểu đầy đủ tương tác), và chỉ ra rằng phần lớn nghiên cứu dự báo coi dự báo là mục tiêu tự thân mà bỏ qua bước chuyển thành quyết định nhập hàng. Rất nên đưa vào Introduction. *Chưa đọc toàn văn.*
- Nên bổ sung thêm 2–3 bài từ hội nghị mục tiêu (ví dụ KSE, SoICT, ACIIDS) để phản biện thấy bài phù hợp với venue.
