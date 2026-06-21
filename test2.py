from rag.qdrant_manager import QdrantManager

qdrant = QdrantManager()

points, _ = qdrant.client.scroll(
    collection_name=qdrant.COLLECTION_NAME,
    limit=100,
    with_payload=True,
    with_vectors=False
)

for i, point in enumerate(points, start=1):
    print(f"\n--- CHUNK {i} ---")
    print("SOURCE:", point.payload.get("source"))
    print("TEXT:")
    print(point.payload.get("text"))