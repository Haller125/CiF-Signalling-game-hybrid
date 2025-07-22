from typing import Callable

from src.belief.BeliefStore import BeliefStore
from src.desire_formation.BVolition import BVolition
from src.desire_formation.Volition import Volition
from src.predicates.WorldState import WorldState
from src.social_exchange.BSocialExchangeTemplate import BSocialExchangeTemplate
from src.social_exchange.SocialExchange import SocialExchange
from src.social_exchange.SocialExchangeTemplate import SocialExchangeTemplate
from src.types.NPCTypes import NPCType

DesireFormationType = Callable[[NPCType, list[NPCType], WorldState, list[SocialExchange]], list[Volition]]


BDesireFormationType = Callable[[NPCType, list[NPCType], BeliefStore, list[BSocialExchangeTemplate]], BVolition]
