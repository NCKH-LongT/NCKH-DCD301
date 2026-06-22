# 05_methodology

Folder này chứa các tài liệu về **phương pháp luận** (Tuần 5 + 6).

## File cần có (theo cấu trúc nhánh `main`)

| File | Mô tả | Trạng thái |
|---|---|---|
| `methodology.md` | Mô tả phương pháp tổng thể | 🔶 Nội dung trong `docs/project/agent_context.md` |
| `baseline.md` | Mô tả các baseline so sánh | ✅ Có (file baseline nằm trong `weekly_reports/week_06/code/baselines/`) |
| `dataset.md` | Mô tả dataset sử dụng | 🔶 Có trong `weekly_reports/week_04/sample_data/` |
| `evaluation_metrics.md` | Metric đánh giá | ✅ Có (rubric & comparison plan) |

## Mapping từ repo cũ

| File nguồn | File đích |
|---|---|
| `weekly_reports/week_06/code/baselines/baseline_rule_based.py` | (ref) `05_methodology/baseline.md` |
| `weekly_reports/week_06/code/baselines/baseline_llm_only.md` | (ref) `05_methodology/baseline.md` |
| `weekly_reports/week_06/code/baselines/baseline_rag_only.py` | (ref) `05_methodology/baseline.md` |
| `weekly_reports/week_06/code/baselines/baseline_proposed.py` | (ref) `05_methodology/baseline.md` |
| `weekly_reports/week_04/sample_data/*.csv` | (ref) `05_methodology/dataset.md` |
| `docs/weekly/week-task/week6/W6-quydam/evaluation_rubric.md` | (ref) `05_methodology/evaluation_metrics.md` |
| `docs/weekly/week-task/week6/W6-quydam/baseline_comparison_plan.md` | (ref) `05_methodology/evaluation_metrics.md` |

## Hành động cần làm

1. Tạo `methodology.md` tổng hợp phương pháp từ `agent_context.md` + baseline files
2. Tạo `baseline.md` mô tả 4 baseline (rule-based, LLM-only, RAG-only, proposed)
3. Tạo `dataset.md` mô tả normal/warning/critical sample data
4. Tạo `evaluation_metrics.md` tổng hợp rubric + comparison plan
