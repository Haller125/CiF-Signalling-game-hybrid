from dataclasses import dataclass

from src.predicates.Predicate import PredicateVisibility, Predicate
from src.types.NPCTypes import NPCType


@dataclass
class PredicateTemplate:
    pred_type: str  # "trait", "relationship" etc.
    subtype: str  # "trust", "friendship", "kind", "evil" etc.
    is_single: bool # whether the predicate is single (applies to one NPC) or relational (applies to two NPCs)
    value: float = 1  # the value of the predicate (e.g., trust level, friendship level, evilness level)
    visibility: PredicateVisibility = PredicateVisibility.PUBLIC

    def instantiate(self, subject: NPCType, target: NPCType = None):
        return Predicate(
            pred_type=self.pred_type,
            subtype=self.subtype,
            subject=subject,
            target=target,
            value=self.value,
            visibility=self.visibility
        )
