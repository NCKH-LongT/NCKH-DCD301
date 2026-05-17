# Topic Proposal

## 1. Group Information

- Class: SE1930 
- Group: Group 7     
- Leader: Ngo Dinh Gia Bao
- Members: Doan Quoc Thang , Nguyen Minh Triet

## 2. Proposed Title

English title:
“A Data Quality-Aware Agentic RAG Framework for Real-Time Smart Greenhouse Decision Support Using Multiplexer-Based Combinational Circuits”

Vietnamese title:
"Nghiên cứu khoa học về đề tài Nhà Kính thông minh ứng dụng Agentic RAG phân tích dữ liệu để đưa ra giải pháp hỗ trợ theo thời gian thực với Mạch Tổ Hợp Multiplexer"

## 3. Application Domain

Agriculture (Smart Greenhouse Monitoring and Decision Support)

## 4. Problem Statement

Current greenhouse management systems often struggle to combine real-time sensor data, hardware resource constraints, and explainable decision support. The problem is how to create a practical Smart Greenhouse system that integrates multiple IoT sensors, a multiplexer-based combinational circuit, and an Agentic RAG pipeline to generate reliable and explainable environmental control recommendations.

## 5. Motivation

This problem is important because modern agriculture needs smarter automation to improve resource efficiency, reduce manual intervention, and support sustainable crop production. A solution that combines IoT, digital circuit design, and explainable AI can help greenhouse operators make better decisions while maintaining low hardware cost and strong data reliability.

## 6. Target Users

Primary users:
- Greenhouse operators and managers
- Agricultural researchers and technicians
- Smart farming system developers

## 7. Proposed AI Model / Method

The team plans to use the following methods:
- Agentic RAG framework
- Retrieval-Augmented Generation (RAG)
- Large Language Model (LLM) for explanation and recommendation
- Data quality assessment module
- Rule-based baseline comparison
- Vector embeddings for document retrieval

## 8. System Features

The main system functions:
1. Real-time sensor acquisition from temperature, humidity, soil moisture, and light sensors
2. Multiplexer-based sensor routing to reduce ESP32 GPIO usage
3. Data quality checking for missing values, outliers, stuck sensors, and conflicts
4. Agentic RAG recommendation generation with explainable output and actionable controls

## 9. Expected Contribution

Expected contributions:
1. Integrate IoT sensor monitoring, multiplexer combinational circuit, and Agentic RAG decision support in a cohesive Smart Greenhouse system.
2. Evaluate how sensor data quality affects the reliability and explainability of AI-based recommendations.
3. Compare the proposed Agentic RAG framework with rule-based, LLM-only, and RAG-only baselines.

## 10. Evaluation Plan

The team will evaluate the system as follows:
- Dataset: simulated and real sensor data streams, agricultural knowledge documents, and scenario-based test cases
- Baseline: rule-based control, LLM-only recommendation, RAG-only recommendation
- Metrics: recommendation accuracy, confidence score, latency, explanation quality, fault tolerance
- Expert evaluation: feedback from agricultural or embedded systems experts on recommendation relevance and system feasibility
- User survey: greenhouse operator impressions on usability and trust in system recommendations

## 11. Related Papers

| No | Title | Year | Source | Link / DOI |
|---|---|---|---|---|
| 1 | A Survey on Smart Agriculture Based on Internet of Things | 2020 | Amera Istiqlal Badran and Manar Younis Kashmoola | https://www.researchgate.net/publication/345099559_Smart_Agriculture_Using_Internet_of_Things_A_Survey |
| 2 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | 2020 | NeurIPS | https://doi.org/10.5555/3577580.3577899 |
| 3 | Data Quality Assessment for IoT Sensor Networks | 2019 | IEEE Access | https://doi.org/10.1109/ACCESS.2019.2906758 |
| 4 | Explainable AI for Smart Farming: Challenges and Opportunities | 2022 | Computers and Electronics in Agriculture | https://doi.org/10.1016/j.compag.2022.106817 |
| 5 | Multiplexer-Based Sensor Interface for Embedded Systems | 2018 | IEEE Transactions on Industrial Electronics | https://doi.org/10.1109/TIE.2018.2879467 |
