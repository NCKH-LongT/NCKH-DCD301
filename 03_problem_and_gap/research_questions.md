# research_question.md

# Research Questions

## Research Title

BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems

---

# Main Research Question

How can BCD arithmetic error detection improve the reliability and explainability of sensor data processing in AIoT smart greenhouse systems?

---

# RQ1

## Research Question

How can real-time greenhouse sensor data be integrated with BCD arithmetic processing and agricultural knowledge retrieval to support explainable AIoT decision-making?

## Purpose

This research question investigates:

- integration between sensor data and AIoT systems,
- BCD-based arithmetic processing,
- and explainable recommendation generation using RAG.

The objective is to:

- collect real-time sensor data,
- process decimal arithmetic correctly,
- retrieve relevant agricultural knowledge,
- and generate explainable recommendations.

---

# RQ2

## Research Question

How does BCD arithmetic validity affect sensor data quality and recommendation reliability in smart greenhouse monitoring systems?

## Purpose

This question evaluates:

- how invalid BCD codes indicate sensor anomalies,
- how arithmetic overflow affects reliability,
- and how BCD correction logic contributes to data validation.

The objective is to:

- detect invalid decimal representations,
- identify arithmetic anomalies,
- and improve confidence scoring for AIoT recommendations.

---

# RQ3

## Research Question

Can an Agentic RAG framework integrated with BCD error detection improve contextual relevance and explainability compared with rule-based, LLM-only, and RAG-only approaches?

## Purpose

This question compares the proposed framework with baseline systems.

The evaluation includes:

- recommendation correctness,
- contextual relevance,
- explainability,
- robustness,
- and safety.

The proposed framework includes:

- BCD validation,
- sensor quality checking,
- RAG retrieval,
- and agent reasoning.

---

# RQ4

## Research Question

How effective is the proposed framework under normal, missing-data, invalid-BCD, sensor-fault, and conflicting-sensor scenarios?

## Purpose

This question evaluates system robustness under different conditions.

Test scenarios include:

- normal sensor data,
- missing sensor values,
- invalid BCD codes,
- arithmetic overflow,
- sensor faults,
- and conflicting sensor readings.

The objective is to evaluate:

- reliability,
- confidence stability,
- fault tolerance,
- and recommendation safety.

---

# Sub-Questions for BCD Arithmetic

## RQ4.1

Which binary codes are valid and invalid BCD representations?

---

## RQ4.2

Why must the system add 0110 when a BCD arithmetic result exceeds decimal 9?

1001_2 + 0001_2 = 1010_2

1010_2 + 0110_2 = 1\ 0000_2

---

## RQ4.3

How can the BCD error detection expression be derived?

Err = Cy + S_3S_2 + S_3S_1

---

# Expected Outputs

The research is expected to produce:

- Valid and invalid BCD code tables
- BCD error detection logic
- Smart greenhouse AIoT architecture
- Sensor quality analysis module
- Agentic RAG recommendation workflow
- Explainable recommendation output
- Baseline comparison results
- Scenario-based evaluation metrics

