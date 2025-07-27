from dataclasses import dataclass
from typing import List

from src.belief.BeliefStore import BeliefStore
from src.predicates.PredicateTemplate import PredicateTemplate
from src.types.NPCTypes import BNPCType

@dataclass
class IBEffect:
    label: str
    predicates: List[PredicateTemplate]
    probability: float = 1.0

    def __call__(self, state: BeliefStore, i: BNPCType, r: BNPCType) -> None:
        raise NotImplementedError("Effect must implement __call__ method.")


@dataclass
class BAddPredicateEffect(IBEffect):
    label: str
    predicates: List[PredicateTemplate]
    probability: float = 1.0

    def __call__(self, state: BeliefStore, i: BNPCType, r: BNPCType) -> None:
        for predicate_template in self.predicates:
            predicate = predicate_template.instantiate(subject=i, target=r) if not predicate_template.is_single else predicate_template.instantiate(subject=i)
            state.update(predicate, self.probability)

@dataclass
class BRemovePredicateEffect(IBEffect):
    label: str
    predicates: List[PredicateTemplate]
    probability: float = 0.0

    def __call__(self, state: BeliefStore, i: BNPCType, r: BNPCType) -> None:
        for predicate_template in self.predicates:
            predicate = predicate_template.instantiate(subject=i, target=r) if not predicate_template.is_single else predicate_template.instantiate(subject=i)
            if predicate in state:
                state.update(predicate, self.probability)
