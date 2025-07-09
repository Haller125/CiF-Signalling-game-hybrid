from typing import Callable, List, Optional

from src.desire_formation.Volition import Volition
from src.social_exchange.SocialExchange import SocialExchange

SelectIntentType = Callable[[List[Volition], Optional[float]], Optional[SocialExchange]]
