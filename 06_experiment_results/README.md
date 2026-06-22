# 06_experiment_results

Folder này chứa **kết quả thí nghiệm** (Tuần 7).

## Cấu trúc

```
06_experiment_results/
├── experimental_setup.md         ❌ Chưa có
├── results.md                    ❌ Chưa có
├── figures/                      🔶 Trống (sẽ chứa biểu đồ)
├── tables/                       🔶 Trống (sẽ chứa bảng kết quả)
└── tests/                        ✅ Có sẵn 6 test files
```

## Trạng thái hiện tại

| File yêu cầu | Trạng thái |
|---|---|
| `experimental_setup.md` | ❌ Chưa có |
| `results.md` | ❌ Chưa có |
| `tests/test_*.py` (6 files) | ✅ Có đủ |
| `figures/*.png` | 🔶 Chưa có biểu đồ |
| `tables/*.csv` | 🔶 Chưa có bảng kết quả |

## Hành động cần làm

1. Sau khi chạy baseline (Tuần 7), tạo:
   - `result_rule_based.csv`, `result_llm_only.csv`, `result_rag_only.csv`, `result_proposed.csv`
   - `metrics_summary.csv`
   - `failure_analysis.md`
2. Đặt vào folder `tables/`
3. Vẽ biểu đồ (bar chart, heatmap) vào `figures/`
4. Viết `experimental_setup.md` và `results.md`
