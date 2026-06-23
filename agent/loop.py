import time

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

            if DEBUG:

                print("\n[PLANNER CONTENT]")
                print(response.content)

                print("\n[PLANNER TOOL CALLS]")
                print(response.tool_calls)

            # ==================================================
            # COMPLETION CHECK
            # ==================================================

            if not response.tool_calls:

                print("\n[TASK COMPLETED]")

                print(response.content)

                break

            try:

                result = self.executor.execute(
                    response
                )

            except Exception as e:

                print(f"\n[ERROR]\n{str(e)}")

                if DEBUG:

                    import traceback
                    traceback.print_exc()

                continue

            time.sleep(2)

            # ==================================================
            # OBSERVATION
            # ==================================================

            observation = result

            state.observation = observation

            state.history.append(
                {
                    "tool_calls": response.tool_calls,
                    "content": response.content
                }
            )

            state.step_count += 1

            if DEBUG:

                print("\n[OBSERVATION]")
                print(observation)

            # ==================================================
            # SAFETY LIMIT
            # ==================================================

            if state.step_count >= 20:

                print("\n[ERROR]")
                print("Max steps reached")

                break