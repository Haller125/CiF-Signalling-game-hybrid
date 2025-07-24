from dataclasses import dataclass
from typing import List

from src.CiF.BCiF import BCiF
from src.pygame import MainWindow
from src.pygame.components.Column import Column
from src.pygame.components.TopBar import TopBar


@dataclass
class Game:
    model: BCiF
    npcs: List = None
    actions: List = None

    def __post_init__(self):
        self.npcs = self.model.NPCs
        self.actions = self.model.actions

        self.window = MainWindow.GameWindow()
        topbar = TopBar(width=self.window.width, height=self.window.height // 5)
        self.window.add_object(topbar)

        # Left column
        content_y = topbar.height
        content_h = self.window.height - topbar.height
        column = Column(
            x=0,
            y=content_y,
            width=self.window.width // 4,
            height=content_h,
            items=self.npcs,
        )
        self.window.add_object(column)


