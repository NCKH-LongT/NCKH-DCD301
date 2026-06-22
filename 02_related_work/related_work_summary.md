# Related Work Summary

The research scope of this project lies at the intersection of four core academic domains: IoT/AIoT systems in smart agriculture, RAG and LLM-based decision support systems, real-time sensor data quality assessment, and stateful agentic frameworks featuring causal explainability (XAI). Below is a comprehensive academic overview of the existing literature in these respective areas.

---

## 2.1 IoT and AIoT in Smart Agriculture

Recent literature (2022–2024) has extensively systematized IoT architectures designed for precision agriculture, outlining sensor layers, wireless sensor network (WSN) communication protocols (such as LoRa and Zigbee), hardware gateway configurations, cloud/edge computing infrastructure, and practical deployment scenarios including greenhouse monitoring, smart irrigation, and automated pest management. 

Current AIoT trends emphasize the integration of lightweight machine learning models directly onto edge devices (Edge Intelligence / TinyML) to strike a viable balance between data processing latency and cloud transmission costs. While experimental applications, such as smart greenhouse monitoring prototypes, have successfully demonstrated practical feasibility on a small scale, long-term empirical evaluations and dynamic adaptation under highly volatile real-world environmental conditions remain severely limited. Furthermore, the vast majority of existing systems rely heavily on static, rule-based thresholding mechanisms for physical device control, completely lacking dynamic, contextual reasoning capabilities when faced with transient environmental anomalies or hardware configuration updates.

---

## 2.2 RAG and LLM for Decision Support Systems

Large Language Models (LLMs) have shown remarkable capabilities in natural language understanding. However, the inherent issue of "hallucination" and the lack of domain-specific, real-time updated knowledge pose critical barriers when deploying LLMs in highly sensitive domains like agriculture. The introduction of Retrieval-Augmented Generation (RAG) by Lewis et al. (2020) effectively resolved these limitations by dynamically coupling the parametric memory of LLMs with external, non-parametric knowledge sources stored in Vector Databases.

In the agricultural sector, recent frameworks such as AgriIR (Seal et al., 2026) have shown that RAG pipelines can be modularized to operate efficiently within narrow domains, retrieving technical farming guidelines with deterministic, verifiable citations even when utilizing smaller, open-source models. Nevertheless, comprehensive RAG surveys (Huang & Huang, 2024) highlight that the generation quality is entirely bottlenecked by the accuracy of the retrieval mechanism (Retriever). When queries are complex or context windows become diluted with semantic noise, traditional RAG systems often retrieve irrelevant or conflicting documents, thereby compromising the correctness and physical safety of the generated decision support recommendations.

---

## 2.3 Sensor Data Quality and Anomaly Detection

Virtually all contemporary agricultural AIoT and RAG frameworks operate under an idealized assumption: that raw data harvested from physical sensors is consistently clean, continuous, and highly accurate. In reality, the harsh and unpredictable physical environment of agricultural fields (characterized by extreme temperature fluctuations, high humidity, dust, and chemical interference) renders sensors highly prone to diverse data quality anomalies. These anomalies include missing values due to network disruption, extreme noise and outliers, stuck sensor values, calibration drift caused by hardware degradation, and cross-sensor parameter conflicts.

Research in IoT data quality (Zhang et al., 2023; Al-Omari et al., 2024) has yielded mathematical and machine learning techniques for anomaly detection and data imputation. However, these methods are almost exclusively designed as isolated, independent preprocessing modules. Currently, there is a distinct lack of research on integrating these real-time data quality indicators directly into the prompt and reasoning workflows of LLMs/RAG systems. Consequently, existing frameworks remain vulnerable to propagating undetected sensor faults into downstream logical reasoning processes.

---

## 2.4 Agentic RAG and Stateful Explainability (XAI)

To transcend the architectural limitations of static, single-turn RAG systems, contemporary research is shifting toward stateful Agentic RAG paradigms built on frameworks like LangGraph and ReAct (Yao et al., 2023). Agentic RAG enables autonomous agents to iteratively plan, select appropriate tools (such as Data Quality Checkers and domain-specific RAG Retrievers), execute reasoning loops, and maintain state over extended operational horizons.

When deploying Agentic RAG for physical agricultural control, explainability and safety are paramount. Literature on LLM-based XAI (Bilal et al., 2025) underscores that numerical confidence weights or statistical probability scores are practically meaningless to human farm operators. Instead, causal explanation paradigms, exemplified by the CEMA framework (Causal Explanations in Multi-Agent systems, 2025), propose probabilistic counterfactual simulations to generate natural language explanations structured around causes and effects (e.g., *"The system recommends activating the cooling fan because the ambient temperature exceeds 35°C; counterfactual simulation indicates that failing to act will lead to crop heat stress within 10 minutes"*). Synthesizing stateful Agentic RAG with causal, evidence-backed explanations represents a critical frontier in delivering agricultural decision support that is highly adaptive, transparent, and capable of fostering human operator trust.
