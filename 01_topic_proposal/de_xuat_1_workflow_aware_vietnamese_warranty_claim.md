Research Topic Proposal
Reliable Sensor Data Processing in AIoT Smart Greenhouse Using BCD Error Detection and Agentic RAG
Short title: AIoT Smart Greenhouse: BCD Error Detection + Agentic RAG

1. Idea Summary
This topic proposes an AIoT smart greenhouse monitoring system that combines BCD arithmetic error detection with an Agentic Retrieval-Augmented Generation (RAG) pipeline to support reliable and explainable agricultural decision-making.
The main idea is to build a data quality gate before sensor data is used by the AI model. Sensor readings such as temperature, humidity, soil moisture, light intensity, and water flow are validated using BCD logic to detect invalid codes or arithmetic overflow.
After BCD validation, the system calculates a Data Quality Score (DQ_score) to estimate the reliability of sensor data. This score determines whether the system should provide a full recommendation, lower the confidence level, require human confirmation, or reject the recommendation when data quality is too poor.
Finally, the validated data is processed by the Agentic RAG pipeline. This component retrieves relevant agricultural knowledge, performs multi-step reasoning, verifies its output, and generates recommendations with explanations and confidence levels.
2. Why This Topic Can Be Developed into a Conference Paper
Existing smart greenhouse studies usually focus on sensor data collection, automation, or AI-based recommendation. However, one important issue is still not fully addressed: the reliability of sensor data before it enters the AI reasoning process.
If sensor data is missing, faulty, or contradictory, an AI model may generate inaccurate recommendations. This is especially risky in smart agriculture because actions such as turning on fans, activating irrigation, or sending alerts directly affect the crop-growing environment.
This topic addresses that gap by combining three core components:
•	BCD Error Detection for low-level sensor data validation.
•	Data Quality Score for evaluating sensor reliability.
•	Agentic RAG for knowledge retrieval and explainable recommendation generation.
Gap Statement
Existing smart greenhouse systems mainly focus on IoT data collection, automation, or AI-based recommendation. However, limited attention has been paid to validating sensor data quality before AI reasoning. This paper proposes a unified AIoT framework that integrates BCD arithmetic error detection, data quality scoring, and Agentic RAG to improve the reliability and explainability of smart greenhouse decision support.
3. Research Objectives
Code	Objective
O1	Integrate BCD arithmetic error detection to validate sensor data in an AIoT smart greenhouse system.
O2	Develop a Data Quality Score formula to evaluate reliability based on BCD validity, data completeness, and sensor consistency.
O3	Design an Agentic RAG pipeline that can retrieve agricultural knowledge, perform multi-step reasoning, and generate explainable recommendations.
O4	Evaluate the proposed framework through simulated sensor fault scenarios and compare it with baseline methods.

4. Research Questions
RQ1: How can real-time IoT sensor data be integrated with agricultural knowledge bases to support decision-making in smart greenhouses?
RQ2: How can BCD error detection be used as a sensor data quality validation mechanism before AI reasoning is performed?
RQ3: Can Agentic RAG improve recommendation accuracy and explainability compared with rule-based systems, LLM-only reasoning, and Naive RAG?
RQ4: How does the system respond to faulty data conditions such as missing data, invalid BCD codes, or conflicting sensor readings?
5. Problem Scope
5.1 Input and Environment
The system operates in a simulated smart greenhouse environment. The input data includes five types of sensors:
Sensor Type	Purpose
Temperature sensor	Measures greenhouse temperature.
Humidity sensor	Measures air humidity.
Soil moisture sensor	Measures soil moisture level.
Light intensity sensor	Measures light intensity inside the greenhouse.
Water flow sensor	Measures water flow in the irrigation system.

This study does not focus on real hardware manufacturing or commercial deployment. Instead, it focuses on framework design, sensor data processing, and simulation-based evaluation.
5.2 Output
The system generates recommended actions for greenhouse actuators:
Action	Meaning
turn_on_fan	Turn on the fan.
turn_off_fan	Turn off the fan.
turn_on_irrigation	Activate the irrigation system.
turn_off_irrigation	Deactivate the irrigation system.
turn_on_grow_light	Turn on the grow light.
send_alert	Send an alert to the greenhouse manager.

6. System Architecture and Data Preprocessing
6.1 Four-Layer System Architecture
Layer	Layer Name	Input	Output
1	Sensor + BCD Processing	Raw sensor data	BCD values and validity flags
2	Data Quality Evaluation	BCD flags and sensor readings	DQ_score and confidence tier
3	Agentic RAG Pipeline	DQ_score and contextual query	Retrieved evidence, relevant knowledge, and reasoning chain
4	Recommendation Engine	Evidence and sensor context	Recommendation, explanation, and confidence level

6.2 BCD Error Detection Logic
The system uses a Boolean expression to detect errors in BCD results:
Err = Cy + S3 · S2 + S3 · S1
Symbol	Meaning
Cy	Carry-out
S3, S2, S1	Bits in the BCD result
Err	BCD error flag

