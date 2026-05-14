# Hướng dẫn từng bước cho sinh viên thực hiện đề tài

## Đề tài đề xuất

**A Data Quality-Aware Agentic RAG Framework for Real-Time AIoT Decision Support in Smart Agriculture**

---

## 1. Mục tiêu của đề tài

Sinh viên cần xây dựng một hệ thống AIoT hỗ trợ ra quyết định trong nông nghiệp thông minh. Hệ thống phải có khả năng:

1. Nhận dữ liệu cảm biến IoT theo thời gian thực.
2. Kiểm tra chất lượng dữ liệu cảm biến.
3. Phát hiện dữ liệu thiếu, lỗi, bất thường hoặc mâu thuẫn.
4. Truy xuất tri thức nông nghiệp từ tài liệu kỹ thuật bằng RAG.
5. Dùng Agentic RAG để phân tích tình huống và đưa ra khuyến nghị.
6. Giải thích vì sao hệ thống đưa ra khuyến nghị đó.
7. So sánh hệ thống đề xuất với các baseline như rule-based, LLM-only và RAG-only.
8. Đánh giá hệ thống trong các kịch bản bình thường, thiếu dữ liệu, lỗi sensor và sensor mâu thuẫn.

---

## 2. Research Questions

### RQ1

**How can real-time IoT sensor data be integrated with domain-specific agricultural knowledge to support explainable decision-making in smart agriculture?**

Mục tiêu:

- Thiết kế cách tích hợp dữ liệu sensor thời gian thực với tài liệu kỹ thuật nông nghiệp.
- Tạo pipeline RAG để truy xuất kiến thức phù hợp.
- Tạo output có giải thích và evidence.

### RQ2

**How does sensor data quality affect the reliability of AIoT-based agricultural recommendations?**

Mục tiêu:

- Kiểm tra dữ liệu sensor có thiếu, nhiễu, lỗi hoặc mâu thuẫn không.
- Tính điểm tin cậy dữ liệu.
- Phân tích dữ liệu lỗi ảnh hưởng thế nào đến khuyến nghị của AI.

### RQ3

**Can an Agentic RAG framework improve the contextual relevance and explainability of agricultural decision support compared with rule-based or LLM-only approaches?**

Mục tiêu:

- Xây hệ thống đề xuất Agentic RAG.
- Xây các baseline để so sánh.
- Đánh giá xem Agentic RAG có cải thiện độ đúng, độ liên quan ngữ cảnh và khả năng giải thích hay không.

### RQ4

**How effective is the proposed framework under normal, missing-data, sensor-fault, and conflicting-sensor scenarios?**

Mục tiêu:

- Tạo các kịch bản test.
- Chạy hệ thống trong nhiều tình huống khác nhau.
- Đo accuracy, confidence, latency, explanation score và failure cases.

---

## 3. Phạm vi đề tài cần chốt

Sinh viên không nên làm quá rộng là “smart agriculture”. Cần chọn một domain cụ thể.

### Các domain gợi ý

| Domain | Sensor có thể dùng | Action có thể khuyến nghị |
|---|---|---|
| Smart greenhouse | Temperature, humidity, soil moisture, light | Bật quạt, tưới nước, bật đèn, cảnh báo |
| Smart irrigation | Soil moisture, temperature, humidity, rain forecast | Tưới / không tưới / trì hoãn tưới |
| Egg incubator | Temperature, humidity, turning speed | Tăng/giảm nhiệt, tăng/giảm ẩm, kiểm tra motor đảo trứng |
| Poultry farm | Temperature, humidity, NH3, CO2 | Bật quạt, tăng thông gió, cảnh báo môi trường |
| Aquaculture | Water temperature, pH, dissolved oxygen | Bật sục khí, thay nước, cảnh báo pH |

### Khuyến nghị chọn phạm vi

Nếu sinh viên mới bắt đầu, nên chọn một trong hai hướng:

1. **Smart greenhouse monitoring**
2. **Egg incubator monitoring**

Vì hai hướng này dễ mô phỏng sensor, dễ tạo test case và dễ demo.

---

## 4. Kiến trúc hệ thống cần xây

```text
IoT Sensor / Sensor Simulator
        ↓
Data Ingestion API
        ↓
Time-series Database / Storage
        ↓
Sensor Data Quality Module
        ↓
State Analyzer
        ↓
RAG Knowledge Base
        ↓
Agentic Reasoning Workflow
        ↓
Recommendation + Explanation + Confidence Score
        ↓
Dashboard / API Response / Control Action
```

