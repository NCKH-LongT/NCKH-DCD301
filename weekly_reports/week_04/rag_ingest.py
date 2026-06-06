"""
RAG Ingest - Chunk and ingest documents into ChromaDB
Week 4: RAG Engineer Task

Handles:
- Reading documents from knowledge_base_docs/
- Chunking text using RecursiveCharacterTextSplitter
- Generating embeddings using sentence-transformers
- Storing in ChromaDB persistent store
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DocumentIngestor:
    """Ingests documents into ChromaDB vector store"""

    def __init__(
        self,
        knowledge_base_path: Optional[str] = None,
        vector_db_path: Optional[str] = None,
        collection_name: str = "greenhouse_knowledge",
        embedding_model: str = "all-MiniLM-L6-v2",
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        """
        Initialize the document ingestor.

        Args:
            knowledge_base_path: Path to knowledge_base_docs folder
            vector_db_path: Path to ChromaDB persistent directory
            collection_name: Name of collection to create
            embedding_model: sentence-transformers model name
            chunk_size: Max characters per chunk
            chunk_overlap: Overlap between chunks (characters)
        """
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Default paths
        script_dir = Path(__file__).parent
        self.knowledge_base_path = knowledge_base_path or str(
            script_dir / 'knowledge_base_docs'
        )
        self.vector_db_path = vector_db_path or str(
            script_dir / 'vector_db'
        )

        logger.info(f"Knowledge base: {self.knowledge_base_path}")
        logger.info(f"Vector DB: {self.vector_db_path}")

    def _load_documents(self) -> List[dict]:
        """Load all .txt/.md files from knowledge_base_docs"""
        docs = []
        kb_path = Path(self.knowledge_base_path)

        if not kb_path.exists():
            raise FileNotFoundError(
                f"Knowledge base path not found: {kb_path}\n"
                "Please create the knowledge_base_docs folder with documents."
            )

        # Supported extensions
        extensions = ['.txt', '.md']

        for ext in extensions:
            for file_path in kb_path.rglob(f'*{ext}'):
                # Determine category from folder name
                relative = file_path.relative_to(kb_path)
                category = relative.parts[0] if len(relative.parts) > 1 else 'general'

                # Read file content
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if content.strip():
                        docs.append({
                            'title': file_path.stem,
                            'content': content,
                            'source': str(file_path),
                            'category': category
                        })
                        logger.info(f"  Loaded: {file_path.name} ({category})")
                except Exception as e:
                    logger.warning(f"  Failed to read {file_path}: {e}")

        return docs

    def _chunk_text(self, text: str, title: str) -> List[dict]:
        """
        Chunk text using RecursiveCharacterTextSplitter.

        Args:
            text: Text to chunk
            title: Document title (for metadata)

        Returns:
            List of chunk dicts with text and metadata
        """
        try:
            from langchain.text_splitter import RecursiveCharacterTextSplitter
        except ImportError:
            logger.error("langchain not installed. Install with: pip install langchain")
            raise

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        # Split text
        splits = splitter.split_text(text)

        # Create chunks with metadata
        chunks = []
        for i, split in enumerate(splits):
            chunk_id = f"{title}_chunk_{i+1}"
            chunks.append({
                'id': chunk_id,
                'text': split,
                'metadata': {
                    'chunk_id': chunk_id,
                    'title': title,
                    'chunk_index': i + 1,
                    'total_chunks': len(splits)
                }
            })

        return chunks

    def ingest(self, force_recreate: bool = False):
        """
        Ingest all documents from knowledge_base_docs into PostgreSQL + pgvector.

        Args:
            force_recreate: If True, delete existing rows before insert
        """
        from sentence_transformers import SentenceTransformer
        try:
            import psycopg2
        except ImportError as exc:
            raise RuntimeError(
                'psycopg2-binary is required for pgvector ingest. '
                'Install it with: pip install psycopg2-binary'
            ) from exc

        # Load documents
        logger.info("=" * 60)
        logger.info("RAG INGEST - Starting document ingestion (pgvector)")
        logger.info("=" * 60)
        logger.info("\n[1/4] Loading documents...")
        documents = self._load_documents()
        if not documents:
            logger.warning("No documents found to ingest!")
            return
        logger.info(f"\nFound {len(documents)} documents")

        # Chunk all documents
        logger.info("\n[2/4] Chunking documents...")
        all_chunks = []
        for doc in documents:
            chunks = self._chunk_text(doc['content'], doc['title'])
            for chunk in chunks:
                chunk['metadata']['source'] = doc['source']
                chunk['metadata']['category'] = doc['category']
            all_chunks.extend(chunks)
        logger.info(
            f"Created {len(all_chunks)} chunks from {len(documents)} documents"
        )

        # Load embedding model
        logger.info(
            f"\n[3/4] Loading embedding model: {self.embedding_model_name}"
        )
        embedding_model = SentenceTransformer(self.embedding_model_name)

        # Generate embeddings
        logger.info("\n[4/4] Generating embeddings and upserting to pgvector...")
        texts = [chunk['text'] for chunk in all_chunks]
        
        # Generate embeddings in batches
        batch_size = 32
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            embeddings.extend(embedding_model.encode(batch).tolist())
            if (i + batch_size) % 100 == 0 or i + batch_size >= len(texts):
                logger.info(
                    f" Embedded {min(i + batch_size, len(texts))}/{len(texts)} chunks"
                )

        dsn = (
            f"host={os.getenv('PG_HOST', 'localhost')} "
            f"port={int(os.getenv('PG_PORT', '5432'))} "
            f"dbname={os.getenv('PG_DBNAME', 'dcd_rag')} "
            f"user={os.getenv('PG_USER', 'postgres')} "
            f"password={os.getenv('PG_PASSWORD', 'postgres')}"
        )
        pg_table = os.getenv('PG_TABLE', 'document_embeddings')

        with psycopg2.connect(dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"CREATE TABLE IF NOT EXISTS {pg_table} ("
                    "id BIGSERIAL PRIMARY KEY, chunk_id TEXT NOT NULL, "
                    "source TEXT NOT NULL, content TEXT NOT NULL, "
                    "metadata JSONB, embedding vector(384));"
                )
                cur.execute(
                    f"CREATE INDEX IF NOT EXISTS idx_{pg_table}_embedding "
                    f"ON {pg_table} USING ivfflat "
                    f"(embedding vector_cosine_ops) WITH (lists = 100);"
                )
                if force_recreate:
                    cur.execute(f"TRUNCATE {pg_table};")
                
                rows = []
                for chunk, emb in zip(all_chunks, embeddings):
                    rows.append((
                        chunk['metadata'].get('chunk_id'),
                        chunk['metadata'].get('source'),
                        chunk['text'],
                        json.dumps(chunk['metadata']),
                        emb,
                    ))
                
                cur.executemany(
                    f"INSERT INTO {pg_table} "
                    f"(chunk_id, source, content, metadata, embedding) "
                    f"VALUES (%s, %s, %s, %s, %s)",
                    rows,
                )
            conn.commit()

        logger.info("\n" + "=" * 60)
        logger.info(f"✓ Successfully ingested {len(all_chunks)} chunks")
        logger.info(f"✓ Table '{pg_table}' in database 'dcd_rag'")
        logger.info("=" * 60)
        return {
            'documents': len(documents),
            'chunks': len(all_chunks),
            'table': pg_table,
            'dbname': os.getenv('PG_DBNAME', 'dcd_rag'),
        }

def main():
    """Main entry point for rag_ingest.py"""
    import argparse

    parser = argparse.ArgumentParser(description='Ingest documents into pgvector')
    parser.add_argument(
        '--knowledge-base',
        help='Path to knowledge_base_docs folder'
    )
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=500,
        help='Max characters per chunk (default: 500)'
    )
    parser.add_argument(
        '--chunk-overlap',
        type=int,
        default=50,
        help='Overlap between chunks (default: 50)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Delete existing data and recreate'
    )

    args = parser.parse_args()

    ingestor = DocumentIngestor(
        knowledge_base_path=args.knowledge_base,
        vector_db_path='', # Not used for pgvector
        collection_name='', # Not used for pgvector
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap
    )

    result = ingestor.ingest(force_recreate=args.force)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()