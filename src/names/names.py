from dataclasses import dataclass
import random

from names_dataset import NameDataset

@dataclass
class Names:
    names: NameDataset = NameDataset()
    fnames = list(names.first_names)

    def get_name(self):
        return random.choice(list(self.names.first_names))

    def get_n_name(self, n: int):
        return random.sample(self.fnames, n)
