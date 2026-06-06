# Weekly Report - Week 4

## Group Information

- Class: SE1930
- Group: G07
- Leader:
- Members: Nguyễn Thành Quý Đam (Agent/Evaluation + RAG Engineer), Nam (IoT/Data Engineer), Huy (RAG Engineer - đã chuyển task cho Quý Đam), Member 3 (W4-ntb)

---

## Tasks Completed This Week

| Member | Task | Result |
|---|---|---|
| Nam (Member 1) | Sensor simulator + REST API + Database schema | ✅ Complete - 17 files, 4900+ LOC |
| Quý Đam (Member 2/4) | RAG Query API + pgvector + Evaluation | ✅ Complete - 10/10 eval passed, 7/7 integration passed |
| Huy | RAG Ingest (đã chuyển cho Quý Đam) | ✅ Merged into Quý Đam's work |
| Member 3 | Sensor API validation | ⚠️ Template only (DB `sensor_pipeline` chưa tạo) |

### Core Deliverables

**IoT Sensor Pipeline (Nam):**
- `sensor_simulator.py` - 12 sensors, 3 scenarios (normal/warning/critical), batch + continuous mode
- `sensor_api/app.py` - Flask REST API, 5 endpoints, PostgreSQL + TimescaleDB
- `database/schema.sql` - Hypertable + 3 tables (sensor_devices, sensor_alerts, data_quality_metrics)
- `sample_data/` - 3 CSV files (72 rows total): normal, warning, critical

**RAG Pipeline (Quý Đam + Huy):**
- `rag_ingest.py` - Chunk + embed + upsert vào PostgreSQL/pgvector
- `rag_query_api/` - FastAPI + pgvector retriever
- `knowledge_base_docs/` - 9 tài liệu kỹ thuật về nhà kính/nông nghiệp
- `rag_evaluation_week4.md` - 10/10 passed (Recall@3=0.95, MRR=1.0)
- `rag_query_test_results.md` - 7/7 integration test passed

---

## Git Commits

(Đang chờ commit vào branch SE1930_G07)

---

## Current Problems

1. **Database `sensor_pipeline` chưa được tạo trên PostgreSQL** → Member 3 không chạy được validation script, `api_test_report.md` và `db_validation_report.md` vẫn là template rỗng.
2. **sensor_pipeline DB name mismatch**: README.md hướng dẫn tạo DB tên `sensor_pipeline`, nhưng MCP config hiện trỏ vào `dcd_rag` (DB RAG của Quý Đam).
3. **validate_api_db_fixed.py chưa chạy được** vì Flask API server (port 5000) chưa chạy.
4. **RAG API đang dùng `all-mpnet-base-v2`** - cần xác nhận model embedding cuối cùng sẽ dùng trong production (hiện pgvector table đang dùng vector(384) phù hợp với `all-MiniLM-L6-v2`).

---

## Plan for Next Week (Week 5)

1. **Data Quality Module**: Xây `data_quality_checker.py` (missing, outlier, stuck, drift, conflict detection).
2. **Agent Workflow**: Xây `agent_workflow.py` - kết nối Sensor API + RAG API + Data Quality → trả về JSON recommendation.
3. **Tích hợp sensor_pipeline DB**: Tạo DB trên PostgreSQL hoặc đổi config để dùng `dcd_rag` shared DB.
4. **Baseline preparation**: Chuẩn bị structure cho rule-based, LLM-only, RAG-only baselines.

---

## Questions for Instructor

1. DB `sensor_pipeline` nên tạo riêng hay dùng chung `dcd_rag` cho cả sensor data và RAG?
2. validate_api_db_fixed.py có cần chạy lại với DB thật không, hay template là acceptable?
3. Model embedding cuối cùng: `all-mpnet-base-v2` (768d) hay `all-MiniLM-L6-v2` (384d)? Cần recreate index nếu đổi.
