def count_char(text, letter):
    count = 0
    for c in text:
        if c == letter:
            count += 1
    return count


def anagram(s1: str, s2: str) -> bool:
    s1 = s1.lower()
    s2 = s2.lower()

    a = ""
    for c in s1:
        if c != " ":
            a += c

    b = ""
    for c in s2:
        if c != " ":
            b += c

    if len(a) != len(b):
        return False

    for c in a:
        if count_char(a, c) != count_char(b, c):
            return False

    return True


print(anagram("listen", "silent"))
print(anagram("Triangle", "Integral"))
print(anagram("Dormitory", "Dirty Room"))
print(anagram("hello", "world"))
print(anagram("", ""))
print(anagram("abc", "abcc"))
