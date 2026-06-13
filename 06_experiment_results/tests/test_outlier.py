"""Unit tests for the OutlierDetector module."""
import os
import sys

_PIPELINE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PIPELINE_ROOT not in sys.path:
    sys.path.insert(0, _PIPELINE_ROOT)

import numpy as np
import pandas as pd
import pytest

from src.data_quality.outlier import (
    OutlierDetector,
    SENSOR_THRESHOLDS,
    SENSOR_THRESHOLDS_ALIASES,
)


@pytest.fixture
def detector() -> OutlierDetector:
    return OutlierDetector()


# ======================================================================
# IQR method
# ======================================================================


class TestDetectOutliersIQR:
    def test_no_outliers(self, detector):
        """Should return all False for normally distributed data."""
        np.random.seed(42)
        data = pd.Series(np.random.normal(25, 2, 100))
        mask = detector.detect_outliers_iqr(data)
        # Expect few false positives — at most 2
        assert mask.sum() <= 2

    def test_with_outliers(self, detector):
        """Should flag injected outliers."""
        data = pd.Series([10, 12, 13, 14, 15, 16, 17, 18, 19, 100])
        mask = detector.detect_outliers_iqr(data)
        assert bool(mask.iloc[-1])  # 100 should be outlier

    def test_all_identical(self, detector):
        """Should not flag any outliers when all values are the same."""
        data = pd.Series([25.0] * 10)
        mask = detector.detect_outliers_iqr(data)
        assert mask.sum() == 0

    def test_empty_series(self, detector):
        """Should handle empty Series gracefully."""
        data = pd.Series([], dtype=float)
        mask = detector.detect_outliers_iqr(data)
        assert len(mask) == 0

    def test_custom_multiplier(self, detector):
        """Should respect a custom IQR multiplier."""
        data = pd.Series(list(range(20)) + [50])
        # With multiplier 1.5, 50 is an outlier
        mask_15 = detector.detect_outliers_iqr(data, multiplier=1.5)
        assert bool(mask_15.iloc[-1])
        # With multiplier 3.0, 50 may not be an extreme outlier
        mask_30 = detector.detect_outliers_iqr(data, multiplier=3.0)
        # The IQR range is wider, 50 might not be flagged
        # We just verify the call works
        assert len(mask_30) == len(data)


# ======================================================================
# Z-score method
# ======================================================================


class TestDetectOutliersZScore:
    def test_no_outliers(self, detector):
        """Should return all False for data within threshold."""
        np.random.seed(42)
        data = pd.Series(np.random.normal(25, 2, 100))
        mask = detector.detect_outliers_zscore(data)
        # With z=3, expect < 1% false positives
        assert mask.sum() <= 2

    def test_with_outliers(self, detector):
        """Should flag extreme values."""
        # Many tight-cluster points + 1 extreme outlier
        rng = np.random.default_rng(42)
        normal = rng.normal(25.0, 1.0, 100)
        data = pd.Series(np.concatenate([normal, [100.0]]))
        mask = detector.detect_outliers_zscore(data)
        # The last element (100.0) should be flagged as outlier
        assert bool(mask.iloc[-1])

    def test_all_identical(self, detector):
        """Should not flag any outliers when std is zero."""
        data = pd.Series([25.0] * 10)
        mask = detector.detect_outliers_zscore(data)
        assert mask.sum() == 0

    def test_empty_series(self, detector):
        """Should handle empty Series gracefully."""
        data = pd.Series([], dtype=float)
        mask = detector.detect_outliers_zscore(data)
        assert len(mask) == 0

    def test_single_element(self, detector):
        """Should handle single-element Series gracefully."""
        data = pd.Series([42.0])
        mask = detector.detect_outliers_zscore(data)
        assert len(mask) == 0

    def test_custom_threshold(self, detector):
        """Should respect a custom z-score threshold."""
        data = pd.Series([10, 12, 13, 14, 15, 16, 17, 18, 19, 100])
        # With z=1, more points may be flagged
        mask = detector.detect_outliers_zscore(data, z_threshold=1.0)
        assert mask.sum() >= 1  # at least the extreme 100


# ======================================================================
# Threshold method
# ======================================================================


