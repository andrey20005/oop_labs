from . import PhysicalArmor, FireWard, MissArmor, Equipment

class TowerShield(PhysicalArmor, FireWard, MissArmor, Equipment):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.modif_dmg = -4
        self.modif_acc = -3

    def get_attacks(self):
        return []
