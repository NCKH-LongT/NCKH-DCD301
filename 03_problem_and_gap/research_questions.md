# research_question.md

# Research Questions

## Research Title

**Smart Greenhouse Monitoring with BCD-Based Error Detection**

---

# Main Research Question

**How can BCD-based error detection be used to check sensor data in a smart greenhouse monitoring system?**

---

# RQ1

## Research Question

**How can greenhouse sensor values be converted into BCD format?**

## Purpose

This question investigates how greenhouse sensor values such as temperature, humidity, soil moisture, and light intensity can be represented as decimal numbers and converted into Binary Coded Decimal (BCD) format.

The objective is to:

- use simulated greenhouse sensor data,
- convert decimal sensor values into BCD format,
- represent each decimal digit using 4-bit BCD,
- and prepare the converted data for validation and error detection.

Example:

```text
Temperature = 28°C

Decimal digits:
2 and 8

BCD:
2 = 0010
8 = 1000

Final BCD:
0010 1000
```

---

# RQ2

## Research Question

**How can the system detect invalid BCD values and overflow errors?**

## Purpose

This question evaluates how the system can identify invalid BCD codes and detect overflow when sensor values exceed the allowed range.

The objective is to:

- detect valid BCD values from `0000` to `1001`,
- detect invalid BCD values from `1010` to `1111`,
- detect overflow values,
- detect abnormal sensor readings,
- and prevent faulty sensor data from being used directly in monitoring alerts.

Valid BCD values:

```text
0000 = 0
0001 = 1
0010 = 2
0011 = 3
0100 = 4
0101 = 5
0110 = 6
0111 = 7
1000 = 8
1001 = 9
```

Invalid BCD values:

```text
1010
1011
1100
1101
1110
1111
```

---

# RQ3

## Research Question

**How can the system show warning alerts when sensor data is invalid or abnormal?**

## Purpose

This question examines how the system displays warning alerts when sensor data is missing, invalid, overflow, or abnormal.

The objective is to:

- show raw sensor data,
- show BCD value,
- show validation status,
- detect missing sensor values,
- detect abnormal readings,
- and display warning alerts on a simple dashboard.

Example alert cases:

| Condition | Alert |
|---|---|
| Valid data | Normal |
| Invalid BCD value | Invalid BCD value detected |
| Missing data | Missing sensor data |
| Overflow | Sensor value exceeds allowed range |
| Abnormal temperature | High temperature warning |
| Low soil moisture | Low soil moisture warning |

---

# Sub-Questions for BCD-Based Error Detection

## RQ3.1

Which binary codes are valid and invalid BCD representations?

## RQ3.2

How can decimal greenhouse sensor values be converted into BCD format?

## RQ3.3

How can invalid BCD values from `1010` to `1111` be detected?

## RQ3.4

How can overflow or abnormal sensor readings be detected and shown as warning alerts?

---

# BCD Arithmetic Error Detection Logic

BCD only allows decimal digits from 0 to 9.

If a BCD arithmetic result is greater than 9 or produces a carry, the system must add `0110` to correct the result.

Example:

```text
1001₂ + 0001₂ = 1010₂
```

In decimal:

```text
9 + 1 = 10
```

However, `1010₂` is invalid in BCD because BCD only allows values from `0000` to `1001`.

So the system adds `0110`:

```text
1010₂ + 0110₂ = 1 0000₂
```

This represents decimal 10 in BCD:

```text
0001 0000
```

BCD correction condition:

```text
Err = Cy + S3S2 + S3S1
```

Where:

- `Cy` is the carry output,
- `S3`, `S2`, and `S1` are sum bits,
- `Err` indicates that BCD correction is needed.

This logic helps detect invalid BCD arithmetic results and prevents incorrect sensor data processing.

---

# Expected Outputs

The research is expected to produce:

- A simulated smart greenhouse prototype using sample sensor data.
- A BCD conversion and validation module for greenhouse sensor values.
- BCD-based error detection for invalid BCD values.
- Overflow detection for sensor values outside the allowed range.
- Missing data detection when sensor values are empty or unavailable.
- Abnormal reading detection for unusual greenhouse conditions.
- A simple dashboard showing raw data, BCD value, validation status, and alerts.
- Basic testing using valid data, invalid BCD, overflow, missing data, and abnormal sensor scenarios.

---

# Simple System Flow

```text
Sample Sensor Data
        ↓
BCD Conversion
        ↓
BCD Validation
        ↓
Error Detection
        ↓
Dashboard Alert
```

Detailed flow:

```text
Temperature / Humidity / Soil Moisture / Light Data
        ↓
Check Missing Data
        ↓
Convert Decimal Value to BCD
        ↓
Validate BCD Digits
        ↓
Check Overflow and Abnormal Readings
        ↓
Generate Validation Status
        ↓
Display Dashboard Alert
```

---

# Proposed System Architecture

