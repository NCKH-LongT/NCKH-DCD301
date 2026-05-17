# Paper 06 Summary

## Citation
- **Title:** Finite State Machine Design and VHDL Coding Techniques
- **Authors:** V. A. Pedroni
- **Year:** 2010
- **Source:** 10th International Conference on DEVELOPMENT AND APPLICATION SYSTEMS
- **Link:** https://kolegite.com/EE_library/papers/HDL/Finite_state_machines_in_VHDL.pdf

## Problem
- Poor HDL coding habits often lead to critical hardware bugs, such as unintentional latches, race conditions, and non-synthesizable state machines.

## Method
- This methodology paper outlines comprehensive design rules and template-driven coding techniques for implementing robust Mealy and Moore FSMs in VHDL.

## Dataset / Tools
- **Tools:** VHDL standards, IEEE library specifications, and standard EDA synthesis tools.

## Evaluation
- The techniques were tested across various hardware synthesis tools to guarantee clean, hazard-free physical circuits.

## Results
- Provided explicit templates for single-process and multi-process FSM coding styles, ensuring optimal state encoding (One-hot vs. Gray).

## Limitations
- It is a general tutorial paper, so it does not apply these coding techniques to a specific end-user application like a lock.

## Relevance to our topic
- This will serve as our group's primary coding handbook when we begin writing hardware code for our password lock.

## Possible improvement
- We can apply these exact standard VHDL templates to construct our sequence-detection states for the password door lock.
