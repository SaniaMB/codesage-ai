import requests


class EmbeddingClient:

    MODEL = "nomic-embed-text"

    def embed(self, text: str):

        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={
                "model": self.MODEL,
                "prompt": text
            }
        )

        if response.status_code != 200:
            print("FAILED!")
            print(response.text)
            response.raise_for_status()

        return response.json()["embedding"]