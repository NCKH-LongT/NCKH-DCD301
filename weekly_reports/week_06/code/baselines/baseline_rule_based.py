"""
baseline_rule_based.py — Rule-based Baseline for Greenhouse Monitoring

Compares sensor values against predefined thresholds using if-else logic,
outputs status, recommended actions, and confidence scores.

Output JSON format:
{
    "status": "pass" | "warning" | "critical",
    "sensor_readings": [ ... ],
    "overall_assessment": { ... },
    "recommendations": [ ... ],
    "timestamp": "..."
}
"""

import csv
import json
import os
import sys
import warnings
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# DEFAULT FIELD MAPPING — remap if your project uses different
# column names than the expected internal field names.
# ============================================================
# Usage:
#   process_readings(data, field_mapping={"sensor_id": "id", "value": "temperature"})

DEFAULT_FIELD_MAP: Dict[str, str] = {
    "sensor_id": "sensor_id",
    "sensor_type": "sensor_type",
    "value": "value",
    "location": "location",
    "timestamp": "timestamp",
}

REQUIRED_FIELDS = ["value"]
OPTIONAL_FIELDS_WITH_DEFAULTS = {
    "sensor_id": "unknown",
    "sensor_type": "unknown",
    "location": "unknown",
    "timestamp": "",
}


# ============================================================
# 1. DEFINE THRESHOLDS FOR EACH SENSOR TYPE
# ============================================================
# Each threshold has: (critical_low, warning_low, warning_high, critical_high)
# Values between warning_low and warning_high are considered "normal"

THRESHOLDS = {
    "temperature": {
        "critical_low": 10.0,
        "warning_low": 15.0,
        "warning_high": 35.0,
        "critical_high": 40.0,
        "unit": "°C",
    },
    "humidity": {
        "critical_low": 30.0,
        "warning_low": 40.0,
        "warning_high": 70.0,
        "critical_high": 85.0,
        "unit": "%",
    },
    "soil_moisture": {
        "critical_low": 20.0,
        "warning_low": 30.0,
        "warning_high": 70.0,
        "critical_high": 85.0,
        "unit": "%",
    },
    "light": {
        "critical_low": 500.0,
        "warning_low": 2000.0,
        "warning_high": 30000.0,
        "critical_high": 45000.0,
        "unit": "lux",
    },
}

# Map sensor_type → display name
SENSOR_DISPLAY = {
    "temperature": "Temperature",
    "humidity": "Humidity",
    "soil_moisture": "Soil Moisture",
    "light": "Light",
}

# Recommended actions mapped by sensor type and threshold zone
ACTIONS = {
    "temperature": {
        "critical_low": {"action": "turn_on_heater", "level": 3, "duration_minutes": 30, "detail": "Temperature critically low — turn on heater"},
        "warning_low": {"action": "turn_on_heater", "level": 1, "duration_minutes": 15, "detail": "Temperature low — turn on heater at low power"},
        "warning_high": {"action": "turn_on_fan", "level": 1, "duration_minutes": 15, "detail": "Temperature high — turn on ventilation fan"},
        "critical_high": {"action": "turn_on_fan_and_mist", "level": 3, "duration_minutes": 30, "detail": "Temperature critically high — turn on fan + mist cooling"},
    },
    "humidity": {
        "critical_low": {"action": "turn_on_humidifier", "level": 3, "duration_minutes": 30, "detail": "Humidity critically low — turn on humidifier"},
        "warning_low": {"action": "turn_on_humidifier", "level": 1, "duration_minutes": 15, "detail": "Humidity low — turn on humidifier at low power"},
        "warning_high": {"action": "turn_on_ventilation", "level": 1, "duration_minutes": 15, "detail": "Humidity high — turn on ventilation system"},
        "critical_high": {"action": "turn_on_ventilation_and_dehumidifier", "level": 3, "duration_minutes": 30, "detail": "Humidity critically high — turn on ventilation + dehumidifier"},
    },
    "soil_moisture": {
        "critical_low": {"action": "start_irrigation", "level": 3, "duration_minutes": 20, "detail": "Soil critically dry — start irrigation"},
        "warning_low": {"action": "start_irrigation", "level": 1, "duration_minutes": 10, "detail": "Soil dry — light irrigation"},
        "warning_high": {"action": "stop_irrigation", "level": 1, "duration_minutes": 0, "detail": "Soil moisture high — stop irrigation"},
        "critical_high": {"action": "stop_irrigation_and_check_drainage", "level": 3, "duration_minutes": 0, "detail": "Soil moisture critically high — stop irrigation, check drainage"},
    },
    "light": {
        "critical_low": {"action": "turn_on_grow_light", "level": 3, "duration_minutes": 60, "detail": "Light critically low — turn on grow lights"},
        "warning_low": {"action": "turn_on_grow_light", "level": 1, "duration_minutes": 30, "detail": "Light low — turn on supplemental lights"},
        "warning_high": {"action": "lower_shade_curtain", "level": 1, "duration_minutes": 0, "detail": "Light high — lower shade curtain"},
        "critical_high": {"action": "lower_shade_curtain_and_monitor", "level": 3, "duration_minutes": 0, "detail": "Light critically high — lower shade curtain + monitor temperature"},
    },
}

