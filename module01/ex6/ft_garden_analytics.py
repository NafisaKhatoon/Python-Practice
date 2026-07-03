class Plant:
    class Statistics:
        def __init__(self):
            self.grow = 0
            self.age = 0
            self.show = 0

        def display(self):
            print(f"Stats: {self.grow} grow, {self.age} age, {self.show} show")

    def __init__(self, name: str, height: float, age: int):
        self._name = name
        self._height = height
        self._age = age
        self._stats = Plant.Statistics()

    def grow(self):
        self._height += 5
        self._stats.grow += 1

    def age(self):
        self._age += 1
        self._stats.age += 1

    def show(self):
        self._stats.show += 1
        print(f"{self._name}: {self._height:.1f}cm, {self._age} days old")

    @staticmethod
    def older_than_year(days):
        return days > 365

    @classmethod
    def anonymous(cls):
        return cls("Unknown plant", 0, 0)


class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self.color = color
        self.bloomed = False

    def bloom(self):
        self.bloomed = True

    def show(self):
        super().show()
        print("Color:", self.color)
        if self.bloomed:
            print(f"{self._name} is blooming beautifully!")
        else:
            print(f"{self._name} has not bloomed yet")


class Tree(Plant):
    def __init__(self, name, height, age, trunk):
        super().__init__(name, height, age)
        self.trunk = trunk
        self.shade_calls = 0

    def show(self):
        super().show()
        print(f"Trunk diameter: {self.trunk:.1f}cm")

    def produce_shade(self):
        self.shade_calls += 1
        print(
            f"Tree {self._name} now produces a shade of "
            f"{self._height:.1f}cm long and {self.trunk:.1f}cm wide.")

    def show_stats(self):
        self._stats.display()
        print(self.shade_calls, "shade")


class Seed(Flower):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age, color)
        self.seeds = 0

    def bloom(self):
        super().bloom()
        self.seeds = 42

    def show(self):
        super().show()
        print("Seeds:", self.seeds)


def display_statistics(plant):
    plant._stats.display()


if __name__ == "__main__":
    print("=== Garden statistics ===")
    print("=== Check year-old")
    print("Is 30 days more than a year? ->", Plant.older_than_year(30))
    print("Is 400 days more than a year? ->", Plant.older_than_year(400))

    print("\n=== Flower")
    rose = Flower("Rose", 15, 10, "red")
    rose.show()
    print("[statistics for Rose]")
    display_statistics(rose)
    print("[asking the rose to grow and bloom]")

    rose.grow()
    rose.bloom()
    rose.show()
    print("[statistics for Rose]")
    display_statistics(rose)

    print("\n=== Tree")
    oak = Tree("Oak", 200, 365, 5)
    oak.show()
    print("[statistics for Oak]")
    oak.show_stats()
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print("[statistics for Oak]")
    oak.show_stats()

    print("\n=== Seed")
    sunflower = Seed("Sunflower", 80, 45, "yellow")
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age()
    sunflower.bloom()
    sunflower.show()
    print("[statistics for Sunflower]")
    display_statistics(sunflower)

    print("\n=== Anonymous")
    unknown = Plant.anonymous()
    unknown.show()
    print("[statistics for Unknown plant]")
    display_statistics(unknown)
