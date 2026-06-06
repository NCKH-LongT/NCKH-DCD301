"""
Sensor Data API - REST API for receiving and storing sensor data
Week 4: IoT/Data Engineer Task

Endpoint: POST /api/sensor-data
Receives sensor readings and stores them in database
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from psycopg2.pool import SimpleConnectionPool
from datetime import datetime
import os
import logging
import json
from typing import Dict, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'sensor_pipeline'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
}

# Connection pool
conn_pool: Optional[SimpleConnectionPool] = None

# Maximum connections in pool
MIN_CONN = 2
MAX_CONN = 10


class DatabaseManager:
    """Manages database connections and operations"""

    def __init__(self, config: Dict):
        """Initialize database manager"""
        self.config = config
        self.pool = None

    def init_pool(self):
        """Initialize connection pool"""
        try:
            self.pool = SimpleConnectionPool(
                MIN_CONN, MAX_CONN,
                host=self.config['host'],
                port=self.config['port'],
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password'],
            )
            logger.info("✓ Database connection pool initialized")
            return True
        except psycopg2.Error as e:
            logger.error(f"✗ Failed to initialize connection pool: {str(e)}")
            return False

    def close_pool(self):
        """Close connection pool"""
        if self.pool:
            self.pool.closeall()
            logger.info("✓ Database connection pool closed")

    def get_connection(self):
        """Get connection from pool"""
        try:
            return self.pool.getconn()
        except psycopg2.Error as e:
            logger.error(f"✗ Failed to get connection from pool: {str(e)}")
            return None

    def return_connection(self, conn):
        """Return connection to pool"""
        if conn and self.pool:
            self.pool.putconn(conn)

    def insert_sensor_reading(self, reading: Dict) -> Tuple[bool, str]:
        """
        Insert a single sensor reading into database

        Args:
            reading: Sensor reading dict

        Returns:
            Tuple of (success: bool, message: str)
        """
        conn = self.get_connection()
        if not conn:
            return False, "Failed to get database connection"

        try:
            cursor = conn.cursor()

            # Parse timestamp
            timestamp = datetime.fromisoformat(reading['timestamp'].replace('Z', '+00:00'))

            # Prepare data
            query = """
                INSERT INTO sensor_data 
                (time, sensor_id, sensor_name, sensor_type, value, unit, status, location, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """

            cursor.execute(query, (
                timestamp,
                reading['sensor_id'],
                reading.get('sensor_name'),
                reading['sensor_type'],
                reading['value'],
                reading.get('unit'),
                reading.get('status', 'normal'),
                reading.get('location'),
                json.dumps(reading.get('metadata', {}))
            ))

            # Update sensor device last reading time
            update_device_query = """
                INSERT INTO sensor_devices 
                (sensor_id, sensor_name, sensor_type, location, unit)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (sensor_id) DO UPDATE SET
                    last_reading_time = EXCLUDED.last_reading_time,
                    updated_at = CURRENT_TIMESTAMP
            """

            cursor.execute(update_device_query, (
                reading['sensor_id'],
                reading.get('sensor_name'),
                reading['sensor_type'],
                reading.get('location'),
                reading.get('unit')
            ))

            conn.commit()
            logger.info(f"✓ Stored reading: {reading['sensor_id']} = {reading['value']}")
            return True, "Reading stored successfully"

        except Exception as e:
            conn.rollback()
            logger.error(f"✗ Failed to insert reading: {str(e)}")
            return False, f"Database error: {str(e)}"
        finally:
            cursor.close()
            self.return_connection(conn)

    def insert_batch_readings(self, readings: list) -> Tuple[int, int]:
        """
        Insert multiple sensor readings efficiently

        Args:
            readings: List of sensor reading dicts

        Returns:
            Tuple of (inserted_count, failed_count)
        """
        conn = self.get_connection()
        if not conn:
            logger.error("Failed to get database connection for batch insert")
            return 0, len(readings)

        inserted = 0
        failed = 0

        try:
            cursor = conn.cursor()

            for reading in readings:
                success, msg = self.insert_sensor_reading(reading)
                if success:
                    inserted += 1
                else:
                    failed += 1

            logger.info(f"✓ Batch insert: {inserted} successful, {failed} failed")
            return inserted, failed

        except Exception as e:
            logger.error(f"✗ Batch insert error: {str(e)}")
            return inserted, len(readings) - inserted
        finally:
            self.return_connection(conn)

    def get_latest_readings(self, limit: int = 100) -> list:
        """Get latest sensor readings"""
        conn = self.get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = """
                SELECT * FROM sensor_data
                ORDER BY time DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            readings = cursor.fetchall()
            cursor.close()
            return readings
        except Exception as e:
            logger.error(f"Failed to fetch readings: {str(e)}")
            return []
        finally:
            self.return_connection(conn)

    def get_sensor_status(self) -> Dict:
        """Get overall sensor status"""
        conn = self.get_connection()
        if not conn:
            return {}

        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = """
                SELECT 
                    sensor_type,
                    status,
                    COUNT(*) as count
                FROM sensor_data
                WHERE time > NOW() - INTERVAL '1 hour'
                GROUP BY sensor_type, status
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()

            # Format results
            status_summary = {}
            for row in results:
                sensor_type = row['sensor_type']
                if sensor_type not in status_summary:
                    status_summary[sensor_type] = {}
                status_summary[sensor_type][row['status']] = row['count']

            return status_summary
        except Exception as e:
            logger.error(f"Failed to get sensor status: {str(e)}")
            return {}
        finally:
            self.return_connection(conn)


# Initialize database manager
db_manager = DatabaseManager(DB_CONFIG)


@app.before_request
def before_request():
    """Initialize database pool before first request"""
    if db_manager.pool is None:
        db_manager.init_pool()


@app.teardown_appcontext
def teardown_db(exception):
    """Close database connections"""
    pass  # Connections are managed by pool


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    """
    Receive and store sensor data

    Expected JSON payload:
    {
        "sensor_id": "temp_1",
        "sensor_name": "Temperature Sensor 1",
        "sensor_type": "temperature",
        "value": 25.5,
        "unit": "C",
        "status": "normal",
        "location": "greenhouse_1",
        "timestamp": "2024-01-15T10:30:00Z",
        "metadata": {
            "quality_flag": "ok"
        }
    }

    Returns:
        JSON response with status and message
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['sensor_id', 'sensor_type', 'value', 'timestamp']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {required_fields}'
            }), 400

        # Insert into database
        success, message = db_manager.insert_sensor_reading(data)

        if success:
            return jsonify({
                'status': 'success',
                'message': message,
                'data': {
                    'sensor_id': data['sensor_id'],
                    'value': data['value'],
                    'timestamp': data['timestamp']
                }
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': message
            }), 500

    except Exception as e:
        logger.error(f"Error in receive_sensor_data: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/api/sensor-data/batch', methods=['POST'])
def receive_batch_data():
    """
    Receive and store multiple sensor readings at once

    Expected JSON payload:
    [
        {sensor_reading_1},
        {sensor_reading_2},
        ...
    ]

    Returns:
        JSON response with insertion statistics
    """
    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({
                'status': 'error',
                'message': 'Expected JSON array'
            }), 400

        if len(data) == 0:
            return jsonify({
                'status': 'error',
                'message': 'Empty batch'
            }), 400

        # Insert batch
        inserted, failed = db_manager.insert_batch_readings(data)

        return jsonify({
            'status': 'success',
            'message': f'Batch processed: {inserted} inserted, {failed} failed',
            'inserted': inserted,
            'failed': failed,
            'total': len(data)
        }), 201

    except Exception as e:
        logger.error(f"Error in receive_batch_data: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/api/sensor-data/latest', methods=['GET'])
def get_latest():
    """Get latest sensor readings"""
    try:
        limit = request.args.get('limit', default=100, type=int)
        limit = min(limit, 1000)  # Max 1000

        readings = db_manager.get_latest_readings(limit)
        return jsonify({
            'status': 'success',
            'count': len(readings),
            'data': readings
        }), 200

    except Exception as e:
        logger.error(f"Error in get_latest: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/api/sensor-data/status', methods=['GET'])
def get_status():
    """Get overall sensor status"""
    try:
        status = db_manager.get_sensor_status()
        return jsonify({
            'status': 'success',
            'data': status
        }), 200

    except Exception as e:
        logger.error(f"Error in get_status: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/', methods=['GET'])
def index():
    """API information"""
    return jsonify({
        'name': 'Sensor Data API',
        'version': '1.0',
        'endpoints': {
            'POST /api/sensor-data': 'Store single sensor reading',
            'POST /api/sensor-data/batch': 'Store multiple readings',
            'GET /api/sensor-data/latest': 'Get latest readings',
            'GET /api/sensor-data/status': 'Get sensor status summary',
            'GET /health': 'Health check'
        }
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Initialize database pool
    if db_manager.init_pool():
        logger.info("Starting Sensor API server...")
        app.run(
            host=os.getenv('API_HOST', '0.0.0.0'),
            port=int(os.getenv('API_PORT', 5000)),
            debug=os.getenv('DEBUG', 'False').lower() == 'true'
        )
    else:
        logger.error("Failed to initialize database. Exiting.")
        exit(1)