```text
+--------------------------+
| Simulated Sensor Data    |
| - Temperature            |
| - Humidity               |
| - Soil Moisture          |
| - Light Intensity        |
+------------+-------------+
             |
             v
+--------------------------+
| BCD Conversion Module    |
| Decimal to BCD           |
+------------+-------------+
             |
             v
+--------------------------+
| BCD Validation Module    |
| Valid / Invalid BCD      |
+------------+-------------+
             |
             v
+--------------------------+
| Error Detection Module   |
| - Invalid BCD            |
| - Overflow               |
| - Missing Data           |
| - Abnormal Reading       |
+------------+-------------+
             |
             v
+--------------------------+
| Simple Dashboard         |
| - Raw Data               |
| - BCD Value              |
| - Validation Status      |
| - Warning Alert          |
+--------------------------+
```

---

# Example Sensor Data

| Sensor | Raw Value | BCD Value | Validation Status | Alert |
|---|---:|---|---|---|
| Temperature | 28°C | 0010 1000 | Valid | Normal |
| Humidity | 65% | 0110 0101 | Valid | Normal |
| Soil Moisture | 20% | 0010 0000 | Valid | Low soil moisture warning |
| Light Intensity | 850 lux | 1000 0101 0000 | Valid | Normal |
| Temperature | 60°C | 0110 0000 | Valid but Abnormal | High temperature warning |
| Humidity | Missing | N/A | Invalid | Missing sensor data |
| Soil Moisture | Invalid BCD 1010 | 1010 | Invalid | Invalid BCD value detected |
| Humidity | 130% | 0001 0011 0000 | Valid BCD but Overflow | Humidity overflow warning |

---

# Example Dashboard Output

## Valid Sensor Data

```text
Sensor: Temperature
Raw Data: 28°C
BCD Value: 0010 1000
Validation Status: Valid
Alert: Normal
```

## Abnormal Sensor Data

```text
Sensor: Temperature
Raw Data: 60°C
BCD Value: 0110 0000
Validation Status: Valid BCD, but Abnormal
Alert: High temperature warning
```

## Missing Sensor Data

```text
Sensor: Humidity
Raw Data: Missing
BCD Value: N/A
Validation Status: Invalid
Alert: Missing sensor data
```

## Invalid BCD Data

```text
Sensor: Soil Moisture
Raw Data: Invalid BCD
BCD Value: 1010
Validation Status: Invalid
Alert: Invalid BCD value detected
```

## Overflow Sensor Data

```text
Sensor: Humidity
Raw Data: 130%
BCD Value: 0001 0011 0000
Validation Status: Valid BCD, but Overflow
Alert: Humidity value exceeds allowed range
```

---

# Testing Scenarios

| Scenario | Example Input | Expected Result |
|---|---|---|
| Valid data | Temperature = 28°C | Convert to valid BCD and show normal status |
| Valid humidity | Humidity = 65% | Convert to valid BCD and show normal status |
| Low soil moisture | Soil Moisture = 20% | Show low soil moisture warning |
| Invalid BCD | BCD value = 1010 | Show invalid BCD alert |
| Invalid BCD range | BCD value from 1010 to 1111 | Mark the data as invalid |
| Overflow | Humidity = 130% | Show overflow warning |
| Missing data | Sensor value is null or empty | Show missing data alert |
| Abnormal temperature | Temperature = 60°C | Show high temperature warning |
| Abnormal light | Light intensity exceeds expected range | Show abnormal light warning |
| BCD arithmetic error | 1001 + 0001 = 1010 | Detect invalid BCD result and apply correction logic |

---

# Evaluation Method

The system can be evaluated using scenario-based testing.

The evaluation focuses on:

- whether decimal sensor values are correctly converted into BCD format,
- whether valid BCD values are accepted,
- whether invalid BCD values are rejected,
- whether overflow values are detected,
- whether missing data is detected,
- whether abnormal sensor readings generate warning alerts,
- and whether the dashboard correctly displays raw data, BCD value, validation status, and alerts.

Example evaluation metrics:

| Metric | Description |
|---|---|
| BCD Conversion Accuracy | Checks whether decimal values are correctly converted to BCD |
| Invalid BCD Detection | Checks whether invalid BCD values are detected |
| Overflow Detection | Checks whether out-of-range sensor values are detected |
| Missing Data Detection | Checks whether empty or null values are detected |
| Alert Correctness | Checks whether the correct warning message is shown |
| Dashboard Clarity | Checks whether the output is easy to understand |

---

# Scope of the Project

This project focuses on a simple simulation-based smart greenhouse monitoring system.

The project includes:

- simulated sensor data,
- decimal to BCD conversion,
- BCD validation,
- invalid BCD detection,
- overflow detection,
- missing data detection,
- abnormal sensor reading detection,
- and simple dashboard output.

The project does not require:

- advanced artificial intelligence,
- Agentic RAG,
- complex IoT hardware,
- cloud deployment,
- or production-level real-time sensor integration.

Optional hardware such as Arduino or ESP32 can be used, but simulation is enough for this project.

---

# Short Description

This research focuses on using BCD-based error detection to check the reliability of sensor data in a smart greenhouse monitoring system. The system uses simulated sensor data, converts decimal sensor values into BCD format, validates the BCD values, detects invalid data, overflow errors, missing data, and abnormal readings, then displays warning alerts through a simple dashboard.

The goal is to make sensor data checking more reliable, understandable, and suitable for a student-level smart greenhouse prototype.
