from typing import List, Optional

from src.desire_formation.Volition import Volition
from src.social_exchange.SocialExchange import SocialExchange


def select_intent(
    volitions: List[Volition],
    threshold: float = 0.0,
) -> Optional[SocialExchange]:
    if not volitions or volitions[0].score < threshold:
        return None

    top_score = volitions[0].score
    toppers = [ex.social_exchange for ex in volitions if ex.score == top_score]

    return toppers[0]