---

## 5. Thành phần bắt buộc của hệ thống

| Thành phần | Bắt buộc | Mô tả |
|---|---|---|
| Sensor simulator hoặc IoT device thật | Có | Sinh dữ liệu sensor theo thời gian thực |
| API nhận dữ liệu sensor | Có | Nhận dữ liệu qua REST/MQTT/WebSocket |
| Database lưu sensor data | Có | Có thể dùng PostgreSQL, MongoDB, TimescaleDB |
| Data quality module | Có | Kiểm tra missing, outlier, drift, conflict |
| RAG pipeline | Có | Nạp tài liệu kỹ thuật, chunking, embedding, vector DB |
| Agent workflow | Có | Phân tích tình huống và gọi các module cần thiết |
| Recommendation output | Có | Trả về JSON có status, action, confidence, evidence |
| Baseline comparison | Có | Rule-based, LLM-only, RAG-only |
| Evaluation test cases | Có | Normal, warning, critical, missing, fault, conflict |

---

## 6. Chia vai trò trong nhóm

### Nếu nhóm có 5 sinh viên

| Vai trò | Công việc |
|---|---|
| Student 1 - IoT/Data Engineer | Sensor simulator, API nhận dữ liệu, database |
| Student 2 - Data Quality Engineer | Missing data, outlier, sensor fault, conflict detection |
| Student 3 - RAG Engineer | Thu thập tài liệu, chunking, embedding, vector database |
| Student 4 - Agent/Evaluation Engineer | Agent workflow, baseline, test case, metrics |
| Student 5 - Paper/System Integrator | Viết paper, tổng hợp kết quả, vẽ kiến trúc, làm slide |

### Nếu nhóm có 3 sinh viên

| Vai trò | Công việc |
|---|---|
| Student 1 | IoT data + data quality |
| Student 2 | RAG + Agent workflow |
| Student 3 | Evaluation + paper writing |

---

## 7. Timeline thực hiện 8 tuần

## Tuần 1: Chốt phạm vi và hiểu RQ

### Việc cần làm

1. Đọc và giải thích 4 RQ bằng tiếng Việt.
2. Chọn domain cụ thể.
3. Chọn sensor cần dùng.
4. Chọn action hệ thống có thể khuyến nghị.
5. Xác định dữ liệu đầu vào và đầu ra.

### Output cần nộp

| File | Nội dung |
|---|---|
| `rq_explanation.md` | Giải thích từng RQ bằng tiếng Việt |
| `domain_scope.md` | Domain đã chọn và lý do chọn |
| `sensor_action_table.md` | Bảng sensor, ý nghĩa, action liên quan |
| `system_output_schema.json` | Cấu trúc JSON output dự kiến |

### Checklist tuần 1

- [ ] Đã chọn domain cụ thể.
- [ ] Đã liệt kê sensor.
- [ ] Đã liệt kê action.
- [ ] Đã hiểu 4 RQ.
- [ ] Đã xác định output hệ thống.

---

## Tuần 2: Literature Review và Gap Analysis

### Việc cần làm

1. Mỗi sinh viên đọc 3–5 bài báo liên quan.
2. Phân loại bài báo theo nhóm:
   - IoT/AIoT smart agriculture.
   - RAG/LLM decision support.
   - Sensor data quality/anomaly detection.
   - Edge-AIoT nếu có.
   - Smart irrigation/greenhouse/incubator nếu đúng domain.
3. Tạo literature review matrix.
4. Xác định gap nghiên cứu.
5. Chốt contribution của đề tài.

### Output cần nộp

| File | Nội dung |
|---|---|
| `literature_review_matrix.md` | Bảng tổng hợp bài báo |
| `research_gap.md` | Gap nghiên cứu chính |
| `related_work_summary.md` | Tóm tắt các nhóm bài liên quan |
| `contribution.md` | Các contribution dự kiến |

### Template literature review matrix

| Paper | Year | Venue | Problem | Method | Dataset/System | Limitation | Relation to our work |
|---|---:|---|---|---|---|---|---|

### Checklist tuần 2

- [ ] Mỗi sinh viên đã đọc ít nhất 3 bài.
- [ ] Có matrix tổng hợp.
- [ ] Có gap rõ.
- [ ] Có contribution rõ.
- [ ] Biết bài của mình khác gì bài cũ.

---

## Tuần 3: Thiết kế kiến trúc và dữ liệu

### Việc cần làm

