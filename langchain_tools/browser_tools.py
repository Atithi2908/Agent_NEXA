from langchain.tools import tool

browser = None


def set_browser_tool(tool_instance):
    global browser
    browser = tool_instance


@tool
def browser_navigate(url: str):
    """
    Navigate the browser to a URL.
    """
    return browser.navigate(url)


@tool
def browser_click(element_id: int):
    """
    Click an element using its element id.
    """
    return browser.click(element_id=element_id)


@tool
def browser_type_text(
    element_id: int,
    text: str
):
    """
    Type text into an input field on browser.
    """
    return browser.type(
        element_id=element_id,
        text=text
    )


@tool
def browser_press(key: str):
    """
    Press a keyboard key.
    """
    return browser.press(key)


@tool
def browser_observe():
    """
    Observe the current webpage and return page information.
    """
    return browser.observe()


@tool
def browser_close_browser():
    """
    Close the browser.
    """
    return browser.close()


BROWSER_TOOLS = [
    browser_navigate,
    browser_click,
    browser_type_text,
    browser_press,
    browser_observe,
    browser_close_browser
]