class TestDetectOutliersThreshold:
    @pytest.mark.parametrize(
        "sensor, lo, hi",
        [
            ("temperature", 5, 45),
            ("humidity", 20, 100),
            ("soil_moisture", 0, 100),
            ("light", 0, 1000),
        ],
    )
    def test_thresholds_from_spec(self, detector, sensor, lo, hi):
        """Should use the correct thresholds from the task specification."""
        inside = pd.Series([(lo + hi) / 2])
        outside_low = pd.Series([lo - 1])
        outside_high = pd.Series([hi + 1])
        assert detector.detect_outliers_threshold(inside, sensor).sum() == 0
        assert detector.detect_outliers_threshold(outside_low, sensor).sum() == 1
        assert detector.detect_outliers_threshold(outside_high, sensor).sum() == 1

    @pytest.mark.parametrize(
        "alias, canonical",
        [
            ("temp", "temperature"),
            ("soil", "soil_moisture"),
            ("soil moisture", "soil_moisture"),
            ("air_humidity", "humidity"),
        ],
    )
    def test_sensor_aliases(self, detector, alias, canonical):
        """Should resolve sensor aliases correctly."""
        lo, hi = SENSOR_THRESHOLDS[canonical]
        inside = pd.Series([(lo + hi) / 2])
        assert detector.detect_outliers_threshold(inside, alias).sum() == 0

    def test_unknown_sensor_raises(self, detector):
        """Should raise ValueError for unknown sensor names."""
        with pytest.raises(ValueError, match="Unknown sensor"):
            detector.detect_outliers_threshold(pd.Series([1.0]), "nonexistent_sensor")

    def test_empty_series(self, detector):
        """Should handle empty Series gracefully."""
        data = pd.Series([], dtype=float)
        mask = detector.detect_outliers_threshold(data, "temperature")
        assert len(mask) == 0


# ======================================================================
# Combined detect_all
# ======================================================================


class TestDetectAll:
    def test_returns_all_methods(self, detector):
        """detect_all should return all requested method columns."""
        data = pd.Series([10, 12, 13, 14, 15, 16, 17, 18, 19, 100])
        result = detector.detect_all(data, "temperature")
        assert "is_outlier_iqr" in result.columns
        assert "is_outlier_zscore" in result.columns
        assert "is_outlier_threshold" in result.columns
        assert "is_any_outlier" in result.columns
        assert "value" in result.columns
        assert "sensor" in result.columns

    def test_is_any_outlier_combined(self, detector):
        """is_any_outlier should be True if any method flags the point."""
        data = pd.Series([15.0, 200.0])  # 200 is threshold outlier for temperature
        result = detector.detect_all(data, "temperature")
        assert bool(result.iloc[1]["is_any_outlier"])

    def test_custom_methods(self, detector):
        """Should only run requested methods."""
        data = pd.Series([10, 12, 13, 14, 15, 16, 17, 18, 19, 100])
        result = detector.detect_all(data, "temperature", methods=["iqr"])
        assert "is_outlier_iqr" in result.columns
        assert "is_outlier_zscore" not in result.columns
        assert "is_outlier_threshold" not in result.columns

    def test_empty_series(self, detector):
        """Should handle empty Series gracefully."""
        data = pd.Series([], dtype=float)
        result = detector.detect_all(data, "temperature")
        assert len(result) == 0


# ======================================================================
# Summary
# ======================================================================


class TestOutliersSummary:
    def test_summary_counts(self, detector):
        """Summary should correctly count outliers per method."""
        data = pd.Series([10, 12, 13, 14, 15, 16, 17, 18, 19, 100])
        result = detector.detect_all(data, "temperature")
        summary = detector.outliers_summary(result)
        assert len(summary) == 3  # iqr, zscore, threshold
        total = summary["outlier_count"].sum()
        assert total > 0


# ======================================================================
# Custom thresholds
# ======================================================================


class TestCustomThresholds:
    def test_custom_thresholds_override(self):
        """Custom thresholds should override defaults."""
        custom = {"temperature": (10.0, 30.0)}
        det = OutlierDetector(thresholds=custom)
        data = pd.Series([8.0, 25.0, 35.0])
        mask = det.detect_outliers_threshold(data, "temperature")
        # 8.0 < 10 -> outlier, 25 fine, 35 > 30 -> outlier
        assert mask.tolist() == [True, False, True]
