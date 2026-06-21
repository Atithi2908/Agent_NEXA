from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)


class QdrantManager:

    COLLECTION_NAME = "knowledge_base"
    VECTOR_SIZE = 768

    def __init__(self):

        self.client = QdrantClient(
            path="./data/qdrant"
        )

        self.create_collection()
        
    def close(self):
        self.client.close()
        
    def create_collection(self):

        collections = self.client.get_collections()

        existing_collections = [
            collection.name
            for collection in collections.collections
        ]

        if self.COLLECTION_NAME in existing_collections:
            return

        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=self.VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )

        print(
            f"Created collection: {self.COLLECTION_NAME}"
        )
    def insert_chunk(
    self,
    chunk_id,
    chunk_text,
    embedding,
    source
    ):

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=chunk_id,
                    vector=embedding,
                    payload={
                        "text": chunk_text,
                        "source": source
                    }
            )
        ]
    )
    
    def count_points(self):

        return self.client.count(
        collection_name=self.COLLECTION_NAME,
        exact=True
        ).count
        
    def search(
    self,
    query_embedding,
    limit=5
        ):

        results = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=query_embedding,
            limit=limit
    )

        return results.points
    
    def delete_source(
    self,
    source
):

        self.client.delete(
            collection_name=self.COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="source",
                        match=MatchValue(
                            value=source
                    )
                )
            ]
        )
    )