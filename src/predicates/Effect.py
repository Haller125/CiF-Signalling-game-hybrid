from dataclasses import dataclass
from typing import List

from src.predicates.PredicateTemplate import PredicateTemplate
from src.predicates.WorldState import WorldState
from src.types.NPCTypes import NPCType


@dataclass
class IEffect:
    label: str

    def __call__(self, state: WorldState, i: NPCType, r: NPCType) -> None:
        raise NotImplementedError("Effect must implement __call__ method.")

@dataclass
class AddPredicateEffect(IEffect):
    predicates: List[PredicateTemplate]

    def __call__(self, state: WorldState, i: NPCType, r: NPCType) -> None:
        for predicate_template in self.predicates:
            predicate = predicate_template.instantiate(subject=i, target=r) if not predicate_template.is_single else predicate_template.instantiate(subject=i)
            state.add(predicate)

@dataclass
class RemovePredicateEffect(IEffect):
    predicates: List[PredicateTemplate]

    def __call__(self, state: WorldState, i: NPCType, r: NPCType) -> None:
        for predicate_template in self.predicates:
            predicate = predicate_template.instantiate(subject=i, target=r) if not predicate_template.is_single else predicate_template.instantiate(subject=i)
            state.remove(predicate)
