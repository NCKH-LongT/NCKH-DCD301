"""Unit tests for the MissingDataDetector module."""
import os
import sys

_PIPELINE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PIPELINE_ROOT not in sys.path:
    sys.path.insert(0, _PIPELINE_ROOT)

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pytest

from src.data_quality.missing_data import MissingDataDetector


@pytest.fixture
def detector() -> MissingDataDetector:
    return MissingDataDetector()


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """A clean DataFrame with no missing values."""
    now = datetime.now()
    timestamps = [now + timedelta(seconds=i * 60) for i in range(10)]
    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "sensor": ["temperature"] * 10,
            "value": [25.0 + i for i in range(10)],
        }
    )


# ======================================================================
# Null / NaN detection
# ======================================================================


class TestDetectNullValues:
    def test_no_nulls(self, detector, sample_df):
        """Should return an empty DataFrame when there are no nulls."""
        result = detector.detect_null_values(sample_df)
        assert len(result) == 0

    def test_with_nulls(self, detector):
        """Should detect rows that contain NaN."""
        df = pd.DataFrame({"a": [1.0, np.nan, 3.0], "b": [4.0, 5.0, np.nan]})
        result = detector.detect_null_values(df)
        assert len(result) == 2  # rows 1 and 2

    def test_null_columns_reported(self, detector):
        """Should list which columns are null in each row."""
        df = pd.DataFrame({"a": [1.0, np.nan], "b": [np.nan, 5.0]})
        result = detector.detect_null_values(df)
        row_null_cols = result["_null_columns"].tolist()
        # Row 0: a=1.0 (ok), b=NaN (null) -> _null_columns = ['b']
        assert row_null_cols[0] == ["b"]
        # Row 1: a=NaN (null), b=5.0 (ok) -> _null_columns = ['a']
        assert row_null_cols[1] == ["a"]

    def test_column_subset(self, detector):
        """Should only check specified columns."""
        df = pd.DataFrame({"a": [1.0, np.nan], "b": [np.nan, 5.0], "c": [1.0, 2.0]})
        result = detector.detect_null_values(df, columns=["a", "c"])
        # Only row 1 (index 1) has a null in 'a'
        assert len(result) == 1

    def test_empty_dataframe(self, detector):
        """Should handle an empty DataFrame gracefully."""
        df = pd.DataFrame()
        result = detector.detect_null_values(df)
        assert len(result) == 0

    def test_none_values(self, detector):
        """Should also detect None as missing."""
        df = pd.DataFrame({"a": [1.0, None, 3.0]})
        result = detector.detect_null_values(df)
        assert len(result) == 1


class TestNullSummary:
    def test_summary_no_nulls(self, detector, sample_df):
        """Summary should show 0% null when there are no nulls."""
        summary = detector.null_summary(sample_df)
        assert (summary["null_count"] == 0).all()

    def test_summary_with_nulls(self, detector):
        """Summary should correctly count nulls per column."""
        df = pd.DataFrame({"a": [1.0, np.nan, np.nan], "b": [4.0, 5.0, np.nan]})
        summary = detector.null_summary(df)
        a_row = summary[summary["column"] == "a"].iloc[0]
        b_row = summary[summary["column"] == "b"].iloc[0]
        assert a_row["null_count"] == 2
        assert b_row["null_count"] == 1
        assert a_row["null_percentage"] == pytest.approx(66.67, rel=1)


# ======================================================================
# Missing records (time gap) detection
# ======================================================================


