# Baseline Comparison Plan — Kế hoạch so sánh các Baseline

> **Mục đích:** Hướng dẫn chi tiết cách chạy, đánh giá và so sánh 4 baseline (Rule-based, LLM-only, RAG-only, Proposed Agentic RAG) trên cùng bộ test case để trả lời RQ2, RQ3, RQ4.
>
> **Phạm vi:** DCD Project — Greenhouse AIoT Agentic RAG System — Tuần 6 + 7

---

## 1. Tổng quan 4 baseline cần so sánh

| # | Baseline | File | Người phụ trách | Trạng thái |
|---|----------|------|-----------------|------------|
| 1 | **Rule-based** | `code/baselines/baseline_rule_based.py` | Nam (Mem1) | ✅ Hoàn thành |
| 2 | **LLM-only** | `code/baselines/baseline_llm_only.md` | Huy (Mem2) | ✅ Hoàn thành |
| 3 | **RAG-only** | `code/baselines/baseline_rag_only.py` | Bảo (Mem3) | ✅ Hoàn thành |
| 4 | **Proposed Agentic RAG** | `code/baselines/baseline_proposed.py` | Bảo (Mem3) | ✅ Hoàn thành |

**Mục tiêu so sánh:**
- RQ2: Hệ thống đề xuất có cải thiện recommendation quality so với baseline không?
- RQ3: Các thành phần (RAG, data quality, agent) đóng góp thế nào vào performance?
- RQ4: Hệ thống hoạt động ra sao trong điều kiện lỗi (faulty sensor, missing data)?

---

## 2. Bộ Test Case bắt buộc (8 test case)

> Theo tài liệu `huong_dan_sinh_vien_aiot_agentic_rag.md` — Tuần 7.

### 2.1 Bảng mô tả test case

| TC | Tên | Mô tả | Kỳ vọng chung |
|----|-----|-------|---------------|
| TC1 | Normal | Tất cả sensor trong ngưỡng bình thường | Không cảnh báo sai, status = `pass` |
| TC2 | Warning | Sensor lệch nhẹ khỏi ngưỡng bình thường | Cảnh báo nhẹ, action cấp 1 |
| TC3 | Critical | Sensor vượt ngưỡng nguy hiểm | Action rõ ràng, cấp 3, có human approval |
| TC4 | Missing data | Một hoặc nhiều sensor mất dữ liệu | Confidence giảm, flag human approval |
| TC5 | Sensor fault | Sensor đứng giá trị (stuck) hoặc nhảy bất thường | Phát hiện lỗi, không hành động trên dữ liệu sai |
| TC6 | Conflicting sensor | Sensor mâu thuẫn nhau (vd: temp cao + humidity cao không khớp) | Không action mạnh, yêu cầu xác minh |
| TC7 | Wrong context | RAG lấy tài liệu không liên quan | Không suy diễn quá mức, giảm confidence |
| TC8 | Control decision | Cần bật/tắt thiết bị (heater, fan, irrigation...) | JSON action rõ ràng, có level + duration |

### 2.2 Định dạng dữ liệu đầu vào (CSV)

**File:** `test_cases.csv`

```csv
test_id,sensor_type,sensor_id,value,location,timestamp,scenario,expected_status,expected_action
TC1,temperature,temp-01,25.5,zone_A,2026-06-22T08:00:00,normal,pass,none
TC1,humidity,hum-01,60.0,zone_A,2026-06-22T08:00:00,normal,pass,none
TC1,soil_moisture,soil-01,50.0,zone_A,2026-06-22T08:00:00,normal,pass,none
TC1,light,light-01,15000,zone_A,2026-06-22T08:00:00,normal,pass,none
TC2,temperature,temp-02,36.5,zone_B,2026-06-22T09:00:00,warning,warning,turn_on_fan
TC3,temperature,temp-03,42.0,zone_C,2026-06-22T10:00:00,critical,critical,turn_on_fan_and_mist
TC4,temperature,temp-04,,zone_D,2026-06-22T11:00:00,missing,warning,verify_sensor
TC5,temperature,temp-05,25.0,zone_E,2026-06-22T12:00:00,stuck,warning,check_sensor
TC6,temperature,temp-06,42.0,zone_F,2026-06-22T13:00:00,conflict,warning,verify
TC6,humidity,hum-06,30.0,zone_F,2026-06-22T13:00:00,conflict,warning,verify
TC7,temperature,temp-07,38.0,zone_G,2026-06-22T14:00:00,wrong_context,warning,turn_on_fan
TC8,soil_moisture,soil-08,15.0,zone_H,2026-06-22T15:00:00,control_critical,critical,start_irrigation
```

