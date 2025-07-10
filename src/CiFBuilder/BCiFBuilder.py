from dataclasses import dataclass, field
from random import random
from typing import List

from src.names.names import Names
from src.social_exchange.SocialExchangeTemplate import SocialExchangeTemplate


@dataclass
class CiFBuilder:
    traits: List[tuple[str, float]]
    relationships: List[tuple[str, float]]
    exchanges: List[SocialExchangeTemplate]
    names: List[str] = field(default_factory=lambda: Names().get_n_name(10))
    n: int = 10

    def build(self):
        pass

    def initialize_beliefs(self, npcs):
        for npc in npcs:
            for trait, probability in self.traits:
                if random() <= probability:
                    npc.beliefs.add_trait(trait)
            for relationship, probability in self.relationships:
                if random() <= probability:
                    npc.beliefs.add_relationship(relationship)

        return npcs
