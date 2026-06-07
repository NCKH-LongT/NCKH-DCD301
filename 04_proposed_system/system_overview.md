# System Overview

This document provides a comprehensive overview of the proposed system:

**BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems**

The core objective of this system is to improve the reliability of smart greenhouse decision-making by validating decimal sensor data before it is used by AI models or actuator control logic. The system combines **BCD arithmetic error detection**, **sensor data quality assessment**, and an **Agentic RAG-based decision support module** to generate safe, explainable, and traceable greenhouse control actions.

## 1. System Vision and Objective

Modern smart greenhouse systems depend heavily on sensors to monitor environmental conditions such as temperature, humidity, soil moisture, light intensity, and water flow. These sensor readings are often decimal values and may be affected by noise, sensor faults, transmission errors, invalid data encoding, or arithmetic overflow during processing.

Traditional AIoT automation systems may pass corrupted or unreliable sensor data directly into AI models or control algorithms. This can cause incorrect irrigation, ventilation, lighting, or warning decisions.

To solve this issue, the proposed system introduces a reliability-aware processing pipeline. Before sensor data is used for AI-based reasoning, the system validates decimal values through **BCD arithmetic error detection** and checks the overall quality of the sensor data. Only reliable and validated data is passed to the Agentic RAG module for decision-making.

The main objective is to ensure that every greenhouse control action is:

* Based on valid decimal sensor data
* Checked for BCD encoding errors
* Protected against overflow and arithmetic errors
* Evaluated for sensor reliability
* Supported by retrieved agricultural knowledge
* Explained clearly in a structured JSON output

## 2. Core Functional Components

The system lifecycle is built on a closed-loop execution pipeline consisting of five main components.

### A. Greenhouse Sensor Data Ingestion

**Purpose:**
This component collects raw environmental data from greenhouse sensors or simulated data files.

**Mechanism:**
The system reads real-time or simulated greenhouse telemetry from structured files such as `.csv` or `.xlsx`.

The expected sensor data includes:

* Temperature
* Air humidity
* Soil moisture
* Light intensity
* Water flow
* Optional pH value
* Optional CO₂ concentration

**Role in the system:**
This component acts as the entry point of the pipeline. It prepares raw sensor data for BCD encoding, arithmetic processing, validation, and AI-based decision support.

### B. BCD Arithmetic Error Detection Module

**Purpose:**
This component validates decimal sensor values at the arithmetic and encoding level.

**Mechanism:**
Sensor values are converted into Binary Coded Decimal (BCD) format before arithmetic processing. The BCD arithmetic module performs decimal operations such as addition, subtraction, comparison, and aggregation.

The BCD error detection module checks for:

* Invalid BCD codes
* Arithmetic overflow
* Decimal correction errors
* Invalid arithmetic output
* Abnormal decimal representation

Examples of invalid BCD codes include:

```text
1010, 1011, 1100, 1101, 1110, 1111
```

These values are invalid because valid BCD digits must only represent decimal numbers from 0 to 9.

**Role in the system:**
This module ensures that decimal sensor data is mathematically valid before it is used for data quality assessment or AI reasoning.

### C. Sensor Data Quality Assessment

**Purpose:**
This component evaluates whether the sensor data is reliable at the application level.

**Mechanism:**
After BCD validation, the system checks the sensor values for missing data, abnormal values, noise, spikes, and out-of-range readings.

The data quality layer performs:

* Missing value detection
* Range validation
* Noise and outlier detection
* Sensor fault warning
* Sensor reliability scoring

Example checks:

```text
Temperature must be within a realistic greenhouse range.
Soil moisture must not suddenly drop from 60% to 5% within a very short time.
Water flow must not be zero when the pump is marked as active.
```

**Role in the system:**
This component ensures that even mathematically valid data is still checked for real-world reliability before being passed to the AI Agent.

### D. Agentic RAG Decision Support Engine

**Purpose:**
This component provides explainable and knowledge-grounded decision-making.

**Mechanism:**
The Agentic RAG engine retrieves relevant agricultural knowledge from digitized documents such as greenhouse manuals, irrigation guidelines, crop growth instructions, and sensor fault handling documents.

When a sensor value crosses a safety threshold, the system generates a semantic query and retrieves supporting reference passages.

Example query:

```text
What should be done when soil moisture is low and greenhouse temperature is high?
```

The retrieved context is then passed to the AI Agent together with validated sensor data and data quality results.