**Số dòng:** ≥ 30 dòng (8 test case × ~4 sensor types).

---

## 3. Quy trình chạy Baseline

### 3.1 Setup môi trường

```bash
cd d:\STUDY\KY7\DCD
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies (nếu chưa có)
pip install -r requirements.txt
```

### 3.2 Chạy từng baseline

#### **Baseline 1: Rule-based**

```bash
python code/baselines/baseline_rule_based.py \
    --input test_cases.csv \
    --output results/result_rule_based.json \
    --format json
```

**Input:** CSV sensor readings (chuẩn schema trên)
**Output:** JSON recommendation

#### **Baseline 2: LLM-only**

```bash
# Sử dụng prompt template trong baseline_llm_only.md
# Gọi API LLM (vd: OpenAI, Gemini, hoặc local LLM)
python code/baselines/run_llm_only.py \
    --input test_cases.csv \
    --output results/result_llm_only.json \
    --prompt-template baseline_llm_only.md
```

**Input:** Mô tả bài toán + sensor data
**Output:** JSON recommendation (do LLM sinh)

#### **Baseline 3: RAG-only**

```bash
python code/baselines/baseline_rag_only.py \
    --input test_cases.csv \
    --output results/result_rag_only.json \
    --knowledge-base data/knowledge_base/
```

**Input:** Sensor data + câu query
**Output:** JSON recommendation có evidence từ RAG

#### **Baseline 4: Proposed Agentic RAG**

```bash
python code/baselines/baseline_proposed.py \
    --input test_cases.csv \
    --output results/result_proposed.json \
    --knowledge-base data/knowledge_base/ \
    --threshold 0.75
```

**Input:** Sensor data + RAG retrieval + data quality metrics
**Output:** JSON recommendation với 4 component confidence score

---

## 4. Metric đánh giá

### 4.1 Metric cho Recommendation Quality

| Metric | Công thức / Cách tính | Áp dụng cho |
|--------|----------------------|-------------|
| **Accuracy** | `(correct predictions) / (total predictions)` | TC1, TC2, TC3, TC8 |
| **Precision** | `TP / (TP + FP)` | Phát hiện lỗi (TC5, TC6) |
| **Recall** | `TP / (TP + FN)` | Phát hiện lỗi (TC5, TC6) |
| **F1-score** | `2 × (P × R) / (P + R)` | Phát hiện lỗi (TC5, TC6) |
| **Rubric Score** | Điểm TB từ 5 tiêu chí × trọng số | Tất cả TC |

### 4.2 Metric cho Data Quality Detection

| Metric | Mô tả |
|--------|-------|
| **Missing data detection accuracy** | Phát hiện đúng missing data (TC4) |
| **Outlier detection recall** | Phát hiện đúng giá trị bất thường (TC5) |
| **Sensor fault detection** | Phát hiện đúng stuck/jump sensor |

### 4.3 Metric cho RAG Performance

| Metric | Công thức | Mục đích |
|--------|----------|----------|
| **Recall@k** | `relevant retrieved / total relevant` trong top-k | Chất lượng retrieval |
| **MRR (Mean Reciprocal Rank)** | `1 / rank of first relevant doc` | Vị trí tài liệu đúng |
| **Relevance score** | Cosine similarity / embedding score | Mức độ liên quan |
| **Context Precision** | `relevant retrieved / total retrieved` | Độ chính xác retrieval |

