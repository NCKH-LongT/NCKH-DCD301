"""
Sensor Stuck Detection Module
Detects when a sensor hasn't changed value for N minutes
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional


class SensorReading:
    """Represents a single sensor reading"""
    def __init__(self, sensor_id: str, value: float, timestamp: datetime):
        self.sensor_id = sensor_id
        self.value = value
        self.timestamp = timestamp
    
    def __repr__(self):
        return f"SensorReading(sensor_id={self.sensor_id}, value={self.value}, timestamp={self.timestamp})"


class SensorStuckDetector:
    """Detects when sensor is stuck (no value change for N minutes)"""
    
    def __init__(self, stuck_threshold_minutes: int = 10):
        """
        Args:
            stuck_threshold_minutes: Number of minutes without value change to consider sensor stuck
        """
        self.stuck_threshold_minutes = stuck_threshold_minutes
    
    def is_stuck(self, readings: List[SensorReading]) -> Tuple[bool, Optional[float]]:
        """
        Check if sensor is stuck by analyzing recent readings.
        
        Args:
            readings: List of SensorReading objects (sorted by timestamp, most recent last)
        
        Returns:
            (is_stuck: bool, duration_minutes: Optional[float])
            - is_stuck: True if sensor hasn't changed value
            - duration_minutes: How long the value has been unchanged
        """
        if len(readings) < 2:
            return False, None
        
        # Get the most recent reading
        latest_reading = readings[-1]
        latest_value = latest_reading.value
        latest_time = latest_reading.timestamp
        
        # Find the first reading with different value
        last_change_time = None
        for i in range(len(readings) - 2, -1, -1):
            if readings[i].value != latest_value:
                last_change_time = readings[i].timestamp
                break
        
        # If no different value found, stuck since the first reading
        if last_change_time is None and len(readings) > 0:
            last_change_time = readings[0].timestamp
        
        if last_change_time is None:
            return False, None
        
        # Calculate duration without change
        duration = latest_time - last_change_time
        duration_minutes = duration.total_seconds() / 60
        
        is_stuck = duration_minutes >= self.stuck_threshold_minutes
        
        return is_stuck, duration_minutes
    
    def detect(self, readings: List[SensorReading]) -> Dict:
        """
        Detect if sensor is stuck and return detailed report.
        
        Args:
            readings: List of SensorReading objects
        
        Returns:
            {
                'is_stuck': bool,
                'sensor_id': str,
                'current_value': float,
                'duration_minutes': float,
                'threshold_minutes': int,
                'last_change_time': datetime
            }
        """
        if not readings:
            return {
                'is_stuck': False,
                'sensor_id': None,
                'error': 'No readings provided'
            }
        
        is_stuck, duration_minutes = self.is_stuck(readings)
        
        latest_reading = readings[-1]
        
        # Find when the last value change occurred
        last_change_time = None
        for i in range(len(readings) - 2, -1, -1):
            if readings[i].value != latest_reading.value:
                last_change_time = readings[i].timestamp
                break
        
        if last_change_time is None:
            last_change_time = readings[0].timestamp
        
        return {
            'is_stuck': is_stuck,
            'sensor_id': latest_reading.sensor_id,
            'current_value': latest_reading.value,
            'duration_minutes': duration_minutes,
            'threshold_minutes': self.stuck_threshold_minutes,
            'last_change_time': last_change_time,
            'latest_timestamp': latest_reading.timestamp
        }


def check_sensor_stuck(readings: List[Dict], stuck_threshold_minutes: int = 10) -> Dict:
    """
    Convenience function to check if sensor is stuck.
    
    Args:
        readings: List of dicts with keys 'sensor_id', 'value', 'timestamp' (datetime)
        stuck_threshold_minutes: Threshold in minutes
    
    Returns:
        Detection result dict
    """
    sensor_readings = [
        SensorReading(r['sensor_id'], r['value'], r['timestamp'])
        for r in readings
    ]
    
    detector = SensorStuckDetector(stuck_threshold_minutes)
    return detector.detect(sensor_readings)
