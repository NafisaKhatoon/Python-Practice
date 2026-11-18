"""Entry point: uv run python -m src"""
import argparse
import json
import sys
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from .decoder import ConstrainedDecoder, DecodeError
from .models import FunctionCall, FunctionDef, PromptItem

T = TypeVar("T", bound=BaseModel)


class InputError(Exception):
    """Raised for missing or malformed input files."""


def load_list(path: str, model: type[T]) -> list[T]:
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise InputError(f"{path}: expected a JSON array")
        return [model.model_validate(item) for item in data]
    except FileNotFoundError:
        raise InputError(f"file not found: {path}") from None
    except json.JSONDecodeError as err:
        raise InputError(f"{path}: invalid JSON ({err})") from None
    except ValidationError as err:
        raise InputError(f"{path}: wrong structure ({err})") from None
    except OSError as err:
        raise InputError(f"cannot read {path}: {err}") from None


def parse_args() -> argparse.Namespace:
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        functions = load_list(args.functions_definition, FunctionDef)
        prompts = load_list(args.input, PromptItem)
        if not functions:
            raise InputError("no functions defined")
    except InputError as err:
        print(f"error: {err}", file=sys.stderr)
        return 1

    try:
        from llm_sdk import Small_LLM_Model
        decoder = ConstrainedDecoder(Small_LLM_Model())
    except Exception as err:  # model loading can fail in many ways
        print(f"error: cannot load the model: {err}", file=sys.stderr)
        return 1

    results: list[FunctionCall] = []
    for item in prompts:
        try:
            name, params = decoder.decode_call(item.prompt, functions)
            results.append(
                FunctionCall(prompt=item.prompt, name=name, parameters=params)
            )
        except DecodeError as err:
            print(f"warning: skipped {item.prompt!r}: {err}", file=sys.stderr)

    try:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as file:
            json.dump([r.model_dump() for r in results], file, indent=2)
    except OSError as err:
        print(f"error: cannot write output: {err}", file=sys.stderr)
        return 1
    print(f"wrote {len(results)} results to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
