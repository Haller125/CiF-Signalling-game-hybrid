from dataclasses import dataclass, field

from src.belief.BeliefStore import BeliefStore
from src.predicates.Predicate import Predicate

@dataclass
class NPC:
    id: int
    name: str
    # beliefs: BeliefStore = field(default_factory=BeliefStore)

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

    def desire_formation(self):
        pass


