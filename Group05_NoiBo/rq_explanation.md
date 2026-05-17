# Research Question (RQ) Explanation

## Research Theme 8: Memory & Error Detection

---

# RQ-08

## Question

For a 4-bit data word, determine the number of parity bits required to construct a Hamming code. Identify the syndrome and describe the process of locating an erroneous bit when the data is received.

## Explanation

RQ-08 focuses on the use of Hamming Code for detecting and correcting errors during binary data transmission.

The research objectives are:

- determine the number of required parity bits,
- generate Hamming code for 4-bit data,
- calculate the syndrome value,
- detect transmission errors,
- identify the position of the erroneous bit.

The purpose of this research is to improve data reliability during transmission or storage processes.

---

# RQ8.1

## Question

What formula is used to determine the number of parity bits required for m-bit data?

## Explanation

The number of parity bits in Hamming Code is determined using the formula:

:contentReference[oaicite:0]{index=0}

Where:

- **m**: number of data bits.
- **r**: number of parity bits.

This formula ensures that the system has enough combinations to:

- identify all possible error positions,
- include one additional state representing no error.

Parity bits are used to detect and correct transmission errors.

---

# RQ8.2

## Question

Why are 3 parity bits required for 4-bit data in Hamming (7,4) code?

## Explanation

For 4-bit data:

- m = 4

Using the formula:

:contentReference[oaicite:1]{index=1}

Testing with **r = 2**:

:contentReference[oaicite:2]{index=2}

- 4 < 7 → Not sufficient.

Testing with **r = 3**:

:contentReference[oaicite:3]{index=3}

- 8 ≥ 8 → Condition satisfied.

Therefore, 3 parity bits are required.

**Total bits:**

- 4 data bits + 3 parity bits = 7 bits.
- This is called Hamming (7,4) code.

---

# RQ8.3

## Question

How is the syndrome calculated and how is it used to identify the error position?

## Explanation

The syndrome is calculated by rechecking the parity bits after the encoded data is received.

**The process includes:**

1. Receive the encoded Hamming data.
2. Recalculate the parity checks.
3. Compare the parity results.
4. Generate the syndrome value.
5. Use the syndrome to determine the error position.

**Example:**

- **Syndrome = 000** → No error.
- **Syndrome = 100** → Error at bit position 4.

After identifying the error position, the incorrect bit can be flipped to recover the original data. The syndrome allows the system to detect and correct single-bit errors without retransmitting the entire data.
