from tools.desktop import DesktopTool

from langchain_tools.desktop_tools import (
    set_desktop_tool,
    open_app,
    observe_desktop,
    type_text,
    press_key,
    inspect_active_window
)

desktop = DesktopTool()

set_desktop_tool(desktop)

print("\n=== OPEN APP ===")
result = open_app.invoke(
    {
        "app_name": "notepad"
    }
)

print(result)

input("\nPress Enter after Notepad opens...")

print("\n=== OBSERVE ===")
result = observe_desktop.invoke({})

print(result)

print("\n=== TYPE TEXT ===")
result = type_text.invoke(
    {
        "text": "Hello from LangChain Tool!"
    }
)

print(result)

print("\n=== INSPECT ACTIVE WINDOW ===")
result = inspect_active_window.invoke({})

print(result)

print("\n=== PRESS KEY ===")
result = press_key.invoke(
    {
        "key": "enter"
    }
)

print(result)