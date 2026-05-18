from attacks import CuttingAttack
from equipments import ParryArmor, MissArmor, Equipment
from utils import DiceRoll, stat_to_modiff
from gladiator import BaseGladiator

class SwordCut(CuttingAttack):
    def __init__(self):
        super().__init__()
        self.name = "sword cut"
        self.dmg = DiceRoll(6)
        self.bleeding_dmg = DiceRoll(3)


class Sword(ParryArmor, MissArmor, Equipment):
    def __init__(self, owner: BaseGladiator):
        super().__init__()
        self.owner = owner
        self.modif_acc = -1

    def get_attacks(self):
        atk = SwordCut()
        if self.parry:
            atk.accuracy.advantage()
        if self.owner:
            atk.dmg.add_modif(stat_to_modiff(self.owner.strength))
            atk.accuracy.add_modif(stat_to_modiff(self.owner.dexterity))
        return [atk]
