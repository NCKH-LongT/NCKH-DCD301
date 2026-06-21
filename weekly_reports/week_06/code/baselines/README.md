# Baselines for Greenhouse Agentic RAG System

This folder contains baseline implementations for comparing against the **Proposed Agentic RAG** system in the NCKH-DCD301 project.

## 📁 Structure

```
code/baselines/
├── README.md                        # This file
├── baseline_rule_based.py           # Member 1 — Rule-based threshold logic
├── baseline_llm_only.md             # Member 2 — LLM-only (no RAG)
├── baseline_rag_only.py             # Member 3 — RAG-only (no data quality)
├── baseline_proposed.py             # Member 3 — Full Proposed Agentic RAG
├── evaluation_rubric.md             # Member 4 — Evaluation rubric
└── baseline_comparison_plan.md      # Member 4 — Comparison plan
```

## 🔧 How to Use

### 1. Rule-based Baseline (`baseline_rule_based.py`)

Compares sensor values against predefined thresholds using simple if-else logic and outputs JSON.

```bash
python baseline_rule_based.py <path_to_sensor_csv>
```

**Example:**
```bash
python baseline_rule_based.py ../../weekly_reports/week_04/sample_data/sample_sensor_data_normal.csv
```

**Output format:**
```json
{
  "status": "pass | warning | critical",
  "overall_confidence": 0.85,
  "requires_human_approval": false,
  "sensor_readings": [
    {
      "sensor_id": "temp_1",
      "sensor_type": "temperature",
      "value": 22.5,
      "unit": "°C",
      "status": "pass",
      "confidence": 0.73,
      "recommendation": {}
    }
  ],
  "recommendations": [
    {
      "sensor_id": "temp_1",
      "action": "turn_on_fan",
      "level": 2,
      "duration_minutes": 15,
      "detail": "Temperature high — turn on ventilation fan"
    }
  ],
  "summary": { "pass": 20, "warning": 4, "critical": 0 },
  "timestamp": "2026-06-18T08:20:32+00:00"
}
```

### 2. LLM-only Baseline (`baseline_llm_only.md`)
Coming soon — Member 2.

### 3. RAG-only Baseline (`baseline_rag_only.py`)
Coming soon — Member 3.

### 4. Proposed Agentic RAG (`baseline_proposed.py`)
Coming soon — Member 3.

## 📊 Threshold Definitions

| Sensor Type | Critical Low | Warning Low | Normal Range | Warning High | Critical High | Unit |
|------------|-------------|-------------|--------------|--------------|---------------|------|
| Temperature | 10.0 | 15.0 | 15.0 – 35.0 | 35.0 | 40.0 | °C |
| Humidity | 30.0 | 40.0 | 40.0 – 70.0 | 70.0 | 85.0 | % |
| Soil Moisture | 20.0 | 30.0 | 30.0 – 70.0 | 70.0 | 85.0 | % |
| Light | 500 | 2000 | 2000 – 30000 | 30000 | 45000 | lux |

## 🚀 Integration Guide

### Quick start — data already in memory

```python
import sys
sys.path.insert(0, "code/baselines")
from baseline_rule_based import process_readings

# Your data as a list of dicts (from DB, API, MQTT, ...)
sensor_data = [
    {"sensor_id": "temp_1", "sensor_type": "temperature", "value": 42.5, "location": "GH1"},
    {"sensor_id": "humid_1", "sensor_type": "humidity", "value": 88.3, "location": "GH2"},
]

result = process_readings(sensor_data)

if result["status"] == "critical":
    for rec in result["recommendations"]:
        print(f"{rec['sensor_id']}: {rec['action']} (level {rec['level']})")
```

### Custom field names

If your project uses **different column names**, pass a `field_mapping`:

```python
result = process_readings(
    sensor_data,
    field_mapping={
        "sensor_id": "id",        # your "id" → internal "sensor_id"
        "sensor_type": "type",    # your "type" → internal "sensor_type"
        "value": "temperature",   # your "temperature" → internal "value"
        "location": "loc",
        "timestamp": "ts",
    },
)
```

### Skip invalid records

```python
result = process_readings(sensor_data, skip_errors=True)
# Bad records are skipped with a warning, good ones are still processed
```

### Load from CSV

```python
from baseline_rule_based import read_sensor_data, process_readings

records = read_sensor_data("path/to/data.csv")
result = process_readings(records)
```

### Load CSV with different column names

```python
records = read_sensor_data(
    "path/to/data.csv",
    field_mapping={
        "sensor_id": "ID",
        "sensor_type": "Type",
        "value": "Temp",
        "location": "Loc",
        "timestamp": "Time",
    },
)
result = process_readings(records)
```

### For API integration

Pipe the JSON output to any HTTP endpoint:

```bash
python baseline_rule_based.py data.csv | curl -X POST -H "Content-Type: application/json" -d @- http://your-api/analyze
```

### Import as a module

```python
import sys
sys.path.append("path/to/code/baselines")
from baseline_rule_based import (
    process_readings,
    read_sensor_data,
    evaluate_sensor,
    get_recommendation,
    get_confidence,
    THRESHOLDS,
    DEFAULT_FIELD_MAP,
)
```

## 📐 Confidence Score Formula

```
confidence = 0.4 × sensor_quality + 0.3 × rag_relevance + 0.2 × rule_consistency + 0.1 × historical_stability
```

For the rule-based baseline specifically, confidence is derived from:
- Distance from threshold boundary (further = more confident)
- Severity level (critical > warning > pass)

## 📋 Status Priority

| Status | Priority | Description |
|--------|----------|-------------|
| `pass` | 0 | All sensors within normal range |
| `warning` | 1 | Some sensors near thresholds |
| `critical` | 2 | Sensors exceeding critical thresholds — alerts triggered |
