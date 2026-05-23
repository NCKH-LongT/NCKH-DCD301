# Paper 15 Summary

## 15. AI-powered Sensor Fault Detection for Cost-effective Smart Greenhouses

## Citation

**Title:** AI-powered Sensor Fault Detection for Cost-effective Smart Greenhouses  
**Authors:** Seyed Mohammadhossein Shekarian, Mahdi Aminian, Amir Mohammad Fallah, Vaha Akbary Moghaddam  
**Year:** 2024  
**Source:** Computers and Electronics in Agriculture, Elsevier, Volume 224, Article 109198  
**DOI/Link:** https://doi.org/10.1016/j.compag.2024.109198  
**Link:** https://doi.org/10.1016/j.compag.2024.109198

## Problem

The paper addresses the problem of sensor faults in smart greenhouse systems.

Smart greenhouses depend on sensors to monitor environmental conditions such as temperature, humidity, CO₂ concentration, light intensity, and other climate-related parameters. If a sensor produces faulty or abnormal readings, the greenhouse system may make wrong decisions about irrigation, ventilation, lighting, or climate control.

This can reduce crop quality, waste resources, and affect the reliability of the whole greenhouse monitoring system.

## Method

The paper proposes an AI-powered sensor fault detection approach for cost-effective smart greenhouses.

The method uses sensor data collected from a greenhouse environment and applies AI or deep learning techniques to identify faulty sensor behavior. The system learns relationships among greenhouse variables and detects abnormal readings when sensor values are inconsistent with expected patterns.

The paper focuses on improving sensor reliability without requiring expensive industrial-grade sensor systems.

## Dataset

The paper uses greenhouse sensor data collected from a smart greenhouse system.

The data includes environmental parameters related to greenhouse monitoring, such as indoor and outdoor climate conditions. These sensor readings are used to train and evaluate the AI-based fault detection model.

## Evaluation

The paper evaluates the proposed fault detection system using AI model performance and sensor reliability criteria, including:

- Fault detection performance
- Ability to identify abnormal sensor readings
- Reliability improvement
- Cost-effectiveness of the greenhouse monitoring system
- Practical usefulness for smart greenhouse deployment

## Results

The results show that AI-powered fault detection can improve the reliability of smart greenhouse monitoring systems.

The proposed approach helps detect faulty or abnormal sensor readings, making the greenhouse system more trustworthy. This is especially useful for cost-effective smart greenhouse designs that may use low-cost sensors.

## Limitations

The paper focuses on AI-based sensor fault detection, not BCD arithmetic or FPGA-based decimal processing.

It does not discuss invalid BCD code detection, arithmetic overflow detection, or hardware-level decimal error checking. The approach also depends on the availability and quality of training data.

Another limitation is that the model may need adaptation when applied to different greenhouse environments, sensor types, or crop conditions.

## Relevance to Our Topic

This paper is relevant to the topic **BCD Arithmetic Error Detection for Reliable Sensor Data Processing in AIoT Smart Greenhouse Systems** because it supports the sensor reliability and data quality part of the project.

While our topic focuses on BCD arithmetic error detection for decimal sensor data, this paper focuses on AI-based fault detection for greenhouse sensors. Both approaches aim to improve the reliability of sensor data before it is used for decision-making.

## Possible Improvement

Our group can combine AI-powered sensor fault detection with BCD arithmetic error detection.

Possible improvements include:

- Checking invalid BCD codes before AI model processing
- Detecting overflow or arithmetic errors in decimal sensor calculations
- Combining BCD error flags with AI fault detection results
- Assigning reliability scores to sensor readings
- Using validated sensor data for Agentic RAG recommendations
- Building a complete reliable greenhouse sensor processing pipeline
