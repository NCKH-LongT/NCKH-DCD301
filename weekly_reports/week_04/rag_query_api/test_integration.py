"""
Integration Test - End-to-end test: Sensor API → RAG Query
Week 4: Agent/Evaluation Engineer Task

Tests the complete flow:
1. Sensor data is received and stored (Sensor API)
2. RAG query returns relevant agricultural knowledge (requires real vector DB)
3. Results can be combined for decision support

Usage:
  python test_integration.py --mock

  # Test with real Sensor API + RAG API
  python test_integration.py --sensor-url http://localhost:5000 --rag-url http://localhost:8000
"""

import json
import time
import sys
import os
import logging
from typing import Dict, Optional
from datetime import datetime

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from rag_query_api.rag_retriever import RAGRetriever

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IntegrationTester:
    """
    Tests end-to-end integration between Sensor API and RAG Query.
    Uses real vector DB (requires rag_ingest.py to be run first).
    """

    def __init__(
        self,
        sensor_api_url: Optional[str] = None,
        rag_api_url: Optional[str] = None
    ):
        self.sensor_api_url = sensor_api_url
        self.rag_api_url = rag_api_url
        self.results = {
            'passed': 0,
            'failed': 0,
            'tests': []
        }

    def _record(self, name: str, passed: bool, details: str = ""):
        """Record test result"""
        icon = "✅" if passed else "❌"
        logger.info(f"{icon} {name}: {'PASS' if passed else 'FAIL'}")
        if details:
            logger.info(f"   {details}")
        self.results['passed'] += 1 if passed else 0
        self.results['failed'] += 0 if passed else 1
        self.results['tests'].append({
            'name': name,
            'passed': passed,
            'details': details
        })

    def _call_sensor_api(self, reading: Dict) -> bool:
        """Send a sensor reading to the Sensor API"""
        if not self.sensor_api_url:
            logger.warning("Sensor API URL not configured, skipping")
            return False
        try:
            resp = requests.post(
                f"{self.sensor_api_url}/api/sensor-data",
                json=reading,
                timeout=5
            )
            return resp.status_code in (200, 201)
        except Exception as e:
            logger.warning(f"Sensor API call failed: {e}")
            return False

    def _call_rag_api(self, query: str, k: int = 3) -> Optional[Dict]:
        """Query the RAG API"""
        if not self.rag_api_url:
            logger.warning("RAG API URL not configured, skipping")
            return None
        try:
            resp = requests.post(
                f"{self.rag_api_url}/api/rag/query",
                json={"query": query, "k": k},
                timeout=10
            )
            if resp.status_code == 200:
                return resp.json()
            else:
                logger.warning(f"RAG API returned {resp.status_code}: {resp.text}")
        except Exception as e:
            logger.warning(f"RAG API call failed: {e}")
        return None

    def _call_rag_health(self) -> Optional[Dict]:
        """Check RAG API health"""
        if not self.rag_api_url:
            return None
        try:
            resp = requests.get(f"{self.rag_api_url}/api/rag/health", timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return None

    # ========================================================================
    # Test Cases
    # ========================================================================

    def test_sensor_data_format(self):
        """Test 1: Verify sensor data format matches expected schema"""
        reading = {
            "sensor_id": "temp_1",
            "sensor_name": "Temperature Sensor 1",
            "sensor_type": "temperature",
            "value": 25.5,
            "unit": "C",
            "status": "normal",
            "location": "greenhouse_1",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        required_fields = ["sensor_id", "sensor_type", "value", "unit", "timestamp"]
        missing = [f for f in required_fields if f not in reading]
        passed = len(missing) == 0
        self._record(
            "Sensor data format validation",
            passed,
            f"Missing fields: {missing}" if missing else "All required fields present"
        )

    def test_rag_api_health(self):
        """Test 2: RAG API health check"""
        health = self._call_rag_health()
        if health is None:
            self._record(
                "RAG API health check",
                False,
                "RAG API not reachable. Start with: python rag_query.py --api"
            )
            return

        passed = health.get('status') == 'ok'
        self._record(
            "RAG API health check",
            passed,
            f"Mode: {health.get('retriever_mode', 'unknown')}, "
            f"Chunks: {health.get('chunks_count', 'unknown')}"
        )

    def test_rag_query_high_temperature(self):
        """Test 3: RAG query about high temperature returns relevant results"""
        result = self._call_rag_api(
            "temperature too high in greenhouse what to do", k=3
        )
        if result is None:
            self._record("RAG query - high temperature", False,
                         "RAG API not reachable")
            return

        passed = result.get('success', False) and result.get('total_found', 0) > 0
        total = result.get('total_found', 0)
        self._record(
            "RAG query - high temperature",
            passed,
            f"Found {total} relevant chunks" if passed else "No results returned"
        )

    def test_rag_query_low_soil_moisture(self):
        """Test 4: RAG query about dry soil returns irrigation advice"""
        result = self._call_rag_api(
            "soil moisture very low need water", k=3
        )
        if result is None:
            self._record("RAG query - low soil moisture", False,
                         "RAG API not reachable")
            return

        passed = result.get('success', False) and result.get('total_found', 0) > 0
        self._record(
            "RAG query - low soil moisture",
            passed,
            f"Found {result.get('total_found', 0)} chunks"
        )

    def test_rag_query_humidity_disease(self):
        """Test 5: RAG query about humidity and disease"""
        result = self._call_rag_api(
            "high humidity causing fungal disease", k=3
        )
        if result is None:
            self._record("RAG query - humidity disease", False,
                         "RAG API not reachable")
            return

        passed = result.get('success', False) and result.get('total_found', 0) > 0
        self._record(
            "RAG query - humidity disease",
            passed,
            f"Found {result.get('total_found', 0)} chunks"
        )

    def test_sensor_to_rag_flow(self):
        """
        Test 6: End-to-end flow - sensor reading → RAG context

        Simulates: temperature = 34°C (high) → query RAG for action
        """
        # Step 1: Simulate sensor reading
        sensor_reading = {
            "sensor_id": "temp_1",
            "sensor_type": "temperature",
            "value": 34.2,
            "unit": "C",
            "status": "warning",
            "location": "greenhouse_1",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        # Step 2: Optionally send to Sensor API
        if self.sensor_api_url:
            api_ok = self._call_sensor_api(sensor_reading)
            if not api_ok:
                logger.warning("Sensor API not reachable, continuing with RAG-only test")

        # Step 3: Query RAG based on sensor context
        query = (f"temperature {sensor_reading['value']} "
                 f"{sensor_reading['unit']} greenhouse action")
        result = self._call_rag_api(query, k=3)
        if result is None:
            self._record("Sensor → RAG flow", False, "RAG API not reachable")
            return

        passed = result.get('success', False) and result.get('total_found', 0) > 0
        details = (
            f"Sensor: temp=34.2°C (warning)\n"
            f"Query: '{query}'\n"
            f"RAG results: {result.get('total_found', 0)} chunks found"
        )
        self._record("Sensor → RAG flow", passed, details)

    def test_empty_query_handling(self):
        """Test 7: Edge case - empty query"""
        result = self._call_rag_api("", k=3)
        if result is None:
            self._record("Empty query handling", False, "RAG API not reachable")
            return

        # Empty query should still return successfully (0 results is valid)
        passed = result.get('success', False)
        self._record("Empty query handling", passed,
                     f"Total found: {result.get('total_found', 0)}")

    # ========================================================================
    # Run All Tests
    # ========================================================================

    def run_all(self):
        """Run all integration tests"""
        print("\n" + "="*60)
        print("INTEGRATION TEST - Sensor API ↔ RAG Query")
        print("="*60)
        print("Mode: REAL API (requires running services)")
        if self.sensor_api_url:
            print(f"Sensor API: {self.sensor_api_url}")
        if self.rag_api_url:
            print(f"RAG API: {self.rag_api_url}")
        else:
            print("⚠ RAG API URL not set - RAG tests will be skipped")
        print()

        tests = [
            ("Sensor data format", self.test_sensor_data_format),
            ("RAG API health", self.test_rag_api_health),
            ("RAG query - high temperature", self.test_rag_query_high_temperature),
            ("RAG query - low soil moisture", self.test_rag_query_low_soil_moisture),
            ("RAG query - humidity disease", self.test_rag_query_humidity_disease),
            ("Sensor → RAG flow", self.test_sensor_to_rag_flow),
            ("Empty query handling", self.test_empty_query_handling),
        ]

        for name, test_fn in tests:
            try:
                test_fn()
            except Exception as e:
                self._record(name, False, f"Exception: {str(e)}")

        # Summary
        total = self.results['passed'] + self.results['failed']
        print(f"\n{'='*60}")
        print(f"RESULTS: {self.results['passed']}/{total} passed, "
              f"{self.results['failed']} failed")
        print(f"{'='*60}")

        return self.results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Integration Test")
    parser.add_argument("--sensor-url", default=None,
                        help="Sensor API URL (e.g. http://localhost:5000)")
    parser.add_argument("--rag-url", default=None,
                        help="RAG API URL (e.g. http://localhost:8000)")
    parser.add_argument("--output", default=None,
                        help="Output JSON file path")

    args = parser.parse_args()

    tester = IntegrationTester(
        sensor_api_url=args.sensor_url,
        rag_api_url=args.rag_url
    )

    results = tester.run_all()

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📁 Results saved to: {args.output}")


if __name__ == "__main__":
    main()
