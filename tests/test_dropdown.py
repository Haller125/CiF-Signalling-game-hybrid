import os
import pygame

from src.pygame.components.Dropdown import Dropdown


def setup_module():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()


def teardown_module():
    pygame.quit()


def test_dropdown_select_and_scroll():
    surface = pygame.Surface((200, 200))
    dd = Dropdown(0, 0, 100, 20, options=[str(i) for i in range(10)], max_visible=3)

    event_open = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(5, 10), button=1)
    dd.handle_event(event_open)
    assert dd.active

    wheel_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(5, 25), button=5)
    dd.handle_event(wheel_event)
    assert dd.scroll_offset > 0

    select_pos = (5, dd.y + dd.height + dd.item_height // 2)
    select_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=select_pos, button=1)
    dd.handle_event(select_event)
    assert dd.selected_index is not None
    assert not dd.active

    dd.draw(surface)
