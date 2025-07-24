from dataclasses import dataclass
from typing import List

from src.belief.BeliefStore import BeliefStore
from src.predicates.PredicateTemplate import PredicateTemplate
from src.types.NPCTypes import NPCType

@dataclass
class IBEffect:
    label: str

    def __call__(self, state: BeliefStore, i: NPCType, r: NPCType) -> None:
        raise NotImplementedError("Effect must implement __call__ method.")


@dataclass
class BAddPredicateEffect(IBEffect):
    predicates: List[PredicateTemplate]
    probability: float = 0.9

    def __call__(self, state: BeliefStore, i: NPCType, r: NPCType) -> None:
        for predicate_template in self.predicates:
            predicate = predicate_template.instantiate(subject=i, target=r) if not predicate_template.is_single else predicate_template.instantiate(subject=i)
            state.update(predicate, self.probability)

@dataclass
class BRemovePredicateEffect(IBEffect):
    predicates: List[PredicateTemplate]

    def __call__(self, state: BeliefStore, i: NPCType, r: NPCType) -> None:
        for predicate_template in self.predicates:
            predicate = predicate_template.instantiate(subject=i, target=r) if not predicate_template.is_single else predicate_template.instantiate(subject=i)
            if predicate in state:
                state.update(predicate, 0.0)
