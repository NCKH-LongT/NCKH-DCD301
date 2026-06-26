"""Agent Workflow — run DQ checks → State Analyzer → RAG → Recommendation + Explanation + Confidence Score."""

import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import psycopg2
import psycopg2.extras

from src.data_quality.checker import check_all
from src.rag.rag_client import RAGClient

logger = logging.getLogger(__name__)


class AgentWorkflow:
    def __init__(self):
        self.dsn = (
            f"host={os.getenv('DB_HOST', 'localhost')} "
            f"port={int(os.getenv('DB_PORT', '5432'))} "
            f"dbname={os.getenv('DB_NAME', 'dcd_rag')} "
            f"user={os.getenv('DB_USER', 'postgres')} "
            f"password={os.getenv('DB_PASSWORD', '123456')}"
        )
        self.table = os.getenv("DB_TABLE", "sensor")
        self.ts_col = os.getenv("DB_TIMESTAMP_COL", "timestamp")
        self.rag = RAGClient()

    def fetch_recent_readings(self, minutes: Optional[int] = None, limit: int = 500) -> List[Dict]:
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                if minutes is not None:
                    cur.execute(
                        f"SELECT sensor, sensor_type, value, {self.ts_col} AS timestamp "
                        f"FROM {self.table} "
                        f"WHERE {self.ts_col} >= NOW() - INTERVAL '%s minutes' "
                        f"ORDER BY {self.ts_col} DESC LIMIT %s",
                        (minutes, limit),
                    )
                else:
                    cur.execute(
                        f"SELECT sensor, sensor_type, value, {self.ts_col} AS timestamp "
                        f"FROM {self.table} ORDER BY {self.ts_col} DESC LIMIT %s",
                        (limit,),
                    )
                return [dict(r) for r in cur.fetchall()]

    def _explain_decision(self, dq: Dict, weather_text: str) -> str:
        status = dq["status"]
        analyzed = dq.get("analyzed_state")
        score = dq["sensor_quality_score"]
        if status == "no_data":
            return "No sensor data available for analysis."
        if status == "pass":
            return f"All sensors operating normally (quality_score={score:.2f})."
        parts = [f"Sensor quality score is {score:.2f}."]
        if analyzed:
            parts.append(f"Detected issue: {analyzed}.")
        parts.append(weather_text.split(".")[0] if weather_text else "RAG knowledge base queried for guidance.")
        return " ".join(parts)

    def _compute_confidence_score(self, dq: Dict, rag_result: Dict) -> Dict:
        sqs = dq.get("sensor_quality_score", 0.5)
        evidence = rag_result.get("evidence", [])
        avg_rag = sum(e.get("relevance_score", 0) for e in evidence) / max(len(evidence), 1)
        rag_relevance = avg_rag
        issue_count = len(dq.get("issues", []))
        rule_consistency = max(0.0, 1.0 - 0.15 * issue_count)
        historical_stability = 0.5

        final = 0.4 * sqs + 0.3 * rag_relevance + 0.2 * rule_consistency + 0.1 * historical_stability
        return {
            "final": round(min(1.0, final), 4),
            "sensor_quality_score": round(sqs, 4),
            "rag_relevance_score": round(rag_relevance, 4),
            "rule_consistency_score": round(rule_consistency, 4),
            "historical_stability_score": historical_stability,
            "formula": "0.4*SQS + 0.3*RAG + 0.2*Rule + 0.1*Historical",
        }

    def run(
        self,
        minutes: Optional[int] = None,
        rag_k: int = 3,
    ) -> Dict[str, Any]:
        readings = self.fetch_recent_readings(minutes=minutes)
        if not readings:
            empty_conf = {"final": 0.0, "sensor_quality_score": 0.0, "rag_relevance_score": 0.0, "rule_consistency_score": 0.0, "historical_stability_score": 0.0, "formula": "0.4*SQS + 0.3*RAG + 0.2*Rule + 0.1*Historical"}
            return {"status": "no_data", "detected_issue": None, "sensor_quality_score": 0.0, "recommendation": {"action": None, "level": 0, "duration_minutes": 0, "confidence": 0.0}, "explanation": "No sensor data available.", "evidence": [], "requires_human_approval": False, "confidence": empty_conf, "timestamp": datetime.now(timezone.utc).isoformat()}

        dq = check_all(readings)

        rag_result = self.rag.query_context(dq.get("issues", []), sensor_context="sensor reading issues in greenhouse", k=rag_k)
        rag_text = self.rag.format_rag_context(rag_result)

        confidence = self._compute_confidence_score(dq, rag_result)

        explanation = self._explain_decision(dq, rag_text)

        return {
            "status": dq["status"],
            "detected_issue": dq.get("analyzed_state"),
            "sensor_quality_score": dq["sensor_quality_score"],
            "recommendation": {
                **dq.get("recommendation", {}),
                "confidence": confidence["final"],
            },
            "explanation": explanation,
            "evidence": rag_result.get("evidence", []),
            "requires_human_approval": dq.get("requires_human_approval", False),
            "confidence": confidence,
            "issues": dq["issues"],
            "rag_context": rag_text,
            "readings_analyzed": len(readings),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def run_from_readings(
        self,
        readings: List[Dict],
        rag_k: int = 3,
    ) -> Dict[str, Any]:
        """Run pipeline on pre-loaded readings (no DB fetch). Used by experiments."""
        if not readings:
            empty_conf = {"final": 0.0, "sensor_quality_score": 0.0, "rag_relevance_score": 0.0, "rule_consistency_score": 0.0, "historical_stability_score": 0.0, "formula": "0.4*SQS + 0.3*RAG + 0.2*Rule + 0.1*Historical"}
            return {"status": "no_data", "detected_issue": None, "sensor_quality_score": 0.0, "recommendation": {"action": None, "level": 0, "duration_minutes": 0, "confidence": 0.0}, "explanation": "No sensor data available.", "evidence": [], "requires_human_approval": False, "confidence": empty_conf, "timestamp": datetime.now(timezone.utc).isoformat()}

        dq = check_all(readings)
        rag_result = self.rag.query_context(dq.get("issues", []), sensor_context="sensor reading issues in greenhouse", k=rag_k)
        rag_text = self.rag.format_rag_context(rag_result)
        confidence = self._compute_confidence_score(dq, rag_result)
        explanation = self._explain_decision(dq, rag_text)

        return {
            "status": dq["status"],
            "detected_issue": dq.get("analyzed_state"),
            "sensor_quality_score": dq["sensor_quality_score"],
            "recommendation": {
                **dq.get("recommendation", {}),
                "confidence": confidence["final"],
            },
            "explanation": explanation,
            "evidence": rag_result.get("evidence", []),
            "requires_human_approval": dq.get("requires_human_approval", False),
            "confidence": confidence,
            "issues": dq["issues"],
            "rag_context": rag_text,
            "readings_analyzed": len(readings),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def run_and_print(self, minutes: Optional[int] = None) -> None:
        result = self.run(minutes=minutes)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
