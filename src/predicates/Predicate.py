from dataclasses import dataclass
import enum
import typing

from src.types.NPCTypes import NPCType


class PredicateVisibility(enum.Enum):
    PRIVATE = 'private'
    PUBLIC = 'public'

@dataclass(frozen=True, slots=True)
class Predicate:
    pred_type: str        # "trait", "relationship" etc.
    subtype: str          # "trust", "friendship", "kind", "evil" etc.
    subject: NPCType          # first NPC (itself)
    target: NPCType = None    # second NPC (if applicable, e.g., in relationships)
    value: float = 1      # the value of the predicate (e.g., trust level, friendship level, evilness level)
    visibility: PredicateVisibility = PredicateVisibility.PUBLIC

    def __str__(self):
        return f"{self.pred_type}({self.subject}, {self.target if self.target else 'None'}, {self.value})"

    def __hash__(self):
        return hash((self.pred_type, self.subtype, self.subject.id, self.target.id if self.target else None, self.value, self.visibility))

    def __repr__(self):
        return f"Predicate(pred_type={self.pred_type}, subtype={self.subtype}, subject={self.subject.name}, target={self.target.name if self.target else None}, value={self.value}, visibility={self.visibility})"

    def __eq__(self, other):
        if not isinstance(other, Predicate):
            return NotImplemented
        return (self.pred_type == other.pred_type and
                self.subtype == other.subtype and
                self.subject.id == other.subject.id and
                (self.target.id if self.target else None) == (other.target.id if other.target else None) and
                self.value == other.value and
                self.visibility == other.visibility)