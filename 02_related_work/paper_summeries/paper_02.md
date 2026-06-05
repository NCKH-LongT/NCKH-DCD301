# Paper 02 Summary

## Citation

- **Paper Title:** Optimization of CMOS Decoders Using Three-Transistor Logic
- **Authors:** Dimitrios Balobas, Nikos Konofaos
- **Year:** 2025
- **Conference:** MDPI Electronics (Journal Article)
- **DOI/Link:** https://www.mdpi.com/2079-9292/14/5/914

## Problem

The paper addresses the significant power consumption (both active and standby) and propagation delays in conventional static CMOS decoder circuits. As digital systems and memory arrays scale up, traditional decoders require an extensive number of transistors, leading to hardware inefficiencies in modern nano-scale semiconductor technologies (such as 15 nm FinFET).

## Method

The authors introduce a new design approach called **3-Transistor Logic (3TL)** for optimizing CMOS decoders. This hybrid methodology strategically combines:
- Static CMOS
- Transmission-Gate Logic (TGL)
- Dual-Value Logic (DVL)

The design provides a complete transistor-level implementation methodology scalable for decoder sizes from $2 \times 4$ up to $8 \times 256$.

## Dataset

The study uses transistor-level netlists and architectural layouts simulated under modern **15 nm Predictive Technology Models (PTM) for FinFET devices**. Standard binary address patterns and switching sequences are applied to evaluate circuit behaviors.

## Evaluation

The proposed 3TL decoder circuits are evaluated using the following hardware performance metrics:
- **Active Power Consumption:** Power dissipated during switching transitions.
- **Standby Power Consumption:** Static leakage power when the circuit is idle.
- **Propagation Delay:** The time required for a signal to pass from the inputs to the outputs.
- **Transistor Count:** Total number of transistors utilized to assess silicon area efficiency.

## Results

The 3TL architecture achieved the best overall performance compared to conventional static CMOS and previous low-power designs. It dramatically reduced the transistor count, resulting in lower capacitance. Consequently, the circuits demonstrated a substantial reduction in both active and standby leakage power while simultaneously minimizing propagation delays across all evaluated decoder dimensions ($2 \times 4$ to $8 \times 256$).

## Limitations

Although the 3TL approach works exceptionally well at the isolated decoder level, the paper focuses primarily on flat address-decoding applications. It lacks automated hierarchical optimization or high-level EDA tool synthesis workflows when these optimized decoders are integrated with massive multi-stage OR-gate networks for irregular, non-continuous Boolean expressions.

## Relevance to our topic

This paper directly supports our **RQ2.3** regarding the advantages of implementing decoder-based logic over traditional discrete gate structures. It provides solid hardware-level evidence (transistor count, area, and power metrics) proving that an optimized decoder is highly efficient, which serves as a powerful baseline justification for our proposed framework.

## Possible improvement

Our project can extend this work by mapping the transistor-level hardware efficiency of the 3TL decoder into our high-level functional architecture. We can develop an EDA-aware translation script that automatically generates the customized 3TL decoder layout logic mapping based on our standardized JSON configuration outputs.