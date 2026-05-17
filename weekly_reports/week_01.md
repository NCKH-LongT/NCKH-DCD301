# Week 1 Progress Report - Research Theme 9

- **Class:** SE1930
- **Group:** G07
- **Project Title:** A Data Quality-Aware Agentic RAG Framework for Real-Time AIoT Decision Support in Smart Greenhouse

---

## 1. What did the group accomplish this week?
During the first week of the DCD course, the group established the theoretical and structural foundation of the project:
- **Project Registration & Domain Selection:** Selected the **Smart Greenhouse Control System** as our practical domain and successfully registered our Git branch **`SE1930_G07`** for collaborative work.
- **Directory Structure Initialization:** Created and committed the standard 16-week folder structure (from `01_topic_proposal` to `weekly_reports`) on the group branch.
- **Academic Research & RQ Solutions:** Deeply researched basic sequential circuits, distinguishing them from combinational circuits and formulating comprehensive academic answers for the four research questions (**RQ-09, RQ9.1, RQ9.2, RQ9.3**).
- **Sensor-Action Mapping & JSON Output Schema Design:** Drafted the mapping rules for greenhouse sensors and actuators, and structured the JSON schema conforming 100% to the guidelines with the required keys (`status`, `action`, `confidence`, `evidence`).

---

## 2. What are the specific outputs (files, code, tables)?
The following deliverables have been successfully pushed to our Git branch:
1. **topic_proposal.md**: Project abstract, problem definition, and research goals.
2. **domain_scope.md**: Detailed agricultural application domain and sequential circuit logic.
3. **sensor_action_table.md**: Tabular mapping of sensors to control states, incorporating data quality fault scenarios (Data Conflict and Fault/Missing).
4. **rq_explanation.md**: Detailed academic explanations for **RQ-09, RQ9.1, RQ9.2, and RQ9.3**.
5. **system_output_schema.json**: Standardized decision-output schema conforming to course specifications.
6. **paper_list.md**: The seed references for our literature review database.

---

## 3. Which RQs do these outputs address?
- The file **`rq_explanation.md`** directly addresses and answers all theoretical sequential circuit questions: **RQ-09, RQ9.1, RQ9.2, and RQ9.3**.
- The files **`domain_scope.md`**, **`sensor_action_table.md`**, and **`system_output_schema.json`** lay the groundwork for addressing **RQ1** (Knowledge integration with telemetry for explainable decisions) and **RQ2** (Effect of sensor data quality on agricultural recommendations).

---

## 4. Are there any current issues with the deliverables?
- The theoretical foundation, FSM states, and output structure are successfully finalized.
- There are no outstanding conceptual issues. For the upcoming weeks, the main challenge is setting up the Python workspace and initializing agronomical document ingestion (using ChromaDB and Docling).

---

## 5. What will the group do next week?
For Week 2, the group will focus on the **Literature Review** stage:
- Collect at least 5-10 high-quality academic papers regarding smart agriculture and sensor anomaly detection.
- Construct the literature review matrix (`literature_review_matrix.md`).
- Identify the research gap (`research_gap.md`) and define the unique contributions of our system.

---

## 6. What assistance does the group need from the instructor?
- We kindly request the instructor to review our **Topic Proposal** and **JSON Output Schema** to ensure they align perfectly with the research expectations before we begin coding.
