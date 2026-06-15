import time
import json

DEBUG = True


class AgentLoop:

    def __init__(
        self,
        planner,
        executor,
        tools
    ):
        self.planner = planner
        self.executor = executor
        self.tools = tools

    def run(self, state):

        print(f"\n[GOAL]\n{state.goal}")

        while True:

            if not DEBUG:
                print(f"\n[STEP {state.step_count}]")

            response = self.planner.plan(state)

            if response is None:
                print("\n[ERROR] Planner returned None")
                break

            if not DEBUG:
                print("\n[PLANNER RESPONSE]")
                print(json.dumps(response, indent=2))

            # Goal completed
            if response.get("status") == "completed":
                print("\n[TASK COMPLETED]")
                print(response.get("reason", "Goal achieved"))
                break

            try:
                result =  self.executor.execute(response)

                if not DEBUG:
                    print("\n[RESULT]\nsuccess")

            except Exception as e:

                print(f"\n[ERROR]\n{str(e)}")

                if DEBUG:
                    import traceback
                    traceback.print_exc()

                continue

            time.sleep(2)

            tool_used = response["tool"]
            tool = self.tools[tool_used]
            if hasattr(tool,"observe"):
                observation = tool.observe()
            else:
                observation = result
            
            state.observation = observation
            state.history.append(response)

            state.step_count += 1

            if DEBUG:
                print("\n[OBSERVATION]")
                print(json.dumps(observation, indent=2))

            if state.step_count >= 20:
                print("\n[ERROR]\nMax steps reached")
                break