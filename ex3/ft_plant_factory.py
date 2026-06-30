class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age

    def grow(self) -> None:
        self.height += 25.0
        self.age += 1

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age} days old")


print("=== Plant Factory Output ===")

plants = [
    Plant("Rose", 25.0, 30),
    Plant("Ook", 200.0, 365),
    Plant("Cactus", 5.0, 90),
    Plant("Sunflower", 80.0, 45),
    Plant("Fern", 15.0, 120)
]


for each in plants:
    print("Created:", end=" ")
    each.show()
