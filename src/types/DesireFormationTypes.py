from typing import Callable

from src.belief.BeliefStore import BeliefStore
from src.desire_formation.BVolition import BVolition
from src.social_exchange.BSocialExchangeTemplate import BSocialExchangeTemplate
from src.types.NPCTypes import NPCType

BDesireFormationType = Callable[[NPCType, list[NPCType], BeliefStore, list[BSocialExchangeTemplate]], BVolition]
