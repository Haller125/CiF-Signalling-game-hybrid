from dataclasses import dataclass, field

from src.belief.BeliefStore import BeliefStore
from src.social_exchange.BSocialExchange import BSocialExchange
from src.types.NPCTypes import BNPCType


@dataclass
class BNPC(BNPCType):
    id: int
    name: str
    beliefStore: BeliefStore = field(default_factory=BeliefStore)

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

    def perform_action(self, action: BSocialExchange):
        action.perform(self.beliefStore)
