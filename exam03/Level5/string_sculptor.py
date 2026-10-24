def string_sculptor(text: str) -> str:
    result = ""
    letter_count = 0

    for c in text:
        if c.isalpha():
            if letter_count % 2 == 0:
                result += c.lower()
            else:
                result += c.upper()
            letter_count += 1
        else:
            result += c
    return result


print(string_sculptor("Hello World"))
