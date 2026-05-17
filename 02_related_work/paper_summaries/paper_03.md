# Paper 03 Summary

## Citation
- **Title:** FPGA Based System Login Security Lock Design Using Finite State Machine
- **Authors:** Saroch, et al.
- **Year:** 2012
- **Source:** IOSR Journals (Indexed in Semantic Scholar)
- **Link:** https://www.semanticscholar.org/paper/FPGA-Based-System-Login-Security-Lock-Design-Using-Journals-Saroch/33f014663cc4503d921461014700b614fed36adb

## Problem
- Standard software login mechanisms are vulnerable to operating system-level breaches. Hardware-defined authentication is needed to guarantee that a lock cannot be bypassed by software overrides.

## Method
- The paper details the design of a secure login lock utilizing an automated FSM written in VHDL. The lock only grants access when a strict, sequential binary sequence is entered by the user.

## Dataset / Tools
- **Tools:** VHDL, Xilinx ISE, and Spartan-3 FPGA kit.

## Evaluation
- The circuit was evaluated by measuring its maximum operating frequency ($f_{max}$) and estimating power consumption through simulation reports.

## Results
- The VHDL-synthesized FSM executed perfectly at high frequencies, successfully blocking unauthorized states and keeping power consumption low.

## Limitations
- The password sequence length was hardcoded into the FSM logic, making it inflexible for users to change the password without modifying the hardware code.

## Relevance to our topic
- This paper is a direct reference for our project's core logic, as it models a hardware-based sequential lock that closely mirrors our target `1011` sequence detection.

## Possible improvement
- Our group can design a more flexible FSM that allows password re-programming through an administrative state.
