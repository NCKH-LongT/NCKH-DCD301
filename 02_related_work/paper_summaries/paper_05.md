# Paper 05 Summary

## Citation
- **Title:** Synthesis of a Finite State Machine With Elementary Chains of States
- **Authors:** O. Barkalov, et al.
- **Year:** 2022
- **Source:** 2022 IEEE 9th International Conference on Problems of Infocommunications, Science and Technology (PIC S&T)
- **Link:** https://ieeexplore.ieee.org/document/10238579/

## Problem
- Choosing strictly between a Mealy or Moore machine introduces a trade-off: Mealy reacts faster but is prone to glitches, while Moore is stable but requires more states and introduces a one-clock delay.

## Method
- The paper proposes a hybrid structure to synthesize a Combined FSM that can generate output functions of both Mealy and Moore types depending on the current chain of states.

## Dataset / Tools
- **Tools:** HDL synthesis software, logic minimization matrices.

## Evaluation
- Evaluated by comparing the hybrid FSM against pure Mealy and pure Moore implementations regarding logic cell reduction and propagation delay.

## Results
- The combined approach achieved a significant reduction in total logic cells while maintaining the safe timing behaviors typical of Moore machines.

## Limitations
- The design increases the complexity of the state transition verification process, making debugging more challenging.

## Relevance to our topic
- This directly aligns with our core research objective of evaluating Mealy and Moore machines for the password lock system.

## Possible improvement
- We can implement separate Mealy and Moore lock designs first, then use this paper's insights to see if a hybrid model prevents glitches in our system.
