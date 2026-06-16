from rag.chunker import Chunker

chunker = Chunker()

text = "A" * 1500

chunks = chunker.chunk_text(text)

print(
    f"Chunks: {len(chunks)}"
)

for i, chunk in enumerate(chunks):

    print(
        f"Chunk {i+1}: {len(chunk)} chars"
    )