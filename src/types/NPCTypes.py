import typing


class NPCType(typing.Protocol):
    id: int
    name: str
