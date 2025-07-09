from src.predicates.Predicate import Predicate


class NPC:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        # self.belief_store = belief_store
        # self.goals = goals
        # self.utility_preferences = utility_preferences

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

    def desire_formation(self):
        pass

    def add_trait(self, predicate: Predicate, value: bool):
        self.traits[predicate] = value

