# Domain Scope

## Selected Domain
Smart Greenhouse Monitoring

---

## Rationale for Choosing This Domain

Smart greenhouse monitoring is suitable for this topic because:

1. It uses multiple sensors that operate continuously.
2. It is easy to simulate real-time sensor data.
3. It involves many numerical calculations.
4. It can be integrated with BCD arithmetic.
5. It is suitable for creating sensor error test cases.
6. It fits AIoT and embedded system contexts.

---

## Role of the BCD Adder in the System

The BCD adder is used to:

- add decimal-based sensor data
- process arithmetic operations for display output
- check overflow conditions
- detect invalid BCD codes

Example:

28 + 15 = 43

If the sum is greater than 9:

- the system must add `0110` for BCD correction.

---

## System Objectives

The system needs to:

- receive greenhouse sensor data
- check sensor data quality
- detect invalid BCD values
- use Agentic RAG to generate recommendations
- return explanations and confidence scores

---

## Sensors Used

- Temperature sensor
- Humidity sensor
- Soil moisture sensor
- Light sensor
- Water flow sensor

---

## Possible System Actions

- Turn on fan
- Turn off fan
- Start irrigation
- Stop irrigation
- Turn on grow light
- Send warning notification

---

## Research Contribution

This topic does not only build a basic IoT system.

The main contributions are:

- applying BCD arithmetic and error detection
- improving the reliability of sensor data
- integrating data quality checking into an Agentic RAG AIoT framework

---

## Implementation Scope

The system will:

- simulate real-time sensor data
- build BCD error detection logic
- build a RAG pipeline
- build an agent workflow
- evaluate the system under different sensor error scenarios

The system will not include:

- real hardware fabrication
- large-scale deployment
- commercial greenhouse system implementation
