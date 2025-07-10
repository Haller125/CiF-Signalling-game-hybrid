from dataclasses import dataclass, field

from src.belief.BeliefStore import BeliefStore
from src.types.NPCTypes import BNPCType


@dataclass
class BNPC(BNPCType):
    id: int
    name: str
    beliefStore: BeliefStore = field(default_factory=BeliefStore)

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

    def perform_action(self, action):
        # Todo implement action logic
        print(f"{self.name} is performing action: {action}")
