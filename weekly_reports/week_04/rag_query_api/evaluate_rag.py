"""
RAG Evaluation Script - Test retrieval quality with metrics
Week 4: Agent/Evaluation Engineer Task

Measures:
- Recall@k: Fraction of relevant docs retrieved in top-k
- MRR (Mean Reciprocal Rank): Rank of first relevant result
- Precision@k: Fraction of retrieved docs that are relevant
- Average relevance score
- Latency
"""

import json
import time
import logging
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict

from rag_query_api.rag_retriever import RAGRetriever

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TestQuery:
    """A test query with expected relevant sources"""
    query: str
    expected_topics: List[str]  # Expected metadata topics
    expected_sources: List[str]  # Expected source documents
    category: str  # normal, warning, critical, fault


@dataclass
class QueryResult:
    """Result of a single test query"""
    query: str
    category: str
    retrieved_topics: List[str]
    retrieved_sources: List[str]
    relevance_scores: List[float]
    recall_at_k: float
    precision_at_k: float
    mrr: float
    avg_relevance: float
    latency_ms: float
    passed: bool


# ============================================================================
# Test Queries (prepared in advance)
# ============================================================================

TEST_QUERIES = [
    TestQuery(
        query="What is the optimal temperature for tomato plants?",
        expected_topics=["temperature"],
        expected_sources=["greenhouse_guidelines.pdf"],
        category="normal"
    ),
    TestQuery(
        query="temperature too high in greenhouse what to do",
        expected_topics=["temperature", "temperature_action"],
        expected_sources=["greenhouse_guidelines.pdf", "ventilation_guide.pdf"],
        category="warning"
    ),
    TestQuery(
        query="extreme heat above 38 degrees greenhouse emergency",
        expected_topics=["temperature_action", "temperature"],
        expected_sources=["ventilation_guide.pdf", "greenhouse_guidelines.pdf"],
        category="critical"
    ),
    TestQuery(
        query="When should I water my plants soil moisture dry",
        expected_topics=["soil_moisture", "irrigation_action"],
        expected_sources=["irrigation_manual.pdf"],
        category="normal"
    ),
    TestQuery(
        query="humidity high fungal disease prevention greenhouse",
        expected_topics=["humidity", "disease"],
        expected_sources=["greenhouse_guidelines.pdf", "disease_prevention.pdf"],
        category="warning"
    ),
    TestQuery(
        query="sensor stuck at same value not changing fault",
        expected_topics=["sensor_maintenance"],
        expected_sources=["sensor_calibration.pdf"],
        category="fault"
    ),
    TestQuery(
        query="light intensity too high shade cloth needed",
        expected_topics=["light"],
        expected_sources=["lighting_guide.pdf"],
        category="warning"
    ),
    TestQuery(
        query="low humidity below 30 percent water stress",
        expected_topics=["humidity"],
        expected_sources=["greenhouse_guidelines.pdf"],
        category="warning"
    ),
    TestQuery(
        query="soil moisture above 70 percent waterlogging root rot",
        expected_topics=["soil_moisture"],
        expected_sources=["irrigation_manual.pdf"],
        category="critical"
    ),
    TestQuery(
        query="greenhouse ventilation fan cooling system",
        expected_topics=["temperature_action", "temperature"],
        expected_sources=["ventilation_guide.pdf"],
        category="normal"
    ),
]


# ============================================================================
# Evaluation Metrics
# ============================================================================

