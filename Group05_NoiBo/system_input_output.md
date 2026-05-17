# System Input, Output, and Processing Flow

**Domain:** Reliable IoT Sensor Data Transmission using Hamming Code (7,4)  
**Objective:** Detect and automatically correct single-bit errors (SEC) to ensure IoT data integrity over noisy wireless channels.

---

## 1. System Inputs

### 1.1. Raw Sensor Data
* **Source:** Physical IoT sensors (e.g., DHT22 temperature/humidity, vibration sensors).
* **Signal Type:** Analog or digital telemetry signals via hardware interfaces (I2C, SPI, UART).

### 1.2. Partitioned Data Blocks
* **Format:** The raw continuous bitstream is processed and sliced into fixed 4-bit data blocks.
* **Mathematical Representation:** $D = \{D_1, D_2, D_3, D_4\}$, where each $D_i \in \{0, 1\}$.

---

## 2. System Outputs

### 2.1. Validated Payload Data
* **Format:** Clean 4-bit original data blocks ($D = \{D_1, D_2, D_3, D_4\}$) extracted after stripping the parity bits.
* **Destination:** Forwarded to the central database (MySQL/MongoDB) and real-time monitoring dashboards.

### 2.2. Error-Correction Telemetry & Logs
* **System Status Codes:**
  * `00`: Perfect transmission (No errors detected).
  * `01`: 1-bit error detected and successfully corrected.
  * `10`: Severe error ($\ge$ 2 bits flipped), exceeding Hamming SEC capacity (triggers ARQ retransmission request).
* **Error Index:** Integer value ($1 \dots 7$) pinpointing the exact corrupted bit position.

---

## 3. End-to-End Processing Flow

### Step 1: Sensing and Slicing
The edge micro-controller periodically samples sensor telemetry and slices the binary format into independent 4-bit data blocks ($D_1, D_2, D_3, D_4$).

### Step 2: Hamming (7,4) Encoding
Parity bits ($P_1, P_2, P_4$) are mapped to positions that are powers of 2 ($1, 2, 4$). 

**The final 7-bit codeword structure is:**
| Bit Position (Index) | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Bit Identifier** | $P_1$ | $P_2$ | $D_1$ | $P_4$ | $D_2$ | $D_3$ | $D_4$ |

The parity values are computed using logical XOR ($\oplus$) operations based on even parity:
* $P_1 = D_1 \oplus D_2 \oplus D_4$
* $P_2 = D_1 \oplus D_3 \oplus D_4$
* $P_4 = D_2 \oplus D_3 \oplus D_4$

Resulting 7-bit codeword: $C = \{P_1, P_2, D_1, P_4, D_2, D_3, D_4\}$.

### Step 3: Wireless Transmission
The 7-bit codeword is transmitted via wireless protocols (LoRa, Wi-Fi, RF). Channel noise may cause a single-bit flip, turning the sent codeword $C$ into the received codeword $C' = \{P_1', P_2', D_1', P_4', D_2', D_3', D_4'\}$.

### Step 4: Syndrome Calculation
At the receiver end (Gateway/Server), the system calculates a 3-bit Syndrome vector $S = [S_4, S_2, S_1]$ by recalculating the parity checks:
* $S_1 = P_1' \oplus D_1' \oplus D_2' \oplus D_4'$
* $S_2 = P_2' \oplus D_1' \oplus D_3' \oplus D_4'$
* $S_4 = P_4' \oplus D_2' \oplus D_3' \oplus D_4'$

### Step 5: Error Isolation and Auto-Correction
The receiver evaluates the binary value of the Syndrome vector ($S_4 S_2 S_1$):
* **Case 1:** $S = [0, 0, 0]$ (Decimal 0) $\rightarrow$ Transmission is clean; no action required.
* **Case 2:** $S \neq [0, 0, 0]$ (Decimal $1 \dots 7$) $\rightarrow$ The decimal value points exactly to the corrupted bit index. The system automatically flips the faulty bit back to its correct state ($Bit_n = \neg Bit_n'$).

### Step 6: Decoding and Storage
The system discards the parity bits at positions 1, 2, and 4. The clean 4-bit data payload ($D_1 D_2 D_3 D_4$) is reassembled, logged into the database, and pushed to the monitoring dashboard.