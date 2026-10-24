def hidenp(small: str, big: str) -> bool:
    i = 0
    for ch in big:
        if i < len(small) and ch == small[i]:
            i += 1
    return i == len(small)


print(hidenp("abc", "aXbYcZ"))   # True
print(hidenp("abc", "acb"))      # False  (wrong order)
print(hidenp("ABC", "abc"))      # False  (case-sensitive)
print(hidenp("", "anything"))    # True   (empty string)
print(hidenp("abc", ""))         # False
