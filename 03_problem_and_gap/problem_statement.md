# problem_statement.md

# Problem Statement

## Title

BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems

---

# Background

Smart agriculture systems increasingly rely on AIoT (Artificial Intelligence of Things) technologies to automate environmental monitoring and decision-making processes. In smart greenhouse systems, IoT sensors continuously collect real-time environmental data such as temperature, humidity, soil moisture, and light intensity. These sensor readings are then processed by embedded systems and AI-based decision support frameworks to generate recommendations and control actions.

However, the reliability of AIoT recommendations strongly depends on the quality and correctness of sensor data. Sensor faults, communication noise, data corruption, and arithmetic overflow may lead to invalid or inconsistent sensor values. If incorrect data is processed without validation, the system may produce unsafe or inaccurate recommendations, such as unnecessary irrigation or incorrect environmental control actions.

Most existing smart agriculture systems focus primarily on cloud analytics, machine learning models, or IoT dashboards. Limited attention is given to hardware-level arithmetic validation and low-level data integrity checking during sensor data processing. In particular, Binary Coded Decimal (BCD) arithmetic error detection mechanisms are rarely integrated into AIoT sensor quality assessment frameworks.

BCD arithmetic is commonly used in embedded systems and digital displays because it preserves decimal representation directly. However, BCD operations require correction logic when arithmetic results exceed valid decimal ranges. Invalid BCD codes may indicate arithmetic overflow, sensor corruption, transmission error, or faulty sensor behavior. Therefore, BCD error detection can serve as an additional data quality verification layer for AIoT systems.

---

# Problem

Current AIoT smart agriculture systems lack hardware-assisted decimal arithmetic validation mechanisms capable of detecting invalid sensor computations and corrupted decimal representations in real time. Existing approaches mainly focus on high-level anomaly detection while ignoring low-level arithmetic integrity verification.

As a result:

- Invalid sensor values may propagate through the AIoT pipeline.
- Sensor quality assessment may become unreliable.
- Recommendation confidence may decrease.
- Faulty sensor data may trigger unsafe agricultural actions.

Furthermore, existing BCD adder studies mainly focus on arithmetic optimization and FPGA implementation, while existing AIoT smart agriculture studies mainly focus on sensor monitoring and machine learning. Very limited research integrates BCD arithmetic error detection with sensor quality analysis and explainable AIoT decision-support systems.

---

# Proposed Direction

This research proposes an AIoT smart greenhouse framework that integrates:

- BCD arithmetic processing,
- BCD error detection logic,
- sensor data quality assessment,
- Agentic RAG reasoning,
- and explainable recommendation generation.

The system will:

1. Collect real-time greenhouse sensor data.
2. Represent sensor values using BCD arithmetic.
3. Detect invalid BCD conditions and arithmetic overflow.
4. Evaluate sensor reliability based on arithmetic validity.
5. Integrate validated sensor data with agricultural knowledge retrieval.
6. Generate explainable recommendations with confidence scores.

The proposed framework aims to improve:

- sensor data reliability,
- recommendation safety,
- explainability,
- and robustness under faulty sensor conditions.

---

# Research Significance

This study contributes to:

- digital arithmetic applications in AIoT,
- hardware-assisted sensor validation,
- explainable smart agriculture systems,
- and reliable edge-based decision support.

The research also creates an interdisciplinary bridge between:

- digital logic design,
- embedded systems,
- FPGA/SoC engineering,
- AIoT,
- and smart agriculture applications.

