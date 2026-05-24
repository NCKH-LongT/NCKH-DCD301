# Literature Review Matrix (Week 02)

This is a working matrix summarizing the key papers reviewed so far and how they relate to our project goals.

| Paper | Year | Venue | Problem | Method | Dataset / System | Limitation | Relation to our work |
|---|---:|---|---|---|---|---|---|
| Subrahmanyam et al. — Mixed-logic decoder design | 2023 | Springer (LN in EE) | High transistor count and power in conventional decoders | Mixed-logic (TG/PTL/CMOS) decoder to reduce transistors and switching capacitance | Schematic simulations of small decoder blocks | No post-layout analysis; limited scalability and fan-out study | Inform low-power baseline and transistor-level techniques |
| Lim et al. — Decoder-LUT for ECC | 2024 | IEEE TVLSI | Timing skew and glitching in gate-level ECC implementations | Centralized decoder + OR/NOR selection (LUT-like) | ECC combinational blocks (simulation/RTL) | Area inefficiency for sparse functions; exponential scaling | Provide architectural baseline for latency/glitch improvements |
| Gerasimenko & Zakrevskij — Hierarchical decoder synthesis | 2022 | Microprocessors & Microsystems | EDA inefficiency for large decoder-based functions (PQC) | Boolean decomposition + hierarchical decoders + multiplexers | Large Boolean functions; FPGA/ASIC mapping experiments | Single-output focus; limited shared-decoder optimization | Algorithmic approach for hierarchical decomposition we can extend |

Notes:
- Add 2–3 more papers focused on "sparse decoder" and "shared decoder" to complete the matrix.
- Use this matrix to select 2 benchmark functions for implementation (one sparse, one dense).
