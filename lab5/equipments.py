from attacks import Attack, FireAttack, MissAttack, PhysicalAttack


class Equipment:
    def get_attacks(self) -> list[Attack]:
        return []
    
    def protect(self, attack: Attack):
        pass 


class MissArmor(Equipment):
    def __init__(self):
        super().__init__()
        self.modif_acc = 0
    
    def protect(self, attack):
        super().protect(attack)
        if isinstance(attack, MissAttack) and attack.is_active_miss():
            attack.accuracy.add_modif(self.modif_acc)


class PhysicalArmor(Equipment):
    def __init__(self):
        super().__init__()
        self.modif_dmg = 0

    def protect(self, attack: Attack):
        super().protect(attack)
        if isinstance(attack, PhysicalAttack) and attack.is_active_phys():
            attack.dmg.add_modif(self.modif_dmg)


class FireWard(Equipment):
    def __init__(self):
        super().__init__()

    def protect(self, attack: Attack):
        super().protect(attack)
        # Если это огонь и он активен -> полностью блокируем механику поджога
        if isinstance(attack, FireAttack) and attack.is_active_fire():
            attack._fire_active = False


class EvasiveGear(Equipment):
    def __init__(self):
        super().__init__()

    def protect(self, attack: Attack):
        super().protect(attack)
        # Помеха на проверку попадания
        if isinstance(attack, MissAttack):
            attack.accuracy.disadvantage()

