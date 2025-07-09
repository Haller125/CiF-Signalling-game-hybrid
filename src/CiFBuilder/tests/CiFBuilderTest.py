import unittest
from src.CiFBuilder.CiFBuilder import CiFBuilder
from src.irs.IRS import InfluenceRuleSet
from src.predicates.Condition import HasCondition
from src.predicates.Effect import AddPredicateEffect, RemovePredicateEffect
from src.predicates.Predicate import Predicate
from src.predicates.PredicateTemplate import PredicateTemplate
from src.predicates.WorldState import WorldState
from src.rule.Rule import Rule
from src.social_exchange.ExchangeEffects import ExchangeEffects
from src.social_exchange.SocialExchangeTemplate import SocialExchangeTemplate


class TestCiFBuilder(unittest.TestCase):
    def setUp(self):
        self.traits = [("kind", 0.8), ("evil", 0.2)]
        self.relationships = [("friendship", 0.5), ("rivalry", 0.3)]

        intent_pred = PredicateTemplate("relationship", "dating", is_single=False)

        preconds = [

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
                     HasCondition([PredicateTemplate("trait", "shy", is_single=True)]),
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
        self.exchanges = [SocialExchangeTemplate("test", preconds, intent_pred, initiator_irs=init_irs, responder_irs=resp_irs, effects=ExchangeEffects(accept_effects=[accept1, accept2], reject_effects=[reject_effect]))]
        self.builder = CiFBuilder(traits=self.traits, relationships=self.relationships, exchanges=self.exchanges)

    def test_initialization(self):
        self.assertEqual(self.builder.traits, self.traits)
        self.assertEqual(self.builder.relationships, self.relationships)
        self.assertEqual(self.builder.exchanges, self.exchanges)
        self.assertEqual(len(self.builder.names), 10)
        self.assertEqual(self.builder.n, 10)

    def test_build(self):
        cif = self.builder.build()
        self.assertEqual(len(cif.NPCs), 10)
        self.assertEqual(cif.actions, self.exchanges)
        self.assertIsInstance(cif.state, WorldState)

    def test_create_world_state(self):
        npcs = self.builder.build().NPCs
        world_state = self.builder.create_world_state(npcs)
        self.assertIsInstance(world_state, WorldState)
        self.assertGreaterEqual(len(world_state.predicates), 0)

        # Check that predicates match traits and relationships
        for predicate in world_state.predicates:
            self.assertIsInstance(predicate, Predicate)
            if predicate.pred_type == "trait":
                self.assertIn(predicate.subtype, [trait[0] for trait in self.traits])
            elif predicate.pred_type == "relationship":
                self.assertIn(predicate.subtype, [relationship[0] for relationship in self.relationships])


if __name__ == '__main__':
    unittest.main()
