from tools.filesystem import FileSystemTool

from langchain_tools.filesystem_tools import (
    set_filesystem_tool,
    read_file
)

fs = FileSystemTool()

set_filesystem_tool(fs)

result = read_file.invoke(
    {
        "path":"user_info.txt"
    }
)

print(result)