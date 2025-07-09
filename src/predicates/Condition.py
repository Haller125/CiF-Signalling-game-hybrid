from dataclasses import dataclass
from typing import Callable, Sequence

from src.predicates.Predicate import Predicate
from src.predicates.PredicateTemplate import PredicateTemplate
from src.predicates.WorldState import WorldState
import logging

from src.types.NPCTypes import NPCType


class ICondition:
    def __call__(self, state: WorldState, i: NPCType, r: NPCType = None) -> bool:
        raise NotImplementedError("Condition must implement __call__ method.")


@dataclass
class HasCondition(ICondition):
    req_predicates: Sequence[PredicateTemplate]

    def __call__(self, state: WorldState, i: NPCType, r: NPCType = None) -> bool:
        if not self.req_predicates:
            logging.error("Condition is empty.")
            return False
        for predicate in self.req_predicates:
            pred: Predicate = predicate.instantiate(subject=i, target=r) if not predicate.is_single else predicate.instantiate(subject=i)
            if pred not in state.predicates:
                logging.debug(f"Condition failed for predicate {pred}.")
                return False
        logging.debug("Condition passed.")
        return True
