from dataclasses import dataclass
from typing import Sequence

from src.irs.BIRS import BInfluenceRuleSet
from src.predicates.BCondition import IBCondition
from src.predicates.PredicateTemplate import PredicateTemplate
from src.social_exchange.BExchangeEffects import BExchangeEffects
from src.social_exchange.BSocialExchange import BSocialExchange
from src.types.NPCTypes import NPCType


@dataclass
class BSocialExchangeTemplate:
    name: str
    preconditions: Sequence[IBCondition]
    intent: PredicateTemplate
    initiator_irs: BInfluenceRuleSet
    responder_irs: BInfluenceRuleSet
    effects: BExchangeEffects

    def instantiate(self, initiator: NPCType, responder: NPCType) -> BSocialExchange:
        intent = self.intent.instantiate(subject=initiator, target=responder)

        return BSocialExchange(
            name=self.name,
            initiator=initiator,
            responder=responder,
            intent=intent,
            preconditions=self.preconditions,
            initiator_irs=self.initiator_irs,
            responder_irs=self.responder_irs,
            effects=self.effects,
        )
