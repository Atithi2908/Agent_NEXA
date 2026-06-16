class Chunker:

    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100

    def __init__(self):
        pass

    def chunk_text(self, text):

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.CHUNK_SIZE

            chunks.append(
                text[start:end]
            )

            start += (
                self.CHUNK_SIZE
                - self.CHUNK_OVERLAP
            )

        return chunks