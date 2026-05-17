# Paper 08 Summary

## Citation
- **Title:** State Minimization of Finite State Machines
- **Year:** 2015
- **Source:** Springer / IEEE

## Problem
- Unoptimized FSM designs contain redundant states, which leads to larger flip-flop chains and unnecessary logic gates, making the overall hardware less efficient.

## Method
- This paper explores classic and modern state reduction algorithms (like the Implication Table method) to identify and merge equivalent states in complex sequential circuits.

## Dataset / Tools
- **Tools:** Discrete mathematics models, CAD state minimization algorithms.

## Evaluation
- Algorithms were evaluated by comparing the initial state count against the minimized state count across multiple design layouts.

## Results
- Demonstrated that reducing even a single state can drastically decrease the complexity of the next-state decoder logic.

## Limitations
- Manual state minimization using implication tables becomes highly error-prone as the number of inputs and states grows.

## Relevance to our topic
- It guides us to construct the absolute minimum number of states necessary to detect the `1011` code without wasting hardware resources.

## Possible improvement
- We can document our state reduction process step-by-step using an implication table to prove our lock design is mathematically minimized.
