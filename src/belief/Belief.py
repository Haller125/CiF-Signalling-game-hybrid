from src.predicates.Predicate import Predicate

class Belief:
    def __init__(self, predicate: Predicate, probability: float):
        self.predicate = predicate
        self.probability = probability

