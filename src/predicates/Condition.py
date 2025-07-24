import logging
from dataclasses import dataclass
from typing import Sequence

from src.predicates.Predicate import Predicate
from src.predicates.PredicateTemplate import PredicateTemplate
from src.predicates.WorldState import WorldState
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
            return True
        for predicate_temp in self.req_predicates:
            pred: Predicate = predicate_temp.instantiate(subject=i, target=r) if not predicate_temp.is_single else predicate_temp.instantiate(subject=i)
            if pred not in state.predicates:
                logging.debug(f"Condition failed for predicate {pred}.")
                return False
        logging.debug("Condition passed.")
        return True
