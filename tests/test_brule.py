import pytest
from src.rule.BRule import BRule
from src.belief.BeliefStore import BeliefStore
from src.predicates.BCondition import BHasCondition, IBCondition
from src.predicates.PredicateTemplate import PredicateTemplate

class DummyNPC:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class InvalidCondition(IBCondition):
    def __call__(self, state, i, r=None):
        return 1.5  # invalid probability >1


def test_rule_probability_product():
    npc = DummyNPC(1, 'A')
    template = PredicateTemplate('trait', 'kind', True)
    store = BeliefStore()
    store.add_belief(template.instantiate(subject=npc), probability=0.5)

    cond = BHasCondition(req_predicate=template)
    rule = BRule(name='rule', condition=[cond], weight=0.9)

    assert pytest.approx(rule.probability(store, npc)) == 0.5


def test_rule_empty_condition_raises():
    rule = BRule(name='rule', condition=[])
    with pytest.raises(ValueError):
        rule.probability(BeliefStore(), DummyNPC(1,'A'))


def test_invalid_condition_probability_raises():
    npc = DummyNPC(1,'A')
    rule = BRule(name='rule', condition=[InvalidCondition(req_predicate=None)])
    with pytest.raises(ValueError):
        rule.probability(BeliefStore(), npc)
