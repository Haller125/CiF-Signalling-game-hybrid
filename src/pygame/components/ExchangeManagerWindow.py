import logging
from dataclasses import field, dataclass
from typing import Optional, List

import pygame

from src.CiF.BCiF import BCiF
from src.predicates.PredicateTemplate import PredicateTemplate
from src.pygame.components.Dropdown import Dropdown
from src.pygame.components.IComponent import IComponent
from src.pygame.components.Column import Column
from src.pygame.components.Button import Button
from src.pygame.components.InputBox import InputBox
from src.social_exchange.BSocialExchangeTemplate import make_template


@dataclass
class PreconditionRow:
    cond_dropdown: Dropdown
    pred_dropdown: Dropdown
    remove_button: Button


@dataclass
class ExchangeManagerWindow(IComponent):
    x: int
    y: int
    width: int
    height: int
    model: BCiF
    visible: bool = False

    font: pygame.font.Font = field(init=False)
    column: Column = field(init=False)
    add_button: Button = field(init=False)
    edit_button: Button = field(init=False)
    delete_button: Button = field(init=False)
    name_input: InputBox = field(init=False)
    text_input: InputBox = field(init=False)
    confirm_button: Button = field(init=False)
    close_button: Button = field(init=False)
    editing: bool = field(init=False, default=False)
    edit_index: Optional[int] = field(init=False, default=None)
    selected_index: Optional[int] = field(init=False, default=None)
    on_close: Optional[callable] = field(default=None, repr=False)

    def __post_init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 20)
        column_w = self.width // 3
        self.column = Column(self.x, self.y, column_w, self.height,
                             items=[ex.name for ex in self.model.actions])
        btn_w, btn_h = 80, 25
        btn_y = self.y
        top_padding = 10
        self.add_button = Button(self.x + column_w + 10, btn_y + top_padding,
                                 btn_w, btn_h,
                                 "Add", on_click=self.start_add)
        self.edit_button = Button(self.x + column_w + 10, btn_y + btn_h + 5 + top_padding,
                                  btn_w, btn_h,
                                  "Edit", on_click=self.start_edit)
        self.delete_button = Button(self.x + column_w + 10, btn_y + 2 * (btn_h + 5) + top_padding,
                                    btn_w, btn_h,
                                    "Delete", on_click=self.delete_selected)
        input_x = self.x + column_w + 10
        input_w = self.width - column_w - 20

        top_y = self.y + self.height // 2 - 80
        d_btwn = 60
        self.intent_dropdown = Dropdown(
            input_x,
            top_y,
            input_w,
            25,
            options=list(self.model.relationships),
            label="Intent Relationship of Exchange",
        )
        self.refresh_dropdown()
        self.name_input = InputBox(
            input_x,
            top_y + d_btwn,
            input_w,
            25,
            label='Name of Exchange',
        )
        self.text_input = InputBox(
            input_x,
            top_y + d_btwn * 2,
            input_w,
            25,
            label='Text of Exchange (for logging in history tab)',
        )
        self.confirm_button = Button(
            input_x,
            btn_h + 5,
            btn_w,
            btn_h,
            "OK",
            on_click=self.confirm_edit,
        )
        close_x = self.x + self.width - btn_w - 10
        self.close_button = Button(close_x, self.y + 5, btn_w, btn_h,
                                   "Close", on_click=self.close_window)
        if self.model.actions:
            self.selected_index = 0
            tpl = self.model.actions[self.selected_index]
            self.name_input.text = tpl.name
            self.text_input.text = tpl.text
            try:
                self.intent_dropdown.selected_index = self.model.relationships.index(
                    tpl.intent.subtype
                )
            except ValueError:
                self.intent_dropdown.selected_index = None
        elif self.model.relationships:
            self.intent_dropdown.selected_index = 0

    def start_add(self):
        self.editing = True
        self.edit_index = None
        self.name_input.text = ""
        self.text_input.text = ""
        self.selected_index = None

        if self.model.relationships:
            self.intent_dropdown.selected_index = 0
        else:
            self.intent_dropdown.selected_index = None

    def refresh_dropdown(self):
        self.intent_dropdown.options = list(self.model.relationships)
        self.intent_dropdown.scroll_offset = 0
        self.intent_dropdown.selected_index = None if self.intent_dropdown.options is None else (self.intent_dropdown.selected_index or 0)

    def close_window(self):
        self.editing = False
        self.edit_index = None
        self.column.selected_index = None
        self.selected_index = None
        self.name_input.text = ""
        self.text_input.text = ""
        self.intent_dropdown.selected_index = None
        if self.on_close:
            self.on_close()

    def start_edit(self):
        idx = self.column.get_selected_index()
        if idx is None:
            return
        self.editing = True
        self.edit_index = idx
        tpl = self.model.actions[idx]
        self.name_input.text = tpl.name
        self.text_input.text = tpl.text
        try:
            self.intent_dropdown.selected_index = self.model.relationships.index(
                tpl.intent.subtype
            )
        except ValueError:
            self.intent_dropdown.selected_index = None
        self.selected_index = idx

    def delete_selected(self):
        idx = self.column.get_selected_index()
        if idx is None:
            return
        try:
            del self.model.actions[idx]
        except Exception as exc:
            logging.error(f"Delete exchange error: {exc}")
        self.column.items = [ex.name for ex in self.model.actions]
        self.column.selected_index = None
        self.selected_index = None
        self.name_input.text = ""
        self.text_input.text = ""

    def confirm_edit(self):
        name = self.name_input.text.strip()
        text = self.text_input.text.strip()
        intent_idx = self.intent_dropdown.selected_index
        intent_subtype = (
            self.intent_dropdown.options[intent_idx]
            if intent_idx is not None and intent_idx < len(self.intent_dropdown.options)
            else None
        )
        if not name:
            self.editing = False
            return
        if self.edit_index is None:
            tpl = make_template()
            tpl.name = name
            tpl.text = text
            self.model.actions.append(tpl)

            if intent_subtype is not None:
                tpl.intent = PredicateTemplate("relationship", intent_subtype, False)
        else:
            tpl = self.model.actions[self.edit_index]
            tpl.name = name
            tpl.text = text
            if intent_subtype is not None:
                tpl.intent = PredicateTemplate("relationship", intent_subtype, False)

        self.column.items = [ex.name for ex in self.model.actions]
        self.editing = False
        self.column.selected_index = None
        self.selected_index = None
        self.name_input.text = ""
        self.text_input.text = ""
        self.intent_dropdown.selected_index = None

    def handle_event(self, event):
        if not self.visible:
            return
        # If any dropdown menu is open, capture clicks within it
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.MOUSEWHEEL):
            mx, my = event.pos if hasattr(event, "pos") else pygame.mouse.get_pos()
            open_dds = []
            if self.intent_dropdown.active:
                open_dds.append(self.intent_dropdown)
            for dd in open_dds:
                if dd.menu_rect().collidepoint(mx, my):
                    dd.handle_event(event)
                    return
        prev_selected = self.column.get_selected_index()
        self.column.handle_event(event)
        if not self.editing:
            idx = self.column.get_selected_index()
            if idx is not None and idx != prev_selected:
                self.selected_index = idx
                tpl = self.model.actions[idx]
                self.name_input.text = tpl.name
                self.text_input.text = tpl.text

                try:
                    self.intent_dropdown.selected_index = self.model.relationships.index(
                        tpl.intent.subtype
                    )
                except ValueError:
                    self.intent_dropdown.selected_index = None
                self.refresh_dropdown()
            elif idx is None:
                self.selected_index = None
                self.name_input.text = ""
                self.text_input.text = ""
                self.intent_dropdown.selected_index = None
        self.add_button.handle_event(event)
        self.edit_button.handle_event(event)
        self.delete_button.handle_event(event)
        self.close_button.handle_event(event)
        if self.editing:
            self.name_input.handle_event(event)
            self.text_input.handle_event(event)
            self.confirm_button.handle_event(event)
            self.intent_dropdown.handle_event(event)

    def draw(self, surface):
        if not self.visible:
            return
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, (40, 40, 40), rect)
        self.column.draw(surface)
        self.add_button.draw(surface)
        self.edit_button.draw(surface)
        self.delete_button.draw(surface)
        self.close_button.draw(surface)
        self.name_input.draw(surface)
        self.text_input.draw(surface)
        self.intent_dropdown.draw(surface)
        open_menus = []
        if self.intent_dropdown.active:
            open_menus.append(self.intent_dropdown)

        if self.editing:
            self.confirm_button.draw(surface)

        for dd in open_menus:
            dd.draw(surface)

    def _predicate_options(self) -> List[str]:
        return [f"trait:{t}" for t in self.model.traits] + [f"relationship:{r}" for r in self.model.relationships]
