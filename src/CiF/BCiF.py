from dataclasses import dataclass, field
from typing import List, Dict, Sequence

from src.social_exchange.BSocialExchange import BSocialExchange
from src.social_exchange.BSocialExchangeTemplate import BSocialExchangeTemplate
from src.types.NPCTypes import BNPCType


@dataclass
class BCiF:
    NPCs: List[BNPCType]
    actions: List[BSocialExchangeTemplate]
    traits: List[str]
    relationships: List[str]
    actions_done: List[BSocialExchange] = field(default_factory=list)
    trait_opposites: Dict[str, Sequence[str]] = field(default_factory=dict)
    relationship_opposites: Dict[str, Sequence[str]] = field(default_factory=dict)

    def iteration(self):
        actions_done: List[BSocialExchange] = []

        for npc in self.NPCs:
            action = npc.iteration(self.NPCs, self.actions)

            if action is not None:
                actions_done.append(action)

        for npc in self.NPCs:
            npc.update_beliefs_from_observation(actions_done)

        self.actions_done.extend(actions_done)

    def get_exchanges(self, i, r):
        res = []
        for exch in self.actions_done:
            if (exch.initiator is i and exch.responder is r) or (exch.initiator is r and exch.responder is i):
                res.append(exch)
        return res