**Role in the system:**
The RAG engine reduces unsupported AI decisions by grounding recommendations in reference documents.

### E. Intelligent AI Agent Control Core

**Purpose:**
This component generates safe, explainable, and structured greenhouse control actions.

**Mechanism:**
The AI Agent receives three synchronized inputs:

1. Validated greenhouse sensor data
2. BCD validation and data quality results
3. Retrieved agricultural knowledge from the RAG engine

The AI Agent then decides whether an actuator command should be generated or blocked.

Possible actuator actions include:

* Turn on ventilation fan
* Activate water pump
* Turn on grow light
* Stop automatic control
* Generate sensor error warning
* Request sensor revalidation

**Safety behavior:**
If the system detects invalid BCD data, overflow, missing values, or unreliable sensor readings, the AI Agent must not execute automatic actuator commands. Instead, it must output a warning and explain why the action is blocked.

## 3. High-Level Operational Flow

The proposed system follows this closed-loop processing flow:

1. **Sensor Data Collection**
   The system receives greenhouse sensor data from real sensors or simulated `.csv` / `.xlsx` files.

2. **BCD Encoding and Arithmetic Processing**
   Decimal sensor values are encoded into BCD format and processed by the BCD arithmetic unit.

3. **BCD Error Detection**
   The system checks for invalid BCD codes, overflow, and decimal correction errors.

4. **Sensor Data Quality Checking**
   The system checks for missing values, outliers, abnormal changes, and unreliable sensor behavior.

5. **Knowledge Retrieval**
   If a greenhouse parameter is outside the safe range, the Agentic RAG module retrieves relevant agricultural knowledge from the document store.

6. **AI Agent Reasoning**
   The AI Agent combines validated sensor data, BCD validation results, data quality status, and retrieved evidence to decide the next action.

7. **Command Generation or Safety Blocking**
   If the data is valid and reliable, the AI Agent generates actuator commands. If the data is invalid or unreliable, the AI Agent blocks automatic control and produces a warning.

8. **Structured JSON Output**
   The final decision is serialized into a JSON file containing sensor data, BCD validation status, data quality result, control command, reasoning explanation, verification evidence, and safety decision.

## 4. Example System Scenario

### Case 1: Valid Sensor Data

Input condition:

```text
Temperature = 34.5°C
Soil moisture = 24%
BCD validation = Valid
Overflow = False
Data quality = Reliable
```

System decision:

```text
Turn on fan.
Activate water pump with a defined water volume.
```

Reason:

```text
The temperature is high and soil moisture is below the recommended level. Since BCD validation passed and the data is reliable, automatic control is allowed.
```

### Case 2: Invalid BCD Sensor Data

Input condition:

```text
Temperature BCD digit = 1010
BCD validation = Invalid
Data quality = Unreliable
```

System decision:

```text
Block automatic control.
Generate sensor error warning.
```

Reason:

```text
The temperature value contains an invalid BCD code. The system cannot trust the sensor data, so actuator control is blocked to prevent unsafe greenhouse operation.
```

## 5. Expected System Output

The final system output is a structured JSON file defined in `data_flow.md`.

The output includes:

* Timestamp
* System status
* Sensor data
* BCD validation result
* Data quality assessment
* Actuator control commands
* AI reasoning explanation
* Retrieved verification evidence
* Safety decision
* Recommendation or warning message

This structured output ensures that the system can be connected to simulated actuators, dashboards, or future physical greenhouse control devices.

## 6. System Contribution

The proposed system contributes to smart greenhouse research by combining hardware-level decimal reliability with AI-based decision support.

The main contributions include:

* BCD arithmetic error detection for decimal sensor values
* Invalid BCD code and overflow detection
* Sensor data quality assessment for AIoT greenhouse systems
* Agentic RAG-based explainable recommendation generation
* Safety blocking when data is invalid or unreliable
* Structured JSON output for actuator control and traceability

## 7. Summary

The proposed system is a reliability-aware AIoT smart greenhouse framework. It does not rely only on raw sensor data or direct AI prediction. Instead, it validates decimal sensor values using BCD arithmetic error detection, evaluates sensor data quality, retrieves agricultural knowledge through Agentic RAG, and then generates safe and explainable control actions.

The core principle of the system is:

```text
No greenhouse actuator should be controlled automatically unless the sensor data is valid, reliable, and supported by retrieved evidence.
```

By following this principle, the system improves the safety, transparency, and reliability of AIoT smart greenhouse decision-making.
