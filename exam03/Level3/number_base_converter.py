def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if not (2 <= from_base <= 36 and 2 <= to_base <= 36):
        return "ERROR"
    if not number.isalnum():
        return "ERROR"

    try:
        value = int(number, from_base)   # step 1: read the number in from_base
    except ValueError:
        return "ERROR"                   # invalid digit for that base

    if value == 0:
        return "0"

    result = ""
    while value > 0:                     # step 2: write it in to_base
        result = digits[value % to_base] + result
        value //= to_base
    return result


print(number_base_converter("3", 10, 2))     # "ERROR"
print(number_base_converter("FF", 16, 10))   # 255
print(number_base_converter("123", 10, 2))   # 111101
print(number_base_converter("123", 1, 10))   # "ERROR"
print(number_base_converter("G", 16, 10))    # "ERROR"
