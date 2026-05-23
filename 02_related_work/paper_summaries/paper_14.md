# Paper 14 Summary

## 14. Impact of Radix-10 Redundant Digit Set [-6, 9] on Basic Decimal Arithmetic Operations

## Citation

**Title:** Impact of Radix-10 Redundant Digit Set [-6, 9] on Basic Decimal Arithmetic Operations  
**Authors:** Ghassem Jaberipur, Farzad Ghazanfari  
**Year:** 2022  
**Source:** IEEE Transactions on Very Large Scale Integration (VLSI) Systems  
**DOI/Link:** https://doi.org/10.1109/TVLSI.2021.3120065  
**Link:** https://doi.org/10.1109/TVLSI.2021.3120065

## Problem

The paper addresses the efficiency problem in decimal arithmetic operations. Conventional decimal arithmetic, including BCD-based arithmetic, often suffers from carry propagation delay. This delay becomes more significant when decimal operations are performed on multiple digits.

The authors investigate whether an alternative radix-10 redundant digit set can improve the performance of basic decimal arithmetic operations.

## Method

The paper studies the impact of the radix-10 redundant digit set **[-6, 9]** on decimal arithmetic.

Instead of using only standard decimal digits from 0 to 9, the method uses a redundant digit representation. This representation provides more flexibility during arithmetic computation and can reduce the effect of long carry propagation chains.

The paper analyzes how this redundant digit set affects basic decimal operations such as addition and related arithmetic operations.

## Dataset

This paper does not use a dataset because it is a decimal arithmetic and VLSI-oriented hardware study.

Instead, the paper uses arithmetic analysis, circuit-level reasoning, and hardware-oriented evaluation to study the effect of the redundant digit set.

## Evaluation

The paper evaluates the decimal arithmetic approach using hardware and arithmetic performance considerations, including:

- Carry propagation behavior
- Arithmetic operation efficiency
- Hardware complexity
- Decimal representation effectiveness
- Suitability for VLSI decimal arithmetic design

## Results

The paper shows that alternative decimal digit representations can improve the efficiency of decimal arithmetic operations.

The radix-10 redundant digit set **[-6, 9]** provides a useful way to reduce carry-related limitations in decimal arithmetic. This supports the idea that decimal arithmetic can be optimized not only by changing the adder circuit, but also by changing the internal number representation.

## Limitations

The paper is more theoretical and VLSI-oriented than application-oriented.

It does not focus specifically on FPGA implementation, IoT sensor data, smart greenhouse systems, or Agentic RAG decision support. The method may also be more complex than standard BCD arithmetic, making it harder to implement in a simple educational project.

## Relevance to Our Topic

This paper is relevant to the topic **BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems** because it provides an advanced decimal arithmetic reference.

Although the paper does not directly discuss BCD error detection, it supports the hardware arithmetic side of the project by showing that decimal arithmetic performance can be improved through alternative radix-10 representations.

This can help our group compare standard BCD arithmetic with more advanced decimal arithmetic approaches.

## Possible Improvement

Our group can extend the idea of redundant decimal representation by adding reliability checking and error detection mechanisms.

Possible improvements include:

- Detecting invalid decimal digit representations
- Adding overflow detection for decimal arithmetic
- Comparing standard BCD with redundant radix-10 representation
- Evaluating delay, area, and reliability on FPGA
- Applying decimal error detection to greenhouse sensor values
- Producing validity flags before AIoT decision-making
