# Paper 02 Summary

## 2. Hardware Modeling of Binary Coded Decimal Adder in Field Programmable Gate Array

## Citation

**Title:** Hardware Modeling of Binary Coded Decimal Adder in Field Programmable Gate Array  
**Authors:** Muhammad Ibn Ibrahimy, Rezwanul Ahsan, Iksannurazmi Bambang Soeroso  
**Year:** 2013  
**Source:** American Journal of Applied Sciences, 10(5), 466–477  
**DOI/Link:** https://doi.org/10.3844/ajassp.2013.466.477  
**Alternative Link:** https://www.researchgate.net/publication/260449465_Hardware_Modeling_of_Binary_Coded_Decimal_Adder_in_FPGA

## Problem

The paper addresses the lack of practical FPGA-based implementations of Binary Coded Decimal (BCD) adders. Although BCD arithmetic is useful for decimal-based applications, many previous works focused more on theoretical arithmetic design than actual FPGA realization.

The paper also addresses the delay problem caused by carry propagation in conventional adder structures.

## Method

The paper designs and compares two BCD adder architectures: **Ripple Carry (RC) adder** and **Carry Look-Ahead (CLA) adder**.

The RC adder is simpler but slower because each carry depends on the previous stage. The CLA adder improves speed by generating carry signals in advance.

The design is modeled using **Verilog HDL** and implemented using **Altera Quartus II EDA tools**. The design flow includes functional simulation, timing simulation, synthesis, and hardware implementation on an FPGA board.

## Dataset

This paper does not use a dataset because it is a hardware modeling and FPGA implementation study.

Instead, the authors use testbench input combinations to verify the correctness of the BCD adder. Example binary/decimal test inputs are applied to check whether the output is correctly represented in BCD and displayed on a 7-segment display.

## Evaluation

The paper evaluates the BCD adder using hardware-oriented metrics, including:

- Data arrival time
- Area utilization
- Cell usage
- Functional correctness
- Timing analysis
- Physical FPGA implementation result

The main comparison is between the RC-based adder and the CLA-based adder.

## Results

The results show that the **CLA-based BCD adder is faster** than the RC-based BCD adder.

In the synthesis results, the CLA architecture has lower data arrival time than the RC architecture. However, the CLA design uses more area and more cells, which may lead to higher power consumption.

The final design was implemented on an **Altera DE2 board** containing an **Altera Cyclone II 2C35 FPGA device**. The hardware test confirmed that the BCD adder produced correct decimal outputs on the 7-segment display.

## Limitations

The paper mainly compares only two architectures: Ripple Carry and Carry Look-Ahead. It does not explore more advanced BCD adder designs such as parallel-prefix adders, carry-select adders, or mixed BCD/Excess-6 adders.

Another limitation is that the FPGA platform is relatively old. The paper also focuses more on timing and area than on power analysis, scalability, or integration into a larger sensor-processing system.

## Relevance to Our Topic

This paper is relevant to the topic **BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems** because it provides a practical FPGA-based BCD adder implementation.

The design flow using Verilog, simulation, synthesis, and FPGA deployment can help our group build the arithmetic-processing module for decimal sensor data.

The comparison between RC and CLA is also useful because it shows that faster carry-generation logic can improve decimal arithmetic performance.

## Possible Improvement

Our group can improve this work by adding **invalid BCD code detection**, **overflow detection**, and **sensor-data validation logic** to the BCD adder.

Instead of only producing decimal addition output, the improved design can also detect whether the input or output contains invalid decimal codes.

Another improvement is to implement the design on a modern FPGA board and compare delay, area, LUT usage, and power consumption. The improved arithmetic module can then be integrated into an AIoT greenhouse system for reliable sensor data processing.
