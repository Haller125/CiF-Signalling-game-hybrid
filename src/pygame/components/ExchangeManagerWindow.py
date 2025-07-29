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

    precondition_rows: List[PreconditionRow] = field(init=False, default_factory=list)
    add_precond_button: Button = field(init=False)

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
        self.preconditions_y = self.text_input.y + d_btwn // 2
        self.precond_cond_w = input_w // 3
        self.precond_pred_w = input_w - self.precond_cond_w - 35
        self.add_precond_button = Button(
            input_x,
            self.preconditions_y,
            btn_w,
            btn_h,
            "+Cond",
            on_click=self.add_precondition_row,
        )
        self.confirm_button = Button(
            input_x,
            self.preconditions_y + btn_h + 5,
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
        self.precondition_rows.clear()
        self.reposition_preconditions()

        if self.model.relationships:
            self.intent_dropdown.selected_index = 0
        else:
            self.intent_dropdown.selected_index = None

    def refresh_dropdown(self):
        self.intent_dropdown.options = list(self.model.relationships)
        self.intent_dropdown.scroll_offset = 0
        self.intent_dropdown.selected_index = None if self.intent_dropdown.options is not None else (self.intent_dropdown.selected_index or 0)

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
        self.precondition_rows.clear()
        for cond in getattr(tpl, "preconditions", []):
            self.add_precondition_row(from_condition=cond)
        if not self.precondition_rows:
            self.reposition_preconditions()
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

        tpl.preconditions = self.get_preconditions_from_rows()
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
            self.add_precond_button.handle_event(event)
            for row in self.precondition_rows:
                row.cond_dropdown.handle_event(event)
                row.pred_dropdown.handle_event(event)
                row.remove_button.handle_event(event)

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
        if self.editing:
            for row in self.precondition_rows:
                row.cond_dropdown.draw(surface)
                row.pred_dropdown.draw(surface)
                row.remove_button.draw(surface)
            self.add_precond_button.draw(surface)
            self.confirm_button.draw(surface)

    def _predicate_options(self) -> List[str]:
        return [f"trait:{t}" for t in self.model.traits] + [f"relationship:{r}" for r in self.model.relationships]

    def _cond_options(self) -> List[str]:
        return ["Has", "Has not", "Constant"]

    def reposition_preconditions(self):
        y = self.preconditions_y
        for row in self.precondition_rows:
            row.cond_dropdown.x = self.intent_dropdown.x
            row.pred_dropdown.x = self.intent_dropdown.x + self.precond_cond_w + 5
            row.remove_button.x = self.intent_dropdown.x + self.precond_cond_w + self.precond_pred_w + 10
            row.cond_dropdown.y = y
            row.pred_dropdown.y = y
            row.remove_button.y = y
            y += row.cond_dropdown.height + 5
        self.add_precond_button.y = y
        self.confirm_button.y = y + self.add_precond_button.height + 5

    def add_precondition_row(self, from_condition=None):
        cond_dd = Dropdown(
            self.intent_dropdown.x,
            0,
            self.precond_cond_w,
            25,
            options=self._cond_options(),
        )
        pred_dd = Dropdown(
            self.intent_dropdown.x + self.precond_cond_w + 5,
            0,
            self.precond_pred_w,
            25,
            options=self._predicate_options(),
        )
        rm_btn = Button(
            self.intent_dropdown.x + self.precond_cond_w + self.precond_pred_w + 10,
            0,
            25,
            25,
            "-",
            on_click=lambda: self.remove_precondition_row(row)
        )
        row = PreconditionRow(cond_dropdown=cond_dd, pred_dropdown=pred_dd, remove_button=rm_btn)
        if from_condition is not None:
            ctype, pval = self._condition_to_ui(from_condition)
            if ctype in cond_dd.options:
                cond_dd.selected_index = cond_dd.options.index(ctype)
            if pval and pval in pred_dd.options:
                pred_dd.selected_index = pred_dd.options.index(pval)
        else:
            if cond_dd.options:
                cond_dd.selected_index = 0
            if pred_dd.options:
                pred_dd.selected_index = 0
        self.precondition_rows.append(row)
        self.reposition_preconditions()

    def remove_precondition_row(self, row: PreconditionRow):
        if row in self.precondition_rows:
            self.precondition_rows.remove(row)
        self.reposition_preconditions()

    def _condition_to_ui(self, cond) -> tuple:
        from src.predicates.BCondition import BHasCondition, BHasNotCondition, BConstantCondition
        if isinstance(cond, BHasCondition):
            val = f"{cond.req_predicate.pred_type}:{cond.req_predicate.subtype}"
            return "Has", val
        if isinstance(cond, BHasNotCondition):
            val = f"{cond.req_predicate.pred_type}:{cond.req_predicate.subtype}"
            return "Has not", val
        if isinstance(cond, BConstantCondition):
            return "Constant", None
        return "Constant", None

    def get_preconditions_from_rows(self):
        from src.predicates.BCondition import BHasCondition, BHasNotCondition, BConstantCondition
        res = []
        for row in self.precondition_rows:
            ctype = row.cond_dropdown.options[row.cond_dropdown.selected_index] if row.cond_dropdown.selected_index is not None else "Has"
            pred_val = None
            if row.pred_dropdown.selected_index is not None and row.pred_dropdown.selected_index < len(row.pred_dropdown.options):
                pred_val = row.pred_dropdown.options[row.pred_dropdown.selected_index]
            if ctype == "Constant":
                res.append(BConstantCondition(1.0))
            else:
                if pred_val is None:
                    continue
                ptype, subtype = pred_val.split(":", 1)
                templ = PredicateTemplate(ptype, subtype, ptype == "trait")
                if ctype == "Has":
                    res.append(BHasCondition(templ))
                else:
                    res.append(BHasNotCondition(templ))
        return res