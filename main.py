
from tools.browser import BrowserTool
search = SearchTool()
knowledge = KnowledgeTool()
browser = BrowserTool()
desktop = DesktopTool()
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
from tools.desktop import DesktopTool
from tools.filesystem import FileSystemTool
from tools.search import SearchTool
from tools.knowledge import KnowledgeTool
from execution.executor import Executor

from observation.observer import Observer

from llm.groq_client import GroqClient
from llm.planner import Planner

from agent.state import AgentState
from agent.loop import AgentLoop
from dotenv import load_dotenv
import os
load_dotenv()
fileSystem = FileSystemTool()
set_filesystem_tool(
    fileSystem
)
set_knowledge_tool(
    knowledge
)
set_browser_tool(browser)
set_desktop_tool(desktop)
def main():

    goal = input("Enter Goal: ")
    tools = {
        "browser": browser,
        "desktop": desktop,
        "filesystem": fileSystem,
        "search": search,
        "knowledge": knowledge
        
        
    }

    executor = Executor(tools)

    llm = GroqClient(
        api_key=os.getenv("GROQ_API_KEY")
    )

    planner = Planner(llm)

    state = AgentState(goal)

    loop = AgentLoop(
        planner,
        executor,
        tools
    )

    loop.run(state)
    input("\nPress Enter to close browser...")


if __name__ == "__main__":
    main()