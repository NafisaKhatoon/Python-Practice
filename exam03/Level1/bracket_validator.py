def bracket_validator(s: str) -> bool:
    stack: list[str] = []

    for char in s:
        if char == "(" or char == "[" or char == "{":
            stack.append(char)

        elif char == ")" or char == "}" or char == "]":
            if not stack:
                return False

            last = stack.pop()

            if char == ")" and last != "(":
                return False
            if char == "]" and last != "[":
                return False
            if char == "}" and last != "{":
                return False

    return len(stack) == 0


print(bracket_validator("()"))
print(bracket_validator("()[]{}"))
print(bracket_validator("(]"))
print(bracket_validator("(()"))
print(bracket_validator(")("))
print(bracket_validator("{[]}"))
print(bracket_validator("hello(world)"))
print(bracket_validator("([)]"))
print(bracket_validator(""))
