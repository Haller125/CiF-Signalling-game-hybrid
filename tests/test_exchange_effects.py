import pytest
from src.social_exchange.BExchangeEffects import BExchangeEffects
from src.predicates.BEffect import BAddPredicateEffect, BRemovePredicateEffect
from src.predicates.PredicateTemplate import PredicateTemplate
from src.belief.BeliefStore import BeliefStore

class DummyNPC:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def test_accept_and_reject_effects():
    template = PredicateTemplate('trait','kind',True)
    store = BeliefStore()
    npc = DummyNPC(1,'A')

    add_effect = BAddPredicateEffect(label='add', predicates=[template], probability=0.9)
    remove_effect = BRemovePredicateEffect(label='rem', predicates=[template])
    exch = BExchangeEffects(accept_effects=[add_effect], reject_effects=[remove_effect])

    exch.accept(store, npc, None)
    assert store.get_probability(template, npc, None) == pytest.approx(0.9)

    exch.reject(store, npc, None)
    assert store.get_probability(template, npc, None) == pytest.approx(0.0)
