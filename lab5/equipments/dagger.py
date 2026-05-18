import random
from attacks import CuttingAttack
from . import Equipment, MissArmor, PhysicalArmor
from utils import DiceRoll, stat_to_modiff
from gladiator import BaseGladiator

# Локальная модификация атаки, определена в модуле оружия
class QuickCut(CuttingAttack):
    def __init__(self):
        super().__init__()
        self.name = "quick cut"
        self.dmg = DiceRoll(4)
        self.bleeding_dmg = DiceRoll(1)


class Dagger(PhysicalArmor, MissArmor, Equipment):
    def __init__(self, owner: BaseGladiator):
        super().__init__()
        self.owner = owner
        self.modif_dmg = 0
        self.modif_acc = 1

    def get_attacks(self):
        atk = QuickCut()
        if self.owner:
            atk.dmg.add_modif(stat_to_modiff(self.owner.strength))
            atk.accuracy.add_modif(stat_to_modiff(self.owner.dexterity))
        return [atk]
