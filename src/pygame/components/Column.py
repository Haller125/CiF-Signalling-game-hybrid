from dataclasses import dataclass, field
from typing import List, Tuple, Optional

import pygame

from src.pygame.components.IComponent import IComponent


@dataclass
class Column(IComponent):
    x: int
    y: int
    width: int
    height: int
    items: List[str]
    bg_color: Tuple[int, int, int] = (30, 30, 30)
    text_color: Tuple[int, int, int] = (255, 255, 255)
    selected_color: Tuple[int, int, int] = (70, 70, 120)
    padding: int = 5
    line_height: int = 20

    font: pygame.font.Font = field(init=False)
    scroll_offset: int = field(init=False, default=0)
    max_scroll: int = field(init=False, default=0)
    selected_index: Optional[int] = field(init=False, default=None)


    def __post_init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont(None, self.line_height)
        total_height = len(self.items) * (self.line_height + self.padding)
        self.max_scroll = max(0, total_height - self.height)

    def handle_event(self, event: pygame.event.Event):
        mx, my = pygame.mouse.get_pos()
        in_column = self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (4, 5) and in_column:
                # Scroll when mouse over column
                if event.button == 4:
                    self.scroll_offset = max(0, self.scroll_offset - (self.line_height + self.padding))
                else:
                    self.scroll_offset = min(self.max_scroll, self.scroll_offset + (self.line_height + self.padding))
            elif event.button == 1 and in_column:
                # Click: calculate index
                relative_y = my - self.y + self.scroll_offset - self.padding
                idx = relative_y // (self.line_height + self.padding)
                if 0 <= idx < len(self.items):
                    # Toggle selection
                    if self.selected_index == idx:
                        self.selected_index = None
                    else:
                        self.selected_index = idx

    def draw(self, surface: pygame.Surface):
        # Draw background
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.bg_color, rect)
        # Clip drawing
        surface.set_clip(rect)
        # Draw items with individual boxes
        y_offset = self.y - self.scroll_offset + self.padding
        for i, item in enumerate(self.items):
            item_rect = pygame.Rect(self.x + self.padding, y_offset,
                                    self.width - 2*self.padding, self.line_height)
            color = self.selected_color if i == self.selected_index else self.bg_color
            pygame.draw.rect(surface, color, item_rect)
            text_surf = self.font.render(item, True, self.text_color)
            surface.blit(text_surf, (item_rect.x + 5, item_rect.y))
            y_offset += self.line_height + self.padding
        # Reset clip
        surface.set_clip(None)