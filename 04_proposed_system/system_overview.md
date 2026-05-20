# System Overview

This document provides a comprehensive overview of the Data Quality-Aware Agentic RAG Framework. The core objective of this software system is to enable reliable, real-time automated decision support for high-tech greenhouse agriculture by executing a resilient, data-validated processing loop.

## 1. System Vision & Objective
Traditional AIoT automation models often fail when physical sensors malfunction, feeding corrupted data directly into decision-making algorithms. This framework introduces a computer-based software pipeline that cross-references cleaned environmental observations with digitized technical knowledge bases, ensuring that every automated actuator action is mathematically sound and procedurally verified.

## 2. Core Functional Components
The system's lifecycle is built entirely upon a closed-loop 3-step cycle execution:

### A. Data Quality-Aware Ingestion
* **Purpose:** Acts as the system’s first line of defense against corrupted telemetry.
* **Mechanism:** The application processes simulated environmental timelines containing essential greenhouse metrics: Temperature, Humidity, and pH levels via structured files (`.csv`/`.xlsx`).
* **Resilience Testing:** To rigorously evaluate data handling capabilities, an embedded scripting module actively performs targeted error injection (such as dropping rows or generating anomalous numeric spikes), forcing the data quality sub-module to dynamically identify and flag broken sensor simulations.

### B. Retrieval-Augmented Generation (RAG) Engine
* **Purpose:** Provides a verifiable, authoritative knowledge foundation to eliminate AI hallucinations.
* **Mechanism:** Comprehensive physical booklets, cultivation rulebooks, and specialized plant nutrition manuals are parsed, indexed, and transformed into vector stores. 
* **Dynamic Querying:** When raw metrics cross acceptable agricultural thresholds, the system automatically translates the real-world warning into a semantic search query, instantly retrieving the exact procedural guidelines needed for mitigation.

### C. Intelligent Agentic Control Core
* **Purpose:** Synthesizes status and triages remediation steps.
* **Mechanism:** Powered by a Large Language Model (LLM) orchestration core, the AI Agent acts upon two concurrent streams: validated, non-corrupted environmental metrics and the exact textual source snippets retrieved by the RAG engine.
* **Action Output:** The final determination is compiled into a programmatic, machine-executable format to trigger simulated components (e.g., initiating precise irrigation dosages in milliliters or enabling air exchange fans).

## 3. High-Level Operational Flow
1. **File Parsing:** The platform continuously reads incoming time-series greenhouse telemetry logs.
2. **Quality Scrubbing:** Data packets pass structural checks; missing fields or corrupted telemetry spikes are identified and isolated.
3. **Anomaly Identification:** Cleaned environmental values are cross-checked against crop-specific growth boundaries.
4. **Knowledge Retrieval:** If an environmental parameter is out of bounds, relevant digitized instruction segments are extracted.
5. **Agent Inference:** The LLM-driven core maps the raw telemetry data onto the extracted textual rule framework.
6. **Command Serialization:** The system generates a highly structured JSON file detailing exact corrective commands, transparent logical reasoning, and exact source verifications.