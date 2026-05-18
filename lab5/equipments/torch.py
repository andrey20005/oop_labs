from attacks import FireAttack
from . import Equipment
from utils import DiceRoll, stat_to_modiff
from gladiator import BaseGladiator

class FireBurst(FireAttack):
    def __init__(self):
        super().__init__()
        self.name = "fire burst"
        self.fire_dmg = 3

class Torch(Equipment):
    def __init__(self, owner: BaseGladiator):
        super().__init__()
        self.owner = owner

    def get_attacks(self):
        atk = FireBurst()
        if self.owner:
            atk.accuracy.add_modif(stat_to_modiff(self.owner.dexterity))
        return [atk]
