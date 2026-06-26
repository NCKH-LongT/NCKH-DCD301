import os
import glob
import re
import uuid
from pathlib import Path
from dotenv import load_dotenv

from src.database.db_handler import DBHandler
from src.embedding.embedder import Embedder

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DOCS_PATH = str(BASE_DIR / "document" / "IoT_Sensor_Pipeline" / "knowledge_base_docs")
MAX_TOKENS = 512
OVERLAP_TOKENS = 50

class RAGIngestor:
    def __init__(self, docs_path=None, max_tokens=MAX_TOKENS, overlap_tokens=OVERLAP_TOKENS):
        self.docs_path = docs_path or DEFAULT_DOCS_PATH
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        
        self.db = DBHandler()
        self.embedder = Embedder()
        self._tokenizer = None

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer(self.embedder.model_name)
            self._tokenizer = model.tokenizer
        return self._tokenizer

    def count_tokens(self, text):
        return len(self.tokenizer.encode(text))

    def split_text(self, text):
        """
        Chia văn bản thành các chunks với kích thước tối đa max_tokens.
        Hỗ trợ overlap giữa các chunks để giữ ngữ cảnh.
        """
        paragraphs = re.split(r'\n\s*\n', text.strip())
        chunks = []

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            if self.count_tokens(para) <= self.max_tokens:
                chunks.append(para)
            else:
                # Chia đoạn văn dài thành các câu
                sentences = re.split(r'(?<=[.!?])\s+', para)
                current = ""
                for sent in sentences:
                    candidate = current + " " + sent if current else sent
                    if self.count_tokens(candidate) <= self.max_tokens:
                        current = candidate
                    else:
                        if current:
                            chunks.append(current.strip())
                        current = sent
                if current:
                    chunks.append(current.strip())

        # Gộp các chunks nhỏ lại với nhau nếu không vượt quá max_tokens
        # (để tạo overlap tự nhiên)
        final_chunks = []
        for chunk in chunks:
            if final_chunks and self.count_tokens(final_chunks[-1] + " " + chunk) <= self.max_tokens:
                # Gộp với chunk trước đó
                final_chunks[-1] = final_chunks[-1] + " " + chunk
            else:
                final_chunks.append(chunk)

        return final_chunks

    def process_files(self):
        files = glob.glob(os.path.join(self.docs_path, "**/*.txt"), recursive=True) + \
                glob.glob(os.path.join(self.docs_path, "**/*.md"), recursive=True)

        print(f"Found {len(files)} documents to process.")
        all_chunks_to_insert = []
        chunk_idx = 0

        for file_path in files:
            # Handle Unicode file paths for Windows console
            try:
                print(f"  Processing: {file_path}")
            except UnicodeEncodeError:
                print(f"  Processing: {file_path.encode('ascii', 'replace').decode()}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                base_meta = {
                    "source": file_path,
                    "filename": os.path.basename(file_path),
                    "category": Path(file_path).parent.name
                }

                chunks = self.split_text(content)

                for chunk in chunks:
                    chunk_id = f"{uuid.uuid4().hex[:12]}"
                    metadata = {**base_meta, "chunk_id": chunk_id}
                    embedding = self.embedder.embed_text(chunk)
                    all_chunks_to_insert.append((chunk, embedding, metadata))
                    chunk_idx += 1

            except Exception as e:
                print(f"  Error processing {file_path}: {e}")

        print(f"Total chunks created: {len(all_chunks_to_insert)}")
        if all_chunks_to_insert:
            self.db.insert_documents(all_chunks_to_insert)
        else:
            print("No content to insert.")

    def run(self):
        print(f"RAG Ingest Pipeline")
        print(f"  Docs path: {self.docs_path}")
        print(f"  Max tokens per chunk: {self.max_tokens}")
        print(f"  Overlap tokens: {self.overlap_tokens}")
        print()
        try:
            self.process_files()
        finally:
            self.db.close()

if __name__ == "__main__":
    ingestor = RAGIngestor()
    ingestor.run()
