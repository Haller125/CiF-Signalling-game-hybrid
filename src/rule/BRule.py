import logging
import math
from dataclasses import dataclass, field
from typing import Optional, Sequence

from src.belief.BeliefStore import BeliefStore
from src.predicates.BCondition import BHasCondition
from src.predicates.BEffect import IBEffect
from src.types.NPCTypes import NPCType, BNPCType


@dataclass(slots=True)
class BRule:
    name: str
    condition: Sequence[BHasCondition]
    weight: Optional[float] = None
    effects: Sequence[IBEffect] = field(default_factory=list)

    def is_true(self, state: BeliefStore, i: NPCType, r: NPCType = None) -> bool:
        if not self.condition:
            logging.error(f"Rule '{self.name}' has no conditions.")
            return True
        return all(cond(state, i, r) for cond in self.condition)

    def get_weight(self, state: BeliefStore, i: NPCType, r: NPCType = None) -> float:
        if self.weight is None:
            logging.error(f"Rule '{self.name}' has no weight defined.")
            return 0.0
        return self.weight if self.is_true(state, i, r) else 0.0

    def probability(self, beliefs: BeliefStore, i: BNPCType, r: BNPCType = None) -> float:
        if not self.condition:
            raise ValueError(f"Rule '{self.name}' has no conditions.")

        cond_probs = [float(cond(beliefs, i, r)) for cond in self.condition]
        if any(p < 0 or p > 1 for p in cond_probs):
            raise ValueError("Condition probabilities must be within [0,1].")

        prob = math.prod(cond_probs)
        return prob
