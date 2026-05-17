# Selected Domain and Reason

Domain: Smart Greenhouse

Reason: This research aims to build a Smart Greenhouse system that applies IoT combined with a Multiplexer circuit to automatically monitor and control the greenhouse environment, while evaluating the efficiency of hardware resource optimization in embedded systems. By using temperature, humidity, light, and soil moisture sensors together with an ESP32/Arduino microcontroller and a Multiplexer circuit, the system can collect real-time environmental data to perform functions such as turning on fans, watering, turning on lights, and issuing alerts when environmental conditions exceed allowable thresholds.

Through system analysis and design combining IoT and digital circuits, the research shows that applying a Multiplexer helps reduce the number of I/O pins used on the microcontroller, optimize hardware costs, increase system scalability, and improve the efficiency of collecting data from multiple sensors simultaneously. At the same time, the topic demonstrates the high practical applicability of the Smart Greenhouse in supporting smart agriculture, saving water resources, and reducing dependence on manual human intervention.

The research results show that factors such as real-time data processing capability, sensor signal stability, system scalability, and hardware resource optimization significantly affect the performance of the Smart Greenhouse system. In that context, the use of a Multiplexer circuit plays an important role in improving the system’s stability and integrability, contributing to a foundation for further research in IoT, embedded systems, and ASIC design.

This scope is proposed for a 3-person team to complete in 60 days. The project focuses on Smart Greenhouse Monitoring and Decision Support using realtime sensor data, a Multiplexer-based combinational circuit, and an Agentic RAG workflow.

## Project Scope
- Smart Greenhouse Monitoring and Decision Support
- Four sensors: temperature, humidity, soil moisture, light
- Real-time environment monitoring
- Real-time data analysis
- Recommendations and automated actions: turn on fan, turn on irrigation, turn on lights, send alert

## Multiplexer Research Theme
To fit the research theme of combinational circuits, the group will integrate a Multiplexer (MUX) into the Smart Greenhouse system to:
- optimize ESP32 GPIO usage
- allow multiple sensors to share one ADC input
- reduce hardware cost
- improve scalability

Example:
- multiple soil moisture sensors using a single ADC input through a MUX

## Why this scope is reasonable
The scope includes:
- IoT realtime 
- Data quality 
- RAG 
- Agent workflow 
- Evaluation 
- Multiplexer combinational circuit 
- Baseline comparison 
- Explainable AI 

## Technical Scope
### Hardware Layer
- 1 Multiplexer: CD4051 or 74HC151
- ESP32 or Arduino
- 2–4 sensors

ESP32 responsibilities:
- control MUX select pins
- read sensors sequentially

Example mapping:
- MUX Select 00 → Temperature
- MUX Select 01 → Humidity
- MUX Select 10 → Soil Moisture
- MUX Select 11 → Light

### AIoT + Agentic RAG
Workflow:
- Sensor/MUX
- Data API
- Database
- Data Quality Module
- State Analyzer
- RAG Retrieval
- LLM Agent
- Recommendation JSON

## Keep it simple
Sensors:
- only 4 sensors

Actions:
- turn on fan
- turn on irrigation
- turn on lights
- send alert

Data quality module covers:
- missing data 
- outliers 
- sensor stuck 
- conflict detection 

RAG:
- 5–10 PDF documents

Agent:
- single workflow agent

No need for:
- multi-agent
- autonomous planning

## Research Contribution
- Integrate realtime sensors, Multiplexer combinational circuit, and Agentic RAG.
- Evaluate how sensor data quality affects AI recommendation.
- Compare rule-based, LLM-only, RAG-only, and proposed Agentic RAG.
- Evaluate missing data, faulty sensors, and conflicting sensor scenarios.

## Feasibility in 60 days
- Prototype 
- Multiplexer integration 
- RAG pipeline 
- Agent workflow 
- Evaluation 
- Paper draft 
- Demo 

## Why this is ideal for student research
This scope balances AI, IoT, digital circuits, RAG, explainability, evaluation, baseline comparison, and contribution, while staying small enough for completion in 60 days with a team of 3 people.
