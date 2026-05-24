# Contributions (Planned / Draft)

This document lists the expected contributions of our project based on the current literature review and proposed directions.

1. Shared-decoder architecture for multi-output combinational logic: design methods to share minterm generation across multiple outputs to reduce area and redundant logic.
2. Partial minterm generation strategy: algorithms to generate only activated minterms for sparse boolean functions to improve area efficiency.
3. EDA-aware decomposition flow: automated variable partitioning guided by energy/area metrics and generation of RTL (Verilog) suited for FPGA/ASIC mapping.
4. Empirical evaluation framework: benchmark suite and measurement scripts to compare decoder-based vs gate-level implementations on metrics: area (LUTs/est. gates), maximum frequency, glitch-induced dynamic power, and synthesis/routing results.
5. Demonstration and validation: FPGA prototype or RTL post-route estimates to validate area/frequency tradeoffs.

These contributions will be refined after further literature additions and preliminary experiments.
