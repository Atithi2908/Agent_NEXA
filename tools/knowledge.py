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