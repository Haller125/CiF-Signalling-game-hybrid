from typing import Callable

from src.desire_formation.Volition import Volition
from src.predicates.WorldState import WorldState
from src.social_exchange.SocialExchange import SocialExchange
from src.types.NPCTypes import NPCType

DesireFormationType = Callable[[NPCType, list[NPCType], WorldState, list[SocialExchange]], list[Volition]]
