import os
import psycopg2
from psycopg2.extras import execute_values, Json
from dotenv import load_dotenv

load_dotenv()

class DBHandler:
    def __init__(self):
        self.conn_params = {
            "dbname": os.getenv("DB_NAME", "dcd_rag"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", "123456"),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432")
        }
        self.conn = None

    def connect(self):
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(**self.conn_params)
        return self.conn

    def insert_documents(self, documents):
        """
        documents: List of tuples (content, embedding, metadata)
        """
        conn = self.connect()
        cur = conn.cursor()
        
        # SQL cho pgvector
        query = "INSERT INTO knowledge_base (content, embedding, metadata) VALUES %s"
        
        # Format data: content, embedding (list), metadata (dict)
        data = [(doc[0], doc[1], Json(doc[2])) for doc in documents]
        
        try:
            execute_values(cur, query, data)
            conn.commit()
            print(f"Successfully inserted {len(documents)} chunks into DB.")
        except Exception as e:
            conn.rollback()
            print(f"Error inserting documents: {e}")
            raise e
        finally:
            cur.close()

    def similarity_search(self, query_embedding, k=3):
        """
        Perform cosine similarity search using pgvector.
        Returns: List of tuples (content, distance, metadata)
        """
        conn = self.connect()
        cur = conn.cursor()
        
        # Sử dụng toán tử <=> cho cosine distance trong pgvector
        # Distance = 1 - cosine_similarity
        # Cần cast query_embedding thành vector type
        query = """
            SELECT content, embedding <=> %s::vector AS distance, metadata 
            FROM knowledge_base 
            ORDER BY distance ASC 
            LIMIT %s
        """
        
        try:
            cur.execute(query, (query_embedding, k))
            results = cur.fetchall()
            return results
        except Exception as e:
            print(f"Error during similarity search: {e}")
            raise e
        finally:
            cur.close()

    def vector_search(self, query_vector, top_k=3):
        """
        Tìm kiếm vector tương đồng và trả về kết quả với similarity score.
        Returns: List of tuples (content, metadata, similarity_score)
        """
        # similarity_search trả về (content, distance, metadata)
        # distance = 1 - cosine_similarity
        # similarity = 1 - distance = cosine_similarity
        results = self.similarity_search(query_vector, top_k)
        
        formatted_results = []
        for content, distance, metadata in results:
            similarity = 1.0 - float(distance)
            formatted_results.append((content, metadata, similarity))
        
        return formatted_results

    def close(self):
        if self.conn:
            self.conn.close()
