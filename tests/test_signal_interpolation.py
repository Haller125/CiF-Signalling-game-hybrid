import pytest

from src.npc.BNPC import BNPC
from src.belief.BeliefStore import BeliefStore
from src.predicates.PredicateTemplate import PredicateTemplate
from src.predicates.BCondition import BHasCondition
from src.rule.BRule import BRule
from src.irs.BIRS import BInfluenceRuleSet
from src.social_exchange.BExchangeEffects import BExchangeEffects
from src.social_exchange.BSocialExchange import BSocialExchange
from src.signal_interpolation.SignalInterpolation import update_beliefs_from_observation


def make_exchange(i, r, weight=0.8):
    cond_pred = PredicateTemplate('relationship', 'ally', False)
    condition = BHasCondition(req_predicate=cond_pred)
    rule = BRule(name='rule', condition=[condition], weight=weight)
    irs = BInfluenceRuleSet(name='irs', rules=[rule])
    intent_tpl = PredicateTemplate('action', 'test', False)
    effects = BExchangeEffects([], [])
    exchange = BSocialExchange(
        name='ex',
        initiator=i,
        responder=r,
        intent=intent_tpl.instantiate(i, r),
        preconditions=[lambda *a, **k: True],
        initiator_irs=irs,
        responder_irs=irs,
        effects=effects,
        text='Test exchange',
    )
    return exchange, cond_pred


def test_update_beliefs_from_observation():
    i = BNPC(0, 'I')
    r = BNPC(1, 'R')
    observer = BNPC(2, 'O')
    exchange, cond_pred = make_exchange(i, r, weight=0.8)

    update_beliefs_from_observation(observer, exchange, accepted=True)
    prob = observer.beliefStore.get_probability(cond_pred, i, r)
    assert prob >= 0.5
