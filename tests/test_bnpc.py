from src.npc.BNPC import BNPC
from src.social_exchange.BSocialExchangeTemplate import BSocialExchangeTemplate
from src.social_exchange.BExchangeEffects import BExchangeEffects
from src.predicates.PredicateTemplate import PredicateTemplate
from src.irs.BIRS import BInfluenceRuleSet
from src.rule.BRule import BRule
from src.predicates.BCondition import BHasCondition
from src.predicates.BEffect import BAddPredicateEffect


def make_template():
    template = PredicateTemplate('trait','kind',True)
    cond = BHasCondition(req_predicate=template)
    rule = BRule(name='rule', condition=[cond], weight=1.0)
    irs = BInfluenceRuleSet(name='irs', rules=[rule])
    effects = BExchangeEffects(accept_effects=[BAddPredicateEffect(label='a', predicates=[template])], reject_effects=[])
    return BSocialExchangeTemplate(
        name='greet',
        preconditions=[],
        intent=template,
        initiator_irs=irs,
        responder_irs=irs,
        effects=effects
    )


def test_desire_formation_and_select_intent():
    alice = BNPC(id=1, name='Alice')
    bob = BNPC(id=2, name='Bob')
    tpl = make_template()

    volitions = alice.desire_formation([bob], [tpl])
    assert len(volitions) == 1
    se = alice.select_intent(volitions)
    assert se is not None
    assert se.initiator is alice and se.responder is bob
