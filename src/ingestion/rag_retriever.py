"""
RAG Retriever - Truy vấn vector database để lấy relevant chunks.

Sử dụng pgvector để thực hiện semantic search.
"""

from typing import List, Dict, Any, Optional

from src.database.db_handler import DBHandler
from src.embedding.embedder import Embedder


class RAGRetriever:
    """RAG Retriever class để query vector database."""

    def __init__(self, top_k: int = 3):
        """
        Initialize RAG Retriever.

        Args:
            top_k: Số lượng chunks tối đa trả về (default: 3)
        """
        self.top_k = top_k
        self.db = DBHandler()
        self.embedder = Embedder()

    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Truy vấn vector database để lấy relevant chunks.

        Args:
            query: Câu hỏi truy vấn
            top_k: Số lượng chunks trả về (override default)

        Returns:
            List of dict chứa content, metadata và similarity score
        """
        k = top_k or self.top_k

        # Embed query
        query_embedding = self.embedder.embed_text(query)

        # Search in vector DB
        results = self.db.vector_search(query_embedding, top_k=k)

        # Format results
        formatted_results = []
        for content, metadata, similarity_score in results:
            formatted_results.append({
                "content": content,
                "metadata": metadata,
                "score": similarity_score,
                "distance": 1.0 - similarity_score
            })

        return formatted_results

    def retrieve_with_context(
        self,
        query: str,
        top_k: Optional[int] = None,
        min_score: float = 0.0
    ) -> Dict[str, Any]:
        """
        Truy vấn và trả về kết quả với context được ghép lại.

        Args:
            query: Câu hỏi truy vấn
            top_k: Số lượng chunks trả về
            min_score: Ngưỡng similarity tối thiểu (0.0 - 1.0)

        Returns:
            Dict chứa:
                - chunks: List các chunks đã retrieve
                - context: Tất cả chunks ghép lại thành 1 string
                - sources: List source files
                - scores: List similarity scores
        """
        k = top_k or self.top_k
        results = self.retrieve(query, top_k=k)

        # Filter by min_score
        filtered_results = [r for r in results if r["score"] >= min_score]

        # Build context
        context_parts = []
        sources = []
        scores = []

        for r in filtered_results:
            context_parts.append(r["content"])
            if r["metadata"] and "source" in r["metadata"]:
                sources.append(r["metadata"]["source"])
            scores.append(r["score"])

        context = "\n\n---\n\n".join(context_parts)

        return {
            "chunks": filtered_results,
            "context": context,
            "sources": list(set(sources)),
            "scores": scores,
            "num_chunks": len(filtered_results)
        }

    def batch_retrieve(self, queries: List[str], top_k: Optional[int] = None) -> List[List[Dict[str, Any]]]:
        """
        Truy vấn nhiều câu hỏi cùng lúc.

        Args:
            queries: List các câu hỏi
            top_k: Số lượng chunks trả về cho mỗi query

        Returns:
            List của list results
        """
        return [self.retrieve(q, top_k) for q in queries]

    def close(self):
        """Đóng kết nối database."""
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    """Demo sử dụng RAG Retriever."""
    print("=" * 60)
    print("RAG Retriever - Demo")
    print("=" * 60)

    # Test queries
    test_queries = [
        "Cách điều chỉnh nhiệt độ trong nhà kính?",
        "Hệ thống tưới tiêu tự động hoạt động như thế nào?",
        "Cảm biến độ ẩm đất cần bảo trì như thế nào?"
    ]

    with RAGRetriever(top_k=3) as retriever:
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            print("-" * 40)

            try:
                results = retriever.retrieve(query)

                if not results:
                    print("  ❌ Không tìm thấy kết quả phù hợp")
                else:
                    print(f"  ✅ Tìm thấy {len(results)} kết quả:")
                    for i, r in enumerate(results, 1):
                        preview = r["content"][:100] + "..." if len(r["content"]) > 100 else r["content"]
                        print(f"    {i}. [Score: {r['score']:.4f}] {preview}")

            except Exception as e:
                print(f"  ❌ Error: {e}")

    print("\n" + "=" * 60)
    print("Demo hoàn tất")
    print("=" * 60)


if __name__ == "__main__":
    main()