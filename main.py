from tools.browser import BrowserTool
from tools.desktop import DesktopTool
from tools.filesystem import FileSystemTool
from tools.search import SearchTool
from tools.knowledge import KnowledgeTool
from agent.graph import NexaGraph
from langchain_tools.browser_tools import (
    set_browser_tool
)
from langchain_tools.desktop_tools import (
    set_desktop_tool
)
from langchain_tools.filesystem_tools import (
    set_filesystem_tool
)
from langchain_tools.knowledge_tools import (
    set_knowledge_tool
)
from langchain_tools.search_tools import (
    set_search_tool
)

from langchain_tools.all_tools import ALL_TOOLS

from execution.executor import Executor

from llm.groq_client import GroqClient
from llm.planner import Planner

from dotenv import load_dotenv

import os

load_dotenv()


# =====================================================
# REAL TOOLS
# =====================================================

search = SearchTool()
knowledge = KnowledgeTool()
browser = BrowserTool()
desktop = DesktopTool()
fileSystem = FileSystemTool()


# =====================================================
# CONNECT REAL TOOLS TO LANGCHAIN WRAPPERS
# =====================================================

set_filesystem_tool(
    fileSystem
)

set_knowledge_tool(
    knowledge
)

set_search_tool(
    search
)

set_browser_tool(
    browser
)

set_desktop_tool(
    desktop
)


# =====================================================
# MAIN
# =====================================================

def main():

    goal = input("Enter Goal: ")

    tools = {
        "browser": browser,
        "desktop": desktop,
        "filesystem": fileSystem,
        "search": search,
        "knowledge": knowledge
    }

    llm = GroqClient(
        api_key=os.getenv("GROQ_API_KEY")
    )

    planner = Planner(
        llm
    )

    executor = Executor(
        ALL_TOOLS
    )


    graph = NexaGraph(
    planner,
    executor,
    tools
)
    print(browser.observe())
    graph.run(goal)

    input(
        "\nPress Enter to close browser..."
    )


if __name__ == "__main__":
    main()