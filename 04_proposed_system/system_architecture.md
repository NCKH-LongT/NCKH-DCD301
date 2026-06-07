
# System Architecture Specification

This document describes the architectural design and block-level components of the proposed system:

**BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems**

The system is designed as a modular AIoT-based decision support framework for smart greenhouse monitoring. It collects greenhouse sensor data, validates decimal values using BCD arithmetic error detection, evaluates sensor data quality, retrieves agricultural knowledge using Agentic RAG, and generates safe control decisions for greenhouse actuators.

## 1. High-Level Block Architecture

The system consists of five main operational layers that form a closed-loop execution pipeline:

```text
+--------------------------------------------------------------------------------+
|                              DATA INGESTION LAYER                              |
|                                                                                |
|  [Greenhouse Sensors / CSV / Excel Input]                                      |
|        |                                                                       |
|        v                                                                       |
|  [Raw Sensor Data Reader]                                                      |
|        |                                                                       |
|        v                                                                       |
|  Temperature | Humidity | Soil Moisture | Light Intensity | Water Flow         |
+--------------------------------------+-----------------------------------------+
                                       |
                                       v
+--------------------------------------------------------------------------------+
|                       BCD ARITHMETIC PROCESSING LAYER                          |
|                                                                                |
|  [Decimal Sensor Value Encoder]                                                |
|        |                                                                       |
|        v                                                                       |
|  [BCD Arithmetic Unit] ---> [Decimal Correction Logic]                         |
|        |                                                                       |
|        v                                                                       |
|  [BCD Error Detection Module]                                                  |
|        |                                                                       |
|        +--> Invalid BCD Code Detection                                         |
|        +--> Overflow Detection                                                 |
|        +--> Arithmetic Correction Error Detection                              |
+--------------------------------------+-----------------------------------------+
                                       |
                                       v
+--------------------------------------------------------------------------------+
|                         SENSOR DATA QUALITY CONTROL LAYER                      |
|                                                                                |
|  [Missing Value Checker]                                                       |
|        |                                                                       |
|        v                                                                       |
|  [Range Validation Filter]                                                     |
|        |                                                                       |
|        v                                                                       |
|  [Noise / Outlier Detection]                                                   |
|        |                                                                       |
|        v                                                                       |
|  [Sensor Reliability Scoring]                                                  |
+--------------------------------------+-----------------------------------------+
                                       |
                                       v
+--------------------------------------------------------------------------------+
|                         INTELLIGENT AGENTIC RAG LAYER                          |
|                                                                                |
|  [Validated Sensor Data]                                                       |
|        |                                                                       |
|        v                                                                       |
|  [Semantic Query Generator] <=======> [Vector Database / Document Store]       |
|        |                                      ^                                |
|        |                                      |                                |
|        v                                      v                                |
|  [Retrieved Agricultural Knowledge and Greenhouse Guidelines]                  |
|        |                                                                       |
|        v                                                                       |
|  +--------------------------------------------------------------------------+  |
|  |                              LLM AI AGENT                                |  |
|  |                                                                          |  |
|  |   [Reasoning Core] ---> [Safety Checker] ---> [Control Plan Generator]   |  |
|  |                                                                          |  |
|  |   [Structured JSON Output Formatter]                                     |  |
|  +--------------------------------------------------------------------------+  |
+--------------------------------------+-----------------------------------------+
                                       |
                                       v
+--------------------------------------------------------------------------------+
|                             ACTUATOR OUTPUT LAYER                              |
|                                                                                |
|  [Standard Execution JSON Output]                                              |
|        |                                                                       |
|        v                                                                       |
|  Fan Control | Water Pump Control | Grow Light Control | Warning Alert         |
+--------------------------------------------------------------------------------+
```

## 2. Detailed Component Breakdown

### 2.1 Data Ingestion Layer

The Data Ingestion Layer collects greenhouse environmental data from either real sensors or simulated files.

#### Main Components

**Telemetry Reader**

The Telemetry Reader parses incoming greenhouse data from `.csv`, `.xlsx`, or sensor stream input.

The expected sensor values include:

