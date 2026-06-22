# Research Gap

Based on a systematic review of the literature matrix and related work, the research team has identified three critical gaps in the existing body of knowledge:

---

## 1. Lack of Data Quality Awareness and Self-Correction in LLM/RAG Decision Support Systems

*   **Current State:** Most state-of-the-art decision-making systems in smart agriculture (whether rule-based or based on classical machine learning) operate under the naive assumption that sensor data is pristine, continuous, and highly accurate.
*   **The Gap:** In actual deployment environments, hardware degradation and connection issues frequently cause missing telemetry values, calibration drift, stuck sensors, or cross-sensor conflicts. While independent data quality pipelines exist in IoT literature, modern RAG and LLM frameworks are completely "blind" to these anomalies. They directly ingest faulty sensor readings into prompts, leading to highly unsafe or hallucinated actions without any mechanism to down-weight recommendation confidence or activate robust, adaptive reasoning paths in response to poor data quality.

---

## 2. Inability of Static RAG to Support Stateful, Dynamic Reasoning and Context Filtering

*   **Current State:** Traditional RAG systems are designed as single-turn, stateless query-retrieval-generation pipelines optimized primarily for semantic similarity (cosine similarity).
*   **The Gap:** Precision agriculture is inherently a highly dynamic and stateful physical environment. A control action (e.g., watering) cannot be determined solely by a single static sensor reading; it requires reasoning over temporal states (irrigation history), real-time microclimate trends, weather forecasts, and authoritative agricultural guidelines. Static RAG pipelines lack the architecture to represent and maintain states over time, such as integrating a Finite State Machine (FSM). Furthermore, they lack specialized semantic filtering to prevent topic drift or handle conflicting technical guidelines within the vector database, leading to degraded recommendation accuracy.

---

## 3. Absence of Verifiable Causal Explainability and Unified Confidence Scoring for Physical Control Actions

*   **Current State:** Explainability in current AIoT systems is restricted to technical, numerical, or statistical outputs (e.g., *"Model confidence: 92%"* or *"Feature importance: 0.45"*), which are unintuitive and unactionable for farm operators.
*   **The Gap:** There is a complete lack of natural language explanations structured around **causal and teleological logic**—specifically answering *why an action was recommended (motivation)* and *what would happen if the recommendation were ignored (counterfactual simulation)*—supported by verifiable citations from domain literature. Moreover, existing systems lack a unified confidence scoring metric that integrates sensor reliability (data quality) and retriever relevance (RAG score) into a single, standardized safety indicator before executing autonomous physical actions in the real world.

---

## 🎯 Core Overarching Research Gap

> [!IMPORTANT]
> **Core Research Gap:** To date, no study has successfully integrated a **Data Quality-Aware Agentic RAG Framework** for real-time physical AIoT control. 
> Existing frameworks fail to bridge the gap between low-level sensor telemetry anomalies and high-level knowledge-based LLM reasoning. There is no unified, stateful system capable of automatically detecting sensor faults, executing state-aware RAG reasoning over physical guidelines, and producing explainable recommendations with verified evidence and a unified, multi-dimensional confidence score.
