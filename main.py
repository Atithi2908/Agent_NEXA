from tools.browser import BrowserTool

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

    tools = {
        "browser": browser
    }

    executor = Executor(tools)

    observation = browser.observe()

    llm = GroqClient(
        api_key=os.getenv("GROQ_API_KEY")
    )

    planner = Planner(llm)

    state = AgentState(goal)

    loop = AgentLoop(
        planner,
        executor,
        browser
    )

    loop.run(state)
    input("\nPress Enter to close browser...")
    browser.close()


if __name__ == "__main__":
    main()