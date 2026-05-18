from . import PhysicalArmor, EvasiveGear, FireWard, MissArmor, Equipment
from gladiator import BaseGladiator

class FullPlateArmor(PhysicalArmor, EvasiveGear, FireWard, MissArmor, Equipment):
    def __init__(self, owner: BaseGladiator):
        super().__init__()
        self.owner = owner
        self.modif_dmg = -3
        self.modif_acc = -2

    def get_attacks(self):
        return []
