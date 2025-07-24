from dataclasses import dataclass, field
from typing import List, Tuple

import pygame

from src.pygame.components.IComponent import IComponent


@dataclass
class TabWindow(IComponent):
    x: int
    y: int
    width: int
    height: int
    tabs: List[str]
    header_height: int = 30
    bg_color: Tuple[int, int, int] = (40, 40, 40)
    tab_color: Tuple[int, int, int] = (60, 60, 60)
    selected_tab_color: Tuple[int, int, int] = (80, 80, 120)
    text_color: Tuple[int, int, int] = (255, 255, 255)
    font: pygame.font.Font = field(init=False)
    selected_index: int = field(init=False, default=0)

    def __post_init__(self):
        pygame.font.init()
        font_size = max(14, self.header_height - 10)
        self.font = pygame.font.SysFont(None, font_size)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if self.y <= my <= self.y + self.header_height and self.x <= mx <= self.x + self.width:
                tab_w = self.width / len(self.tabs)
                idx = int((mx - self.x) // tab_w)
                if 0 <= idx < len(self.tabs): self.selected_index = idx

    def draw(self, surface):
        # draw background
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.bg_color, rect)
        # draw headers
        tab_w = self.width / len(self.tabs)
        for i, tab in enumerate(self.tabs):
            hdr_rect = pygame.Rect(self.x + i * tab_w, self.y, tab_w, self.header_height)
            clr = self.selected_tab_color if i == self.selected_index else self.tab_color
            pygame.draw.rect(surface, clr, hdr_rect)
            txt = self.font.render(tab, True, self.text_color)
            tr = txt.get_rect(center=hdr_rect.center)
            surface.blit(txt, tr)
        # draw content placeholder below
        content_rect = pygame.Rect(self.x, self.y + self.header_height,
                                   self.width, self.height - self.header_height)
        pygame.draw.rect(surface, self.bg_color, content_rect)
        # TODO: draw content for selected tab
