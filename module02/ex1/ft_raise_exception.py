def input_temperature(temp_str: str) -> int:
    temperature = int(temp_str)

    if temperature > 40:
        raise ValueError(f"{temperature}°C is too hot for plants (max 40°C)")
    if temperature < 0:
        raise ValueError(f"{temperature}°C is too cold for plants (min 0°C)")

    return temperature


def test_temperature():
    print("=== Garden Temperature Checker ===")

    temperature = ["25", "abc", "100", "-50"]

    for temp in temperature:
        print(f"input data is '{temp}'")

        try:
            temperature = input_temperature(temp)
            print(f"Temperature is now {temp}°C")
        except ValueError as error:
            print(f"caught input_temperature error: {error}")

    print("All tests completed - program didn't crash")


test_temperature()
