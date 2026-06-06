"""
RAG Query API - FastAPI server for querying agricultural knowledge base
Week 4: Agent/Evaluation Engineer Task

Endpoints:
- POST /api/rag/query - Query knowledge base
- GET  /api/rag/health - Health check
"""

import os
import sys
import logging
from typing import Optional, List

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from fastapi import FastAPI, HTTPException, Query
    from pydantic import BaseModel, Field
    import uvicorn
except ImportError:
    # Fallback: use Flask if FastAPI not available
    FastAPI = None

from rag_query_api.rag_retriever import RAGRetriever

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# Data Models
# ============================================================================

class QueryRequest(BaseModel):
    """RAG query request"""
    query: str = Field(..., description="The search query text")
    k: int = Field(default=3, ge=1, le=20, description="Number of results")
    score_threshold: float = Field(default=0.0, ge=0.0, le=1.0,
                                   description="Minimum relevance score")
    include_text: bool = Field(default=True,
                               description="Include text snippets in response")


class EvidenceItem(BaseModel):
    """Single evidence item in response"""
    source: str
    chunk_id: str
    relevance_score: float
    text_snippet: Optional[str] = None
    metadata: dict = {}


class RAGQueryResponse(BaseModel):
    """RAG query response"""
    success: bool
    query: str
    total_found: int
    latency_ms: float
    evidence: List[EvidenceItem] = []


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str = "1.0.0"
    retriever_mode: str
    collection: Optional[str] = None
    chunks_count: Optional[int] = None


# ============================================================================
# App Factory
# ============================================================================

def create_app(
    embedding_model: str = 'all-mpnet-base-v2'
):
    """
    Create and configure the FastAPI application.

    Args:
        embedding_model: Tên model sentence-transformers để tạo embedding

    Raises:
        ImportError: If FastAPI is not installed
        RuntimeError: If vector DB connection fails
    """
    if FastAPI is None:
        raise ImportError("FastAPI is not installed. Run: pip install fastapi uvicorn")

    app = FastAPI(
        title="RAG Query API",
        description="Retrieval-Augmented Generation Query API for Smart Agriculture",
        version="1.0.0"
    )

    # Initialize retriever (will raise error if no vector DB)
    retriever = RAGRetriever(
        embedding_model=embedding_model
    )

    @app.get("/api/rag/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint"""
        try:
            count = retriever.db.get_count()
            status = "ok"
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            status = "error"
            count = 0

        return HealthResponse(
            status=status,
            retriever_mode="pgvector",
            collection=retriever.db.table,
            chunks_count=count
        )

    @app.post("/api/rag/query", response_model=RAGQueryResponse)
    async def query_knowledge(request: QueryRequest):
        """
        Query the agricultural knowledge base.

        Returns relevant document chunks with similarity scores.
        """
        try:
            result = retriever.retrieve(
                query=request.query,
                k=request.k,
                score_threshold=request.score_threshold
            )

            formatted = retriever.format_results(
                result,
                include_text=request.include_text
            )

            evidence = []
            for item in formatted['evidence']:
                evidence.append(EvidenceItem(**item))

            return RAGQueryResponse(
                success=True,
                query=formatted['query'],
                total_found=formatted['total_found'],
                latency_ms=formatted['latency_ms'],
                evidence=evidence
            )

        except Exception as e:
            logger.error(f"Query error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/rag/query")
    async def query_knowledge_get(
        q: str = Query(..., description="Search query"),
        k: int = Query(3, ge=1, le=20),
        score_threshold: float = Query(0.0, ge=0.0, le=1.0)
    ):
        """Query knowledge base via GET (for quick testing)"""
        result = retriever.retrieve(
            query=q, k=k, score_threshold=score_threshold
        )
        formatted = retriever.format_results(result, include_text=True)
        return {
            "success": True,
            **formatted
        }

    return app


# ============================================================================
# CLI Entry Point
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="RAG Query API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    parser.add_argument("--embedding-model", default="all-mpnet-base-v2",
                        help="Embedding model name")

    args = parser.parse_args()

    logger.info(f"Starting RAG Query API on {args.host}:{args.port}")
    logger.info(f"Mode: REAL VECTOR DB (pgvector)")

    app = create_app(
        embedding_model=args.embedding_model
    )

    uvicorn.run(app, host=args.host, port=args.port)
