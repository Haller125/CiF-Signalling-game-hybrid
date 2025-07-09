import unittest

from src.irs.IRS import InfluenceRuleSet
from src.npc.NPC import NPC
from src.predicates.Condition import HasCondition
from src.predicates.Effect import AddPredicateEffect, RemovePredicateEffect
from src.predicates.Predicate import Predicate
from src.predicates.PredicateTemplate import PredicateTemplate
from src.predicates.WorldState import WorldState
from src.rule.Rule import Rule
from src.social_exchange.ExchangeEffects import ExchangeEffects
from src.social_exchange.SocialExchange import SocialExchange


def make_ask_on_date(i: NPC, r: NPC) -> SocialExchange:
    intent_pred = Predicate("relationship", "dating", i, r, 1)

    preconds = [
        HasCondition([PredicateTemplate("status", "crush", is_single=False)]),
    ]

    init_irs = InfluenceRuleSet("AskOnDate_i")
    init_irs.add(
        Rule("has_crush",
             [
                 HasCondition([PredicateTemplate("status", "crush", is_single=False)]),
             ],
             +5),
        Rule("is_shy",
             [
                 HasCondition([PredicateTemplate("trait",  "shy", is_single=True)]),
             ],
             -4),
    )

    resp_irs = InfluenceRuleSet("AskOnDate_r")
    resp_irs.add(
        Rule("initiator_popular",
             [
                 HasCondition([PredicateTemplate("status", "popular", is_single=False)]),
             ],
             +4),
        Rule("already_dating",
             [
                 HasCondition([PredicateTemplate("relationship", "dating", is_single=False)]),
             ],
             -5),
    )

    accept1 = AddPredicateEffect(
        "accepted1",
        [PredicateTemplate("relationship", "dating", is_single=False)],
    )
    accept2 = RemovePredicateEffect(
        "accepted2",
        [PredicateTemplate("status", "crush", is_single=False)],
    )

    reject_effect = AddPredicateEffect(
        "rejected",
        [PredicateTemplate("status", "embarrassed", is_single=True)],
    )

    return SocialExchange(
        name="AskOnDate",
        initiator=i,
        responder=r,
        intent=intent_pred,
        preconditions=preconds,
        initiator_irs=init_irs,
        responder_irs=resp_irs,
        effects=ExchangeEffects(accept_effects=[accept1, accept2], reject_effects=[reject_effect]),
    )


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.alice = NPC(1, "Alice")
        self.bob = NPC(2, "Bob")

        self.exchange = make_ask_on_date(self.alice, self.bob)

    def test_exchange_initialization(self):
        self.assertEqual(self.exchange.name, "AskOnDate")
        self.assertEqual(self.exchange.initiator, self.alice)
        self.assertEqual(self.exchange.responder, self.bob)
        self.assertIsInstance(self.exchange.intent, Predicate)
        self.assertEqual(len(self.exchange.preconditions), 1)
        self.assertIsInstance(self.exchange.initiator_irs, InfluenceRuleSet)
        self.assertIsInstance(self.exchange.responder_irs, InfluenceRuleSet)
        self.assertIsInstance(self.exchange.effects, ExchangeEffects)

    def test_exchange_is_playable(self):
        initial_state = [
            Predicate("status", "crush", self.alice, self.bob, 1),
            Predicate("trait", "shy", self.alice),
        ]

        initial_state = WorldState(initial_state)
        self.assertTrue(self.exchange.is_playable(initial_state))

        initial_state.add(Predicate("relationship", "dating", self.alice, self.bob, 1))
        self.assertLessEqual(0, self.exchange.initiator_score(initial_state))

    def test_initiator_score(self):
        initial_state = WorldState([
            Predicate("status", "crush", self.alice, self.bob, 1),
            Predicate("trait", "shy", self.alice),
        ])

        score = self.exchange.initiator_score(initial_state)
        self.assertGreater(score, 0)

    def test_responder_accepts(self):
        initial_state = WorldState([
            Predicate("status", "crush", self.alice, self.bob, 1),
            Predicate("trait", "shy", self.alice),
        ])

        will_accept = self.exchange.responder_accepts(initial_state)
        self.assertTrue(will_accept)

    def test_perform_accept(self):
        initial_state = WorldState([
            Predicate("status", "crush", self.alice, self.bob, 1),
            Predicate("trait", "shy", self.alice),
        ])

        self.exchange.perform(initial_state)

        self.assertIn(Predicate("relationship", "dating", self.alice, self.bob, 1), initial_state)
        self.assertNotIn(Predicate("status", "crush", self.alice, self.bob, 1), initial_state)

    def test_perform_reject(self):
        initial_state = WorldState([
            Predicate("status", "crush", self.alice, self.bob, 1),
            Predicate("trait", "shy", self.alice),
        ])

        # dummy rule to ensure rejection
        self.exchange.responder_irs.add(
            Rule("reject",
                 [HasCondition([PredicateTemplate('trait', 'shy', is_single=True)])],
                 weight=-10)
        )

        self.exchange.perform(initial_state)

        predicate = Predicate("status", "embarrassed", self.alice, value=1)

        self.assertIn(predicate, initial_state)
        self.assertNotIn(Predicate("relationship", "dating", self.alice, self.bob, 1), initial_state)


if __name__ == '__main__':
    unittest.main()
