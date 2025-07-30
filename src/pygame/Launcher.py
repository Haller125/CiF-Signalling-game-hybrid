from dataclasses import dataclass, field
from typing import List
import os
import pygame
import yaml

from src.pygame.MainWindow import GameWindow
from src.pygame.components.Button import Button
from src.pygame.components.Dropdown import Dropdown
from src.CiFBuilder.BCiFBuilder import CiFBuilder
from src.social_exchange.exchange_loader import load_exchange_templates
from src.save_system.save_system import load_model
from src.pygame.Game import Game
from src.names.names import Names


SAVES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "saves")
CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "configs")


@dataclass
class Launcher:
    window: GameWindow = field(default_factory=GameWindow)
    dropdown: Dropdown | None = None
    buttons: List[Button] = field(default_factory=list)

    def __post_init__(self):
        os.makedirs(SAVES_DIR, exist_ok=True)
        files = [f for f in os.listdir(SAVES_DIR) if f.endswith(".cif")]

        dd_width = self.window.width // 2
        dd_x = (self.window.width - dd_width) // 2
        dd_y = self.window.height // 3
        self.dropdown = Dropdown(
            x=dd_x,
            y=dd_y,
            width=dd_width,
            height=30,
            options=files,
            label="Choose save",
        )
        self.window.add_object(self.dropdown)

        btn_w = 100
        btn_h = 30
        btn_y = dd_y + 60
        load_btn = Button(
            x=dd_x,
            y=btn_y,
            width=btn_w,
            height=btn_h,
            text="Load",
            on_click=self.load_game,
        )
        create_btn = Button(
            x=dd_x + btn_w + 20,
            y=btn_y,
            width=btn_w,
            height=btn_h,
            text="Create",
            on_click=self.create_game,
        )
        self.buttons = [load_btn, create_btn]
        for b in self.buttons:
            self.window.add_object(b)

    def run(self):
        running = True
        while running:
            self.window.running_step()
            if not pygame.get_init():
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def load_game(self):
        if not self.dropdown or self.dropdown.selected_index is None:
            return
        filename = self.dropdown.options[self.dropdown.selected_index]
        path = os.path.join(SAVES_DIR, filename)
        model = load_model(path)
        game = Game(model)
        game.run()

    def create_game(self):
        traits_path = os.path.join(CONFIG_DIR, "traits.yaml")
        relationships_path = os.path.join(CONFIG_DIR, "relationships.yaml")
        exchanges_path = os.path.join(CONFIG_DIR, "exchanges.yaml")

        with open(traits_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        trait_probs = data.get("probabilities", {})
        trait_pairs = list(trait_probs.items())
        trait_opps = data.get("opposites", {})

        with open(relationships_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        rel_probs = data.get("probabilities", {})
        rel_pairs = list(rel_probs.items())
        rel_opps = data.get("opposites", {})

        templates = load_exchange_templates(exchanges_path)
        names = Names().get_n_name(5)
        builder = CiFBuilder(
            traits=trait_pairs,
            relationships=rel_pairs,
            exchanges=templates,
            names=names,
            n=5,
            trait_opposites=trait_opps,
            relationship_opposites=rel_opps,
        )
        model = builder.build()
        game = Game(model)
        game.run()
