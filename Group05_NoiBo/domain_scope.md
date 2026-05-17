# Domain Scope

## Research Theme 8: Memory & Error Detection

---

# Selected Domain

Reliable IoT Sensor Data Transmission

---

# 1. Domain Description

In IoT systems, sensor data is often transmitted through networks or digital communication channels. During data transmission, signal noise or hardware faults may alter one or more bits of the transmitted data.

This may lead to:
- inaccurate data,
- incorrect sensor information,
- system processing errors,
- or reduced reliability of the communication system.

To improve transmission reliability, this research applies Hamming Code (7,4) to detect and correct single-bit errors in binary data.

---

# 2. Research Scope

This research focuses on:
- studying the operating mechanism of Hamming Code,
- calculating parity bits for 4-bit data,
- encoding data using Hamming Code (7,4),
- detecting errors in received data,
- calculating the syndrome to identify the error position,
- correcting 1-bit errors during data transmission.

---

# 3. Scope Limitation

This research is limited to the following scope:
- only Hamming Code (7,4) is used,
- only single-bit errors are handled,
- multiple-bit errors are not processed,
- no implementation on real hardware,
- sensor data is simulated using simple binary data.

---

# 4. Reason for Choosing the Domain

The group chose the domain "Reliable IoT Sensor Data Transmission" because:
- it is closely related to Error Detection & Correction,
- it has practical applications in IoT and communication systems,
- it is easy to simulate and test,
- it is suitable for a conference/student research project,
- it helps the group better understand parity bits, syndrome calculation, and error correction mechanisms.

---

# 5. Expected Outcome

The proposed system is expected to:
- detect errors in received data,
- identify the error position using the syndrome,
- automatically correct single-bit errors,
- output the corrected data and error-handling status.