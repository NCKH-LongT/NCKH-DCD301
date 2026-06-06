#!/usr/bin/env python3
"""
RAG Query - Command-line interface for querying agricultural knowledge base
Week 4: Agent/Evaluation Engineer Task

Usage:
  python rag_query.py "high temperature in greenhouse"
  python rag_query.py --api "temperature too high" --k 5
"""

import sys
import os
import json
import argparse

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag_query_api.rag_retriever import RAGRetriever


def main():
    parser = argparse.ArgumentParser(
        description="Query the agricultural RAG knowledge base"
    )
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--k", type=int, default=3, help="Number of results")
    parser.add_argument("--api", action="store_true",
                        help="Use API mode (start server)")
    parser.add_argument("--host", default="0.0.0.0", help="API host")
    parser.add_argument("--port", type=int, default=8000, help="API port")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--db-path", help="Path to ChromaDB directory")

    args = parser.parse_args()

    # API mode: start the server
    if args.api:
        from rag_query_api.app import create_app
        import uvicorn

        print(f"🚀 Starting RAG Query API on {args.host}:{args.port}")
        print(f"   Mode: REAL VECTOR DB (requires rag_ingest.py to be run first)")

        app = create_app(
            embedding_model="all-mpnet-base-v2"
        )
        uvicorn.run(app, host=args.host, port=args.port)
        return

    # CLI mode: run a single query
    if not args.query:
        parser.print_help()
        return

    retriever = RAGRetriever(
        embedding_model="all-mpnet-base-v2"
    )

    result = retriever.retrieve(args.query, k=args.k)
    formatted = retriever.format_results(result)

    if args.json:
        print(json.dumps(formatted, indent=2, ensure_ascii=False))
    else:
        print(f"\n📝 Query: '{formatted['query']}'")
        print(f"   Found: {formatted['total_found']} chunks "
              f"({formatted['latency_ms']}ms)")
        print()

        for i, item in enumerate(formatted['evidence'], 1):
            print(f"  [{i}] {item['source']}")
            print(f"      Chunk: {item['chunk_id']}")
            print(f"      Score: {item['relevance_score']:.4f}")
            if 'text_snippet' in item:
                print(f"      Text: {item['text_snippet']}")
            print()


if __name__ == "__main__":
    main()
