from dataclasses import dataclass
from typing import List, Optional

from src.predicates.WorldState import WorldState
from src.social_exchange.SocialExchange import SocialExchange
from src.social_exchange.SocialExchangeTemplate import SocialExchangeTemplate
from src.types.DesireFormationTypes import DesireFormationType
from src.desire_formation.desire_formation import desire_formation
from src.select_intent.select_intent import select_intent
from src.types.NPCTypes import NPCType
from src.types.SelectIntentTypes import SelectIntentType


@dataclass
class CiF:
    NPCs: List[NPCType]
    actions: List[SocialExchangeTemplate]
    state: WorldState
    desire_formation: Optional[DesireFormationType] = desire_formation
    select_intent: Optional[SelectIntentType] = select_intent

    def iteration(self):
        volitions = [[
            npc, self.desire_formation(npc, self.NPCs, self.state, self.actions)
        ] for npc in self.NPCs]

        actions: List[List[NPCType, SocialExchange]] = [[npc, self.select_intent(volitiones, 0)] for npc, volitiones in volitions]
        for npc, action in actions:
            if action is not None:
                action.perform(self.state)

