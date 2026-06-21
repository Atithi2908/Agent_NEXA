from pathlib import Path
from uuid import uuid4

from rag.chunker import Chunker
from rag.embedder import Embedder
from rag.qdrant_manager import QdrantManager


class KnowledgeTool:

    def __init__(self):

        self.chunker = Chunker()
        self.embedder = Embedder()
        self.qdrant = QdrantManager()

    def add_document(self, path):

        try:

            path = Path(path)

            text = path.read_text(
                encoding="utf-8"
            )

            chunks = self.chunker.chunk_text(
                text
            )
            self.qdrant.delete_source(
            path.name
            )
            for chunk in chunks:

                embedding = self.embedder.embed(
                    chunk
                )

                self.qdrant.insert_chunk(
                    chunk_id=str(uuid4()),
                    chunk_text=chunk,
                    embedding=embedding,
                    source=path.name
                )

            return {
                "success": True,
                "file": path.name,
                "chunks_added": len(chunks)
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }
            
    def retrieve(
    self,
    question,
    limit=5
):

        try:

            query_embedding = self.embedder.embed(
            question
            )

            results = self.qdrant.search(
            query_embedding,
            limit
            )
            print(results)

            chunks = []

            for result in results:

                chunks.append({
                "score": result.score,
                "text": result.payload["text"],
                "source": result.payload["source"]
                })

            return {
            "success": True,
            "question": question,
            "chunks": chunks
            }

        except Exception as e:

            return {
            "success": False,
            "error": str(e)
        }