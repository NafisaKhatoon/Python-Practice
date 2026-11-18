from .models import FunctionDef


def build_prompt(request: str, functions: list[FunctionDef]) -> str:
    """Build the text the model reads before it writes the function call."""
    lines = []
    for func in functions:
        params = ", ".join(
            f"{name}: {spec.type}" for name, spec in func.parameters.items()
        )
        lines.append(f"- {func.name}({params}): {func.description}")
    tools = "\n".join(lines)

    return (
        "<|im_start|>system\n"
        "Turn the user request into one function call as JSON with the "
        "keys name and parameters. Copy values exactly from the request.\n"
        f"Functions:\n{tools}<|im_end|>\n"
        f"<|im_start|>user\n{request}<|im_end|>\n"
        "<|im_start|>assistant\n<think>\n\n</think>\n\n"
    )
