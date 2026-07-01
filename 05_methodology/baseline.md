# Baseline Comparison Plan

## 1. Purpose of Baselines

The proposed system combines BCD arithmetic error detection, sensor data quality assessment, Agentic RAG, and safe-failure control. To prove that this design is useful, the system must be compared with simpler baseline methods.

Baselines are used to answer the following question:

```text
Does the proposed reliability-aware Agentic RAG system produce safer, more correct,
more explainable, and more robust greenhouse decisions than simpler approaches?
```

## 2. Systems to Compare

The experiment compares four systems on the same test cases.

| System | Description | BCD Validation | Data Quality | RAG Evidence | Agent Workflow | Safe-Failure |
|---|---|---|---|---|---|---|
| Rule-based baseline | Uses fixed thresholds to generate alerts/actions | No | Partial | No | No | Partial |
| LLM-only baseline | Sends sensor data directly to an LLM prompt | No | No | No | No | Weak |
| RAG-only baseline | Retrieves greenhouse documents before generating a response | No | No | Yes | No | Weak |
| Proposed system | Uses BCD validation, data quality, Agentic RAG, and safety blocking | Yes | Yes | Yes | Yes | Strong |

## 3. Baseline 1: Rule-Based System

### Description

The rule-based baseline uses fixed threshold rules to decide greenhouse actions. It does not use an LLM, RAG, or BCD validation.

Example rules:

| Condition | Action |
|---|---|
| Temperature > 33°C | Turn on fan |
| Soil moisture < 30% | Activate water pump |
| Light intensity < 500 lux | Turn on grow light |
| Humidity > 85% | Turn on fan |
| Missing value | Show missing data warning |

### Expected Strengths

- Fast and easy to implement.
- Produces deterministic output.
- Works well for simple threshold cases.

### Expected Weaknesses

- Cannot explain decisions using retrieved evidence.
- Cannot detect invalid BCD codes unless extra logic is added.
- Cannot handle complex context or conflicting sensor conditions well.
- May execute unsafe actions when data looks numeric but is actually corrupted.

## 4. Baseline 2: LLM-Only System

### Description

The LLM-only baseline sends raw sensor data directly to a language model and asks it to recommend greenhouse actions.

Example prompt:

```text
You are a smart greenhouse assistant.
Given the following sensor data, recommend the next action.

Temperature: 34.5°C
Humidity: 72%
Soil moisture: 24%
Light intensity: 18000 lux
Water flow: 0 ml/min

Return action, explanation, and confidence.
```

### Expected Strengths

- Can generate natural language explanations.
- Can reason flexibly about multiple sensor values.
- Easy to adapt to different greenhouse scenarios.

### Expected Weaknesses

- May hallucinate unsupported agricultural knowledge.
- Does not know whether BCD data is valid.
- May trust missing, overflow, or corrupted sensor values.
- May produce inconsistent action format across test cases.

## 5. Baseline 3: RAG-Only System

### Description

The RAG-only baseline retrieves relevant greenhouse documents before asking the LLM to generate a recommendation. However, it does not include BCD validation or a data quality module.

Example pipeline:

```text
Sensor data
    -> Query construction
    -> Retrieve greenhouse guideline chunks
    -> LLM recommendation
    -> Output with evidence
```

### Expected Strengths

- Produces more grounded explanations than LLM-only.
- Can cite agricultural guidelines.
- Reduces hallucination compared with LLM-only.

### Expected Weaknesses

- Still assumes that sensor data is reliable.
- May generate evidence-supported but unsafe actions if the input data is corrupted.
- Does not block actuator control when invalid BCD or overflow is detected.
- Does not quantify sensor reliability.

## 6. Proposed System

### Description

The proposed system uses the full reliability-aware pipeline:

```text
Sensor data
    -> BCD conversion and validation
    -> Invalid BCD / overflow detection
    -> Sensor data quality assessment
    -> RAG retrieval
    -> Agentic reasoning
    -> Safe actuator action or blocked warning
```

### Expected Strengths

- Detects invalid BCD digits before AI reasoning.
- Detects overflow, missing data, abnormal values, and conflicting sensor conditions.
- Uses retrieved evidence to support recommendations.
- Produces structured JSON output.
- Blocks automatic actuator control when data is unreliable.

### Expected Weaknesses

- More complex than the baselines.
- May have higher latency due to validation, retrieval, and agent reasoning.
- Requires carefully designed test cases and labels.

## 7. Shared Input and Output Format

All systems must receive the same sensor test cases from `dataset.md`.

The final output should be normalized into the following fields for comparison:

| Field | Meaning |
|---|---|
| `case_id` | Test case ID |
| `predicted_status` | Normal / Warning / Critical / Blocked |
| `predicted_action` | Recommended actuator action or warning |
| `automatic_control_allowed` | Whether the system allows actuator control |
| `explanation` | Natural language reason |
| `evidence` | Retrieved document evidence, if available |
| `confidence` | System confidence score, if available |
| `latency_ms` | End-to-end response time |

## 8. Comparison Criteria

The baselines and proposed system will be compared using these criteria:

| Criterion | Why It Matters |
|---|---|
| Decision correctness | Checks whether the output matches the expected action |
| Invalid data handling | Checks whether unsafe input is detected |
| Robustness | Checks performance under missing, fault, overflow, and conflict cases |
| Explainability | Checks whether the system explains why an action is chosen |
| Evidence support | Checks whether the output cites retrieved greenhouse knowledge |
| Safety behavior | Checks whether actuator control is blocked when data is unreliable |
| Latency | Checks whether the system is still suitable for real-time support |

## 9. Expected Result Pattern

The expected result is not that the proposed system is always faster. The expected result is:

- Rule-based baseline should be fastest but less flexible.
- LLM-only baseline should produce readable explanations but may fail under corrupted data.
- RAG-only baseline should improve evidence support but may still trust invalid sensor data.
- Proposed system should perform best in invalid BCD, overflow, missing data, and conflicting sensor scenarios.
- Proposed system should provide the strongest safety behavior because it can block automatic control.

## 10. Example Comparison Table

| Case | Expected Action | Rule-Based | LLM-Only | RAG-Only | Proposed System |
|---|---|---|---|---|---|
| Normal | No action | Correct | Correct | Correct | Correct |
| Low soil moisture | Activate pump | Correct | Correct | Correct with evidence | Correct with evidence |
| Invalid BCD | Block control | Incorrect or not detected | May recommend action | May recommend action | Correctly blocked |
| Humidity overflow | Block control | May warn | May trust value | May trust value | Correctly blocked |
| Conflicting sensor | Request validation | Weak | Unstable | Partially correct | Correctly cautious |

## 11. Role in Research Questions

| Research Question | Baseline Role |
|---|---|
| RQ1 | Shows that simple systems do not validate decimal representation |
| RQ2 | Tests whether invalid BCD and overflow detection improve reliability |
| RQ3 | Tests whether reliability score and data quality improve decision safety |
| RQ4 | Compares full Agentic RAG behavior under normal and faulty scenarios |

## 12. Summary

The baseline comparison is necessary to prove the contribution of the proposed system. A good result should show that BCD validation and data quality assessment are not just extra modules, but important safety layers that help Agentic RAG avoid unsafe decisions when greenhouse sensor data is corrupted or unreliable.
