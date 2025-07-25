from dataclasses import dataclass, field
from typing import List

import pygame

from src.CiF.BCiF import BCiF
from src.npc.BNPC import BNPC
from src.pygame import MainWindow
from src.pygame.components.Button import Button
from src.pygame.components.Column import Column
from src.pygame.components.TabWindow import TabWindow
from src.pygame.components.TopBar import TopBar
from src.social_exchange.BSocialExchange import BSocialExchange


@dataclass
class Game:
    model: BCiF
    npcs: List = None
    actions: List = None
    traits: List[str] = None
    relationships: List[str] = None

    left_column: Column = None
    left_column_exclude_items: List = field(default_factory=list)
    right_column: Column = None
    right_column_exclude_items: List = field(default_factory=list)

    mid_window: TabWindow = None

    def __post_init__(self):
        self.npcs = self.model.NPCs
        self.actions = self.model.actions
        self.traits = self.model.traits
        self.relationships = self.model.relationships

        self.window = MainWindow.GameWindow()
        topbar = TopBar(width=self.window.width, height=self.window.height // 5)
        btn_w, btn_h = 80, topbar.height - 10
        spacing = 10
        x_start = topbar.width - (btn_w * 2 + spacing * 3)
        buttons = [

            Button(x=x_start + spacing, y=5, width=btn_w, height=btn_h, text="Home"),
            Button(x=x_start + 2 * spacing + btn_w, y=5, width=btn_w, height=btn_h, text="Next iteration", on_click=self.next_iteration),
            # Button(x=spacing, y=5, width=btn_w, height=btn_h, text="Braincheck")
        ]
        topbar.buttons = buttons
        self.window.add_object(topbar)

        # Left column
        content_y = topbar.height
        content_h = self.window.height - topbar.height
        column_left = Column(
            x=0,
            y=content_y,
            width=self.window.width // 4,
            height=content_h,
            items=self.npcs,
            exclude_items= self.left_column_exclude_items,
        )
        self.left_column = column_left
        self.window.add_object(column_left)

        # Right column
        column_right = Column(
            x=self.window.width - self.window.width // 4,
            y=content_y,
            width=self.window.width // 4,
            height=content_h,
            items=self.npcs,
            exclude_items=self.npcs.copy(),
        )
        self.right_column = column_right
        self.window.add_object(column_right)

        mid = TabWindow(x=self.window.width // 4, y=content_y,
                        width=self.window.width // 2, height=content_h,
                        tabs=['History', 'Traits', 'Relationships'],
                        get_data_for_tab=self.get_data_for_mid_window)
        self.window.add_object(mid)
        self.mid_window = mid

    def run(self):
        running = True
        counter = 0
        while running:
            self.window.running_step()
            if counter >= 1:
                self.update_state()
                counter = 0
            counter += 1
        pygame.quit()

    def update_state(self):
        selected_left = self.get_left_column_selection()
        selected_right = self.get_right_column_selection()

        if selected_left is None:
            self.right_column.exclude_items = self.npcs
            self.mid_window.disable()
        else:
            self.right_column.exclude_items = [selected_left]
            self.mid_window.enable()
            if selected_right is None:
                self.mid_window.disable_tab(0)
                self.mid_window.disable_tab(2)
            else:
                self.mid_window.enable_all_tabs()

    def next_iteration(self):
        self.model.iteration()

    def get_left_column_selection(self):
        selected_index = self.left_column.get_selected_index()
        if selected_index is None:
            return None
        return self.left_column.items[selected_index]

    def get_right_column_selection(self):
        selected_index = self.right_column.get_selected_index()
        if selected_index is None:
            return None
        return self.right_column.items[selected_index]

    def get_traits(self):
        npc: BNPC = self.get_left_column_selection()

        beliefs = npc.get_traits()
        data = [f"{belief.predicate.subtype}" for belief in beliefs]
        return data

    def get_relationships(self):
        subject: BNPC = self.get_left_column_selection()
        target: BNPC = self.get_right_column_selection()

        beliefs = subject.get_relationships(subject, target)
        data = [(f"{belief.predicate.subtype}", belief.probability) for belief in beliefs]
        return data

    def get_history(self):
        subject: BNPC = self.get_left_column_selection()
        target: BNPC = self.get_right_column_selection()

        exchanges: List[BSocialExchange] = self.model.get_exchanges(subject, target)

        exchanges.reverse()

        return [f"{exchange.initiator} {exchange.text} {exchange.responder}" for exchange in exchanges]

    def get_data_for_mid_window(self, i: int):
        match i:
            case 0:
                return self.get_history()
            case 1:
                return self.get_traits()
            case 2:
                return self.get_relationships()

    def save(self, path: str) -> None:
        from src.save_system.save_system import save_model
        save_model(self.model, path)

    @staticmethod
    def load(path: str) -> 'Game':
        from src.save_system.save_system import load_model
        model = load_model(path)
        return Game(model)


