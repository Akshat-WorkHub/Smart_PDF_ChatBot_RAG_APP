from qdrant_client import QdrantClient

client = QdrantClient(
    host="localhost",
    port=6333
)

print("Connected Successfully")

print(client.get_collections())