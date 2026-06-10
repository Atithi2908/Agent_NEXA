from tools.filesystem import FileSystemTool
import json

fs = FileSystemTool()

print("\n" + "=" * 50)
print("TEST 3 : LIST DIRECTORY")
print("=" * 50)

result = fs.list_directory(".")
print(json.dumps(result, indent=2))

print("\n" + "=" * 50)
print("TEST 4 : CREATE FOLDER")
print("=" * 50)

result = fs.create_folder("test_folder")
print(json.dumps(result, indent=2))

print("\n" + "=" * 50)
print("TEST 5 : CREATE FILE")
print("=" * 50)

result = fs.create_file("test_folder/test.txt")
print(json.dumps(result, indent=2))

print("\n" + "=" * 50)
print("TEST 6 : WRITE FILE")
print("=" * 50)

result = fs.write_file(
    "test_folder/test.txt",
    "Hello from NEXA"
)
print(json.dumps(result, indent=2))

print("\n" + "=" * 50)
print("TEST 7 : READ FILE")
print("=" * 50)

result = fs.read_file(
    "test_folder/test.txt"
)
print(json.dumps(result, indent=2))

print("\n" + "=" * 50)
print("TEST 8 : OPEN FILE")
print("=" * 50)

answer = input(
    "Open test file? (y/n): "
)

if answer.lower() == "y":

    result = fs.open_file(
        "test_folder/test.txt"
    )

    print(json.dumps(result, indent=2))

print("\n" + "=" * 50)
print("FILESYSTEM TOOL TEST COMPLETE")
print("=" * 50)