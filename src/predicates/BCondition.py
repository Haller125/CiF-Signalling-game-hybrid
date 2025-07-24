import logging
from dataclasses import dataclass

from src.belief.BeliefStore import BeliefStore
from src.predicates.PredicateTemplate import PredicateTemplate

@dataclass
class IBCondition:
    req_predicate: PredicateTemplate
    threshold: float = 0.0

    def __call__(self, state: BeliefStore, i, r=None) -> bool:
        raise NotImplementedError("Subclasses should implement this method.")


@dataclass
class BHasCondition(IBCondition):
    req_predicate: PredicateTemplate
    threshold: float = 0.0

    def __call__(self, state: BeliefStore, i, r=None) -> float:
        if not self.req_predicate:
            logging.error("Condition is empty.")
            return True
        return state.get_probability(self.req_predicate, i, r)
