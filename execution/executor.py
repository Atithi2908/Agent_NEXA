import json

DEBUG = False


class Executor:
    def __init__(self, tools):
        self.tools = tools
    
    def execute(self, action):
        # Validate action is a dict
        if not isinstance(action, dict):
            if DEBUG:
                print(f"[ERROR] Action is not a dict: {action}")
            raise ValueError("Action must be a dictionary")
        
        tool_name = action.get("tool")
        if not tool_name:
            if DEBUG:
                print("[ERROR] Missing 'tool' field in action")
            raise ValueError("Action missing 'tool' field")
        
        if tool_name not in self.tools:
            if DEBUG:
                print(f"[ERROR] Tool '{tool_name}' not found")
            raise ValueError(f"Tool {tool_name} not found in executor")
        
        tool = self.tools[tool_name]
        method_name = action.get("method")
        
        if not method_name:
            if DEBUG:
                print("[ERROR] Missing 'method' field in action")
            raise ValueError("Action missing 'method' field")
        
        if not hasattr(tool, method_name):
            if DEBUG:
                print(f"[ERROR] Method '{method_name}' not found in tool '{tool_name}'")
            raise ValueError(f"Method {method_name} not found in tool {tool_name}")
        
        method = getattr(tool, method_name)
        params = action.get("params", {})
        
        try:
            result = method(**params)
            if DEBUG:
                print(f"[DEBUG] Action executed successfully: {tool_name}.{method_name}({params})")
            return result
        except KeyError as e:
            error_msg = f"Missing parameter in action: {str(e)}"
            if DEBUG:
                print(f"[ERROR] {error_msg}")
            raise ValueError(error_msg)
        except TypeError as e:
            error_msg = f"Invalid parameters for {tool_name}.{method_name}: {str(e)}"
            if DEBUG:
                print(f"[ERROR] {error_msg}")
            raise ValueError(error_msg)
        except ValueError as e:
            if DEBUG:
                print(f"[ERROR] Validation error: {str(e)}")
            raise
        except Exception as e:
            error_msg = f"Execution failed for {tool_name}.{method_name}({params}): {str(e)}"
            if DEBUG:
                print(f"[ERROR] {error_msg}")
            raise RuntimeError(error_msg)

    