# Priority levels for aggregating overall status
STATUS_PRIORITY = {"pass": 0, "warning": 1, "critical": 2}


# ============================================================
# 2. PER-SENSOR EVALUATION FUNCTIONS
# ============================================================

def evaluate_sensor(sensor_type: str, value: float) -> Tuple[str, str, float]:
    """
    Evaluate a single sensor value against predefined thresholds.
    Returns: (status, zone, confidence)
      - status: "pass" | "warning" | "critical"
      - zone: zone name for action lookup (e.g. "critical_low", "warning_high", ...)
      - confidence: confidence score (0.0 - 1.0)
    """
    th = THRESHOLDS.get(sensor_type)
    if not th:
        return ("pass", "normal", 0.5)

    if value <= th["critical_low"]:
        return ("critical", "critical_low", 0.95)
    elif value <= th["warning_low"]:
        return ("warning", "warning_low", 0.75)
    elif value <= th["warning_high"]:
        return ("pass", "normal", 0.90)
    elif value <= th["critical_high"]:
        return ("warning", "warning_high", 0.75)
    else:
        return ("critical", "critical_high", 0.95)


def get_recommendation(sensor_type: str, zone: str) -> Dict:
    """Get recommended action based on sensor type and threshold zone."""
    if zone == "normal":
        return {}
    sensor_actions = ACTIONS.get(sensor_type, {})
    return sensor_actions.get(zone, {})


def get_confidence(sensor_type: str, value: float, status: str) -> float:
    """
    Compute confidence score based on:
    - Severity level (critical > warning)
    - Distance from threshold (further from threshold = more confident)
    """
    th = THRESHOLDS.get(sensor_type)
    if not th:
        return 0.5

    if status == "pass":
        # Near midpoint of normal range → higher confidence
        mid = (th["warning_low"] + th["warning_high"]) / 2
        dist = abs(value - mid) / (th["warning_high"] - th["warning_low"])
        return round(min(0.95, 0.7 + dist * 0.25), 4)
    elif status == "warning":
        # Near critical threshold → higher confidence
        if value <= th["warning_low"]:
            ratio = (th["warning_low"] - value) / (th["warning_low"] - th["critical_low"] + 0.001)
        else:
            ratio = (value - th["warning_high"]) / (th["critical_high"] - th["warning_high"] + 0.001)
        return round(min(0.90, 0.6 + ratio * 0.3), 4)
    else:  # critical
        if value <= th["critical_low"]:
            ratio = (th["critical_low"] - value) / (th["critical_low"] + 0.001)
        else:
            ratio = (value - th["critical_high"]) / (th["critical_high"] + 0.001)
        return round(min(0.99, 0.85 + ratio * 0.14), 4)


# ============================================================
# 3. CSV DATA PROCESSING
# ============================================================

def read_sensor_data(
    filepath: str,
    field_mapping: Optional[Dict[str, str]] = None,
) -> List[Dict]:
    """
    Read sensor CSV file and return a list of dicts.

    Parameters
    ----------
    filepath : str
        Path to the CSV file.
    field_mapping : dict, optional
        Maps internal field names to CSV column names.
        E.g. {"sensor_id": "ID", "value": "temperature"}.

    Returns
    -------
    List[Dict]
        List of sensor records with internal field names.
    """
    mapping = {**DEFAULT_FIELD_MAP, **(field_mapping or {})}
    # Build reverse mapping: CSV column → internal name
    reverse_map = {v: k for k, v in mapping.items()}

    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_num, raw in enumerate(reader, start=2):  # header = line 1
            record = {}
            for csv_col, val in raw.items():
                internal = reverse_map.get(csv_col, csv_col)
                record[internal] = val

            # Convert value to float
            raw_val = record.get("value")
            if raw_val is None or str(raw_val).strip() == "":
                raise ValueError(
                    f"Line {row_num}: missing required field 'value'. "
                    f"Available CSV columns: {list(raw.keys())}"
                )
            try:
                record["value"] = float(raw_val)
            except (ValueError, TypeError):
                raise ValueError(
                    f"Line {row_num}: 'value' is not a valid number: {raw_val!r}"
                )

            records.append(record)

    return records


def _resolve_field(record: Dict, field: str, default: Any = None) -> Any:
    """Get a field from a record, falling back to default if missing."""
    val = record.get(field)
    if val is None or (isinstance(val, str) and val.strip() == ""):
        return default
    return val


