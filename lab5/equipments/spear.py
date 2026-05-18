import random
from attacks import PhysicalAttack, StunAttack
from . import Equipment, MissArmor, PhysicalArmor
from utils import DiceRoll, stat_to_modiff
from gladiator import BaseGladiator

class StabAttack(PhysicalAttack):
    def __init__(self):
        super().__init__()
        self.name = "stab"
        self.dmg = DiceRoll(4)
        self.accuracy.add_modif(2)


class TripStab(PhysicalAttack, StunAttack):
    def __init__(self):
        super().__init__()
        self.name = "trip stab"
        self.dmg = DiceRoll(3)
        self.stun_diff = 10
        self.stun_steps = 1
        self.accuracy.add_modif(2)


class Spear(PhysicalArmor, MissArmor, Equipment):
    def __init__(self, owner: BaseGladiator):
        super().__init__()
        self.owner = owner
        self.modif_dmg = -1
        self.modif_acc = -1

    def get_attacks(self):
        atk1 = StabAttack()
        if self.owner:
            atk1.dmg.add_modif(stat_to_modiff(self.owner.strength))
            atk1.accuracy.add_modif(stat_to_modiff(self.owner.dexterity))
        atk2 = StabAttack()
        if self.owner:
            atk2.dmg.add_modif(stat_to_modiff(self.owner.strength))
            atk2.accuracy.add_modif(stat_to_modiff(self.owner.dexterity))
        return [atk2]
