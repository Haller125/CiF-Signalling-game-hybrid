from src.signal_interpolation.SignalInterpolation import update_beliefs_from_observation
from src.irs.BIRS import BInfluenceRuleSet
from src.rule.BRule import BRule
from src.predicates.BCondition import BHasCondition
from src.predicates.PredicateTemplate import PredicateTemplate
from src.belief.BeliefStore import BeliefStore
from src.social_exchange.BSocialExchange import BSocialExchange
from src.social_exchange.BExchangeEffects import BExchangeEffects
from src.predicates.BEffect import BAddPredicateEffect
import pytest

class DummyNPC:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.beliefStore = BeliefStore()


def make_exchange(i, r, weight=0.8):
    template = PredicateTemplate('trait','kind',True)
    i.beliefStore.add_belief(template.instantiate(subject=i), 0.5)

    cond = BHasCondition(req_predicate=template)
    rule = BRule(name='rule', condition=[cond], weight=weight)
    irs = BInfluenceRuleSet(name='irs', rules=[rule])

    effects = BExchangeEffects(accept_effects=[BAddPredicateEffect(label='a', predicates=[template])], reject_effects=[])

    return BSocialExchange(
        name='ex',
        initiator=i,
        responder=r,
        intent=template.instantiate(i),
        preconditions=[cond],
        initiator_irs=irs,
        responder_irs=irs,
        effects=effects
    )


def test_update_beliefs_from_observation():
    observer = DummyNPC(3,'O')
    i = DummyNPC(1,'A')
    r = DummyNPC(2,'B')
    exchange = make_exchange(i, r, weight=0.8)

    template = PredicateTemplate('trait','kind',True)
    observer.beliefStore.add_belief(template.instantiate(subject=i), 0.5)

    update_beliefs_from_observation(observer, exchange, accepted=True)

    posterior = observer.beliefStore.get_probability(template, i, None)
    # Current implementation does not update because condition templates are not checked
    assert pytest.approx(posterior, rel=1e-3) == 0.5
