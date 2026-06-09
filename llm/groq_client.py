from groq import Groq
class GroqClient:

    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def generate(self, prompt):

        response = self.client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            
        )

        return response.choices[0].message.content