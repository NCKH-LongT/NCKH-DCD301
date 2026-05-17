# Paper 02 Summary

## Citation
- **Title:** FPGA-based assistive framework for smart home automation
- **Year:** 2022
- **Source:** IEEE Xplore
- **Link:** https://ieeexplore.ieee.org/document/9845625/

## Problem
- Smart home systems require seamless integration of multiple security and automation sub-systems, but software-based microcontrollers often suffer from latency and security vulnerabilities when processing concurrent tasks.

## Method
- The authors propose a hardware-based smart home framework implemented on an FPGA. Within this framework, the password-protected door lock system is modeled as a dedicated sequential Finite State Machine (FSM).

## Dataset / Tools
- **Tools:** Xilinx Vivado, Verilog HDL, and a physical Nexys FPGA development board.

## Evaluation
- The system was evaluated based on resource utilization (Look-Up Tables, Flip-Flops) and physical hardware validation of the lock's operational states.

## Results
- The FSM successfully managed the password-verification process within a larger multi-tasking environment without software lag, proving the efficiency of hardware-level control.

## Limitations
- Due to the integration of multiple smart home features on a single chip, the overall hardware resource consumption and routing complexity were relatively high.

## Relevance to our topic
- It shows how our password lock system can act as an independent, high-speed subsystem within a larger architecture, validating the use of FSM for hardware security.

## Possible improvement
- We can isolate the door lock FSM to focus purely on state optimization, reducing resource consumption by testing more efficient state encoding techniques.
