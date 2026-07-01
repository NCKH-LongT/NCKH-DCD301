# Methodology

## 1. Methodology Overview

This research uses a scenario-based experimental methodology to evaluate a reliability-aware AIoT smart greenhouse system.

The proposed method combines four main layers:

1. **BCD arithmetic error detection** for checking decimal sensor validity.
2. **Sensor data quality assessment** for detecting missing, abnormal, overflow, and conflicting readings.
3. **Agentic RAG decision support** for retrieving agricultural evidence and generating explainable recommendations.
4. **Safe-failure control policy** for blocking automatic actuator commands when the input data is unreliable.

The methodology is designed to prove that the proposed system can produce safer and more explainable greenhouse decisions than simpler baseline systems.

## 2. Research Workflow

The research workflow follows this sequence:

```text
Greenhouse Sensor Data
        ↓
BCD Conversion
        ↓
BCD Validation and Arithmetic Error Detection
        ↓
Sensor Data Quality Assessment
        ↓
RAG Knowledge Retrieval
        ↓
Agentic Reasoning
        ↓
Recommendation / Warning / Safety Blocking
        ↓
Evaluation against Baselines and Metrics
```

## 3. Input Data Preparation

The system uses simulated smart greenhouse sensor data because the current scope focuses on prototype validation rather than real hardware deployment.

The input data includes:

| Sensor Field | Purpose |
|---|---|
| Temperature | Detect heat stress and ventilation need |
| Humidity | Detect high or low air humidity |
| Soil moisture | Detect irrigation need |
| Light intensity | Detect grow-light need |
| Water flow | Check irrigation actuator consistency |
| BCD representation | Validate decimal encoding and arithmetic correctness |

The detailed dataset design is described in `dataset.md`.

## 4. BCD Validation Method

Each decimal sensor value is converted into Binary Coded Decimal format. Every decimal digit must be represented by a valid 4-bit BCD code.

Valid BCD codes:

```text
0000, 0001, 0010, 0011, 0100,
0101, 0110, 0111, 1000, 1001
```

Invalid BCD codes:

```text
1010, 1011, 1100, 1101, 1110, 1111
```

The system checks:

- Whether each BCD digit is valid.
- Whether arithmetic correction is needed.
- Whether overflow occurs.
- Whether an invalid decimal value should be blocked before AI processing.

If BCD validation fails, the system must mark the record as unreliable and block automatic control.

## 5. Sensor Data Quality Method

After BCD validation, the system checks application-level data quality.

The data quality module evaluates:

| Quality Dimension | Meaning |
|---|---|
| Validity | Sensor values are correctly encoded and within allowed range |
| Completeness | Required fields are not missing |
| Consistency | Related sensor values and actuator states do not conflict |
| Timeliness | Sensor readings are not delayed |
| Plausibility | Readings are physically reasonable for a greenhouse |

The output of this module is a data quality status and a quality score.

Example status values:

```text
Reliable
Partially Reliable
Unreliable
```

## 6. Agentic RAG Method

The Agentic RAG module is used only after sensor data has passed validation or when the system needs evidence to explain a warning.

The module performs these steps:

1. Build a query from the current greenhouse condition.
2. Retrieve relevant agricultural guideline passages.
3. Combine retrieved evidence with sensor data and validation results.
4. Generate a structured recommendation or warning.
5. Attach explanation, evidence, confidence, and safety decision.

The system must not generate unsupported free-text recommendations. The final output should follow the JSON structure defined in `04_proposed_system/data_flow.md`.

## 7. Safe-Failure Decision Policy

The core safety rule is:

```text
If BCD validation fails, overflow is detected, or sensor data quality is unreliable,
automatic actuator control must be blocked.
```

The system can allow automatic control only when:

- BCD validation is valid.
- No overflow is detected.
- Required sensor fields are complete.
- Data quality score is above the accepted threshold.
- The recommended action is supported by retrieved evidence.

## 8. Baseline Comparison Method

The proposed system is compared against three baseline methods:

| Baseline | Purpose |
|---|---|
| Rule-based | Tests simple threshold-based control |
| LLM-only | Tests direct LLM recommendation without retrieved evidence |
| RAG-only | Tests evidence-grounded generation without BCD and data quality checking |

All baselines use the same test cases as the proposed system. The detailed comparison design is described in `baseline.md`.

## 9. Evaluation Method

The evaluation uses labeled scenario-based test cases.

Main scenario groups:

- Normal sensor data.
- Warning greenhouse condition.
- Critical greenhouse condition.
- Missing sensor data.
- Invalid BCD code.
- Overflow value.
- Sensor fault.
- Conflicting sensor condition.
- Wrong or irrelevant retrieved context.

Each system output is compared against the expected label and expected action.

The evaluation focuses on:

- Detection accuracy.
- Recommendation correctness.
- Explanation quality.
- Evidence relevance.
- Safety blocking behavior.
- Response latency.
- Improvement over baselines.

The detailed metric definitions are described in `evaluation_metrics.md`.

## 10. Expected Output

Each test run should produce a structured output containing:

| Output Field | Description |
|---|---|
| `case_id` | Test case identifier |
| `system_status` | Normal, Warning, Critical, or Blocked |
| `bcd_validation` | Valid or invalid BCD result |
| `data_quality_assessment` | Reliability score and detected issues |
| `control_commands` | Actuator command or blocked warning |
| `reasoning` | Explanation of the decision |
| `verification` | Retrieved evidence from RAG |
| `safety_decision` | Whether automatic control is allowed |

## 11. Relationship with Research Questions

| Research Question | Methodology Component |
|---|---|
| RQ1 | BCD conversion and representation of greenhouse sensor values |
| RQ2 | Invalid BCD, overflow, and arithmetic error detection |
| RQ3 | Data quality score and reliability-aware decision support |
| RQ4 | Scenario-based evaluation and baseline comparison |

## 12. Summary

This methodology evaluates the proposed system as a complete reliability-aware AIoT pipeline. The key idea is to validate sensor data before AI reasoning, use Agentic RAG for evidence-based recommendations, and enforce safe-failure behavior when data cannot be trusted.

The supporting files are:

- `dataset.md`: defines test data and scenarios.
- `baseline.md`: defines comparison systems.
- `evaluation_metrics.md`: defines metrics and scoring methods.
