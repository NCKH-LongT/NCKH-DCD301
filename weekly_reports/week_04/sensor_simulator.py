"""
Sensor Data Simulator - Generates realistic sensor data with different scenarios
Week 4: IoT/Data Engineer Task

Generates data for:
- Temperature (Celsius)
- Humidity (%)
- Soil Moisture (%)
- Light Intensity (lux)

Scenarios:
- normal: Data within healthy ranges
- warning: Data approaching threshold
- critical: Data beyond safe threshold
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SensorSimulator:
    """Simulates IoT sensors with realistic data patterns"""

    # Sensor configuration with min/max values and thresholds
    SENSOR_CONFIG = {
        'temperature': {
            'unit': 'C',
            'ranges': {
                'normal': (18, 28),
                'warning': (15, 32),
                'critical': (5, 45)
            },
            'min_threshold': 15,
            'max_threshold': 32,
            'critical_min': 5,
            'critical_max': 45,
        },
        'humidity': {
            'unit': '%',
            'ranges': {
                'normal': (40, 70),
                'warning': (30, 80),
                'critical': (10, 95)
            },
            'min_threshold': 30,
            'max_threshold': 80,
            'critical_min': 10,
            'critical_max': 95,
        },
        'soil_moisture': {
            'unit': '%',
            'ranges': {
                'normal': (30, 60),
                'warning': (20, 70),
                'critical': (5, 85)
            },
            'min_threshold': 20,
            'max_threshold': 70,
            'critical_min': 5,
            'critical_max': 85,
        },
        'light': {
            'unit': 'lux',
            'ranges': {
                'normal': (10000, 30000),
                'warning': (5000, 40000),
                'critical': (0, 50000)
            },
            'min_threshold': 5000,
            'max_threshold': 40000,
            'critical_min': 0,
            'critical_max': 50000,
        }
    }

    def __init__(self, sensors: Optional[List[Dict]] = None, api_endpoint: Optional[str] = None):
        """
        Initialize the sensor simulator

        Args:
            sensors: List of sensor configs. If None, creates default sensors
            api_endpoint: Optional API endpoint to send data to (e.g., http://localhost:5000/api/sensor-data)
        """
        self.api_endpoint = api_endpoint
        self.sensors = sensors or self._create_default_sensors()
        self.sensor_state = {}  # Track sensor state for realistic data generation
        self._initialize_sensor_state()

    def _create_default_sensors(self) -> List[Dict]:
        """Create default sensor configuration"""
        sensors = []
        locations = ['greenhouse_1', 'field_2', 'storage_3']
        sensor_types = ['temperature', 'humidity', 'soil_moisture', 'light']

        for location in locations:
            for sensor_type in sensor_types:
                sensor_id = f"{sensor_type.split('_')[0]}_{location.split('_')[1]}"
                sensors.append({
                    'sensor_id': sensor_id,
                    'sensor_name': f"{sensor_type.replace('_', ' ').title()} Sensor {location.split('_')[1]}",
                    'sensor_type': sensor_type,
                    'location': location,
                })
        return sensors

    def _initialize_sensor_state(self):
        """Initialize state tracking for each sensor"""
        for sensor in self.sensors:
            sensor_id = sensor['sensor_id']
            sensor_type = sensor['sensor_type']
            config = self.SENSOR_CONFIG[sensor_type]
            normal_min, normal_max = config['ranges']['normal']

            self.sensor_state[sensor_id] = {
                'last_value': random.uniform(normal_min, normal_max),
                'trend': random.choice([-1, 0, 1]),  # -1: decreasing, 0: stable, 1: increasing
                'drift': random.uniform(-0.5, 0.5),
            }

    def generate_sensor_reading(self, sensor: Dict, scenario: str = 'normal') -> Dict:
        """
        Generate a realistic sensor reading

        Args:
            sensor: Sensor configuration dict
            scenario: 'normal', 'warning', or 'critical'

        Returns:
            Sensor reading dict
        """
        sensor_id = sensor['sensor_id']
        sensor_type = sensor['sensor_type']
        config = self.SENSOR_CONFIG[sensor_type]

        # Get value range based on scenario
        value_range = config['ranges'][scenario]

        # Add realistic drift to simulate sensor behavior
        state = self.sensor_state[sensor_id]
        state['drift'] += random.uniform(-0.1, 0.1)
        state['drift'] = max(-2, min(2, state['drift']))  # Clamp drift

        # Generate value with drift and trend
        base_value = state['last_value']
        trend_adjustment = state['trend'] * random.uniform(0, 0.5)
        new_value = base_value + trend_adjustment + state['drift']
        new_value = max(value_range[0], min(value_range[1], new_value))

        state['last_value'] = new_value

        # Determine status
        status = self._determine_status(sensor_type, new_value)

        reading = {
            'sensor_id': sensor_id,
            'sensor_name': sensor['sensor_name'],
            'sensor_type': sensor_type,
            'location': sensor['location'],
            'value': round(new_value, 2),
            'unit': config['unit'],
            'status': status,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'metadata': {
                'scenario': scenario,
                'quality_flag': 'ok',
            }
        }

        return reading

    def _determine_status(self, sensor_type: str, value: float) -> str:
        """Determine sensor status based on value"""
        config = self.SENSOR_CONFIG[sensor_type]

        if value < config['critical_min'] or value > config['critical_max']:
            return 'critical'
        elif value < config['min_threshold'] or value > config['max_threshold']:
            return 'warning'
        else:
            return 'normal'

    def generate_batch(
        self,
        count: int = 10,
        scenario_distribution: Optional[Dict[str, float]] = None
    ) -> List[Dict]:
        """
        Generate a batch of sensor readings

        Args:
            count: Number of readings to generate
            scenario_distribution: Dict with keys 'normal', 'warning', 'critical'
                                  representing percentage distribution (must sum to ~1.0)

        Returns:
            List of sensor readings
        """
        if scenario_distribution is None:
            scenario_distribution = {'normal': 0.7, 'warning': 0.2, 'critical': 0.1}

        batch = []
        scenarios = []

        # Create scenario list based on distribution
        for scenario, percentage in scenario_distribution.items():
            scenarios.extend([scenario] * int(count * percentage))

        # Fill remaining slots with 'normal'
        while len(scenarios) < count:
            scenarios.append('normal')

        # Shuffle to randomize order
        random.shuffle(scenarios)

        # Generate readings
        for i in range(count):
            sensor = random.choice(self.sensors)
            scenario = scenarios[i]
            reading = self.generate_sensor_reading(sensor, scenario)
            batch.append(reading)

        return batch

    def send_to_api(self, reading: Dict) -> bool:
        """
        Send sensor reading to API endpoint

        Args:
            reading: Sensor reading dict

        Returns:
            True if successful, False otherwise
        """
        if not self.api_endpoint:
            logger.warning("API endpoint not configured. Skipping API send.")
            return False

        try:
            response = requests.post(
                self.api_endpoint,
                json=reading,
                timeout=5
            )
            if response.status_code == 200 or response.status_code == 201:
                logger.info(f"✓ Sent reading: {reading['sensor_id']} = {reading['value']} {reading['unit']}")
                return True
            else:
                logger.error(f"✗ API returned {response.status_code}: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Failed to send to API: {str(e)}")
            return False

    def simulate_continuous(
        self,
        interval: float = 5.0,
        duration: Optional[float] = None,
        scenario_distribution: Optional[Dict[str, float]] = None
    ):
        """
        Run continuous simulation

        Args:
            interval: Seconds between readings
            duration: Total seconds to run (None = infinite)
            scenario_distribution: Distribution of scenarios
        """
        start_time = time.time()
        reading_count = 0

        logger.info(f"Starting continuous simulation (interval={interval}s)")
        if self.api_endpoint:
            logger.info(f"Sending data to: {self.api_endpoint}")

        try:
            while True:
                if duration and (time.time() - start_time) > duration:
                    logger.info(f"Simulation ended after {reading_count} readings")
                    break

                batch = self.generate_batch(count=1, scenario_distribution=scenario_distribution)
                reading = batch[0]

                # Print reading
                print(f"[{reading['timestamp']}] {reading['sensor_name']}: {reading['value']} {reading['unit']} [{reading['status']}]")

                # Send to API if endpoint configured
                if self.api_endpoint:
                    self.send_to_api(reading)

                reading_count += 1
                time.sleep(interval)

        except KeyboardInterrupt:
            logger.info(f"Simulation interrupted after {reading_count} readings")

    def export_batch_to_file(self, filename: str, batch: List[Dict]):
        """Export batch of readings to JSONL file"""
        try:
            with open(filename, 'a') as f:
                for reading in batch:
                    f.write(json.dumps(reading) + '\n')
            logger.info(f"Exported {len(batch)} readings to {filename}")
        except IOError as e:
            logger.error(f"Failed to export to file: {str(e)}")


def main():
    """Example usage"""
    import argparse

    parser = argparse.ArgumentParser(description='Sensor Data Simulator')
    parser.add_argument('--mode', choices=['batch', 'continuous'], default='batch',
                        help='Simulation mode')
    parser.add_argument('--count', type=int, default=100,
                        help='Number of readings (for batch mode)')
    parser.add_argument('--interval', type=float, default=5.0,
                        help='Interval between readings in seconds (for continuous mode)')
    parser.add_argument('--duration', type=float, default=None,
                        help='Duration of simulation in seconds (for continuous mode)')
    parser.add_argument('--api-endpoint', type=str, default=None,
                        help='API endpoint to send data to (e.g., http://localhost:5000/api/sensor-data)')
    parser.add_argument('--output-file', type=str, default=None,
                        help='Output file for batch mode (JSONL format)')
    parser.add_argument('--scenario', choices=['normal', 'warning', 'critical', 'mixed'], default='mixed',
                        help='Data scenario')

    args = parser.parse_args()

    # Create simulator
    simulator = SensorSimulator(api_endpoint=args.api_endpoint)

    # Determine scenario distribution
    scenario_dist = None
    if args.scenario == 'normal':
        scenario_dist = {'normal': 1.0, 'warning': 0.0, 'critical': 0.0}
    elif args.scenario == 'warning':
        scenario_dist = {'normal': 0.0, 'warning': 1.0, 'critical': 0.0}
    elif args.scenario == 'critical':
        scenario_dist = {'normal': 0.0, 'warning': 0.0, 'critical': 1.0}
    else:  # mixed
        scenario_dist = {'normal': 0.7, 'warning': 0.2, 'critical': 0.1}

    if args.mode == 'batch':
        batch = simulator.generate_batch(count=args.count, scenario_distribution=scenario_dist)
        print(f"\nGenerated {len(batch)} sensor readings:\n")
        for reading in batch[:10]:  # Print first 10
            print(json.dumps(reading, indent=2))
        if len(batch) > 10:
            print(f"... and {len(batch) - 10} more readings")

        if args.output_file:
            simulator.export_batch_to_file(args.output_file, batch)

    else:  # continuous
        simulator.simulate_continuous(
            interval=args.interval,
            duration=args.duration,
            scenario_distribution=scenario_dist
        )


if __name__ == '__main__':
    main()
