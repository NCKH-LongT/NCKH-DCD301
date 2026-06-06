"""
RAG Retriever - Logic truy xuất dữ liệu cho hệ thống RAG
Tuần 4: Task của Agent/Evaluation Engineer

Xử lý:
- Kết nối với Vector Database (pgvector) thông qua DBHandler
- Tạo embedding cho câu truy vấn sử dụng Embedder (Sentence-Transformers)
- Truy xuất các đoạn văn bản (chunks) liên quan nhất dựa trên độ tương đồng cosine
- Định dạng kết quả trả về kèm theo metadata
"""

import os
import logging
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
import psycopg2
from psycopg2.extras import RealDictCursor

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class RetrievedChunk:
    """Một đoạn văn bản được truy xuất kèm thông tin về độ liên quan"""
    chunk_id: str
    source: str
    text: str
    relevance_score: float
    metadata: Dict


@dataclass
class RetrievalResult:
    """Kết quả tổng thể của một yêu cầu truy xuất RAG"""
    query: str
    results: List[RetrievedChunk]
    total_found: int
    latency_ms: float


class EmbeddingModel:
    """Embedding wrapper sử dụng sentence-transformers."""

    def __init__(self, model_name: str = 'all-mpnet-base-v2'):
        self.model_name = model_name
        self._model = None

    def _load(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:
                raise RuntimeError(
                    'sentence-transformers is required. '
                    'Install it with: pip install sentence-transformers'
                ) from exc
            self._model = SentenceTransformer(self.model_name)

    def embed_text(self, text: str) -> List[float]:
        self._load()
        vector = self._model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        self._load()
        vectors = self._model.encode(texts, normalize_embeddings=True)
        return [v.tolist() for v in vectors]


class VectorDB:
    """Minimal client for PostgreSQL + pgvector."""

    def __init__(self):
        self.dsn = (
            f"host={os.getenv('PG_HOST', 'localhost')} "
            f"port={int(os.getenv('PG_PORT', '5432'))} "
            f"dbname={os.getenv('PG_DBNAME', 'dcd_rag')} "
            f"user={os.getenv('PG_USER', 'postgres')} "
            f"password={os.getenv('PG_PASSWORD', 'postgres')}"
        )
        self.table = os.getenv('PG_TABLE', 'document_embeddings')

    def similarity_search(self, query_vector: List[float], top_k: int = 3) -> List[Dict]:
        """Search for top-k similar vectors using cosine distance (<=>)."""
        try:
            with psycopg2.connect(self.dsn) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    # Vector cosine distance: smaller is more similar
                    # pgvector <=> is cosine distance (1 - cosine_similarity)
                    cur.execute(
                        f"SELECT (metadata->>'chunk_id') as chunk_id, (metadata->>'source') as source, content as text, metadata, "
                        f"1 - (embedding <=> %s::vector) as score "
                        f"FROM {self.table} "
                        f"ORDER BY embedding <=> %s::vector "
                        f"LIMIT %s",
                        (query_vector, query_vector, top_k),
                    )
                    return cur.fetchall()
        except Exception as e:
            logger.error(f"pgvector similarity_search error: {e}")
            return []

    def get_count(self) -> int:
        """Get the total number of embeddings in the table."""
        try:
            with psycopg2.connect(self.dsn) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT count(*) FROM {self.table}")
                    return cur.fetchone()[0]
        except Exception as e:
            logger.error(f"pgvector get_count error: {e}")
            return 0


class RAGRetriever:
    """Truy xuất các đoạn văn bản liên quan từ Vector Database (PostgreSQL + pgvector)."""
    def __init__(self, embedding_model: str = 'all-mpnet-base-v2'):
        self.embedder = EmbeddingModel(model_name=embedding_model)
        self.db = VectorDB()
        logger.info("✓ Đã khởi tạo RAGRetriever với pgvector.")

    def _retrieve_vector(
        self,
        query: str,
        k: int = 3,
        score_threshold: float = 0.0,
    ) -> List[RetrievedChunk]:
        """Truy xuất các đoạn văn bản liên quan từ pgvector."""
        query_vector = self.embedder.embed_text(query)
        rows = self.db.similarity_search(query_vector=query_vector, top_k=k)
        chunks = []
        for row in rows:
            if row['score'] >= score_threshold:
                chunks.append(
                    RetrievedChunk(
                        chunk_id=row.get('chunk_id', 'unknown'),
                        source=row.get('source', 'unknown'),
                        text=row.get('text', ''),
                        relevance_score=round(float(row.get('score', 0)), 4),
                        metadata=row.get('metadata', {}),
                    )
                )
        return chunks

    def retrieve(
        self,
        query: str,
        k: int = 3,
        score_threshold: float = 0.0,
    ) -> RetrievalResult:
        """Hàm chính để thực hiện truy xuất RAG."""
        start_time = time.time()
        results = self._retrieve_vector(query, k, score_threshold)
        latency_ms = (time.time() - start_time) * 1000
        return RetrievalResult(
            query=query,
            results=results,
            total_found=len(results),
            latency_ms=round(latency_ms, 2),
        )

    def format_results(
        self,
        result: RetrievalResult,
        include_text: bool = True,
    ) -> Dict:
        """Định dạng kết quả truy xuất để trả về cho API."""
        evidence = []
        for chunk in result.results:
            entry: Dict = {
                'source': chunk.source,
                'chunk_id': chunk.chunk_id,
                'relevance_score': chunk.relevance_score,
                'metadata': chunk.metadata,
            }
            if include_text:
                if len(chunk.text) > 200:
                    entry['text_snippet'] = chunk.text[:200] + '...'
                else:
                    entry['text_snippet'] = chunk.text
            evidence.append(entry)
        return {
            'query': result.query,
            'total_found': result.total_found,
            'latency_ms': result.latency_ms,
            'evidence': evidence,
        }
