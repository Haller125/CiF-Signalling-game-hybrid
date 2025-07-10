import logging
from dataclasses import dataclass
from typing import List

from src.belief.BeliefStore import BeliefStore
from src.predicates.Condition import ICondition
from src.predicates.PredicateTemplate import PredicateTemplate


@dataclass
class BHasCondition(ICondition):
    req_predicates: List[PredicateTemplate]
    threshold: float = 0.0

    def __call__(self, state: BeliefStore, i, r=None) -> bool:
        if not self.req_predicates:
            return True
        cumulative_prob = 0.0
        for predicate_temp in self.req_predicates:
            cumulative_prob += state.get_probability(predicate_temp, i, r)
        return (cumulative_prob / len(self.req_predicates)) >= self.threshold
