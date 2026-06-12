# Phân công task tuần 5 - Data Quality Module và Agent Workflow

## Tổng quan Week 5

**Mục tiêu:** Xây Data Quality Module và Agent Workflow

**Domain:** Smart Greenhouse  
**Sensor:** Nhiệt độ, Độ ẩm không khí, Độ ẩm đất, Ánh sáng  
**Action:** Bật quạt, Tưới nước, Bật đèn, Cảnh báo

---

## Thành viên và Phân công

### Member 1 - Data Quality (Missing Data + Outlier Detection)

**Task:**

1. **Missing Data Detection**
   - Viết hàm phát hiện dữ liệu thiếu (null, NaN, không có bản ghi)
   - Xử lý khi sensor không gửi dữ liệu trong khoảng thời gian

2. **Outlier Detection**
   - Viết hàm phát hiện outlier dùng IQR hoặc Z-score
   - Đặt ngưỡng threshold cho từng sensor:
     - Temperature: 5-45°C
     - Humidity: 20-100%
     - Soil moisture: 0-100%
     - Light: 0-1000 lux

3. **Unit tests cho cả hai hàm**

**Output files:**

- `src/data_quality/missing_data.py`
- `src/data_quality/outlier.py`
- `tests/test_missing_data.py`
- `tests/test_outlier.py`

---

### Member 2 - Data Quality (Sensor Fault + Drift + Timestamp)

**Task:**

1. **Sensor Stuck Detection**
   - Phát hiện sensor không thay đổi giá trị trong N phút
   - Cấu hình N = 10 phút (có thể điều chỉnh)

2. **Sensor Drift Detection**
   - Phát hiện sự thay đổi gradient bất thường
   - So sánh tốc độ thay đổi với ngưỡng cho phép

3. **Timestamp Delay Detection**
   - Phát hiện sensor gửi dữ liệu trễ so với expected interval
   - Đánh dấu warning nếu trễ > 30 giây

4. **Unit tests cho cả ba hàm**

**Output files:**

- `src/data_quality/sensor_stuck.py`
- `src/data_quality/sensor_drift.py`
- `src/data_quality/timestamp_delay.py`
- `tests/test_sensor_stuck.py`
- `tests/test_sensor_drift.py`
- `tests/test_timestamp_delay.py`

---

### Member 3 - Agent Workflow + RAG Integration

**Task:**

1. **Agent Workflow Implementation**
   - Nhận sensor data mới nhất
   - Gọi data quality checker
   - Phân tích trạng thái hiện tại (normal/warning/critical)
   - Gọi RAG để lấy tài liệu liên quan
   - Tạo recommendation
   - Gắn confidence score
   - Trả về JSON có explanation và evidence

2. **RAG Query Integration**
   - Kết nối với RAG pipeline (vector DB đã setup ở tuần 4)
   - Viết hàm query RAG với context từ sensor data

3. **Agent Service Code**

**Output files:**

- `src/agent/agent_workflow.py`
- `src/agent/rag_integration.py`
- `src/agent/agent_service.py`
- `tests/test_agent_workflow.py`

---

### Member 4 - Confidence Score + Documentation

**Task:**

1. **Confidence Score Calculation**
   - Cài đặt công thức:
   ```
   Final Confidence =
   0.4 × Sensor Quality Score
   + 0.3 × RAG Relevance Score
   + 0.2 × Rule Consistency Score
   + 0.1 × Historical Stability Score
   ```
   - Viết hàm tính từng thành phần
   - Viết hàm tổng hợp

2. **Agent Output Formatting**
   - Đảm bảo output có: status, detected_issue, sensor_quality_score, recommendation, explanation, evidence, requires_human_approval

3. **Demo Output JSON**
   - Tạo file demo_output.json mẫu với đầy đủ trường

4. **Documentation**

**Output files:**

- `src/agent/confidence_score.py`
- `docs/confidence_score.md`
- `docs/agent_workflow.md`
- `demo_output.json`

---

## Output cần nộp cuối tuần

