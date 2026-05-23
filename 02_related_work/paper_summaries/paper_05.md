# Paper 05 Summary

## 5. A Fast FPGA-Based BCD Adder

## Citation

**Title:** A Fast FPGA-Based BCD Adder  
**Authors:** Mubin Ul Haque, Zarrin Tasnim Sworna, Hafiz Md. Hasan Babu, Ashis Kumer Biswas  
**Year:** 2018  
**Source:** Circuits, Systems, and Signal Processing, Springer, Volume 37, Pages 4384–4408  
**DOI/Link:** https://doi.org/10.1007/s00034-018-0770-3  
**Link:** https://link.springer.com/article/10.1007/s00034-018-0770-3

## Problem

The paper addresses the delay and hardware cost problems in FPGA-based Binary Coded Decimal (BCD) adders. Conventional BCD adders usually perform binary addition first and then apply decimal correction logic when the result is greater than 9. This correction step increases the critical path delay and hardware complexity.

The authors aim to design a faster and more resource-efficient BCD adder for FPGA implementation.

## Method

The paper proposes a fast FPGA-based BCD adder using a LUT-based design approach. Since Look-Up Tables (LUTs) are the main logic resources in FPGA devices, the proposed circuit is optimized to reduce LUT usage and logic depth.

The design uses a tree-structured parallel BCD addition approach to reduce carry propagation delay. The proposed adder is coded in VHDL and implemented on a Xilinx Virtex-6 XC6VLX75T FPGA using Xilinx ISE 13.1.

## Dataset

This paper does not use a dataset because it is a hardware design and FPGA implementation study.

Instead, the authors use arithmetic test inputs and FPGA synthesis experiments to verify the correctness and performance of the proposed BCD adder.

## Evaluation

The paper evaluates the proposed BCD adder using hardware performance metrics, including:

- Area
- Delay
- Area-delay product
- Power consumption
- FPGA resource usage
- Comparison with previous BCD adder designs

The main purpose of the evaluation is to prove that the proposed LUT-based BCD adder is faster and more efficient than earlier FPGA-based BCD adder architectures.

## Results

The experimental results show that the proposed BCD adder improves FPGA-based decimal addition performance.

Compared with previous approaches, the proposed design reduces area, delay, area-delay product, and power consumption. This shows that a carefully designed LUT-based architecture can improve both speed and hardware efficiency in FPGA-based decimal arithmetic.

## Limitations

The paper mainly focuses on BCD addition and does not discuss a complete decimal arithmetic system.

The proposed design is optimized for FPGA architecture, so its performance may vary on different FPGA families. The paper also does not focus on IoT sensor data processing, smart greenhouse systems, or BCD error detection.

## Relevance to Our Topic

This paper is highly relevant to the topic **BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems** because it provides a strong FPGA-based BCD adder architecture.

In our project, decimal sensor values such as temperature, humidity, soil moisture, light intensity, and water flow may need accurate decimal arithmetic processing. A fast FPGA-based BCD adder can support reliable and efficient decimal computation before the data is checked or used by the AIoT recommendation system.

## Possible Improvement

Our group can extend this work by adding BCD arithmetic error detection to the fast FPGA-based BCD adder.

Possible improvements include:

- Invalid BCD code detection
- Overflow detection
- Sensor value range checking
- Error flag generation
- Integration with AIoT smart greenhouse sensor pipelines

This would make the BCD adder not only fast, but also more reliable for real-time sensor data processing.
