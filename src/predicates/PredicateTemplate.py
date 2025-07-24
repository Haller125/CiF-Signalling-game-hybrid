from __future__ import annotations

from dataclasses import dataclass

from src.types.NPCTypes import NPCType


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
