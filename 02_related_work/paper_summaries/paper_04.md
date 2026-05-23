# Paper 04 Summary

## 4. Decimal Addition on FPGA Based on a Mixed BCD/Excess-6 Representation

## Citation

**Title:** Decimal Addition on FPGA Based on a Mixed BCD/Excess-6 Representation  
**Authors:** Horácio Neto, Mário Véstias  
**Year:** 2017  
**Source:** Microprocessors and Microsystems, Elsevier, Volume 55, Pages 91–99  
**DOI/Link:** https://doi.org/10.1016/j.micpro.2017.08.008  
**Link:** https://www.sciencedirect.com/science/article/abs/pii/S0141933116303908

## Problem

The paper addresses the inefficiency of conventional BCD adders when implemented on FPGA.

Traditional BCD adders usually perform binary addition first and then apply decimal correction logic. This correction stage increases area and delay, especially when the design is implemented on FPGA LUT-based architectures.

The authors aim to improve decimal addition performance by using a number representation that maps more efficiently to FPGA hardware.

## Method

The paper proposes a decimal adder based on a **mixed BCD/Excess-6 representation**.

Instead of performing every operation directly in standard BCD format, the adder uses a mixed representation that makes intermediate decimal addition more efficient. Conversion back to normal BCD is performed only when needed.

The design is optimized for FPGA architectures using **6-input Look-Up Tables (LUTs)**.

The proposed decimal adder is described using **VHDL** and implemented on a **Xilinx Virtex-7 FPGA** using **Xilinx ISE 14.6**.

## Dataset

This paper does not use a dataset because it is a hardware arithmetic design paper.

Instead, the authors use arithmetic test cases and synthesis experiments to verify correctness and measure FPGA implementation performance.

The evaluation is based on circuit-level outputs, FPGA resource usage, and timing results.

## Evaluation

The paper evaluates the proposed design using FPGA hardware metrics, including:

- Area usage
- Delay
- LUT utilization
- Comparison with previous decimal adder architectures
- Efficiency of single-digit and multi-digit decimal addition

The main purpose of the evaluation is to show that the mixed BCD/Excess-6 representation can reduce hardware cost and improve speed.

## Results

The results show that the proposed mixed BCD/Excess-6 decimal adder improves both **area** and **delay** compared with previous decimal adder designs.

The paper reports that a single-digit decimal adder can be implemented efficiently using FPGA LUT resources. The design is also extended to support **multioperand decimal addition** and **mixed binary/decimal addition**.

This demonstrates that changing the internal decimal representation can improve FPGA-based decimal arithmetic performance.

## Limitations

The proposed architecture is more complex than a conventional BCD adder.

The mixed BCD/Excess-6 representation may be difficult for beginners to understand and implement.

Another limitation is that conversion back to standard BCD is still required at the final stage. The paper also focuses on arithmetic circuit optimization rather than application-level integration with IoT or smart greenhouse systems.

## Relevance to Our Topic

This paper is highly relevant to the topic **BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems** because it focuses on optimizing decimal addition on FPGA.

It shows that reliable and efficient decimal arithmetic can be improved not only by changing adder structure, but also by changing the internal number representation.

For our project, this paper can support the hardware arithmetic part, especially if the group wants to compare conventional BCD arithmetic with more optimized FPGA-based decimal arithmetic.

## Possible Improvement

Our group can improve or extend this work by adding **error detection logic** to the mixed BCD/Excess-6 decimal arithmetic system.

Possible improvements include:

- Detecting invalid BCD input codes
- Detecting invalid Excess-6 conversion results
- Checking overflow during decimal sensor data processing
- Adding reliability flags for abnormal arithmetic outputs
- Integrating the arithmetic module into an AIoT smart greenhouse data validation pipeline

This would connect advanced FPGA decimal arithmetic with reliable sensor data processing.
