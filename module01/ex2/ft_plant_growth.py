class Plant:

    name: str
    height: float
    age: int
    growth_rate: float

    def show(self) -> None:
        print(f"{self.name:} {self.height}cm, {self.age} days old ",)

    def grow(self) -> None:
        self.height = round(self.height + self.growth_rate, 1)

    def aging(self) -> None:
        self.age += 1


rose = Plant()
rose.name = "Rose"
rose.height = 25
rose.age = 30
rose.growth_rate = 0.8

print("=== Garden Plant Growth ===")
rose.show()

initial_height = rose.height

for day in range(1, 8):
    print(f"=== Day {day} ===")
    rose.grow()
    rose.aging()
    rose.show()

growth = round(rose.height - initial_height, 1)
print(f"Growth this week: {growth}cm")
