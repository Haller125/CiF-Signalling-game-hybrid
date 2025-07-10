from dataclasses import dataclass

from src.predicates.Predicate import Predicate
from src.predicates.PredicateTemplate import PredicateTemplate


@dataclass
class Belief:
    predicate: Predicate
    probability: float
    predicate_template: PredicateTemplate

