# Topic Proposal

## 1. Group Information

- **Class:** SE1930
- **Group:** 6
- **Leader:** Phạm Lê Nhật Minh - SE193155
- **Members:** - Phan Trí Dũng - SE193224
  - Trần Minh Nhựt - SE193149
  - Lê Nguyễn Hoàng Lộc - SE193098

## 2. Proposed Title

- **English title:** Implementing Arbitrary Logic Functions using Decoders and OR Gates for Automated Synthesis
- **Vietnamese title:** Hiện thực hóa các hàm logic bất kỳ sử dụng bộ giải mã (Decoder) và cổng OR phục vụ tổng hợp logic tự động

## 3. Application Domain

Electronic Design Automation (EDA), VLSI, and Combinational Logic Circuit Design.

## 4. Problem Statement

In traditional digital logic design, implementing a Boolean function requires custom, irregular networks of basic logic gates (AND, OR, NOT). This manual routing process becomes exponentially complex, hardware-inefficient, and prone to human error when handling large or irregular Boolean functions in modern IC design. There is a need for a standardized, modular approach to logic synthesis.

## 5. Motivation

As modern semiconductor systems scale (e.g., in Machine Learning hardware, Binarized Neural Networks, or complex VLSI architectures), minimizing transistor count, power consumption, and routing complexity is critical. Standardizing logic implementation using a Decoder-OR architecture not only optimizes physical hardware resources but also enables algorithmic verification and paves the way for fully automated, machine-readable logic synthesis workflows.

## 6. Target Users

Hardware Engineers, Digital Circuit Designers, EDA Tool Developers, and VLSI Architecture Researchers.

## 7. Proposed Method

Instead of AI models, this hardware-centric project utilizes the following core algorithms and architectural methods:
- **Boolean Decomposition Algorithm:** To partition input variables and handle complex logic functions.
- **Algorithmic Logic Verification:** To mathematically prove the 1-to-1 equivalence between minterms and decoder outputs.
- **Automated Routing Generation:** To translate mathematical equations into structured hardware connections (JSON schema).
- **Decoder-OR Synthesis Architecture:** Utilizing optimized hardware topologies (e.g., assessing advantages like 3-Transistor Logic equivalents) over discrete gate networks.

## 8. System Features

1. Parse input Boolean equations and verify their mathematical equivalence to canonical minterm expressions.
2. Automatically decompose variables for efficient hardware mapping.
3. Map identified minterms strictly to the corresponding hardware output pins of a Decoder.
4. Generate a standardized, machine-readable JSON routing schema that dictates the physical connections between Decoder outputs and OR-gate inputs.

## 9. Expected Contribution

1. A standardized, automated procedure to translate any Boolean function into a Decoder-OR hardware configuration.
2. Algorithmic and theoretical verification proving the accurate mapping of minterms to decoder outputs, eliminating human routing errors.
3. Demonstrated hardware efficiency (e.g., transistor count reduction and structural modularity) of the proposed architecture compared to traditional discrete gate networks.

## 10. Evaluation Plan

- **Dataset:** Standard benchmark combinational circuits (e.g., 1-bit full adder, BCD to 7-segment display decoder).
- **Baseline:** Traditional logic implementations using discrete basic logic gates (AND/OR/NOT).
- **Metrics:** Hardware efficiency metrics including transistor count, gate count (structural complexity), and modularity.
- **Expert evaluation:** Verification of the automated JSON routing logic correctness by VLSI instructors or domain experts.
- **User survey:** N/A (The evaluation focuses purely on quantitative hardware metrics and mathematical accuracy).

## 11. Related Papers

| No | Title | Year | Source | Link / DOI |
|---|---|---|---|---|
| 1 | Accuracy recovery: A decomposition procedure for the synthesis of partially-specified Boolean functions | 2023 | INTEGRATION, the VLSI journal | https://www.sciencedirect.com/science/article/pii/S0167926022001791 |
| 2 | Optimization of CMOS Decoders Using Three-Transistor Logic | 2025 | MDPI Electronics | https://www.mdpi.com/2079-9292/14/5/914 |
| 3 | Interactive Algorithms for the Verification of the Equality between Complex and Simplified Boolean-Algebra Expressions in Digital Decoders | 2020 | Review of Computer Engineering Research | https://archive.conscientiabeam.com/index.php/76/article/view/1476 |
