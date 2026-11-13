from pathlib import Path
import argparse
import json


def save_json(path: str, data: list) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_json(path: str) -> list:
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Translate prompts into structured function calls."
    )

    parser.add_argument(
        "--input",
        default="data/input/function_calling_tests.json",
        help="Path to the prompts JSON file.",
    )

    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json",
        help="Path to the function definitions JSON file.",
    )

    parser.add_argument(
        "--output",
        default="data/output/function_calling_results.json",
        help="Path for the output JSON file.",
    )

    args = parser.parse_args()

    try:
        prompts = load_json(args.input)
        functions = load_json(args.functions_definition)

        if not isinstance(prompts, list):
            raise ValueError("The prompts file must contain a JSON array.")

        if not isinstance(functions, list):
            raise ValueError("The functions file must contain a JSON array.")

        for item in prompts:
            if not isinstance(item, dict):
                raise ValueError("Each prompt item must be a JSON object.")

            if "prompt" not in item:
                raise ValueError("Each prompt item must have a 'prompt' field.")

            if not isinstance(item["prompt"], str):
                raise ValueError("The 'prompt' field must contain a string.")

        for function in functions:
            if not isinstance(function, dict):
                raise ValueError("Each function must be a JSON object.")

            if "name" not in function:
                raise ValueError("Each function must have a 'name' field.")

            if not isinstance(function["name"], str):
                raise ValueError("The function 'name' must be a string.")

            if "description" not in function:
                raise ValueError("Each function must have a 'description' field.")

            if not isinstance(function["description"], str):
                raise ValueError("The function 'description' must be a string.")

            if "parameters" not in function:
                raise ValueError("Each function must have a 'parameters' field.")

            if not isinstance(function["parameters"], dict):
                raise ValueError("The function 'parameters' must be a JSON object.")

            for name, details in function["parameters"].items():
                if not isinstance(details, dict):
                    raise ValueError(
                        f"Parameter '{name}' must be a JSON object."
                    )

                if "type" not in details:
                    raise ValueError(
                        f"Parameter '{name}' must have a 'type' field."
                    )

                if not isinstance(details["type"], str):
                    raise ValueError(
                        f"The type of parameter '{name}' must be a string."
                    )

            if "returns" not in function:
                raise ValueError("Each function must have a 'returns' field.")

            if not isinstance(function["returns"], dict):
                raise ValueError("The function 'returns' must be a JSON object.")

            if "type" not in function["returns"]:
                raise ValueError("The 'returns' field must have a 'type' field.")

            if not isinstance(function["returns"]["type"], str):
                raise ValueError("The return type must be a string.")

        print("Prompts:")
        for item in prompts:
            print(item["prompt"])

        print("\nAvailable functions:")
        for function in functions:
            print("Name:", function["name"])
            print("Description:", function["description"])
            print("Parameters:")

            for name, details in function["parameters"].items():
                print(f"  {name}: {details['type']}")

        results = []
        save_json(args.output, results)
        print(f"\nResults saved to: {args.output}")

    except OSError as error:
        print(f"Error reading input files: {error}")
    except json.JSONDecodeError as error:
        print(f"Error: invalid JSON: {error}")
    except ValueError as error:
        print(f"Invalid input: {error}")


if __name__ == "__main__":
    main()
