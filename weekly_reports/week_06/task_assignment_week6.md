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

### Member 4 - Evaluation Rubric + Comparison Plan
- [ ] Viết `evaluation_rubric.md`: 5 tiêu chí × 3 mức điểm (1/3/5)
- [ ] Viết `baseline_comparison_plan.md`: cách so sánh, metric, data test

**Output:** `docs/evaluation_rubric.md`, `docs/baseline_comparison_plan.md`

---

## Output chung cần nộp

| File | Người làm | Trạng thái |
|------|-----------|------------|
| `baseline_rule_based.py` | Member 1 (Nam) | ✅ Hoàn thành |
| `baseline_llm_only.md` | Member 2 (Huy) | ✅ Hoàn thành |
| `baseline_rag_only.py` | Member 3 (Bảo) | ✅ Hoàn thành |
| `baseline_proposed.py` | Member 3 (Bảo) | ✅ Hoàn thành |
| `baseline_comparison_plan.md` | Member 4 (Quy Đam) | ⏳ Chưa làm |
| `evaluation_rubric.md` | Member 4 (Quy Đam) | ⏳ Chưa làm |

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
- [ ] Có rubric đánh giá (Quy Đam - chưa làm)

---

## Tiến độ cập nhật (2026-06-21)

| Thành viên | Task | Trạng thái | Ghi chú |
|-----------|------|------------|---------|
| Nam (Mem1) | Rule-based Baseline | ✅ Hoàn thành | `baseline_rule_based.py` - 4 sensor types, JSON output |
| Huy (Mem2) | LLM-only Baseline | ✅ Hoàn thành | `baseline_llm_only.md` - prompt + 4 test cases + đánh giá |
| Bảo (Mem3) | RAG-only + Proposed | ✅ Hoàn thành | `baseline_rag_only.py` + `baseline_proposed.py` |
| Quy Đam (Mem4) | Evaluation Rubric + Comparison Plan | ⏳ Chưa làm | Cần hoàn thành |

**Files đã tổng hợp:** 4/6 files
**Files còn thiếu:** `evaluation_rubric.md`, `baseline_comparison_plan.md`
