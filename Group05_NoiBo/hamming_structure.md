# Hamming Code (7,4) Structure

## Introduction
Hamming Code (7,4) is an error detection and correction code used to detect and correct single-bit errors.

## Structure of Hamming (7,4)

The code contains:
- 4 data bits
- 3 parity bits

Total:
- 7 bits

## Bit Positions

| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| Type | P1 | P2 | D1 | P4 | D2 | D3 | D4 |

Where:
- P1, P2, P4 are parity bits
- D1–D4 are data bits

## Parity Check Groups

| Parity Bit | Checks Positions |
|---|---|
| P1 | 1,3,5,7 |
| P2 | 2,3,6,7 |
| P4 | 4,5,6,7 |

## Formula for Parity Bits

2^r >= m + r + 1

Where:
- m = number of data bits
- r = number of parity bits

For 4-bit data:
- r = 3

Therefore:
- Hamming (7,4) requires 3 parity bits.