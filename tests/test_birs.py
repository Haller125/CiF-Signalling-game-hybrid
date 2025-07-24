import math
from src.irs.BIRS import BInfluenceRuleSet
from src.rule.BRule import BRule
from src.belief.BeliefStore import BeliefStore
from src.predicates.BCondition import BHasCondition
from src.predicates.PredicateTemplate import PredicateTemplate

class DummyNPC:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def test_expected_value_and_acceptance():
    npc = DummyNPC(1,'A')
    template = PredicateTemplate('trait','kind',True)
    store = BeliefStore()
    store.add_belief(template.instantiate(subject=npc), 0.6)

    cond = BHasCondition(req_predicate=template)
    rule = BRule(name='rule', condition=[cond], weight=0.5)

    irs = BInfluenceRuleSet(name='irs', rules=[rule])

    expected = 0.5 * 0.5
    assert irs.expected_value(store, npc, npc) == expected

    prob = 1.0 / (1.0 + math.exp(-expected))
    assert irs.acceptance_probability(store, npc, npc) == prob
