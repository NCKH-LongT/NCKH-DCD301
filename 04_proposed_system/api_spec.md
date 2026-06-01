# API Specification - Smart Greenhouse Agentic RAG

## Introduction

This document describes the REST API specification for the Smart Greenhouse system with Agentic RAG Framework. The API is designed to receive sensor data, perform data quality analysis, and return recommendations with explanations.

---

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, authentication is not required. Can be extended in the future with JWT.

---

## Endpoints

### 1. POST /api/sensor-data

**Description:** Receive sensor data from device or simulator and store in database.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "device_id": "greenhouse_01",
  "timestamp": "2026-05-14T10:30:00Z",
  "temperature": 34.2,
  "humidity": 78,
  "soil_moisture": 25,
  "light": 820
}
```

**Request Body Schema:**
| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| device_id | string | Yes | Device/sensor ID | max 50 chars |
| timestamp | string | Yes | Recording timestamp | ISO 8601 format |
| temperature | float | No | Temperature (°C) | -50 to 100 |
| humidity | float | No | Air humidity (%) | 0 to 100 |
| soil_moisture | float | No | Soil moisture (%) | 0 to 100 |
| light | float | No | Light intensity (lux) | >= 0 |

**Response 200 (Success):**
```json
{
  "status": "success",
  "reading_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Sensor data received and stored.",
  "timestamp": "2026-05-14T10:30:00Z"
}
```

**Response 422 (Validation Error):**
```json
{
  "status": "error",
  "error_code": "VALIDATION_ERROR",
  "message": "Missing required field: device_id",
  "details": [
    {
      "field": "device_id",
      "error": "Field required"
    }
  ]
}
```

**Response 500 (Server Error):**
```json
{
  "status": "error",
  "error_code": "INTERNAL_ERROR",
  "message": "Failed to store sensor data"
}
```

---

### 2. GET /api/sensor-data/{device_id}

**Description:** Get sensor data history by device_id.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| device_id | string | Yes | ID of device to query |

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| start_time | string | No | - | Start time (ISO 8601) |
| end_time | string | No | - | End time (ISO 8601) |
| limit | integer | No | 100 | Maximum records to return (1-1000) |

**Response 200 (Success):**
```json
{
  "status": "success",
  "device_id": "greenhouse_01",
  "readings": [
    {
      "reading_id": "550e8400-e29b-41d4-a716-446655440000",
      "timestamp": "2026-05-14T10:30:00Z",
      "temperature": 34.2,
      "humidity": 78,
      "soil_moisture": 25,
      "light": 820
    },
    {
      "reading_id": "550e8400-e29b-41d4-a716-446655440001",
      "timestamp": "2026-05-14T10:25:00Z",
      "temperature": 33.8,
      "humidity": 76,
      "soil_moisture": 26,
      "light": 810
    }
  ],
  "total": 2,
  "limit": 100
}
```

**Response 404 (Not Found):**
```json
{
  "status": "error",
  "error_code": "DEVICE_NOT_FOUND",
  "message": "No sensor data found for device_id: greenhouse_01"
}
```

---

### 3. POST /api/recommend

**Description:** Trigger agent analysis and return recommendation based on sensor data and RAG context.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body (Option A - Query by device_id):**
```json
{
  "device_id": "greenhouse_01",
  "include_history": true,
  "history_window_minutes": 30
}
```

**Request Body (Option B - Direct sensor data):**
```json
{
  "sensor_data": {
    "temperature": 34.2,
    "humidity": 78,
    "soil_moisture": 25,
    "light": 820
  },
  "timestamp": "2026-05-14T10:30:00Z"
}
```

**Request Body Schema:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| device_id | string | No* | Device ID (if no sensor_data) |
| sensor_data | object | No* | Direct sensor data |
| include_history | boolean | No | Include recent history |
| history_window_minutes | integer | No | History time window (default: 30) |

*Note: Must provide device_id OR sensor_data

**Response 200 (Success):**
```json
{
  "recommendation_id": "rec_550e8400-e29b-41d4-a716-446655440000",
  "status": "warning",
  "detected_issue": "Temperature exceeds optimal range (34.2°C > 32°C)",
  "sensor_quality_score": 0.92,
  "recommendation": {
    "action": "turn_on_fan_level_1",
    "confidence": 0.87,
    "duration_minutes": 15,
    "priority": "high"
  },
  "explanation": "The current temperature of 34.2°C exceeds the optimal range for greenhouse crops (25-32°C). Based on the retrieved knowledge base, turning on the fan at level 1 for 15 minutes is recommended to reduce temperature. The humidity level (78%) is within acceptable range.",
  "evidence": [
    {
      "source": "greenhouse_guidelines.md",
      "section": "Temperature Management",
      "relevance": 0.95,
      "content": "Optimal temperature range for most greenhouse crops is 25-32°C. When temperature exceeds 32°C, activate ventilation fans."
    },
    {
      "source": "crop_requirements.json",
      "section": "Tomato Growth Conditions",
      "relevance": 0.88,
      "content": "Tomatoes require temperature between 20-30°C for fruit development. High temperatures can cause blossom drop."
    }
  ],
  "requires_human_approval": false,
  "timestamp": "2026-05-14T10:30:05Z"
}
```

**Response 400 (Bad Request):**
```json
{
  "status": "error",
  "error_code": "INVALID_INPUT",
  "message": "Must provide either device_id or sensor_data"
}
```

**Response 422 (Validation Error):**
```json
{
  "status": "error",
  "error_code": "VALIDATION_ERROR",
  "message": "Invalid sensor value: temperature must be between -50 and 100"
}
```

**Response 500 (Server Error):**
```json
{
  "status": "error",
  "error_code": "AGENT_ERROR",
  "message": "Failed to generate recommendation"
}
```

---

### 4. GET /api/recommend/{recommendation_id}

**Description:** Get recommendation result by ID.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| recommendation_id | string | Yes | ID of recommendation to query |

**Response 200 (Success):**
```json
{
  "recommendation_id": "rec_550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "result": {
    "status": "warning",
    "detected_issue": "Temperature exceeds optimal range (34.2°C > 32°C)",
    "sensor_quality_score": 0.92,
    "recommendation": {
      "action": "turn_on_fan_level_1",
      "confidence": 0.87,
      "duration_minutes": 15,
      "priority": "high"
    },
    "explanation": "The current temperature of 34.2°C exceeds the optimal range...",
    "evidence": [...],
    "requires_human_approval": false
  },
  "created_at": "2026-05-14T10:30:05Z",
  "processing_time_ms": 1250
}
```

**Response 202 (Processing):**
```json
{
  "recommendation_id": "rec_550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "message": "Recommendation is being generated",
  "created_at": "2026-05-14T10:30:05Z"
}
```

**Response 404 (Not Found):**
```json
{
  "status": "error",
  "error_code": "RECOMMENDATION_NOT_FOUND",
  "message": "Recommendation not found: rec_550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 5. GET /api/quality-report/{device_id}

**Description:** Get latest sensor quality report for device.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| device_id | string | Yes | ID of device to query |

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| limit | integer | No | 10 | Maximum reports to return |

**Response 200 (Success):**
```json
{
  "status": "success",
  "device_id": "greenhouse_01",
  "latest_report": {
    "report_id": "qr_550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2026-05-14T10:30:00Z",
    "quality_score": 0.92,
    "overall_status": "good",
    "issues": [],
    "details": {
      "completeness": 1.0,
      "consistency": 0.95,
      "freshness": 0.85,
      "validity": 0.88
    }
  },
  "recent_reports": [
    {
      "report_id": "qr_550e8400-e29b-41d4-a716-446655440000",
      "timestamp": "2026-05-14T10:30:00Z",
      "quality_score": 0.92,
      "overall_status": "good"
    }
  ]
}
```

**Response 404 (Not Found):**
```json
{
  "status": "error",
  "error_code": "DEVICE_NOT_FOUND",
  "message": "No quality report found for device_id: greenhouse_01"
}
```

---

## Output JSON Schema (Recommendation Response)

This is the JSON output structure of the recommendation system, including **8 required fields**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "status",
    "detected_issue",
    "sensor_quality_score",
    "recommendation",
    "explanation",
    "evidence",
    "requires_human_approval"
  ],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["normal", "warning", "critical"],
      "description": "Overall system status"
    },
    "detected_issue": {
      "type": "string",
      "nullable": true,
      "description": "Detected issue (null if no issue)"
    },
    "sensor_quality_score": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Sensor data quality score (0-1)"
    },
    "recommendation": {
      "type": "object",
      "required": ["action", "confidence"],
      "properties": {
        "action": {
          "type": "string",
          "description": "Recommended action (e.g., turn_on_fan, turn_on_irrigation, alert)"
        },
        "confidence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Recommendation confidence (0-1)"
        },
        "duration_minutes": {
          "type": "integer",
          "description": "Action execution time (minutes)"
        },
        "priority": {
          "type": "string",
          "enum": ["low", "medium", "high", "critical"],
          "description": "Action priority level"
        }
      }
    },
    "explanation": {
      "type": "string",
      "description": "Natural language explanation for recommendation"
    },
    "evidence": {
      "type": "array",
      "description": "List of RAG document sources",
      "items": {
        "type": "object",
        "properties": {
          "source": {
            "type": "string",
            "description": "Source file name"
          },
          "section": {
            "type": "string",
            "description": "Section in document"
          },
          "relevance": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "Relevance score (0-1)"
          },
          "content": {
            "type": "string",
            "description": "Quoted content"
          }
        }
      }
    },
    "requires_human_approval": {
      "type": "boolean",
      "description": "Whether manual approval is required before executing action"
    }
  }
}
```

---

## HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success - Request completed successfully |
| 201 | Created - Resource created successfully |
| 202 | Accepted - Request accepted, processing in progress |
| 400 | Bad Request - Invalid input parameters |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

---

## Error Response Format

All error responses follow this format:

```json
{
  "status": "error",
  "error_code": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": [] // Optional: additional error details
}
```

---

## Rate Limiting

Currently, there is no rate limiting. Can be extended in the future.

---

## Versioning

API version: v1

Base URL: `/api/v1` (in the future)

---

## Usage Examples

### Example 1: Send sensor data

```bash
curl -X POST http://localhost:8000/api/sensor-data \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "greenhouse_01",
    "timestamp": "2026-05-14T10:30:00Z",
    "temperature": 34.2,
    "humidity": 78,
    "soil_moisture": 25,
    "light": 820
  }'
```

### Example 2: Get recommendation

```bash
curl -X POST http://localhost:8000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "greenhouse_01",
    "include_history": true,
    "history_window_minutes": 30
  }'
```

### Example 3: Get sensor history

```bash
curl "http://localhost:8000/api/sensor-data/greenhouse_01?start_time=2026-05-14T10:00:00Z&end_time=2026-05-14T10:30:00Z&limit=10"