from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="qwen2.5:3b"
)

prompt = ChatPromptTemplate.from_template(
"""
Answer the question.

Question:
{question}
"""
)

chain = prompt | llm

response = chain.invoke(
{
    "question":"What is Python?"
}
)

print(response.content)