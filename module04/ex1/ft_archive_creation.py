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
            print(f"File '{filename}' closed")

        except OSError as error:
            print(f"Error opening file '{filename}': {error}")

        else:
            split_content = content.split("\n")
            new_list = [item + "#" for item in split_content]
            transformed_content = "\n".join(new_list)

            if content.endswith("\n"):
                transformed_content += "\n"
            print("Transform data:")
            print("---")
            print(transformed_content)
            print("---")

            txt_file = input("Enter new file name (or empty): ")
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
                    print(f"Error opening file '{txt_file}': {error}")
                    print("Data not saved.")
    else:
        print("Usage: ft_archive_creation.py <file>")


if __name__ == "__main__":
    main()
