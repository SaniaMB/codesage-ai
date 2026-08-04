import math

from app.engines.ai_engine.embedding_client import EmbeddingClient


class Retriever:

    def __init__(self):
        self.embedding_client = EmbeddingClient()

    def retrieve(self, repository_chunks, question, top_k=5):

        question_embedding = self.embedding_client.embed(question)

        scored_chunks = []

        for item in repository_chunks:

            similarity = self.cosine_similarity(
                question_embedding,
                item["embedding"]
            )

            scored_chunks.append({
                "chunk": item["chunk"],
                "score": similarity
            })

        scored_chunks.sort(
            key=lambda chunk: chunk["score"],
            reverse=True
        )

        return [
            item["chunk"] for item in scored_chunks[:top_k]
        ]

    def cosine_similarity(self, vector1, vector2):

        dot_product = sum(a * b for a, b in zip(vector1, vector2))

        magnitude1 = math.sqrt(sum(a * a for a in vector1))
        magnitude2 = math.sqrt(sum(b * b for b in vector2))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0

        return dot_product / (magnitude1 * magnitude2)