class TestDetectMissingRecords:
    def test_no_gaps(self, detector, sample_df):
        """Should return empty when records are evenly spaced."""
        result = detector.detect_missing_records(sample_df)
        assert len(result) == 0

    def test_detects_gap(self, detector):
        """Should detect a gap larger than the tolerance."""
        now = datetime.now()
        timestamps = [
            now,
            now + timedelta(seconds=60),  # OK
            now + timedelta(minutes=10),  # gap: 9 min > 2 * 60s
        ]
        df = pd.DataFrame(
            {"timestamp": timestamps, "sensor": "temperature", "value": [25.0, 26.0, 27.0]}
        )
        result = detector.detect_missing_records(df)
        assert len(result) == 1
        gap_info = result.iloc[0]
        assert gap_info["sensor"] == "temperature"
        assert gap_info["gap_seconds"] >= 9 * 60

    def test_multiple_sensors(self, detector):
        """Should handle multiple sensors independently."""
        now = datetime.now()
        timestamps_ok = [now + timedelta(seconds=i * 60) for i in range(3)]
        timestamps_gap = [
            now,
            now + timedelta(minutes=10),
        ]
        df = pd.DataFrame(
            {
                "timestamp": timestamps_ok + timestamps_gap,
                "sensor": ["temperature"] * 3 + ["humidity"] * 2,
                "value": [25.0, 26.0, 27.0, 60.0, 61.0],
            }
        )
        result = detector.detect_missing_records(df)
        # Only humidity should have a gap
        assert len(result) == 1
        assert result.iloc[0]["sensor"] == "humidity"

    def test_custom_interval(self, detector):
        """Should respect custom expected intervals."""
        now = datetime.now()
        timestamps = [
            now,
            now + timedelta(seconds=30),  # within custom 20s tolerance?  30 > 20*2 = 40? No, 30 < 40
            now + timedelta(seconds=90),  # 90 > 40 -> gap
        ]
        df = pd.DataFrame(
            {"timestamp": timestamps, "sensor": "light", "value": [500.0, 510.0, 520.0]}
        )
        # light defaults to 60s interval -> threshold = 120s
        # gaps are 30s and 60s, both < 120s, so no gap
        result = detector.detect_missing_records(df)
        assert len(result) == 0

        # Now with a custom 20s interval -> threshold = 40s
        det = MissingDataDetector(expected_intervals={"light": 20})
        result = det.detect_missing_records(df)
        assert len(result) == 1  # the 90s gap > 40s

    def test_single_record_per_sensor(self, detector):
        """Should skip sensors with only one record (cannot infer gaps)."""
        now = datetime.now()
        df = pd.DataFrame(
            {"timestamp": [now], "sensor": ["temperature"], "value": [25.0]}
        )
        result = detector.detect_missing_records(df)
        assert len(result) == 0

    def test_unsorted_timestamps(self, detector):
        """Should work even if timestamps are not sorted."""
        now = datetime.now()
        timestamps = [
            now + timedelta(minutes=10),
            now,
            now + timedelta(seconds=60),
        ]
        df = pd.DataFrame(
            {"timestamp": timestamps, "sensor": "temperature", "value": [27.0, 25.0, 26.0]}
        )
        result = detector.detect_missing_records(df)
        # gap between now and now+60 is fine, gap between now+60 and now+10min is ~9 min > 120s
        assert len(result) == 1

    def test_empty_dataframe(self, detector):
        """Should handle empty DataFrame gracefully."""
        df = pd.DataFrame({"timestamp": [], "sensor": [], "value": []})
        result = detector.detect_missing_records(df)
        assert len(result) == 0

    def test_missing_required_columns(self, detector, sample_df):
        """Should raise ValueError if required columns are missing."""
        bad_df = sample_df.drop(columns=["timestamp"])
        with pytest.raises(ValueError, match="missing required columns"):
            detector.detect_missing_records(bad_df)

    def test_severity_classification(self, detector):
        """Should classify severity based on gap size."""
        now = datetime.now()
        # Gap large enough to exceed even 10x interval
        timestamps = [
            now,
            now + timedelta(hours=1),  # 3600s gap, interval=60s -> 60x -> critical
        ]
        df = pd.DataFrame(
            {"timestamp": timestamps, "sensor": "temperature", "value": [25.0, 30.0]}
        )
        result = detector.detect_missing_records(df)
        assert result.iloc[0]["severity"] == "critical"


# ======================================================================
# Convenience method
# ======================================================================


class TestDetectAll:
    def test_returns_all_keys(self, detector, sample_df):
        """detect_all should return all expected keys."""
        result = detector.detect_all(sample_df)
        assert "null_values" in result
        assert "null_summary" in result
        assert "missing_records" in result
