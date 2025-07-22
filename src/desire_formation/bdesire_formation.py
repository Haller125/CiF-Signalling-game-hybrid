from typing import Iterable, Sequence, List

from src.belief.BeliefStore import BeliefStore
from src.desire_formation.BVolition import BVolition
from src.desire_formation.Volition import Volition
from src.social_exchange.BSocialExchangeTemplate import BSocialExchangeTemplate
from src.social_exchange.SocialExchangeTemplate import SocialExchangeTemplate
from src.types.NPCTypes import NPCType


def desire_formation(
    initiator: NPCType,
    others: Iterable[NPCType],
    state: BeliefStore,
    actions: Sequence[BSocialExchangeTemplate],
) -> List[BVolition]:
    volitions: List[BVolition] = []

    for r in others:
        if r is initiator:
            continue
        for tpl in actions:

            exch = tpl.instantiate(initiator, r)

            if not exch.is_playable(state):
                continue

            score = exch.initiator_score(state)
            volitions.append(BVolition(exch, score))

    volitions.sort(key=lambda t: t.score, reverse=True)
    return volitions
