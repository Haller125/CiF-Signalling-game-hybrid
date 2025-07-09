from dataclasses import dataclass
from typing import Sequence

from src.irs.IRS import InfluenceRuleSet
from src.predicates.Condition import ICondition
from src.predicates.Predicate import Predicate
from src.predicates.WorldState import WorldState
from src.social_exchange.ExchangeEffects import ExchangeEffects
from src.types.NPCTypes import NPCType


@dataclass(slots=True)
class SocialExchange:
    name: str
    initiator: NPCType
    responder: NPCType
    intent: Predicate
    preconditions: Sequence[ICondition]
    initiator_irs: InfluenceRuleSet
    responder_irs: InfluenceRuleSet
    effects: ExchangeEffects

    def is_playable(self, state: WorldState) -> bool:
        return all(cond(state, self.initiator, self.responder) for cond in self.preconditions)

    def initiator_score(self, state: WorldState) -> float:
        return self.initiator_irs.score(state, self.initiator, self.responder)

    def responder_accepts(self, state: WorldState, threshold: float = 0.0) -> bool:
        return self.responder_irs.accept_or_reject(state, self.initiator, self.responder, threshold)

    def perform(self, state: WorldState) -> None:
        if not self.is_playable(state):
            raise ValueError(f"Exchange '{self.name}' is not playable in the current state.")

        if self.responder_accepts(state):
            self.effects.accept(state, self.initiator, self.responder)
        else:
            self.effects.reject(state, self.initiator, self.responder)
