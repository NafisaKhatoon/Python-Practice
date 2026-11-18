"""Constrained decoding of one function call."""
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
    return text != "" and all(c != '"' and ord(c) >= 32 for c in text)


def _closes_string(text: str) -> bool:
    if '"' not in text:
        return False
    before = text.split('"', 1)[0]
    return before == "" or _plain(before)


def build_prompt(request: str, functions: list[FunctionDef]) -> str:
    lines = []
    for func in functions:
        args = ", ".join(f"{k}: {v.type}" for k, v in func.parameters.items())
        lines.append(f"- {func.name}({args}): {func.description}")
    tools = "\n".join(lines)
    return (
        "<|im_start|>system\n"
        "Turn the user request into one function call as JSON with the "
        "keys name and parameters. Copy values exactly from the request.\n"
        "Example: [abc] matches a, b or c. [^abc] matches any character except a, b or c.\n"
        f"Functions:\n{tools}<|im_end|>\n"
        f"<|im_start|>user\n{request}<|im_end|>\n"
        "<|im_start|>assistant\n<think>\n\n</think>\n\n"
    )



class ConstrainedDecoder:
    def __init__(self, model: Small_LLM_Model) -> None:
        self.model = model
        vocab = Vocab(model.get_path_to_vocab_file())
        self.text_to_id = vocab.text_to_id
        self.ids = np.array(sorted(vocab.texts), dtype=np.int64)
        self.texts = [vocab.texts[i] for i in self.ids.tolist()]
        self.plain = np.array([_plain(t) for t in self.texts])
        self.closing = np.array([_closes_string(t) for t in self.texts])
        chars = set("0123456789.-")
        self.numeric = [
            k for k, t in enumerate(self.texts) if t and set(t) <= chars
        ]

    # ---- helpers -------------------------------------------------
    def _encode(self, text: str) -> list[int]:
        return self.model.encode(text)[0].tolist()

    def _logits(self, ids: list[int]) -> np.ndarray:
        raw = self.model.get_logits_from_input_ids(ids)
        return np.asarray(raw, dtype=np.float32)

    @staticmethod
    def _top(scores: np.ndarray, mask: np.ndarray) -> tuple[int, float]:
        masked = np.where(mask, scores, -np.inf)
        k = int(np.argmax(masked))
        return k, float(masked[k])

    # ---- value generators ---------------------------------------
    def _choose(self, ids: list[int], options: list[str]) -> str:
        """Pick one of `options`, token by token (closing quote = stop)."""
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
                raise DecodeError(f"no option matches {cur!r}")
            if len(pool) == 1:
                tid = next(iter(pool))  # forced, skip the model call
            else:
                logits = self._logits(ids)
                tid = max(pool, key=lambda i: float(logits[i]))
            if pool[tid] == "":
                return cur
            ids.append(tid)
            cur += pool[tid]

    def _number(self, ids: list[int], integer: bool) -> str:
        prefix = INT_PREFIX if integer else FLOAT_PREFIX
        done = INT_DONE if integer else FLOAT_DONE
        cur = ""
        for _ in range(MAX_NUMBER):
            scores = self._logits(ids)[self.ids]
            best, best_score = -1, -np.inf
            for k in self.numeric:
                if prefix.fullmatch(cur + self.texts[k]):
                    if scores[k] > best_score:
                        best, best_score = k, float(scores[k])
            finished = done.fullmatch(cur) is not None
            if finished and (best < 0 or float(scores.max()) > best_score):
                return cur
            if best < 0:
                raise DecodeError("no valid number continuation")
            ids.append(int(self.ids[best]))
            cur += self.texts[best]
        if done.fullmatch(cur):
            return cur
        raise DecodeError("number is too long")

    def _string(self, ids: list[int]) -> str:
        ids.extend(self._encode('"'))
        cur = ""
        for _ in range(MAX_STRING):
            scores = self._logits(ids)[self.ids]
            k_cont, s_cont = self._top(scores, self.plain)
            k_end, s_end = self._top(scores, self.closing)
            if s_end >= s_cont:
                cur += self.texts[k_end].split('"', 1)[0]
                break
            ids.append(int(self.ids[k_cont]))
            cur += self.texts[k_cont]
        ids.extend(self._encode(cur[-1:] + '"') if cur else self._encode('"'))
        try:
            return json.loads('"' + cur + '"')  # turn JSON escapes into real characters
        except json.JSONDecodeError:
            return cur


    def _value(self, ids: list[int], kind: str) -> Any:
        if kind == "number":
            return float(self._number(ids, integer=False))
        if kind == "integer":
            return int(self._number(ids, integer=True))
        if kind == "string":
            return self._string(ids)
        if kind == "boolean":
            return self._choose(ids, ["true", "false"]) == "true"
        raise DecodeError(f"unsupported parameter type: {kind}")

    # ---- public --------------------------------------------------
    def decode_call(
        self, request: str, functions: list[FunctionDef]
    ) -> tuple[str, dict[str, Any]]:
        by_name = {f.name: f for f in functions}
        ids = self._encode(build_prompt(request, functions))
        ids += self._encode('{"name": "')
        name = self._choose(ids, list(by_name))
        ids += self._encode('", "parameters": {')
        params: dict[str, Any] = {}
        for i, (key, spec) in enumerate(by_name[name].parameters.items()):
            ids += self._encode(f'{", " if i else ""}"{key}": ')
            params[key] = self._value(ids, spec.type)
        return name, params
