# research_gap.md

# Research Gap

## Existing Research Areas

Current studies related to this topic can generally be divided into three major categories:

1. BCD arithmetic and digital circuit design
2. AIoT smart agriculture systems
3. Sensor data quality and anomaly detection

---

# Gap 1: BCD Research Focuses Mainly on Arithmetic Optimization

Existing BCD adder studies primarily focus on:

- high-speed arithmetic,
- FPGA implementation,
- carry propagation optimization,
- hardware resource reduction,
- and low-power arithmetic architectures.

These works successfully explain:

- valid and invalid BCD representations,
- BCD correction logic,
- and decimal arithmetic processing.

However, most existing studies do not investigate how BCD error detection can be applied to real-world AIoT sensor reliability problems.

Specifically, current BCD studies rarely:

- connect arithmetic validity with sensor integrity,
- use invalid BCD codes for anomaly detection,
- or integrate BCD correction mechanisms into AIoT decision-support systems.

---

# Gap 2: AIoT Smart Agriculture Systems Lack Hardware-Level Arithmetic Validation

Most AIoT smart agriculture systems focus on:

- cloud-based monitoring,
- IoT dashboards,
- machine learning prediction,
- environmental automation,
- and high-level anomaly detection.

Although many systems evaluate sensor quality using statistical or AI-based approaches, limited attention is given to low-level arithmetic correctness during sensor data processing.

Current systems often assume:

- sensor values are already valid,
- decimal computations are correct,
- and embedded arithmetic operations are reliable.

As a result, hardware-level decimal arithmetic faults may remain undetected and propagate through the AIoT pipeline.

---

# Gap 3: Limited Integration Between Digital Logic and AIoT Data Quality Assessment

Existing sensor quality studies commonly detect:

- missing data,
- outliers,
- drift,
- timestamp inconsistency,
- and conflicting sensors.

However, few works consider invalid decimal arithmetic states as a form of sensor anomaly.

In particular:

- invalid BCD codes,
- arithmetic overflow,
- and decimal correction failures

are rarely treated as indicators of sensor corruption or transmission error.

Therefore, there is a research gap in integrating:

- BCD arithmetic validation,
- embedded error detection logic,
- and AIoT sensor quality assessment.

---

# Gap 4: Explainability and Reliability Under Faulty Sensor Conditions Remain Limited

Many existing AIoT recommendation systems provide:

- automatic actions,
- environmental recommendations,
- and predictive analytics.

However, several limitations remain:

- weak explainability,
- lack of confidence estimation,
- insufficient handling of corrupted sensor data,
- and poor robustness under fault scenarios.

Few studies combine:

- sensor quality analysis,
- arithmetic validation,
- knowledge retrieval,
- and explainable agent reasoning

within a unified framework.

---

# Identified Research Gap

Based on the literature review, there is limited research that integrates:

- BCD arithmetic error detection,
- sensor quality validation,
- AIoT smart greenhouse systems,
- Agentic RAG reasoning,
- and explainable decision support

into a single intelligent framework.

Most existing works study these components independently rather than as an integrated AIoT reliability architecture.

---

# Proposed Contribution

This research proposes a framework that combines:

- BCD arithmetic processing,
- invalid BCD detection,
- sensor quality assessment,
- Agentic RAG reasoning,
- and explainable recommendation generation

for reliable AIoT smart greenhouse monitoring.

The proposed system aims to:

- improve sensor reliability,
- detect arithmetic anomalies,
- reduce unsafe recommendations,
- and increase explainability under faulty sensor scenarios.
