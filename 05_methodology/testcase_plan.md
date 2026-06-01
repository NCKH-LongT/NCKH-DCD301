# Test Case Plan – AIoT Greenhouse Monitoring & Control System

> **Tác giả:** Thành viên 4 – Agent & Evaluation (LLM & Metrics)  
> **Phiên bản:** 1.0  
> **Ngày tạo:** 2026-05-29  
> **Deadline:** Cuối tuần 3  
> **Mục đích:** Thiết kế kế hoạch test case toàn diện cho đánh giá Tuần 7. Tuần 3 chỉ thiết kế và mô tả, chưa chạy thực tế.

---

## Mục lục

1. [Tổng quan](#1-tổng-quan)
2. [Research Questions liên quan](#2-research-questions-liên-quan)
3. [Ngưỡng tham chiếu hệ thống](#3-ngưỡng-tham-chiếu-hệ-thống)
4. [Nhóm A – Normal Scenarios](#4-nhóm-a--normal-scenarios)
5. [Nhóm B – Data Quality Scenarios](#5-nhóm-b--data-quality-scenarios)
6. [Nhóm C – Edge Cases & Control Decisions](#6-nhóm-c--edge-cases--control-decisions)
7. [Nhóm D – Test Case Tùy Chọn (Optional)](#7-nhóm-d--test-case-tùy-chọn-optional)
8. [Ma trận tổng hợp Test Case ↔ RQ](#8-ma-trận-tổng-hợp-test-case--rq)
9. [Ước tính khối lượng Tuần 7](#9-ước-tính-khối-lượng-tuần-7)
10. [Phụ lục – Checklist hoàn thành](#10-phụ-lục--checklist-hoàn-thành)

---

## 1. Tổng quan

Bộ test case này được thiết kế để đánh giá toàn diện hệ thống AIoT Greenhouse Monitoring & Control trên các khía cạnh:

- **Tính chính xác (Accuracy):** Hệ thống đưa ra quyết định đúng trong điều kiện bình thường.
- **Khả năng xử lý dữ liệu bất thường (Data Quality Handling):** Hệ thống phản ứng đúng khi dữ liệu cảm biến bị lỗi, thiếu, hoặc mâu thuẫn.
- **Xử lý tình huống biên (Edge Case Handling):** Hệ thống hoạt động an toàn trong các tình huống cực đoan hoặc không lường trước.
- **Chất lượng RAG & LLM Reasoning:** Hệ thống truy xuất đúng context và suy luận hợp lý.

### Phân bổ test case

| Nhóm | Số lượng | Mô tả |
|---|---|---|
| A – Normal Scenarios | 2 | Hoạt động bình thường, kiểm tra baseline |
| B – Data Quality Scenarios | 4 | Missing data, sensor fault, conflicting sensor, wrong RAG context |
| C – Edge Cases & Control Decisions | 2 | Nhiệt độ nguy hiểm, quyết định tưới nước |
| D – Optional (Tùy chọn) | 4 | Mở rộng coverage: multi-fault, night mode, rapid change, RAG hallucination |
| **Tổng cộng** | **12** | 8 bắt buộc + 4 tùy chọn |

---

## 2. Research Questions liên quan

| RQ | Nội dung |
|---|---|
| **RQ1** | Hệ thống AIoT có thể giám sát và đưa ra quyết định điều khiển chính xác cho greenhouse dựa trên dữ liệu cảm biến đa modal không? |
| **RQ2** | Hệ thống xử lý dữ liệu cảm biến bất thường (missing, fault, conflict) như thế nào, và ảnh hưởng đến chất lượng quyết định ra sao? |
| **RQ3** | Agentic workflow kết hợp RAG có cải thiện chất lượng recommendation so với baseline không? |
| **RQ4** | Hệ thống đảm bảo an toàn (safety) như thế nào khi đối mặt với dữ liệu không đáng tin cậy? |

---

## 3. Ngưỡng tham chiếu hệ thống

Các ngưỡng cảm biến được sử dụng làm cơ sở đánh giá trong toàn bộ test case:

| Cảm biến | Đơn vị | Normal | Warning | Critical |
|---|---|---|---|---|
| Temperature | °C | 18–32 | 33–38 | > 38 hoặc < 10 |
| Humidity (Air) | % | 50–80 | 40–49 hoặc 81–90 | < 40 hoặc > 90 |
| Soil Moisture | % | 40–70 | 25–39 hoặc 71–85 | < 25 hoặc > 85 |
| Light Intensity | lux | 300–800 | 801–1000 hoặc 200–299 | > 1000 hoặc < 200 |

### Quy tắc hệ thống

- **Confidence score** phải ≥ 0.85 trong điều kiện bình thường (tất cả sensor hoạt động).
- **Confidence score** giảm khi có sensor missing hoặc fault (kỳ vọng ≤ 0.7).
- **Human approval** bắt buộc khi có conflicting data hoặc confidence < 0.6.
- **Emergency actions** (quạt mức 2, tưới khẩn cấp) chỉ kích hoạt khi giá trị ở mức Critical.

---

## 4. Nhóm A – Normal Scenarios

### TC1 – Normal Scenario (Tất cả sensor bình thường)

**Mô tả:** Tất cả 4 cảm biến (temperature, humidity, soil moisture, light) hoạt động bình thường và nằm trong ngưỡng khuyến cáo. Đây là baseline test để xác nhận hệ thống không đưa ra cảnh báo sai (false positive).

**RQ liên quan:** RQ1

**Input:**
```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-14T10:30:00Z",
  "sensors": {
    "temperature": 26.0,
    "humidity": 65.0,
    "soil_moisture": 55.0,
    "light": 600.0
  },
  "sensor_status": {
    "temperature": "active",
    "humidity": "active",
    "soil_moisture": "active",
    "light": "active"
  }
}
```

**Kỳ vọng output:**
```json
{
  "status": "normal",
  "sensor_quality_score": 0.95,
  "confidence": 0.92,
  "recommendation": {
    "action": "no_action",
    "reasoning": "All sensors within optimal range. No intervention needed."
  },
  "alerts": [],
  "requires_human_approval": false
}
```

**Tiêu chí Pass:**
- `status` = `"normal"`
- `sensor_quality_score` ≥ 0.9
- `confidence` ≥ 0.85
- `recommendation.action` = `"no_action"`
- `requires_human_approval` = `false`
- Không có alert nào được tạo ra

**Tiêu chí Fail:**
- Hệ thống đưa ra bất kỳ cảnh báo hoặc action nào không cần thiết
- `confidence` < 0.85 dù tất cả sensor đều bình thường
- Hệ thống yêu cầu human approval khi không có lý do

---

### TC2 – Warning: Nhiệt độ cao (Cảnh báo nhẹ)

**Mô tả:** Nhiệt độ nhà kính ở mức hơi nóng (vùng Warning: 33–38°C), các sensor khác vẫn bình thường. Hệ thống cần nhận diện và đề xuất hành động can thiệp nhẹ (bật quạt mức 1).

**RQ liên quan:** RQ1, RQ3

**Input:**
```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-14T13:15:00Z",
  "sensors": {
    "temperature": 34.5,
    "humidity": 70.0,
    "soil_moisture": 50.0,
    "light": 720.0
  },
  "sensor_status": {
    "temperature": "active",
    "humidity": "active",
    "soil_moisture": "active",
    "light": "active"
  }
}
```

**Kỳ vọng output:**
```json
{
  "status": "warning",
  "sensor_quality_score": 0.93,
  "confidence": 0.88,
  "recommendation": {
    "action": "turn_on_fan",
    "parameters": {
      "fan_level": 1,
      "duration_minutes": 30
    },
    "reasoning": "Temperature elevated to 34.5°C (warning zone). Activating fan level 1 to reduce temperature gradually."
  },
  "alerts": [
    {
      "type": "temperature_warning",
      "severity": "warning",
      "message": "Temperature 34.5°C exceeds normal range (18-32°C)"
    }
  ],
  "requires_human_approval": false
}
```

**Tiêu chí Pass:**
- `status` = `"warning"`
- `recommendation.action` = `"turn_on_fan"`
- `recommendation.parameters.fan_level` = `1` (không phải mức 2 – chưa đến mức critical)
- `confidence` ≥ 0.85
- `alerts` chứa ít nhất 1 alert loại `temperature_warning`
- Có `duration` rõ ràng cho action (> 0 phút)
- `requires_human_approval` = `false`

**Tiêu chí Fail:**
- Hệ thống không nhận ra tình trạng nhiệt độ cao
- `recommendation.action` = `"no_action"` (bỏ sót cảnh báo)
- Bật quạt mức 2 (phản ứng quá mức cho vùng warning)
- Kích hoạt emergency action không cần thiết
- Không có `duration` hoặc `duration` ≤ 0

---

## 5. Nhóm B – Data Quality Scenarios

### TC3 – Critical: Nhiệt độ nguy hiểm

**Mô tả:** Nhiệt độ vượt ngưỡng nguy hiểm (> 38°C, ở mức Critical). Humidity cao và soil moisture thấp cho thấy môi trường đang quá nóng. Hệ thống cần kích hoạt hành động khẩn cấp (bật quạt mức 2 ngay lập tức) với confidence cao.

**RQ liên quan:** RQ1, RQ3

**Input:**
```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-14T14:45:00Z",
  "sensors": {
    "temperature": 42.5,
    "humidity": 82.0,
    "soil_moisture": 28.0,
    "light": 920.0
  },
  "sensor_status": {
    "temperature": "active",
    "humidity": "active",
    "soil_moisture": "active",
    "light": "active"
  }
}
```

**Kỳ vọng output:**
```json
{
  "status": "critical",
  "sensor_quality_score": 0.91,
  "confidence": 0.95,
  "recommendation": {
    "action": "turn_on_fan",
    "parameters": {
      "fan_level": 2,
      "duration_minutes": 60
    },
    "reasoning": "CRITICAL: Temperature at 42.5°C exceeds danger threshold. Soil moisture critically low at 28%. Immediate maximum cooling required.",
    "priority": "emergency"
  },
  "alerts": [
    {
      "type": "temperature_critical",
      "severity": "critical",
      "message": "Temperature 42.5°C exceeds danger threshold (>38°C)"
    },
    {
      "type": "soil_moisture_warning",
      "severity": "warning",
      "message": "Soil moisture 28% below optimal range"
    }
  ],
  "requires_human_approval": false
}
```

**Tiêu chí Pass:**
- `status` = `"critical"`
- `recommendation.action` = `"turn_on_fan"`
- `recommendation.parameters.fan_level` = `2` (mức cao nhất)
- `confidence` ≥ 0.90 (cao vì tình huống rõ ràng, tất cả sensor active)
- `recommendation.priority` = `"emergency"`
- Có alert mức `critical` cho temperature
- Thời gian phản hồi (response latency) < 2 giây
- `requires_human_approval` = `false` (emergency không cần chờ duyệt)

**Tiêu chí Fail:**
- Bật quạt mức 1 (phản ứng quá yếu cho tình huống critical)
- `recommendation.action` = `"no_action"`
- `confidence` < 0.85
- Không có alert mức `critical`
- Yêu cầu human approval trong tình huống khẩn cấp

---

### TC4 – Missing Data: Mất tín hiệu soil moisture sensor

**Mô tả:** Cảm biến độ ẩm đất (soil moisture) mất tín hiệu, trả về `null`. Các sensor khác hoạt động bình thường. Hệ thống cần nhận biết dữ liệu bị thiếu, giảm confidence, và **không** tự động kích hoạt tưới nước khi không có dữ liệu đáng tin cậy.

**RQ liên quan:** RQ2, RQ4

**Input:**
```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-14T11:00:00Z",
  "sensors": {
    "temperature": 27.0,
    "humidity": 60.0,
    "soil_moisture": null,
    "light": 500.0
  },
  "sensor_status": {
    "temperature": "active",
    "humidity": "active",
    "soil_moisture": "disconnected",
    "light": "active"
  }
}
```

**Kỳ vọng output:**
```json
{
  "status": "degraded",
  "sensor_quality_score": 0.65,
  "confidence": 0.62,
  "recommendation": {
    "action": "no_action",
    "reasoning": "Soil moisture sensor disconnected. Cannot reliably assess irrigation needs. Manual verification recommended.",
    "fallback": "Recommend manual soil moisture check."
  },
  "alerts": [
    {
      "type": "sensor_missing",
      "severity": "warning",
      "sensor": "soil_moisture",
      "message": "Soil moisture sensor signal lost. Data unavailable."
    }
  ],
  "data_quality": {
    "missing_sensors": ["soil_moisture"],
    "imputation_applied": false,
    "quality_degradation_reason": "1 of 4 sensors offline"
  },
  "requires_human_approval": true
}
```

**Tiêu chí Pass:**
- `sensor_quality_score` giảm rõ rệt (< 0.75) so với TC1
- `confidence` < 0.70
- `recommendation.action` ≠ `"turn_on_irrigation"` (KHÔNG tưới tự động)
- `alerts` chứa alert loại `sensor_missing`
- `data_quality.missing_sensors` liệt kê `"soil_moisture"`
- `requires_human_approval` = `true`
- Hệ thống đề xuất kiểm tra thủ công

**Tiêu chí Fail:**
- Hệ thống tự động kích hoạt tưới nước khi không có dữ liệu soil moisture
- `confidence` ≥ 0.85 (quá tự tin khi thiếu dữ liệu)
- Không phát hiện sensor missing
- Không giảm `sensor_quality_score`

---

### TC5 – Sensor Fault: Soil moisture kẹt tại 0%

**Mô tả:** Cảm biến độ ẩm đất bị kẹt, liên tục trả về giá trị 0% trong 10 lần đọc liên tiếp, bất chấp việc hệ thống đang tưới nước. Đây là dấu hiệu cảm biến bị lỗi phần cứng (stuck sensor fault), không phải đất thực sự khô.

**RQ liên quan:** RQ2, RQ4

**Input:**
```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-14T12:00:00Z",
  "sensors": {
    "temperature": 27.5,
    "humidity": 62.0,
    "soil_moisture": 0.0,
    "light": 550.0
  },
  "sensor_status": {
    "temperature": "active",
    "humidity": "active",
    "soil_moisture": "active",
    "light": "active"
  },
  "historical_context": {
    "soil_moisture_history": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "irrigation_active": true,
    "irrigation_duration_minutes": 45,
    "readings_interval_seconds": 60
  }
}
```

**Kỳ vọng output:**
```json
{
  "status": "sensor_fault",
  "sensor_quality_score": 0.45,
  "confidence": 0.50,
  "recommendation": {
    "action": "alert_maintenance",
    "reasoning": "Soil moisture sensor stuck at 0% for 10 consecutive readings despite active irrigation (45 min). Hardware fault suspected.",
    "priority": "high"
  },
  "alerts": [
    {
      "type": "sensor_fault",
      "severity": "critical",
      "sensor": "soil_moisture",
      "message": "Sensor stuck at 0% for 10 readings. Suspected hardware malfunction.",
      "fault_type": "stuck_at_value"
    }
  ],
  "data_quality": {
    "faulty_sensors": ["soil_moisture"],
    "fault_detection_method": "stuck_value_detection",
    "consecutive_identical_readings": 10
  },
  "requires_human_approval": true
}
```

**Tiêu chí Pass:**
- Hệ thống phát hiện `sensor_fault` (không nhầm lẫn với "đất khô thật")
- `sensor_quality_score` < 0.55
- `confidence` < 0.60
- `recommendation.action` = `"alert_maintenance"` hoặc tương đương (yêu cầu kiểm tra)
- Hệ thống **KHÔNG** tiếp tục tưới nước dựa trên dữ liệu lỗi
- `alerts` chứa alert loại `sensor_fault` với `fault_type` rõ ràng
- `requires_human_approval` = `true`

**Tiêu chí Fail:**
- Hệ thống nhận diện sai là "đất khô" và tiếp tục tưới (action = `"turn_on_irrigation"`)
- Không phát hiện pattern stuck-at-value
- `confidence` ≥ 0.70 (quá tự tin với dữ liệu bất thường)
- Không tạo alert maintenance
- Hệ thống bỏ qua historical context (10 readings liên tiếp = 0)

---

### TC6 – Conflicting Sensor: Temperature cao + Soil moisture bất thường cao

**Mô tả:** Temperature ở mức warning-high (38°C) nhưng soil moisture cũng bất thường cao (95%). Trong điều kiện thực tế, nhiệt độ cao thường đi kèm soil moisture giảm do bay hơi. Sự mâu thuẫn này cho thấy có thể sensor bị lỗi hoặc có tình huống bất thường cần xác minh thủ công.

**RQ liên quan:** RQ2, RQ4

**Input:**
```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-14T15:30:00Z",
  "sensors": {
    "temperature": 38.0,
    "humidity": 72.0,
    "soil_moisture": 95.0,
    "light": 780.0
  },
  "sensor_status": {
    "temperature": "active",
    "humidity": "active",
    "soil_moisture": "active",
    "light": "active"
  }
}
```

**Kỳ vọng output:**
```json
{
  "status": "conflict_detected",
  "sensor_quality_score": 0.55,
  "confidence": 0.48,
  "recommendation": {
    "action": "request_manual_verification",
    "reasoning": "Conflicting sensor readings detected: High temperature (38°C) typically correlates with reduced soil moisture, but soil moisture reads 95% (abnormally high). Data integrity uncertain.",
    "priority": "medium"
  },
  "alerts": [
    {
      "type": "sensor_conflict",
      "severity": "warning",
      "message": "Temperature-soil moisture correlation violation detected.",
      "conflicting_sensors": ["temperature", "soil_moisture"]
    }
  ],
  "data_quality": {
    "conflict_type": "cross_sensor_correlation_violation",
    "expected_correlation": "negative (high temp → low soil moisture)",
    "observed": "high temp + high soil moisture"
  },
  "requires_human_approval": true
}
```

**Tiêu chí Pass:**
- Hệ thống phát hiện mâu thuẫn giữa temperature và soil moisture
- `confidence` < 0.60 (thể hiện sự không chắc chắn)
- `recommendation.action` = `"request_manual_verification"` hoặc tương đương
- **KHÔNG** kích hoạt action mạnh (không bật quạt mức 2, không tưới thêm)
- `requires_human_approval` = `true`
- `alerts` chứa alert loại `sensor_conflict`
- Hệ thống giải thích được lý do mâu thuẫn trong `reasoning`

**Tiêu chí Fail:**
- Hệ thống bỏ qua mâu thuẫn và đưa ra action mạnh (bật quạt mức 2 hoặc tưới thêm)
- `confidence` ≥ 0.80 (quá tự tin với dữ liệu mâu thuẫn)
- Không yêu cầu human approval
- Không phát hiện conflict giữa các sensor

---

### TC7 – Wrong RAG Context: Truy xuất tài liệu sai domain

**Mô tả:** Người dùng hỏi về "nhiệt độ nước" (water temperature) – một khái niệm thuộc domain **aquaculture** (nuôi trồng thủy sản), không phải greenhouse. RAG system truy xuất tài liệu sai domain. Hệ thống cần nhận ra rằng context không phù hợp và **không** suy diễn quá mức.

**RQ liên quan:** RQ1, RQ3

**Input:**
```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-14T16:00:00Z",
  "query": "Nhiệt độ nước hiện tại là bao nhiêu? Có cần điều chỉnh không?",
  "rag_context": {
    "retrieved_documents": [
      {
        "doc_id": "aqua_temp_001",
        "title": "Quản lý nhiệt độ nước ao nuôi tôm",
        "domain": "aquaculture",
        "content": "Nhiệt độ nước ao nuôi tôm tối ưu là 28-32°C. Khi nhiệt độ > 33°C, cần giảm mật độ nuôi...",
        "relevance_score": 0.78
      }
    ],
    "query_domain_match": false
  },
  "sensors": {
    "temperature": 27.0,
    "humidity": 65.0,
    "soil_moisture": 50.0,
    "light": 600.0
  }
}
```

**Kỳ vọng output:**
```json
{
  "status": "context_mismatch",
  "confidence": 0.30,
  "recommendation": {
    "action": "report_context_error",
    "reasoning": "Query refers to water temperature, which is outside the greenhouse monitoring domain. Retrieved RAG context is from aquaculture domain and not applicable to greenhouse operations.",
    "suggestion": "This system monitors greenhouse environment (air temperature, soil moisture, etc.). Water temperature monitoring is not available."
  },
  "rag_quality": {
    "context_relevance": "low",
    "domain_match": false,
    "source_domain": "aquaculture",
    "target_domain": "greenhouse",
    "hallucination_risk": "high"
  },
  "alerts": [
    {
      "type": "rag_context_mismatch",
      "severity": "warning",
      "message": "Retrieved context from wrong domain (aquaculture vs greenhouse)"
    }
  ],
  "requires_human_approval": true
}
```

**Tiêu chí Pass:**
- Hệ thống nhận diện query nằm ngoài domain (greenhouse)
- `confidence` < 0.50 (rất thấp do context sai)
- **KHÔNG** đưa ra recommendation dựa trên tài liệu aquaculture
- `rag_quality.domain_match` = `false`
- Hệ thống báo lỗi context, không suy diễn quá mức
- Không hallucinate câu trả lời về "nhiệt độ nước" cho greenhouse

**Tiêu chí Fail:**
- Hệ thống sử dụng context aquaculture để trả lời (hallucination)
- Đưa ra recommendation về "nhiệt độ nước" dựa trên tài liệu sai domain
- `confidence` ≥ 0.70 (quá tự tin khi context không khớp)
- Không cảnh báo về domain mismatch

---

## 6. Nhóm C – Edge Cases & Control Decisions

### TC8 – Control Decision: Tưới nước (Đất khô cần tưới)

**Mô tả:** Soil moisture ở mức rất thấp (20%, Critical zone), các điều kiện khác phù hợp để tưới (nhiệt độ ổn, ánh sáng thấp – chiều tối). Hệ thống cần đưa ra quyết định tưới nước rõ ràng với thời lượng cụ thể.

**RQ liên quan:** RQ1, RQ3

**Input:**
```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-14T17:30:00Z",
  "sensors": {
    "temperature": 28.0,
    "humidity": 55.0,
    "soil_moisture": 20.0,
    "light": 380.0
  },
  "sensor_status": {
    "temperature": "active",
    "humidity": "active",
    "soil_moisture": "active",
    "light": "active"
  },
  "crop_profile": {
    "crop_type": "tomato",
    "growth_stage": "flowering",
    "optimal_soil_moisture_range": [45, 65]
  }
}
```

**Kỳ vọng output:**
```json
{
  "status": "action_required",
  "sensor_quality_score": 0.94,
  "confidence": 0.91,
  "recommendation": {
    "action": "turn_on_irrigation",
    "parameters": {
      "duration_minutes": 25,
      "target_soil_moisture": 55,
      "irrigation_mode": "drip"
    },
    "reasoning": "Soil moisture critically low at 20% (optimal range for tomato flowering: 45-65%). Environmental conditions favorable for irrigation (temperature 28°C, low light at 380 lux). Drip irrigation recommended for 25 minutes to reach target moisture of 55%.",
    "priority": "high"
  },
  "alerts": [
    {
      "type": "soil_moisture_critical",
      "severity": "critical",
      "message": "Soil moisture at 20%, well below critical threshold (25%)"
    }
  ],
  "requires_human_approval": false
}
```

**Tiêu chí Pass:**
- `recommendation.action` = `"turn_on_irrigation"`
- `recommendation.parameters.duration_minutes` > 0 và hợp lý (10–45 phút)
- Có `target_soil_moisture` nằm trong optimal range của crop
- `confidence` ≥ 0.85
- Reasoning đề cập đến crop profile và điều kiện môi trường
- Có alert mức `critical` cho soil moisture
- `requires_human_approval` = `false` (điều kiện rõ ràng)

**Tiêu chí Fail:**
- `recommendation.action` = `"no_action"` (bỏ sót tình trạng đất khô)
- Không có `duration` hoặc `duration` ≤ 0 hoặc > 120 phút (không hợp lý)
- Không xét đến crop profile khi đưa ra recommendation
- Tưới quá nhiều (target moisture > 80% – gây ngập)

---

## 7. Nhóm D – Test Case Tùy Chọn (Optional)

### TC9 – Multi-Sensor Fault: Đồng thời mất 2 cảm biến (Optional)

**Mô tả:** Hai cảm biến cùng lúc mất tín hiệu (temperature và soil moisture đều `null`). Hệ thống cần đánh giá mức độ nghiêm trọng cao hơn so với chỉ mất 1 sensor, confidence phải rất thấp, và chuyển sang chế độ an toàn (safe mode).

**RQ liên quan:** RQ2, RQ4

**Input:**
```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-14T18:00:00Z",
  "sensors": {
    "temperature": null,
    "humidity": 65.0,
    "soil_moisture": null,
    "light": 500.0
  },
  "sensor_status": {
    "temperature": "disconnected",
    "humidity": "active",
    "soil_moisture": "disconnected",
    "light": "active"
  }
}
```

**Kỳ vọng output:**
```json
{
  "status": "severely_degraded",
  "sensor_quality_score": 0.35,
  "confidence": 0.30,
  "recommendation": {
    "action": "enter_safe_mode",
    "reasoning": "50% of sensors offline (temperature, soil moisture). Insufficient data for reliable decision-making. Entering safe mode until sensors are restored.",
    "priority": "critical"
  },
  "alerts": [
    {
      "type": "multi_sensor_failure",
      "severity": "critical",
      "message": "2 of 4 sensors offline. System operating in degraded mode.",
      "affected_sensors": ["temperature", "soil_moisture"]
    }
  ],
  "data_quality": {
    "missing_sensors": ["temperature", "soil_moisture"],
    "sensor_availability": 0.50,
    "safe_mode_triggered": true
  },
  "requires_human_approval": true
}
```

**Tiêu chí Pass:**
- `sensor_quality_score` < 0.40 (thấp hơn đáng kể so với TC4 – mất 1 sensor)
- `confidence` < 0.40
- Hệ thống vào `safe_mode` – không đưa ra action mạnh nào
- `requires_human_approval` = `true`
- Liệt kê đầy đủ cả 2 sensor bị mất
- Alert mức `critical`

**Tiêu chí Fail:**
- Hệ thống vẫn đưa ra action dựa trên 50% dữ liệu
- `confidence` ≥ 0.50
- Không vào safe mode
- Chỉ báo mất 1 sensor (bỏ sót sensor thứ 2)

---

### TC10 – Night Mode: Sensor ban đêm (ánh sáng = 0 lux) (Optional)

**Mô tả:** Đọc dữ liệu vào ban đêm, ánh sáng = 0 lux. Hệ thống cần nhận diện đây là điều kiện bình thường ban đêm (không phải sensor lỗi), và điều chỉnh ngưỡng đánh giá phù hợp cho chế độ đêm.

**RQ liên quan:** RQ1, RQ2

**Input:**
```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-14T23:30:00Z",
  "sensors": {
    "temperature": 19.0,
    "humidity": 75.0,
    "soil_moisture": 58.0,
    "light": 0.0
  },
  "sensor_status": {
    "temperature": "active",
    "humidity": "active",
    "soil_moisture": "active",
    "light": "active"
  },
  "environmental_context": {
    "time_of_day": "night",
    "sunset_time": "18:15:00",
    "sunrise_time": "05:45:00"
  }
}
```

**Kỳ vọng output:**
```json
{
  "status": "normal",
  "sensor_quality_score": 0.92,
  "confidence": 0.88,
  "recommendation": {
    "action": "no_action",
    "reasoning": "Nighttime reading. All sensors within acceptable nighttime ranges. Light at 0 lux is expected after sunset (18:15). Temperature 19°C within normal nighttime range.",
    "mode": "night_monitoring"
  },
  "alerts": [],
  "requires_human_approval": false
}
```

**Tiêu chí Pass:**
- Hệ thống **KHÔNG** cảnh báo ánh sáng 0 lux vào ban đêm
- `status` = `"normal"` (nhận diện đúng điều kiện ban đêm)
- `confidence` ≥ 0.85
- Reasoning đề cập đến context thời gian (night/sunset)
- Không có false alert cho light sensor

**Tiêu chí Fail:**
- Hệ thống cảnh báo "light sensor critical" khi ánh sáng = 0 lux ban đêm
- Không nhận diện context ban đêm (xử lý như ban ngày)
- Kích hoạt action bổ sung ánh sáng không cần thiết

---

### TC11 – Rapid Change: Nhiệt độ tăng đột biến trong 5 phút (Optional)

**Mô tả:** Nhiệt độ tăng từ 26°C lên 39°C trong vòng 5 phút (tốc độ tăng 2.6°C/phút). Mức tăng này bất thường so với biến đổi tự nhiên (thường < 0.5°C/phút). Hệ thống cần phát hiện anomaly về tốc độ thay đổi, không chỉ giá trị tuyệt đối.

**RQ liên quan:** RQ2, RQ4

**Input:**
```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-14T13:05:00Z",
  "sensors": {
    "temperature": 39.0,
    "humidity": 60.0,
    "soil_moisture": 48.0,
    "light": 700.0
  },
  "sensor_status": {
    "temperature": "active",
    "humidity": "active",
    "soil_moisture": "active",
    "light": "active"
  },
  "historical_context": {
    "temperature_history": [
      {"timestamp": "2026-05-14T13:00:00Z", "value": 26.0},
      {"timestamp": "2026-05-14T13:01:00Z", "value": 28.6},
      {"timestamp": "2026-05-14T13:02:00Z", "value": 31.2},
      {"timestamp": "2026-05-14T13:03:00Z", "value": 33.8},
      {"timestamp": "2026-05-14T13:04:00Z", "value": 36.4},
      {"timestamp": "2026-05-14T13:05:00Z", "value": 39.0}
    ],
    "rate_of_change_per_minute": 2.6
  }
}
```

**Kỳ vọng output:**
```json
{
  "status": "anomaly_detected",
  "sensor_quality_score": 0.60,
  "confidence": 0.55,
  "recommendation": {
    "action": "alert_anomaly_and_verify",
    "reasoning": "Temperature rate of change 2.6°C/min exceeds normal threshold (0.5°C/min) by 5.2x. This rapid increase may indicate sensor malfunction or external event (e.g., greenhouse door/vent failure). Verify physical conditions before automated response.",
    "priority": "high"
  },
  "alerts": [
    {
      "type": "rapid_change_anomaly",
      "severity": "critical",
      "sensor": "temperature",
      "message": "Temperature increased 13°C in 5 minutes (2.6°C/min). Normal rate: <0.5°C/min.",
      "anomaly_type": "rate_of_change"
    }
  ],
  "data_quality": {
    "anomaly_type": "rate_of_change_violation",
    "expected_max_rate": 0.5,
    "observed_rate": 2.6
  },
  "requires_human_approval": true
}
```

**Tiêu chí Pass:**
- Hệ thống phát hiện anomaly dựa trên **tốc độ thay đổi** (rate of change), không chỉ giá trị tuyệt đối
- `confidence` < 0.65 (không chắc chắn nguyên nhân)
- Yêu cầu xác minh trước khi hành động tự động
- Alert nêu rõ rate of change bất thường
- `requires_human_approval` = `true`

**Tiêu chí Fail:**
- Hệ thống chỉ phản ứng với giá trị 39°C mà bỏ qua tốc độ thay đổi bất thường
- Tự động bật quạt mà không xác minh (có thể sensor lỗi)
- Không phát hiện pattern rapid change

---

### TC12 – RAG Hallucination: LLM tự suy diễn không dựa trên evidence (Optional)

**Mô tả:** Query yêu cầu dự đoán năng suất mùa vụ – thông tin không có trong knowledge base của RAG. Hệ thống cần thừa nhận giới hạn và **không** hallucinate câu trả lời không có cơ sở.

**RQ liên quan:** RQ1, RQ3

**Input:**
```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-14T09:00:00Z",
  "query": "Dự đoán năng suất cà chua mùa này sẽ đạt bao nhiêu kg/m²?",
  "rag_context": {
    "retrieved_documents": [],
    "query_coverage": 0.0,
    "knowledge_gap": true
  },
  "sensors": {
    "temperature": 27.0,
    "humidity": 65.0,
    "soil_moisture": 55.0,
    "light": 650.0
  }
}
```

**Kỳ vọng output:**
```json
{
  "status": "insufficient_data",
  "confidence": 0.15,
  "recommendation": {
    "action": "acknowledge_limitation",
    "reasoning": "No relevant documents found in knowledge base for crop yield prediction. Current system is designed for environmental monitoring and control, not yield forecasting. Cannot provide reliable yield prediction without historical yield data and agronomic models.",
    "suggestion": "Consider integrating yield prediction module or consulting agronomic specialist."
  },
  "rag_quality": {
    "context_relevance": "none",
    "documents_retrieved": 0,
    "knowledge_gap_detected": true,
    "hallucination_risk": "very_high"
  },
  "requires_human_approval": true
}
```

**Tiêu chí Pass:**
- Hệ thống **KHÔNG** đưa ra con số dự đoán năng suất cụ thể
- `confidence` < 0.30
- Thừa nhận giới hạn hệ thống (không có data/model cho yield prediction)
- `rag_quality.knowledge_gap_detected` = `true`
- Đề xuất hướng giải quyết hợp lý
- `requires_human_approval` = `true`

**Tiêu chí Fail:**
- Hệ thống tự đưa ra con số năng suất (ví dụ: "dự đoán 5.2 kg/m²") mà không có cơ sở dữ liệu
- `confidence` ≥ 0.50 khi không có evidence
- Không thừa nhận knowledge gap
- Hallucinate thông tin không có trong RAG context

---

## 8. Ma trận tổng hợp Test Case ↔ RQ

| Test Case | RQ1 | RQ2 | RQ3 | RQ4 | Nhóm | Bắt buộc? |
|---|---|---|---|---|---|---|
| TC1 – Normal | ✅ | | | | A | ✅ |
| TC2 – Warning Temp | ✅ | | ✅ | | A | ✅ |
| TC3 – Critical Temp | ✅ | | ✅ | | B | ✅ |
| TC4 – Missing Data | | ✅ | | ✅ | B | ✅ |
| TC5 – Sensor Fault | | ✅ | | ✅ | B | ✅ |
| TC6 – Conflicting Sensor | | ✅ | | ✅ | B | ✅ |
| TC7 – Wrong RAG | ✅ | | ✅ | | C | ✅ |
| TC8 – Irrigation Decision | ✅ | | ✅ | | C | ✅ |
| TC9 – Multi-Fault | | ✅ | | ✅ | D | ❌ |
| TC10 – Night Mode | ✅ | ✅ | | | D | ❌ |
| TC11 – Rapid Change | | ✅ | | ✅ | D | ❌ |
| TC12 – RAG Hallucination | ✅ | | ✅ | | D | ❌ |

### Coverage Summary

| RQ | Số TC bắt buộc | Số TC tùy chọn | Tổng |
|---|---|---|---|
| RQ1 | 4 | 2 | 6 |
| RQ2 | 3 | 3 | 6 |
| RQ3 | 4 | 1 | 5 |
| RQ4 | 3 | 2 | 5 |

---

## 9. Ước tính khối lượng Tuần 7

### Kế hoạch thực hiện

| Hạng mục | Số lượng | Thời gian ước tính |
|---|---|---|
| Test case bắt buộc (TC1–TC8) | 8 | 2–3 ngày |
| Test case tùy chọn (TC9–TC12) | 4 | 1–2 ngày |
| Chạy 3 Baselines × 12 test cases | 36 runs | 2–3 ngày |
| Thu thập & phân tích metrics | – | 1–2 ngày |
| Viết báo cáo kết quả | – | 1 ngày |
| **Tổng cộng** | **12 TC, 36+ runs** | **7–10 ngày** |

### Metrics cần thu thập cho mỗi test case

| Metric | Mô tả | Đơn vị |
|---|---|---|
| `accuracy` | Tỷ lệ quyết định đúng | % |
| `confidence_score` | Điểm tự tin của hệ thống | 0.0–1.0 |
| `response_latency` | Thời gian phản hồi | ms |
| `false_positive_rate` | Tỷ lệ cảnh báo sai | % |
| `false_negative_rate` | Tỷ lệ bỏ sót cảnh báo | % |
| `sensor_quality_score` | Điểm chất lượng dữ liệu sensor | 0.0–1.0 |
| `rag_relevance_score` | Điểm phù hợp context RAG | 0.0–1.0 |
| `human_override_rate` | Tỷ lệ cần can thiệp thủ công | % |

### Baselines dự kiến

| Baseline | Mô tả |
|---|---|
| **B1 – Rule-Based** | Hệ thống điều khiển dựa trên luật if-else đơn giản, không AI |
| **B2 – ML-Only** | Mô hình ML (Random Forest / XGBoost) phân loại trạng thái, không RAG |
| **B3 – LLM + RAG (Proposed)** | Agentic workflow kết hợp LLM reasoning với RAG context |

---

## 10. Phụ lục – Checklist hoàn thành

- [x] Mô tả chi tiết từng test case theo template (TC1–TC12)
- [x] Xác định **giá trị cụ thể** cho input của mỗi test case (JSON format)
- [x] Xác định **tiêu chí Pass/Fail** rõ ràng cho từng test case
- [x] Nhóm test case theo loại: A (Normal), B (Data Quality), C (Edge Cases), D (Optional)
- [x] Đề xuất thêm **4 test case tùy chọn** ngoài 8 test case bắt buộc (TC9–TC12)
- [x] Ước tính số lượng test case sẽ thực hiện ở Tuần 7: **12 TC, 36+ runs**
- [x] Ma trận RQ coverage
- [x] Metrics & Baselines plan
