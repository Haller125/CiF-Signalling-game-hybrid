from src.belief.Belief import Belief
from src.predicates.Predicate import Predicate

class BeliefStore:
    def __init__(self, beliefs: dict[Predicate, Belief]):
        self.beliefs = beliefs


