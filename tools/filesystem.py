from pathlib import Path
import os

class FileSystemTool:
    def __init__(self):
        pass
    
    def find_file(self, filename):
        try:
            matches = []
            
            for path in Path.home().rglob(filename):
                matches.append(str(path))
                if len(matches) >= 20:
                    break
            return {
                "success": True,
                "matches": matches[:20]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def find_folder(self, folder_name):
        try:
            matches = []
            
            for path in Path.home().rglob("*"):
                if path.is_dir():
                    if folder_name.lower() in path.name.lower():
                        matches.append(str(path))
                        if len(matches) >= 20:
                            break
            
            return {
                "success": True,
                "matches": matches[:20]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_directory(self, path):
        try:
            path = Path(path)
            items = []
            
            for item in path.iterdir():
                items.append({
                    "name": item.name,
                    "type": "folder" if item.is_dir() else "file"
                })
            
            return {
                "success": True,
                "items": items[:20]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def open_file(self, path):

        try:

            path = str(Path(path).resolve())

            os.startfile(path)

            return {
            "success": True,
            "path": path
            }

        except Exception as e:

            return {
            "success": False,
            "error": str(e)
            }
            
    def create_file(self, path):

        try:

            Path(path).touch()

            return {
            "success": True,
            "path": path
            }

        except Exception as e:

            return {
            "success": False,
            "error": str(e)
        }
            
            
    def create_folder(self, path):

        try:

            Path(path).mkdir(
            parents=True,
            exist_ok=True
        )

            return {
            "success": True,
            "path": path
        }

        except Exception as e:

            return {
            "success": False,
            "error": str(e)
            }
            
    def read_file(self, path):

        try:

         path = Path(path)

         content = path.read_text(
            encoding="utf-8"
        )[:2000]

         return {
                "success": True,
            "path": str(path),
            "content": content
         }

        except Exception as e:

            return {
            "success": False,
            "error": str(e)
        }
            
    def write_file(self, path, content):

        try:

            path = Path(path)

            path.write_text(
            content,
            encoding="utf-8"
        )

            return {
            "success": True,
            "path": str(path)
        }

        except Exception as e:

            return {
            "success": False,
            "error": str(e)
            }
            
    def append_file(
    self,
    path,
    content
):

        try:

            with open(
            path,
            "a",
            encoding="utf-8"
            ) as file:

                file.write("\n" + content)

            return {
            "success": True,
            "path": path,
            "message": "Content appended successfully"
            }

        except Exception as e:

            return {
            "success": False,
            "error": str(e)
            }