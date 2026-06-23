from typing import TypedDict, Any
from langgraph.graph import StateGraph, END


class GraphState(TypedDict):
    goal: str
    history: list
    observation: Any
    step_count: int

    response: Any
    result: Any


class NexaGraph:

    def __init__(
        self,
        planner,
        executor,
        tools
    ):
        self.planner = planner
        self.executor = executor
        self.tools = tools

        builder = StateGraph(GraphState)

        builder.add_node(
            "planner",
            self.planner_node
        )

        builder.add_node(
            "tool",
            self.tool_node
        )

        builder.add_node(
            "observe",
            self.observe_node
        )

        builder.set_entry_point(
            "planner"
        )

        builder.add_conditional_edges(
            "planner",
            self.should_continue,
            {
                "tool": "tool",
                "end": END
            }
        )

        builder.add_edge(
            "tool",
            "observe"
        )

        builder.add_edge(
            "observe",
            "planner"
        )

        self.graph = builder.compile()

    def planner_node(
        self,
        state: GraphState
    ):

        response = self.planner.plan(
            state
        )

        print("\n[PLANNER CONTENT]")
        print(response.content)

        print("\n[PLANNER TOOL CALLS]")
        print(response.tool_calls)

        return {
            "response": response
        }

    def should_continue(
        self,
        state: GraphState
    ):

        response = state["response"]

        if not response.tool_calls:

            print("\n[TASK COMPLETED]")

            if response.content:
                print(response.content)

            return "end"

        return "tool"

    def tool_node(
        self,
        state: GraphState
    ):

        response = state["response"]

        result = self.executor.execute(
            response
        )

        print("\n[TOOL RESULT]")
        print(result)

        return {
            "result": result
        }

    def observe_node(
        self,
        state: GraphState
    ):

        response = state["response"]

        tool_name = (
            response.tool_calls[0]["name"]
        )
        print(tool_name)
        result = state["result"]

        try:

            if tool_name.startswith(
                "browser_"
            ):

                observation = (
                    self.tools["browser"].observe()
                )

            elif tool_name in [
                "open_app",
                "switch_window",
                "type_text",
                "press_key"
            ]:

                if hasattr(
                    self.tools["desktop"],
                    "observe"
                ):

                    observation = (
                        self.tools["desktop"]
                        .observe()
                    )

                else:
                    observation = result

            else:

                observation = result

        except Exception:

            observation = result

        history = list(
            state["history"]
        )

        history.append(
            {
                "tool": tool_name,
                "args": response.tool_calls[0]["args"],
                "result": result
            }
        )

        print("\n[OBSERVATION]")
        print(observation)

        return {
            "observation": observation,
            "history": history[-10:],
            "step_count":
                state["step_count"] + 1
        }

    def run(
        self,
        goal: str
    ):

        return self.graph.invoke(
            {
                "goal": goal,
                "history": [],
                "observation": {},
                "step_count": 0,
                "response": None,
                "result": None
            }
        )