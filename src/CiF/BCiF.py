from dataclasses import dataclass
from typing import List, Optional

from src.desire_formation import bdesire_formation
from src.select_intent.bselect_intent import bselect_intent
from src.social_exchange.BSocialExchange import BSocialExchange
from src.social_exchange.BSocialExchangeTemplate import BSocialExchangeTemplate
from src.social_exchange.SocialExchange import SocialExchange
from src.social_exchange.SocialExchangeTemplate import SocialExchangeTemplate
from src.types.DesireFormationTypes import DesireFormationType, BDesireFormationType
from src.types.NPCTypes import NPCType, BNPCType
from src.types.SelectIntentTypes import SelectIntentType


@dataclass
class BCiF:
    NPCs: List[BNPCType]
    actions: List[BSocialExchangeTemplate]
    desire_formation: Optional[BDesireFormationType] = bdesire_formation
    select_intent: Optional[SelectIntentType] = bselect_intent

    def iteration(self):
        volitions = [[
            npc, self.desire_formation(npc, self.NPCs, npc.beliefStore, self.actions)
        ] for npc in self.NPCs]

        actions: List[List[NPCType, BSocialExchange]] = [[npc, self.select_intent(volitiones, 0)] for npc, volitiones in
                                                        volitions]
        for npc, action in actions:
            if action is not None:
                npc.perform_action(action)
