from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - used for type hints only
    from src.social_exchange.BSocialExchange import BSocialExchange


@dataclass(slots=True, frozen=True)
class BVolition:
    social_exchange: "BSocialExchange"
    score: float
