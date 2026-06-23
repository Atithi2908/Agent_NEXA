from langchain_groq import ChatGroq


class GroqClient(ChatGroq):

    def __init__(self, api_key):

        super().__init__(
            model="qwen/qwen3-32b",
            api_key=api_key,
            temperature=0,
            reasoning_effort="none"
        )