### 4.4 Metric cho Explainability

| Metric | Cách đánh giá |
|--------|---------------|
| **% output có explanation** | Số output có field `explanation` / tổng output |
| **% có evidence chain** | Số output trích dẫn được doc/source / tổng output |
| **Avg length of explanation** | Đếm từ trong `explanation` field |

### 4.5 Metric cho Safety

| Metric | Cách đánh giá |
|--------|---------------|
| **% require_human_approval đúng** | Đếm TC mà flag = true hợp lý / tổng TC cần flag |
| **False positive rate** | Over-cautions (flag khi không cần) |
| **False negative rate** | Under-cautions (không flag khi cần) |

### 4.6 Metric cho Performance

| Metric | Đơn vị | Cách đo |
|--------|--------|---------|
| **Latency** | milliseconds | `time.time()` trước & sau khi chạy baseline |
| **Throughput** | requests/sec | Số TC xử lý / tổng thời gian |

---

## 5. Output schema chuẩn

> Tất cả baseline PHẢI output JSON theo schema này để so sánh được.

```json
{
  "test_id": "TC1",
  "baseline": "rule_based | llm_only | rag_only | proposed",
  "timestamp": "2026-06-22T08:00:00",
  "input": {
    "sensor_readings": [
      {
        "sensor_id": "temp-01",
        "sensor_type": "temperature",
        "value": 25.5,
        "location": "zone_A"
      }
    ]
  },
  "output": {
    "status": "pass | warning | critical",
    "sensor_quality_score": 0.85,
    "rag_relevance_score": 0.0,
    "rule_consistency_score": 1.0,
    "historical_stability_score": 0.95,
    "final_confidence": 0.92,
    "recommendations": [
      {
        "action": "turn_on_fan",
        "level": 3,
        "duration_minutes": 30,
        "detail": "Turn on ventilation fan"
      }
    ],
    "explanation": "Temperature 25.5°C is within normal range.",
    "evidence": [
      {
        "source": "knowledge_base/greenhouse_mgmt.pdf",
        "chunk_id": "doc-104",
        "relevance_score": 0.92,
        "content_excerpt": "Optimal temperature range: 15-35°C"
      }
    ],
    "requires_human_approval": false
  },
  "expected": {
    "status": "pass",
    "action": "none"
  },
  "evaluation": {
    "correct": true,
    "correctness_score": 5,
    "context_relevance_score": 4,
    "explainability_score": 3,
    "actionability_score": 5,
    "safety_score": 5,
    "final_score": 4.4,
    "notes": "Đúng status, nhưng explanation hơi ngắn"
  },
  "performance": {
    "latency_ms": 145
  }
}
```

---

## 6. File output cần nộp

| File | Mô tả | Người tạo |
|------|-------|-----------|
| `test_cases.csv` | Bộ 8+ test case | Member 4 (Quy Đam) |
| `result_rule_based.json` | Output từ Rule-based | Nam (Mem1) |
| `result_llm_only.json` | Output từ LLM-only | Huy (Mem2) |
| `result_rag_only.json` | Output từ RAG-only | Bảo (Mem3) |
| `result_proposed.json` | Output từ Proposed | Bảo (Mem3) |
| `metrics_summary.csv` | Tổng hợp metric tất cả baseline | Member 4 (Quy Đam) |
| `comparison_table.md` | Bảng so sánh trực quan | Member 4 (Quy Đam) |
| `failure_analysis.md` | Phân tích trường hợp hệ thống sai | Member 4 (Quy Đam) |

---

## 7. Bảng so sánh (Template)

### 7.1 Bảng so sánh tổng hợp theo Test Case

