"""Constrained decoding of one function call."""
from pydantic import BaseModel, ConfigDict
from numpy.typing import NDArray
import json
import re
from typing import Any

import numpy as np
from llm_sdk import Small_LLM_Model

from .models import FunctionDef
from .vocab import Vocab


FLOAT_PREFIX = re.compile(r"-?(\d+(\.\d*)?)?")
FLOAT_DONE = re.compile(r"-?\d+(\.\d+)?")
INT_PREFIX = re.compile(r"-?\d*")
INT_DONE = re.compile(r"-?\d+")

MAX_STRING = 100
MAX_NUMBER = 20


class DecodeError(Exception):
    """Raised when no valid continuation exists."""


def _plain(text: str) -> bool:
    """Check whether a token contains normal string content."""
    return text != "" and all(
        c != '"' and ord(c) >= 32 for c in text
    )


def _closes_string(text: str) -> bool:
    """Check whether a token can close a string."""
    if '"' not in text:
        return False

    before = text.split('"', 1)[0]
    return before == "" or _plain(before)


def build_prompt(request: str, functions: list[FunctionDef]) -> str:
    """Build a prompt containing available functions and user request."""

    lines = []

    for func in functions:
        args = ", ".join(
            f"{k}: {v.type}"
            for k, v in func.parameters.items()
        )
        lines.append(
            f"- {func.name}({args}): {func.description}"
        )

    tools = "\n".join(lines)

    return (
        "<|im_start|>system\n"
        "Turn the user request into one function call as JSON with the "
        "keys name and parameters.\n"
        "Extract or derive arguments accurately from the request.\n"
        "Preserve negative signs, decimal points and numeric values.\n"
        "Preserve the order of arguments when appropriate.\n"
        "Preserve literal string values exactly.\n"
        "Ensure arguments match their declared types.\n"
        "Only select a function if it matches the user request.\n"
        "If no available function matches, select no_match.\n"
        "Do not add whitespace to extracted argument values.\n"
        f"Functions:\n{tools}<|im_end|>\n"
        f"<|im_start|>user\n{request}<|im_end|>\n"
        "<|im_start|>assistant\n<think>\n\n</think>\n\n"
    )


