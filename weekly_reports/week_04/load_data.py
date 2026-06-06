"""
Data Loading Utility - Load sample data into database
Week 4: Helper script for Member 1
"""

import csv
import json
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_csv_to_database(csv_file: str, db_config: dict) -> tuple:
    """
    Load sensor data from CSV file to database

    Args:
        csv_file: Path to CSV file
        db_config: Database configuration dict

    Returns:
        Tuple of (inserted_count, failed_count)
    """
    inserted = 0
    failed = 0

    try:
        # Connect to database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Read CSV file
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        logger.info(f"Loading {len(rows)} records from {csv_file}")

        # Insert data
        for row in rows:
            try:
                # Parse timestamp
                timestamp = datetime.fromisoformat(row['timestamp'].replace('Z', '+00:00'))

                # Insert into sensor_data table
                cursor.execute("""
                    INSERT INTO sensor_data 
                    (time, sensor_id, sensor_name, sensor_type, value, unit, status, location)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    timestamp,
                    row['sensor_id'],
                    row['sensor_name'],
                    row['sensor_type'],
                    float(row['value']),
                    row['unit'],
                    row['status'],
                    row['location']
                ))

                inserted += 1

            except Exception as e:
                failed += 1
                logger.warning(f"Failed to insert row {inserted + failed}: {str(e)}")

        # Commit transaction
        conn.commit()

        logger.info(f"✓ Loaded {inserted} records successfully, {failed} failed")

        # Close connection
        cursor.close()
        conn.close()

        return inserted, failed

    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        return 0, len(rows)


def load_jsonl_to_database(jsonl_file: str, db_config: dict) -> tuple:
    """
    Load sensor data from JSONL file to database

    Args:
        jsonl_file: Path to JSONL file (one JSON object per line)
        db_config: Database configuration dict

    Returns:
        Tuple of (inserted_count, failed_count)
    """
    inserted = 0
    failed = 0

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Count lines
        with open(jsonl_file, 'r') as f:
            total = sum(1 for _ in f)

        logger.info(f"Loading {total} records from {jsonl_file}")

        # Read and insert
        with open(jsonl_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    reading = json.loads(line.strip())

                    # Parse timestamp
                    timestamp = datetime.fromisoformat(
                        reading['timestamp'].replace('Z', '+00:00')
                    )

                    # Insert
                    cursor.execute("""
                        INSERT INTO sensor_data 
                        (time, sensor_id, sensor_name, sensor_type, value, unit, status, location, metadata)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
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

                    if line_num % 100 == 0:
                        conn.commit()
                        logger.info(f"  Processed {line_num}/{total} records")

                    inserted += 1

                except Exception as e:
                    failed += 1
                    logger.warning(f"Failed to insert line {line_num}: {str(e)}")

        # Final commit
        conn.commit()

        logger.info(f"✓ Loaded {inserted} records successfully, {failed} failed")

        cursor.close()
        conn.close()

        return inserted, failed

    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        return 0, total


def main():
    parser = argparse.ArgumentParser(description='Load sensor data into database')

    parser.add_argument('--file', type=str, required=True,
                        help='Path to CSV or JSONL file')
    parser.add_argument('--host', type=str, default='localhost',
                        help='Database host')
    parser.add_argument('--port', type=int, default=5432,
                        help='Database port')
    parser.add_argument('--db', type=str, default='sensor_pipeline',
                        help='Database name')
    parser.add_argument('--user', type=str, default='postgres',
                        help='Database user')
    parser.add_argument('--password', type=str, default='postgres',
                        help='Database password')

    args = parser.parse_args()

    # Prepare database config
    db_config = {
        'host': args.host,
        'port': args.port,
        'database': args.db,
        'user': args.user,
        'password': args.password,
    }

    # Determine file type
    if args.file.endswith('.csv'):
        inserted, failed = load_csv_to_database(args.file, db_config)
    elif args.file.endswith('.jsonl'):
        inserted, failed = load_jsonl_to_database(args.file, db_config)
    else:
        logger.error("Unsupported file format. Use .csv or .jsonl")
        return

    # Print summary
    print(f"\n{'='*50}")
    print(f"Load Summary:")
    print(f"  Total Inserted: {inserted}")
    print(f"  Failed: {failed}")
    print(f"  Total: {inserted + failed}")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()
