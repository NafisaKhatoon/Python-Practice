from ex0 import CreatureFactory, FlameFactory, AquaFactory


def testing_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()

    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())


def battle(factory1: CreatureFactory, factory2: CreatureFactory) -> None:
    first_creature = factory1.create_base()
    second_creature = factory2.create_base()

    print(f"{first_creature.describe()} \n vs.\n{second_creature.describe()}")
    print("fight!")
    print(first_creature.attack())
    print(second_creature.attack())


flame_factory = FlameFactory()
aqua_factory = AquaFactory()

print("Testing factory")
testing_factory(flame_factory)
print("\nTesting factory")
testing_factory(aqua_factory)
print("\nTesting battle:")
battle(flame_factory, aqua_factory)
