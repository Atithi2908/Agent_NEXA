from langchain_tools.browser_tools import BROWSER_TOOLS
from langchain_tools.desktop_tools import DESKTOP_TOOLS
from langchain_tools.filesystem_tools import FILESYSTEM_TOOLS
from langchain_tools.search_tools import SEARCH_TOOLS
from langchain_tools.knowledge_tools import KNOWLEDGE_TOOLS

ALL_TOOLS = (
    BROWSER_TOOLS
    + DESKTOP_TOOLS
    + FILESYSTEM_TOOLS
    + SEARCH_TOOLS
    + KNOWLEDGE_TOOLS
)