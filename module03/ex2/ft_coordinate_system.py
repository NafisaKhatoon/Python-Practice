import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        coordinates = input(
            "Enter new coordinates as floats in format 'x,y,z': "
        )

        try:
            values = coordinates.split(",")

            if len(values) != 3:
                print("Invalid syntax")
                continue

            x = float(values[0].strip())
            y = float(values[1].strip())
            z = float(values[2].strip())

            return (x, y, z)

        except ValueError as error:
            parameter = coordinates.split(",")[1].strip()
            print(f"Error on parameter '{parameter}': {error}")


print("=== Game Coordinate System ===\n")

print("Get a first set of coordinates")
first = get_player_pos()

print(f"Got a first tuple: {first}")
print(f"It includes: X={first[0]}, Y={first[1]}, Z={first[2]}")

distance_center = math.sqrt(
    first[0] ** 2 + first[1] ** 2 + first[2] ** 2
)

print(f"Distance to center: {round(distance_center, 4)}")

print("Get a second set of coordinates")
second = get_player_pos()

distance_between = math.sqrt(
    (second[0] - first[0]) ** 2 +
    (second[1] - first[1]) ** 2 +
    (second[2] - first[2]) ** 2
)

print(f"Distance between the 2 sets of coordinates: "
      f"{round(distance_between, 4)}")
