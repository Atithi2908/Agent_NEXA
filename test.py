from tools.desktop import DesktopTool
import json

desktop = DesktopTool()



print("\n=== ACTIVE WINDOW OBSERVATION ===")

result = desktop.inspect_window(window_name="Notepad")

print(
    json.dumps(
        result,
        indent=2
    )
)