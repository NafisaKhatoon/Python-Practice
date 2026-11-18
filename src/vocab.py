import json


def byte_to_char() -> dict[int, str]:
    """The model stores bytes as printable look-alike characters."""
    printable = (
        list(range(33, 127)) + list(range(161, 173)) + list(range(174, 256))
    )
    table = {}
    extra = 0
    for byte in range(256):
        if byte in printable:
            table[byte] = chr(byte)
        else:
            table[byte] = chr(256 + extra)
            extra += 1
    return table


def load_token_texts(path: str) -> list[str]:
    """Return a list where texts[token_id] is the real text of that token."""
    with open(path, encoding="utf-8") as file:
        vocab: dict[str, int] = json.load(file)

    char_to_byte = {char: byte for byte, char in byte_to_char().items()}
    texts = [""] * (max(vocab.values()) + 1)  # "" means "unusable token"

    for token, token_id in vocab.items():
        try:
            raw_bytes = bytes(char_to_byte[char] for char in token)
            texts[token_id] = raw_bytes.decode("utf-8")
        except (KeyError, UnicodeDecodeError):
            pass  # token is only half of a character: leave it unusable
    return texts


def is_plain(text: str) -> bool:
    """Safe inside a JSON string: no quote, no backslash, no control char."""
    return text != "" and all(c not in '"\\' and ord(c) >= 32 for c in text)


def closes_string(text: str) -> bool:
    """A token that ends with a quote, with only plain text before it."""
    return text.endswith('"') and (len(text) == 1 or is_plain(text[:-1]))
