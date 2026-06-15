from tools.browser import BrowserTool
from tools.desktop import DesktopTool
from tools.filesystem import FileSystemTool
from tools.search import SearchTool
from execution.executor import Executor

from observation.observer import Observer

from llm.groq_client import GroqClient
from llm.planner import Planner

from agent.state import AgentState
from agent.loop import AgentLoop
from dotenv import load_dotenv
import os
load_dotenv()
def main():

    goal = input("Enter Goal: ")

    browser = BrowserTool()
    desktop = DesktopTool()
    fileSystem = FileSystemTool()
    search = SearchTool()

    tools = {
        "browser": browser,
        "desktop": desktop,
        "filesystem": fileSystem,
        "search": search
        
        
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