| TC | Rule-based | LLM-only | RAG-only | Proposed | Best |
|----|------------|----------|----------|----------|------|
| TC1 - Normal | 4.2 | 3.8 | 4.0 | 4.6 | Proposed |
| TC2 - Warning | 4.0 | 3.5 | 3.9 | 4.5 | Proposed |
| TC3 - Critical | 4.5 | 3.0 | 3.7 | 4.7 | Proposed |
| TC4 - Missing Data | 2.8 | 3.0 | 2.5 | 4.4 | Proposed |
| TC5 - Sensor Fault | 1.5 | 2.5 | 2.0 | 4.6 | Proposed |
| TC6 - Conflicting | 2.5 | 2.8 | 2.3 | 4.0 | Proposed |
| TC7 - Wrong Context | 2.0 | 4.2 | 2.0 | 4.2 | LLM/Proposed |
| TC8 - Control | 4.5 | 3.5 | 4.0 | 4.8 | Proposed |
| **Trung bình** | **3.25** | **3.29** | **3.05** | **4.48** | **Proposed** |

### 7.2 Bảng so sánh theo tiêu chí Rubric (trung bình trên 8 TC)

| Tiêu chí | Rule-based | LLM-only | RAG-only | Proposed |
|----------|------------|----------|----------|----------|
| Correctness | 4.0 | 3.0 | 3.5 | 4.6 |
| Context Relevance | 2.5 | 4.0 | 4.2 | 4.7 |
| Explainability | 2.0 | 4.3 | 4.0 | 4.8 |
| Actionability | 4.5 | 3.5 | 4.0 | 4.8 |
| Safety | 3.0 | 2.5 | 2.5 | 4.6 |
| **Weighted Avg** | **3.30** | **3.50** | **3.71** | **4.69** |

### 7.3 Bảng so sánh Performance

| Metric | Rule-based | LLM-only | RAG-only | Proposed |
|--------|------------|----------|----------|----------|
| Latency (ms) | ~50 | ~3000 | ~2500 | ~3500 |
| Throughput (req/s) | ~20 | ~0.3 | ~0.4 | ~0.3 |
| Memory (MB) | ~100 | ~500 | ~600 | ~800 |

---

## 8. Phân tích Failure Cases

### 8.1 Mục đích

Sau khi chạy baseline, ghi nhận các trường hợp **baseline sai hoặc output không như kỳ vọng** để phân tích nguyên nhân và rút ra bài học.

### 8.2 Template ghi nhận

| Field | Mô tả |
|-------|-------|
| **Test ID** | TC mà baseline thất bại |
| **Baseline** | Tên baseline bị fail |
| **Expected output** | Kết quả kỳ vọng |
| **Actual output** | Kết quả thực tế |
| **Root cause** | Nguyên nhân gốc rễ (threshold sai, missing data, RAG retrieval kém, hallucination...) |
| **Severity** | Critical (gây nguy hiểm) / Major (sai logic) / Minor (sai chi tiết) |
| **Proposed fix** | Đề xuất cách sửa |

### 8.3 Ví dụ

```markdown
### Failure 1: Rule-based fail trên TC5 (Sensor Fault)

- **Test ID:** TC5 - Sensor Fault
- **Baseline:** Rule-based
- **Expected:** Phát hiện sensor bị stuck, không hành động (status = warning, action = check_sensor)
- **Actual:** Status = pass, không phát hiện stuck sensor
- **Root cause:** Rule-based chỉ so sánh giá trị hiện tại với threshold, không có logic kiểm tra stuck value (giá trị không đổi theo thời gian)
- **Severity:** Major
- **Proposed fix:** Bổ sung stuck-detection logic: nếu giá trị không đổi > N lần đọc liên tiếp → flag stuck
```

### 8.4 Phân tích xu hướng fail

**Câu hỏi cần trả lời:**

1. Baseline nào fail nhiều nhất? Trên loại TC nào?
2. Failure có tập trung vào một tiêu chí Rubric nào không (vd: Safety fail nhiều)?
3. Failure có liên quan đến data quality (TC4, TC5, TC6) không?
4. Proposed system có giảm được bao nhiêu % failure so với baseline khác?

