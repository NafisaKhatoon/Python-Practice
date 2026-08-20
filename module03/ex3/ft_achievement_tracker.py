import random


achievements = [
    "Sharp Mind"
    "Unstoppable"
    "First Steps",
    "Boss Slayer",
    "Speed Runner",
    "Master Explorer",
    "Tresure Hunter",
    "Strategist",
    "Survivor",
    "Crafting Genius",
    "World Savior",
    "Collector Supreme",
    "Untouchable",
    "Hidden Path Finder",
    "Legendry Hero"
]


def gen_player_achievements():
    number = random.randint(5, 9)
    selected = random.sample(achievements, number)
    return set(selected)


print("=== Achievement Tracker System ===\n")

alice = gen_player_achievements()
bob = gen_player_achievements()
charlie = gen_player_achievements()
dylan = gen_player_achievements()

print("Player Alice:", alice)
print("Player Bob:", bob)
print("Player Charlie:", charlie)
print("Player Dylan:", dylan, "\n")

all_achievements = alice.union(bob, charlie, dylan)
print("All distinct achievements:", all_achievements, "\n")

common = alice.intersection(bob, charlie, dylan)
print("Common achievements:", common, "\n")

besides_alice: set[str] = bob.union(charlie, dylan)
print("Only Alice has:", alice.difference(besides_alice))

besides_bob: set[str] = alice.union(charlie, dylan)
print("Only Bob has:", bob.difference(besides_bob))

besides_charlie: set[str] = alice.union(charlie, dylan)
print("Only Charlie has:", charlie.difference(besides_charlie))

besides_dylan: set[str] = alice.union(charlie, dylan)
print("Only Dylan has:", dylan.difference(besides_dylan), "\n")

print("Alice is missing:", all_achievements.difference(alice))
print("Bob is missing:", all_achievements.difference(bob))
print("Charlie is missing:", all_achievements.difference(charlie))
print("Dylan is missing:", all_achievements.difference(dylan))
