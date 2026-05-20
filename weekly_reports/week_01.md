# Weekly Report - Week 01

* **Project:** A Data Quality-Aware Agentic RAG Framework for Real-Time AIoT Decision Support in Smart Agriculture
* **Progress Status:** Week 1 objectives completed (100%)

---

## 1. Progress Checklist Week 01

| Task Item | Status | Notes / Evidences |
| :--- | :---: | :--- |
| **Select specific domain** | [x] Completed | High-tech smart agriculture greenhouse |
| **List Sensor system** | [x] Completed | Identified 3 parameters: Temperature, Humidity, pH |
| **List Action system** | [x] Completed | Identified: Fan on/off, Watering by volume in ml |
| **Understand 4 Research Questions (RQs)** | [x] Completed | Defined the core research problems |
| **Define system Output structure** | [x] Completed | Standardized output structure in JSON format |

---

## 2. Detailed Results

* **Domain:** A PC-based AIoT software system designed to manage and automate high-tech agricultural greenhouses.
* **Operational Cycle (3 Steps):**
    1.  *Data Quality:* Read environmental data from Excel/CSV files, write code to proactively inject errors to test the filter for detecting junk data or faulty sensors.
    2.  *RAG:* Digitize cultivation manual documents into a digital database so the AI can "flip through the book" to find technical guidelines when anomalies occur.
    3.  *AI Agent:* Use an LLM Agent to synthesize clean sensor data with the retrieved documents to output device control commands (JSON) along with clear reasoning citations.

---

## 3. Next Week's Plan (Week 02)
* Define the set of document search keywords (`02_related_work/search_keywords.md`).
* Collect and compile a list of 3-5 high-quality scientific papers (`02_related_work/paper_list.md`).
* Conduct analysis and draft preliminary summaries for the selected papers (`02_related_work/paper_summaries/`).