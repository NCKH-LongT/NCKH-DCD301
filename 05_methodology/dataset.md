# Sensor List & Data Quality Control Testing Scenario

## 1. Collected Sensor Parameters
[cite_start]The system reads environmental time-series data from a high-tech agricultural greenhouse, focusing on three core parameters[cite: 4]:
* [cite_start]**Temperature:** Monitors the ambient air temperature inside the greenhouse[cite: 9].
* [cite_start]**Humidity:** Monitors the air and soil moisture levels[cite: 9].
* [cite_start]**pH Level:** Monitors the acidity or alkalinity of the nutrient solution[cite: 9].

## 2. Data Ingestion Method
* [cite_start]The system actively reads environmental data (Temperature, Humidity, pH) from an existing Excel or CSV file[cite: 9].

## 3. Data Quality Control Experimental Scenario
* [cite_start]**Active Error Injection:** The development team will write specific source code to actively inject errors into the input file (such as deleting data entries or modifying values to spikes)[cite: 10].
* [cite_start]**Testing Objective:** To verify and evaluate whether the software can automatically detect these injected junk data inputs or recognize simulated broken sensors[cite: 10].