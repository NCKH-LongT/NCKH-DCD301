# Sensor Action Table

| Sensor | Description | Sample Data | BCD Role | Related Action |
|---|---|---|---|---|
| Temperature | Measures greenhouse air temperature | 34°C | BCD arithmetic and overflow checking | Turn on fan |
| Humidity | Measures air humidity level | 82% | BCD validation | Turn on ventilation |
| Soil Moisture | Measures soil moisture level | 25% | Decimal arithmetic | Start irrigation |
| Light Sensor | Measures light intensity | 800 lux | BCD display processing | Turn on grow light |
| Water Flow Sensor | Measures irrigation water flow rate | 15 L/min | BCD accumulation | Stop irrigation |
| Sensor Quality Checker | Detects invalid BCD codes | 1111 → invalid | Error detection logic | Send warning |

---

# Example Rules

| Condition | Recommendation |
|---|---|
| Temperature > 35°C | Turn on fan |
| Soil moisture < 30% | Start irrigation |
| Light < threshold | Turn on grow light |
| Invalid BCD detected | Reduce confidence score |
| Multiple sensor conflicts | Require human approval |

---

# Example Invalid BCD Codes

| Binary | Status |
|---|---|
| 0000 | Valid |
| 0001 | Valid |
| 1001 | Valid |
| 1010 | Invalid |
| 1100 | Invalid |
| 1111 | Invalid |
