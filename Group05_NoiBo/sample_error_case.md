# Sample Error Detection and Correction Case

## Original Data
1011

---

## Step 1 — Encode Data

The 4-bit data ($m=4$) requires 3 parity bits ($r=3$), forming a Hamming (7,4) code. 
We place the parity bits at positions that are powers of 2 (1, 2, 4) using 1-based indexing.

**Bit Positions Setup:**
| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Bit Type** | P1 | P2 | D1 | P4 | D2 | D3 | D4 |
| **Value** | **0** | **1** | 1 | **0** | 0 | 1 | 1 |

**Parity Bit Calculations (Using Even Parity):**
* **P1** checks positions 1, 3, 5, 7:  
    $P1 = D1 \oplus D2 \oplus D4 = 1 \oplus 0 \oplus 1 = 0$
* **P2** checks positions 2, 3, 6, 7:  
    $P2 = D1 \oplus D3 \oplus D4 = 1 \oplus 1 \oplus 1 = 1$
* **P4** checks positions 4, 5, 6, 7:  
    $P4 = D2 \oplus D3 \oplus D4 = 0 \oplus 1 \oplus 1 = 0$

**Encoded Data Stream:** `0110011`

---

## Step 2 — Introduce Error (Transmission)

Assume signal interference occurs during transmission, causing a 1-bit error at **position 5** (D2 flips from `0` to `1`).

* **Received Data Stream:** `0110111`

---

## Step 3 — Calculate Syndrome

Upon receiving the data, the receiver recalculates the parity checks ($S_4 S_2 S_1$) to identify any discrepancies.

* **S1** (Checks 1, 3, 5, 7):  
    $S1 = P1 \oplus D1 \oplus D2 \oplus D4 = 0 \oplus 1 \oplus 1 \oplus 1 = 1$
* **S2** (Checks 2, 3, 6, 7):  
    $S2 = P2 \oplus D1 \oplus D3 \oplus D4 = 1 \oplus 1 \oplus 1 \oplus 1 = 0$
* **S4** (Checks 4, 5, 6, 7):  
    $S4 = P4 \oplus D2 \oplus D3 \oplus D4 = 0 \oplus 1 \oplus 1 \oplus 1 = 1$

**Syndrome Matrix ($S_4 S_2 S_1$):**
$$\text{Syndrome} = 101_2 = 5_{10}$$

Since the Syndrome value is $5$, the system mathematically pinpoints that the error occurred precisely at **bit position 5**.

---

## Step 4 — Correct Error & Extract Data

1.  **Error Correction:** Flip the corrupted bit at position 5 back to its original state (from `1` to `0`).
    * **Corrected Stream:** `0110011`
2.  **Data Extraction:** Extract the data bits from positions 3, 5, 6, and 7 ($D_1 D_2 D_3 D_4$).
    * **Final Recovered Data:** `1011` (Matches the original input perfectly).