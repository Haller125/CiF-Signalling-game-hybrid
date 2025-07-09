from dataclasses import dataclass, field
from typing import List, Dict

from src.predicates.WorldState import WorldState
from src.rule.Rule import Rule
from src.types.NPCTypes import NPCType


@dataclass(slots=True)
class InfluenceRuleSet:
    name: str
    rules: List[Rule] = field(default_factory=list)

    def add(self, *new_rules: Rule) -> None:
        self.rules.extend(new_rules)

    def _true_rules(self, state: WorldState, i: NPCType, r: NPCType = None) -> List[Rule]:
        return [rule for rule in self.rules if rule.is_true(state, i, r)]

    def score(self, state: WorldState, i: NPCType, r: NPCType = None) -> float:
        return sum(rule.get_weight(state, i, r) for rule in self._true_rules(state, i, r)
                   if rule.weight is not None)

    def accept_or_reject(self, state: WorldState, i: NPCType, r: NPCType = None,
                         threshold: float = 0.0) -> bool:
        return self.score(state, i, r) >= threshold
