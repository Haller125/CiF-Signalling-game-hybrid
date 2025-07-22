from dataclasses import dataclass
from typing import List, Optional

from src.desire_formation import bdesire_formation
from src.select_intent.bselect_intent import bselect_intent
from src.signal_interpolation.SignalInterpolation import update_beliefs_from_observation
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
    signal_interpolation = update_beliefs_from_observation

    def iteration(self):
        actions_done: List[BSocialExchange] = []

        for npc in self.NPCs:
            action = npc.iteration(self.NPCs, self.actions)

            if action is not None:
                actions_done.append(action)

        for npc in self.NPCs:
            npc.update_beliefs_from_observation(actions_done)
