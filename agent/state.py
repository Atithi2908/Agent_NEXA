class AgentState:
    def __init__(self,goal):
        self.goal = goal
        self.history = []
        self.observation= {}
        self.last_result = {}
        self.step_count = 0
