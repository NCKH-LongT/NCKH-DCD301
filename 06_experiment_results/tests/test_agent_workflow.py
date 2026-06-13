"""Unit tests for AgentWorkflow, RAGClient, and Checker (Phase 1)."""

import json
import os
import sys
from datetime import datetime, timezone

import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.data_quality.checker import check_all
from src.rag.rag_client import RAGClient
from src.agent.agent_workflow import AgentWorkflow


class TestChecker:
    def test_check_all_empty(self):
        result = check_all([])
        assert result["status"] == "pass"
        assert result["issues"] == []
        assert result["sensor_quality_score"] == 1.0

    def test_check_all_return_keys(self):
        df = pd.DataFrame({
            "sensor": ["temp_1"] * 5,
            "value": [25.0, 25.1, 24.9, 25.2, 25.0],
            "timestamp": pd.date_range("2024-01-01", periods=5, freq="5min"),
        })
        result = check_all(df)
        assert "status" in result
        assert "issues" in result
        assert "sensor_quality_score" in result
        assert "analyzed_state" in result
        assert "recommendation" in result
        assert "requires_human_approval" in result

    def test_check_all_null_values(self):
        df = pd.DataFrame({
            "sensor": ["temp_1"] * 4,
            "value": [25.0, None, 24.9, None],
            "timestamp": pd.date_range("2024-01-01", periods=4, freq="5min"),
        })
        result = check_all(df)
        missing = [i for i in result["issues"] if i["type"] == "missing_value"]
        assert len(missing) >= 1

    def test_check_all_outlier(self):
        df = pd.DataFrame({
            "sensor": ["temp_1"] * 5,
            "value": [25.0, 25.1, 99.9, 25.2, 25.0],
            "timestamp": pd.date_range("2024-01-01", periods=5, freq="5min"),
        })
        result = check_all(df)
        outliers = [i for i in result["issues"] if i["type"] == "outlier"]
        assert len(outliers) >= 1

    def test_cross_sensor_conflict(self):
        df = pd.DataFrame({
            "sensor": ["temp_1", "temp_2"],
            "value": [25.0, 35.0],
            "timestamp": ["2024-01-01", "2024-01-01"],
        })
        result = check_all(df)
        conflicts = [i for i in result["issues"] if i["type"] == "cross_sensor_conflict"]
        assert len(conflicts) >= 1

    def test_analyzed_state_high_temp(self):
        df = pd.DataFrame({
            "sensor": ["temp_1"] * 5,
            "value": [45.0, 46.0, 47.0, 48.0, 49.0],
            "timestamp": pd.date_range("2024-01-01", periods=5, freq="5min"),
        })
        result = check_all(df)
        assert result["analyzed_state"] is not None


class TestRAGClient:
    def test_init(self):
        client = RAGClient()
        assert client.embedding_model == "all-mpnet-base-v2"

    def test_format_rag_context_empty(self):
        client = RAGClient()
        text = client.format_rag_context({"evidence": []})
        assert text == "No relevant knowledge base entries found."

    def test_evidence_keys(self):
        client = RAGClient()
        ev = {"evidence": [{"source": "doc.pdf", "chunk_id": "chunk_01", "relevance_score": 0.95}]}
        assert ev["evidence"][0]["source"] == "doc.pdf"
        assert ev["evidence"][0]["chunk_id"] == "chunk_01"


class TestAgentWorkflow:
    def test_init(self):
        wf = AgentWorkflow()
        assert wf.table == "sensor"

    def test_no_data_handling(self, monkeypatch):
        def mock_fetch(*args, **kwargs):
            return []
        wf = AgentWorkflow()
        monkeypatch.setattr(wf, "fetch_recent_readings", mock_fetch)
        result = wf.run()
        assert result["status"] == "no_data"
        assert result["confidence"]["final"] == 0.0

    def test_confidence_key_structure(self):
        wf = AgentWorkflow()
        dq_good = {"sensor_quality_score": 1.0, "issues": []}
        rag_good = {"evidence": [{"relevance_score": 0.9}, {"relevance_score": 0.8}]}
        c = wf._compute_confidence_score(dq_good, rag_good)
        assert isinstance(c, dict)
        assert "final" in c
        assert "sensor_quality_score" in c
        assert "rag_relevance_score" in c
        assert "rule_consistency_score" in c
        assert "historical_stability_score" in c
        assert 0.0 < c["final"] <= 1.0

    def test_confidence_zero(self):
        wf = AgentWorkflow()
        dq_bad = {"sensor_quality_score": 0.0, "issues": []}
        rag_empty = {"evidence": []}
        c = wf._compute_confidence_score(dq_bad, rag_empty)
        assert c["final"] >= 0.0

    def test_output_has_mentor_fields(self, monkeypatch):
        def mock_fetch(*args, **kwargs):
            return [{"sensor": "temp_1", "sensor_type": "temperature", "value": 25.0, "timestamp": "2024-01-01T00:00:00+00:00"}]
        def mock_rag(*args, **kwargs):
            return {"evidence": []}
        wf = AgentWorkflow()
        monkeypatch.setattr(wf, "fetch_recent_readings", mock_fetch)
        monkeypatch.setattr(wf.rag, "query_context", mock_rag)
        result = wf.run()
        assert "status" in result
        assert "detected_issue" in result
        assert "sensor_quality_score" in result
        assert "recommendation" in result
        assert "explanation" in result
        assert "evidence" in result
        assert "requires_human_approval" in result
        assert "confidence" in result


class TestIntegrationWithRealDB:
    @pytest.fixture
    def workflow(self):
        return AgentWorkflow()

    def test_fetch_readings_all(self, workflow):
        readings = workflow.fetch_recent_readings()
        assert len(readings) > 0
        assert "sensor" in readings[0]
        assert "value" in readings[0]
        assert "timestamp" in readings[0]

    def test_checker_with_db_data(self, workflow):
        readings = workflow.fetch_recent_readings()
        result = check_all(readings)
        assert "status" in result
        assert "sensor_quality_score" in result
        assert "analyzed_state" in result
        assert "recommendation" in result

    def test_full_workflow_output_keys(self, workflow):
        result = workflow.run(rag_k=1)
        assert "status" in result
        assert "detected_issue" in result
        assert "sensor_quality_score" in result
        assert "recommendation" in result
        assert "explanation" in result
        assert "evidence" in result
        assert "requires_human_approval" in result
        assert "confidence" in result
        assert "readings_analyzed" in result
        assert result["readings_analyzed"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
