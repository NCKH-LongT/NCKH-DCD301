Smart Greenhouse Monitoring with BCD Arithmetic Error Detection & Agentic RAG
Vietnamese Title

Hệ Thống Nhà Kính Thông Minh AIoT: Ứng Dụng Phát Hiện Lỗi Số Học BCD và Agentic RAG

English Title

A Data Quality-Aware Agentic RAG Framework Using BCD Error Detection for AIoT Smart Agriculture

1. Project Overview

This project proposes an intelligent greenhouse monitoring framework that integrates:

Real-time AIoT sensor processing
Hardware-level BCD arithmetic validation
Data quality assessment
Agentic Retrieval-Augmented Generation (Agentic RAG)
Explainable and safe AI decision-making

The system continuously monitors greenhouse environmental conditions such as temperature, humidity, soil moisture, and light intensity. Sensor values are encoded using Binary Coded Decimal (BCD) representation and validated through lightweight arithmetic error-detection logic before entering the AI reasoning pipeline.

The proposed framework introduces a hardware-aware data validation layer that prevents corrupted sensor data from propagating into the AI decision system.

2. Research Motivation

Most existing smart agriculture systems focus on:

IoT monitoring
Deep learning prediction
Rule-based automation
RAG-based agricultural assistance

However, current systems rarely consider:

Hardware-level arithmetic corruption
Invalid BCD sensor codes
Sensor conflict reliability
AI hallucination caused by low-quality sensor data
Safe-failure mechanisms for unreliable environments

This project bridges the gap between:

Digital hardware validation
AIoT data quality assessment
Agentic RAG reasoning systems
3. Research Gap

Existing studies have explored smart agriculture, IoT sensor networks, and data quality assessment separately. However, limited attention has been given to integrating real-time hardware-level validation such as BCD arithmetic error detection with Agentic RAG frameworks for explainable agricultural decision support.

Furthermore, the influence of invalid BCD codes, arithmetic overflow, and sensor corruption on AI recommendation reliability and safe-failure behavior remains underexplored.

4. Research Objectives
ID	Objective
O1	Develop a real-time IoT sensor pipeline using BCD encoding
O2	Design a Data Quality (DQ) scoring engine
O3	Build an agricultural RAG knowledge base
O4	Implement an Agentic RAG reasoning workflow
O5	Compare proposed system against multiple baselines
O6	Evaluate robustness under multiple fault scenarios
O7	Build a web dashboard for monitoring and visualization
5. Research Questions
RQ1

How can real-time IoT sensor data be integrated with domain-specific agricultural knowledge through RAG to support explainable greenhouse decision-making?

RQ2

How does hardware-level corruption such as invalid BCD codes and missing sensor values affect AI recommendation reliability?

RQ3

Can an Agentic RAG framework improve contextual relevance, explainability, and safe-failure capability compared with:

Rule-based systems
LLM-only systems
Naive RAG systems?
RQ4

How effective is the framework under:

Normal conditions
Missing data
BCD logic faults
Conflicting sensors?
RQ-BCD

How can BCD arithmetic error detection serve as a lightweight real-time data validation gate for AIoT systems?

Inline hardware validation equation:

Err=Cy+S
3
	​

S
2
	​

+S
3
	​

S
1
	​


6. Proposed System Architecture
Multi-Layer Architecture
IoT Sensors
    ↓
BCD Encoding Layer
    ↓
BCD Error Detection Gate
    ↓
Data Quality Engine
    ↓
Agentic RAG Pipeline
    ↓
LLM Decision Engine
    ↓
Recommendation API
    ↓
Dashboard & Actuator Control
7. Hardware-Level BCD Validation
BCD Error Detection Logic

The system validates sensor bitstreams using minimized Boolean logic.

BCD correction and overflow detection equation:

Err=Cy+S
3
	​

S
2
	​

+S
3
	​

S
1
	​


Where:

Cy = Carry bit
S3 S2 S1 = Sum bits from BCD arithmetic

If:

Err = 1
Invalid BCD code detected
Overflow occurs

Then:

Data quality score is reduced
System enters uncertainty-aware mode
Unsafe actuator actions are blocked
8. Data Quality Assessment Engine
Data Quality Dimensions
Dimension	Metric	Detection Method
Validity	BCD invalid rate	Boolean logic checking
Completeness	Missing ratio	Null/drop packet analysis
Consistency	Sensor variance	Cross-sensor correlation
Data Quality Formula

DQ
Score
	​

=0.40S
bcd
	​

+0.35S
complete
	​

+0.25S
consistent
	​


