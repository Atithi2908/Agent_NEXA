from tools.knowledge import KnowledgeTool

knowledge = KnowledgeTool()

result = knowledge.retrieve(
    "What technologies have I worked with?"
)

print(result)
knowledge.qdrant.close()