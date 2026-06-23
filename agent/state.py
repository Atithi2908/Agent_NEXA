from typing import TypedDict


class GraphState(TypedDict):

    goal: str

    history: list

    observation: dict

    step_count: int

    response: object

    result: object