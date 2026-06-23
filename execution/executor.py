DEBUG = True


class Executor:

    def __init__(self, tools):

        self.tool_map = {}

        for tool in tools:
            self.tool_map[tool.name] = tool

    def execute(self, response):

        if not response.tool_calls:

            if DEBUG:
                print("[EXECUTOR] No tool calls found")

            return None

        if len(response.tool_calls) > 1:

            raise ValueError(
                "Multiple tool calls returned. NEXA currently supports one action per step."
            )

        tool_call = response.tool_calls[0]

        tool_name = tool_call["name"]

        args = tool_call["args"]

        if DEBUG:

            print("\n[EXECUTOR]")
            print(f"Tool: {tool_name}")
            print(f"Args: {args}")

        if tool_name not in self.tool_map:

            raise ValueError(
                f"Tool '{tool_name}' not registered"
            )

        tool = self.tool_map[tool_name]

        result = tool.invoke(args)

        if DEBUG:

            print("\n[TOOL RESULT]")
            print(result)

        return result