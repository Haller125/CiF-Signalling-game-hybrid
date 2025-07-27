from dataclasses import dataclass
from typing import Sequence

from src.irs.BIRS import BInfluenceRuleSet
from src.predicates.BCondition import IBCondition, BHasCondition
from src.predicates.PredicateTemplate import PredicateTemplate
from src.rule.BRule import BRule
from src.social_exchange.BExchangeEffects import BExchangeEffects
from src.social_exchange.BSocialExchange import BSocialExchange
from src.types.NPCTypes import BNPCType


@dataclass
class BSocialExchangeTemplate:
    name: str
    preconditions: Sequence[IBCondition]
    intent: PredicateTemplate
    initiator_irs: BInfluenceRuleSet
    responder_irs: BInfluenceRuleSet
    effects: BExchangeEffects
    text: str = ""   # text that will be used to describe the exchange in the UI (npc i {text} npc r)

    def instantiate(self, initiator: BNPCType, responder: BNPCType) -> BSocialExchange:
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
            text=self.text
        )

def make_template():
    tmpl = PredicateTemplate('relationship', 'ally', False)
    rule = BRule(name='r', condition=[DummyCondition(1.0)], weight=1.0)
    irs = BInfluenceRuleSet(name='irs', rules=[rule])
    effects = BExchangeEffects([], [])
    return BSocialExchangeTemplate(
        name='ally_request',
        preconditions=[lambda *a, **k: True],
        intent=tmpl,
        initiator_irs=irs,
        responder_irs=irs,
        effects=effects
    )

class DummyCondition(BHasCondition):
    def __init__(self, value: float = 1.0):
        super().__init__(req_predicate=PredicateTemplate('trait','dummy',True))
        self.value = value

    def __call__(self, *args, **kwargs) -> float:
        return self.value
