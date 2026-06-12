"""Test sensor_stuck với dữ liệu thật từ sensor_fault.json + CSV samples."""
import os
import sys
import json
from datetime import datetime, timedelta

_PIPELINE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PIPELINE_ROOT not in sys.path:
    sys.path.insert(0, _PIPELINE_ROOT)

import pytest
from src.data_quality.sensor_stuck import (
    SensorReading,
    SensorStuckDetector,
    check_sensor_stuck,
)

WEEK4_NTB = os.path.join(
    _PIPELINE_ROOT, "..", "..", "docs", "weekly", "week-task", "week4-file", "W4-ntb"
)


def load_fault_scenarios():
    path = os.path.join(WEEK4_NTB, "sensor_fault.json")
    with open(path) as f:
        return json.load(f)


def make_readings_from_sequence(seq: list[dict], sensor_id: str, sensor_key: str):
    readings = []
    for entry in seq:
        readings.append({
            "sensor_id": sensor_id,
            "value": entry["sensors"][sensor_key],
            "timestamp": datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00")),
        })
    return readings


class TestSensorStuckWithFaultData:
    """Dùng stuck_humidity_sensor scenario từ sensor_fault.json (humidity stuck 61.345 qua 5 readings)."""

    @pytest.fixture(scope="class")
    def stuck_scenario(self):
        scenarios = load_fault_scenarios()
        return [s for s in scenarios if s["scenario_name"] == "stuck_humidity_sensor"][0]

    @pytest.fixture
    def stuck_readings(self, stuck_scenario):
        return make_readings_from_sequence(
            stuck_scenario["data_sequence"],
            sensor_id="humid_1",
            sensor_key="humidity",
        )

    def test_detect_stuck_with_low_threshold(self, stuck_readings):
        result = check_sensor_stuck(stuck_readings, stuck_threshold_minutes=1)
        assert result["is_stuck"] is True
        assert result["sensor_id"] == "humid_1"
        assert result["current_value"] == 61.345
        assert result["duration_minutes"] >= 4.0

    def test_no_stuck_with_high_threshold(self, stuck_readings):
        result = check_sensor_stuck(stuck_readings, stuck_threshold_minutes=60)
        assert result["is_stuck"] is False

    def test_stuck_detector_class_no_threshold(self, stuck_readings):
        detector = SensorStuckDetector(stuck_threshold_minutes=1)
        assert detector.is_stuck([]) == (False, None)
        assert detector.is_stuck([SensorReading("a", 10, datetime.now())]) == (False, None)


class TestSensorStuckWithNormalCSV:
    """Dùng sample_sensor_data_normal.csv — sensor temp_1 thay đổi giá trị qua các reading."""

    @pytest.fixture
    def normal_temp_readings(self):
        raw = [
            ("temp_1", 22.5, "2024-01-15T09:00:00Z"),
            ("temp_1", 23.1, "2024-01-15T09:05:00Z"),
        ]
        return [
            {"sensor_id": sid, "value": v, "timestamp": datetime.fromisoformat(ts.replace("Z", "+00:00"))}
            for sid, v, ts in raw
        ]

    def test_no_stuck_different_values(self, normal_temp_readings):
        """Values different (22.5→23.1) nhưng giá trị cũ là 22.5 ở 09:00, nên duration từ lần cuối khác = 5 phút.
        Dùng threshold > 5 để tránh stuck."""
        result = check_sensor_stuck(normal_temp_readings, stuck_threshold_minutes=10)
        assert result["is_stuck"] is False


class TestSensorStuckBoundary:
    """Edge cases."""

    def test_single_reading(self):
        now = datetime.now()
        readings = [{"sensor_id": "t1", "value": 25.0, "timestamp": now}]
        res = check_sensor_stuck(readings)
        assert res["is_stuck"] is False

    def test_empty_readings(self):
        result = check_sensor_stuck([])
        assert result["is_stuck"] is False
        assert "error" in result

    def test_exact_threshold(self):
        now = datetime.now()
        readings = [
            {"sensor_id": "t1", "value": 25.0, "timestamp": now - timedelta(minutes=10)},
            {"sensor_id": "t1", "value": 25.0, "timestamp": now},
        ]
        res = check_sensor_stuck(readings, stuck_threshold_minutes=10)
        assert res["is_stuck"] is True

    def test_below_threshold(self):
        now = datetime.now()
        readings = [
            {"sensor_id": "t1", "value": 25.0, "timestamp": now - timedelta(minutes=9)},
            {"sensor_id": "t1", "value": 25.0, "timestamp": now},
        ]
        res = check_sensor_stuck(readings, stuck_threshold_minutes=10)
        assert res["is_stuck"] is False
