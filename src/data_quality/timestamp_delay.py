"""
Timestamp Delay Detection Module
Detects when sensor data arrives late compared to expected interval
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple


class TimestampDelayDetector:
    """Detects delays in sensor data timestamps"""
    
    def __init__(self, expected_interval_seconds: int = 60, delay_warning_threshold_seconds: int = 30):
        """
        Args:
            expected_interval_seconds: Expected interval between readings (default 60s = 1 min)
            delay_warning_threshold_seconds: Threshold to raise warning (default 30s)
        """
        self.expected_interval_seconds = expected_interval_seconds
        self.delay_warning_threshold_seconds = delay_warning_threshold_seconds
    
    def calculate_delay(self, 
                       expected_timestamp: datetime,
                       actual_timestamp: datetime) -> float:
        """
        Calculate delay in seconds.
        
        Args:
            expected_timestamp: When we expected the reading
            actual_timestamp: When we actually received it
        
        Returns:
            Delay in seconds (positive means late, negative means early)
        """
        delay = (actual_timestamp - expected_timestamp).total_seconds()
        return delay
    
    def detect_delay_from_interval(self, readings: List[Dict]) -> Tuple[bool, Optional[float]]:
        """
        Detect delay by checking interval between consecutive readings.
        
        Args:
            readings: List of dicts with 'timestamp' (datetime)
        
        Returns:
            (has_delay: bool, actual_interval_seconds: float)
        """
        if len(readings) < 2:
            return False, None
        
        # Get interval between last two readings
        latest = readings[-1]['timestamp']
        previous = readings[-2]['timestamp']
        
        actual_interval = (latest - previous).total_seconds()
        
        # If interval is significantly larger than expected, data arrived late
        delay = actual_interval - self.expected_interval_seconds
        has_delay = delay > self.delay_warning_threshold_seconds
        
        return has_delay, delay
    
    def detect_delay_from_system_time(self,
                                       reading_timestamp: datetime,
                                       current_system_time: Optional[datetime] = None) -> Tuple[bool, float]:
        """
        Detect if a single reading timestamp is old compared to current system time.
        
        Args:
            reading_timestamp: Timestamp from the sensor reading
            current_system_time: Current system time (default: now)
        
        Returns:
            (has_delay: bool, delay_seconds: float)
        """
        if current_system_time is None:
            tz = reading_timestamp.tzinfo
            current_system_time = datetime.now(tz) if tz else datetime.now()
        
        delay = (current_system_time - reading_timestamp).total_seconds()
        has_delay = delay > self.delay_warning_threshold_seconds
        
        return has_delay, delay
    
    def detect(self, readings: List[Dict]) -> Dict:
        """
        Detect timestamp delays and return detailed report.
        
        Args:
            readings: List of dicts with 'timestamp' (datetime) and 'sensor_id'
        
        Returns:
            Detection result dict
        """
        if not readings:
            return {'has_delay': False, 'error': 'No readings provided'}
        
        # Check interval-based delay
        has_interval_delay, interval_delay = self.detect_delay_from_interval(readings)
        
        # Check system time-based delay
        latest_reading = readings[-1]
        has_system_delay, system_delay = self.detect_delay_from_system_time(
            latest_reading['timestamp']
        )
        
        has_any_delay = has_interval_delay or has_system_delay
        
        return {
            'has_delay': has_any_delay,
            'sensor_id': latest_reading.get('sensor_id'),
            'latest_timestamp': latest_reading['timestamp'],
            'interval_delay_seconds': interval_delay,
            'system_delay_seconds': system_delay,
            'delay_threshold_seconds': self.delay_warning_threshold_seconds,
            'expected_interval_seconds': self.expected_interval_seconds,
            'has_interval_delay': has_interval_delay,
            'has_system_delay': has_system_delay
        }
    
    def detect_multiple_delays(self, readings: List[Dict]) -> List[Dict]:
        """
        Detect delays for all intervals in the readings list.
        
        Args:
            readings: List of dicts with 'timestamp' and 'sensor_id'
        
        Returns:
            List of delay detection reports for each interval
        """
        delays = []
        
        for i in range(1, len(readings)):
            prev_time = readings[i-1]['timestamp']
            curr_time = readings[i]['timestamp']
            actual_interval = (curr_time - prev_time).total_seconds()
            delay = actual_interval - self.expected_interval_seconds
            
            has_delay = delay > self.delay_warning_threshold_seconds
            
            delays.append({
                'from_timestamp': prev_time,
                'to_timestamp': curr_time,
                'actual_interval_seconds': actual_interval,
                'expected_interval_seconds': self.expected_interval_seconds,
                'delay_seconds': delay,
                'has_delay': has_delay
            })
        
        return delays


def check_timestamp_delay(readings: List[Dict], 
                         expected_interval_seconds: int = 60,
                         delay_threshold_seconds: int = 30) -> Dict:
    """
    Convenience function to check timestamp delays.
    
    Args:
        readings: List of dicts with 'timestamp' (datetime) and 'sensor_id'
        expected_interval_seconds: Expected interval between readings
        delay_threshold_seconds: Threshold to raise warning
    
    Returns:
        Detection result dict
    """
    detector = TimestampDelayDetector(expected_interval_seconds, delay_threshold_seconds)
    return detector.detect(readings)
