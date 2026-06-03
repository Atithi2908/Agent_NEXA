class Executor:
    def __init__(self,tools):
        self.tools = tools
    
    def execute(self,action):
        tool_name = action["tool"]
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found in executor.")
        tool = self.tools[tool_name]
        method_name = action["method"]
        if not hasattr(tool, method_name):
            raise ValueError(f"Method {method_name} not found in tool {tool_name}.")
        method = getattr(tool, method_name)
        params = action.get("params", {})
        result = method(**params)
        return result
    