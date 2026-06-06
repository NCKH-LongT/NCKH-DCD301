-- Sensor Data Pipeline Database Schema
-- Week 4: IoT/Data Engineer Task
-- For PostgreSQL with TimescaleDB

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- ============================================================================
-- Table: sensor_data (Hypertable for time-series data)
-- ============================================================================

CREATE TABLE IF NOT EXISTS sensor_data (
    id BIGSERIAL,
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

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_sensor_data_sensor_id_time 
    ON sensor_data (sensor_id, time DESC);

CREATE INDEX IF NOT EXISTS idx_sensor_data_status_time 
    ON sensor_data (status, time DESC);

CREATE INDEX IF NOT EXISTS idx_sensor_data_sensor_type_time 
    ON sensor_data (sensor_type, time DESC);

CREATE INDEX IF NOT EXISTS idx_sensor_data_location_time 
    ON sensor_data (location, time DESC);

-- ============================================================================
-- Table: sensor_devices (Device registry and configuration)
-- ============================================================================

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

CREATE INDEX IF NOT EXISTS idx_sensor_devices_type 
    ON sensor_devices(sensor_type);

CREATE INDEX IF NOT EXISTS idx_sensor_devices_location 
    ON sensor_devices(location);

-- ============================================================================
-- Table: sensor_alerts (Alert logging)
-- ============================================================================

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

CREATE INDEX IF NOT EXISTS idx_sensor_alerts_sensor_id 
    ON sensor_alerts(sensor_id);

CREATE INDEX IF NOT EXISTS idx_sensor_alerts_triggered_at 
    ON sensor_alerts(triggered_at DESC);

CREATE INDEX IF NOT EXISTS idx_sensor_alerts_is_resolved 
    ON sensor_alerts(is_resolved);

-- ============================================================================
-- Table: data_quality_metrics (Quality tracking)
-- ============================================================================

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

CREATE INDEX IF NOT EXISTS idx_data_quality_metrics_sensor_date 
    ON data_quality_metrics(sensor_id, metric_date DESC);

-- ============================================================================
-- Compression Policy for TimescaleDB (Optional)
-- ============================================================================

-- Enable compression
ALTER TABLE sensor_data SET (
    timescaledb.compress,
    timescaledb.compress_orderby = 'time DESC',
    timescaledb.compress_segmentby = 'sensor_id, location'
);

-- Add compression policy (compress data older than 7 days)
SELECT add_compression_policy('sensor_data', INTERVAL '7 days', if_not_exists => TRUE);

-- ============================================================================
-- Useful Queries for Testing
-- ============================================================================

-- Check total records
-- SELECT COUNT(*) as total_records FROM sensor_data;

-- Get latest readings
-- SELECT * FROM sensor_data ORDER BY time DESC LIMIT 10;

-- Count records by sensor
-- SELECT sensor_id, COUNT(*) as record_count FROM sensor_data GROUP BY sensor_id;

-- Status distribution
-- SELECT status, COUNT(*) as count FROM sensor_data GROUP BY status;

-- Hourly aggregates
-- SELECT 
--     time_bucket('1 hour', time) AS hour,
--     sensor_id,
--     AVG(value) AS avg_value,
--     MIN(value) AS min_value,
--     MAX(value) AS max_value
-- FROM sensor_data
-- WHERE time > NOW() - INTERVAL '24 hours'
-- GROUP BY hour, sensor_id
-- ORDER BY hour DESC;