* Greenhouse temperature
* Air humidity
* Soil moisture
* Light intensity
* Water flow
* Optional pH value
* Optional CO₂ value

**Raw Sensor Data Formatter**

This component converts raw sensor readings into a unified internal structure before BCD encoding and validation.

Example raw input:

```json
{
  "temperature_celsius": 34.5,
  "humidity_percent": 72,
  "soil_moisture_percent": 24,
  "light_intensity_lux": 18000,
  "water_flow_ml_per_min": 120
}
```

### 2.2 BCD Arithmetic Processing Layer

This layer is the core hardware/data reliability layer of the proposed topic.

Its purpose is to process decimal sensor values using BCD arithmetic and detect low-level decimal representation errors before the data is used by AI models.

#### Main Components

**Decimal Sensor Value Encoder**

This component converts decimal sensor values into BCD format for arithmetic processing.

Example:

```text
Temperature = 34.5°C
BCD representation = 0011 0100 0101
```

**BCD Arithmetic Unit**

The BCD Arithmetic Unit performs decimal operations on sensor values.

Possible operations include:

* Decimal addition
* Decimal subtraction
* Decimal averaging
* Decimal comparison
* Sensor value aggregation

These operations may be used for calculating:

* Average temperature
* Total water flow
* Difference between current and threshold values
* Soil moisture deficit
* Environmental risk score

**Decimal Correction Logic**

BCD addition requires correction logic when a 4-bit digit result exceeds 9. This component ensures that arithmetic outputs remain valid decimal values.

**BCD Error Detection Module**

This module checks whether the BCD data is valid.

It detects:

* Invalid BCD codes, such as `1010`, `1011`, `1100`, `1101`, `1110`, `1111`
* Overflow during decimal calculation
* Decimal correction failure
* Invalid arithmetic output
* Sensor value representation error

If any BCD error is detected, the system must generate an error flag and stop automatic control execution.

Example error flags:

```text
INVALID_BCD_CODE
BCD_OVERFLOW
DECIMAL_CORRECTION_FAILED
ARITHMETIC_OUTPUT_INVALID
```

### 2.3 Sensor Data Quality Control Layer

After BCD validation, the system evaluates whether the sensor data is reliable at the application level.

This layer checks not only decimal correctness but also sensor reliability.

#### Main Components

**Missing Value Checker**

This component detects missing or null sensor values.

Example:

```text
temperature = null
soil_moisture = 24%
```

**Range Validation Filter**

This component checks whether sensor values are within realistic greenhouse ranges.

Example:

```text
Temperature safe range: 18°C - 35°C
Soil moisture safe range: 30% - 70%
Humidity safe range: 50% - 80%
```

**Noise and Outlier Detection**

This component detects abnormal spikes, sudden drops, or unrealistic sensor changes.

Example:

```text
Temperature jumps from 28°C to 80°C within one minute.
```

**Sensor Reliability Scoring**

Each sensor reading receives a reliability score.

Example:

```json
{
  "temperature_reliability": 0.95,
  "humidity_reliability": 0.91,
  "soil_moisture_reliability": 0.62
}
```

If the reliability score is too low, the AI Agent must avoid automatic actuator control and generate a warning.

### 2.4 Agentic RAG Layer

The Agentic RAG Layer combines validated sensor data with retrieved agricultural knowledge to generate explainable greenhouse decisions.

#### Main Components

**Knowledge Vectorization**

Agricultural documents, greenhouse manuals, irrigation guidelines, and plant care rules are divided into chunks and converted into vector embeddings.

Possible knowledge sources include:

* Greenhouse temperature control manuals
* Irrigation guidelines
* Plant growth condition documents
* Smart agriculture technical references
* Sensor fault handling procedures

**Semantic Query Generator**

This component generates search queries based on validated greenhouse sensor data.

Example:

```text
"What should be done when soil moisture is low and greenhouse temperature is high?"
```

**Context Retrieval Engine**

The retrieval engine searches the vector database and returns relevant knowledge passages.

Example retrieved context:

```text
"When soil moisture is below the recommended level, irrigation should be applied to prevent plant water stress."
```

