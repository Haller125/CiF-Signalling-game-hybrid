from src.CiF.BCiF import BCiF
from src.pygame.components.ListManagerWindow import ListManagerWindow


class RelationshipsManagerWindow(ListManagerWindow):
    def __init__(self, x: int, y: int, width: int, height: int, model: BCiF, visible: bool = False):
        self.model = model
        super().__init__(x, y, width, height, model.relationships, visible)