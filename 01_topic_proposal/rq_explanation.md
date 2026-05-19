# RQ Explanation

## Research Topic

**BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems**

---

## RQ1

### Original RQ

How can real-time IoT sensor data be integrated with domain-specific agricultural knowledge to support explainable decision-making in smart agriculture?

### Explanation

RQ1 focuses on integrating real-time sensor data with agricultural knowledge to support intelligent decision-making.

In this topic:

- Greenhouse sensors send temperature, humidity, light, and soil moisture data.
- The data is processed using digital logic and an AIoT system.
- The RAG system retrieves relevant agricultural technical documents.
- The agent generates recommendations such as turning on the fan or starting irrigation.

Example:

- If the temperature is too high and the humidity is low, the system recommends turning on the fan and starting irrigation.

The system needs to explain:

- why the recommendation was made
- which sensor data was used
- which document or evidence supports the decision

---

## RQ2

### Original RQ

How does sensor data quality affect the reliability of AIoT-based agricultural recommendations?

### Explanation

RQ2 focuses on sensor data quality.

In this topic:

- Sensor data is represented using BCD.
- Invalid BCD codes may indicate:
  - sensor failure
  - data transmission error
  - noisy or corrupted data

Examples:

Valid BCD:

- `0000` → 0
- `1001` → 9

Invalid BCD:

- `1010`
- `1111`

The system uses:

- BCD error detection logic
- invalid code checking
- overflow checking

to evaluate the reliability of sensor data.

If the data contains an error:

- the confidence score will decrease
- the recommendation will become less certain

---

## RQ3

### Original RQ

Can an Agentic RAG framework improve the contextual relevance and explainability of agricultural decision support compared with rule-based or LLM-only approaches?

### Explanation

RQ3 evaluates whether Agentic RAG performs better than:

- rule-based systems
- LLM-only systems
- RAG-only systems

In this topic:

- Rule-based system:
  - only checks sensor thresholds.

- LLM-only system:
  - uses an LLM but has no knowledge base.

- RAG-only system:
  - uses documents but does not check sensor data quality.

- Proposed system:
  - includes BCD error detection
  - checks sensor data quality
  - uses RAG
  - applies agent reasoning

The proposed system is expected to provide:

- more accurate recommendations
- clearer explanations
- safer behavior when sensor errors occur

Evaluation metrics:

- Recommendation accuracy compared with ground-truth scenarios
- Explainability score based on whether clear evidence is provided
- Safe-failure rate based on whether the system avoids dangerous recommendations when sensor data is faulty

---

## RQ4

### Original RQ

How effective is the proposed framework under normal, missing-data, sensor-fault, and conflicting-sensor scenarios?

### Explanation

RQ4 evaluates the system under different scenarios, including:

- normal data
- missing data
- sensor faults
- conflicting sensor readings

In this topic:

- invalid BCD codes can simulate sensor faults
- carry overflow can simulate arithmetic anomalies
- the system must detect and handle these errors

Example:

- If the temperature sensor reports `1111` in BCD, the value is invalid.
- The system must:
  - detect the error
  - reduce the confidence score
  - avoid unsafe recommendations

The goal is to improve the reliability of AIoT-based decision support.
