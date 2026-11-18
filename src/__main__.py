import argparse
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import TypeAdapter

from .decoder import ConstrainedDecoder
from .models import FunctionCall, FunctionDef, PromptItem


def load(path: str, adapter: TypeAdapter[Any]) -> Any:
    """Read a JSON file and check its structure.
      Exit with a message on error."""
    try:
        return adapter.validate_json(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:  # missing file, bad UTF-8/JSON/shape
        sys.exit(f"error: {path}: {err}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json",
    )
    parser.add_argument(
        "--input", default="data/input/function_calling_tests.json"
    )
    parser.add_argument(
        "--output", default="data/output/function_calling_results.json"
    )
    args = parser.parse_args()

    functions = load(args.functions_definition, TypeAdapter(list[FunctionDef]))
    prompts = load(args.input, TypeAdapter(list[PromptItem]))
    if not functions:
        sys.exit("error: no functions defined")

    try:
        from llm_sdk import Small_LLM_Model

        decoder = ConstrainedDecoder(Small_LLM_Model())
    except Exception as err:
        sys.exit(f"error: cannot load the model: {err}")

    results = []
    for item in prompts:
        try:
            name, params = decoder.decode_call(item.prompt, functions)
        except (ValueError, RuntimeError) as err:
            print(f"warning: skipped {item.prompt!r}: {err}", file=sys.stderr)
            continue  # one bad prompt must not stop the others
        results.append(
            FunctionCall(prompt=item.prompt, name=name, parameters=params))

    output = Path(args.output)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps([r.model_dump() for r in results], indent=2),
            encoding="utf-8",
        )
    except OSError as err:
        sys.exit(f"error: cannot write output: {err}")

    print(f"wrote {len(results)} results to {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
