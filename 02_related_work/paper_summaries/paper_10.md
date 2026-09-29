# Paper 10 Summary

**Nhóm:** Direct (M5 / bán lẻ)

> Tóm tắt dựa trên abstract và ghi chú trong `M5_papers_baseline_gap.xlsx`. Cần đọc toàn văn để bổ sung số liệu chi tiết.

## Citation

Tên bài: Controllable Sequence Editing for Biological and Clinical Trajectories (CLEF)
Tác giả: Michelle M. Li, Kevin Li, Yasha Ektefaie, Ying Jin, Yepeng Huang, Shvat Messica, Tianxi Cai, Marinka Zitnik
Năm: 2025
Nguồn: ICLR 2026 (arXiv:2502.03569)
DOI/Link: https://arxiv.org/abs/2502.03569

## Problem

Sinh chuỗi có điều kiện với kiểm soát chính xác thời điểm và phạm vi tác động của can thiệp.

## Method

CLEF học các "temporal concept" mô tả cách và thời điểm điều kiện làm thay đổi chuỗi tương lai.

## Dataset

8 dataset (sinh học, lâm sàng, bán hàng); M5 với giá là điều kiện, chia theo bang (CA/TX/WI).

## Evaluation

MAE.

## Results

Cải thiện MAE trung bình 16,28% (chỉnh sửa tức thời), 26,73% (chỉnh sửa trễ), 62,84% (sinh chuỗi phản thực tế).

## Limitations

M5 không có ground-truth phản thực tế; mục tiêu chính là lĩnh vực y sinh.

## Relevance to our topic

**Thấp.** Chỉ gợi ý cách chia dữ liệu theo bang để kiểm tra khả năng tổng quát hóa.

## Possible improvement

Có thể thêm thí nghiệm train trên CA, test trên TX/WI (robustness).
