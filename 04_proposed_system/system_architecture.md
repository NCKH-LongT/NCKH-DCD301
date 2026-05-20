# System Architecture Specification

This document details the architectural design and block-level components of the Data Quality-Aware Agentic RAG Framework. The system is designed as a modular, computer-based automated decision support application that processes incoming environment data to produce valid control actions.

## 1. High-Level Block Architecture
The system consists of three decoupled operational layers that form a single closed-loop execution pipeline:
+-----------------------------------------------------------------------------+
|                               DATA INGESTION LAYER                          |
|  [Simulated Input: CSV/Excel] ---> [Error & Anomaly Injection Script]       |
+------------------------------------+----------------------------------------+
| (Raw & Injected Streams)
v
+-----------------------------------------------------------------------------+
|                            DATA QUALITY CONTROL LAYER                       |
|  [Statistical Imputation Engine] ---> [Noise & Outlier Isolation Filter]    |
+------------------------------------+----------------------------------------+
| (Cleaned Environmental Vectors)
v
+-----------------------------------------------------------------------------+
|                         INTELLIGENT AGENTIC RAG LAYER                       |
|  [Semantic Query Generator] <=======> [Vector Database / Document Store]    |
|               |                                      ^                      |
|               | (Cleaned Telemetry)                  | (Retrieved Context)  |
|               v                                      v                      |
|  +-----------------------------------------------------------------------+  |
|  |                             LLM AI AGENT                              |  |
|  |      [Reasoning & Planning Core] ----> [Structured Output Formatter]  |  |
|  +-------------------------------------------------+---------------------+  |
+----------------------------------------------------+------------------------+
|
v
[Standard Execution JSON Output]
## 2. Detailed Component Breakdown

### 2.1. Data Ingestion & Quality Layer
* **Telemetry Reader:** Actively parses time-series files (`.csv` or `.xlsx`) capturing parameters like Greenhouse Temperature, Air/Soil Humidity, and Nutrient Solution pH.
* **Error-Aware Validation Engine:** Evaluates data completeness. It checks for structural missing values (NaN) or extreme numeric deviations (spikes caused by broken sensors) based on predefined statistical bounds. It ensures only mathematically valid vectors proceed to the reasoning pipeline.

### 2.2. Retrieval-Augmented Generation (RAG) Core
* **Knowledge Vectorization:** Agricultural rulebooks, plant manuals, and irrigation guidelines are chunked and converted into semantic embeddings.
* **Context Retrieval Engine:** When telemetry values deviate from standard agricultural thresholds, the system generates queries to search the local knowledge store, pulling exact instructional paragraphs required to mitigate the detected greenhouse anomaly.

### 2.3. Agentic Orchestrator & Decision Core
* **LLM Reasoning Agent:** Serves as the centralized control center. It accepts the synchronized system inputs: the real-time cleaned sensor data and the validated technical manual segments.
* **Structured Command Formatter:** Evaluates the consolidated prompt, reasons through the corrective tasks (e.g., assessing if a fan or pump adjustment is required), and formats the operational decisions into a deterministic, programmatic output structure.

## 3. Communication Protocols & Data Contracts
The sub-modules communicate internally via object interfaces. The final boundary contract exiting the system is strictly bounded to the structured JSON schema specified in `data_flow.md`, ensuring decoupled interoperability between the core AI software framework and simulated hardware actuators.