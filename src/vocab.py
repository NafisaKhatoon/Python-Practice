"""Token id to text mapping built from the vocabulary file."""
import json


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


class Vocab:
    """Maps token ids to the real text they stand for."""

    def __init__(self, path: str) -> None:
        with open(path, encoding="utf-8") as file:
            raw: dict[str, int] = json.load(file)
        decoder = _byte_decoder()
        self.texts: dict[int, str] = {}
        for token, idx in raw.items():
            try:
                data = bytes(decoder[c] for c in token)
                self.texts[idx] = data.decode("utf-8")
            except (KeyError, UnicodeDecodeError):
                continue  # partial UTF-8 byte tokens are not used
        self.text_to_id = {t: i for i, t in self.texts.items()}
