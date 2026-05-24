# Related Work Summaries (Week 02)

Short summaries of the three core papers reviewed this week:

1) Subrahmanyam et al. (2023) — Mixed-logic decoder design
- Problem: High transistor count, power and delay in conventional decoders.
- Approach: Combine transmission gates, pass-transistor logic and CMOS blocks to reduce transistor count and switching capacitance.
- Result: Schematic simulations show ~28–32% power reduction and significant transistor count reduction; lacks post-layout validation.

2) Lim et al. (2024) — Decoder-LUT architecture for ECC
- Problem: Timing skew and glitch power in gate-level ECC combinational logic.
- Approach: Centralized decoder generates minterms; structured OR/NOR selection creates regular, balanced paths similar to LUTs.
- Result: Improved max frequency (~15%), reduced glitch power (>40%), but area-inefficient for sparse functions.

3) Gerasimenko & Zakrevskij (2022) — Automated hierarchical decoder synthesis
- Problem: EDA tools struggle to generate efficient decoder-based designs for very large boolean functions (PQC use cases).
- Approach: Boolean decomposition, partitioning inputs into groups, generate local decoders and combine hierarchically with OR networks.
- Result: Faster synthesis and better mapping to FPGA/ASIC; limitations include single-output focus and limited sharing optimizations.
