import re
from typing import Any

import numpy as np

from .models import FunctionDef
from .prompt import build_prompt
from .vocab import closes_string, is_plain, load_token_texts

# For each number type: "could still become a number" and "is a full number"
CAN_CONTINUE = {
    "number": re.compile(r"-?(\d+(\.\d*)?)?"),
    "integer": re.compile(r"-?\d*"),
}
IS_COMPLETE = {
    "number": re.compile(r"-?\d+(\.\d+)?"),
    "integer": re.compile(r"-?\d+"),
}

MAX_TOKENS = 100  # safety limit so a value can never loop forever


class ConstrainedDecoder:
    def __init__(self, model: Any) -> None:
        self.model = model
        self.texts = load_token_texts(model.get_path_to_vocab_file())
        self.token_id = {t: i for i, t in enumerate(self.texts) if t}

        # Masks: True where a token is allowed in that situation
        self.plain = np.array([is_plain(t) for t in self.texts])
        self.closing = np.array([closes_string(t) for t in self.texts])
        digits = set("0123456789.-")
        self.numeric_ids = [
            i for i, t in enumerate(self.texts) if t and set(t) <= digits
        ]

    def _encode(self, text: str) -> list[int]:
        return self.model.encode(text)[0].tolist()

    def _scores(self, ids: list[int]) -> np.ndarray:
        """One score per token. Higher means the model likes it more."""
        logits = np.asarray(self.model.get_logits_from_input_ids(ids))
        return logits[: len(self.texts)]

    @staticmethod
    def _best(scores: np.ndarray, allowed: np.ndarray) -> int:
        """Id of the highest-scoring token among the allowed ones."""
        return int(np.argmax(np.where(allowed, scores, -np.inf)))

    def _choose(self, ids: list[int], options: list[str]) -> str:
        """Pick one of the options (function name, true/false)."""
        chosen = ""
        while True:
            # Tokens that continue at least one option: token id -> its text
            candidates: dict[int, str] = {}
            for option in options:
                if option.startswith(chosen):
                    rest = option[len(chosen):]
                    for n in range(1, len(rest) + 1):
                        if rest[:n] in self.token_id:
                            candidates[self.token_id[rest[:n]]] = rest[:n]

            if chosen in options:
                if not candidates:
                    return chosen  # nothing longer is possible
                candidates[self.token_id['"']] = ""  # "" means: stop here

            if not candidates:
                raise ValueError(f"no option matches {chosen!r}")

            if len(candidates) == 1:
                token = next(iter(candidates))  # no need to ask the model
            else:
                scores = self._scores(ids)
                token = max(candidates, key=lambda t: scores[t])

            if candidates[token] == "":
                return chosen
            ids.append(token)
            chosen += candidates[token]

    def _number(self, ids: list[int], kind: str) -> str:
        can_continue, is_complete = CAN_CONTINUE[kind], IS_COMPLETE[kind]
        text = ""
        for _ in range(MAX_TOKENS):
            scores = self._scores(ids)

            # Best number token that keeps the text a valid number start
            valid = [
                t for t in self.numeric_ids
                if can_continue.fullmatch(text + self.texts[t])
            ]
            best = max(valid, key=lambda t: scores[t], default=None)

            # Stop when the number is complete and the model wants
            # something else next (for example a comma)
            if is_complete.fullmatch(text):
                if best is None or scores.max() > scores[best]:
                    return text
            if best is None:
                raise ValueError("no valid number continuation")

            ids.append(best)
            text += self.texts[best]

        if not is_complete.fullmatch(text):
            raise ValueError("number is too long")
        return text

    def _string(self, ids: list[int]) -> str:
        ids.extend(self._encode('"'))  # opening quote
        text = ""
        for _ in range(MAX_TOKENS):
            scores = self._scores(ids)
            plain = self._best(scores, self.plain)
            closing = self._best(scores, self.closing)

            if scores[closing] >= scores[plain]:
                ids.append(closing)
                return text + self.texts[closing][:-1]  # drop the quote

            ids.append(plain)
            text += self.texts[plain]

        ids.extend(self._encode('"'))  # too long: close it ourselves
        return text

    def _value(self, ids: list[int], kind: str) -> Any:
        if kind == "number":
            return float(self._number(ids, kind))
        if kind == "integer":
            return int(self._number(ids, kind))
        if kind == "string":
            return self._string(ids)
        if kind == "boolean":
            return self._choose(ids, ["true", "false"]) == "true"
        raise ValueError(f"unsupported parameter type: {kind}")

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
            separator = ", " if i else ""
            ids += self._encode(f'{separator}"{key}": ')
            params[key] = self._value(ids, spec.type)
        return name, params
