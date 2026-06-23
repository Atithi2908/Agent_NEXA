from langchain.tools import tool

filesystem = None


def set_filesystem_tool(tool_instance):
    global filesystem
    filesystem = tool_instance


@tool
def find_file(filename: str):
    """
    Find a file by name on the system.
    """
    return filesystem.find_file(filename)


@tool
def find_folder(folder_name: str):
    """
    Find a folder by name on the system.
    """
    return filesystem.find_folder(folder_name)


@tool
def list_directory(path: str):
    """
    List files and folders inside a directory.
    """
    return filesystem.list_directory(path)


@tool
def open_file(path: str):
    """
    Open a file using the default application.
    """
    return filesystem.open_file(path)


@tool
def create_file(path: str):
    """
    Create a new file.
    """
    return filesystem.create_file(path)


@tool
def create_folder(path: str):
    """
    Create a new folder.
    """
    return filesystem.create_folder(path)


@tool
def read_file(path: str):
    """
    Read the contents of a file.
    """
    return filesystem.read_file(path)


@tool
def write_file(
    path: str,
    content: str
):
    """
    Overwrite a file with content.
    """
    return filesystem.write_file(
        path,
        content
    )


@tool
def append_file(
    path: str,
    content: str
):
    """
    Append content to an existing file.
    """
    return filesystem.append_file(
        path,
        content
    )


FILESYSTEM_TOOLS = [
    find_file,
    find_folder,
    list_directory,
    open_file,
    create_file,
    create_folder,
    read_file,
    write_file,
    append_file
]