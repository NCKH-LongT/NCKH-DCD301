# Research Questions (RQs) - Theme 5: Registers and Counters

## RQ-05: Design of a Synchronous Mod-10 Counter Using D Flip-Flops and Invalid State Handling

- **Explanation:** This task requires designing a logic circuit that cyclically counts from 0 to 9, where all Flip-Flops share the same Clock signal (synchronous operation). Since 4 Flip-Flops are used (capable of representing up to 16 states from 0–15), the circuit must include a logic mechanism to handle the invalid states from 10 to 15. If the circuit accidentally enters one of these states due to noise or disturbances, it should not become stuck; instead, it must automatically return to a valid counting state.

---

## RQ5.1: Construct the State Transition Table for the Synchronous Mod-10 Counter

- **Explanation:** Describe the steps for listing the Present State (`Q3Q2Q1Q0`) and the Next State (`Q3+Q2+Q1+Q0+`) for decimal values 0 through 9. For the invalid states from 10–15, define their next states as well (commonly forced back to `0000`) in order to support the design of a self-correcting circuit.

---

## RQ5.2: Use Karnaugh Maps (K-maps) to Derive the Excitation Equations for Each D Flip-Flop

- **Explanation:** Explain how to use 4-variable Karnaugh Maps for each input `D3`, `D2`, `D1`, `D0`. Since, for a D Flip-Flop, the input equation is identical to the next-state equation (`D = Q+`), the K-map method helps simplify these logic expressions into the most optimized combination of AND, OR, and NOT gates.

---

## RQ5.3: Self-starting Mechanism for Recovery from Invalid States

- **Explanation:** Explain the principle of the “self-starting” mechanism. When the circuit is affected by electrical noise and jumps into invalid binary states from `1010` (10) to `1111` (15), the logic equations designed in RQ5.2 ensure that the next clock pulse forces the circuit back into a valid state (for example, `0000`). This allows the system to continue operating normally without requiring a manual Reset button.