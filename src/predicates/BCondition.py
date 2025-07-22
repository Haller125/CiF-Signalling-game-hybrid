import logging
from dataclasses import dataclass
from typing import List

from src.belief.BeliefStore import BeliefStore
from src.predicates.Condition import ICondition
from src.predicates.PredicateTemplate import PredicateTemplate

@dataclass
class IBCondition:
    req_predicates: List[PredicateTemplate]
    threshold: float = 0.0

    def __call__(self, state: BeliefStore, i, r=None) -> bool:
        raise NotImplementedError("Subclasses should implement this method.")

    def __str__(self):
        return f"IBCondition(req_predicates={self.req_predicates}, threshold={self.threshold})"


@dataclass
class BHasCondition(ICondition):
    req_predicates: List[PredicateTemplate]
    threshold: float = 0.0

    def __call__(self, state: BeliefStore, i, r=None) -> bool:
        if not self.req_predicates:
            logging.error("Condition is empty.")
            return True
        cumulative_prob = 0.0
        for predicate_temp in self.req_predicates:
            cumulative_prob += state.get_probability(predicate_temp, i, r)
        return (cumulative_prob / len(self.req_predicates)) >= self.threshold