1. Vẽ system architecture.
2. Vẽ data flow.
3. Thiết kế database schema.
4. Thiết kế API nhận sensor.
5. Thiết kế output JSON.
6. Thiết kế test case ban đầu.

### Output cần nộp

| File | Nội dung |
|---|---|
| `architecture.png` | Sơ đồ kiến trúc hệ thống |
| `data_flow.png` | Luồng dữ liệu từ sensor đến recommendation |
| `database_schema.md` | Cấu trúc bảng/collection |
| `api_spec.md` | Đặc tả API |
| `testcase_plan.md` | Kế hoạch test case |

### API nhận sensor gợi ý

```http
POST /api/sensor-data
Content-Type: application/json
```

```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-14T10:30:00Z",
  "temperature": 34.2,
  "humidity": 78,
  "soil_moisture": 25,
  "light": 820
}
```

### Output recommendation gợi ý

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
      "source": "greenhouse_guideline.pdf",
      "chunk_id": "chunk_12",
      "relevance_score": 0.91
    }
  ],
  "requires_human_approval": false
}
```

### Checklist tuần 3

- [ ] Có architecture.
- [ ] Có data flow.
- [ ] Có API spec.
- [ ] Có output schema.
- [ ] Có kế hoạch test case.

---

## Tuần 4: Xây dựng Sensor Data Pipeline và RAG Pipeline

### Việc cần làm

#### Phần sensor data

1. Xây sensor simulator hoặc kết nối thiết bị thật.
2. Gửi dữ liệu định kỳ vào API.
3. Lưu dữ liệu vào database.
4. Tạo dữ liệu normal/warning/critical.

#### Phần RAG

1. Thu thập tài liệu kỹ thuật.
2. Chuyển PDF/doc sang text.
3. Chunking tài liệu.
4. Embedding tài liệu.
5. Lưu vào vector database.
6. Tạo API query RAG.

### Output cần nộp

| File/Module | Nội dung |
|---|---|
| `sensor_simulator.py/js` | Sinh dữ liệu sensor |
| `sensor_api` | API nhận và lưu sensor |
| `rag_ingest.py/js` | Nạp tài liệu vào vector DB |
| `rag_query.py/js` | Truy vấn tài liệu |
| `sample_sensor_data.csv` | Dữ liệu mẫu |
| `knowledge_base_docs/` | Tài liệu kỹ thuật đã thu thập |

### Checklist tuần 4

- [ ] API nhận sensor chạy được.
- [ ] Sensor simulator chạy được.
- [ ] Dữ liệu được lưu vào database.
- [ ] Tài liệu được ingest vào vector DB.
- [ ] Query RAG trả về đoạn tài liệu liên quan.

---

## Tuần 5: Xây Data Quality Module và Agent Workflow

### Việc cần làm

#### Data quality module

Xây các hàm kiểm tra:

1. Missing data.
2. Outlier.
3. Sensor stuck.
4. Sensor drift.
5. Timestamp delay.
6. Cross-sensor conflict.

#### Agent workflow

Agent cần thực hiện các bước:

1. Nhận sensor data mới nhất.
2. Gọi data quality checker.
3. Phân tích trạng thái hiện tại.
4. Gọi RAG để lấy tài liệu liên quan.
5. Tạo recommendation.
6. Gắn confidence score.
7. Trả về JSON có explanation và evidence.

### Output cần nộp

| File/Module | Nội dung |
|---|---|
| `data_quality_checker.py/js` | Module kiểm tra chất lượng dữ liệu |
| `confidence_score.md` | Công thức tính confidence |
| `agent_workflow.md` | Mô tả workflow agent |
| `agent_service.py/js` | Code agent |
| `demo_output.json` | Output mẫu của hệ thống |

### Công thức confidence gợi ý

```text
Final Confidence =
0.4 × Sensor Quality Score
+ 0.3 × RAG Relevance Score
+ 0.2 × Rule Consistency Score
+ 0.1 × Historical Stability Score
```

### Checklist tuần 5

- [ ] Phát hiện được missing data.
- [ ] Phát hiện được outlier.
- [ ] Phát hiện được sensor fault.
- [ ] Phát hiện được conflicting sensor.
- [ ] Agent gọi được data quality module.
- [ ] Agent gọi được RAG.
- [ ] Output có explanation và evidence.

---

## Tuần 6: Xây Baseline để so sánh

### Việc cần làm

Sinh viên phải xây ít nhất 3 baseline:

| Baseline | Mô tả |
|---|---|
| Rule-based | Nếu sensor vượt ngưỡng thì cảnh báo/action |
| LLM-only | Đưa sensor data vào LLM, không dùng RAG |
| RAG-only | Dùng RAG nhưng không xét data quality |
| Proposed Agentic RAG | Hệ thống đầy đủ có data quality + RAG + agent |

### Output cần nộp

| File/Module | Nội dung |
|---|---|
| `baseline_rule_based.py/js` | Baseline rule-based |
| `baseline_llm_only.md` | Prompt và output LLM-only |
| `baseline_rag_only.py/js` | Baseline RAG-only |
| `baseline_comparison_plan.md` | Kế hoạch so sánh |
| `evaluation_rubric.md` | Rubric chấm output |

### Rubric đánh giá recommendation

| Tiêu chí | Điểm 1 | Điểm 3 | Điểm 5 |
|---|---|---|---|
| Correctness | Sai hoặc nguy hiểm | Tạm đúng | Đúng và an toàn |
| Context relevance | Không bám sensor/domain | Có bám một phần | Bám sát sensor + tài liệu |
| Explainability | Không giải thích | Giải thích chung chung | Có lý do + evidence |
| Actionability | Không có action rõ | Có action nhưng mơ hồ | Action rõ, có mức độ/thời gian |
| Safety | Có thể gây hại | Cần kiểm tra thêm | An toàn, biết khi nào cần human approval |

### Checklist tuần 6

- [ ] Có rule-based baseline.
- [ ] Có LLM-only baseline.
- [ ] Có RAG-only baseline.
- [ ] Có proposed system.
- [ ] Có rubric đánh giá.

---

## Tuần 7: Chạy thí nghiệm và đánh giá

### Việc cần làm

1. Tạo bộ test case.
2. Chạy từng baseline trên cùng bộ test case.
3. Ghi kết quả.
4. Tính metric.
5. Phân tích trường hợp hệ thống sai.
6. Tạo bảng kết quả và biểu đồ.

### Test case bắt buộc

| Test case | Mô tả | Kỳ vọng |
|---|---|---|
| TC1 - Normal | Sensor bình thường | Không cảnh báo sai |
| TC2 - Warning | Sensor lệch nhẹ | Cảnh báo nhẹ |
| TC3 - Critical | Sensor vượt ngưỡng nguy hiểm | Action rõ ràng |
| TC4 - Missing data | Mất dữ liệu một sensor | Giảm confidence |
| TC5 - Sensor fault | Sensor đứng giá trị hoặc nhảy bất thường | Phát hiện lỗi sensor |
| TC6 - Conflicting sensor | Sensor mâu thuẫn | Không action mạnh, yêu cầu xác minh |
| TC7 - Wrong context | RAG lấy tài liệu không liên quan | Không suy diễn quá mức |
| TC8 - Control decision | Cần bật/tắt thiết bị | JSON action rõ ràng |

### Metric cần đo

| Thành phần | Metric |
|---|---|
| Data quality detection | Precision, Recall, F1-score |
| Recommendation quality | Correctness score |
| Context relevance | Rubric score |
| Explainability | Rubric score |
| Robustness | Accuracy under faulty scenarios |
| Performance | Latency |
| RAG retrieval | Recall@k, MRR, relevance score |

### Output cần nộp

| File | Nội dung |
|---|---|
| `test_cases.csv/json` | Bộ test case |
| `result_rule_based.csv` | Kết quả rule-based |
| `result_llm_only.csv` | Kết quả LLM-only |
| `result_rag_only.csv` | Kết quả RAG-only |
| `result_proposed.csv` | Kết quả hệ thống đề xuất |
| `metrics_summary.csv` | Tổng hợp metric |
| `failure_analysis.md` | Phân tích lỗi |

### Checklist tuần 7

- [ ] Có ít nhất 8 test case.
- [ ] Chạy được tất cả baseline.
- [ ] Có bảng kết quả.
- [ ] Có metric.
- [ ] Có phân tích lỗi.
- [ ] Có kết luận trả lời RQ2, RQ3, RQ4.

---

## Tuần 8: Viết paper và chuẩn bị báo cáo

### Việc cần làm

1. Viết Introduction.
2. Viết Related Work.
3. Viết Methodology.
4. Viết Experiment Setup.
5. Viết Results.
6. Viết Discussion.
7. Viết Conclusion.
8. Làm slide/demo video.

### Cấu trúc paper gợi ý

```text
Title
Abstract
Keywords

