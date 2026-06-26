import json
from langchain_core.prompts import ChatPromptTemplate
DEBUG = True
from langchain_tools.all_tools import ALL_TOOLS
planner_prompt = ChatPromptTemplate.from_template(
    """
    You are an autonomous AI agent capable of using Browser, Desktop, and Filesystem tools.

    ## USER GOAL

    {goal}

    ---

    ## RECENT ACTIONS

    {history}

    ---

    ## CURRENT OBSERVATION

    {observation}

    ---

   
    
Your objective is to achieve the USER GOAL by repeatedly:

1. Analyzing the current observation.
2. Selecting exactly one action.
3. Using the result of that action to determine the next step.
4. Continuing until the goal is fully achieved.

You may require multiple actions to complete a task.

---

## GOAL COMPLETION RULE

A task is completed ONLY when the final outcome requested by the user has been achieved.

Finding information is NOT completion.

Opening an application is NOT always completion.

Typing text is NOT always completion.

Discovering a path is NOT completion.

Only return completed when the user's requested outcome exists.


---

---

## DISCOVERY RULE

If information required to complete a task is unknown:

DO NOT GUESS.

Use available tools to discover it.

---
When the goal is fully achieved and no further actions are required,
respond with a single short completion message only.
Do not ask follow-up questions or suggest additional actions.
Do not add extra explanation.

Do not call a tool if the task is already complete.

If CURRENT OBSERVATION contains:


DO NOT return completed.

Use the error message to determine the next action.

Attempt to discover missing information and continue.

When a search action returns results:

- Read the content in the search results.
- If the answer to the user's question can be determined from the results, 

- Use only information present in the search results.
- Do not invent information.
- If the results are insufficient or unclear, perform another search with a better query.

---
---
---

USER MEMORY

A file named user_info.txt exists in the project directory.
- If the user asks any personal question about themselves, always retrieve the answer from the knowledge base only.
- Never read user_info.txt directly for answering personal questions.
- When the user asks NEXA to remember something, save it to user_info.txt.
- After updating user_info.txt, add it to the knowledge base so it becomes part of the RAG pipeline.
- When answering memory-related questions, retrieve information through the knowledge base.
- Do not answer memory questions from assumptions.

Use at most one tool at a time.

When additional information is required,
use an appropriate tool.

When the goal is complete,
respond only with the final answer in one brief line.
When the user's goal has been fully completed, do not call any more tools.
Respond with a single short completion message confirming success. 
Do not ask follow-up questions, offer additional help, or suggest further actions.
    """
)
    

class Planner:

    def __init__(self, llm):
        self.llm = llm
        self.llm_with_tools = llm.bind_tools(
            ALL_TOOLS
        )
    
    def build_prompt(self, state):

        return planner_prompt.invoke(
        {
            "goal": state["goal"],
            "history": json.dumps(
                state["history"][-2:],
                indent=2
            ),
            "observation": json.dumps(
                state["observation"],
                indent=2
            )
        }
    )

    def plan(self, state):

        prompt = self.build_prompt(state)
        prompt_text = prompt.to_string()

        if DEBUG:
            print(f"\n[DEBUG] Prompt length: {len(prompt_text)}")

        response = self.llm_with_tools.invoke(
            prompt_text
            )

        if DEBUG:
            print(f"\n[DEBUG] RAW LLM RESPONSE:\n{response}")
        return response