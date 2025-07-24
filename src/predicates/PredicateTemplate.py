from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.types.NPCTypes import NPCType

if TYPE_CHECKING:  # pragma: no cover - used for type hints only
    from src.predicates.Predicate import Predicate


@dataclass
class PredicateTemplate:
    pred_type: str  # "trait", "relationship" etc.
    subtype: str  # "trust", "friendship", "kind", "evil" etc.
    is_single: bool  # whether the predicate is single (applies to one NPC) or relational (applies to two NPCs)

    def instantiate(self, subject: NPCType, target: NPCType = None) -> "Predicate":
        from src.predicates.Predicate import Predicate

        return Predicate(
            pred_type=self.pred_type,
            subtype=self.subtype,
            subject=subject,
            target=target,
            is_single=self.is_single,
            template=self,
        )
