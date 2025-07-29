import logging
from dataclasses import field, dataclass
from typing import Optional

import pygame

from src.CiF.BCiF import BCiF
from src.pygame.components.IComponent import IComponent
from src.pygame.components.Column import Column
from src.pygame.components.Button import Button
from src.pygame.components.InputBox import InputBox
from src.social_exchange.BSocialExchangeTemplate import make_template

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
        self.add_button = Button(self.x + column_w + 10, btn_y, btn_w, btn_h,
                                 "Add", on_click=self.start_add)
        self.edit_button = Button(self.x + column_w + 10, btn_y + btn_h + 5,
                                  btn_w, btn_h, "Edit", on_click=self.start_edit)
        self.delete_button = Button(self.x + column_w + 10, btn_y + 2 * (btn_h + 5),
                                    btn_w, btn_h, "Delete", on_click=self.delete_selected)
        input_x = self.x + column_w + 10
        input_w = self.width - column_w - 20
        self.name_input = InputBox(input_x, self.y + self.height // 2 - 40, input_w, 25)
        self.text_input = InputBox(input_x, self.y + self.height // 2, input_w, 25)
        self.confirm_button = Button(
            input_x,
            self.y + self.height // 2 + 35,
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
            tpl = self.model.actions[0]
            self.name_input.text = tpl.name
            self.text_input.text = tpl.text

    def start_add(self):
        self.editing = True
        self.edit_index = None
        self.name_input.text = ""
        self.text_input.text = ""
        self.selected_index = None

    def close_window(self):
        self.editing = False
        self.edit_index = None
        self.column.selected_index = None
        self.selected_index = None
        self.name_input.text = ""
        self.text_input.text = ""
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
        if not name:
            self.editing = False
            return
        if self.edit_index is None:
            tpl = make_template()
            tpl.name = name
            tpl.text = text
            self.model.actions.append(tpl)
        else:
            tpl = self.model.actions[self.edit_index]
            tpl.name = name
            tpl.text = text
        self.column.items = [ex.name for ex in self.model.actions]
        self.editing = False
        self.column.selected_index = None
        self.selected_index = None
        self.name_input.text = ""
        self.text_input.text = ""

    def handle_event(self, event):
        if not self.visible:
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
            elif idx is None:
                self.selected_index = None
                self.name_input.text = ""
                self.text_input.text = ""
        self.add_button.handle_event(event)
        self.edit_button.handle_event(event)
        self.delete_button.handle_event(event)
        self.close_button.handle_event(event)
        if self.editing:
            self.name_input.handle_event(event)
            self.text_input.handle_event(event)
            self.confirm_button.handle_event(event)

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
        if self.editing:
            self.confirm_button.draw(surface)