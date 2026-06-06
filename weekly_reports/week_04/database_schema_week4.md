# Sensor Data Pipeline - Database Schema (Week 4)

## Database Choice: PostgreSQL with TimescaleDB Extension

We use PostgreSQL with TimescaleDB for time-series data optimization, as it's ideal for handling high-volume sensor data with efficient compression and querying.

---

## Schema Design

### 1. Hypertable: `sensor_data` (Time-Series Data)

This is the main table storing all sensor readings. It's converted to a hypertable for optimized time-series operations.

```sql
-- Create the base sensor_data table
CREATE TABLE IF NOT EXISTS sensor_data (
    id BIGSERIAL PRIMARY KEY,
    time TIMESTAMPTZ NOT NULL,
    sensor_id VARCHAR(50) NOT NULL,
    sensor_name VARCHAR(100),
    sensor_type VARCHAR(50) NOT NULL,  -- 'temperature', 'humidity', 'soil_moisture', 'light'
    value FLOAT NOT NULL,
    unit VARCHAR(20),  -- 'C', '%', 'lux', etc.
    status VARCHAR(20) DEFAULT 'normal',  -- 'normal', 'warning', 'critical'
    location VARCHAR(100),  -- e.g., 'greenhouse_1', 'field_2'
    metadata JSONB,  -- Additional sensor info as JSON
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Convert to hypertable (must be done after table creation)
SELECT create_hypertable('sensor_data', 'time', if_not_exists => TRUE);

-- Create indexes for common queries
CREATE INDEX idx_sensor_data_sensor_id_time ON sensor_data (sensor_id, time DESC);
CREATE INDEX idx_sensor_data_status_time ON sensor_data (status, time DESC);
CREATE INDEX idx_sensor_data_sensor_type_time ON sensor_data (sensor_type, time DESC);
CREATE INDEX idx_sensor_data_location_time ON sensor_data (location, time DESC);
```

---

### 2. Table: `sensor_devices` (Device Registry)

Stores metadata about physical sensors.

```sql
CREATE TABLE IF NOT EXISTS sensor_devices (
    sensor_id VARCHAR(50) PRIMARY KEY,
    sensor_name VARCHAR(100) NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,  -- 'temperature', 'humidity', 'soil_moisture', 'light'
    location VARCHAR(100),
    unit VARCHAR(20),
    min_threshold FLOAT,  -- Warning threshold
    max_threshold FLOAT,  -- Warning threshold
    critical_min FLOAT,  -- Critical threshold
    critical_max FLOAT,  -- Critical threshold
    is_active BOOLEAN DEFAULT TRUE,
    last_reading_time TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sensor_devices_type ON sensor_devices(sensor_type);
CREATE INDEX idx_sensor_devices_location ON sensor_devices(location);
```

---

### 3. Table: `sensor_alerts` (Alert Log)

Stores triggered alerts for monitoring.

```sql
CREATE TABLE IF NOT EXISTS sensor_alerts (
    id BIGSERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL REFERENCES sensor_devices(sensor_id),
    alert_type VARCHAR(50),  -- 'warning', 'critical', 'offline'
    alert_message TEXT,
    triggered_at TIMESTAMPTZ NOT NULL,
    resolved_at TIMESTAMPTZ,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensor_devices(sensor_id)
);

CREATE INDEX idx_sensor_alerts_sensor_id ON sensor_alerts(sensor_id);
CREATE INDEX idx_sensor_alerts_triggered_at ON sensor_alerts(triggered_at DESC);
CREATE INDEX idx_sensor_alerts_is_resolved ON sensor_alerts(is_resolved);
```

---

### 4. Table: `data_quality_metrics` (Quality Tracking)

Tracks data quality metrics for validation.

```sql
CREATE TABLE IF NOT EXISTS data_quality_metrics (
    id BIGSERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    metric_date DATE NOT NULL,
    total_records INT,
    missing_values INT,
    outliers INT,
    quality_score FLOAT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensor_devices(sensor_id)
);

CREATE INDEX idx_data_quality_metrics_sensor_date ON data_quality_metrics(sensor_id, metric_date DESC);
```

---

## Setup Instructions

### 1. Install PostgreSQL and TimescaleDB

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install timescaledb-postgresql-12  # Replace 12 with your PG version

# macOS (using Homebrew)
brew install postgresql
brew install timescaledb
```

### 2. Create Extension and Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create extension in your database
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

# Create database for sensor data
CREATE DATABASE sensor_pipeline;
```

### 3. Run Schema SQL

```bash
psql -U postgres -d sensor_pipeline -f database_schema_week4.sql
```

---

## Data Retention Policy

For long-term data storage with compression:

```sql
-- Enable compression for data older than 7 days
ALTER TABLE sensor_data SET (
    timescaledb.compress,
    timescaledb.compress_orderby = 'time DESC',
    timescaledb.compress_segmentby = 'sensor_id, location'
);

-- Compress data older than 7 days every day
SELECT add_compression_policy('sensor_data', INTERVAL '7 days', if_not_exists => TRUE);

-- Optional: Set data retention (e.g., keep last 90 days raw, compress older)
SELECT add_retention_policy('sensor_data', INTERVAL '90 days', if_not_exists => TRUE);
```

---

## Query Examples

### Recent Sensor Data
```sql
SELECT * FROM sensor_data 
WHERE sensor_id = 'temp_sensor_01' 
ORDER BY time DESC 
LIMIT 100;
```

### Aggregated Data (1-hour average)
```sql
SELECT 
    time_bucket('1 hour', time) AS hour,
    sensor_id,
    AVG(value) AS avg_value,
    MIN(value) AS min_value,
    MAX(value) AS max_value
FROM sensor_data
WHERE sensor_type = 'temperature' AND time > NOW() - INTERVAL '7 days'
GROUP BY hour, sensor_id
ORDER BY hour DESC;
```

### Active Alerts
```sql
SELECT * FROM sensor_alerts
WHERE is_resolved = FALSE
ORDER BY triggered_at DESC;
```

---

## Performance Tuning

- **Hypertables**: Automatically partition data by time for faster queries
- **Compression**: Reduces storage by 80-95% for older data
- **Indexes**: Optimized for time-series queries by sensor_id and time
- **Continuous Aggregates**: Can be created for real-time dashboards

---

## Migration from Other DBs

If migrating from MongoDB or other systems:
- Export data as CSV
- Use `COPY` command to bulk insert
- Validate row counts and data integrity post-migration
