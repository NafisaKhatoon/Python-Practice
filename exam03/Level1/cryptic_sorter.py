def count_vowels(s: str) -> int:
    count = 0
    for ch in s:
        if ch.lower() in "aeiou":
            count += 1
    return count


def comes_before(a: str, b: str) -> bool:
    if len(a) != len(b):
        return len(a) < len(b)
    if a.lower() != b.lower():
        return a.lower() < b.lower()
    return count_vowels(a) < count_vowels(b)


def cryptic_sorter(strings: list[str]) -> list[str]:
    result = strings[:]
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        while j >= 0 and comes_before(current, result[j]):
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current

    return result


print(cryptic_sorter(["apple", "cat", "banana", "dog", "elephant"]))
print(cryptic_sorter(["aaa", "bbb", "AAA", "BBB"]))
print(cryptic_sorter(["hello", "world", "hi", "test"]))
print(cryptic_sorter([]))
print(cryptic_sorter(['']))
