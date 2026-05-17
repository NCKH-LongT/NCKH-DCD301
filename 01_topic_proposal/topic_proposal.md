# Research Topic Proposal

- **Class:** SE1930
- **Group:** G07
- **Proposed Project Title:** *A Data Quality-Aware Agentic RAG Framework for Real-Time AIoT Decision Support in Smart Greenhouse*
- **Research Theme:** Research Theme 9 - Basic Sequential Circuits

---

## 1. Problem Statement and Research Motivation

In modern high-tech agriculture, particularly within **Smart Greenhouse** environments, real-time control decisions (irrigation, ventilation, heating, shading) are crucial for crop yield and resource conservation.

However, practical AIoT control systems face two severe challenges:
1. **Sensor Data Quality Issues:** IoT sensors deployed in harsh greenhouse environments (high heat, humidity, dust) are highly susceptible to physical degradation, causing data drift, missing values, noise, or severe contradictions (e.g., soil moisture reading 0% while humidity is 95% and temperature is moderate).
2. **Limitations of Instantaneous Logic:** Relying solely on combinational logic thresholds (e.g., turning on the pump immediately when soil moisture is under 40% and off when above) causes severe control oscillation (chattering) which damages electrical actuators.

**Research Objective:**
To construct a state-aware **AgriAgent** that incorporates a **Finite State Machine (FSM)** based on sequential circuit design principles, integrated with an **Agentic RAG** framework (anchored on agronomical textbooks) and a **Sensor Data Quality Module (SDQM)**. This system will execute optimal control recommendations, autonomously resolve sensor quality faults, and provide zero-hallucination explainable justifications.

---

## 2. Research Domain & Scope
The group focuses on the **Smart Greenhouse Control System** domain, encompassing:
- **Telemetry Inputs:** Temperature, air humidity, soil moisture, light intensity (Lux).
- **Sequential FSM States:** `IDLE`, `COOLING`, `HEATING`, `WATERING`.
- **Actuators:** Water pumps, ventilation fans, heating lamps, shading screens.
- **Data Quality:** Filtering noise, handling missing packets, and detecting conflicting sensor anomalies using cross-channel sensor fusion.

*For more details, see:* **domain_scope.md**

---

## 3. Targeted Research Questions (RQs)
The project aims to answer and implement the following foundational sequential circuit and AIoT questions:

1. **RQ-09:** Distinction between Combinational and Sequential Circuits. Why do Sequential Circuits require memory elements such as Latch or Flip-Flop?
2. **RQ9.1:** What factors determine the output of a Combinational Circuit?
3. **RQ9.2:** How does the output of a Sequential Circuit depend on both the current input and the previous state?
4. **RQ9.3:** What roles do Latch and Flip-Flop play in storing the state of a Sequential Circuit?

*For theoretical solutions, see:* **rq_explanation.md**

---

## 4. Standardized Output Model (JSON Schema)
The decision support system outputs telemetry diagnostic data and actuator actions using a strict JSON schema conforming 100% to the course guidelines, explicitly containing the mandatory keys: `status`, `action`, `confidence`, and `evidence`.

*For the schema design, see:* **system_output_schema.json**
