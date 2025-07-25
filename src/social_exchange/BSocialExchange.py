from dataclasses import dataclass
from typing import Sequence

from src.belief.BeliefStore import BeliefStore
from src.irs.BIRS import BInfluenceRuleSet
from src.predicates.BCondition import IBCondition
from src.predicates.Predicate import Predicate
from src.social_exchange.BExchangeEffects import BExchangeEffects
from src.types.NPCTypes import BNPCType


@dataclass(slots=True)
class BSocialExchange:
    name: str
    initiator: BNPCType
    responder: BNPCType
    intent: Predicate
    preconditions: Sequence[IBCondition]
    initiator_irs: BInfluenceRuleSet
    responder_irs: BInfluenceRuleSet
    effects: BExchangeEffects
    text: str   # text that will be used to describe the exchange in the UI (npc i {text} npc r)
    is_accepted: bool = None

    def is_playable(self, state: BeliefStore) -> bool:
        return all(cond(state, self.initiator, self.responder) for cond in self.preconditions)

    def initiator_score(self, state: BeliefStore) -> float:
        return self.initiator_irs.expected_value(state, self.initiator, self.responder)

    def initiator_probability(self, state: BeliefStore) -> float:
        return self.initiator_irs.acceptance_probability(state, self.initiator, self.responder)

    def responder_probability(self, state: BeliefStore) -> float:
        return self.responder_irs.acceptance_probability(state, self.responder, self.initiator)

    def responder_accepts(self, state: BeliefStore, threshold: float = 0.0) -> bool:
        return self.responder_irs.acceptance_probability(state, self.responder, self.initiator, threshold) > 0.5

    def perform(self, state: BeliefStore) -> None:
        if not self.is_playable(state):
            raise ValueError(f"Exchange '{self.name}' is not playable in the current state.")

        if self.responder_accepts(state):
            self.effects.accept(state, self.initiator, self.responder)
            self.is_accepted = True
        else:
            self.effects.reject(state, self.initiator, self.responder)
            self.is_accepted = False
