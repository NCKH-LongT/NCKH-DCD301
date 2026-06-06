# Week 4 - Member 1 Deliverables Summary

## Project: IoT/Data Engineer - Sensor Data Pipeline

### Overview
Complete implementation of a sensor data pipeline including simulator, REST API, and database integration for the Week 4 project.

---

## ✅ Deliverables Completed

### 1. **Sensor Simulator** (`sensor_simulator.py`)
- ✓ Generates realistic sensor data with time-series characteristics
- ✓ Supports 4 sensor types: temperature, humidity, soil_moisture, light
- ✓ Three data scenarios: normal, warning, critical
- ✓ Configurable thresholds and ranges
- ✓ Continuous and batch modes
- ✓ Direct API integration capability
- ✓ JSON/JSONL export support

**Features:**
- Realistic drift and trend simulation
- Scenario-based data generation
- 12 default sensors across 3 locations
- Command-line interface with flexible options

### 2. **Database Schema** (`database_schema_week4.md` + `database/schema.sql`)
- ✓ PostgreSQL + TimescaleDB hypertable design
- ✓ Time-series optimized schema for sensor_data
- ✓ Device registry (sensor_devices table)
- ✓ Alert tracking (sensor_alerts table)
- ✓ Quality metrics tracking (data_quality_metrics table)
- ✓ Optimized indexes for common queries
- ✓ Compression policies for long-term storage
- ✓ Query examples and best practices

**Components:**
- Hypertable: `sensor_data` (time-series data)
- Table: `sensor_devices` (device registry)
- Table: `sensor_alerts` (alert logs)
- Table: `data_quality_metrics` (quality tracking)

### 3. **REST API** (`sensor_api/app.py`)
- ✓ Flask-based REST API server
- ✓ Endpoint: `POST /api/sensor-data` - Store single reading
- ✓ Endpoint: `POST /api/sensor-data/batch` - Store batch readings
- ✓ Endpoint: `GET /api/sensor-data/latest` - Retrieve latest readings
- ✓ Endpoint: `GET /api/sensor-data/status` - Get sensor status summary
- ✓ Endpoint: `GET /health` - Health check
- ✓ PostgreSQL connection pooling
- ✓ CORS support
- ✓ Error handling and logging
- ✓ Data validation

**API Features:**
- Connection pooling for performance
- Automatic sensor device registration
- Status-based queries
- Batch operations support
- Comprehensive error messages

### 4. **Sample Data Files** (3 CSV files)
- ✓ `sample_data/sample_sensor_data_normal.csv` - 24 records (normal range)
- ✓ `sample_data/sample_sensor_data_warning.csv` - 24 records (warning range)
- ✓ `sample_data/sample_sensor_data_critical.csv` - 24 records (critical range)

**Data Coverage:**
- 3 locations (greenhouse_1, field_2, storage_3)
- 4 sensor types per location (temperature, humidity, soil_moisture, light)
- Multiple time points (2 readings per sensor at 5-minute intervals)
- Realistic sensor values for each scenario

### 5. **Supporting Files**
- ✓ `requirements.txt` - Python dependencies
- ✓ `.env.example` - Environment configuration template
- ✓ `README.md` - Comprehensive documentation and setup guide
- ✓ `load_data.py` - Utility to load CSV/JSONL data into database
- ✓ `quickstart.sh` - Automated setup script
- ✓ `sensor_api/__init__.py` - Package initialization

---

## 📦 Project Structure

```
IoT_Sensor_Pipeline/
├── sensor_simulator.py              # Main sensor data generator
├── sensor_api/
│   ├── app.py                       # Flask REST API (main application)
│   └── __init__.py
├── database/
│   └── schema.sql                   # PostgreSQL schema (ready-to-run)
├── sample_data/
│   ├── sample_sensor_data_normal.csv
│   ├── sample_sensor_data_warning.csv
│   └── sample_sensor_data_critical.csv
├── database_schema_week4.md         # Schema documentation
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── load_data.py                     # Data loading utility
├── quickstart.sh                    # Quick start script
└── README.md                        # Full documentation
```

---

## 🚀 Quick Start

### 1. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
# Setup PostgreSQL with TimescaleDB
psql -U postgres -d sensor_pipeline < database/schema.sql
```

### 3. Start API Server
```bash
cd sensor_api
python -m flask run
# API at http://localhost:5000
```

### 4. Run Simulator
```bash
# Batch mode
python sensor_simulator.py --mode batch --count 100

