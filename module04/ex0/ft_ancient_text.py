import sys


def main() -> None:
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print("=== Cyber Archives Recovery ===")
        print(f"Accessing file '{filename}'")
        try:
            file_object = open(filename)
            content = file_object.read()
            print("---")
            print(content)
            print("---")
            file_object.close()
            print(f"File '{filename}' closed.")
        except OSError as error:
            print(f"Error opening file '{filename}': {error}")
    else:
        print("Usage: ft_ancient_text.py <file>")


if __name__ == "__main__":
    main()
