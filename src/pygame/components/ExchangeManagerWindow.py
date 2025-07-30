import logging
from dataclasses import field, dataclass
from typing import Optional

import pygame

from src.CiF.BCiF import BCiF
from src.predicates.PredicateTemplate import PredicateTemplate
from src.pygame.components.Dropdown import Dropdown
from src.pygame.components.IComponent import IComponent
from src.pygame.components.Column import Column
from src.pygame.components.Button import Button
from src.pygame.components.InputBox import InputBox
from src.pygame.components.PreconditionEditor import PreconditionEditor
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

    precond_label_y: int = field(init=False, default=0)
    precond_editor: PreconditionEditor = field(init=False)

    editing: bool = field(init=False, default=False)
    edit_index: Optional[int] = field(init=False, default=None)
    selected_index: Optional[int] = field(init=False, default=None)
    on_close: Optional[callable] = field(default=None, repr=False)

    scroll_offset: int = field(init=False, default=0)
    max_scroll: int = field(init=False, default=0)
    scroll_speed: int = 20
    intent_dropdown_y0: int = field(init=False, default=0)
    name_input_y0: int = field(init=False, default=0)
    text_input_y0: int = field(init=False, default=0)
    precond_editor_y0: int = field(init=False, default=0)

    def __post_init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 20)
        self._init_column()
        self._init_buttons()
        self._init_inputs()

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

        self.precond_editor.refresh()
        self.intent_dropdown_y0 = self.intent_dropdown.y
        self.name_input_y0 = self.name_input.y
        self.text_input_y0 = self.text_input.y
        self.precond_editor_y0 = self.precond_editor.y
        self._update_scroll_limits()

    def _init_column(self):
        self.column_w = self.width // 3
        self.column = Column(
            self.x,
            self.y,
            self.column_w,
            self.height,
            items=[ex.name for ex in self.model.actions],
        )

    def _init_buttons(self):
        btn_w, btn_h = 80, 25
        self.btn_h = btn_h
        column_w = self.column_w
        btn_y = self.y
        top_padding = 10
        self.add_button = Button(
            self.x + column_w + 10,
            btn_y + top_padding,
            btn_w,
            btn_h,
            "Add",
            on_click=self.start_add,
        )
        self.edit_button = Button(
            self.x + column_w + 10,
            btn_y + btn_h + 5 + top_padding,
            btn_w,
            btn_h,
            "Edit",
            on_click=self.start_edit,
        )
        self.delete_button = Button(
            self.x + column_w + 10,
            btn_y + 2 * (btn_h + 5) + top_padding,
            btn_w,
            btn_h,
            "Delete",
            on_click=self.delete_selected,
        )
        close_x = self.x + self.width - btn_w - 10
        self.close_button = Button(
            close_x,
            self.y + 5,
            btn_w,
            btn_h,
            "Close",
            on_click=self.close_window,
        )

    def _init_inputs(self):
        column_w = self.column_w
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
            label="Name of Exchange",
        )
        self.text_input = InputBox(
            input_x,
            top_y + d_btwn * 2,
            input_w,
            25,
            label="Text of Exchange (for logging in history tab)",
        )
        self.precond_label_y = top_y + d_btwn * 3
        self.confirm_button = Button(
            input_x,
            self.btn_h + 5,
            80,
            self.btn_h,
            "OK",
            on_click=self.confirm_edit,
        )
        self.precond_editor = PreconditionEditor(
            self.name_input.x,
            self.precond_label_y,
            input_w,
            self.model,
            lambda: self.selected_index,
            lambda y: setattr(self.confirm_button, "y", y),
        )

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
        self.precond_editor.refresh()
        self._update_scroll_limits()
        self._apply_scroll()

    def refresh_dropdown(self):
        self.intent_dropdown.options = list(self.model.relationships)
        self.intent_dropdown.scroll_offset = 0
        self.intent_dropdown.selected_index = None if self.intent_dropdown.options is None else (
                self.intent_dropdown.selected_index or 0)

    def close_window(self):
        self.editing = False
        self.edit_index = None
        self.column.selected_index = None
        self.selected_index = None
        self.name_input.text = ""
        self.text_input.text = ""
        self.intent_dropdown.selected_index = None
        self.precond_editor.refresh()
        self._update_scroll_limits()
        self._apply_scroll()

    def _update_scroll_limits(self):
        num_preconds = 0
        if self.selected_index is not None and self.selected_index < len(self.model.actions):
            num_preconds = len(self.model.actions[self.selected_index].preconditions)
        height = 25
        spacing = 5
        bottom = self.precond_editor_y0 + num_preconds * (height + spacing) + 5 + self.confirm_button.height
        self.max_scroll = max(0, bottom - (self.y + self.height))
        self.scroll_offset = min(self.scroll_offset, self.max_scroll)

    def _apply_scroll(self):
        self.intent_dropdown.y = self.intent_dropdown_y0 - self.scroll_offset
        self.name_input.y = self.name_input_y0 - self.scroll_offset
        self.text_input.y = self.text_input_y0 - self.scroll_offset
        self.precond_editor.set_scroll(self.scroll_offset)

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
        self.precond_editor.refresh()
        self._update_scroll_limits()
        self._apply_scroll()

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
        self.precond_editor.refresh()
        self._update_scroll_limits()
        self._apply_scroll()

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
        self.precond_editor.refresh()

    def handle_event(self, event):
        if not self.visible:
            return
        # If any dropdown menu is open, capture clicks within it
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.MOUSEWHEEL):
            mx, my = event.pos if hasattr(event, "pos") else pygame.mouse.get_pos()
            open_dds = []
            if self.intent_dropdown.active:
                open_dds.append(self.intent_dropdown)
            if self.editing:
                open_dds.extend(self.precond_editor.get_active_dropdowns())
            for dd in open_dds:
                if dd.menu_rect().collidepoint(mx, my):
                    dd.handle_event(event)
                    return

        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL):
            mx, my = event.pos if hasattr(event, "pos") else pygame.mouse.get_pos()
            if self.x + self.column_w <= mx <= self.x + self.width and self.y <= my <= self.y + self.height:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5):
                    delta = -self.scroll_speed if event.button == 4 else self.scroll_speed
                    self.scroll_offset = max(0, min(self.scroll_offset + delta, self.max_scroll))
                    self._apply_scroll()
                    return
                elif event.type == pygame.MOUSEWHEEL:
                    delta = -event.y * self.scroll_speed
                    self.scroll_offset = max(0, min(self.scroll_offset + delta, self.max_scroll))
                    self._apply_scroll()
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
                self.precond_editor.refresh()
                self._update_scroll_limits()
                self._apply_scroll()
            elif idx is None:
                self.selected_index = None
                self.name_input.text = ""
                self.text_input.text = ""
                self.intent_dropdown.selected_index = None
                self.precond_editor.refresh()
                self._update_scroll_limits()
                self._apply_scroll()
        self.add_button.handle_event(event)
        self.edit_button.handle_event(event)
        self.delete_button.handle_event(event)
        self.close_button.handle_event(event)
        if self.editing:
            self.name_input.handle_event(event)
            self.text_input.handle_event(event)
            self.confirm_button.handle_event(event)
            self.intent_dropdown.handle_event(event)
        if self.editing:
            self.precond_editor.handle_event(event)

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
        surface.set_clip(rect)
        self.name_input.draw(surface)
        self.text_input.draw(surface)
        self.intent_dropdown.draw(surface)
        open_menus = []
        if self.intent_dropdown.active:
            open_menus.append(self.intent_dropdown)

        if self.editing:
            self.confirm_button.draw(surface)

        active = self.precond_editor.draw(surface, self.editing)
        open_menus.extend(active)

        surface.set_clip(None)

        for dd in open_menus:
            dd.draw(surface)
