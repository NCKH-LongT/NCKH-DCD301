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

## 2. Research Questions and Theoretical Solutions (RQ-09 to RQ9.3)

The project aims to answer and implement the following foundational sequential circuit and AIoT questions:

### RQ-09: Distinction between Combinational and Sequential Circuits. Why do Sequential Circuits require memory elements such as Latch or Flip-Flop?

*   **Combinational Circuits:** The output depends strictly on the current values of inputs at that exact moment. They do not feature feedback loops or memory elements.
*   **Sequential Circuits:** The output depends on both the current inputs and the previous states (operation history) of the circuit. They utilize feedback paths to return signals from memory elements to input terminals.
*   **Need for Memory:** Sequential circuits require Latch or Flip-Flop memory elements to store the "current state". Without them, the circuit would lose historical context and immediately act as a combinational circuit, making sequential operations impossible.

### RQ9.1: What factors determine the output of a Combinational Circuit?

*   The outputs of a combinational logic circuit depend solely on the **current physical input values** active at the logic gate terminals at that exact moment. They are completely independent of prior states or synchronization clock pulses.

### RQ9.2: How does the output of a Sequential Circuit depend on both the current input and the previous state?

*   **Mealy Machine:** Output is a function of both inputs and current state: $Y(t) = f(X(t), S(t))$. Output changes immediately when inputs shift.
*   **Moore Machine:** Output depends strictly on the current state: $Y(t) = g(S(t))$. Output only transitions synchronously with clock edges.
*   **Greenhouse Example:** If soil moisture drops below the threshold (current input), the FSM checks if the system is already in the `WATERING` state. If active, it maintains irrigation instead of re-triggering, preventing component degradation.

### RQ9.3: What roles do Latch and Flip-Flop play in storing the state of a Sequential Circuit?

*   **State Storage:** Each Latch/Flip-Flop holds a single binary digit (`0` or `1`), forming State Registers to represent complex FSM states.
*   **Feedback loop:** They capture the "Next State" signal, hold it, and feed it back to the input block as the "Present State" in the next clock cycle.
*   **Synchronization:** Latches are level-sensitive (asynchronous), while Flip-Flops are edge-triggered (synchronous), ensuring highly stable state transitions.

*For full solutions, see:* **rq_explanation.md**

---

## 3. Selected Domain & Scope (Smart Greenhouse)

The group focuses on the **Smart Greenhouse Control System** domain, encompassing:
- **Telemetry Inputs:** Temperature, air humidity, soil moisture, light intensity (Lux).
- **Sequential FSM States:** `IDLE` (Normal), `COOLING` (Ventilation active), `HEATING` (Heater active), `WATERING` (Pump active).
- **Actuators:** Water pumps, ventilation fans, heating lamps, shading screens.

*For more details, see:* **domain_scope.md**

---

## 4. Sensor-Action Mapping Table (IoT Telemetry & SDQM)

This table defines the system inputs (sensors), their physical meanings, and the corresponding control signals or next states executed by the FSM.

| Sensor / Input | Physical Meaning | Anomalous Condition | Target Control Action / Next State |
|---|---|---|---|
| **Temperature** | Measures Celsius temp | Extreme Heat / Cold | Transition to `COOLING` or `HEATING` state. |
| **Air Humidity** | Measures water vapor % | Extremely dry / humid | coupled with temperature to adjust fans/misters. |
| **Soil Moisture** | Measures soil water % | Severe drought | Transition to `WATERING` state (activate pump). |
| **Light (Lux)** | Measures light intensity | Day-darkness / Scorching sun | Turn grow lights ON or lower shading screens. |
| **Timer Clock** | FSM sync and debounce clock | (Anti-chattering support) | Lock current state and ignore sensor fluctuations until timer finishes. |

### Sensor Data Quality Module (SDQM) Integration
The system performs cross-sensor comparison to catch hardware faults before changing control states:
- **Data Conflict:** Soil moisture reads 0% (indicating desert-dry soil) while temperature is 20°C and air humidity is 95% (indicating wet, cool rainy conditions). -> *AgriAgent detects soil sensor fault.*
- **Data Fault/Missing:** Light sensor stays at 0 Lux at noon (indicative of disconnected cabling). -> *Agent discards light reading and keeps shading screens open.*

*For more details, see:* **sensor_action_table.md**

---

## 5. Standardized Output Model (JSON Schema)

The decision support system outputs telemetry diagnostic data and actuator actions using a strict JSON schema conforming 100% to the course guidelines, explicitly containing the mandatory keys: `status`, `action`, `confidence`, and `evidence`.

*For the schema design, see:* **system_output_schema.json**
