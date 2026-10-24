def echo_validator(text: str) -> bool:
    cleaned = ""
    for ch in text:
        if ch.isalpha():
            cleaned += ch.lower()

    return cleaned == cleaned[::-1]


print(echo_validator("A man a plan a canal Panama"))   # True
print(echo_validator("Race a car"))                    # False
print(echo_validator("No 'x' in Nixon!"))              # True
print(echo_validator("hello"))                         # False
print(echo_validator(""))                              # True
print(echo_validator("Was it a car or a cat I saw"))   # True
print(echo_validator("abccba"))                        # False
