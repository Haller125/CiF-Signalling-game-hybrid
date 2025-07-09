from dataclasses import dataclass
from typing import List, Sequence

from src.predicates.Predicate import Predicate


@dataclass(slots=True)
class WorldState(Sequence[Predicate]):
    predicates: List[Predicate]

    def __getitem__(self, idx: int):
        return self.predicates[idx]

    def __len__(self) -> int:
        return len(self.predicates)

    def add(self, predicate: Predicate) -> None:
        if predicate not in self.predicates:
            self.predicates.append(predicate)

    def remove(self, predicate: Predicate) -> None:
        if predicate in self.predicates:
            self.predicates.remove(predicate)
