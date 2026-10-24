def count_char(text, letter):
    count = 0
    for c in text:
        if c == letter:
            count += 1
    return count


def string_permutation_checker(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False

    for c in s1:
        if count_char(s1, c) != count_char(s2, c):
            return False

    return True


print(string_permutation_checker("abc", "cba"))        # True
print(string_permutation_checker("Abc", "abc"))        # False (case matters)
print(string_permutation_checker("a b", "ab"))         # False (space counts)
print(string_permutation_checker("a b", "b a"))        # True
print(string_permutation_checker("hi!", "!ih"))        # True
print(string_permutation_checker("", ""))              # True
