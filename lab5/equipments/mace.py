from attacks import Hit
from . import Equipment, PhysicalArmor, MissArmor, EvasiveGear
from utils import DiceRoll, stat_to_modiff
from gladiator import BaseGladiator

class MaceHit(Hit):
    def __init__(self):
        super().__init__()
        self.name = "mace hit"
        self.dmg = DiceRoll(8)

class Mace(PhysicalArmor, MissArmor, EvasiveGear, Equipment):
    def __init__(self, owner: BaseGladiator):
        super().__init__()
        self.owner = owner
        self.modif_dmg = -1
        self.modif_acc = 0

    def get_attacks(self):
        atk = MaceHit()
        if self.owner:
            atk.dmg.add_modif(stat_to_modiff(self.owner.strength))
            atk.accuracy.add_modif(stat_to_modiff(self.owner.dexterity))
        return [atk]
