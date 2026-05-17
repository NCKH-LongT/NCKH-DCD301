# 1. Selected Domain Name
**Smart Greenhouse Control System**

# 2. Rationale for Selecting the Domain
This domain is selected based on three core evaluation criteria of the project:
- **Compliance with the "Smart Agriculture" Guideline:** It represents a quintessential smart agriculture application, strictly aligning with the course requirements.
- **Application of Sequential Logic (FSM):** Greenhouse management operations (such as irrigation and heating control) do not occur instantaneously but instead require state memory and time delays (counters/timers). This serves as a practical demonstration of sequential circuits.
- **Data Quality (SDQM) Potential:** In agricultural environments, sensors are highly prone to faults (e.g., due to dust, extreme humidity, or degradation), generating rich test cases (data noise, loss, and contradiction) for analysis.

# 3. Sequential Circuit Analysis in Smart Greenhouse (Connecting to RQ9)
A greenhouse control system cannot rely solely on **combinational logic**.
*Example:* If a simple threshold rule is used: "If soil moisture < 40% turn ON the pump, else turn OFF", the pump would repeatedly switch ON and OFF every second when moisture oscillates near 40% (a phenomenon called chattering), rapidly damaging the pump.

Thus, the system must be designed as a **sequential circuit** with state memory:
- **States:** `IDLE` (Normal operation), `HEATING` (Heating active), `COOLING` (Ventilation/misting active), `WATERING` (Drip irrigation active).
- **Memory Elements (Flip-Flops):** When transitioning to the `WATERING` state, a hardware timer built from flip-flops is activated. The pump runs continuously for exactly 10 minutes (Output depends on the active state) even if sensors report moisture rising above 40% during the second minute.

# 4. System Inputs and Outputs
**Inputs (Real-Time Sensor Telemetry):**
```json
{
  "temperature": 35.5,
  "humidity": 60.0,
  "soil_moisture": 30.5,
  "light_lux": 15000
}
```

**Outputs (Agentic RAG Recommendation Output):**
- `current_state`: Active system state (e.g., `IDLE`).
- `next_state`: Target state transition (e.g., `WATERING`).
- `confidence`: Telemetry confidence rating.
- `explanation`: Contextual justification linking the decision to the agronomical guidelines.
