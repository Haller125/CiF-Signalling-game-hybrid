import itertools
from dataclasses import dataclass, field
from random import random
from typing import List

from src.CiF.BCiF import BCiF
from src.names.names import Names
from src.npc.BNPC import BNPC
from src.predicates.PredicateTemplate import PredicateTemplate
from src.social_exchange.BSocialExchangeTemplate import BSocialExchangeTemplate
from src.types.NPCTypes import BNPCType


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
            actions=self.exchanges,
            traits=[trait for trait, _ in self.traits],
            relationships=[relationship for relationship, _ in self.relationships],
        )

    def initialize_beliefs(self, npcs: List[BNPCType]):
        for npc in npcs:
            self.initialize_traits(npc)

        for npc1, npc2 in itertools.permutations(npcs, 2):
            self.initialize_relationship(npc1, npc2)

        return npcs

    def get_trait_templates(self):
        templates: List[tuple[PredicateTemplate, float]] = []

        for trait, probability in self.traits:
            template = PredicateTemplate(pred_type="trait", subtype=trait, is_single=True)
            templates.append((template, probability))

        return templates

    def get_relationship_templates(self):
        templates: List[tuple[PredicateTemplate, float]] = []

        for relationship, probability in self.relationships:
            template = PredicateTemplate(pred_type="relationship", subtype=relationship, is_single=False)
            templates.append((template, probability))

        return templates

    def initialize_traits(self, npc: BNPCType):
        for trait, probability in self.get_trait_templates():
            if random() <= probability:
                npc.beliefStore.add_belief(trait.instantiate(subject=npc))

        return npc

    def initialize_relationship(self, npc1: BNPCType, npc2: BNPCType):
        for relationship, probability in self.get_relationship_templates():
            if random() <= probability:
                npc1.beliefStore.add_belief(relationship.instantiate(subject=npc1, target=npc2))

