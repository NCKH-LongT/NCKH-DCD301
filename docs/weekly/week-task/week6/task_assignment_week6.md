# Phân công Task Tuần 6 - Xây Baseline để so sánh

Dựa trên: `reference/repo_cua_thay/huong_dan_sinh_vien_aiot_agentic_rag.md` (Tuần 6)

---

## 4 Baseline cần xây

| Baseline | Mô tả |
|----------|-------|
| **Rule-based** | Nếu sensor vượt ngưỡng → cảnh báo/action |
| **LLM-only** | Đưa sensor data vào LLM, không dùng RAG |
| **RAG-only** | Dùng RAG nhưng không xét data quality |
| **Proposed Agentic RAG** | Hệ thống đầy đủ (data quality + RAG + agent) |

---

## Phân công

### Member 1 - Rule-based Baseline (Nam) ✅
- [x] Viết `baseline_rule_based.py`: if-else theo threshold từng sensor
- [x] Định nghĩa threshold: temp, humidity, soil_moisture, light
- [x] Output JSON đúng format (status, action, confidence)
- [x] Test với sample sensor data

**Output:** `code/baselines/baseline_rule_based.py` ✅

---

### Member 2 - LLM-only Baseline (Huy) ✅
- [x] Viết prompt đưa sensor data vào LLM (không RAG)
- [x] Chạy với các sample sensor data
- [x] Ghi lại output và prompt
- [x] Đánh giá ưu/nhược điểm

**Output:** `code/baselines/baseline_llm_only.md` (prompt + output) ✅

---

### Member 3 - RAG-only Baseline + Proposed System (Bảo) ✅
- [x] Viết `baseline_rag_only.py`: RAG query nhưng bỏ qua data quality
- [x] Tích hợp Proposed Agentic RAG từ code tuần 5 (data quality + RAG + agent)
- [x] Đảm bảo cả 2 đều output JSON đúng format

**Output:** `code/baselines/baseline_rag_only.py`, `code/baselines/baseline_proposed.py` ✅

---

### Member 4 - Evaluation Rubric + Comparison Plan (Quy Đam) ✅
- [x] Viết `evaluation_rubric.md`: 5 tiêu chí × 3 mức điểm (1/3/5)
- [x] Viết `baseline_comparison_plan.md`: cách so sánh, metric, data test

**Output:** `docs/weekly/week-task/week6/W6-quydam/evaluation_rubric.md` ✅
**Output:** `docs/weekly/week-task/week6/W6-quydam/baseline_comparison_plan.md` ✅

**Commit:** `c72507b` — đã push lên `origin/SE1930_G07` (2026-06-22)

---

## Output chung cần nộp

| File | Người làm | Trạng thái |
|------|-----------|------------|
| `baseline_rule_based.py` | Member 1 (Nam) | ✅ Hoàn thành |
| `baseline_llm_only.md` | Member 2 (Huy) | ✅ Hoàn thành |
| `baseline_rag_only.py` | Member 3 (Bảo) | ✅ Hoàn thành |
| `baseline_proposed.py` | Member 3 (Bảo) | ✅ Hoàn thành |
| `baseline_comparison_plan.md` | Member 4 (Quy Đam) | ✅ Hoàn thành (commit `c72507b`) |
| `evaluation_rubric.md` | Member 4 (Quy Đam) | ✅ Hoàn thành (commit `c72507b`) |

---

## Rubric đánh giá

| Tiêu chí | Điểm 1 | Điểm 3 | Điểm 5 |
|----------|--------|--------|--------|
| Correctness | Sai hoặc nguy hiểm | Tạm đúng | Đúng và an toàn |
| Context relevance | Không bám sensor/domain | Có bám một phần | Bám sát sensor + tài liệu |
| Explainability | Không giải thích | Giải thích chung chung | Có lý do + evidence |
| Actionability | Không có action rõ | Có action nhưng mơ hồ | Action rõ, có mức độ/thời gian |
| Safety | Có thể gây hại | Cần kiểm tra thêm | An toàn, biết khi nào cần human approval |

---

## Checklist

- [x] Có rule-based baseline (Nam ✅)
- [x] Có LLM-only baseline (Huy ✅)
- [x] Có RAG-only baseline (Bảo ✅)
- [x] Có proposed system (Bảo ✅)
- [x] Có rubric đánh giá (Quy Đam ✅ — commit `c72507b`)
- [x] Có comparison plan (Quy Đam ✅ — commit `c72507b`)

---

## Tiến độ cập nhật (2026-06-22)

| Thành viên | Task | Trạng thái | Ghi chú |
|-----------|------|------------|---------|
| Nam (Mem1) | Rule-based Baseline | ✅ Hoàn thành | `baseline_rule_based.py` - 4 sensor types, JSON output |
| Huy (Mem2) | LLM-only Baseline | ✅ Hoàn thành | `baseline_llm_only.md` - prompt + 4 test cases + đánh giá |
| Bảo (Mem3) | RAG-only + Proposed | ✅ Hoàn thành | `baseline_rag_only.py` + `baseline_proposed.py` |
| Quy Đam (Mem4) | Evaluation Rubric + Comparison Plan | ✅ Hoàn thành | `evaluation_rubric.md` (12.5 KB) + `baseline_comparison_plan.md` (20 KB) trong `W6-quydam/`. Đã push commit `c72507b` lên `origin/SE1930_G07` |

**Files đã tổng hợp:** 6/6 files ✅ **HOÀN THÀNH 100%**
**Trạng thái repo:** Branch `SE1930_G07` đã sync với origin — sẵn sàng cho Tuần 7