**Template bảng tổng hợp:**

| Baseline | Số TC fail | TC fail phổ biến | Tiêu chí Rubric yếu nhất | Tỷ lệ fail (%) |
|----------|------------|------------------|--------------------------|----------------|
| Rule-based | 4/8 | TC4, TC5, TC6, TC7 | Explainability, Context Relevance | 50% |
| LLM-only | 3/8 | TC3, TC5, TC7 | Correctness, Safety | 37.5% |
| RAG-only | 4/8 | TC4, TC5, TC6, TC7 | Safety, Context Relevance | 50% |
| Proposed | 1/8 | TC7 | Context Relevance | 12.5% |

---

## 9. Trả lời Research Question

### 9.1 RQ2: Hệ thống đề xuất có cải thiện recommendation quality không?

**Cách trả lời:**
- So sánh `final_score` của Proposed vs 3 baseline trên 8 TC
- So sánh `safety_score` đặc biệt (vì đây là điểm mạnh chính của hệ thống đề xuất)
- Tính % cải thiện: `((Proposed_score - best_baseline_score) / best_baseline_score) × 100%`

**Kỳ vọng:**
- Proposed có score cao nhất trên TC3 (critical), TC4 (missing), TC5 (fault), TC6 (conflict)
- Đề xuất có safety score ≥ 4.0 trên tất cả TC

### 9.2 RQ3: Thành phần nào (RAG, data quality, agent) đóng góp nhiều nhất?

**Cách trả lời (Ablation Study):**
- So sánh 3 phiên bản:
  - `RAG-only` (không có data quality)
  - `RAG + data quality` (chưa có agent reasoning)
  - `Proposed = RAG + data quality + agent`
- Đo sự cải thiện qua từng bước

**Kỳ vọng:**
- Data quality giúp tăng Safety score + Correctness score trên TC4, TC5, TC6
- Agent giúp tăng Actionability + Explainability trên tất cả TC

### 9.3 RQ4: Hệ thống hoạt động ra sao trong điều kiện lỗi?

**Cách trả lời:**
- Phân tích performance trên 4 TC lỗi: TC4, TC5, TC6, TC7
- Đếm số lần baseline flag `requires_human_approval: true` đúng
- So sánh false positive rate và false negative rate

**Kỳ vọng:**
- Proposed có false negative rate thấp nhất (không bỏ sót tình huống nguy hiểm)
- Proposed có false positive rate hợp lý (không quá over-cautious)

---

## 10. Timeline & Phân công

### 10.1 Timeline Tuần 6–7

| Ngày | Task | Người |
|------|------|-------|
| 2026-06-22 (T6) | Hoàn thành 2 file: `evaluation_rubric.md` + `baseline_comparison_plan.md` | Quy Đam (Mem4) |
| 2026-06-23 (T7) | Tạo `test_cases.csv` (≥ 8 TC) | Quy Đam (Mem4) |
| 2026-06-23 (T7) | Chạy Rule-based trên test_cases | Nam (Mem1) |
| 2026-06-23 (T7) | Chạy LLM-only trên test_cases | Huy (Mem2) |
| 2026-06-23 (T7) | Chạy RAG-only + Proposed trên test_cases | Bảo (Mem3) |
| 2026-06-24 (T8) | Tổng hợp `metrics_summary.csv` | Quy Đam (Mem4) |
| 2026-06-24 (T8) | Tạo `comparison_table.md` + biểu đồ | Quy Đam (Mem4) |
| 2026-06-25 (T9) | Viết `failure_analysis.md` | Quy Đam (Mem4) |
| 2026-06-25 (T9) | Trả lời RQ2, RQ3, RQ4 | Cả nhóm review |

### 10.2 Công cụ hỗ trợ

- **Visualization:** Matplotlib / Seaborn cho bar chart, heatmap
- **Statistical analysis:** scipy, numpy
- **Notebook:** Jupyter notebook `analysis_week7.ipynb` để chạy analysis

