# System Output Specification & Schema

## 1. Technical Output Format

The final output of the closed-loop AIoT smart greenhouse execution cycle must be exported as a single, structurally unified **JSON file**.

This JSON output represents the result after the system has completed the following processing stages:

1. Raw greenhouse sensor data collection
2. BCD arithmetic validation
3. Invalid BCD code detection
4. Overflow and abnormal value checking
5. Sensor data quality assessment
6. Agentic RAG knowledge retrieval
7. AI Agent reasoning and control decision generation

The purpose of this output is to ensure that every actuator command is traceable, explainable, and based only on validated sensor data.

## 2. Mandatory Schema Fields

To ensure system reliability, safety, and usability, each generated JSON file must include the following components:

### 2.1 Timestamp

The system must include the exact time when the decision was generated.

### 2.2 System Status

The output must clearly indicate the overall system condition.

Possible values include:

* `Normal`
* `Warning`
* `Critical`
* `Blocked`

The status `Blocked` must be used when invalid BCD data, overflow, or unreliable sensor data is detected.

### 2.3 Sensor Data

The JSON file must include the current greenhouse sensor readings, such as:

* Temperature
* Humidity
* Soil moisture
* Light intensity
* Water flow

### 2.4 BCD Validation Result

The system must report whether the decimal sensor data passed BCD validation.

This section should include:

* BCD validity status
* Invalid BCD code detection result
* Overflow detection result
* Decimal correction status
* Error flags if any problem is found

### 2.5 Data Quality Assessment

The system must include a data quality result to show whether the sensor data is reliable enough for AI-based decision-making.

This section may include:

* Data quality score
* Sensor reliability status
* Detected abnormal values
* Missing or inconsistent data

### 2.6 Device Control Commands

The JSON file must include explicit actuator control commands only if the input sensor data is valid and reliable.

Possible actuator commands include:

* Turn on/off fan
* Activate water pump
* Turn on/off grow light
* Stop automatic control
* Send sensor error warning

Each command must include the actuator name, status, and quantitative parameters if needed.

Example quantitative parameters:

* Water volume in milliliters
* Fan speed level
* Lighting duration
* Pump duration

### 2.7 Reasoning Explanation

The output must include a clear natural language explanation describing why the AI Agent generated the control action.

The explanation must mention:

* Which sensor value caused the decision
* Whether the BCD validation passed
* Why the actuator action is necessary
* How the action helps maintain greenhouse conditions

### 2.8 Verification Evidence

The output must include evidence retrieved by the Agentic RAG module.

This section must contain:

* Document title
* Exact quote from the retrieved reference document
* Explanation of how the quote supports the decision

This improves transparency, traceability, and user trust.

### 2.9 Safety Decision

The output must include a safety decision field.

If the sensor data contains invalid BCD codes, overflow, or unreliable values, the AI Agent must block automatic actuator control and generate an alert instead.

## 3. Sample JSON Output Schema: Valid Sensor Data

```json
{
  "timestamp": "2026-05-20T16:45:00Z",
  "system_status": "Warning",
  "sensor_data": {
    "temperature_celsius": 34.5,
    "humidity_percent": 72,
    "soil_moisture_percent": 24,
    "light_intensity_lux": 18000,
    "water_flow_ml_per_min": 120
  },
  "bcd_validation": {
    "status": "Valid",
    "invalid_bcd_code_detected": false,
    "overflow_detected": false,
    "decimal_correction_status": "Passed",
    "error_flags": []
  },
  "data_quality_assessment": {
    "quality_status": "Reliable",
    "quality_score": 0.93,
    "abnormal_values": [
      "soil_moisture_percent"
    ],
    "missing_data": false
  },
  "control_commands": [
    {
      "actuator": "Fan",
      "status": "ON",
      "reason": "Temperature and humidity are above the safe range."
    },
    {
      "actuator": "Water Pump",
      "status": "ON",
      "volume_ml": 300,
      "reason": "Soil moisture is below the recommended level."
    }
  ],
  "reasoning": "The BCD validation module confirms that all decimal sensor values are valid and no overflow is detected. The greenhouse temperature is high and soil moisture is low, so the AI Agent activates the fan to reduce heat and activates the water pump to restore soil moisture.",
  "verification": {
    "document_title": "Smart_Greenhouse_Control_Guideline.pdf",
    "exact_quote": "When greenhouse temperature exceeds the safety threshold, ventilation should be activated. When soil moisture falls below the recommended level, irrigation should be applied to prevent plant water stress.",
    "evidence_usage": "The quote supports the decision to turn on the fan and activate the water pump."
  },
  "safety_decision": {
    "automatic_control_allowed": true,
    "reason": "Sensor data is valid, BCD validation passed, and data quality score is reliable."
  }
}
```

## 4. Sample JSON Output Schema: Invalid BCD Data

```json
{
  "timestamp": "2026-05-20T17:10:00Z",
  "system_status": "Blocked",
  "sensor_data": {
    "temperature_celsius": null,
    "humidity_percent": 68,
    "soil_moisture_percent": 31,
    "light_intensity_lux": 17500,
    "water_flow_ml_per_min": 100
  },
  "bcd_validation": {
    "status": "Invalid",
    "invalid_bcd_code_detected": true,
    "overflow_detected": false,
    "decimal_correction_status": "Failed",
    "error_flags": [
      "INVALID_BCD_TEMPERATURE_VALUE"
    ]
  },
  "data_quality_assessment": {
    "quality_status": "Unreliable",
    "quality_score": 0.42,
    "abnormal_values": [
      "temperature_celsius"
    ],
    "missing_data": false
  },
  "control_commands": [
    {
      "actuator": "Automatic Control",
      "status": "BLOCKED",
      "reason": "Invalid BCD code detected in temperature sensor data."
    }
  ],
  "reasoning": "The AI Agent does not execute actuator commands because the temperature value failed BCD validation. Since the data may be corrupted, automatic fan or irrigation control could lead to unsafe greenhouse operation.",
  "verification": {
    "document_title": "Greenhouse_Sensor_Data_Validation_Manual.pdf",
    "exact_quote": "Automatic control decisions should not be executed when sensor data is invalid, missing, or unreliable.",
    "evidence_usage": "The quote supports blocking actuator control when the sensor value fails validation."
  },
  "safety_decision": {
    "automatic_control_allowed": false,
    "reason": "Invalid BCD code detected. Sensor data must be checked before control execution."
  },
  "recommendation": "Check the temperature sensor module, BCD encoding process, and data transmission path before retrying automatic control."
}
```

## 5. Data Flow Explanation

The system output is generated through the following data flow:

```text
Raw Sensor Data
        ↓
BCD Arithmetic Processing
        ↓
BCD Error Detection
        ↓
Sensor Data Quality Assessment
        ↓
Agentic RAG Knowledge Retrieval
        ↓
AI Agent Reasoning
        ↓
JSON Control Output
        ↓
Actuator Control or Safety Blocking
```

## 6. Safety Rule

The AI Agent must follow this safety rule:

```text
If BCD validation fails, overflow is detected, or sensor data quality is unreliable, the system must block automatic actuator control and generate a warning instead.
```

This rule ensures that the smart greenhouse system does not make control decisions based on corrupted or unreliable decimal sensor data.

## 7. Role in the Proposed System

This output schema supports the proposed topic:

**BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems**

The schema connects hardware-level BCD validation, IoT sensor data quality assessment, Agentic RAG reasoning, and safe actuator control into one unified JSON output.

The final output is not only a control command. It also includes validation status, data quality evidence, reasoning explanation, retrieved reference evidence, and safety decision.
