def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temoerature() -> None:
    print("=== Garden Temperature ===\n")

    try:
        print("Input data is '25'")
        temperature = input_temperature("25")
        print(f"Temparture is now {temperature}°C\n")

    except ValueError:
        print("Invalid temperature!")

    try:
        print("Input data is 'abc'")
        temperature = input_temperature("abc")
        print(f"Temparture is now {temperature}°C")

    except ValueError as error:
        print(f"Caught input_temperature error: {error}\n")

    print("All tests completed - program didn't crash!")


test_temoerature()
