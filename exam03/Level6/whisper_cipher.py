def whisper_cipher(text: str, shift: int) -> str:
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    for char in text:
        if char in lower:
            index = lower.index(char)
            result += lower[(index + shift) % 26]
        elif char in upper:
            index = upper.index(char)
            result += upper[(index + shift) % 26]
        else:
            result += char

    return result


print(whisper_cipher("Hello, World!", 3))   # Khoor, Zruog!
print(whisper_cipher("Khoor, Zruog!", -3))  # Hello, World!
print(whisper_cipher("xyz", 2))             # zab
print(whisper_cipher("ABC123def", 5))       # FGH123ijk
