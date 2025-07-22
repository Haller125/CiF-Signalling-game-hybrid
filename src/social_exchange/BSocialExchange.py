from dataclasses import dataclass
from typing import Sequence

from src.belief.BeliefStore import BeliefStore
from src.irs.BIRS import BInfluenceRuleSet
from src.irs.IRS import InfluenceRuleSet
from src.predicates.BCondition import IBCondition
from src.predicates.Condition import ICondition
from src.predicates.Predicate import Predicate
from src.predicates.WorldState import WorldState
from src.social_exchange.BExchangeEffects import BExchangeEffects
from src.social_exchange.ExchangeEffects import ExchangeEffects
from src.types.NPCTypes import NPCType

@dataclass(slots=True)
class BSocialExchange:
    name: str
    initiator: NPCType
    responder: NPCType
    intent: Predicate
    preconditions: Sequence[IBCondition]
    initiator_irs: BInfluenceRuleSet
    responder_irs: BInfluenceRuleSet
    effects: BExchangeEffects

    def is_playable(self, state: BeliefStore) -> bool:
        return all(cond(state, self.initiator, self.responder) for cond in self.preconditions)

    def initiator_score(self, state: BeliefStore) -> float:
        return self.initiator_irs.score(state, self.initiator, self.responder)

    def responder_accepts(self, state: BeliefStore, threshold: float = 0.0) -> bool:
        return self.responder_irs.accept_or_reject(state, self.initiator, self.responder, threshold)

    def perform(self, state: BeliefStore) -> None:
        if not self.is_playable(state):
            raise ValueError(f"Exchange '{self.name}' is not playable in the current state.")

        if self.responder_accepts(state):
            self.effects.accept(state, self.initiator, self.responder)
        else:
            self.effects.reject(state, self.initiator, self.responder)
