class Plant:
    def __init__(self, name: str, height: float, age: int):
        self.name = name
        self._height = 0.0
        self._age = 0

        if height < 0:
            print(f"{self.name}: Error, height can't be negative")
        else:
            self._height = float(height)

        if age < 0:
            print(f"{self.name}: Error, age can't be negative")
        else:
            self._age = age

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age

    def set_height(self, height: float) -> None:
        if height < 0:
            print(f"{self.name}: Error, height can't be negative")
            print("Height update rejected")
            return

        self._height = float(height)
        print(f"Height updated: {round(self._height)}cm")

    def set_age(self, age: int) -> None:
        if age < 0:
            print(f"{self.name}: Error, age can't be negative")
            print("Age update rejected")
            return

        self._age = age
        print(f"Age updated: {self._age} days")

    def __str__(self) -> str:
        return f"{self.name}: {self._height:.1f}cm, {self._age} days old"


if __name__ == "__main__":
    print("=== Garden Security System ===")

    plant = Plant("Rose", 15, 10)
    print(f"Plant created: {plant}")

    plant.set_height(25)
    plant.set_age(30)

    plant.set_height(-5)
    plant.set_age(-10)

    print(f"Current state: {plant}")