---

## 11. Checklist tuần 6 + 7

### Tuần 6 (Baseline + Plan)
- [x] Có rule-based baseline (Nam)
- [x] Có LLM-only baseline (Huy)
- [x] Có RAG-only baseline (Bảo)
- [x] Có proposed system (Bảo)
- [x] **Có evaluation rubric (Quy Đam) ← TASK NÀY**
- [x] **Có baseline comparison plan (Quy Đam) ← TASK NÀY**

### Tuần 7 (Chạy thí nghiệm)
- [ ] Có ≥ 8 test case trong `test_cases.csv`
- [ ] Chạy được cả 4 baseline trên cùng test set
- [ ] Có output JSON theo đúng schema cho mỗi baseline
- [ ] Có `metrics_summary.csv`
- [ ] Có bảng so sánh trực quan
- [ ] Có phân tích failure cases
- [ ] Có trả lời RQ2, RQ3, RQ4

---

## 12. Phụ lục

### 12.1 Threshold mặc định (từ baseline_rule_based.py)

```python
THRESHOLDS = {
    "temperature":     {"critical_low": 10.0, "warning_low": 15.0, "warning_high": 35.0, "critical_high": 40.0},
    "humidity":        {"critical_low": 30.0, "warning_low": 40.0, "warning_high": 70.0, "critical_high": 85.0},
    "soil_moisture":   {"critical_low": 20.0, "warning_low": 30.0, "warning_high": 70.0, "critical_high": 85.0},
    "light":           {"critical_low": 500.0, "warning_low": 2000.0, "warning_high": 30000.0, "critical_high": 45000.0},
}
```

### 12.2 Confidence Formula (từ baseline_proposed.py)

```
final_confidence = 0.4 × sensor_quality_score
                + 0.3 × rag_relevance_score
                + 0.2 × rule_consistency_score
                + 0.1 × historical_stability_score

Threshold for human approval: final_confidence < 0.75 → requires_human_approval = true
```

### 12.3 Action mapping (từ baseline_rule_based.py)

| Sensor | Zone | Action | Level | Duration |
|--------|------|--------|-------|----------|
| temperature | critical_low | turn_on_heater | 3 | 30 min |
| temperature | warning_low | turn_on_heater | 1 | 15 min |
| temperature | warning_high | turn_on_fan | 1 | 15 min |
| temperature | critical_high | turn_on_fan_and_mist | 3 | 30 min |
| humidity | critical_low | turn_on_humidifier | 3 | 30 min |
| humidity | warning_low | turn_on_humidifier | 1 | 15 min |
| humidity | warning_high | turn_on_ventilation | 1 | 15 min |
| humidity | critical_high | turn_on_ventilation_and_dehumidifier | 3 | 30 min |
| soil_moisture | critical_low | start_irrigation | 3 | 20 min |
| soil_moisture | warning_low | start_irrigation | 1 | 10 min |
| soil_moisture | warning_high | stop_irrigation | 1 | 0 min |
| soil_moisture | critical_high | stop_irrigation_and_check_drainage | 3 | 0 min |
| light | critical_low | turn_on_grow_light | 3 | 60 min |
| light | warning_low | turn_on_grow_light | 1 | 30 min |
| light | warning_high | lower_shade_curtain | 1 | 0 min |
| light | critical_high | lower_shade_curtain_and_monitor | 3 | 0 min |

### 12.4 Tham khảo

- File baseline: `code/baselines/baseline_*.{py,md}`
- Rubric đánh giá: `docs/evaluation_rubric.md`
- Hướng dẫn gốc: `reference/repo_cua_thay/huong_dan_sinh_vien_aiot_agentic_rag.md` (Tuần 6 + 7)

---

> **Tác giả:** Member 4 (Quy Đam) — DCD Project Week 6–7  
> **Ngày tạo:** 2026-06-22  
> **Cập nhật lần cuối:** 2026-06-22