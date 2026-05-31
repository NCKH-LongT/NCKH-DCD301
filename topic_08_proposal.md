# RESEARCH TOPIC PROPOSAL

## 1. General Information
* **Research Theme:** Theme 8: Memory & Error Detection
* **Topic Name:** Reliable IoT Sensor Data Transmission using Hamming Code (7,4)
* **Team Members:**
    * Huynh Anh Khoi - SE193685 
    * Nguyen Nhat An- SE192555
    * Huỳnh Thị Thanh Nguyên - SE183370
    * Nguyen Duong Hoai An - SE184221

---

## 2. Context & Problem Statement
In IoT ecosystems, telemetry data collected from physical sensors is continuously transmitted over noisy wireless channels. Due to environmental interference, hardware limitations, or channel degradation, binary data blocks are highly susceptible to single-bit flips (e.g., a `0` becoming a `1` or vice versa). Such errors compromise data integrity, leading to inaccurate system analytics and potentially flawed automated decisions.

To mitigate this, this research proposes an end-to-end simulation framework implementing the **Hamming Code (7,4)** algorithm. By embedding error-correcting capabilities directly into the data payload stream, the system can automatically detect and correct single-bit transmission errors without relying on heavy Automatic Repeat-reQuest (ARQ) retransmission overhead, thereby ensuring robust and reliable IoT communication.

---

## 3. Research Scope & Limitations
* **Scope:**
    * Deep-dive analysis of even-parity bit generation and Syndrome vector decoding logic.
    * Development of a software-based simulation pipeline that models sensory telemetry chunking, encoding, noisy transmission, error isolation, and autonomous correction.
* **Limitations:**
    * The architecture is strictly optimized for Single-Bit Error Correction (SEC).
    * Multiple-bit errors ($\ge$ 2 bits flipped) exceed the standard recovery scope of this implementation.
    * The system behaves as a high-fidelity software model; physical microcontroller hardware validation is omitted at this stage.

---

## 4. Expected Outcomes
1. **Core Algorithmic Library:** High-efficiency, modular Encoder and Decoder functions handling 4-bit data structures.
2. **Simulation System:** An end-to-end demonstrator executing data generation, noise injection, and real-time state recovery.
3. **Technical Schema & Documentation:** Formalized mathematical proofs, operational processing flows, and standardized JSON output data definitions for cloud/database ingestion.