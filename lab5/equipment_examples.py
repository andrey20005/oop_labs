from attacks import Attack, CuttingAttack, FireAttack, Hit
from equipments import Equipment, EvasiveGear, FireWard, MissArmor, PhysicalArmor
from gladiator import BaseGladiator
from utils import DiceRoll, stat_to_modiff


class Sword(PhysicalArmor, MissArmor, Equipment):
    def __init__(self, owner: BaseGladiator):
        super().__init__() # Пройдёт по цепочке миксинов вверх до object
        self.owner = owner
        # Параметры защиты задаём уже здесь, после инициализации миксинов
        self.modif_dmg = 2
        self.modif_acc = -1

    def get_attacks(self) -> list[Attack]:
        atk = CuttingAttack()
        if self.owner:
            # Меч: классическое распределение
            atk.dmg.add_modif(stat_to_modiff(self.owner.strength))
            atk.accuracy.add_modif(stat_to_modiff(self.owner.dexterity))
        return [atk]


class Mace(PhysicalArmor, MissArmor, EvasiveGear, Equipment):
    def __init__(self, owner: BaseGladiator):
        super().__init__()
        self.owner = owner
        self.modif_dmg = -1
        self.modif_acc = 0

    def get_attacks(self) -> list[Attack]:
        atk = Hit()
        atk.dmg = DiceRoll(8)
        if self.owner:
            atk.dmg.add_modif(stat_to_modiff(self.owner.strength))
            atk.accuracy.add_modif(stat_to_modiff(self.owner.dexterity)) 
        return [atk]


class Torch(Equipment):
    def __init__(self, owner: BaseGladiator):
        super().__init__()
        self.owner = owner

    def get_attacks(self) -> list[Attack]:
        atk = FireAttack()
        if self.owner:
            atk.accuracy.add_modif(stat_to_modiff(self.owner.dexterity))
        return [atk]


class FullPlateArmor(PhysicalArmor, EvasiveGear, FireWard, MissArmor, Equipment):
    def __init__(self, owner: BaseGladiator):
        super().__init__()
        self.owner = owner
        self.modif_dmg = -3
        self.modif_acc = -2

    def get_attacks(self) -> list[Attack]:
        return []

