"""Test sensor_drift với dữ liệu thật từ sensor_fault.json + CSV samples."""
import os
import sys
import json
from datetime import datetime, timedelta

_PIPELINE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PIPELINE_ROOT not in sys.path:
    sys.path.insert(0, _PIPELINE_ROOT)

import pytest
from src.data_quality.sensor_drift import SensorDriftDetector, check_sensor_drift

WEEK4_NTB = os.path.join(
    _PIPELINE_ROOT, "..", "..", "docs", "weekly", "week-task", "week4-file", "W4-ntb"
)


def load_fault_scenarios():
    path = os.path.join(WEEK4_NTB, "sensor_fault.json")
    with open(path) as f:
        return json.load(f)


def make_readings(seq, sensor_id, sensor_key):
    readings = []
    for entry in seq:
        readings.append({
            "sensor_id": sensor_id,
            "value": entry["sensors"][sensor_key],
            "timestamp": datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00")),
        })
    return readings


class TestSensorDriftErraticSoil:
    """Dùng erratic_soil_moisture — soil moisture nhảy 50→15→95→20 trong 4 phút = drift cực mạnh."""

    @pytest.fixture(scope="class")
    def erratic_scenario(self):
        scenarios = load_fault_scenarios()
        return [s for s in scenarios if s["scenario_name"] == "erratic_soil_moisture"][0]

    @pytest.fixture
    def erratic_readings(self, erratic_scenario):
        return make_readings(erratic_scenario["data_sequence"], "soil_1", "soil_moisture")

    def test_detect_drift_real_data(self, erratic_readings):
        result = check_sensor_drift(erratic_readings, "soil_moisture")
        assert result["has_drift"] is True
        assert result["sensor_type"] == "soil_moisture"
        assert result["max_rate_of_change"] > 3.0  # vượt threshold 3%/min

    def test_detect_drift_trend(self, erratic_readings):
        detector = SensorDriftDetector()
        trend = detector.detect_drift_trend(erratic_readings, "soil_moisture", window_size=4)
        assert trend["has_drift"] is True
        assert trend["readings_analyzed"] == 4


class TestSensorDriftNormalCSV:
    """Dùng CSV — temperature chỉ thay đổi 22.5→23.1 trong 5 phút (0.12°C/min) → không drift."""

    @pytest.fixture
    def normal_temp_readings(self):
        readings = []
        for i, (val, minute) in enumerate([(22.5, 0), (23.1, 5)]):
            readings.append({
                "sensor_id": "temp_1",
                "value": val,
                "timestamp": datetime(2024, 1, 15, 9, minute, 0),
            })
        return readings

    def test_no_drift_normal(self, normal_temp_readings):
        result = check_sensor_drift(normal_temp_readings, "temperature")
        assert result["has_drift"] is False

    def test_detect_drift_with_high_gradient(self):
        """Thay đổi 10°C trong 1 phút → drift."""
        t1 = datetime(2024, 1, 1, 0, 0, 0)
        t2 = datetime(2024, 1, 1, 0, 1, 0)
        readings = [
            {"sensor_id": "t1", "value": 25.0, "timestamp": t1},
            {"sensor_id": "t1", "value": 35.0, "timestamp": t2},
        ]
        result = check_sensor_drift(readings, "temperature")
        assert result["has_drift"] is True
        assert result["avg_rate_of_change"] == 10.0


class TestSensorDriftBoundary:
    def test_single_reading(self):
        now = datetime.now()
        readings = [{"sensor_id": "t1", "value": 25.0, "timestamp": now}]
        res = check_sensor_drift(readings, "temperature")
        assert res["has_drift"] is False
        assert "error" not in res

    def test_empty_readings(self):
        res = check_sensor_drift([], "temperature")
        assert res["has_drift"] is False
        assert "error" in res

    def test_zero_time_diff(self):
        now = datetime.now()
        readings = [
            {"sensor_id": "t1", "value": 25.0, "timestamp": now},
            {"sensor_id": "t1", "value": 30.0, "timestamp": now},
        ]
        detector = SensorDriftDetector()
        rate = detector.calculate_rate_of_change(25.0, now, 30.0, now)
        assert rate == 0.0

    def test_unknown_sensor_type(self):
        now = datetime.now()
        readings = [
            {"sensor_id": "x1", "value": 10, "timestamp": now - timedelta(minutes=1)},
            {"sensor_id": "x1", "value": 20, "timestamp": now},
        ]
        res = check_sensor_drift(readings, "unknown_type")
        assert "has_drift" in res
