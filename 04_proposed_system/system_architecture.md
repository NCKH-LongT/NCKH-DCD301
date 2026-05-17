# System Architecture

## 1. Sensor & Recommended Action Table

| Sensor Name | Purpose / Function | Input Data | Recommended System Action |
| :--- | :--- | :--- | :--- |
| **Infrared Proximity Sensor (IR Proximity)** | Detects products moving on the conveyor belt to generate Clock pulses for the counter. | Digital Signal: `High` (Object Detected) / `Low` (No Object). | Generate one Clock Pulse for the Mod-10 counter to increment by one. |
| **Motor Current Sensor (ACS712)** | Monitors the current consumed by the packaging actuator to detect mechanical jams. | Analog Signal -> Converted into Ampere (A) values. | If the current exceeds the safe threshold due to a jam, stop the conveyor belt and trigger an alarm. |
| **Circuit State Monitor (Logic State Monitor)** | Monitors the outputs $Q_3Q_2Q_1Q_0$ of the counter to detect abnormal states. | Digital Signal (4-bit output from Flip-Flops). | If a state within the range `1010` - `1111` is detected, activate the noise-error logging mechanism while allowing the circuit to self-correct back to `0000`. |

---

## 2. Expected JSON Output Schema (`system_output_schema.json`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DecadeCounterSystemOutput",
  "type": "object",
  "properties": {
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "counter_status": {
      "type": "object",
      "properties": {
        "current_state_binary": {
          "type": "string",
          "pattern": "^[0-1]{4}$"
        },
        "current_state_decimal": {
          "type": "integer",
          "minimum": 0,
          "maximum": 15
        },
        "is_valid_state": {
          "type": "boolean"
        }
      },
      "required": [
        "current_state_binary",
        "current_state_decimal",
        "is_valid_state"
      ]
    },
    "sensor_data": {
      "type": "object",
      "properties": {
        "product_detected": {
          "type": "boolean"
        },
        "motor_current_ampere": {
          "type": "number"
        }
      },
      "required": [
        "product_detected",
        "motor_current_ampere"
      ]
    },
    "system_action": {
      "type": "object",
      "properties": {
        "command": {
          "type": "string",
          "enum": [
            "KEEP_COUNTING",
            "TRIGGER_PACKAGING",
            "SELF_STARTING_RESET",
            "EMERGENCY_STOP"
          ]
        },
        "description": {
          "type": "string"
        }
      },
      "required": [
        "command",
        "description"
      ]
    }
  },
  "required": [
    "timestamp",
    "counter_status",
    "sensor_data",
    "system_action"
  ]
}