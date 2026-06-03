class Planner:

    def plan(self, state):

        if state.step_count == 0:
            return {
                "tool": "browser",
                "method": "navigate",
                "params": {
                    "url": "https://google.com"
                }
            }

        if state.step_count == 1:
            return {
                "tool": "browser",
                "method": "type",
                "params": {
                    "selector": "textarea",
                    "text": state.goal
                }
            }

        return {
            "tool": "system",
            "method": "stop",
            "params": {}
        }