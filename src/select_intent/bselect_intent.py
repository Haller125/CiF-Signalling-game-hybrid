from typing import List, Optional

from src.desire_formation.BVolition import BVolition
from src.social_exchange.BSocialExchange import BSocialExchange


def bselect_intent(
    volitions: List[BVolition],
    threshold: float = 0.0,
) -> Optional[BSocialExchange]:
    if not volitions or volitions[0].score < threshold:
        return None

    top_score = volitions[0].score
    toppers = [ex.social_exchange for ex in volitions if ex.score >= top_score]

    return toppers[0]
