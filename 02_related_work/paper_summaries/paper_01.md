# Paper 01 Summary

## Citation
- **Title:** Digital (Electronic) Locker
- **Authors:** N. Sharma, A. Kumar, and S. Singh
- **Year:** 2020
- **Source:** 2020 First IEEE International Conference on Measurement, Instrumentation, Control and Automation (ICMICA)
- **Link:** https://ieeexplore.ieee.org/document/9242688/

## Problem
- Traditional mechanical locks are vulnerable to physical tampering and lack flexibility. Standard combinational logic circuits cannot be used for password authentication because they lack memory elements to track sequential, multi-step inputs over time.

## Method
- The paper implements a 4-digit digital password locker using a Finite State Machine (FSM) modeled in Verilog HDL. The system transitions through distinct states based on key inputs, manages user attempts, and triggers specific outputs for password correctness, time-out constraints, and alarm signals.

## Dataset / Tools
- **Software Tools:** Xilinx ISE Design Suite for hardware description and compilation, and ModelSim for behavioral waveform simulation.

## Evaluation
- The design is evaluated through behavioral simulation workflows to verify that state transitions occur correctly under both valid and invalid input sequences. Hardware complexity is assessed via gate-count and device utilization reports.

## Results
- The FSM successfully detects the correct 4-digit sequence, correctly triggers an unlock signal, counts incorrect attempts to trigger a security alarm after 3 failed tries, and manages a countdown timer for user input.

## Limitations
- The proposed architecture was only validated within a software simulation environment. It lacked deployment and physical testing on an actual FPGA hardware board, leaving real-world hardware glitches and timing delays unaddressed.

## Relevance to our topic
- This paper provides a direct foundational architecture for our Password Door Lock System. It proves that a sequential FSM structure is the ideal methodology for handling sequence-matching and timing constraints in digital security hardware.

## Possible improvement
- Our group can improve upon this design by implementing both Mealy and Moore machine variations for the lock, analyzing the exact differences in output behavior, and specifically studying how to mitigate timing glitches when inputs change between clock cycles.
