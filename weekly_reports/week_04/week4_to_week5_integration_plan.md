# Week 4 → Week 5 Integration Plan

## 1. Tổng quan

Tài liệu này mô tả kế hoạch tích hợp các module đã xây dựng trong **Week 4** (Sensor Pipeline + RAG Pipeline) để chuẩn bị cho **Week 5** (Agent Workflow).

---

## 2. Kiến trúc tổng thể sau Week 4

```
┌─────────────────────────────┐
│     Sensor Simulator        │ ← Nam
│  (sensor_simulator.py)      │
└─────────────┬───────────────┘
              │ POST /api/sensor-data
              ▼
┌─────────────────────────────┐
│      Sensor API (Flask)     │ ← Nam
│   (sensor_api/app.py)       │
└─────────────┬───────────────┘
              │ INSERT
              ▼
┌─────────────────────────────┐
│   PostgreSQL + TimescaleDB  │ ← Nam
│   (database/schema.sql)     │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐      ┌─────────────────────────────┐
│   RAG Retriever             │◄─────│   Vector DB (ChromaDB)      │ ← Huy
│   (rag_retriever.py)        │      │   (knowledge_base_docs/)    │
└─────────────┬───────────────┘      └─────────────────────────────┘
              │ POST /api/rag/query
              ▼
┌─────────────────────────────┐
│    RAG Query API (FastAPI)  │ ← Quý Đam
│   (rag_query_api/app.py)    │
└─────────────────────────────┘
```

---

## 3. Các module đã hoàn thành Week 4

| Module | File | Trạng thái |
|:---|---|:---:|
| Sensor Simulator | `sensor_simulator.py` | ✅ Nam |
| Sensor API | `sensor_api/app.py` | ✅ Nam |
| Database Schema | `database/schema.sql` | ✅ Nam |
| Sample Data | `sample_data/*.csv` | ✅ Nam |
| RAG Retriever | `rag_query_api/rag_retriever.py` | ✅ Quý Đam |
| RAG Query API | `rag_query_api/app.py` | ✅ Quý Đam |
| Evaluation Script | `rag_query_api/evaluate_rag.py` | ✅ Quý Đam |
| Integration Test | `rag_query_api/test_integration.py` | ✅ Quý Đam |
| RAG Ingest | `rag_ingest.py` | ⏳ Huy (đang chờ) |

---

## 4. Kế hoạch tích hợp Week 5

### 4.1. Agent Workflow sẽ cần gì từ Week 4?

Agent Workflow (Week 5) là module trung tâm sẽ:

```
1. Lấy sensor data mới nhất từ Sensor API / Database (Nam)
2. Gọi Data Quality Checker để kiểm tra chất lượng (Member 3)
3. Gọi RAG Query API để lấy kiến thức liên quan (Quý Đam)
4. Phân tích tổng hợp → Recommendation + Explanation (Agent)
5. Trả về JSON với confidence score, evidence
```

### 4.2. Interface tích hợp

#### A. Agent → Sensor API (lấy dữ liệu sensor)

```python
# Agent cần gọi:
GET http://localhost:5000/api/sensor-data/latest
# Trả về: List[sensor_reading]

GET http://localhost:5000/api/sensor-data/status
# Trả về: {sensor_type: {status: count}}
```

#### B. Agent → RAG Query API (lấy kiến thức)

```python
# Agent cần gọi:
POST http://localhost:8000/api/rag/query
{
    "query": "temperature 34C high greenhouse action",
    "k": 3
}
# Trả về: {success, query, evidence: [{source, chunk_id, relevance_score, text_snippet}]}
```

#### C. Agent → Data Quality Module (kiểm tra chất lượng) — Week 5

```python
# Agent cần gọi (sẽ xây trong Week 5):
data_quality_checker.check(reading) -> {missing, outlier, stuck, drift, conflict, quality_score}
```

### 4.3. Output JSON format cho Agent (Week 5)

```json
{
    "status": "warning",
    "detected_issue": "temperature_high",
    "sensor_quality_score": 0.82,
    "recommendation": {
        "action": "turn_on_fan",
        "level": 2,
        "duration_minutes": 10,
        "confidence": 0.86
    },
    "explanation": "Temperature has remained above the recommended range for 15 minutes.",
    "evidence": [
        {
            "source": "greenhouse_guidelines.pdf",
            "chunk_id": "chunk_12",
            "relevance_score": 0.91
        }
    ],
    "requires_human_approval": false
}
```

