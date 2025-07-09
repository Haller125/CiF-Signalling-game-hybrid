from dataclasses import dataclass
from typing import Sequence

from src.predicates.Effect import IEffect
from src.predicates.WorldState import WorldState
from src.types.NPCTypes import NPCType


@dataclass
class ExchangeEffects:
    accept_effects: Sequence[IEffect]
    reject_effects: Sequence[IEffect]

    def accept(self, state: WorldState, i: NPCType, r: NPCType) -> None:
        for effect in self.accept_effects:
            effect(state, i, r)

    def reject(self, state: WorldState, i: NPCType, r: NPCType) -> None:
        for effect in self.reject_effects:
            effect(state, i, r)
