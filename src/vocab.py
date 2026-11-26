"""Token id to text mapping built from the vocabulary file."""
import json
from pydantic import BaseModel, TypeAdapter


def _byte_decoder() -> dict[str, int]:
    """Inverse of the GPT-2 byte-to-unicode table used by Qwen."""
    keep = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    chars = keep[:]
    extra = 0
    for byte in range(256):
        if byte not in keep:
            keep.append(byte)
            chars.append(256 + extra)
            extra += 1
    return {chr(c): b for b, c in zip(keep, chars)}


class Vocab(BaseModel):
    """Maps token IDs to the real text they represent."""

    texts: dict[int, str]
    text_to_id: dict[str, int]

    def __init__(self, path: str) -> None:
        """Load and validate the vocabulary file."""

        with open(path, encoding="utf-8") as file:
            raw = TypeAdapter(
                dict[str, int]
            ).validate_python(
                json.load(file), strict=True
            )

        decoder = _byte_decoder()

        texts: dict[int, str] = {}

        for token, idx in raw.items():
            try:
                data = bytes(decoder[c] for c in token)
                texts[idx] = data.decode("utf-8")

            except (KeyError, UnicodeDecodeError):
                continue

        text_to_id = {
            t: i for i, t in texts.items()
        }

        super().__init__(
            texts=texts,
            text_to_id=text_to_id
        )