### 2.5 LLM AI Agent and Decision Core

The LLM AI Agent is the reasoning and planning center of the system.

It receives:

* Validated sensor data
* BCD validation results
* Sensor data quality scores
* Retrieved agricultural knowledge
* Safety constraints

The AI Agent then decides whether to generate actuator commands or block automatic control.

#### Main Components

**Reasoning Core**

The Reasoning Core analyzes the current greenhouse condition.

Example reasoning:

```text
Soil moisture is below the recommended threshold, while BCD validation passed and no overflow was detected. Therefore, irrigation is allowed.
```

**Safety Checker**

The Safety Checker verifies whether actuator control is allowed.

Automatic control is blocked if:

* Invalid BCD code is detected
* Overflow occurs
* Sensor reliability score is too low
* Sensor value is missing
* Retrieved evidence does not support the action

**Control Plan Generator**

This component creates the actuator plan.

Possible actuator actions include:

* Turn on fan
* Turn off fan
* Activate water pump
* Turn on grow light
* Send sensor warning
* Block automatic control

**Structured JSON Output Formatter**

This component formats the final decision into the standard JSON schema defined in `data_flow.md`.

## 3. Communication Protocols and Data Contracts

The internal modules communicate through structured data objects.

The final boundary contract of the system is a unified JSON output.

The JSON output must include:

* Timestamp
* System status
* Sensor data
* BCD validation result
* Data quality assessment
* Device control commands
* Reasoning explanation
* Verification evidence from RAG
* Safety decision

The output format must follow the schema defined in:

```text
data_flow.md
```

## 4. Closed-Loop Execution Pipeline

The system follows this execution flow:

```text
Step 1: Collect greenhouse sensor data
        ↓
Step 2: Convert decimal sensor values into BCD format
        ↓
Step 3: Perform BCD arithmetic processing
        ↓
Step 4: Detect invalid BCD codes, overflow, and correction errors
        ↓
Step 5: Evaluate sensor data quality and reliability
        ↓
Step 6: Retrieve agricultural knowledge using Agentic RAG
        ↓
Step 7: AI Agent reasons over validated data and retrieved evidence
        ↓
Step 8: Generate structured JSON output
        ↓
Step 9: Execute actuator command or block unsafe action
```

## 5. Safety Policy

The system must follow a strict safety-first policy.

```text
If BCD validation fails, overflow is detected, or sensor data quality is unreliable, the AI Agent must block automatic actuator control and generate a warning.
```

This prevents the smart greenhouse system from making unsafe decisions based on corrupted, invalid, or unreliable sensor data.

## 6. Example System Behavior

### Case 1: Valid Data and Low Soil Moisture

Input condition:

```text
Soil moisture = 24%
BCD validation = Valid
Overflow = False
Data quality = Reliable
```

System output:

```text
Activate water pump with specified water volume.
```

Reason:

```text
The soil moisture value is below the recommended threshold, and the data passed BCD validation. Therefore, irrigation is allowed.
```

### Case 2: Invalid BCD Temperature Data

Input condition:

```text
Temperature BCD value = 1010
BCD validation = Invalid
Data quality = Unreliable
```

System output:

```text
Block automatic control and generate sensor error warning.
```

Reason:

```text
The temperature value contains an invalid BCD code. The AI Agent cannot trust the data and must not control the fan automatically.
```

## 7. Role in the Proposed Topic

This architecture supports the proposed research topic:

**BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems**

The architecture combines:

* BCD arithmetic processing
* Invalid BCD code detection
* Overflow detection
* Sensor data quality assessment
* Agentic RAG knowledge retrieval
* Explainable AI decision-making
* Safe actuator control

The main contribution of this architecture is that it improves the reliability of AIoT greenhouse decision-making by validating decimal sensor data before it is used by the AI Agent.

## 8. Summary

The proposed system is not only a smart greenhouse control framework. It is a reliability-aware AIoT architecture that connects hardware-level decimal error detection with AI-based decision support.

The key principle is:

```text
No actuator command should be executed unless the sensor data is valid, reliable, and supported by retrieved evidence.
```
