import ollama 

class Embedder:
    
    MODEL_NAME = "nomic-embed-text"
    
    def __init__(self):
        pass
    
    def embed(self,text):
        
        response = ollama.embeddings(
            model= self.MODEL_NAME,
            prompt = text
        )
    
        return response["embedding"]