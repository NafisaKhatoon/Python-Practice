def inter(s1: str, s2: str) -> str:
    result = ""

    for char in s1:
        if char in s2 and char not in result:
            result += char

    return result


print(inter("hello", "world"))   # "lo"
print(inter("aabbcc", "abc"))    # "abc"
print(inter("abc", "xyz"))       # ""
print(inter("", "abc"))          # ""
print(inter("Aa", "a"))          # "a"
print(inter("banana", "band"))   # ban
