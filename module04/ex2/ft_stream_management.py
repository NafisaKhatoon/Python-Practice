import sys


def main() -> None:
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print("=== Cyber Archives Recovery & Preservation ===")
        print(f"Accessing file '{filename}'")
        try:
            file_object = open(filename)
            content = file_object.read()
            split_content = content.split("\n")
            new_list = [item + "#" for item in split_content]
            transformed_content = "\n".join(new_list)

            if content.endswith("\n"):
                transformed_content += "\n"
            print("---")
            print(content)
            print("---")
            file_object.close()
            print(f"File '{filename}' closed")
            print("Transform data:")
            print("---")
            print(transformed_content)
            print("---")
            sys.stdout.write("Enter new file name (or empty): ")
            sys.stdout.flush()
            txt_file = sys.stdin.readline().strip()
            if txt_file == "":
                print("Not saving data.")
            else:
                print(f"Saving data to '{txt_file}'")
                try:
                    output_file = open(txt_file, "w")
                    output_file.write(transformed_content)
                    output_file.close()
                    print(f"Data saved in file '{txt_file}'.")
                except OSError as error:
                    sys.stderr.write(
                        f"[STDERR] Error opening file '{txt_file}'"
                        f": {error}\n")
                    print("Data not saved.")
        except OSError as error:
            sys.stderr.write(
                f"[STDERR] Error opening file '{filename}': {error}\n")
    else:
        print("Usage: ft_stream_management.py <file>")


if __name__ == "__main__":
    main()
