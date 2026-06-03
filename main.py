from tools.browser import BrowserTool

from execution.executor import Executor

from observation.observer import Observer

from agent.planner import Planner

from agent.loop import AgentLoop

from agent.state import AgentState


def main():

    browser = BrowserTool()

    tools = {
        "browser": browser
    }

    executor = Executor(tools)

    observer = Observer()

    planner = Planner()

    loop = AgentLoop(
        planner,
        executor,
        observer
    )

    goal = input("Enter Goal: ")

    state = AgentState(
        goal=goal
    )

    loop.run(state)
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()