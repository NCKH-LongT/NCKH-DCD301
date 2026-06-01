# Database Schema Design

## 1. Database Technology Selection

The system uses TimescaleDB as the primary database for storing time-series sensor data from smart greenhouse devices.

TimescaleDB was selected because:

* The system continuously receives real-time sensor streams.
* It provides efficient time-series querying and indexing.
* It extends PostgreSQL, allowing structured relational storage and JSONB support.
* It supports scalability for future large-scale AIoT deployments.

Additionally, Qdrant is used as the vector database for the RAG retrieval pipeline.


## 2. Table: sensor_readings

This table stores raw sensor data collected from greenhouse IoT devices or simulators before quality evaluation and AI reasoning.

| Field                | Type        | Constraint             | Description                                              |
| -------------------- | ----------- | ---------------------- | -------------------------------------------------------- |
| id                   | UUID        | PRIMARY KEY, NOT NULL  | Unique identifier for each sensor reading                |
| device_id            | VARCHAR(50) | NOT NULL, INDEX        | Unique greenhouse device or sensor ID                    |
| timestamp            | TIMESTAMPTZ | NOT NULL, INDEX        | Timestamp when the sensor data was generated             |
| temperature          | FLOAT       | NULL                   | Air temperature in degrees Celsius (°C)                  |
| humidity             | FLOAT       | NULL                   | Air humidity percentage (%)                              |
| soil_moisture        | FLOAT       | NULL                   | Soil moisture percentage (%)                             |
| light                | FLOAT       | NULL                   | Light intensity in lux                                   |
| source_type          | VARCHAR(20) | NOT NULL               | Data source type (`simulator` or `real_sensor`)          |
| ingestion_latency_ms | FLOAT       | NULL                   | Time delay between sensor generation and API ingestion   |
| raw_payload          | JSONB       | NULL                   | Original raw JSON payload received from the API          |
| created_at           | TIMESTAMPTZ | NOT NULL DEFAULT NOW() | Timestamp when the record was inserted into the database |

### Recommended Indexes

```sql
CREATE INDEX idx_sensor_device_time
ON sensor_readings(device_id, timestamp DESC);

CREATE INDEX idx_sensor_timestamp
ON sensor_readings(timestamp DESC);
```

### Example JSON Payload

```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-29T10:30:00Z",
  "temperature": 34.2,
  "humidity": 72,
  "soil_moisture": 25,
  "light": 850
}
```

### Purpose

The `sensor_readings` table acts as the primary storage for all incoming greenhouse sensor streams. It supports:

* real-time monitoring,
* historical sensor analysis,
* data quality assessment,
* FSM state analysis,
* and AI recommendation generation.


## 3. Table: quality_reports

This table stores the results of data quality evaluation for each sensor reading before the information is used by the FSM analyzer and Agentic RAG workflow.

| Field                  | Type        | Constraint             | Description                                                                         |
| ---------------------- | ----------- | ---------------------- | ----------------------------------------------------------------------------------- |
| id                     | UUID        | PRIMARY KEY, NOT NULL  | Unique identifier for each quality report                                           |
| reading_id             | UUID        | FOREIGN KEY, NOT NULL  | Reference to the related sensor reading                                             |
| completeness_score     | FLOAT       | NOT NULL               | Score for missing-value completeness (0–1)                                          |
| validity_score         | FLOAT       | NOT NULL               | Score for sensor value validity and range checking                                  |
| consistency_score      | FLOAT       | NOT NULL               | Score for consistency between multiple sensors                                      |
| timeliness_score       | FLOAT       | NOT NULL               | Score for freshness and real-time availability                                      |
| reliability_score      | FLOAT       | NOT NULL               | Score representing long-term sensor reliability                                     |
| overall_quality_score  | FLOAT       | NOT NULL               | Final aggregated quality score                                                      |
| detected_issue         | TEXT        | NULL                   | Description of detected sensor or data quality issues                               |
| issue_type             | VARCHAR(50) | NULL                   | Type of issue (`missing_data`, `outlier`, `conflict`, `sensor_fault`, `stale_data`) |
| requires_manual_review | BOOLEAN     | NOT NULL DEFAULT FALSE | Indicates whether human verification is required                                    |
| created_at             | TIMESTAMPTZ | NOT NULL DEFAULT NOW() | Timestamp when the quality report was generated                                     |

