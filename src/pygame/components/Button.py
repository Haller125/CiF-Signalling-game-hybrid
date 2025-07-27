import logging
from dataclasses import dataclass, field
from typing import Tuple, Optional, Callable

import pygame

from src.pygame.components.IComponent import IComponent


@dataclass
class Button(IComponent):
    x: int
    y: int
    width: int
    height: int
    text: str
    font_size: int = 20
    bg_color: Tuple[int, int, int] = (70, 70, 70)
    hover_color: Tuple[int, int, int] = (100, 100, 100)
    pressed_color: Tuple[int, int, int] = (150, 150, 150)
    text_color: Tuple[int, int, int] = (255, 255, 255)
    on_click: Optional[Callable[[], None]] = field(default=None, repr=False)

    font: pygame.font.Font = field(init=False)
    is_hovered: bool = field(init=False, default=False)
    is_pressed: bool = field(init=False, default=False)
    click_anim: bool = field(init=False, default=False)
    anim_timer: int = field(init=False, default=0)

    disabled: bool = field(init=False, default=False)

    def __post_init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont(None, self.font_size)

    def handle_event(self, event):
        if self.disabled:
            return
        mx, my = pygame.mouse.get_pos()
        within = self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = within
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and within:
            self.is_pressed = True
            self.click_anim = True
            self.anim_timer = 5
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and within:
                if self.on_click is not None:
                    try:
                        self.on_click()
                    except Exception as exc:
                        logging.error(f"Button on_click error: {exc}")
            self.is_pressed = False

    def draw(self, surface):
        color = self.bg_color
        if self.click_anim:
            color = self.pressed_color
            self.anim_timer -= 1
            if self.anim_timer <= 0:
                self.click_anim = False
        elif self.is_pressed:
            color = self.pressed_color
        elif self.is_hovered:
            color = self.hover_color
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, color, rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)
