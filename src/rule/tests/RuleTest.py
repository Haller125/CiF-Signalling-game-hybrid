import unittest
from typing import List

from src.npc.NPC import NPC
from src.predicates.Condition import Condition
from src.predicates.Effect import Effect
from src.predicates.Predicate import Predicate
from src.predicates.WorldState import WorldState
from src.rule.Rule import Rule


def make_sample_rules(i: NPC, r: NPC) -> List[Rule]:
    friend_pred = Predicate("relationship", "friends", i, r, 1)
    enemy_pred = Predicate("relationship", "enemy", i, r, 1)

    return [

        # Influence rule (weight only)
        Rule(
            name="friends_check",
            condition=[Condition(lambda s: friend_pred in s)],
            weight=2.0
        ),

        # Effect rule (state change only)
        Rule(
            name="enemy_status_with_effect",
            condition=[Condition(lambda s: enemy_pred in s)],
            effects=[Effect(lambda s: s.append(
                Predicate("status", "don't help", r, target=i, value=1)
            ))]
        ),

        Rule(
            name="Double_predicate_rule",
            condition=[Condition(lambda s: friend_pred in s and enemy_pred in s)],
            weight=1.0,
            effects=[Effect(lambda s: s.append(
                    Predicate("status", "conflicting_relationship", r, target=i, value=1)
                ))]
        )
    ]

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.alice = NPC(1, "Alice")
        self.bob = NPC(2, "Bob")

        self.rules = make_sample_rules(self.alice, self.bob)

    def test_something(self):
        rules = self.rules

        self.assertEqual(len(rules), 3)
        self.assertEqual(rules[0].name, "friends_check")
        self.assertEqual(rules[1].name, "enemy_status_with_effect")
        self.assertEqual(rules[2].name, "Double_predicate_rule")

        initial_state = WorldState([Predicate("relationship", "friends", self.alice, self.bob, 1)])
        self.assertTrue(rules[0].is_true(initial_state))
        self.assertFalse(rules[1].is_true(initial_state))
        self.assertFalse(rules[2].is_true(initial_state))

if __name__ == '__main__':
    unittest.main()
