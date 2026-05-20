# System Output Specification & Schema

## 1. Technical Output Format
[cite_start]The ultimate output of the closed-loop execution cycle processed by the AI Agent must be exported as a single, structurally unified **JSON file**[cite: 20].

## 2. Mandatory Schema Fields
[cite_start]To ensure compliance and system usability, each generated JSON file must encompass the following components[cite: 20]:
1. [cite_start]**Device Control Commands:** Explicit instructions defining which actuator to trigger along with quantitative parameters (e.g., turning on a fan, or watering a specific volume in ml)[cite: 19, 20].
2. [cite_start]**Reasoning Explanation:** A clear, natural language explanation detailing exactly why the AI decided on those actions[cite: 20].
3. [cite_start]**Verification Evidence:** An exact text quote from the original digitized technical document discovered by the RAG engine to establish complete trust[cite: 20].

## 3. Sample JSON Output Schema
```json
{
  "timestamp": "2026-05-20T16:45:00Z",
  "system_status": "Warning",
  "control_commands": [
    {
      "actuator": "Fan",
      "status": "ON"
    },
    {
      "actuator": "Water Pump",
      "status": "ON",
      "volume_ml": 250
    }
  ],
  "reasoning": "The current greenhouse temperature has exceeded the standard threshold. The system activates the ventilation fan to cool down the environment and triggers irrigation to prevent plant dehydration.",
  "verification": {
    "document_title": "High_Tech_Agriculture_Manual.pdf",
    "exact_quote": "When the greenhouse temperature exceeds the safety threshold, immediately activate the ventilation system and provide an additional 200ml to 300ml of water to avoid heat shock."
  }
}