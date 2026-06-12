"""Test timestamp_delay với dữ liệu thật từ CSV + sinh realistic time-series."""
import os
import sys
import csv
from datetime import datetime, timedelta

_PIPELINE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PIPELINE_ROOT not in sys.path:
    sys.path.insert(0, _PIPELINE_ROOT)

import pytest
from src.data_quality.timestamp_delay import TimestampDelayDetector, check_timestamp_delay

SAMPLE_DIR = os.path.join(_PIPELINE_ROOT, "sample_data")


def load_csv_readings(filename, sensor_id):
    path = os.path.join(SAMPLE_DIR, filename)
    readings = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["sensor_id"] == sensor_id:
                readings.append({
                    "sensor_id": row["sensor_id"],
                    "value": float(row["value"]),
                    "timestamp": datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")),
                })
    return readings


def make_interval_readings(
    start: datetime, count: int, interval_sec: int, sensor_id="temp_1", value=25.0
):
    readings = []
    for i in range(count):
        readings.append({
            "sensor_id": sensor_id,
            "value": value + (i * 0.1),
            "timestamp": start + timedelta(seconds=i * interval_sec),
        })
    return readings


class TestTimestampDelayNormalCSV:
    """normal.csv: readings cách nhau 5 phút (300s), expected_interval = 300s → không delay."""

    @pytest.fixture
    def normal_temp_readings(self):
        return load_csv_readings("sample_sensor_data_normal.csv", "temp_1")

    def test_no_delay_normal_interval(self):
        """Dùng recent timestamps thay vì CSV (data 2024 bị system_delay)."""
        now = datetime.now()
        readings = [
            {"sensor_id": "temp_1", "value": 22.5, "timestamp": now},
            {"sensor_id": "temp_1", "value": 23.1, "timestamp": now + timedelta(seconds=300)},
        ]
        result = check_timestamp_delay(readings, expected_interval_seconds=300, delay_threshold_seconds=30)
        assert result["has_delay"] is False

    def test_delay_if_expected_interval_lower(self, normal_temp_readings):
        result = check_timestamp_delay(normal_temp_readings, expected_interval_seconds=60, delay_threshold_seconds=30)
        assert result["has_delay"] is True
        assert result["has_interval_delay"] is True
        assert result["interval_delay_seconds"] > 0


class TestTimestampDelayDetectLate:
    """Chủ động tạo readings bị trễ."""

    def test_single_late_reading(self):
        """Interval 120s > expected 60s + threshold 30s → delay."""
        now = datetime.now()
        readings = [
            {"sensor_id": "t1", "value": 25.0, "timestamp": now},
            {"sensor_id": "t1", "value": 26.0, "timestamp": now + timedelta(seconds=120)},
        ]
        result = check_timestamp_delay(readings, expected_interval_seconds=60, delay_threshold_seconds=30)
        assert result["has_delay"] is True

    def test_on_time_reading(self):
        now = datetime.now()
        readings = [
            {"sensor_id": "t1", "value": 25.0, "timestamp": now},
            {"sensor_id": "t1", "value": 26.0, "timestamp": now + timedelta(seconds=60)},
        ]
        result = check_timestamp_delay(readings, expected_interval_seconds=60, delay_threshold_seconds=30)
        assert result["has_delay"] is False


class TestTimestampDelaySystemTime:
    """detect_delay_from_system_time: so sánh reading cũ với current time."""

    def test_old_reading_detected(self):
        detector = TimestampDelayDetector(delay_warning_threshold_seconds=30)
        old = datetime.now() - timedelta(minutes=5)
        has_delay, secs = detector.detect_delay_from_system_time(old)
        assert has_delay is True
        assert secs > 30

    def test_fresh_reading_no_delay(self):
        detector = TimestampDelayDetector(delay_warning_threshold_seconds=30)
        now = datetime.now()
        has_delay, secs = detector.detect_delay_from_system_time(now)
        assert has_delay is False


class TestTimestampDelayMultiple:
    """detect_multiple_delays — trả về danh sách delay cho từng interval."""

    def test_multiple_delays(self):
        start = datetime.now()
        readings = make_interval_readings(start, count=5, interval_sec=120)
        detector = TimestampDelayDetector(expected_interval_seconds=60, delay_warning_threshold_seconds=30)
        delays = detector.detect_multiple_delays(readings)
        assert len(delays) == 4
        assert all(d["has_delay"] is True for d in delays)
        assert all(d["delay_seconds"] == 60.0 for d in delays)


class TestTimestampDelayBoundary:
    def test_single_reading(self):
        now = datetime.now()
        readings = [{"sensor_id": "t1", "value": 25.0, "timestamp": now}]
        result = check_timestamp_delay(readings)
        assert result["has_delay"] is False

    def test_empty_readings(self):
        result = check_timestamp_delay([])
        assert result["has_delay"] is False
        assert "error" in result

    def test_exact_threshold_edge(self):
        """delay == threshold (30s) → has_delay = False vì code dùng strict >."""
        now = datetime.now()
        readings = [
            {"sensor_id": "t1", "value": 25.0, "timestamp": now},
            {"sensor_id": "t1", "value": 26.0, "timestamp": now + timedelta(seconds=90)},
        ]
        result = check_timestamp_delay(readings, expected_interval_seconds=60, delay_threshold_seconds=30)
        assert result["interval_delay_seconds"] == 30.0
        assert result["has_delay"] is False  # 30 > 30 là False

    def test_delay_above_threshold(self):
        """delay 31s > threshold 30s → has_delay = True."""
        now = datetime.now()
        readings = [
            {"sensor_id": "t1", "value": 25.0, "timestamp": now},
            {"sensor_id": "t1", "value": 26.0, "timestamp": now + timedelta(seconds=91)},
        ]
        result = check_timestamp_delay(readings, expected_interval_seconds=60, delay_threshold_seconds=30)
        assert result["has_delay"] is True