Confidence Tiers
Tier	Range	System Action
HIGH	DQ > 0.85	Fully automated
MEDIUM	0.65 < DQ ≤ 0.85	Lower confidence
LOW	0.40 < DQ ≤ 0.65	Require approval
UNRELIABLE	DQ ≤ 0.40	Safe-failure halt
9. Agentic RAG Workflow
Workflow Steps
Observe
    ↓
Diagnose
    ↓
Retrieve
    ↓
Evaluate
    ↓
Verify
    ↓
Conclude
Agent Pipeline
Sensor Stream
    ↓
BCD Validation
    ↓
DQ Scoring
    ↓
RAG Retrieval
    ↓
LLM Reasoning
    ↓
Self Verification
    ↓
Safe Recommendation
10. Knowledge Base Design
Document Sources

The RAG system retrieves agricultural knowledge from:

VietGAP greenhouse standards
FAO climate control guidelines
Irrigation manuals
Environmental control references
Sensor calibration guides
Embedding Pipeline
PDF Documents
    ↓
Chunking
    ↓
Embedding
    ↓
Vector Database
    ↓
Similarity Search
    ↓
Top-k Retrieval
Embedding Model

Recommended embedding model:

multilingual-e5-large

Recommended vector databases:

Qdrant
ChromaDB
11. Experimental Design
Evaluation Scenarios
Scenario	Description
S1	Normal operation
S2	Missing sensor packets
S3	Injected invalid BCD codes
S4	Conflicting sensor values
Baseline Models
Baseline	Description
Rule-Based	Threshold logic only
LLM-Only	No retrieval
Naive RAG	Retrieval without agent reasoning
Proposed	Agentic RAG + BCD validation
12. Expected Results
Baseline Comparison
Model	Accuracy	Hallucination	Safe-Failure	Latency
Rule-Based	0.51	0%	12.5%	12ms
LLM-Only	0.65	18.2%	45.0%	1450ms
Naive RAG	0.72	5.4%	38.8%	1980ms
Agentic RAG + BCD	0.87	<0.8%	98.2%	2340ms
13. Main Contributions

This research makes three major contributions:

Introduces BCD arithmetic error detection as a lightweight hardware-level validation mechanism for AIoT systems.
Proposes a composite Data Quality Score that dynamically controls safe-failure decision behavior.
Demonstrates that Agentic RAG combined with hardware validation significantly improves:
recommendation accuracy
explainability
hallucination resistance
safe-failure capability
14. Recommended Technologies
Layer	Technology
Backend API	FastAPI
Database	PostgreSQL + TimescaleDB
Vector DB	Qdrant
Embedding	multilingual-e5-large
LLM	GPT-4o / Ollama
Frontend	React + TailwindCSS
Dashboard	Recharts
Logic Layer	Python bitwise operations
15. Suggested GitHub Repository Structure
NCKH-BCD-AgenticRAG/
│
├── 01_topic_proposal/
├── 02_related_work/
├── 03_hardware_and_dq_layer/
├── 04_rag_knowledge_base/
├── 05_agentic_pipeline/
├── 06_experimental_suite/
├── 07_system_dashboard/
├── 08_academic_paper/
├── docs/
├── assets/
├── README.md
├── requirements.txt
├── docker-compose.yml
└── .gitignore
16. Suggested README Sections

Your GitHub README should contain:

Project Introduction
System Architecture
Features
Installation Guide
Running the Simulation
Fault Injection Examples
Evaluation Metrics
Dashboard Preview
Experimental Results
Citation & References
17. Suggested Keywords
AI & RAG
Agentic RAG
Explainable AI
Safe-Failure AI
Agricultural LLM
AIoT
Hardware & Validation
BCD arithmetic validation
Digital logic fault detection
Hardware-aware AI
Data quality assessment
Agriculture
Smart greenhouse
Precision agriculture
Climate control
Sensor anomaly detection
18. Final Improved Contribution Statement

This study proposes a novel hardware-aware Agentic RAG framework for AIoT smart agriculture that integrates lightweight BCD arithmetic error detection with data quality-aware reasoning. By combining hardware-level validation, composite data quality scoring, and retrieval-augmented autonomous decision-making, the proposed framework significantly improves recommendation reliability, explainability, and safe-failure robustness under sensor corruption and fault injection scenarios.

19. Recommended GitHub Project Description
Hardware-aware Agentic RAG framework for smart greenhouse monitoring using BCD arithmetic error detection, data quality assessment, and explainable AIoT decision support.
20. Suggested GitHub Topics
agentic-rag
smart-agriculture
aiot
rag
llm
qdrant
fastapi
timescaledb
greenhouse
data-quality
bcd
digital-logic
sensor-fault-detection
safe-failure
explainable-ai
langchain