def _validate_record(record: Dict, index: int) -> None:
    """Validate a single sensor record and raise on fatal issues."""
    # Check required fields exist
    for field in REQUIRED_FIELDS:
        val = record.get(field)
        if val is None:
            raise ValueError(
                f"Record #{index}: missing required field '{field}'. "
                f"Available keys: {list(record.keys())}. "
                "Use field_mapping to remap your column names."
            )

    # Validate value is numeric
    val = record.get("value")
    if not isinstance(val, (int, float)):
        raise ValueError(
            f"Record #{index}: 'value' must be numeric, got {type(val).__name__}: {val!r}"
        )

    # Warn on unknown sensor_type
    sensor_type = record.get("sensor_type", "unknown")
    if sensor_type not in THRESHOLDS and sensor_type != "unknown":
        warnings.warn(
            f"Record #{index}: unknown sensor_type '{sensor_type}'. "
            f"Known types: {list(THRESHOLDS.keys())}. "
            "Falling back to default thresholds."
        )


def process_readings(
    records: List[Dict],
    field_mapping: Optional[Dict[str, str]] = None,
    skip_errors: bool = False,
) -> Dict[str, Any]:
    """
    Process all sensor readings and return aggregated results.

    Parameters
    ----------
    records : List[Dict]
        List of sensor reading dicts with fields matching DEFAULT_FIELD_MAP.
    field_mapping : dict, optional
        Maps internal field names to your custom field names.
        E.g. {"value": "temperature", "sensor_id": "id"}.
    skip_errors : bool, default=False
        If True, skip invalid records instead of raising.

    Returns
    -------
    Dict[str, Any]
        Aggregated result with status, readings, recommendations.
    """
    mapping = {**DEFAULT_FIELD_MAP, **(field_mapping or {})}
    sensor_results = []

    for idx, raw in enumerate(records):
        # Remap fields using user-provided mapping
        rec = {}
        for internal, external in mapping.items():
            rec[internal] = raw.get(external, raw.get(internal))

        # Also copy any unmapped fields through
        for k, v in raw.items():
            if k not in rec:
                rec[k] = v

        # Validate
        try:
            _validate_record(rec, idx)
        except (ValueError, TypeError) as e:
            if skip_errors:
                warnings.warn(f"Skipping record #{idx}: {e}")
                continue
            raise

        sensor_id = _resolve_field(rec, "sensor_id", "unknown")
        sensor_type = _resolve_field(rec, "sensor_type", "unknown")
        value = rec["value"]  # guaranteed by _validate_record
        location = _resolve_field(rec, "location", "unknown")
        timestamp = _resolve_field(rec, "timestamp", "")

        status, zone, base_conf = evaluate_sensor(sensor_type, value)
        confidence = get_confidence(sensor_type, value, status)
        recommendation = get_recommendation(sensor_type, zone)

        sensor_results.append({
            "sensor_id": sensor_id,
            "sensor_type": sensor_type,
            "sensor_name": SENSOR_DISPLAY.get(sensor_type, sensor_type),
            "location": location,
            "value": value,
            "unit": THRESHOLDS.get(sensor_type, {}).get("unit", ""),
            "timestamp": timestamp,
            "status": status,
            "confidence": confidence,
            "recommendation": recommendation,
        })

    # Aggregate overall status
    if not sensor_results:
        overall_status = "pass"
    else:
        max_priority = max(STATUS_PRIORITY.get(r["status"], 0) for r in sensor_results)
        overall_status = {0: "pass", 1: "warning", 2: "critical"}.get(max_priority, "pass")

    # Aggregate all recommendations
    recommendations = []
    for r in sensor_results:
        if r["recommendation"]:
            recommendations.append({
                "sensor_id": r["sensor_id"],
                "sensor_name": r["sensor_name"],
                "location": r["location"],
                "status": r["status"],
                "value": r["value"],
                "unit": r["unit"],
                "threshold": THRESHOLDS.get(r["sensor_type"], {}),
                "action": r["recommendation"]["action"],
                "level": r["recommendation"]["level"],
                "duration_minutes": r["recommendation"]["duration_minutes"],
                "detail": r["recommendation"]["detail"],
            })

    # Compute overall confidence score
    if sensor_results:
        overall_confidence = round(
            sum(r["confidence"] for r in sensor_results) / len(sensor_results), 4
        )
    else:
        overall_confidence = 1.0

    # Determine if human approval is needed
    requires_human_approval = any(
        r["status"] == "critical" for r in sensor_results
    )

    return {
        "status": overall_status,
        "overall_confidence": overall_confidence,
        "requires_human_approval": requires_human_approval,
        "sensor_readings": sensor_results,
        "recommendations": recommendations,
        "total_sensors": len(sensor_results),
        "summary": {
            "pass": sum(1 for r in sensor_results if r["status"] == "pass"),
            "warning": sum(1 for r in sensor_results if r["status"] == "warning"),
            "critical": sum(1 for r in sensor_results if r["status"] == "critical"),
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================
# 4. CLI — RUN FROM TERMINAL
# ============================================================

def main():
    """Entry point: read CSV file and print JSON result."""
    if len(sys.argv) < 2:
        print("Usage: python baseline_rule_based.py <path_to_csv>")
        print("Example: python baseline_rule_based.py sample_sensor_data_normal.csv")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    records = read_sensor_data(filepath)
    result = process_readings(records)

    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
