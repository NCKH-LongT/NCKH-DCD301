# Sensor Reference Table — Readings, Meanings, and Recommended Actions

> System: **Agentic RAG Framework for Smart Agriculture (SmartAgri)**

---

## 1. Sensor Inventory

| ID | Sensor Type | Unit | Sampling Interval | Deployment Position |
|---|---|---|---|---|
| S01 | Air temperature | °C | Every 5 min | 1.5 m height, shaded from direct sun |
| S02 | Air humidity | % RH | Every 5 min | Co-located with S01 |
| S03 | Soil moisture | % | Every 15 min | 15–20 cm depth |
| S04 | Soil pH | pH (0–14) | Every 30 min | 10 cm depth |
| S05 | Light intensity | lux | Every 10 min | Unobstructed position |
| S06 | Rainfall (rain gauge) | mm/hr | Continuous | Open area, no overhang |
| S07 | Soil EC (electrical conductivity) | mS/cm | Every 30 min | 15 cm depth |
| S08 | Field water level | cm | Every 15 min | Corner of field, free water flow |

---

## 2. Threshold Values, Agronomic Meanings, and Recommended Actions

### 2.1. Air Temperature (S01)

| Reading (°C) | Severity | Agronomic Meaning | Crops Affected |
|---|---|---|---|
| < 15 | ⚠️ Cold stress | Too cold — inhibits growth, promotes fungal disease | Rice, vegetables |
| 15 – 22 | 🟡 Suboptimal low | Slow growth; supplemental covering recommended | Vegetables |
| 22 – 30 | ✅ Optimal | Ideal conditions for rice and vegetables | Rice, vegetables |
| 30 – 35 | 🟡 Suboptimal high | Increased evapotranspiration; additional irrigation needed | Rice, vegetables |
| 35 – 38 | ⚠️ Heat stress | Risk of floret sterility at heading stage | Rice (heading stage) |
| > 38 | 🔴 Critical heat | Spikelet sterility; yield loss 30–50% if sustained | Rice |
| > 100 or < −10 | ❌ Sensor fault | Physically impossible value | — |

**Recommended actions:**
- **< 15°C:** Issue cold alert; recommend polyethylene mulch cover; reduce irrigation frequency
- **35–38°C:** Recommend mist irrigation at 05:00–07:00 and 17:00–18:00 to reduce canopy temperature
- **> 38°C:** Issue urgent alert; irrigate immediately; escalate to agronomist if sustained >12 hours

---

### 2.2. Soil Moisture (S03)

| Reading (%) | Severity | Agronomic Meaning | Growth Stage |
|---|---|---|---|
| < 20 | 🔴 Severe drought | Wilting, growth arrest | All stages |
| 20 – 40 | ⚠️ Water deficit | Irrigation required immediately | Tillering, heading |
| 40 – 60 | ✅ Adequate (vegetables) | Optimal for most vegetables | Vegetables |
| 50 – 80 | ✅ Adequate (rice) | Optimal for rice across growth stages | Rice |
| 80 – 90 | 🟡 Near saturation | Mild waterlogging risk for vegetables | Vegetables |
| > 90 | ⚠️ Waterlogged | Root oxygen depletion; root rot risk | Vegetables |
| > 100 | ❌ Sensor fault | Physically impossible | — |

**Recommended actions:**
- **< 30%:** Apply 20–30 mm irrigation immediately, preferably early morning
- **30–50% (rice at heading):** Apply 15 mm supplemental irrigation; re-check every 6 hours
- **> 90% (vegetables):** Stop irrigation; open drainage channels; no watering for at least 48 hours

---

### 2.3. Soil pH (S04)

| Reading (pH) | Severity | Agronomic Meaning | Recommended Action |
|---|---|---|---|
| < 4.0 | 🔴 Severely acidic | Soluble aluminium and iron become toxic to roots | Emergency lime application |
| 4.0 – 5.5 | ⚠️ Moderately acidic | Reduced phosphorus and potassium uptake | Apply dolomitic limestone |
| 5.5 – 6.5 | ✅ Optimal (vegetables) | Best nutrient availability for vegetables | Maintain |
| 5.5 – 7.0 | ✅ Optimal (rice) | Ideal pH range for rice production | Maintain |
| 7.0 – 8.0 | 🟡 Mildly alkaline | Reduced iron and manganese uptake; chlorosis risk | Apply sulphur or acidifying fertiliser |
| > 8.0 | ⚠️ Severely alkaline | Stunted growth, yellowing leaves | Urgent soil treatment |
| < 0 or > 14 | ❌ Sensor fault | Outside physical measurement range | — |

**Recommended actions:**
- **pH < 4.5:** Apply agricultural lime at 1–2 tonnes/ha; re-test after 7 days
- **pH 4.5–5.5:** Apply dolomitic limestone at 500 kg/ha combined with organic matter
- **pH > 7.5:** Apply ammonium sulphate fertiliser; use acidified irrigation water or elemental sulphur

---

### 2.4. Light Intensity (S05)

| Reading (lux) | Severity | Agronomic Meaning |
|---|---|---|
| < 10,000 | ⚠️ Insufficient light | Weak photosynthesis; etiolated growth |
| 10,000 – 30,000 | 🟡 Adequate (greenhouse) | Suitable for seedlings and shade crops |
| 30,000 – 60,000 | ✅ Good | Suitable for outdoor vegetables |
| 60,000 – 80,000 | ✅ Excellent | Optimal for rice |
| > 80,000 | ⚠️ Excessive | Leaf scorch risk; shade cloth recommended |

**Recommended actions:**
- **< 10,000 lux for 3+ consecutive days:** Alert for light deficiency; consider supplemental LED lighting (greenhouse only)
- **> 85,000 lux:** Recommend 30% black shade cloth installation during 11:00–14:00

