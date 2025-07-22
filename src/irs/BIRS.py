from dataclasses import dataclass, field
from typing import List, Dict

from src.belief.BeliefStore import BeliefStore
from src.predicates.WorldState import WorldState
from src.rule.BRule import BRule
from src.rule.Rule import Rule
from src.types.NPCTypes import NPCType


@dataclass(slots=True)
class BInfluenceRuleSet:
    name: str
    rules: List[BRule] = field(default_factory=list)

    def add(self, *new_rules: BRule) -> None:
        self.rules.extend(new_rules)

    def score(self, state: BeliefStore, i: NPCType, r: NPCType = None) -> float:
        return sum(rule.get_weight(state, i, r) for rule in self._true_rules(state, i, r)
                   if rule.weight is not None and isinstance(rule, BRule))

    def accept_or_reject(self, state: BeliefStore, i: NPCType, r: NPCType = None,
                         threshold: float = 0.0) -> bool:
        return self.score(state, i, r) >= threshold

    def _true_rules(self, state: BeliefStore, i: NPCType, r: NPCType = None) -> List[BRule]:
        return [rule for rule in self.rules if isinstance(rule, BRule) and rule.is_true(state, i, r)]