### Foreign Key Relationship

```sql
ALTER TABLE quality_reports
ADD CONSTRAINT fk_quality_reading
FOREIGN KEY (reading_id)
REFERENCES sensor_readings(id);
```

### Example Quality Report

```json
{
  "reading_id": "550e8400-e29b-41d4-a716-446655440000",
  "completeness_score": 0.75,
  "validity_score": 0.90,
  "consistency_score": 0.82,
  "timeliness_score": 0.95,
  "reliability_score": 0.88,
  "overall_quality_score": 0.86,
  "detected_issue": "Missing soil moisture value detected",
  "issue_type": "missing_data",
  "requires_manual_review": true
}
```

### Quality Score Formula

The overall quality score is calculated using weighted quality dimensions:

[
QualityScore = 0.3C + 0.25V + 0.2S + 0.15T + 0.1R
]

Where:

* (C) = Completeness
* (V) = Validity
* (S) = Consistency
* (T) = Timeliness
* (R) = Reliability

### Purpose

The `quality_reports` table is a core component of the Quality-Aware AIoT architecture. It ensures that unreliable or faulty sensor data can be detected before being processed by the FSM analyzer and Agentic RAG reasoning workflow. This helps reduce unsafe automated decisions and improves recommendation reliability.


## 4. Table: recommendations

This table stores AI-generated recommendations and decision outputs produced by the Agentic RAG workflow based on sensor data, quality evaluation, FSM state analysis, and retrieved knowledge context.

| Field                   | Type        | Constraint             | Description                                                  |
| ----------------------- | ----------- | ---------------------- | ------------------------------------------------------------ |
| id                      | UUID        | PRIMARY KEY, NOT NULL  | Unique identifier for each recommendation                    |
| device_id               | VARCHAR(50) | NOT NULL, INDEX        | Greenhouse device identifier                                 |
| quality_report_id       | UUID        | FOREIGN KEY, NOT NULL  | Reference to the related quality report                      |
| fsm_state               | VARCHAR(30) | NOT NULL               | Current FSM state (`Idle`, `Cooling`, `Heating`, `Watering`) |
| status                  | VARCHAR(20) | NOT NULL               | Overall system status (`normal`, `warning`, `critical`)      |
| detected_issue          | TEXT        | NULL                   | Detected environmental or sensor issue                       |
| recommended_action      | VARCHAR(50) | NOT NULL               | Recommended control action                                   |
| action_parameters       | JSONB       | NULL                   | Parameters for the action (duration, fan level, etc.)        |
| confidence_score        | FLOAT       | NOT NULL               | AI confidence score for the recommendation (0–1)             |
| explanation             | TEXT        | NOT NULL               | Natural language explanation generated by the AI system      |
| rag_context_ids         | JSONB       | NULL                   | References to retrieved RAG knowledge documents              |
| requires_human_approval | BOOLEAN     | NOT NULL DEFAULT FALSE | Indicates whether manual confirmation is required            |
| executed                | BOOLEAN     | NOT NULL DEFAULT FALSE | Indicates whether the action has been executed               |
| created_at              | TIMESTAMPTZ | NOT NULL DEFAULT NOW() | Timestamp when the recommendation was generated              |

### Foreign Key Relationship

```sql id="a4o5rc"
ALTER TABLE recommendations
ADD CONSTRAINT fk_recommendation_quality
FOREIGN KEY (quality_report_id)
REFERENCES quality_reports(id);
```

### Example Recommendation Output

```json id="l6d8ok"
{
  "device_id": "greenhouse_01",
  "fsm_state": "Cooling",
  "status": "warning",
  "detected_issue": "High greenhouse temperature detected",
  "recommended_action": "turn_on_fan",
  "action_parameters": {
    "fan_level": 2,
    "duration_seconds": 180
  },
  "confidence_score": 0.91,
  "explanation": "The greenhouse temperature exceeded the recommended threshold. Cooling is recommended to prevent crop stress.",
  "rag_context_ids": [
    "doc_temp_guideline_01",
    "doc_greenhouse_cooling_02"
  ],
  "requires_human_approval": false,
  "executed": false
}
```

