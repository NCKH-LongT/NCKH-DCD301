from sentence_transformers import SentenceTransformer
import os

class Embedder:
    def __init__(self, model_name='all-mpnet-base-v2'):
        self.model_name = model_name
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("Model loaded successfully.")

    def embed_text(self, text):
        """
        Convert text to a vector embedding.
        Returns a list of floats.
        """
        embedding = self.model.encode(text)
        return embedding.tolist()

    def embed_texts(self, texts):
        """
        Convert a list of texts to a list of vector embeddings.
        """
        embeddings = self.model.encode(texts)
        return [emb.tolist() for emb in embeddings]
