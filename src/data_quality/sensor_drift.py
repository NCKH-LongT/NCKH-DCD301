"""
Sensor Drift Detection Module
Detects abnormal rate of change (gradient) in sensor values
"""

from datetime import datetime
from typing import List, Dict, Optional, Tuple


class SensorDriftDetector:
    """Detects sensor drift by monitoring the rate of change"""
    
    def __init__(self, drift_thresholds: Optional[Dict[str, float]] = None):
        """
        Args:
            drift_thresholds: Dict mapping sensor types to max allowed change per minute
                Default thresholds:
                - temperature: 2.0°C/min
                - humidity: 5.0%/min
                - soil_moisture: 3.0%/min
                - light: 50.0 lux/min
        """
        self.drift_thresholds = drift_thresholds or {
            'temperature': 2.0,
            'humidity': 5.0,
            'soil_moisture': 3.0,
            'light': 50.0
        }
    
    def get_threshold(self, sensor_type: str) -> float:
        """Get drift threshold for sensor type"""
        return self.drift_thresholds.get(sensor_type, 5.0)  # Default 5.0 if type not found
    
    def calculate_rate_of_change(self, 
                                 value1: float, 
                                 time1: datetime,
                                 value2: float,
                                 time2: datetime) -> float:
        """
        Calculate rate of change (value per minute).
        
        Args:
            value1: First value
            time1: First timestamp
            value2: Second value (more recent)
            time2: Second timestamp (more recent)
        
        Returns:
            Rate of change in units per minute
        """
        time_diff = (time2 - time1).total_seconds() / 60  # Convert to minutes
        
        if time_diff == 0:
            return 0.0
        
        rate = abs(value2 - value1) / time_diff
        return rate
    
    def detect_drift(self, 
                     readings: List[Dict],
                     sensor_type: str) -> Tuple[bool, Optional[float], float]:
        """
        Check if sensor shows drift by comparing recent rate of change.
        
        Args:
            readings: List of dicts with 'value' and 'timestamp' (datetime)
            sensor_type: Type of sensor (temperature, humidity, soil_moisture, light)
        
        Returns:
            (has_drift: bool, rate_of_change: float, threshold: float)
        """
        if len(readings) < 2:
            return False, None, self.get_threshold(sensor_type)
        
        # Compare most recent reading with previous one
        latest = readings[-1]
        previous = readings[-2]
        
        rate = self.calculate_rate_of_change(
            previous['value'],
            previous['timestamp'],
            latest['value'],
            latest['timestamp']
        )
        
        threshold = self.get_threshold(sensor_type)
        has_drift = rate > threshold
        
        return has_drift, rate, threshold
    
    def detect_drift_trend(self,
                           readings: List[Dict],
                           sensor_type: str,
                           window_size: int = 5) -> Dict:
        """
        Detect drift by analyzing trend over multiple readings (moving window).
        
        Args:
            readings: List of dicts with 'value' and 'timestamp'
            sensor_type: Type of sensor
            window_size: Number of recent readings to analyze
        
        Returns:
            {
                'has_drift': bool,
                'avg_rate_of_change': float,
                'max_rate_of_change': float,
                'threshold': float,
                'readings_analyzed': int
            }
        """
        if len(readings) < 2:
            return {
                'has_drift': False,
                'avg_rate_of_change': 0,
                'max_rate_of_change': 0,
                'threshold': self.get_threshold(sensor_type),
                'readings_analyzed': len(readings)
            }
        
        # Use recent readings up to window_size
        recent_readings = readings[-window_size:]
        
        rates = []
        for i in range(len(recent_readings) - 1):
            rate = self.calculate_rate_of_change(
                recent_readings[i]['value'],
                recent_readings[i]['timestamp'],
                recent_readings[i+1]['value'],
                recent_readings[i+1]['timestamp']
            )
            rates.append(rate)
        
        if not rates:
            return {
                'has_drift': False,
                'avg_rate_of_change': 0,
                'max_rate_of_change': 0,
                'threshold': self.get_threshold(sensor_type),
                'readings_analyzed': len(recent_readings)
            }
        
        avg_rate = sum(rates) / len(rates)
        max_rate = max(rates)
        threshold = self.get_threshold(sensor_type)
        
        has_drift = avg_rate > threshold or max_rate > threshold
        
        return {
            'has_drift': has_drift,
            'avg_rate_of_change': avg_rate,
            'max_rate_of_change': max_rate,
            'threshold': threshold,
            'readings_analyzed': len(recent_readings)
        }
    
    def detect(self, readings: List[Dict], sensor_type: str) -> Dict:
        """
        Detect sensor drift and return detailed report.
        
        Args:
            readings: List of dicts with 'sensor_id', 'value', 'timestamp'
            sensor_type: Type of sensor
        
        Returns:
            Detection result dict
        """
        if not readings:
            return {'has_drift': False, 'error': 'No readings provided'}
        
        # Use moving window analysis
        drift_info = self.detect_drift_trend(readings, sensor_type)
        
        return {
            'has_drift': drift_info['has_drift'],
            'sensor_id': readings[-1].get('sensor_id'),
            'sensor_type': sensor_type,
            'avg_rate_of_change': drift_info['avg_rate_of_change'],
            'max_rate_of_change': drift_info['max_rate_of_change'],
            'threshold': drift_info['threshold'],
            'readings_analyzed': drift_info['readings_analyzed']
        }


def check_sensor_drift(readings: List[Dict], sensor_type: str) -> Dict:
    """
    Convenience function to check sensor drift.
    
    Args:
        readings: List of dicts with 'value', 'timestamp', 'sensor_id'
        sensor_type: Type of sensor (temperature, humidity, soil_moisture, light)
    
    Returns:
        Detection result dict
    """
    detector = SensorDriftDetector()
    return detector.detect(readings, sensor_type)
