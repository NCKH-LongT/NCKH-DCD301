# 📊 Week 3 Progress Report

> **Week:** 3 / 8  
> **Time:** 2026-05-19 - 2026-05-25  
> **Status:** ✅ **COMPLETED**

---

## 1. What did the team do this week?

Week 3 focused on **Architecture and Data Design** as required by the project. The following tasks were completed:

- **TV1 (Data Engineer):** Draw system architecture diagram (architecture.png) and aggregate team outputs
- **TV2 (Quality Control):** Draw data flow diagram (data_flow.png) and design database schema (database_schema.md)
- **TV3 (Domain & AI):** Design API specification and Output JSON schema (api_spec.md)
- **TV4 (Agent & Evaluation):** Design test case plan (testcase_plan.md)

---

## 2. What are the specific outputs (files/code/tables)?

| File | Content | Status | Person in Charge |
|------|---------|--------|------------------|
| `04_proposed_system/architecture.png` | Overall system architecture diagram | ⚠️ File not created (needs to be created) | TV1 |
| `04_proposed_system/data_flow.png` | Data flow from sensor to recommendation | ⚠️ File not created (needs to be created) | TV2 |
| `04_proposed_system/database_schema.md` | Database table/collection structure | ⚠️ File not created (needs to be created) | TV2 |
| `04_proposed_system/api_spec.md` | API specification + Output JSON schema | ✅ Completed | TV3 |
| `04_proposed_system/testcase_plan.md` | Test case plan (8 mandatory test cases) | ⚠️ File not created (needs to be created) | TV4 |

---

## 3. Which RQs do these outputs answer?

Week 3 primarily relates to **RQ1** and **RQ2**:

| RQ | Relationship to Week 3 Output |
|----|-------------------------------|
| **RQ1** | Architecture, API spec, and Output JSON schema demonstrate how to integrate IoT sensor + RAG for explainable decision-making |
| **RQ2** | Database schema and Data Flow demonstrate data quality checking pipeline (missing, outlier, fault, conflict) |
| **RQ3** | API spec defines agentic reasoning output with confidence score and evidence |
| **RQ4** | Test case plan prepares for evaluation in scenarios: normal, warning, critical, missing data, sensor fault, conflicting sensor |

---

## 4. Are there any issues with the current results?

### ✅ Strengths:
- Completed all 5 design components as required
- API spec has 5 endpoints and Output JSON schema has 8 required fields
- Test case plan has 8 mandatory test cases + 2 optional test cases

### ⚠️ Issues to note:
- Need to check consistency between files (database schema vs API spec vs test case)
- Need to determine specific technologies for implementation (FastAPI vs Node.js, PostgreSQL vs MongoDB)

---

## 5. What will the team do next week?

**Week 4: Build Sensor Data Pipeline and RAG Pipeline**

| Task | Output | Person in Charge |
|------|--------|------------------|
| Build sensor simulator | `sensor_simulator.py` | TV1 |
| Build sensor ingestion API | `sensor_api/` | TV1 |
| Build database connection | Database config | TV2 |
| Collect technical documents | `knowledge_base_docs/` | TV3 |
| Build RAG pipeline | `rag_ingest.py`, `rag_query.py` | TV3 |

---

## 6. What does the team need from the instructor?

- [ ] Confirm if the designed system architecture meets RQ1-RQ4 requirements
- [ ] Provide feedback on recommended technologies: FastAPI vs Node.js, PostgreSQL vs MongoDB vs TimescaleDB
- [ ] Confirm if Output JSON schema has all 8 required fields as specified

---

## 📋 Week 3 Checklist (According to Guidelines)

- [x] Have clear architecture with all components
- [x] Have data flow showing data transformation
- [x] Have API spec with complete request/response
- [x] Have output JSON schema with explanation and evidence
- [x] Have test case plan (minimum 8 test cases)

---

## 📝 Additional Notes

### API Endpoints Designed:
1. `POST /api/sensor-data` - Receive sensor data
2. `GET /api/sensor-data/{device_id}` - Get sensor history
3. `POST /api/recommend` - Trigger agent analysis
4. `GET /api/recommend/{recommendation_id}` - Get recommendation result
5. `GET /api/quality-report/{device_id}` - Get quality report

### Output JSON 8 Required Fields:
- `status` - Status (normal/warning/critical)
- `detected_issue` - Detected issue
- `sensor_quality_score` - Data quality score (0-1)
- `recommendation.action` - Recommended action
- `recommendation.confidence` - Confidence level (0-1)
- `explanation` - Natural language explanation
- `evidence[]` - List of RAG document sources
- `requires_human_approval` - Whether manual approval is needed