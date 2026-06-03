class AgentLoop:

    def __init__(
        self,
        planner,
        executor,
        observer
    ):
        self.planner = planner
        self.executor = executor
        self.observer = observer

    def run(self, state):

        while True:

            print(f"\n--- Step {state.step_count} ---")

            action = self.planner.plan(state)

            print("Action:")
            print(action)

            if action is None:
                print("Planner returned None. Stopping.")
                break

            if action["tool"] == "system" and action["method"] == "stop":
                print("Stopping agent.")
                break
                

            result = self.executor.execute(action)

            tool_name = action["tool"]
            tool = self.executor.tools[tool_name]

            observation = self.observer.observe(tool)

            state.history.append(action)
            state.observation = observation
            state.last_result = result
            state.step_count += 1

            print("\nObservation:")
            print(observation)