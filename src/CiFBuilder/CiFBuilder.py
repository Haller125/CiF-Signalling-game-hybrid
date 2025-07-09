from dataclasses import dataclass, field
from random import random
from typing import List
from itertools import combinations

from src.CiF.CiF import CiF
from src.names.names import Names
from src.npc.NPC import NPC
from src.predicates.Predicate import Predicate
from src.predicates.WorldState import WorldState
from src.social_exchange.SocialExchangeTemplate import SocialExchangeTemplate
from src.types.NPCTypes import NPCType


@dataclass
class CiFBuilder:
    traits: List[tuple[str, float]]
    relationships: List[tuple[str, float]]
    exchanges: List[SocialExchangeTemplate]
    names: List[str] = field(default_factory=lambda: Names().get_n_name(10))
    n: int = 10

    def build(self):
        npcs = [NPC(i, self.names[i]) for i in range(self.n)]
        state = self.create_world_state(npcs)

        return CiF(
            NPCs=npcs,
            actions=self.exchanges,
            state=state
        )

    def create_world_state(self, npcs: List[NPCType]):
        predicates = []
        for npc in npcs:
            for trait, probability in self.traits:
                if random() <= probability:
                    predicates.append(Predicate(pred_type='trait', subtype=trait, subject=npc))

        npc_pairs = combinations(npcs, 2)
        for npc1, npc2 in npc_pairs:
            for relationship, probability in self.relationships:
                if random() <= probability:
                    predicates.append(Predicate(pred_type='relationship', subtype=relationship, subject=npc1, target=npc2))

        return WorldState(predicates=predicates)

