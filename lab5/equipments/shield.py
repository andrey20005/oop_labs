from . import ParryArmor
from gladiator import BaseGladiator


class Shield(ParryArmor):
    def __init__(self, owner: BaseGladiator):
        super().__init__()
        self.owner = owner
        # Лёгкий щит — стандартный порог парирования
        self.parry_threshold = 12
