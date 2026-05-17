# Sensor-Action Mapping Table (Smart Greenhouse)

This table defines the system inputs (sensors), their physical meanings, and the corresponding control signals or next states executed by the Finite State Machine (FSM).

| Sensor / Input | Physical Meaning | Anomalous Condition | Target Control Action / Next State |
|---|---|---|---|
| **Temperature** | Measures ambient Celsius temperature | Extreme Heat / Cold | Transition to `COOLING` (fans/misters ON) or `HEATING` (heating lamp ON). |
| **Air Humidity** | Measures ambient water vapor percentage | Extremely dry / humid | Coupled with temperature to adjust misters or boost ventilation. |
| **Soil Moisture** | Measures soil water percentage | Severe drought (< threshold) | Transition to `WATERING` state (activate drip-irrigation pump). |
| **Light (Lux)** | Measures ambient light intensity (Lux) | Dark during daytime / Scorching sun | Turn on supplemental grow lights or lower shading screens. |
| **Timer Clock** | FSM synchronization and debounce clock | (Anti-chattering support) | Lock current state and ignore sensor fluctuations until the timer finishes its cycle. |

## Sensor Data Quality Module (SDQM) Integration
The system performs cross-sensor comparison (Sensor Fusion) to catch hardware faults before changing control states:
- **Data Conflict:** Soil moisture reads 0% (indicating desert-dry soil) while temperature is 20°C and air humidity is 95% (indicating wet, cool rainy conditions). -> *AgriAgent detects soil sensor fault.*
- **Data Fault/Missing:** Light sensor stays at 0 Lux at noon (indicative of disconnected cabling). -> *Agent discards light reading and keeps shading screens open.*
