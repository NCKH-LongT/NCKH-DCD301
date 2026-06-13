# Todo List - Member 3: Agent Workflow + RAG Integration

## Tuần 5 - Deadline: 2026-06-15

---

## Task 1: Agent Workflow Implementation
**Priority:** High | **Status:** ✅ Done

- [x] Nhận sensor data mới nhất từ database (72 readings, PostgreSQL `dcd_rag.sensor`)
- [x] Gọi data quality checker (checker.py — gộp 5 DQ modules + cross-sensor conflict)
- [x] Phân tích trạng thái hiện tại (State Analyzer → detected_issue: temperature_high/sensor_fault/...)
- [x] Gọi RAG để lấy tài liệu liên quan (RAGClient query_context → evidence list)
- [x] Tạo recommendation dựa trên context (action/level/duration lookup table)
- [x] Gắn confidence score (4-term formula: 0.4×SQS + 0.3×RAG + 0.2×Rule + 0.1×Historical)
- [x] Trả về JSON có explanation và evidence (đầy đủ mentor spec fields)

**Output:** `src/agent/agent_workflow.py` ✅

---

## Task 2: RAG Query Integration
**Priority:** High | **Status:** ✅ Done

- [x] Kết nối với PGVector (`dcd_rag.knowledge_base` với pgvector)
- [x] Viết hàm query RAG với context từ sensor data (RAGClient.query_context)
- [x] Xử lý trường hợp RAG không tìm thấy document liên quan (trả về evidence rỗng)
- [x] Đảm bảo query trả về: source, chunk_id, relevance_score

**Output:** `src/rag/rag_client.py` ✅

---

## Task 3: Agent Service
**Priority:** High | **Status:** ⏳ Phase 2

- [ ] Viết agent_service.py làm entry point
- [ ] Cung cấp API endpoint cho agent
- [ ] Xử lý error cases
- [ ] Logging cho debugging

**Output:** `src/agent/agent_service.py` — đợi Member 4 confidence + review toàn team

---

## Task 4: Unit Tests
**Priority:** Medium | **Status:** ✅ Done

- [x] Test checker.py: 6 tests (empty, keys, null, outlier, cross-sensor, state)
- [x] Test RAGClient: 3 tests (init, empty format, evidence keys)
- [x] Test agent_workflow.py: 8 tests (mock workflow + 4 real DB integration)
- [x] 89/89 tests passed (3.3s unit + 14s integration)

---

## LỘ TRÌNH LÀM TRƯỚC (Không đợi thành viên khác)

### ✅ Phase 1 Hoàn thành — Output khớp schema mentor

**1.1. Thiết kế Agent Output JSON Schema**
- [x] Định nghĩa structure output — khớp mentor spec (Requirement-of-Mentor.md lines 264-286)
- [x] Required fields: status, detected_issue, sensor_quality_score, recommendation, explanation, evidence, requires_human_approval, confidence
- [x] Thống nhất format: confidence là dict chứ không phải float đơn

**1.2. Tích hợp thực tế (không skeleton, không mock)**
- [x] Tích hợp real checker.py (gộp missing_data + outlier + sensor_stuck + sensor_drift + timestamp_delay + cross_sensor_conflict)
- [x] Tích hợp real RAGRetriever từ Week 4 (pgvector + sentence-transformers)
- [x] Tích hợp real DB (PostgreSQL `dcd_rag.sensor`)
- [x] 72 readings thật, 176 knowledge_base chunks thật

**Output hoàn chỉnh:**
- `src/data_quality/checker.py` — State Analyzer + recommendation builder
- `src/rag/rag_client.py` — RAG wrapper với evidence format
- `src/agent/agent_workflow.py` — full 7-step workflow
- `tests/test_agent_workflow.py` — 17 tests (unit + integration)
- `docs/agent_workflow.html` — pipeline visualization

---

### ⏳ Phase 2: Agent Service + Documentation

**2.1. Agent Service API**
- [ ] `src/agent/agent_service.py` (FastAPI endpoint `/agent/recommend`)
- [ ] Chờ Member 4 review confidence_score + toàn team thống nhất interface

**2.2. Documentation (Week 5 deliverables)**
- [ ] `docs/confidence_score.md` (Member 4 lo)
- [ ] `docs/agent_workflow.md` (Member 3 + 4)
- [ ] `demo_output.json` (Member 4 lo)

---

## Progress Log

| Date | Task | Status | Notes |
|------|------|--------|-------|
| 2026-06-09 | Phase 1.1: Schema Design | ✅ Xong | Không đợi ai |
| 2026-06-09 | Phase 1.2: Service Skeleton | ✅ Xong (thay = real code luôn) | Không đợi ai |
| 2026-06-09 | Phase 2.1: Mock Functions | ✅ Bỏ qua | Đi thẳng real code |
| 2026-06-09 | Phase 2.2: Workflow with Mocks | ✅ Bỏ qua | Real integration sẵn |
| 2026-06-09 | Task 1: Agent Workflow | ✅ Done | 3 files hoàn chỉnh |
| 2026-06-09 | Task 2: RAG Integration | ✅ Done | Tích hợp với RAGRetriever Week 4 |
| 2026-06-09 | Task 3: Agent Service | ⏳ Phase 2 | Chờ team review |
| 2026-06-09 | Task 4: Unit Tests | ✅ Done | 17 tests, 89/89 passed |
| 2026-06-13 | So sánh mentor spec | ✅ Done | Output JSON schema khớp 100% |
| 2026-06-13 | Cross-sensor conflict | ✅ Done | temp diff >5°C, hum diff >15% |
| 2026-06-13 | Confidence formula (4-term) | ✅ Done | 0.4×SQS + 0.3×RAG + 0.2×Rule + 0.1×Historical |
| 2026-06-13 | Cập nhật task_assignment | ✅ Done | Thêm member3 progress section |
| 2026-06-13 | HTML visualization | ✅ Done | docs/agent_workflow.html |

---

## Action Items còn lại

1. ~~Trao đổi với Member 1 & 2~~ ✅ Đã tích hợp xong
2. **Trao đổi với Member 4:** Để họ replace `historical_stability` placeholder (hiện = 0.5)
3. ~~Lấy code RAG tuần 4~~ ✅ Đã copy và tích hợp
4. **Họp nhóm:** Review toàn bộ integration trước khi push lên repo mentor `SE1930_G07`

---

## Notes

- Tham khảo `docs\project\Requirement-of-Mentor.md` phần Week 5 (lines 264-286 output schema, 342-367 workflow, 377-386 confidence)
- Agent workflow đã emit events (logging) qua logger
- 89 tests passed trong 18s
- HTML viz: `python -m http.server -d docs/` → mở `agent_workflow.html`