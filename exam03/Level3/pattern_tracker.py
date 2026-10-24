def pattern_tracker(text: str) -> int:
    count = 0

    for i in range(len(text) - 1):
        first = text[i]
        second = text[i + 1]

        if first.isdigit() and second.isdigit():
            if int(second) == int(first) + 1:
                count += 1

    return count


print(pattern_tracker("123"))
print(pattern_tracker("12a34"))
print(pattern_tracker("987654321"))
print(pattern_tracker("01234567"))
print(pattern_tracker("abc"))
print(pattern_tracker("112233"))
