# Proposed Research Contributions

To address the identified research gaps, the project **"A Data Quality-Aware Agentic RAG Framework for Real-Time AIoT Decision Support in Smart Agriculture"** proposes the following core academic and practical contributions:

---

## 1. A Novel Data Quality-Aware Agentic RAG Framework

*   **Description:** We propose a comprehensive, closed-loop AIoT architecture that represents the first system to directly couple real-time physical telemetry streams with high-level cognitive LLM reasoning through an orchestrating agent.
*   **Contribution:** Rather than treating sensor noise and data anomalies as isolated preprocessing tasks, this framework introduces data quality metrics directly into the core reasoning loop of the LLM agent. This enables the agent to dynamically adjust its reasoning pathway and tool usage based on the real-time reliability of its physical environment.

---

## 2. An Adaptive Real-Time Sensor Data Quality Module

*   **Description:** We design and implement a specialized module to continuously detect and handle six common agricultural sensor data anomalies in real time:
    1.  *Sudden data loss (Missing Data)*
    2.  *Environmental noise (Outliers)*
    3.  *Sensor freeze faults (Stuck Sensors)*
    4.  *Hardware degradation (Sensor Drift)*
    5.  *Transmission lag (Timestamp Delay)*
    6.  *Physical inconsistency (Cross-Sensor Conflicts—e.g., extremely high temperature paired with saturated soil moisture).*
*   **Contribution:** We introduce a dynamic **Sensor Quality Score (SQS)** calculated in real-time. This metric serves as a decision gate for the agent, automatically triggering fallback reasoning schemas when primary sensors fail.

---

## 3. Stateful Agentic Reasoning Workflow and Unified Multi-Dimensional Confidence Scoring

*   **Description:** We develop a stateful agentic workflow utilizing LangGraph integrated with a Finite State Machine (FSM) representing the physical operational states of a smart greenhouse (Idle, Heating, Cooling, Watering, Lighting).
*   **Contribution:**
    *   **Unified Confidence Score (UCS):** We propose a multi-dimensional linear scoring model that quantifies the safety of physical control actions by combining real-time sensor quality, semantic RAG retrieval relevance, and logical consistency with FSM physical state transition rules:
        $$\text{Final Confidence} = 0.4 \times \text{Sensor Quality Score} + 0.3 \times \text{RAG Relevance Score} + 0.2 \times \text{Rule Consistency Score} + 0.1 \times \text{Historical Stability Score}$$
    *   **Causal & Teleological Explanation Generation:** We implement a counterfactual explainability method (based on Counterfactual Effect Size) that generates intuitive natural language explanations explaining the underlying physical motivations of an action, coupled with deterministic citations of vector database evidence.

---

## 4. Comprehensive Stress-Test Scenario Benchmark and Quantitative Performance Evaluation

*   **Description:** We establish a rigorous empirical validation benchmark consisting of **8 stress-test scenarios** (Normal, Warning, Critical, Missing Data, Sensor Fault, Conflicting Sensor, Wrong Context, Control Decision) and deploy **3 baseline architectures** (Rule-based, LLM-only, RAG-only).
*   **Contribution:** We provide the first comprehensive, quantitative evaluation demonstrating the robustness of a data-quality-aware agentic framework against classical baselines. We evaluate performance across multiple academic dimensions, including recommendation correctness, robustness under fault injections, latency, and explainability ratings based on standardized rubrics. This quantitative dataset directly answers the four core research questions (RQ1–RQ4) of the study.