1. Introduction
2. Related Work
   2.1 IoT/AIoT in Smart Agriculture
   2.2 RAG and LLM-based Decision Support
   2.3 Sensor Data Quality and Anomaly Detection
   2.4 Research Gap

3. Proposed Framework
   3.1 System Architecture
   3.2 Sensor Data Ingestion
   3.3 Data Quality Assessment
   3.4 RAG Knowledge Retrieval
   3.5 Agentic Reasoning Workflow
   3.6 Recommendation and Confidence Scoring

4. Experimental Setup
   4.1 Domain and Sensor Configuration
   4.2 Test Scenarios
   4.3 Baselines
   4.4 Evaluation Metrics

5. Results
   5.1 Data Quality Detection Results
   5.2 Recommendation Quality Comparison
   5.3 Explainability Evaluation
   5.4 Robustness under Faulty Sensor Scenarios
   5.5 Latency Analysis

6. Discussion
   6.1 Answer to Research Questions
   6.2 Strengths
   6.3 Limitations
   6.4 Threats to Validity

7. Conclusion and Future Work
References
```

### Mapping paper section với RQ

| RQ | Section trả lời |
|---|---|
| RQ1 | Proposed Framework |
| RQ2 | Data Quality Results |
| RQ3 | Baseline Comparison |
| RQ4 | Scenario-based Evaluation |

### Output cần nộp

| File | Nội dung |
|---|---|
| `paper_draft.docx/tex/md` | Bản thảo bài báo |
| `presentation.pptx` | Slide báo cáo |
| `demo_video_link.md` | Link video demo |
| `final_result_tables/` | Bảng kết quả cuối |
| `source_code/` | Source code hệ thống |

### Checklist tuần 8

- [ ] Paper có đủ section.
- [ ] Kết quả trả lời được 4 RQ.
- [ ] Có bảng so sánh baseline.
- [ ] Có figure architecture.
- [ ] Có discussion và limitation.
- [ ] Có slide/demo.

---

## 8. Mapping giữa RQ và công việc sinh viên

| RQ | Công việc chính | Output chứng minh |
|---|---|---|
| RQ1 | Tích hợp sensor + RAG + agent | Architecture, RAG pipeline, agent workflow, explainable JSON |
| RQ2 | Data quality và confidence score | Data quality module, confidence score, impact analysis |
| RQ3 | So sánh với baseline | Rule-based, LLM-only, RAG-only, result table |
| RQ4 | Test theo scenario | Test case, metric, failure analysis |

---

## 9. Tiêu chí đánh giá của giảng viên

| Tiêu chí | Trọng số |
|---|---:|
| Hiểu đúng RQ và phạm vi đề tài | 10% |
| Literature review và gap analysis | 15% |
| Thiết kế kiến trúc hợp lý | 15% |
| Prototype chạy được | 20% |
| Data quality module | 10% |
| RAG + Agent workflow | 10% |
| Baseline comparison | 10% |
| Evaluation và paper writing | 10% |

---

## 10. Mẫu báo cáo tiến độ hằng tuần

Mỗi tuần nhóm sinh viên cần trả lời 6 câu:

```text
1. Tuần này nhóm đã làm gì?
2. Output cụ thể là file/code/bảng nào?
3. Output đó trả lời RQ nào?
4. Kết quả hiện tại có vấn đề gì?
5. Tuần sau nhóm sẽ làm gì?
6. Nhóm cần giảng viên hỗ trợ gì?
```

---

## 11. Mẫu checklist giảng viên dùng để kiểm tra

### Checkpoint 1 - Sau tuần 2

- [ ] Nhóm đã chọn domain cụ thể.
- [ ] Có literature review matrix.
- [ ] Có research gap.
- [ ] Có contribution.
- [ ] Có phạm vi sensor/action rõ.

### Checkpoint 2 - Sau tuần 4

- [ ] API nhận sensor chạy được.
- [ ] Có dữ liệu sensor mẫu.
- [ ] RAG ingest chạy được.
- [ ] Query RAG trả về context liên quan.
- [ ] Có kiến trúc hệ thống.

### Checkpoint 3 - Sau tuần 6

- [ ] Có data quality module.
- [ ] Có agent workflow.
- [ ] Có baseline.
- [ ] Output có confidence và evidence.
- [ ] Có rubric đánh giá.

### Checkpoint 4 - Sau tuần 8

- [ ] Có kết quả thực nghiệm.
- [ ] Có bảng so sánh.
- [ ] Có phân tích lỗi.
- [ ] Có paper draft.
- [ ] Có slide/demo.

---

## 12. Lỗi sinh viên thường gặp và cách tránh

| Lỗi thường gặp | Hậu quả | Cách tránh |
|---|---|---|
| Làm quá rộng “smart agriculture” | Không rõ contribution | Chọn domain hẹp |
| Chỉ làm dashboard IoT | Không đủ nghiên cứu | Phải có RAG, data quality, evaluation |
| Không có baseline | Không chứng minh được hệ thống tốt hơn | Bắt buộc có rule-based, LLM-only, RAG-only |
| Không có test case lỗi sensor | Không trả lời được RQ2/RQ4 | Tạo missing, fault, conflict scenarios |
| Chỉ demo bằng vài ví dụ | Không đủ để viết paper | Phải có bảng metric |
| RAG không có evidence | Không chứng minh explainability | Output phải có source/chunk/relevance |
| Agent trả lời tự do | Khó đánh giá | Ép output JSON schema |
| Không phân tích limitation | Paper yếu | Viết rõ threat to validity |

---

## 13. Yêu cầu tối thiểu để được xem là hoàn thành

Một nhóm được xem là hoàn thành đề tài nếu có đủ:

1. Một domain cụ thể.
2. Một pipeline nhận dữ liệu sensor.
3. Một module kiểm tra chất lượng dữ liệu.
4. Một RAG pipeline từ tài liệu kỹ thuật.
5. Một agent workflow tạo recommendation.
6. Output JSON có explanation, evidence và confidence.
7. Ít nhất 3 baseline.
8. Ít nhất 8 test case.
9. Bảng kết quả metric.
10. Paper draft trả lời được 4 RQ.

---

## 14. Định nghĩa output cuối cùng

Cuối dự án, nhóm cần nộp thư mục như sau:

```text
final_submission/
│
├── paper/
│   ├── paper_draft.pdf
│   ├── paper_source.docx_or_tex
│   └── references.bib
│
├── docs/
│   ├── rq_explanation.md
│   ├── literature_review_matrix.md
│   ├── research_gap.md
│   ├── contribution.md
│   ├── architecture.png
│   ├── data_flow.png
│   └── agent_workflow.md
│
├── data/
│   ├── normal.csv
│   ├── warning.csv
│   ├── critical.csv
│   ├── missing_data.csv
│   ├── sensor_fault.csv
│   └── conflict_sensor.csv
│
├── code/
│   ├── sensor_api/
│   ├── sensor_simulator/
│   ├── data_quality/
│   ├── rag_pipeline/
│   ├── agent_service/
│   └── baselines/
│
├── results/
│   ├── result_rule_based.csv
│   ├── result_llm_only.csv
│   ├── result_rag_only.csv
│   ├── result_proposed.csv
│   ├── metrics_summary.csv
│   └── failure_analysis.md
│
└── presentation/
    ├── slides.pptx
    └── demo_video_link.md