### Purpose

The `recommendations` table stores the final decision outputs of the Quality-Aware Agentic RAG framework. It combines:

* sensor observations,
* data quality evaluation,
* FSM-based environmental state analysis,
* and RAG-supported reasoning

to generate explainable and reliable greenhouse management recommendations.


## 5. Relationship Between Tables

The database schema follows the processing pipeline of the Quality-Aware Agentic RAG framework. Each stage of the pipeline generates data that is used by the next stage.

### Relationship Flow

```text
sensor_readings
        ↓
quality_reports
        ↓
recommendations
```

### Relationship Description

| Source Table    | Target Table    | Relationship Type     | Description                                                                                          |
| --------------- | --------------- | --------------------- | ---------------------------------------------------------------------------------------------------- |
| sensor_readings | quality_reports | One-to-One            | Each sensor reading is evaluated by the Data Quality Module and produces one quality report          |
| quality_reports | recommendations | One-to-Many           | A quality report may generate one or multiple AI recommendations depending on the reasoning workflow |
| sensor_readings | recommendations | Indirect Relationship | Recommendations are generated based on validated sensor data through the quality evaluation process  |

### Data Processing Workflow

1. Raw sensor data is received from greenhouse devices or simulators and stored in the `sensor_readings` table.

2. The Data Quality Module analyzes the sensor values for:

   * missing data,
   * invalid ranges,
   * sensor conflicts,
   * stale data,
   * and sensor reliability.

3. The evaluation results are stored in the `quality_reports` table with multiple quality dimension scores and detected issues.

4. The FSM State Analyzer and Agentic RAG workflow use:

   * validated sensor data,
   * quality scores,
   * and retrieved knowledge context

   to generate explainable recommendations.

5. Final recommendation outputs are stored in the `recommendations` table for monitoring, auditing, and control actions.

### Design Rationale

This relational structure supports:

* traceability from sensor input to AI decision,
* explainable AI reasoning,
* quality-aware recommendation generation,
* and future evaluation experiments for recommendation reliability and safety.


## 6. Design Justification

The database schema was designed to support a Quality-Aware Agentic RAG framework for real-time smart greenhouse decision support. The structure follows the overall system pipeline:

```text
Sensor → API → Database → Quality Check → FSM → RAG → Agent → Recommendation
```

### Time-Series Data Support

The system continuously receives environmental sensor streams including temperature, humidity, soil moisture, and light intensity. Therefore, TimescaleDB was selected as the primary database technology because it is optimized for time-series workloads and supports efficient querying of real-time sensor data.

The `sensor_readings` table stores raw IoT sensor streams together with timestamps and original payloads. This design supports:

* real-time monitoring,
* historical analysis,
* fault investigation,
* and future scalability for large-scale AIoT deployments.

### Data Quality Awareness

A dedicated `quality_reports` table was introduced to support the research objective of data quality-aware reasoning. Instead of directly sending raw sensor data to the AI workflow, the system first evaluates data quality dimensions such as:

* completeness,
* validity,
* consistency,
* timeliness,
* and reliability.

This design allows the system to identify:

* missing values,
* conflicting sensor readings,
* stale data,
* and faulty sensors.

The quality evaluation results directly influence AI confidence scores and recommendation safety.

### Explainable AI Recommendations

The `recommendations` table stores the final outputs generated by the Agentic RAG workflow. Each recommendation contains:

* detected issues,
* recommended actions,
* confidence scores,
* FSM states,
* and natural language explanations.

This design improves explainability and allows future evaluation of AI decision reliability.

### Traceability and Relationship Design

The relationships between tables ensure complete traceability from:

* raw sensor input,
* to quality evaluation,
* to final AI recommendation.

This structure supports:

* debugging,
* experiment reproducibility,
* recommendation auditing,
* and future research evaluation.

### Research Contribution Support

The schema design specifically supports the core research contribution of the project:

> improving AI recommendation reliability through sensor data quality awareness.

By separating raw sensor data, quality evaluation, and AI recommendations into different tables, the system can measure how low-quality sensor data affects AI decision-making and recommendation confidence.
