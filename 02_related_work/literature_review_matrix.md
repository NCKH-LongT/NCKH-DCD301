# Literature Review Matrix

| Paper | Year | Venue | Problem | Method | Dataset / System | Limitation | Relation to our work |
|---|---:|---|---|---|---|---|---|
| Subrahmanyam et al. — Mixed-logic decoder design | 2023 | Springer (LN in EE) | High transistor count, power and delay in conventional decoders | Mixed-logic (TG/PTL/CMOS) decoder to reduce transistors and switching capacitance | Schematic simulations of small decoder blocks | No post-layout/parasitic analysis; limited scalability and fan-out study | Shows practical low-power decoder styles we can compare for energy/area baseline |
| Lim et al. — Decoder-LUT for ECC | 2024 | IEEE TVLSI | Timing skew and glitches in gate-level ECC implementations | Centralized decoder + structured OR/NOR selection (LUT-like) to balance paths | ECC combinational blocks (simulation/RTL) | Area inefficiency for sparse functions; exponential growth for large n | Demonstrates performance gains (frequency, glitch power) useful as baseline for latency/robustness trade-offs |
| Gerasimenko & Zakrevskij — Automated synthesis | 2022 | Microprocessors & Microsystems | EDA tools inefficient for large decoder-based designs (PQC) | Boolean decomposition + hierarchical decoders + multiplexer-based reconstruction | Large boolean functions, FPGA/ASIC mapping experiments | Focus on single-output functions; limited shared-decoder optimization | Provides an automated synthesis approach we can adapt for hierarchical/shared decoders in multi-output systems |

Usage notes:

- The *Relation to our work* column helps the team identify which parts of each paper can be reused (architecture, methods, evaluation metrics).
- Add rows when new papers are included; use the DOI list in `paper_list.md` for quick lookup.
