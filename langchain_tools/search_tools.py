from langchain.tools import tool

search_tool = None


def set_search_tool(tool_instance):
    global search_tool
    search_tool = tool_instance


@tool
def search(query: str):
    """
    Search the web for current information.

    Use this tool when the answer is not available
    in memory or the knowledge base and requires
    internet search.
    """
    return search_tool.search(query)


SEARCH_TOOLS = [
    search
]