# Continuous mode with API integration
python sensor_simulator.py --mode continuous --api-endpoint http://localhost:5000/api/sensor-data
```

### 5. Load Sample Data
```bash
python load_data.py --file sample_data/sample_sensor_data_normal.csv
```

---

## 🧪 Testing

### Test API Endpoints
```bash
# Health check
curl http://localhost:5000/health

# Get latest readings
curl http://localhost:5000/api/sensor-data/latest?limit=10

# Get sensor status
curl http://localhost:5000/api/sensor-data/status

# Post single reading
curl -X POST http://localhost:5000/api/sensor-data \
  -H "Content-Type: application/json" \
  -d '{"sensor_id":"temp_1","sensor_type":"temperature","value":25.5,"unit":"C","timestamp":"2024-01-15T10:30:00Z"}'
```

### Test Database
```bash
psql -U postgres -d sensor_pipeline
SELECT COUNT(*) FROM sensor_data;
SELECT * FROM sensor_data ORDER BY time DESC LIMIT 5;
```

---

## 📊 Sensor Configuration

### Thresholds by Type

| Type | Unit | Normal | Warning | Critical |
|------|------|--------|---------|----------|
| Temperature | °C | 18-28 | 15-32 | 5-45 |
| Humidity | % | 40-70 | 30-80 | 10-95 |
| Soil Moisture | % | 30-60 | 20-70 | 5-85 |
| Light | lux | 10000-30000 | 5000-40000 | 0-50000 |

### Default Sensors (12 total)

**Locations:** greenhouse_1, field_2, storage_3

**Types per location:** temperature, humidity, soil_moisture, light

Example sensor IDs:
- `temp_1`, `humid_1`, `soil_1`, `light_1` (greenhouse_1)
- `temp_2`, `humid_2`, `soil_2`, `light_2` (field_2)
- `temp_3`, `humid_3`, `soil_3`, `light_3` (storage_3)

---

## 🔧 Configuration

Environment variables (in `.env`):

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sensor_pipeline
DB_USER=postgres
DB_PASSWORD=postgres
API_HOST=0.0.0.0
API_PORT=5000
DEBUG=False
```

---

## 📝 Dependencies

- **flask==2.3.2** - Web framework for API
- **flask-cors==4.0.0** - CORS support
- **psycopg2-binary==2.9.6** - PostgreSQL driver
- **python-dotenv==1.0.0** - Environment variables
- **requests==2.31.0** - HTTP client for simulator

---

## 🎯 Key Features

✅ **Real-time Simulation**
- Continuous sensor data generation with realistic patterns
- Configurable scenarios and thresholds

✅ **REST API**
- Single and batch data ingestion
- Status monitoring endpoints
- Connection pooling for performance

✅ **Time-Series Database**
- Hypertable optimization for fast queries
- Automatic compression for storage efficiency
- Multiple indexes for query performance

✅ **Data Quality**
- Scenario-based sample data (normal, warning, critical)
- Status tracking per reading
- Quality metrics framework

✅ **Extensibility**
- Modular design for easy feature additions
- Support for custom sensors
- Batch and streaming data ingestion

---

## 📚 Documentation

- **README.md** - Complete setup and usage guide
- **database_schema_week4.md** - Database design documentation
- **sensor_simulator.py** - Inline code documentation
- **sensor_api/app.py** - API endpoint documentation
- **load_data.py** - Data loading utility guide

---

## ✨ Highlights

1. **Production-Ready Code**
   - Comprehensive error handling
   - Logging throughout
   - Connection pooling
   - Data validation

2. **Flexible Configuration**
   - Command-line arguments
   - Environment variables
   - Configurable thresholds

3. **Complete Documentation**
   - Setup guides
   - API documentation
   - Database design
   - Usage examples

4. **Sample Data**
   - 3 scenarios with realistic values
   - CSV format for easy import
   - Multiple sensor types

---

## 🔄 Integration with Week 5

This pipeline is designed to integrate seamlessly with Week 5 components:
- RAG pipeline can query sensor context from this API
- Alert system can be built on top of this foundation
- Agent workflow will consume sensor data through this API

---

## ✅ Checklist

- [x] Sensor simulator implemented and tested
- [x] REST API with multiple endpoints
- [x] Database schema with TimescaleDB optimization
- [x] Sample data for all scenarios (normal, warning, critical)
- [x] Data loading utility
- [x] Comprehensive documentation
- [x] Requirements.txt with all dependencies
- [x] Environment configuration template
- [x] Error handling and logging
- [x] Connection pooling for performance

---

**Status:** ✅ COMPLETE - All Member 1 tasks delivered for Week 4

**Date:** January 15, 2024
**Member:** IoT/Data Engineer (Member 1)