When Err = 1, the system identifies that the data may contain an invalid BCD code or an arithmetic overflow. In this case, a correction mechanism is triggered by adding 0110 to convert the result into a valid BCD form.
6.3 Data Quality Score
The system uses a Data Quality Score to evaluate the reliability of sensor data.
DQ_score = w1 · S_bcd + w2 · S_complete + w3 · S_consistent
Component	Meaning	Weight
S_bcd	Validity level of BCD data	0.40
S_complete	Completeness level of sensor data	0.35
S_consistent	Consistency level among sensor readings	0.25

DQ_score	Confidence Level	System Response
0.85 - 1.00	High	Generate a full recommendation.
0.65 - 0.84	Medium	Generate a recommendation with uncertainty warning.
0.40 - 0.64	Low	Switch to fallback mode and require human confirmation.
< 0.40	Very low	Reject the recommendation and send a maintenance alert.

7. Fault Scenarios and Experimental Dataset
The study uses four simulated scenarios to evaluate the proposed system:
Scenario	Condition	Simulation Method
S1 - Normal	All sensors operate normally.	Complete data with valid BCD values.
S2 - Missing Data	One or more sensors have missing readings.	Intentionally remove 20-60% of sensor readings.
S3 - Sensor Fault	A sensor returns invalid BCD codes.	Inject invalid codes such as 1111 into the data stream.
S4 - Conflicting Readings	Sensor values are contradictory.	Create abnormal differences in temperature or humidity readings.

8. Experimental Models
The proposed framework will be compared with three baseline methods:
Method	Description
Rule-Based System	Uses fixed IF-THEN rules, such as IF temperature > 35°C THEN turn_on_fan.
LLM-Only	Sends sensor data directly to an LLM to generate recommendations.
Naive RAG	Retrieves relevant documents and generates an answer without agents or sensor quality validation.
Agentic RAG + BCD	The proposed framework with BCD validation, DQ_score, multi-step retrieval, and self-verification.

9. Evaluation Metrics
Metric	Meaning
Recommendation Accuracy	The percentage of recommendations that match the expected expert-defined action.
Explainability Score	The clarity of explanations, evidence, and reasoning steps.
Hallucination Rate	The rate of incorrect or unsupported agricultural information generated by the system.
Safe-Failure Rate	The ability of the system to lower confidence or reject recommendations when sensor data is faulty.
Latency	The processing time from sensor data input to recommendation output.
DQ_score	The calculated quality score of sensor data.

10. Proposed Paper Structure
1.	Introduction: Introduce the AIoT smart greenhouse context, the problem of faulty sensor data, and the need for explainable decision-making.
2.	Related Work: Review studies on IoT agriculture, BCD error detection, RAG, and Agentic RAG.
3.	Research Scope and Problem Definition: Define the problem scope, sensor types, simulation environment, and system goals.
4.	System Design: Present the four-layer architecture, data flow, and role of each component.
5.	BCD Error Detection and Data Quality Evaluation: Describe the BCD error detection formula and the DQ_score calculation.
6.	Agentic RAG-based Recommendation Pipeline: Explain how the system retrieves knowledge, performs multi-step reasoning, and generates recommendations.
7.	Planned Comparative Evaluation: Describe the baselines, simulated dataset, and evaluation metrics.
8.	Robustness Evaluation under Fault Scenarios: Analyze how the system handles missing data, sensor faults, and conflicting readings.
9.	Conclusion and Future Work: Summarize the expected contributions and future development directions.
11. Contribution Statement
The expected contributions of this paper are threefold. First, this study proposes the use of BCD arithmetic error detection as a lightweight data validation mechanism for AIoT greenhouse sensor data. Second, it introduces a composite Data Quality Score to estimate the reliability of sensor readings before AI-based reasoning is performed. Third, it presents an Agentic RAG-based decision-support framework that generates agricultural recommendations with explanations, confidence levels, and safe-failure behavior under faulty sensor conditions.
12. Sample Abstract
Abstract. This paper proposes an AIoT smart greenhouse monitoring framework that combines BCD arithmetic error detection with an Agentic Retrieval-Augmented Generation pipeline to support reliable and explainable agricultural decision-making. The system focuses on greenhouse sensor data, including temperature, humidity, soil moisture, light intensity, and water flow. Before the data is used by the AI reasoning module, it is validated through BCD logic to detect invalid codes and arithmetic overflow. A composite Data Quality Score is then calculated based on BCD validity, data completeness, and sensor consistency to estimate the reliability of the input data.
The proposed framework uses Agentic RAG to retrieve relevant agricultural knowledge, perform multi-step reasoning, and generate recommendations with explanations and confidence levels. The planned evaluation will compare the proposed approach with rule-based control, LLM-only reasoning, and Naive RAG under four simulated sensor conditions: normal operation, missing data, sensor fault, and conflicting readings. Evaluation metrics include recommendation accuracy, hallucination rate, safe-failure rate, latency, and explainability score. The expected contribution of this study is a unified framework that links low-level sensor data validation with high-level AI-based decision support for smart greenhouse systems.
