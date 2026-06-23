from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_tools.all_tools import ALL_TOOLS

load_dotenv()


def main():

    print("=" * 50)
    print("AVAILABLE TOOLS")
    print("=" * 50)

    for tool in ALL_TOOLS:
        print(tool.name)

    print("\n")

    llm = ChatGroq(
        model="qwen/qwen3-32b",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    llm_with_tools = llm.bind_tools(
        ALL_TOOLS
    )

    query = """
    Search the web for who created Python.
    """

    print("=" * 50)
    print("QUERY")
    print("=" * 50)
    print(query)

    response = llm_with_tools.invoke(query)

    print("\n")
    print("=" * 50)
    print("RAW RESPONSE")
    print("=" * 50)
    print(response)

    print("\n")
    print("=" * 50)
    print("CONTENT")
    print("=" * 50)
    print(response.content)

    print("\n")
    print("=" * 50)
    print("TOOL CALLS")
    print("=" * 50)
    print(response.tool_calls)

    if response.tool_calls:

        tool_call = response.tool_calls[0]

        print("\n")
        print("=" * 50)
        print("SELECTED TOOL")
        print("=" * 50)

        print(tool_call["name"])

        print("\n")
        print("=" * 50)
        print("ARGS")
        print("=" * 50)

        print(tool_call["args"])

    else:

        print("\nNo tool call generated.")


if __name__ == "__main__":
    main()