---

### 2.5. Rainfall (S06)

| Reading (mm/day) | Level | Agronomic Meaning |
|---|---|---|
| 0 | None | Monitor soil moisture; irrigation likely needed |
| 1 – 10 | Light rain | Minimal supplement; irrigation still required |
| 10 – 25 | Moderate rain | Adequate for vegetables; monitor rice fields |
| 25 – 50 | Heavy rain | Sufficient for rice; suspend scheduled irrigation for 24 h |
| 50 – 100 | Very heavy rain | Waterlogging risk for vegetables |
| > 100 | Extreme rain | Urgent drainage recommended; inspect dykes and bunds |

**Recommended actions:**
- **0 mm for 5+ consecutive days + temperature > 32°C:** Issue drought alert; increase irrigation frequency
- **> 80 mm/day:** Inspect drainage infrastructure; issue waterlogging alert for vegetable plots

---

### 2.6. Soil Electrical Conductivity — EC (S07)

| Reading (mS/cm) | Level | Agronomic Meaning |
|---|---|---|
| < 0.2 | Very low | Nutrient-poor soil |
| 0.2 – 0.8 | ✅ Optimal | Suitable for most crops |
| 0.8 – 1.6 | 🟡 Elevated | Monitor salt-sensitive varieties |
| 1.6 – 3.0 | ⚠️ Saline intrusion | Impaired water uptake |
| > 3.0 | 🔴 Severe salinity | Crop death if untreated |

**Recommended actions:**
- **EC > 2.0 mS/cm:** Apply 50 mm freshwater leaching irrigation; re-test after 48 hours
- **EC > 3.0 mS/cm:** Issue critical alert; contact district extension officer immediately

---

### 2.7. Field Water Level (S08) — Rice Fields Only

| Reading (cm) | Growth Stage | Agronomic Meaning |
|---|---|---|
| −5 to 0 | Tillering | Saturated soil without ponding — ideal |
| 0 – 5 | Seedling stage | Shallow ponding — acceptable |
| 5 – 10 | Active tillering | Moderate ponding — optimal |
| > 15 | Any stage | Deep flooding — risk of damage |
| > 25 | Any stage | Submergence — severe crop loss risk |

**Recommended actions:**
- **> 20 cm (seedling stage):** Open drainage gates; reduce inflow immediately
- **< 0 cm (heading stage):** Apply 5–8 cm of water; maintain throughout the critical 2-week window

---

## 3. Multi-Sensor Decision Matrix

| Air Temp | Soil Moisture | Rainfall | Soil pH | Primary Recommendation | Priority |
|---|---|---|---|---|---|
| > 35°C | < 30% | 0 mm | Normal | **Irrigate immediately — 25–30 mm** | 🔴 Critical |
| 22–30°C | 40–70% | 0 mm | Normal | Maintain; follow scheduled irrigation | 🟢 Low |
| 22–30°C | Normal | 0 mm | < 5.0 | **Apply lime to correct soil pH** | 🟡 Medium |
| Normal | > 90% | > 50 mm | Normal | **Stop irrigation; open drainage** | 🔴 Critical |
| < 15°C | Normal | 0 mm | Normal | **Apply mulch cover; reduce irrigation** | 🟡 Medium |
| > 35°C | < 30% | 0 mm | < 5.0 | **Emergency irrigation + lime application** | 🔴 Very Critical |
| Normal | Normal | Normal | > 7.5 | **Apply acidifying amendment** | 🟡 Medium |
| Conflict | Conflict | — | — | **Escalate — request manual field inspection** | 🟠 Needs Review |

---

## 4. Semantic Mapping — From Raw Readings to RAG Query Text

Layer 2 of the system pipeline converts raw sensor values into natural-language strings used as retrieval queries for the RAG system:

| Sensor | Raw Value | Semantic Text (used as RAG query) |
|---|---|---|
| S01 – Air temp | 38.5°C | "Air temperature is at 38.5°C, critically above the safe threshold for rice at heading stage (>35°C). Risk of spikelet sterility. Immediate action required." |
| S03 – Soil moisture | 18% | "Soil moisture is only 18%, well below the minimum requirement (>50%) for rice during the heading stage. High risk of yield loss due to water deficit." |
| S04 – Soil pH | 4.2 | "Soil pH is 4.2, severely acidic. Phosphorus and micronutrients are locked. Lime application is urgently needed to prevent root toxicity." |
| S06 – Rainfall | 0 mm/24 h | "No rainfall recorded in the past 24 hours. Combined with high air temperature, there is a risk of localised drought stress." |
| S07 – Soil EC | 2.8 mS/cm | "Soil electrical conductivity is 2.8 mS/cm, exceeding the saline intrusion threshold (>1.6 mS/cm). Freshwater leaching irrigation is urgently required." |
| S08 – Water level | 22 cm | "Field water level is 22 cm, exceeding the safe limit (>15 cm). Rice seedlings are at risk of submergence damage." |

---

## 5. Data Quality Flags Reference

| Status Flag | Meaning | System Response |
|---|---|---|
| `ok` | Reading valid and within physical bounds | Used directly in reasoning |
| `missing` | No data received in the expected window | Imputation triggered (neighbour or LSTM) |
| `noisy` | Reading oscillates beyond ±3σ of 24 h history | Down-weighted; soft flag applied |
| `faulty` | Reading outside absolute physical bounds | Excluded from computation; sensor alert sent |
| `imputed` | Value was AI-generated to fill a gap | Used with reduced weight; flagged in output |
| `conflicting` | Two same-type sensors disagree by >20% | Conflict resolution pipeline triggered |

---

*Report date: 16 May 2026*
