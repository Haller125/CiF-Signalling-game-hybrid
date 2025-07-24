import logging
from dataclasses import dataclass, field
from typing import Optional, Sequence

from src.predicates.Condition import HasCondition
from src.predicates.Effect import IEffect
from src.predicates.WorldState import WorldState
from src.types.NPCTypes import NPCType


@dataclass(slots=True)
class Rule:
    name: str
    condition: Sequence[HasCondition]
    weight: Optional[float] = None
    effects: Sequence[IEffect] = field(default_factory=list)

    def is_true(self, state: WorldState, i: NPCType, r: NPCType = None) -> bool:
        if not self.condition:
            logging.error(f"Rule '{self.name}' has no conditions.")
            return True
        return all(cond(state, i, r) for cond in self.condition)

    def get_weight(self, state: WorldState, i: NPCType, r: NPCType = None) -> float:
        if self.weight is None:
            logging.error(f"Rule '{self.name}' has no weight defined.")
            return 0.0
        return self.weight if self.is_true(state, i, r) else 0.0

    def fire(self, state: WorldState, i: NPCType, r: NPCType = None) -> None:
        if self.effects and self.is_true(state, i, r):
            for eff in self.effects:
                eff(state, i, r)
