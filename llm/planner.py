import json

DEBUG = True


class Planner:

    def __init__(self, llm):
        self.llm = llm

    def build_prompt(self, state):

        observation = {
            "title": state.observation.get("title"),
            "url": state.observation.get("url"),
            "text": state.observation.get("text", "")[:1000],
            "buttons": state.observation.get("buttons", []),
            "links": state.observation.get("links", []),
            "inputs": state.observation.get("inputs", [])
        }

        return f"""
You are an autonomous browser agent.

USER GOAL:
{state.goal}

RECENT ACTIONS:
{state.history[-5:]}

CURRENT OBSERVATION:
{json.dumps(observation, indent=2)}

--------------------------------------------------
GOAL COMPLETION CHECK
--------------------------------------------------

Before generating an action, determine whether the
USER GOAL has been fully satisfied.

A task is completed ONLY when the final outcome
requested by the user has been reached.

Examples:

Goal:
search india vs afghanistan

NOT completed:
- browser opened
- google opened
- search box visible
- query typed

Completed:
- search results are visible
- relevant article page is open

--------------------------------------------------

Goal:
open youtube

Completed:
- youtube homepage is open

--------------------------------------------------

Goal:
play tmkoc

NOT completed:
- youtube homepage open
- search results visible

Completed:
- TMKOC video page is open

--------------------------------------------------

Goal:
open github

Completed:
- github homepage is open

--------------------------------------------------

If the goal is completed return:

{{
  "status":"completed",
  "reason":"Goal achieved"
}}

Otherwise return:

{{
  "status":"continue",
  "tool":"browser",
  "method":"click",
  "params": {{
      "element_id": 1
  }}
}}

--------------------------------------------------
AVAILABLE ACTIONS
--------------------------------------------------

navigate(url)
click(element_id)
type(element_id, text)
press(key)
stop()

--------------------------------------------------
RULES
--------------------------------------------------

- Return ONLY JSON.
- Never explain.
- Never use markdown.
- Never invent selectors.
- Never invent element_ids.
- Only use element_ids visible in CURRENT OBSERVATION.
- Use integer element_ids.
- If unsure, continue working toward the goal.
- Do NOT return completed unless the final goal is clearly achieved.

JSON:
"""

    def extract_json(self, response):

        start = response.find("{")
        end = response.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("No JSON found in response")

        return response[start:end]

    def plan(self, state):

        prompt = self.build_prompt(state)

        if DEBUG:
            print(f"\n[DEBUG] Prompt length: {len(prompt)}")

        response = self.llm.generate(prompt)

        if DEBUG:
            print(f"\n[DEBUG] RAW LLM RESPONSE:\n{response}")

        try:

            response = self.extract_json(response)

            if DEBUG:
                print(f"\n[DEBUG] EXTRACTED JSON:\n{response}")

            action = json.loads(response)

        except (ValueError, json.JSONDecodeError) as e:

            print("[ERROR] JSON parse failed")

            if DEBUG:
                print(f"[DEBUG] {str(e)}")
                print(response)

            return {
                "tool": "system",
                "method": "stop",
                "params": {}
            }

        return action