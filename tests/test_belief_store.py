import pytest
from src.belief.BeliefStore import BeliefStore
from src.predicates.PredicateTemplate import PredicateTemplate

class DummyNPC:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def test_add_and_get_probability():
    npc = DummyNPC(1, 'A')
    template = PredicateTemplate(pred_type='trait', subtype='kind', is_single=True)
    store = BeliefStore()

    store.add_belief(template.instantiate(subject=npc), probability=0.8)

    assert pytest.approx(store.get_probability(template, npc, None)) == 0.8

    # updating existing predicate
    store.update(template.instantiate(subject=npc), 0.3)
    assert pytest.approx(store.get_probability(template, npc, None)) == 0.3
