from typing import Optional, List

import pygame
from dataclasses import dataclass, field

from src.pygame.components.Column import Column
from src.pygame.components.IComponent import IComponent
from src.pygame.components.TabWindow import TabWindow
from src.pygame.components.TopBar import TopBar


@dataclass
class GameWindow:
    width: int = 800
    height: int = 600
    title: str = "PyGame Window"
    background_color: tuple = field(default_factory=lambda: (0, 0, 0))
    fps: int = 60
    objects: List[IComponent] = field(default_factory=list)

    # Runtime attributes initialized later
    screen: pygame.Surface = field(init=False)
    clock: pygame.time.Clock = field(init=False)
    running: bool = field(init=False, default=False)

    def __post_init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            for obj in self.objects:
                obj.handle_event(event)

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.background_color)
        for obj in self.objects:
            obj.draw(self.screen)

        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        pygame.quit()

    def add_object(self, obj: IComponent):
        self.objects.append(obj)


if __name__ == "__main__":
    window = GameWindow()

    topbar = TopBar(width=window.width, height=window.height // 5)

    items = [f"Item {i + 1}" for i in range(20)]
    content_y = topbar.height
    content_h = window.height - topbar.height
    column = Column(
        x=0,
        y=content_y,
        width=window.width // 4,
        height=content_h,
        items=items,
    )

    items1 = [f"Item {i + 1}" for i in range(20)]
    content_y = topbar.height
    content_h = window.height - topbar.height
    column1 = Column(
        x=window.width - window.width // 4,
        y=content_y,
        width=window.width // 4,
        height=content_h,
        items=items1,
    )

    mid = TabWindow(x=window.width // 4, y=content_y,
                    width=window.width // 2, height=content_h,
                    tabs=['Tab1', 'Tab2', 'Tab3'])

    window.add_object(topbar)
    window.add_object(column)
    window.add_object(column1)
    window.add_object(mid)

    window.run()