class ConstrainedDecoder(BaseModel):
    """Generate structured function calls."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    model: Small_LLM_Model
    text_to_id: dict[str, int]
    ids: NDArray[np.int64]
    texts: list[str]
    plain: NDArray[np.bool_]
    closing: NDArray[np.bool_]
    numeric: list[int]

    def __init__(self, model: Small_LLM_Model) -> None:
        """Initialize the model and vocabulary."""

        vocab = Vocab(model.get_path_to_vocab_file())

        text_to_id = vocab.text_to_id

        ids = np.array(
            sorted(vocab.texts),
            dtype=np.int64
        )

        texts = [
            vocab.texts[i] for i in ids.tolist()
        ]

        plain = np.array(
            [_plain(t) for t in texts],
            dtype=bool
        )

        closing = np.array(
            [_closes_string(t) for t in texts],
            dtype=bool
        )

        chars = set("0123456789.- ")

        numeric = [
            k for k, t in enumerate(texts)
            if t and set(t) <= chars
        ]

        super().__init__(
            model=model,
            text_to_id=text_to_id,
            ids=ids,
            texts=texts,
            plain=plain,
            closing=closing,
            numeric=numeric
        )
    # ---- helpers -------------------------------------------------

    def _encode(self, text: str) -> list[int]:
        """Convert text into token IDs."""
        tokens = self.model.encode(text)[0].tolist()
        return [int(token) for token in tokens]

    def _logits(self, ids: list[int]) -> np.ndarray:
        """Retrieve next-token logits from the language model."""

        raw = self.model.get_logits_from_input_ids(ids)

        return np.asarray(raw, dtype=np.float32)

    @staticmethod
    def _top(
        scores: np.ndarray,
        mask: np.ndarray
    ) -> tuple[int, float]:
        """Select the highest-scoring valid token."""

        masked = np.where(
            mask & np.isfinite(scores),
            scores,
            -np.inf
        )

        if not np.isfinite(masked).any():
            raise DecodeError("No valid token available")

        k = int(np.argmax(masked))

        return k, float(masked[k])

    # ---- value generators ----------------------------------------

    def _choose(
        self,
        ids: list[int],
        options: list[str]
    ) -> str:
        """Select one of the available options token by token."""

        quote_id = self.text_to_id['"']
        cur = ""

        while True:

            pool: dict[int, str] = {}

            for opt in options:

                if opt.startswith(cur) and opt != cur:

                    rest = opt[len(cur):]

                    for n in range(1, len(rest) + 1):

                        tid = self.text_to_id.get(rest[:n])

                        if tid is not None:
                            pool[tid] = rest[:n]

            if cur in options:

                if not pool:
                    return cur

                pool[quote_id] = ""

            if not pool:
                raise DecodeError(
                    f"No option matches {cur!r}"
                )

            if len(pool) == 1:
                tid = next(iter(pool))

            else:
                logits = self._logits(ids)

                tid = max(
                    pool,
                    key=lambda i: float(logits[i])
                )

            if pool[tid] == "":
                return cur

            ids.append(tid)
            cur += pool[tid]

    def _number(
        self,
        ids: list[int],
        integer: bool
    ) -> str:
        """Generate an integer or floating-point number."""

        prefix = INT_PREFIX if integer else FLOAT_PREFIX
        done = INT_DONE if integer else FLOAT_DONE

        cur = ""

        for _ in range(MAX_NUMBER):

            scores = self._logits(ids)[self.ids]

            best, best_score = -1, -np.inf

            for k in self.numeric:

                candidate = cur + self.texts[k].lstrip() if not cur else (
                    cur + self.texts[k]
                )

                if candidate and prefix.fullmatch(candidate):

                    if scores[k] > best_score:
                        best = k
                        best_score = float(scores[k])

            finished = done.fullmatch(cur) is not None

            if finished and (
                best < 0 or float(scores.max()) > best_score
            ):
                return cur

            if best < 0:
                raise DecodeError(
                    "No valid number continuation"
                )

            ids.append(int(self.ids[best]))
            if not cur:
                cur += self.texts[best].lstrip()
            else:
                cur += self.texts[best]

        if done.fullmatch(cur):
            return cur

        raise DecodeError("Number is too long")

    def _string(self, ids: list[int]) -> str:
        """Generate a string using precomputed token masks."""
        ids.extend(self._encode('"'))
        cur = ""

        for _ in range(MAX_STRING):
            scores = self._logits(ids)[self.ids]

            k_cont, s_cont = self._top(scores, self.plain)
            k_end, s_end = self._top(scores, self.closing)

            if s_end >= s_cont:
                ending = self.texts[k_end].split('"', 1)[0]
                cur += ending
                ids.extend(self._encode(ending + '"'))
                break

            ids.append(int(self.ids[k_cont]))
            cur += self.texts[k_cont]

        else:
            raise DecodeError("String exceeds maximum token limit")

        try:
            value = json.loads('"' + cur + '"')
            if isinstance(value, str):
                return value
        except json.JSONDecodeError:
            pass

        return cur

    def _value(
        self,
        ids: list[int],
        kind: str
    ) -> Any:
        """Generate a value matching the declared parameter type."""

        if kind == "number":
            return float(self._number(ids, integer=False))

        if kind == "integer":
            return int(self._number(ids, integer=True))

        if kind == "string":
            return self._string(ids)

        if kind == "boolean":
            return self._choose(
                ids, ["true", "false"]
            ) == "true"

        raise DecodeError(
            f"Unsupported parameter type: {kind}"
        )

    # ---- public --------------------------------------------------

    def decode_call(
        self,
        request: str,
        functions: list[FunctionDef]
    ) -> tuple[str, dict[str, Any]]:
        """Generate a function name and its required parameters."""

        by_name = {
            f.name: f for f in functions
        }

        ids = self._encode(
            build_prompt(request, functions)
        )

        ids += self._encode('{"name": "')

        name = self._choose(ids, list(by_name) + ["no_match"])

        if name == "no_match":
            raise DecodeError("No matching function found")

        ids += self._encode('", "parameters": {')

        params: dict[str, Any] = {}

        for i, (key, spec) in enumerate(
            by_name[name].parameters.items()
        ):
            separator = ", " if i else ""
            space = "" if spec.type in ("number", "integer") else " "

            ids += self._encode(
                f'{separator}"{key}":{space}'
            )

            params[key] = self._value(ids, spec.type)

        return name, params
