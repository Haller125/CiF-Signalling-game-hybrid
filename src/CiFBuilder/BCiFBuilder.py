from dataclasses import dataclass, field
from random import random
from typing import List

from src.CiF.BCiF import BCiF
from src.names.names import Names
from src.npc.BNPC import BNPC
from src.social_exchange.BSocialExchangeTemplate import BSocialExchangeTemplate


@dataclass
class CiFBuilder:
    traits: List[tuple[str, float]]
    relationships: List[tuple[str, float]]
    exchanges: List[BSocialExchangeTemplate]
    names: List[str] = field(default_factory=lambda: Names().get_n_name(10))
    n: int = 10

    def build(self):
        npcs = [BNPC(i, self.names[i]) for i in range(self.n)]
        npcs = self.initialize_beliefs(npcs)

        return BCiF(
            NPCs=npcs,
            actions=self.exchanges
        )

    def initialize_beliefs(self, npcs):
        for npc in npcs:
            self.initialize_belief(npc)

        return npcs

    def initialize_belief(self, npc):
        for trait, probability in self.traits:
            if random() <= probability:
                npc.beliefs.add_trait(trait)
        for relationship, probability in self.relationships:
            if random() <= probability:
                npc.beliefs.add_relationship(relationship)

        return npc
