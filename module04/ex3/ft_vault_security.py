def secure_archive(
        filename: str, action: str, content: str) -> tuple[bool, str]:
    try:
        if action == "read":
            with open(filename, "r") as file:
                data = file.read()
            return True, data
        elif action == "write":
            with open(filename, "w") as file:
                file.write(content)
            return True, 'Content successfully written to file'
        else:
            return False, "Invalid action"
    except Exception as error:
        return False, str(error)


print("=== Cyber Archives Security ===\n")
print("Using 'secure_archive' to read from a nonexistent file:")
print(secure_archive("/not/existing/file", "read", ""))
print()
print("Using 'secure_archive' to read from an inaccessible file:")
print(secure_archive("/etc/master.passwd", "read", ""))
print()
result = secure_archive("ancient_fragment.txt", "read", "")
print("Using 'secure_archive' to read from a regular file:")
print(result)
print()
content = result[1]
print("Using 'secure_archive' to write previous content to a new file:")
print(secure_archive("new file", "write", content))
