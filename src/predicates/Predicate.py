from dataclasses import dataclass
import enum

from src.predicates.PredicateTemplate import PredicateTemplate
from src.types.NPCTypes import NPCType


class PredicateVisibility(enum.Enum):
    PRIVATE = 'private'
    PUBLIC = 'public'

@dataclass(frozen=True, slots=True)
class Predicate:
    pred_type: str        # "trait", "relationship" etc.
    subtype: str          # "trust", "friendship", "kind", "evil" etc.
    subject: NPCType          # first NPC (itself)
    is_single: bool
    template: PredicateTemplate
    target: NPCType = None    # second NPC (if applicable, e.g., in relationships)

    def __str__(self):
        return f"{self.pred_type}({self.subject}, {self.target if self.target else 'None'})"

    def __repr__(self):
        return f"Predicate(pred_type={self.pred_type}, subtype={self.subtype}, subject={self.subject.name}, target={self.target.name if self.target else None})"

    def __eq__(self, other):
        if not isinstance(other, Predicate):
            return NotImplemented
        return (self.pred_type == other.pred_type and
                self.subtype == other.subtype and
                self.subject.id == other.subject.id and
                (self.target.id if self.target else None) == (other.target.id if other.target else None))

    def matches_template(self, temp: PredicateTemplate):
        return (self.pred_type == temp.pred_type and
                self.subtype == temp.subtype and
                self.is_single == temp.is_single)
