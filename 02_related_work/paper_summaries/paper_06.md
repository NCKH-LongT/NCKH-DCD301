# Paper 06 Summary

## 6. Reduced Delay BCD Adder

## Citation

**Title:** Reduced Delay BCD Adder  
**Authors:** Alp Arslan Bayrakci, Ahmet Akkas  
**Year:** 2007  
**Source:** IEEE International Conference on Application-specific Systems, Architectures and Processors (ASAP), Pages 266–271  
**DOI/Link:** https://doi.org/10.1109/ASAP.2007.4429991  
**Link:** https://www.computer.org/csdl/proceedings-article/asap/2007/04429991/12OmNzd7bzY

## Problem

The paper addresses the high delay problem in conventional BCD adders. Decimal arithmetic is important in financial and commercial applications, but software-based decimal arithmetic is much slower than hardware-based arithmetic.

In a conventional BCD adder, binary addition is performed first, and then correction logic is applied if the result is greater than 9. This creates a long critical path and increases computation delay, especially in multi-digit decimal addition.

## Method

The paper proposes a reduced-delay BCD adder that improves speed by increasing parallelism.

The proposed architecture reduces carry propagation delay by computing important carry and correction signals more efficiently. On the critical path, the design includes two 4-bit binary adders, a carry network, one AND gate, and one OR gate.

The proposed adder and five previous decimal adders are implemented in VHDL and synthesized using a 0.18 micron TSMC ASIC library for comparison.

## Dataset

This paper does not use a dataset because it is a digital circuit design and hardware synthesis study.

Instead, the authors use BCD arithmetic input cases and synthesis experiments to verify the behavior and performance of the proposed architecture.

## Evaluation

The paper evaluates the proposed design using hardware performance metrics, including:

- Delay
- Area
- Critical path analysis
- Comparison with previous decimal adder architectures
- 64-bit decimal addition performance

The main evaluation objective is to show that the proposed BCD adder reduces delay compared with existing decimal adders.

## Results

The synthesis results show that the proposed reduced-delay BCD adder has the shortest delay among the decimal adders compared in the paper.

For 64-bit decimal addition, the proposed BCD adder achieves a delay of **1.40 ns**. It also requires less area than several previously proposed decimal adders.

This result shows that increasing parallelism in the BCD adder architecture can significantly improve decimal addition speed.

## Limitations

The paper mainly focuses on delay reduction and area comparison.

It does not deeply analyze power consumption, FPGA LUT usage, or integration into modern FPGA-based systems. The design is also evaluated using an ASIC library rather than a complete FPGA implementation.

Another limitation is that the paper does not discuss sensor data processing, smart greenhouse systems, or arithmetic error detection.

## Relevance to Our Topic

This paper is directly relevant to the topic **BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems** because it provides an optimized BCD adder architecture for faster decimal arithmetic.

In our project, decimal sensor values need to be processed reliably. A reduced-delay BCD adder can improve the speed of arithmetic operations before applying error detection, data quality checking, or AI-based recommendation generation.

## Possible Improvement

Our group can extend this work by adding reliability and error detection features to the reduced-delay BCD adder.

Possible improvements include:

- Detecting invalid BCD input codes
- Detecting overflow during decimal addition
- Adding output validity flags
- Testing the design on a modern FPGA platform
- Combining arithmetic error detection with greenhouse sensor data validation

This improvement would connect the reduced-delay BCD adder with reliable AIoT sensor data processing.
