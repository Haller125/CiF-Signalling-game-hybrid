import math
import pytest
from src.social_exchange.BSocialExchange import BSocialExchange
from src.social_exchange.BExchangeEffects import BExchangeEffects
from src.predicates.BEffect import BAddPredicateEffect, BRemovePredicateEffect
from src.predicates.BCondition import BHasCondition
from src.predicates.PredicateTemplate import PredicateTemplate
from src.belief.BeliefStore import BeliefStore
from src.irs.BIRS import BInfluenceRuleSet
from src.rule.BRule import BRule

class DummyNPC:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.beliefStore = BeliefStore()


def make_exchange(i, r, prob=1.0, weight=1.0):
    template = PredicateTemplate('trait','kind',True)
    i.beliefStore.add_belief(template.instantiate(subject=i), prob)
    r.beliefStore.add_belief(template.instantiate(subject=r), prob)

    cond = BHasCondition(req_predicate=template)
    rule = BRule(name='rule', condition=[cond], weight=weight)
    irs = BInfluenceRuleSet(name='irs', rules=[rule])

    effects = BExchangeEffects(
        accept_effects=[BAddPredicateEffect(label='a', predicates=[template])],
        reject_effects=[BRemovePredicateEffect(label='r', predicates=[template])]
    )

    return BSocialExchange(
        name='test',
        initiator=i,
        responder=r,
        intent=template.instantiate(i),
        preconditions=[cond],
        initiator_irs=irs,
        responder_irs=irs,
        effects=effects
    )


def test_perform_accept():
    i = DummyNPC(1,'A')
    r = DummyNPC(2,'B')
    exch = make_exchange(i, r, prob=1.0, weight=5.0)

    assert exch.is_playable(i.beliefStore)
    exch.perform(i.beliefStore)

    assert exch.is_accepted is True
    # effect added to initiator store by BAddPredicateEffect default prob=0.9
    template = PredicateTemplate('trait','kind',True)
    assert i.beliefStore.get_probability(template, i, None) == pytest.approx(0.9)


def test_perform_reject():
    i = DummyNPC(1,'A')
    r = DummyNPC(2,'B')
    exch = make_exchange(i, r, prob=0.0, weight=-5.0)

    exch.perform(i.beliefStore)
    assert exch.is_accepted is False
