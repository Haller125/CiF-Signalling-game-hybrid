from dataclasses import dataclass

from src.social_exchange.SocialExchange import SocialExchange


@dataclass(slots=True, frozen=True)
class Volition:
    social_exchange: SocialExchange
    score: float
