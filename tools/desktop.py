import time
import psutil
import pyautogui
import pygetwindow as gw
from pywinauto import Desktop


class DesktopTool:

    def __init__(self):
        pass

    def get_active_window(self):

        try:

            window = gw.getActiveWindow()

            if not window:

                return {
                    "success": False,
                    "title": None
                }

            return {
                "success": True,
                "title": window.title
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }

    def list_open_apps(self):

        windows = []

        IGNORE = {
            "",
            "Program Manager",
            "Windows Input Experience"
        }

        for window in gw.getAllWindows():

            title = window.title.strip()

            if not title:
                continue

            if title in IGNORE:
                continue

            windows.append(title)

        return {
            "success": True,
            "windows": windows
        }

    def switch_window(self, target):

        target = target.lower()

        for window in gw.getAllWindows():

            if not window.title:
                continue

            if target in window.title.lower():

                try:

                    window.activate()

                    return {
                        "success": True,
                        "window": window.title
                    }

                except Exception as e:

                    return {
                        "success": False,
                        "error": str(e)
                    }

        return {
            "success": False,
            "error": "Window not found"
        }

    def open_app(self, app_name):

        try:

            pyautogui.press("win")

            time.sleep(1)

            pyautogui.write(
                app_name,
                interval=0.03
            )

            time.sleep(1)

            pyautogui.press("enter")

            return {
                "success": True,
                "app": app_name
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }

    def close_app(self, app_name):

        target = f"{app_name.lower()}.exe"

        killed = 0

        for proc in psutil.process_iter(
            ["pid", "name"]
        ):

            try:

                process_name = proc.info["name"]

                if not process_name:
                    continue

                if process_name.lower() == target:

                    proc.kill()
                    killed += 1

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                continue

        return {
            "success": True,
            "killed": killed
        }

    def type_text(self, text):

        try:

            pyautogui.write(
                text,
                interval=0.03
            )

            return {
                "success": True,
                "text": text
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }

    def press_key(self, key):

        try:

            pyautogui.press(key)

            return {
                "success": True,
                "key": key
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }

    def hotkey(self, *keys):

        try:

            pyautogui.hotkey(*keys)

            return {
                "success": True,
                "keys": list(keys)
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }

    def observe(self):

        active = self.get_active_window()

        windows = self.list_open_apps()

        return {

            "active_window":
                active.get("title"),

            "open_windows":
                windows.get("windows", [])
        }
        
    def inspect_window(self, window_name):

        window = Desktop(
            backend="uia"
        ).window(
            title_re=f".*{window_name}.*"
        )

        buttons = []
        menus = []
        texts = []

        for child in window.descendants():

            try:

                name = child.window_text().strip()

                if not name:
                    continue

                control_type = (
                    child.element_info.control_type
                )

                if control_type == "Button":

                    buttons.append(name)

                elif control_type == "MenuItem":

                    menus.append(name)

                elif control_type in [
                    "Text",
                    "Document"
                ]:

                    texts.append(name)

            except:
                pass

        return {
            "buttons": buttons,
            "menus": menus,
            "texts": texts
        }
        
    def inspect_active_window(self):

        active = self.get_active_window()

        if not active["success"]:
            return active

        return self.inspect_window(
            active["title"]
        )