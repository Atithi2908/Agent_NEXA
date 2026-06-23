from langchain.tools import tool

browser = None


def set_browser_tool(tool_instance):
    global browser
    browser = tool_instance


@tool
def navigate(url: str):
    """
    Navigate the browser to a URL.
    """
    return browser.navigate(url)


@tool
def click(element_id: int):
    """
    Click an element using its element id.
    """
    return browser.click(element_id=element_id)


@tool
def type_text(
    element_id: int,
    text: str
):
    """
    Type text into an input field.
    """
    return browser.type(
        element_id=element_id,
        text=text
    )


@tool
def press(key: str):
    """
    Press a keyboard key.
    """
    return browser.press(key)


@tool
def observe():
    """
    Observe the current webpage and return page information.
    """
    return browser.observe()


@tool
def close_browser():
    """
    Close the browser.
    """
    return browser.close()


BROWSER_TOOLS = [
    navigate,
    click,
    type_text,
    press,
    observe,
    close_browser
]