---

## 5. Project structure đề xuất cho Week 5

```
document/
└── IoT_Sensor_Pipeline/
    ├── sensor_simulator.py          # Week 4 - Nam
    ├── sensor_api/
    │   └── app.py                   # Week 4 - Nam
    ├── database/
    │   └── schema.sql               # Week 4 - Nam
    ├── sample_data/                 # Week 4 - Nam
    ├── rag_query_api/               # Week 4 - Quý Đam
    │   ├── __init__.py
    │   ├── app.py                   # RAG Query FastAPI
    │   ├── rag_retriever.py         # RAG retrieval logic
    │   ├── evaluate_rag.py          # Evaluation script
    │   └── test_integration.py      # Integration test
    ├── knowledge_base_docs/         # Week 4 - Huy (chờ)
    ├── rag_ingest.py                # Week 4 - Huy (chờ)
    ├── agent_service/               # 📁 Week 5 - Quý Đam
    │   ├── __init__.py
    │   ├── agent_workflow.py        # Agent logic
    │   └── app.py                   # Agent API
    ├── data_quality/                # 📁 Week 5 - Member 3
    │   ├── __init__.py
    │   └── quality_checker.py
    ├── baselines/                   # Week 6
    │   ├── rule_based.py
    │   ├── llm_only.py
    │   └── rag_only.py
    ├── requirements.txt
    ├── .env.example
    └── README.md
```

---

## 6. Timeline Week 5 (dự kiến)

| Thứ | Công việc | Người |
|:---:|---|---|
| Thứ 2 | Thiết kế Agent workflow, setup project structure | Quý Đam |
| Thứ 3 | Xây Data Quality Checker (missing, outlier, stuck, drift) | Member 3 |
| Thứ 4 | Xây Agent core logic (phân tích sensor + gọi RAG) | Quý Đam |
| Thứ 5 | Tích hợp Agent với Sensor API + RAG API | Quý Đam |
| Thứ 6 | Test agent với các scenario, viết demo_output.json | Quý Đam |
| Thứ 7 | Review + fix bugs | Cả nhóm |

---

## 7. Dependencies & Environment

### Python packages cần thêm cho Week 5

```txt
# Đã có trong requirements.txt:
chromadb==0.4.22
sentence-transformers==2.2.2
fastapi==0.104.1
uvicorn==0.24.0

# Cần thêm:
# langchain (nếu dùng LangChain cho Agent)
# openai / google-generativeai (nếu dùng LLM API)
```

### Environment variables cần thêm cho Week 5

```env
# RAG API (đã có)
RAG_API_HOST=0.0.0.0
RAG_API_PORT=8000
VECTOR_DB_PATH=./vector_db

# Agent (cần thêm)
AGENT_API_HOST=0.0.0.0
AGENT_API_PORT=9000
LLM_API_KEY=your_key_here
LLM_MODEL=gpt-4  # hoặc gemini-pro
```

---

## 8. Rủi ro và cách giảm thiểu

| Rủi ro | Tác động | Cách xử lý |
|:---|---|:---|
| Huy chưa có `rag_ingest.py` kịp | Agent không có vector DB thật | Agent dùng mock data tạm, swap sau |
| Member 3 chưa có Data Quality kịp | Agent thiếu module quality | Agent tự tính quality score tạm |
| Không có GPU cho embedding | Chậm | Dùng model nhỏ (all-MiniLM-L6-v2) |
| LLM API key chưa có | Agent không gọi được LLM | Dùng mock LLM hoặc template-based |

---

## 9. Checklist chuyển tiếp

- [ ] Sensor API đang chạy ở localhost:5000
- [ ] RAG Query API đang chạy ở localhost:8000
- [ ] Huy đã ingest tài liệu vào vector DB
- [ ] Member 3 đã có data quality checker
- [ ] Agent có thể gọi được Sensor API + RAG API
- [ ] Agent trả về JSON đúng format
- [ ] Cả nhóm đã biết luồng tích hợp
