# Dataset and Experimental Scenarios

## 1. Dataset Purpose

The dataset is designed to evaluate the proposed system:

**BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems**

The purpose of the dataset is not only to simulate greenhouse sensor readings, but also to test whether the system can detect unreliable data before it is used by the Agentic RAG decision module. Therefore, the dataset must include normal sensor conditions, abnormal greenhouse conditions, missing data, invalid BCD codes, overflow cases, and conflicting sensor situations.

## 2. Data Source

Because the project focuses on a student-level prototype, the dataset can be created using a **sensor simulator** instead of real greenhouse hardware.

The simulator generates structured greenhouse sensor records at fixed time intervals. Each record represents one observation of the greenhouse environment.

Expected data sources:

| Source | Role in the experiment |
|---|---|
| Simulated sensor stream | Main dataset for repeated testing |
| Manually injected error cases | Used to test invalid BCD, overflow, missing data, and conflict detection |
| Greenhouse guideline documents | Knowledge base for RAG retrieval and evidence generation |
| Expected action labels | Ground truth for recommendation and baseline comparison |

## 3. Sensor Fields

Each sensor record should contain the following fields:

| Field | Unit | Expected Range | Purpose |
|---|---:|---:|---|
| `timestamp` | ISO datetime | Valid datetime | Measures timeliness and ordering |
| `device_id` | text | greenhouse device ID | Identifies data source |
| `temperature_celsius` | Celsius | 10-45 | Detects heat stress and fan actions |
| `humidity_percent` | % | 30-95 | Detects excessive or low air humidity |
| `soil_moisture_percent` | % | 15-80 | Detects irrigation need |
| `light_intensity_lux` | lux | 0-30000 | Detects grow-light need |
| `water_flow_ml_per_min` | ml/min | 0-1000 | Checks irrigation actuator consistency |
| `bcd_value` | binary string | valid BCD digits only | Used for BCD validation |
| `expected_status` | label | Normal / Warning / Critical / Blocked | Ground truth for evaluation |
| `expected_action` | label | actuator or warning action | Ground truth for recommendation quality |

## 4. Scenario Categories

The dataset must cover at least the following scenario groups.

| Scenario | Description | Expected System Behavior |
|---|---|---|
| Normal | All sensor values are valid and within safe range | Return `Normal`, no unnecessary actuator action |
| Warning | One or more values are slightly outside the recommended range | Generate a moderate recommendation with explanation |
| Critical | A value exceeds a dangerous threshold | Generate clear actuator action if data is reliable |
| Missing data | One sensor value is null, empty, or delayed | Reduce quality score or block automatic control |
| Invalid BCD | One BCD digit is between `1010` and `1111` | Mark BCD validation as invalid and block control |
| Overflow | Value exceeds the allowed physical range | Detect overflow and block unsafe automation |
| Sensor fault | Sensor is stuck or jumps unrealistically | Flag unreliable data and request checking |
| Conflicting sensors | Sensor values contradict actuator state or related sensors | Avoid strong control action and request validation |
| Wrong retrieval context | RAG returns irrelevant agricultural evidence | Lower confidence and avoid unsupported recommendation |

## 5. Example Dataset Records

| Case ID | Temperature | Humidity | Soil Moisture | Light | Water Flow | BCD Status | Expected Status | Expected Action |
|---|---:|---:|---:|---:|---:|---|---|---|
| TC01 | 28.0 | 65 | 45 | 18000 | 0 | Valid | Normal | No action |
| TC02 | 34.5 | 72 | 24 | 18000 | 0 | Valid | Warning | Turn on fan and activate pump |
| TC03 | 41.0 | 88 | 18 | 21000 | 0 | Valid | Critical | Strong ventilation and irrigation |
| TC04 | null | 68 | 31 | 17500 | 0 | N/A | Blocked | Missing temperature warning |
| TC05 | null | 68 | 31 | 17500 | 0 | Invalid digit `1010` | Blocked | Sensor error warning |
| TC06 | 28.0 | 130 | 45 | 18000 | 0 | Valid | Blocked | Humidity overflow alert |
| TC07 | 30.0 | 66 | 25 | 18000 | 0 | Valid | Warning | Check pump because water flow is zero |
| TC08 | 32.0 | 70 | 22 | 150 | 120 | Valid | Warning | Turn on grow light and monitor irrigation |

## 6. Dataset Size

For the first prototype, the minimum dataset should contain:

| Dataset Split | Minimum Records | Purpose |
|---|---:|---|
| Normal cases | 20 | Confirm that the system does not over-alert |
| Warning cases | 20 | Test moderate recommendation quality |
| Critical cases | 20 | Test urgent actuator decision quality |
| Missing data cases | 10 | Test completeness detection |
| Invalid BCD cases | 10 | Test low-level decimal validation |
| Overflow cases | 10 | Test range and arithmetic reliability |
| Sensor fault cases | 10 | Test robustness under unreliable sensor behavior |
| Conflict cases | 10 | Test safe-failure policy |

Total minimum size: **110 records**.

The dataset can be expanded later for stronger experimental results.

## 7. Labeling Method

Each test case must be labeled before running the system.

The label should include:

1. Expected system status.
2. Expected actuator action or warning.
3. Whether automatic control should be allowed.
4. Expected data quality status.
5. Expected BCD validation status.
6. Expected explanation type.

Example label:

```json
{
  "case_id": "TC05",
  "expected_status": "Blocked",
  "expected_action": "SENSOR_ERROR_WARNING",
  "automatic_control_allowed": false,
  "expected_bcd_status": "Invalid",
  "expected_quality_status": "Unreliable",
  "expected_explanation": "Invalid BCD code detected; actuator control must be blocked."
}
```

## 8. Role in Research Questions

| Research Question | Dataset Role |
|---|---|
| RQ1 | Provides decimal greenhouse values for BCD conversion |
| RQ2 | Provides invalid BCD and overflow cases for error detection |
| RQ3 | Provides quality labels for reliability score evaluation |
| RQ4 | Provides scenario-based test cases for Agentic RAG and safe control decisions |

## 9. Dataset Quality Requirements

The dataset must satisfy these requirements:

- Each record must have a clear case ID.
- Each abnormal case must have a known injected error.
- Normal cases must not contain hidden faults.
- Invalid BCD cases must explicitly include invalid digits from `1010` to `1111`.
- Critical cases must still be separated from invalid-data cases.
- Labels must be created before model output is evaluated.
- All baselines and the proposed system must be tested on the same dataset.

## 10. Summary

The dataset is a scenario-based smart greenhouse dataset designed for evaluation, not only for demonstration. It supports the main contribution of the project by testing whether BCD validation, data quality assessment, and Agentic RAG can produce safer and more explainable decisions than simpler baseline approaches.
