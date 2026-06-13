"""Unified Data Quality checker — gộp 5+1 module DQ từ Member 1 + 2."""

from collections import defaultdict
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd

from src.data_quality import MissingDataDetector, OutlierDetector
from src.data_quality.sensor_stuck import check_sensor_stuck
from src.data_quality.sensor_drift import check_sensor_drift
from src.data_quality.timestamp_delay import check_timestamp_delay

DQ_SENSOR_TYPE_MAP = {
    "temp_1": "temperature", "temp_2": "temperature",
    "hum_1": "humidity", "hum_2": "humidity",
    "soil_1": "soil_moisture", "light_1": "light",
}

CONFLICT_PAIRS = [
    ("temp_1", "temp_2", 5.0),
    ("hum_1", "hum_2", 15.0),
]

SENSOR_CATEGORY = {
    "temp_1": "temperature", "temp_2": "temperature",
    "hum_1": "humidity", "hum_2": "humidity",
    "soil_1": "soil_moisture", "light_1": "light",
}


def _resolve_sensor_type(sensor_id: str, fallback: Optional[str] = None) -> str:
    return DQ_SENSOR_TYPE_MAP.get(sensor_id, fallback or "temperature")


def _check_cross_sensor_conflicts(df: pd.DataFrame, sensor_col: str) -> List[Dict]:
    conflicts = []
    for a, b, threshold in CONFLICT_PAIRS:
        if a not in df[sensor_col].values or b not in df[sensor_col].values:
            continue
        a_data = df[df[sensor_col] == a][["value", "timestamp"]].dropna()
        b_data = df[df[sensor_col] == b][["value", "timestamp"]].dropna()
        if a_data.empty or b_data.empty:
            continue
        a_mean = a_data["value"].mean()
        b_mean = b_data["value"].mean()
        diff = abs(a_mean - b_mean)
        if diff > threshold:
            conflicts.append({
                "type": "cross_sensor_conflict",
                "sensors": [a, b],
                "values": [round(a_mean, 2), round(b_mean, 2)],
                "diff": round(diff, 2),
                "threshold": threshold,
                "count": 1,
            })
    return conflicts


def _analyze_state(issues: List[Dict]) -> Optional[str]:
    for i in issues:
        t = i["type"]
        s = i.get("sensor", "")
        cat = SENSOR_CATEGORY.get(s, "unknown")
        if t == "outlier":
            vals = [r.get("value", 0) for r in i.get("detail", []) if isinstance(r, dict)]
            if vals:
                avg_val = sum(vals) / len(vals)
            else:
                avg_val = 0
            if cat == "temperature" and avg_val > 40:
                return "temperature_high"
            if cat == "temperature" and avg_val < 10:
                return "temperature_low"
            if cat == "humidity" and avg_val > 90:
                return "humidity_high"
            if cat == "humidity" and avg_val < 30:
                return "humidity_low"
            if cat == "soil_moisture" and avg_val < 20:
                return "soil_dry"
            if cat == "light" and avg_val < 100:
                return "light_low"
            return f"{cat}_abnormal"
        if t == "sensor_stuck":
            return "sensor_fault"
        if t == "sensor_drift":
            return "sensor_degradation"
        if t == "time_gap":
            return "data_loss"
        if t == "cross_sensor_conflict":
            return "sensor_conflict"
    return None


def _build_recommendation(issue_type: Optional[str]) -> Dict:
    action_map = {
        "temperature_high":   ("turn_on_fan", 2, 15),
        "temperature_low":    ("turn_on_heater", 2, 10),
        "humidity_high":      ("turn_on_ventilation", 2, 15),
        "humidity_low":       ("turn_on_humidifier", 1, 10),
        "soil_dry":           ("start_irrigation", 3, 20),
        "light_low":          ("turn_on_grow_light", 1, 30),
        "sensor_fault":       ("check_sensor_hardware", 3, 0),
        "sensor_degradation": ("schedule_sensor_maintenance", 2, 0),
        "data_loss":          ("check_data_pipeline", 2, 0),
        "sensor_conflict":    ("verify_sensor_calibration", 2, 0),
    }
    entry = action_map.get(issue_type)
    if entry:
        return {"action": entry[0], "level": entry[1], "duration_minutes": entry[2]}
    return {}


def _needs_human_approval(issue_type: Optional[str]) -> bool:
    return issue_type in ("sensor_fault", "sensor_degradation", "sensor_conflict")


def check_all(readings: Union[List[Dict], pd.DataFrame]) -> Dict:
    if isinstance(readings, pd.DataFrame):
        df = readings
    else:
        df = pd.DataFrame(readings)
    if df.empty:
        return {"status": "pass", "issues": [], "sensor_quality_score": 1.0}

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    issues = []

    missing = MissingDataDetector()
    outlier = OutlierDetector()

    dq = missing.detect_all(df)
    if not dq["null_values"].empty:
        issues.append({"type": "missing_value", "count": len(dq["null_values"]), "detail": dq["null_values"].to_dict("records")})
    if not dq["missing_records"].empty:
        critical = dq["missing_records"][dq["missing_records"]["severity"].isin(["warning", "critical"])]
        if not critical.empty:
            issues.append({"type": "time_gap", "count": len(critical), "detail": critical.to_dict("records")})

    if "sensor" in df.columns:
        sensor_col = "sensor"
    elif "sensor_id" in df.columns:
        sensor_col = "sensor_id"
    else:
        sensor_col = None

    if sensor_col and "value" in df.columns:
        for s_id in df[sensor_col].unique():
            s_data = df[df[sensor_col] == s_id]["value"]
            if s_data.empty:
                continue
            s_type = _resolve_sensor_type(str(s_id))
            try:
                out_result = outlier.detect_all(s_data, s_type)
                flagged = out_result[out_result["is_any_outlier"]]
                if not flagged.empty:
                    issues.append({"type": "outlier", "sensor": s_id, "count": len(flagged), "detail": flagged.to_dict("records")})
            except ValueError:
                pass

    records = df.to_dict("records") if isinstance(readings, pd.DataFrame) else readings
    for s_id in df[sensor_col].unique() if sensor_col else []:
        s_records = [r for r in records if r.get(sensor_col) == s_id]
        if len(s_records) < 2:
            continue
        s_type = _resolve_sensor_type(str(s_id))
        try:
            stuck = check_sensor_stuck(s_records)
            if stuck.get("is_stuck"):
                issues.append({"type": "sensor_stuck", "sensor": s_id, **stuck})
            drift = check_sensor_drift(s_records, s_type)
            if drift.get("has_drift"):
                issues.append({"type": "sensor_drift", "sensor": s_id, **drift})
            delay = check_timestamp_delay(s_records)
            if delay.get("has_delay"):
                issues.append({"type": "timestamp_delay", "sensor": s_id, **delay})
        except Exception:
            pass

    if sensor_col:
        conflicts = _check_cross_sensor_conflicts(df, sensor_col)
        issues.extend(conflicts)

    status = "fail" if any(i["type"] in ("time_gap", "sensor_stuck", "cross_sensor_conflict") for i in issues) else "warning" if issues else "pass"
    return {"status": status, "issues": issues, "sensor_quality_score": max(0.0, 1.0 - 0.1 * len(issues)), "analyzed_state": _analyze_state(issues), "recommendation": _build_recommendation(_analyze_state(issues)), "requires_human_approval": _needs_human_approval(_analyze_state(issues))}