| File | Người phụ trách |
|------|-----------------|
| `data_quality_checker.py/js` | Member 1 + Member 2 |
| `confidence_score.md` | Member 4 |
| `agent_workflow.md` | Member 4 |
| `agent_service.py/js` | Member 3 |
| `demo_output.json` | Member 4 |

---

## Checklist Tuần 5

- [x] Phát hiện được missing data
- [x] Phát hiện được outlier
- [x] Phát hiện được sensor fault (stuck)
- [x] Phát hiện được sensor drift
- [x] Phát hiện được timestamp delay
- [ ] Phát hiện được conflicting sensor (cross-sensor)
- [ ] Agent gọi được data quality module
- [ ] Agent gọi được RAG
- [ ] Output có explanation và evidence
- [ ] Confidence score được tính đúng

---

## Tiến độ thực tế — Member 2 (cập nhật 2026-06-12)

| Deliverable | Trạng thái | Ghi chú |
|-------------|------------|---------|
| `src/data_quality/sensor_stuck.py` | ✅ Đã nộp | ~150 dòng, có `SensorStuckDetector`, `check_sensor_stuck()` |
| `src/data_quality/sensor_drift.py` | ✅ Đã nộp | ~250 dòng, có `SensorDriftDetector`, `check_sensor_drift()` |
| `src/data_quality/timestamp_delay.py` | ✅ Đã nộp | ~180 dòng, có `TimestampDelayDetector`, `check_timestamp_delay()` |
| `tests/test_sensor_stuck.py` | ✅ Đã nộp | Đã có pytest đầy đủ test cases (dùng data từ `sensor_fault.json`) |
| `tests/test_sensor_drift.py` | ✅ Đã nộp | Đã có pytest đầy đủ test cases (dùng data từ `sensor_fault.json`) |
| `tests/test_timestamp_delay.py` | ✅ Đã nộp | Đã có pytest đầy đủ test cases (dùng CSV + synthetic data) |

**Tỷ lệ hoàn thành:** 100% (6/6 file đã nộp; 27/27 tests passed)

---

## Tiến độ thực tế — Member 1 (cập nhật 2026-06-12)

| Deliverable | Trạng thái | Ghi chú |
|-------------|------------|---------|
| `src/data_quality/missing_data.py` | ✅ Đã nộp | ~244 dòng, `MissingDataDetector` với null/NaN detection + time-gap detection |
| `src/data_quality/outlier.py` | ✅ Đã nộp | ~232 dòng, `OutlierDetector` với IQR, Z-score, domain threshold methods |
| `tests/test_missing_data.py` | ✅ Đã nộp | 18 tests (null values, null summary, missing records, detect_all) |
| `tests/test_outlier.py` | ✅ Đã nộp | 27 tests (IQR, Z-score, threshold, aliases, custom thresholds, summary) |
| `README.md` | ✅ Đã nộp | Full integration guide với code example cho Agent (Member 3) |

**Tỷ lệ hoàn thành:** 100% (5/5 file đã nộp; 45/45 tests passed)
- **Commit:** `e823315` trên branch `SE1930_G07` — repo `NCKH-LongT/NCKH-DCD301`
- **Vị trí:** `04_proposed_system/src/data_quality/`, `06_experiment_results/tests/`, `weekly_reports/week_05/`
- **DB test:** PostgreSQL `dcd_rag` (72 rows) — integration test chạy OK

## Ghi chú

- Cần phối hợp giữa Member 1, 2 với Member 3 để đảm bảo data quality checker được agent gọi đúng
- Cần phối hợp với Member 3 (RAG tuần 4) để lấy RAG query code đã viết
- Cross-sensor conflict detection có thể làm chung với Member 2

---

## Research Questions liên quan

- **RQ2:** Data quality ảnh hưởng đến recommendation reliability
- **RQ1:** Agent workflow tích hợp sensor + RAG + data quality
- **RQ3:** Agentic RAG cải thiện context relevance và explainability

---

**Ngày tạo:** 2026-06-09  
**Tuần:** Week 5/8