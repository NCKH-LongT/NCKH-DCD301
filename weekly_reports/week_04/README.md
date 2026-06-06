# Sensor Data Pipeline - Week 4 Setup Guide

## Project Structure

```
IoT_Sensor_Pipeline/
├── sensor_simulator.py          # Sensor data generator
├── sensor_api/
│   ├── app.py                   # Flask REST API
│   └── __init__.py
├── database/
│   └── schema.sql               # Database schema
├── sample_data/
│   ├── sample_sensor_data_normal.csv
│   ├── sample_sensor_data_warning.csv
│   └── sample_sensor_data_critical.csv
├── database_schema_week4.md     # Schema documentation
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

---

## Prerequisites

- **Python 3.8+**
- **PostgreSQL 12+** (or use Docker)
- **TimescaleDB extension** (optional but recommended for time-series)

---

## Quick Start

### 1. Setup Database (PostgreSQL + TimescaleDB)

#### Option A: Using Docker (Recommended)

```bash
# Run PostgreSQL with TimescaleDB
docker run -d \
  --name timescaledb \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  timescale/timescaledb:latest-pg14

# Wait for container to be ready
sleep 5

# Connect and create database
docker exec -it timescaledb psql -U postgres -c "CREATE DATABASE sensor_pipeline;"
```

#### Option B: Manual Installation

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib timescaledb-postgresql-14

# macOS
brew install postgresql
brew install timescaledb

# Start PostgreSQL service
sudo systemctl start postgresql  # Linux
brew services start postgresql  # macOS

# Create database
createdb sensor_pipeline
```

### 2. Initialize Database Schema

```bash
# Connect to database and run schema
psql -U postgres -d sensor_pipeline << EOF

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create sensor_data table
CREATE TABLE IF NOT EXISTS sensor_data (
    id BIGSERIAL PRIMARY KEY,
    time TIMESTAMPTZ NOT NULL,
    sensor_id VARCHAR(50) NOT NULL,
    sensor_name VARCHAR(100),
    sensor_type VARCHAR(50) NOT NULL,
    value FLOAT NOT NULL,
    unit VARCHAR(20),
    status VARCHAR(20) DEFAULT 'normal',
    location VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Convert to hypertable
SELECT create_hypertable('sensor_data', 'time', if_not_exists => TRUE);

-- Create indexes
CREATE INDEX idx_sensor_data_sensor_id_time ON sensor_data (sensor_id, time DESC);
CREATE INDEX idx_sensor_data_status_time ON sensor_data (status, time DESC);

-- Create sensor_devices table
CREATE TABLE IF NOT EXISTS sensor_devices (
    sensor_id VARCHAR(50) PRIMARY KEY,
    sensor_name VARCHAR(100) NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,
    location VARCHAR(100),
    unit VARCHAR(20),
    min_threshold FLOAT,
    max_threshold FLOAT,
    critical_min FLOAT,
    critical_max FLOAT,
    is_active BOOLEAN DEFAULT TRUE,
    last_reading_time TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create sensor_alerts table
CREATE TABLE IF NOT EXISTS sensor_alerts (
    id BIGSERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL REFERENCES sensor_devices(sensor_id),
    alert_type VARCHAR(50),
    alert_message TEXT,
    triggered_at TIMESTAMPTZ NOT NULL,
    resolved_at TIMESTAMPTZ,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create data_quality_metrics table
CREATE TABLE IF NOT EXISTS data_quality_metrics (
    id BIGSERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    metric_date DATE NOT NULL,
    total_records INT,
    missing_values INT,
    outliers INT,
    quality_score FLOAT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

EOF
```

### 3. Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example .env
cp .env.example .env

# Edit .env with your database credentials
# Default values should work if using local PostgreSQL
```

### 5. Start the API Server

```bash
# In terminal 1:
cd sensor_api
python -m flask run
# API will be available at http://localhost:5000
```

### 6. Run Sensor Simulator (In another terminal)

```bash
# Generate batch of 50 readings
python sensor_simulator.py --mode batch --count 50

# Or run continuous simulation
python sensor_simulator.py --mode continuous --interval 5 --api-endpoint http://localhost:5000/api/sensor-data

# Generate specific scenario data
python sensor_simulator.py --mode batch --count 100 --scenario normal --output-file normal_data.jsonl
```

---

## API Endpoints

### 1. Receive Single Sensor Reading
```bash
curl -X POST http://localhost:5000/api/sensor-data \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "temp_1",
    "sensor_name": "Temperature Sensor 1",
    "sensor_type": "temperature",
    "value": 25.5,
    "unit": "C",
    "status": "normal",
    "location": "greenhouse_1",
    "timestamp": "2024-01-15T10:30:00Z",
    "metadata": {"quality_flag": "ok"}
  }'
```

### 2. Receive Batch of Readings
```bash
curl -X POST http://localhost:5000/api/sensor-data/batch \
  -H "Content-Type: application/json" \
  -d '[
    {"sensor_id": "temp_1", ...},
    {"sensor_id": "humid_1", ...}
  ]'
