# Paper 10 Summary

## 10. IoT Data Quality Assessment Framework Using Adaptive Weighted Estimation Fusion

## Citation

**Title:** IoT Data Quality Assessment Framework Using Adaptive Weighted Estimation Fusion  
**Authors:** J. Byabazaire et al.  
**Year:** 2023  
**Source:** Sensors, MDPI  
**DOI/Link:** https://doi.org/10.3390/s23135993  
**Link:** https://www.mdpi.com/1424-8220/23/13/5993

## Problem

The paper addresses the problem of unreliable sensor data in IoT systems. IoT devices often collect data from many sensors, but the data may contain noise, missing values, sensor faults, or communication errors.

Poor data quality can reduce the accuracy of monitoring, prediction, and decision-making systems. This is especially important in AIoT applications, where decisions may be made automatically based on sensor readings.

## Method

The paper proposes an IoT data quality assessment framework using **adaptive weighted estimation fusion**.

The method combines multiple sensor-related indicators and assigns adaptive weights to estimate the reliability of IoT data. Instead of treating all sensor readings equally, the framework evaluates the trustworthiness of data sources and fuses the information to produce a better quality assessment.

## Dataset

The paper uses IoT sensor data for evaluating the proposed data quality framework.

The data is used to test whether adaptive weighted estimation fusion can improve data quality assessment and sensor reliability evaluation.

## Evaluation

The paper evaluates the proposed framework using data quality and sensor reliability assessment criteria, including:

- Data reliability
- Sensor validation performance
- Data fusion quality
- Ability to handle noisy or unreliable sensor readings
- Improvement over non-adaptive quality assessment methods

## Results

The results show that adaptive weighted estimation fusion can improve IoT data quality assessment.

The framework helps identify unreliable sensor data and improves the quality of fused information. This makes IoT systems more reliable for monitoring and decision-making.

## Limitations

The paper focuses on general IoT data quality assessment, not specifically on smart greenhouse systems.

It does not discuss BCD arithmetic, FPGA implementation, or digital arithmetic error detection. Therefore, the method needs adaptation before being applied to hardware-level decimal sensor data processing.

## Relevance to Our Topic

This paper is relevant to the topic **BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems** because it supports the sensor data quality part of the project.

In our system, BCD arithmetic error detection can check whether decimal sensor values are valid at the arithmetic/data representation level. This paper supports the broader data quality framework for evaluating sensor reliability before decision-making.

## Possible Improvement

Our group can combine adaptive IoT data quality assessment with BCD arithmetic error detection.

Possible improvements include:

- Using BCD validity checks before data fusion
- Adding overflow and invalid digit detection to sensor processing
- Assigning lower reliability scores to sensors with repeated BCD/data errors
- Combining hardware-level error flags with AIoT data quality scoring
- Using validated and scored sensor data as input for Agentic RAG recommendations
