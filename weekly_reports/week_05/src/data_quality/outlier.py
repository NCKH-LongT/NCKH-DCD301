"""
Outlier Detection Module for Smart Greenhouse.

Provides utilities to detect outliers in sensor data using:
- Interquartile Range (IQR) method
- Z-score method
- Domain-specific threshold checking

Default sensor thresholds (Smart Greenhouse):
    - Temperature :   5 –  45 °C
    - Humidity    :  20 – 100 %
    - Soil moisture:  0 – 100 %
    - Light       :   0 – 1000 lux
"""

from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd


# Default domain thresholds for Smart Greenhouse sensors
# (min, max) tuples
SENSOR_THRESHOLDS: Dict[str, Tuple[float, float]] = {
    "temperature": (5.0, 45.0),
    "humidity": (20.0, 100.0),
    "soil_moisture": (0.0, 100.0),
    "light": (0.0, 1000.0),
}

# Aliases for convenience
SENSOR_THRESHOLDS_ALIASES: Dict[str, str] = {
    "temp": "temperature",
    "soil": "soil_moisture",
    "soil moisture": "soil_moisture",
    "air_humidity": "humidity",
}


class OutlierDetector:
    """
    Detects outliers in Smart Greenhouse sensor readings.

    Supports three strategies:
        1. **IQR** – flags values outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR].
        2. **Z-score** – flags values whose standardised score exceeds *z_threshold*.
        3. **Threshold** – flags values outside domain-specific [min, max] bounds.
    """

    def __init__(self, thresholds: Optional[Dict[str, Tuple[float, float]]] = None):
        """
        Args:
            thresholds: Optional override for sensor thresholds.
                Falls back to SENSOR_THRESHOLDS for unspecified sensors.
        """
        self._thresholds: Dict[str, Tuple[float, float]] = {}
        if thresholds:
            self._thresholds.update(thresholds)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def detect_outliers_iqr(
        self,
        series: pd.Series,
        multiplier: float = 1.5,
    ) -> pd.Series:
        """
        Detect outliers using the Interquartile Range method.

        Args:
            series: Numeric sensor readings.
            multiplier: IQR multiplier (default 1.5; use 3.0 for extreme outliers).

        Returns:
            Boolean Series where True indicates an outlier.
        """
        if series.empty:
            return pd.Series([], dtype=bool)

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr

        return (series < lower_bound) | (series > upper_bound)

    def detect_outliers_zscore(
        self,
        series: pd.Series,
        z_threshold: float = 3.0,
    ) -> pd.Series:
        """
        Detect outliers using the Z-score method.

        Args:
            series: Numeric sensor readings.
            z_threshold: Maximum acceptable absolute Z-score (default 3.0).

        Returns:
            Boolean Series where True indicates an outlier.
        """
        if series.empty or len(series) < 2:
            return pd.Series([], dtype=bool)

        mean = series.mean()
        std = series.std(ddof=1)

        if std == 0:
            return pd.Series([False] * len(series), index=series.index)

        z_scores = (series - mean).abs() / std
        return z_scores > z_threshold

    def detect_outliers_threshold(
        self,
        series: pd.Series,
        sensor_name: str,
    ) -> pd.Series:
        """
        Detect values that fall outside the domain-specific threshold
        for a given sensor.

        Args:
            series: Numeric sensor readings.
            sensor_name: Sensor type (e.g. "temperature", "humidity", …).
                Aliases such as "temp", "soil" are also accepted.

        Returns:
            Boolean Series where True indicates a value outside the valid range.
        """
        lo, hi = self._resolve_threshold(sensor_name)
        return (series < lo) | (series > hi)

    def detect_all(
        self,
        series: pd.Series,
        sensor_name: str,
        methods: Optional[List[str]] = None,
        iqr_multiplier: float = 1.5,
        z_threshold: float = 3.0,
    ) -> pd.DataFrame:
        """
        Run one or more outlier-detection methods and return a combined
        results DataFrame.

        Args:
            series: Numeric sensor readings.
            sensor_name: Sensor type (used for threshold-based detection).
            methods: Which methods to apply.  Default: ``["iqr", "zscore", "threshold"]``.
            iqr_multiplier: IQR multiplier (passed to ``detect_outliers_iqr``).
            z_threshold: Z-score threshold (passed to ``detect_outliers_zscore``).

        Returns:
            DataFrame with columns:
                value, is_outlier_iqr, is_outlier_zscore, is_outlier_threshold,
                is_any_outlier, sensor
        """
        if methods is None:
            methods = ["iqr", "zscore", "threshold"]

        result = pd.DataFrame({"value": series, "sensor": sensor_name})

        if "iqr" in methods:
            result["is_outlier_iqr"] = self.detect_outliers_iqr(series, iqr_multiplier)
        if "zscore" in methods:
            result["is_outlier_zscore"] = self.detect_outliers_zscore(series, z_threshold)
        if "threshold" in methods:
            result["is_outlier_threshold"] = self.detect_outliers_threshold(series, sensor_name)

        outlier_cols = [c for c in result.columns if c.startswith("is_outlier")]
        if outlier_cols:
            result["is_any_outlier"] = result[outlier_cols].any(axis=1)
        else:
            result["is_any_outlier"] = False

        return result

    def outliers_summary(self, results: pd.DataFrame) -> pd.DataFrame:
        """
        Return a concise summary of outlier detection results.

        Args:
            results: Output from ``detect_all``.

        Returns:
            DataFrame with columns: method, outlier_count, total, percentage.
        """
        total = len(results)
        rows = []
        for col in [c for c in results.columns if c.startswith("is_outlier_")]:
            method = col.replace("is_outlier_", "")
            count = int(results[col].sum())
            rows.append(
                {
                    "method": method,
                    "outlier_count": count,
                    "total": total,
                    "percentage": round(count / total * 100, 2) if total else 0.0,
                }
            )
        return pd.DataFrame(rows).sort_values("outlier_count", ascending=False).reset_index(drop=True)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _resolve_threshold(self, sensor_name: str) -> Tuple[float, float]:
        """Resolve (lower, upper) threshold for *sensor_name*."""
        key = sensor_name.lower().replace(" ", "_").replace("-", "_")

        # Direct lookup
        if key in self._thresholds:
            return self._thresholds[key]
        if key in SENSOR_THRESHOLDS:
            return SENSOR_THRESHOLDS[key]

        # Alias lookup
        if key in SENSOR_THRESHOLDS_ALIASES:
            canonical = SENSOR_THRESHOLDS_ALIASES[key]
            if canonical in self._thresholds:
                return self._thresholds[canonical]
            return SENSOR_THRESHOLDS[canonical]

        raise ValueError(
            f"Unknown sensor '{sensor_name}'. "
            f"Known sensors: {list(SENSOR_THRESHOLDS.keys())} "
            f"(aliases: {list(SENSOR_THRESHOLDS_ALIASES.keys())})"
        )
