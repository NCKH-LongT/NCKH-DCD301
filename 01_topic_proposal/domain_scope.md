# Selected Domain and Rationale

> System: **Agentic RAG in Smart Agriculture (SmartAgri)**

---

## 1. Selected Domain

**Domain name:** Smart Agriculture with IoT in Vietnam  
**English title:** Smart Agriculture with IoT — Vietnamese Rice and Vegetable Cultivation

**Specific scope:**
- **Rice cultivation** in the Mekong Delta region
- **Short-cycle vegetable cultivation** such as mustard greens, cucumber, and tomato
- Use of **outdoor IoT sensor networks** including temperature, soil moisture, pH, light intensity, and rainfall sensors
- Decision support for **irrigation, fertilization, and pest/disease warning**

---

## 2. Rationale for Selecting This Domain

### 2.1. High urgency and strong social impact

Agriculture accounts for approximately **14.3% of Vietnam’s GDP** and supports the livelihood of more than **40% of the national workforce**. The Mekong Delta produces more than **50% of Vietnam’s rice output**, but it is currently facing several major challenges:

- Climate change, including drought, salinity intrusion, abnormal flooding, and rising temperatures
- Rural labor shortages due to urbanization
- Limited access for farmers to timely and specialized technical knowledge

Therefore, an intelligent decision support system is a practical need rather than a purely theoretical research topic.

### 2.2. Strong alignment with the four Research Questions

| RQ | Reason why the domain is suitable |
|---|---|
| RQ1 | Smart agriculture provides diverse IoT sensors and rich real-time data for integration. |
| RQ2 | Harsh field conditions often cause missing, noisy, faulty, or conflicting sensor data, making data quality evaluation highly practical. |
| RQ3 | Existing agricultural advisory systems are often rule-based, which provides a realistic baseline for comparison. |
| RQ4 | Field conditions such as rain, heat, power loss, and unstable connectivity create realistic fault scenarios for robustness testing. |

### 2.3. Availability of rich domain-specific knowledge sources

Vietnam has many high-quality agricultural technical documents, including:

- **Technical guidelines for rice cultivation** issued by the Ministry of Agriculture and Rural Development (MARD), updated in 2022
- **VietGAP standards** for vegetable cultivation
- Documents from the **National Agricultural Extension System**
- Research from **IRRI and Can Tho University** on sustainable rice cultivation

These sources make it possible to build a Vector Database using real and verifiable domain knowledge.

### 2.4. Clear research gap

Current studies on AI in Vietnamese agriculture mainly focus on:

- Basic machine learning models such as Random Forest or CNN for pest/disease detection, often with limited explainability
- Rigid rule-based agricultural advisory systems that cannot adapt well to changing contexts
- A lack of systems that combine **Agentic RAG, IoT, and domain-specific agricultural knowledge** in the Vietnamese context

### 2.5. Feasibility of real-world data collection

- Several smart agriculture and IoT-based farming projects are already active in the Mekong Delta, such as VinFarm, FPT Smart Agri, and Mimosa Technology
- Sensor data can be simulated based on real Vietnamese climate and farming conditions
- Agricultural experts can participate in evaluation by providing gold-standard labels for experimental scenarios

---

## 3. Research Scope

### In-scope

- ✅ IoT sensors measuring five parameters: air temperature, soil moisture, soil pH, light intensity, and rainfall
- ✅ Two main crop groups: rice and short-cycle vegetables
- ✅ Three decision groups: irrigation, fertilization, and pest/disease warning
- ✅ Handling four types of data quality issues: missing, noisy, faulty, and conflicting data
- ✅ Knowledge sources in both Vietnamese and English, including agricultural extension documents and international research papers

### Out-of-scope

- ❌ Pest/disease recognition using image-based computer vision
- ❌ Agricultural price forecasting and business decision-making
- ❌ Automatic actuation or direct control of irrigation devices; the system only provides recommendations
- ❌ Long-term industrial crops such as coffee, rubber, and pepper
- ❌ Aquaculture

---

## 4. Geographical Context

**Primary research area:** Mekong Delta, Vietnam

Representative provinces include:

- An Giang
- Can Tho
- Kien Giang
- Tien Giang

**Climate characteristics:**

- Tropical monsoon climate with two distinct seasons:
  - Rainy season: May to November
  - Dry season: December to April
- Average temperature: 26–28°C
- Peak temperature: up to 38–40°C in April
- Average annual rainfall: 1,400–2,000 mm
