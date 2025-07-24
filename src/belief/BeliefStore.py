from dataclasses import dataclass, field
from typing import List

from src.belief.Belief import Belief
from src.predicates.Predicate import Predicate
from src.predicates.PredicateTemplate import PredicateTemplate
from src.types.NPCTypes import BNPCType


@dataclass
class BeliefStore:
    beliefs: List[Belief] = field(default_factory=list)

    def get_probability(self, predicate_temp: PredicateTemplate, i: BNPCType, r: BNPCType):
        for belief in self.beliefs:
            if belief.predicate_template == predicate_temp and belief.predicate.subject == i and (belief.predicate.target == r or r is None):
                return belief.probability
        return 0.5

    def __iter__(self):
        return iter(self.beliefs)

    def __contains__(self, item: Belief | Predicate):
        if isinstance(item, Belief):
            return item in self.beliefs
        elif isinstance(item, Predicate):
            return any(belief.predicate == item for belief in self.beliefs)
        return False

    def update(self, predicate: Predicate, probability: float):
        for belief in self.beliefs:
            if belief.predicate == predicate:
                belief.probability = probability
                return
        new_belief = Belief(predicate=predicate, probability=probability, predicate_template=predicate.template)
        self.beliefs.append(new_belief)

    def add_belief(self, predicate: Predicate, probability: float = 1.0):
        if not isinstance(predicate, Predicate):
            raise TypeError("Only Predicate instances can be added as traits.")
        self.update(predicate, probability)
