from dataclasses import dataclass
from typing import List

from src.signal_interpolation.SignalInterpolation import update_beliefs_from_observation
from src.social_exchange.BSocialExchange import BSocialExchange
from src.social_exchange.BSocialExchangeTemplate import BSocialExchangeTemplate
from src.types.NPCTypes import BNPCType


@dataclass
class BCiF:
    NPCs: List[BNPCType]
    actions: List[BSocialExchangeTemplate]
    signal_interpolation = update_beliefs_from_observation

    def iteration(self):
        actions_done: List[BSocialExchange] = []

        for npc in self.NPCs:
            action = npc.iteration(self.NPCs, self.actions)

            if action is not None:
                actions_done.append(action)

        for npc in self.NPCs:
            npc.update_beliefs_from_observation(actions_done)
