from typing import Iterable, List, Sequence

from src.desire_formation.Volition import Volition
from src.predicates.WorldState import WorldState
from src.social_exchange.SocialExchangeTemplate import SocialExchangeTemplate
from src.types.NPCTypes import NPCType


def desire_formation(
    initiator: NPCType,
    others: Iterable[NPCType],
    state: WorldState,
    actions: Sequence[SocialExchangeTemplate],
) -> List[Volition]:
    volitions: List[Volition] = []

    for r in others:
        if r is initiator:
            continue
        for tpl in actions:

            exch = tpl.instantiate(initiator, r)

            if not exch.is_playable(state):
                continue

            score = exch.initiator_score(state)
            volitions.append(Volition(exch, score))

    volitions.sort(key=lambda t: t.score, reverse=True)
    return volitions




