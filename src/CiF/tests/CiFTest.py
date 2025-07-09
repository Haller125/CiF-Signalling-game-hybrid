import unittest

from src.CiFBuilder.CiFBuilder import CiFBuilder
from src.irs.IRS import InfluenceRuleSet
from src.predicates.Condition import HasCondition
from src.predicates.Effect import AddPredicateEffect, RemovePredicateEffect
from src.predicates.PredicateTemplate import PredicateTemplate
from src.predicates.WorldState import WorldState
from src.rule.Rule import Rule
from src.social_exchange.ExchangeEffects import ExchangeEffects
from src.social_exchange.SocialExchange import SocialExchange
from src.social_exchange.SocialExchangeTemplate import SocialExchangeTemplate


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.traits = [("kind", 0.8), ("evil", 0.2)]
        self.relationships = [("friendship", 0.5), ("rivalry", 0.3)]

        intent_pred = PredicateTemplate("relationship", "dating", is_single=False)

        preconds = [
            HasCondition([PredicateTemplate("relationship", "friendship", is_single=False)]),
        ]

        init_irs = InfluenceRuleSet("AskOnDate_i")
        init_irs.add(
            Rule("has_crush",
                 [
                     HasCondition([PredicateTemplate("relationship", "crush", is_single=False)]),
                 ],
                 +5),
            Rule("is_shy",
                 [
                     HasCondition([PredicateTemplate("trait", "shy", is_single=True)]),
                 ],
                 -4),
        )

        resp_irs = InfluenceRuleSet("AskOnDate_r")
        resp_irs.add(
            Rule("initiator_popular",
                 [
                     HasCondition([PredicateTemplate("relationship", "popular", is_single=False)]),
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
        self.exchanges = [
            SocialExchangeTemplate("test", preconds, intent_pred, initiator_irs=init_irs, responder_irs=resp_irs,
                                   effects=ExchangeEffects(accept_effects=[accept1, accept2],
                                                           reject_effects=[reject_effect]))]
        self.builder = CiFBuilder(traits=self.traits, relationships=self.relationships, exchanges=self.exchanges)
        self.cif = self.builder.build()

    def test_initialization(self):
        self.assertEqual(len(self.cif.NPCs), 10)
        self.assertEqual(self.cif.actions, self.exchanges)
        self.assertIsInstance(self.cif.state, WorldState)

    def test_iteration(self):
        initial_state = self.cif.state.predicates.copy()
        self.cif.iteration()
        self.assertNotEqual(self.cif.state.predicates, initial_state)  # Ensure state changes after iteration

    def test_desire_formation(self):
        for npc in self.cif.NPCs:
            volitions = self.cif.desire_formation(npc, self.cif.NPCs, self.cif.state, self.cif.actions)
            self.assertIsInstance(volitions, list)

    def test_select_intent(self):
        for npc in self.cif.NPCs:
            volitions = self.cif.desire_formation(npc, self.cif.NPCs, self.cif.state, self.cif.actions)
            action = self.cif.select_intent(volitions, 0)
            if action is not None:
                self.assertIsInstance(action, SocialExchange)


if __name__ == '__main__':
    unittest.main()
