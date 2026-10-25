def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if not (2 <= from_base <= 36 and 2 <= to_base <= 36):
        return "ERROR"
    if number == "":
        return "ERROR"
    for char in number.upper():
        if char not in digits[:from_base]:
            return "ERROR"

    value = int(number, from_base)

    if value == 0:
        return "0"

    result = ""
    while value > 0:
        result = digits[value % to_base] + result
        value //= to_base
    return result


print(number_base_converter("3", 10, 2))      # 11
print(number_base_converter("ff", 16, 10))    # 255
print(number_base_converter("123", 10, 2))    # 1111011
print(number_base_converter("123", 1, 10))    # ERROR
print(number_base_converter("G", 16, 10))     # ERROR
print(number_base_converter("0x1F", 16, 10))  # ERROR
