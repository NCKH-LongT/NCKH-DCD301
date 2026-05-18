# Domain Selection and Rationale

> System: **Agentic RAG Framework for Smart Agriculture (SmartAgri)**

---

## 1. Selected Domain

**Domain name:** Smart Agriculture with IoT Sensor Networks — Vietnamese Rice and Vegetable Cultivation

**Specific scope:**
- **Paddy rice** cultivation in the Mekong River Delta (MRD), Vietnam
- **Short-cycle vegetables** (mustard greens, cucumber, tomato)
- **IoT sensor networks** deployed in the field (air temperature, soil moisture, soil pH, light intensity, rainfall, EC, water level)
- Decision support for **irrigation, fertilisation, and pest/disease alerts**

---

## 2. Rationale for Domain Selection

### 2.1. High Societal Impact and Urgency

Agriculture accounts for approximately **14.3% of Vietnam's GDP** and is the primary livelihood of over **40% of the workforce**. The Mekong River Delta alone produces more than **50% of the country's rice output**, yet faces escalating pressures:
- Climate change: irregular saltwater intrusion, unpredictable flooding, rising temperatures
- Rural labour shortage driven by rapid urbanisation
- Limited access by smallholder farmers to timely, expert agronomic advice

→ **An intelligent, real-time decision-support system addresses a genuine and urgent need**, not a purely theoretical research problem.

### 2.2. Direct Alignment with All Four Research Questions

| RQ | Why This Domain Fits |
|---|---|
| RQ1 | AgriIoT deployments generate diverse, high-frequency sensor streams — ideal for testing real-time data integration with domain knowledge |
| RQ2 | Harsh field environments (rain, heat, flooding, dust) cause frequent sensor failures and data gaps — providing a realistic and challenging data-quality testbed |
| RQ3 | Existing government extension rule systems serve as ready-made, comparable baselines for the Agentic RAG evaluation |
| RQ4 | Highly variable field conditions (weather events, power outages, sensor aging) make fault and conflict scenarios easy to reproduce and verify |

### 2.3. Rich, Verifiable Domain Knowledge Sources

Vietnam possesses a well-developed corpus of agricultural technical knowledge suitable for populating the RAG knowledge base:
- **Rice Cultivation Technical Guidelines** — Ministry of Agriculture and Rural Development (MARD), updated 2022
- **VietGAP standards** for vegetable production
- **National Agricultural Extension System** — thousands of field-tested technical documents
- **IRRI and Can Tho University** research on sustainable rice cultivation in the MRD
- **FAO** guidelines on climate-adaptive irrigation management

→ The Vector Database can be built on **real, citable, and expert-validated sources** — not synthetic content.

### 2.4. Clear Research Gap

Existing AI applications in Vietnamese agriculture primarily focus on:
- Standalone ML models (Random Forest, CNN for pest image recognition) — no explainability, no knowledge integration
- Hard-coded rule-based extension systems — cannot adapt to novel contexts or be updated incrementally
- No published system combines **Agentic RAG + IoT streaming data + domain knowledge retrieval** in a Vietnamese agricultural context

→ This study fills a genuine gap at the intersection of Agentic AI, Retrieval-Augmented Generation, and precision agriculture.

### 2.5. Practical Data Accessibility

- Multiple IoT AgriTech deployments are active in the MRD (VinFarm, FPT Smart Agri, Mimosa Technology)
- Sensor data can be accurately simulated using real historical climate records from the Vietnamese Meteorological and Hydrological Administration (VNMHA)
- Agricultural domain experts are available for collaborative gold-standard labelling of evaluation scenarios

---

## 3. Research Scope Definition

### In-Scope
- ✅ Five core sensor modalities: air temperature, soil moisture, soil pH, light intensity, rainfall
- ✅ Two primary crop types: paddy rice and short-cycle vegetables
- ✅ Three decision categories: irrigation scheduling, fertilisation advice, pest/disease alerts
- ✅ Four data quality failure modes: missing, noisy, faulty, conflicting
- ✅ Bilingual knowledge base: Vietnamese (extension documents) and English (international research)

### Out-of-Scope
- ❌ Image-based pest and disease recognition (computer vision)
- ❌ Commodity price forecasting and farm business decisions
- ❌ Automated actuator control (the system recommends actions; it does not execute them)
- ❌ Long-cycle industrial crops (coffee, rubber, pepper)
- ❌ Aquaculture and fishery management

---

## 4. Geographic Context

**Primary study region:** Mekong River Delta (MRD), Vietnam
- Representative provinces: An Giang, Can Tho, Kien Giang, Tien Giang
- Climate: Tropical monsoon — two distinct seasons (wet: May–November; dry: December–April)
- Mean annual temperature: 26–28°C; peak temperatures 38–40°C in April
- Mean annual rainfall: 1,400–2,000 mm

---

## 5. System Architecture Overview

```
[IoT Sensors]
     │  Raw numeric readings (every 5–30 min)
     ▼
[Layer 1: Edge Processing]
     │  Noise filtering · Hamming error correction · Overflow detection
     ▼
[Layer 2: Semantic Mapping]
     │  Numeric values → contextualised natural-language descriptions
     ▼
[Layer 3: RAG Retrieval — Vector Database]
     │  Embed query → cosine similarity search → top-5 chunks → rerank
     ▼
[Layer 4: Planning Agent + LLM]
     │  Multi-hop reasoning · Self-verification · R_score evaluation
     ▼
[Output: Recommendation + Evidence + Reasoning Chain + Confidence Score]
```

---

*Report date: 16 May 2026*
