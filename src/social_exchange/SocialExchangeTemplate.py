from dataclasses import dataclass
from typing import Sequence

from src.irs.IRS import InfluenceRuleSet
from src.predicates.Condition import HasCondition, ICondition
from src.predicates.PredicateTemplate import PredicateTemplate
from src.social_exchange.ExchangeEffects import ExchangeEffects
from src.social_exchange.SocialExchange import SocialExchange
from src.types.NPCTypes import NPCType

# todo make predicate template
@dataclass
class SocialExchangeTemplate:
    name: str
    preconditions: Sequence[ICondition]
    intent: PredicateTemplate
    initiator_irs: InfluenceRuleSet
    responder_irs: InfluenceRuleSet
    effects: ExchangeEffects

    def instantiate(self, initiator: NPCType, responder: NPCType) -> SocialExchange:
        intent = self.intent.instantiate(subject=initiator, target=responder)

        return SocialExchange(
            name=self.name,
            initiator=initiator,
            responder=responder,
            intent=intent,
            preconditions=self.preconditions,
            initiator_irs=self.initiator_irs,
            responder_irs=self.responder_irs,
            effects=self.effects,
        )