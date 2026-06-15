from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()


class SearchTool:

    def __init__(self):
        self.client = TavilyClient(
            api_key=os.getenv("TAVILY_API_KEY")
        )

    def search(self, query):

        try:

            response = self.client.search(
                query=query,
                search_depth="basic",
                max_results=2
            )

            sources = []

            for result in response.get("results", []):

                sources.append({
                    "title": result.get("title"),
                    "content": result.get("content")
                })

            return {
                "success": True,
                "query": query,
                "answer": response.get("answer", ""),
                "sources": sources
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }