# Paper 04 Summary

## Citation
- **Title:** Design of mealy finite-state machines with the transformation of object codes
- **Authors:** A. Barkalov, et al.
- **Year:** 2011
- **Source:** EUDML (European Digital Mathematics Library)
- **Link:** https://eudml.org/doc/207723

## Problem
- Mealy finite-state machines often suffer from highly complex combinational logic circuits when dealing with complex input conditions, which increases hardware cost and propagation delay.

## Method
- The authors introduce a mathematical and logical optimization method involving the transformation of state and object codes to minimize the logic blocks required for Mealy FSMs.

## Dataset / Tools
- **Tools:** Logic synthesis algorithms and theoretical hardware modeling tools.

## Evaluation
- The method was mathematically proven and tested against standard benchmark circuits to count the reduction in required logic gates.

## Results
- The proposed transformation successfully minimized the number of logic blocks in the Mealy implementation, accelerating the circuit's response time.

## Limitations
- The paper relies heavily on complex mathematical transformations, making it difficult to implement manually without specialized EDA (Electronic Design Automation) tools.

## Relevance to our topic
- It gives us a theoretical background on how to optimize our Mealy FSM architecture to ensure our password lock responds instantly to user inputs.

## Possible improvement
- We can apply simplified versions of these state minimization principles to our `1011` password sequence diagram.
