# Paper 07 Summary

## Citation
- **Title:** A Survey on Finite State Machine Encoding Techniques for Low Power Design
- **Year:** 2018
- **Source:** IEEE Xplore

## Problem
- In sequential circuits, frequent state transitions cause high switching activity, which leads to excessive dynamic power consumption in mobile or battery-operated digital devices.

## Method
- The paper surveys various state encoding strategies—such as Binary, Gray, and One-hot encoding—analyzing their impact on the combinational logic cloud surrounding an FSM.

## Dataset / Tools
- **Tools:** Power analysis simulation software, historical benchmark suites.

## Evaluation
- Circuits were evaluated based on dynamic power dissipation (mW) and maximum clock frequency restrictions.

## Results
- Gray encoding was proven highly effective for sequential tracking due to single-bit changes, while One-hot encoding optimized speed at the cost of register bits.

## Limitations
- The survey focuses purely on power metrics without considering the physical layout constraints of security hardware.

## Relevance to our topic
- It helps our group decide whether to use Gray code or One-hot code when encoding the states for our password input progress.

## Possible improvement
- We can simulate our door lock FSM using both Gray and One-hot encoding to observe which style yields the cleanest timing graphs.
