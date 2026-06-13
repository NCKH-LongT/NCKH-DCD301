"""RAG Client — query knowledge base từ sensor context."""

import json
import logging
import os
import sys
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class RAGClient:
    def __init__(self, embedding_model: str = "all-mpnet-base-v2"):
        self._retriever = None
        self.embedding_model = embedding_model

    def _lazy_init(self):
        if self._retriever is not None:
            return
        os.environ.setdefault("PG_HOST", os.getenv("DB_HOST", "localhost"))
        os.environ.setdefault("PG_PORT", os.getenv("DB_PORT", "5432"))
        os.environ.setdefault("PG_DBNAME", os.getenv("DB_NAME", "dcd_rag"))
        os.environ.setdefault("PG_USER", os.getenv("DB_USER", "postgres"))
        os.environ.setdefault("PG_PASSWORD", os.getenv("DB_PASSWORD", "123456"))
        os.environ.setdefault("PG_TABLE", "knowledge_base")
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
        from rag_query_api.rag_retriever import RAGRetriever

        self._retriever = RAGRetriever(embedding_model=self.embedding_model)

    def query_context(
        self,
        issues: List[Dict],
        sensor_context: Optional[str] = None,
        k: int = 3,
    ) -> Dict:
        self._lazy_init()
        issue_types = {i["type"] for i in issues} if issues else set()
        if sensor_context:
            query = f"{sensor_context}. Issues: {', '.join(issue_types)}" if issue_types else sensor_context
        else:
            query = f"sensor anomalous reading {', '.join(issue_types)}" if issue_types else "greenhouse sensor normal operation"
        result = self._retriever.retrieve(query, k=k)
        formatted = self._retriever.format_results(result)
        evidence = []
        for ev in formatted.get("evidence", []):
            evidence.append({
                "source": ev.get("source", "unknown"),
                "chunk_id": ev.get("chunk_id", "unknown"),
                "relevance_score": ev.get("relevance_score", 0),
            })
        return {"evidence": evidence}

    def format_rag_context(self, rag_result: Dict) -> str:
        if not rag_result.get("evidence"):
            return "No relevant knowledge base entries found."
        lines = []
        for i, ev in enumerate(rag_result["evidence"], 1):
            source = ev.get("source", "unknown")
            cid = ev.get("chunk_id", "unknown")
            score = ev.get("relevance_score", 0)
            lines.append(f"[{i}] [{source}] #{cid} (score={score:.3f})")
        return "\n".join(lines)
