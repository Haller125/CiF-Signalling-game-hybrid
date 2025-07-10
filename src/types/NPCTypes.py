import typing

from src.belief.BeliefStore import BeliefStore


class NPCType(typing.Protocol):
    id: int
    name: str

class BNPCType(typing.Protocol):
    id: int
    name: str
    beliefStore: BeliefStore
