class GardenError(Exception):
    def __init__(self, message="Unknown garden error"):
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message="Unknown plant error"):
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message="Unknown water error"):
        super().__init__(message)


def test_plant():
    raise PlantError("The tomato plant is wilting!")


def test_water():
    raise WaterError("Not enough water in the tank!")


def main():
    print("=== Custom Garden Errors Demo ===\n")

    print("Testing Planterror...")
    try:
        test_plant()
    except PlantError as error:
        print(f"Caught PlantError: {error}\n")

    print("Testing WaterError...")
    try:
        test_water()
    except WaterError as error:
        print(f"Caught WaterError: {error}\n")

    print("Testing catching all garden errors...")

    try:
        test_plant()
    except GardenError as error:
        print(f"Caught GardenError: {error}")

    try:
        test_water()
    except GardenError as error:
        print(f"Caught GardenError: {error}\n")

    print("All custom error types work correctly!")


main()