```

---

## 15. Gợi ý công nghệ triển khai

| Thành phần | Công nghệ gợi ý |
|---|---|
| Backend API | FastAPI / Node.js Express / NestJS |
| Sensor simulator | Python / Node.js |
| Database sensor | PostgreSQL / MongoDB / TimescaleDB |
| Vector database | Qdrant / Chroma / pgvector |
| Embedding | Gemini embedding / OpenAI embedding / sentence-transformers |
| LLM | Gemini / GPT / Llama local |
| Agent workflow | LangGraph / custom workflow |
| Dashboard | ReactJS / Next.js |
| Evaluation | Python pandas, scikit-learn |

---

## 16. Kết luận cho sinh viên

Đề tài này không chỉ yêu cầu xây dựng một hệ thống IoT. Điểm nghiên cứu nằm ở việc chứng minh rằng:

1. Dữ liệu sensor thời gian thực có thể kết hợp với tri thức nông nghiệp bằng RAG.
2. Chất lượng dữ liệu sensor ảnh hưởng trực tiếp đến độ tin cậy của khuyến nghị AI.
3. Agentic RAG có thể cải thiện độ liên quan ngữ cảnh và khả năng giải thích so với rule-based hoặc LLM-only.
4. Hệ thống đề xuất hoạt động tốt hơn trong các tình huống dữ liệu bình thường, thiếu dữ liệu, lỗi sensor và sensor mâu thuẫn.

Nếu nhóm chứng minh được 4 điểm trên bằng prototype, baseline và evaluation rõ ràng, đề tài có thể phát triển thành một bài conference paper có tính ứng dụng và tính nghiên cứu.
