"""
Missing Data Detection Module for Smart Greenhouse.

Provides utilities to detect:
- Null / NaN values in sensor data
- Missing records (gaps) where a sensor did not send data
  within an expected time interval
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd


class MissingDataDetector:
    """
    Detector for missing data in Smart Greenhouse sensor readings.

    Supports both DataFrame-based detection (null/NaN) and
    time-series gap detection (missing records).
    """

    # Default expected intervals per sensor type (in seconds)
    DEFAULT_EXPECTED_INTERVALS: Dict[str, int] = {
        "temperature": 60,  # every 60 seconds
        "humidity": 60,
        "soil_moisture": 60,
        "light": 60,
    }

    # Tolerance multiplier: a gap larger than `interval * tolerance` is flagged
    TOLERANCE: float = 2.0

    def __init__(
        self,
        expected_intervals: Optional[Dict[str, int]] = None,
        tolerance: float = 2.0,
    ):
        """
        Args:
            expected_intervals: Mapping of sensor name -> expected interval (seconds).
                Falls back to DEFAULT_EXPECTED_INTERVALS for unspecified sensors.
            tolerance: Multiplier applied to the interval. A gap larger than
                `interval * tolerance` is considered missing data.
        """
        self._intervals: Dict[str, int] = {}
        if expected_intervals:
            self._intervals.update(expected_intervals)
        self.tolerance = tolerance

    # ------------------------------------------------------------------
    # 1. Null / NaN detection
    # ------------------------------------------------------------------

    def detect_null_values(
        self, df: pd.DataFrame, columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Detect null or NaN values in the given DataFrame.

        Args:
            df: Input sensor data.
            columns: Subset of columns to inspect. If None, inspects all columns.

        Returns:
            A DataFrame with the same index, containing only rows that have
            at least one null/NaN value in the specified columns, plus a
            ``_null_columns`` column listing which columns were null.
        """
        target_cols = columns if columns is not None else df.columns.tolist()

        # Filter to columns that actually exist
        existing = [c for c in target_cols if c in df.columns]
        if not existing:
            return pd.DataFrame()

        null_mask = df[existing].isnull() | df[existing].isna()
        rows_with_null = null_mask.any(axis=1)

        result = df.loc[rows_with_null].copy()
        result["_null_columns"] = null_mask.loc[rows_with_null].apply(
            lambda row: [col for col in existing if row[col]], axis=1
        )
        result["_null_count"] = null_mask.loc[rows_with_null].sum(axis=1)
        return result

    def null_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Return a per-column summary of null/NaN counts and percentages.

        Args:
            df: Input sensor data.

        Returns:
            DataFrame with columns: column, null_count, null_percentage.
        """
        total = len(df)
        records = []
        for col in df.columns:
            n_null = int(df[col].isna().sum())
            records.append(
                {
                    "column": col,
                    "null_count": n_null,
                    "null_percentage": round(n_null / total * 100, 2) if total else 0.0,
                }
            )
        return pd.DataFrame(records).sort_values("null_count", ascending=False).reset_index(drop=True)

    # ------------------------------------------------------------------
    # 2. Missing records (time gap) detection
    # ------------------------------------------------------------------

    def _get_interval(self, sensor_name: str) -> int:
        """Return the expected interval (seconds) for *sensor_name*."""
        name_lower = sensor_name.lower().replace(" ", "_")
        if name_lower in self._intervals:
            return self._intervals[name_lower]
        if name_lower in self.DEFAULT_EXPECTED_INTERVALS:
            return self.DEFAULT_EXPECTED_INTERVALS[name_lower]
        # Fallback – use the most common interval from defaults
        return list(self.DEFAULT_EXPECTED_INTERVALS.values())[0]

    def detect_missing_records(
        self,
        df: pd.DataFrame,
        time_col: str = "timestamp",
        sensor_col: str = "sensor",
        value_col: str = "value",
        gaps: bool = True,
    ) -> pd.DataFrame:
        """
        Detect time periods where a sensor did not send any data.

        Args:
            df: Sensor time-series data. Must contain *time_col* and *sensor_col*.
            time_col: Name of the timestamp column.
            sensor_col: Name of the column identifying the sensor.
            value_col: Name of the value column (used to detect NaN-only gaps).
            gaps: If True, flag gaps between consecutive records. If False, only
                report missing intervals at the start/end of the observed window.

        Returns:
            DataFrame where each row describes a missing-data gap:
                sensor, start_time, end_time, gap_seconds, expected_interval,
                severity
        """
        required = {time_col, sensor_col}
        missing_cols = required - set(df.columns)
        if missing_cols:
            raise ValueError(f"DataFrame missing required columns: {missing_cols}")

        if df.empty:
            return pd.DataFrame()

        df = df.sort_values([sensor_col, time_col]).reset_index(drop=True)
        results: List[Dict] = []

        for sensor_name, group in df.groupby(sensor_col):
            interval_sec = self._get_interval(str(sensor_name))
            threshold_sec = interval_sec * self.tolerance
            times = group[time_col].sort_values()

            if len(times) < 2:
                # Only one record – we cannot infer gaps
                continue

            prev_time: Optional[datetime] = None
            for current_time in times:
                if prev_time is not None:
                    gap = (current_time - prev_time).total_seconds()
                    if gap > threshold_sec:
                        severity = self._classify_severity(gap, interval_sec)
                        results.append(
                            {
                                "sensor": sensor_name,
                                "start_time": prev_time,
                                "end_time": current_time,
                                "gap_seconds": round(gap, 2),
                                "expected_interval_seconds": interval_sec,
                                "severity": severity,
                            }
                        )
                prev_time = current_time

            # Also check if the last record is too old (no new data since then)
            last_time = times.iloc[-1]
            tz = getattr(last_time, "tz", None)
            now = pd.Timestamp.now(tz=tz) if tz else pd.Timestamp.now()
            if isinstance(last_time, pd.Timestamp):
                age = (now - last_time).total_seconds()
                if age > threshold_sec:
                    results.append(
                        {
                            "sensor": sensor_name,
                            "start_time": last_time,
                            "end_time": now.to_pydatetime() if hasattr(now, "to_pydatetime") else now,
                            "gap_seconds": round(age, 2),
                            "expected_interval_seconds": interval_sec,
                            "severity": "critical",
                        }
                    )

        return pd.DataFrame(results)

    def detect_all(
        self,
        df: pd.DataFrame,
        time_col: str = "timestamp",
        sensor_col: str = "sensor",
        value_cols: Optional[List[str]] = None,
    ) -> Dict[str, Union[pd.DataFrame, pd.DataFrame]]:
        """
        Convenience method that runs both null-value detection and
        missing-record detection, returning a dictionary of results.

        Returns:
            dict with keys:
                - "null_values": DataFrame of rows with nulls
                - "null_summary": per-column null summary
                - "missing_records": DataFrame of time-gap events
        """
        return {
            "null_values": self.detect_null_values(df, columns=value_cols),
            "null_summary": self.null_summary(df),
            "missing_records": self.detect_missing_records(
                df, time_col=time_col, sensor_col=sensor_col
            ),
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _classify_severity(gap_seconds: float, interval_seconds: int) -> str:
        """Classify gap severity based on how many intervals were missed."""
        missed = gap_seconds / interval_seconds
        if missed >= 10:
            return "critical"
        if missed >= 5:
            return "warning"
        return "info"