class RAGEvaluator:
    """Evaluates RAG retrieval quality"""

    def __init__(self, retriever: RAGRetriever, k: int = 3):
        self.retriever = retriever
        self.k = k

    def compute_recall_at_k(
        self,
        retrieved_topics: List[str],
        expected_topics: List[str]
    ) -> float:
        """Recall@k = |relevant ∩ retrieved| / |relevant|"""
        if not expected_topics:
            return 1.0
        relevant_retrieved = set(retrieved_topics) & set(expected_topics)
        return len(relevant_retrieved) / len(expected_topics)

    def compute_precision_at_k(
        self,
        retrieved_topics: List[str],
        expected_topics: List[str]
    ) -> float:
        """Precision@k = |relevant ∩ retrieved| / k"""
        if self.k == 0:
            return 0.0
        relevant_retrieved = set(retrieved_topics) & set(expected_topics)
        return len(relevant_retrieved) / self.k

    def compute_mrr(
        self,
        retrieved_topics: List[str],
        expected_topics: List[str]
    ) -> float:
        """MRR = 1/rank of first relevant result (0 if none)"""
        for rank, topic in enumerate(retrieved_topics, 1):
            if topic in expected_topics:
                return 1.0 / rank
        return 0.0

    def evaluate_query(self, test: TestQuery) -> QueryResult:
        """Run evaluation on a single test query"""
        result = self.retriever.retrieve(test.query, k=self.k)

        retrieved_topics = [
            c.metadata.get('topic', 'unknown')
            for c in result.results
        ]
        retrieved_sources = [c.source for c in result.results]
        relevance_scores = [c.relevance_score for c in result.results]

        recall = self.compute_recall_at_k(
            retrieved_topics, test.expected_topics
        )
        precision = self.compute_precision_at_k(
            retrieved_topics, test.expected_topics
        )
        mrr = self.compute_mrr(retrieved_topics, test.expected_topics)
        avg_rel = sum(relevance_scores) / max(len(relevance_scores), 1)

        # Pass if recall >= 0.5 (at least half of expected topics found)
        passed = recall >= 0.5

        return QueryResult(
            query=test.query,
            category=test.category,
            retrieved_topics=retrieved_topics,
            retrieved_sources=retrieved_sources,
            relevance_scores=relevance_scores,
            recall_at_k=round(recall, 4),
            precision_at_k=round(precision, 4),
            mrr=round(mrr, 4),
            avg_relevance=round(avg_rel, 4),
            latency_ms=result.latency_ms,
            passed=passed
        )

    def evaluate_all(self, tests: List[TestQuery]) -> Dict:
        """Run evaluation on all test queries"""
        results = []
        for test in tests:
            logger.info(f"Evaluating: '{test.query[:50]}...' [{test.category}]")
            qr = self.evaluate_query(test)
            results.append(qr)

        # Aggregate metrics
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        avg_recall = sum(r.recall_at_k for r in results) / total
        avg_precision = sum(r.precision_at_k for r in results) / total
        avg_mrr = sum(r.mrr for r in results) / total
        avg_relevance = sum(r.avg_relevance for r in results) / total
        avg_latency = sum(r.latency_ms for r in results) / total

        # By category
        categories = {}
        for r in results:
            cat = r.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r)

        category_summary = {}
        for cat, cat_results in categories.items():
            n = len(cat_results)
            category_summary[cat] = {
                "count": n,
                "avg_recall": round(sum(r.recall_at_k for r in cat_results) / n, 4),
                "avg_mrr": round(sum(r.mrr for r in cat_results) / n, 4),
                "pass_rate": f"{sum(1 for r in cat_results if r.passed)}/{n}"
            }

        return {
            "config": {
                "k": self.k,
                "mode": "pgvector",
                "num_test_queries": total
            },
            "aggregate": {
                "pass_rate": f"{passed}/{total}",
                "avg_recall_at_k": round(avg_recall, 4),
                "avg_precision_at_k": round(avg_precision, 4),
                "avg_mrr": round(avg_mrr, 4),
                "avg_relevance_score": round(avg_relevance, 4),
                "avg_latency_ms": round(avg_latency, 2)
            },
            "by_category": category_summary,
            "results": [asdict(r) for r in results]
        }


# ============================================================================
# Main
# ============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate RAG Retrieval")
    parser.add_argument("--k", type=int, default=3, help="Top-k results")
    parser.add_argument("--output", default=None,
                        help="Output JSON file path")
    args = parser.parse_args()

    print("\n" + "="*60)
    print("RAG EVALUATION - Week 4")
    print("="*60)

    # Initialize (will raise error if no vector DB)
    retriever = RAGRetriever()
    evaluator = RAGEvaluator(retriever, k=args.k)

    # Run evaluation
    print(f"\nRunning {len(TEST_QUERIES)} test queries (k={args.k})...")
    results = evaluator.evaluate_all(TEST_QUERIES)

    # Print summary
    agg = results['aggregate']
    print(f"\n📊 RESULTS SUMMARY")
    print(f"   Mode: {results['config']['mode']}")
    print(f"   Pass rate: {agg['pass_rate']}")
    print(f"   Avg Recall@{args.k}: {agg['avg_recall_at_k']}")
    print(f"   Avg Precision@{args.k}: {agg['avg_precision_at_k']}")
    print(f"   Avg MRR: {agg['avg_mrr']}")
    print(f"   Avg Relevance: {agg['avg_relevance_score']}")
    print(f"   Avg Latency: {agg['avg_latency_ms']}ms")

    print(f"\n📊 BY CATEGORY")
    for cat, summary in results['by_category'].items():
        print(f"   {cat}: {summary}")

    # Print individual results
    print(f"\n📋 INDIVIDUAL RESULTS")
    for r in results['results']:
        status = "✅" if r['passed'] else "❌"
        print(f"   {status} [{r['category']:8s}] Recall={r['recall_at_k']:.2f} "
              f"MRR={r['mrr']:.2f} | {r['query'][:60]}...")

    # Save to file
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n📁 Results saved to: {args.output}")

    print("\n✅ Evaluation complete!")


if __name__ == "__main__":
    main()