```

### 3. Get Latest Readings
```bash
curl http://localhost:5000/api/sensor-data/latest?limit=10
```

### 4. Get Sensor Status
```bash
curl http://localhost:5000/api/sensor-data/status
```

### 5. Health Check
```bash
curl http://localhost:5000/health
```

---

## Sample Data

The pipeline includes sample data for three scenarios:

### Normal Data
```bash
cat sample_data/sample_sensor_data_normal.csv
```
- Temperature: 19-24°C
- Humidity: 40-70%
- Soil Moisture: 30-60%
- Light: 10000-30000 lux

### Warning Data
```bash
cat sample_data/sample_sensor_data_warning.csv
```
- Temperature: 14-34°C
- Humidity: 30-85%
- Soil Moisture: 20-75%
- Light: 4500-42000 lux

### Critical Data
```bash
cat sample_data/sample_sensor_data_critical.csv
```
- Temperature: 3-48°C
- Humidity: 92-97%
- Soil Moisture: 2-90%
- Light: 50-49500 lux

---

## Loading Sample Data into Database

### Using psql COPY

```bash
# Connect to database and import CSV
psql -U postgres -d sensor_pipeline << EOF

-- Convert CSV to sensor_data table format
COPY sensor_data (time, sensor_id, sensor_name, sensor_type, value, unit, status, location)
FROM PROGRAM 'cat sample_data/sample_sensor_data_normal.csv | tail -n +2'
WITH (FORMAT csv, DELIMITER ',');

EOF
```

### Using Python Script

```python
import pandas as pd
import psycopg2

# Read CSV
df = pd.read_csv('sample_data/sample_sensor_data_normal.csv')

# Connect and insert
conn = psycopg2.connect("dbname=sensor_pipeline user=postgres password=postgres")
cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO sensor_data (time, sensor_id, sensor_name, sensor_type, value, unit, status, location)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['timestamp'], row['sensor_id'], row['sensor_name'], row['sensor_type'], 
          row['value'], row['unit'], row['status'], row['location']))

conn.commit()
cursor.close()
conn.close()
```

---

## Testing

### Test API with cURL

```bash
# Test health check
curl http://localhost:5000/health

# Test single sensor data submission
curl -X POST http://localhost:5000/api/sensor-data \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "test_sensor",
    "sensor_type": "temperature",
    "value": 25.5,
    "unit": "C",
    "timestamp": "2024-01-15T10:30:00Z"
  }'

# Test batch submission
curl -X POST http://localhost:5000/api/sensor-data/batch \
  -H "Content-Type: application/json" \
  -d "[
    {\"sensor_id\": \"temp_1\", \"sensor_type\": \"temperature\", \"value\": 22.5, \"unit\": \"C\", \"timestamp\": \"2024-01-15T10:30:00Z\"},
    {\"sensor_id\": \"humid_1\", \"sensor_type\": \"humidity\", \"value\": 65.0, \"unit\": \"%\", \"timestamp\": \"2024-01-15T10:30:00Z\"}
  ]"
```

### Test Database Query

```bash
psql -U postgres -d sensor_pipeline << EOF

-- Check total records
SELECT COUNT(*) FROM sensor_data;

-- Check latest readings
SELECT * FROM sensor_data ORDER BY time DESC LIMIT 5;

-- Check records by sensor
SELECT sensor_id, COUNT(*) as count FROM sensor_data GROUP BY sensor_id;

-- Check status distribution
SELECT status, COUNT(*) as count FROM sensor_data GROUP BY status;

EOF
```

---

## Troubleshooting

### Database Connection Failed
```
Error: could not connect to server: Connection refused
```
**Solution:** Ensure PostgreSQL is running:
```bash
# Check status
sudo systemctl status postgresql  # Linux
brew services list | grep postgresql  # macOS

# Start if not running
sudo systemctl start postgresql
```

### Port 5000 Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process or use different port
export API_PORT=5001
```

### Schema Error with TimescaleDB

```
ERROR: extension "timescaledb" does not exist
```
**Solution:** Install TimescaleDB or remove the extension creation from schema.

---

## Key Components

### sensor_simulator.py
- Generates realistic sensor data with time-series characteristics
- Supports different scenarios (normal, warning, critical)
- Can send data directly to API
- Exports to JSONL/CSV format

### sensor_api/app.py
- Flask REST API for receiving sensor data
- PostgreSQL integration with connection pooling
- Batch and single record endpoints
- Status monitoring endpoints

### Database Schema
- Hypertable for time-series optimization
- Multiple indexes for query performance
- Alert and metrics tracking tables
- Compression policies for long-term storage

---

## Next Steps (Week 5)

1. Add data validation and anomaly detection
2. Implement alert triggering rules
3. Create data quality metrics calculation
4. Integrate with RAG pipeline for intelligent queries
5. Add Web UI dashboard for monitoring

---

## Configuration Reference

| Variable | Default | Description |
|----------|---------|-------------|
| DB_HOST | localhost | PostgreSQL host |
| DB_PORT | 5432 | PostgreSQL port |
| DB_NAME | sensor_pipeline | Database name |
| DB_USER | postgres | Database user |
| DB_PASSWORD | postgres | Database password |
| API_HOST | 0.0.0.0 | API server host |
| API_PORT | 5000 | API server port |
| DEBUG | False | Flask debug mode |

---

## Support

For issues or questions:
1. Check database connection: `psql -U postgres -d sensor_pipeline -c "SELECT 1;"`
2. Verify API health: `curl http://localhost:5000/health`
3. Check logs in application output
4. Review database_schema_week4.md for schema details
