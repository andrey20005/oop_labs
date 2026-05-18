import random
from typing import Optional

from attacks import Attack, CuttingAttack, FireAttack, MissAttack, PhysicalAttack, StunAttack
from equipments import Equipment


class BaseGladiator:
    def __init__(self):
        self.name = "empty"
        self.hp = 20
        self.dexterity = 8
        self.strength = 8
        self.equipments: list[Equipment] = []
        
    def is_active(self) -> bool:
        return self.hp > 0

    def get_attack(self) -> Optional[Attack]:
        attacks = [attack for equipment in self.equipments for attack in equipment.get_attacks()]
        if attacks:
            return random.choice(attacks)
        return None

    def be_attacked(self, attack: Attack) -> None:
        for eq in self.equipments:
            eq.protect(attack)
    
    def update(self):
        pass
    
    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value: int):
        # Автоматическое ограничение от 0 до max_hp
        self._hp = max(0, value)


class HitResolutionMixin(BaseGladiator):
    def __init__(self):
        super().__init__()

    def be_attacked(self, attack: Attack) -> None:
        super().be_attacked(attack)
        if isinstance(attack, MissAttack) and attack.is_active_miss():
            attack.accuracy.roll()
            attack.accuracy_passed = attack.accuracy.last >= self.dexterity


class PhysicalDamageMixin(BaseGladiator):
    def __init__(self):
        super().__init__()

    def be_attacked(self, attack: Attack) -> None:
        super().be_attacked(attack)
        if isinstance(attack, PhysicalAttack) and attack.is_active_phys():
            self.hp -= max(0, attack.dmg.roll())


class BleedMixin(BaseGladiator):
    def __init__(self):
        super().__init__()
        self.bleed_dmg: int = 0

    def be_attacked(self, attack: Attack) -> None:
        super().be_attacked(attack)
        if isinstance(attack, CuttingAttack) and attack.is_active_cut():
            self.bleed_dmg = max(self.bleed_dmg, attack.bleeding_dmg.roll())

    def update(self) -> None:
        super().update()
        if self.bleed_dmg > 0:
            self.hp -= self.bleed_dmg
            self.bleed_dmg -= 1


class BurnMixin(BaseGladiator):
    def __init__(self):
        super().__init__()
        self.burn_turns: int = 0
        self.burn_dmg: int = 0

    def be_attacked(self, attack: Attack) -> None:
        super().be_attacked(attack)
        if isinstance(attack, FireAttack) and attack.is_active_fire():
            self.burn_turns = max(self.burn_turns, 3)
            self.burn_dmg = attack.fire_dmg

    def update(self) -> None:
        super().update()
        if self.burn_turns > 0:
            self.hp -= self.burn_dmg
            self.burn_turns -= 1
        else:
            self.burn_turns = 0
            self.burn_dmg = 0


class StunMixin(BaseGladiator):
    def __init__(self):
        super().__init__()
        self.stun_turns: int = 0

    def be_attacked(self, attack: Attack) -> None:
        super().be_attacked(attack)
        if isinstance(attack, StunAttack) and attack.is_active_stun():
            attack.stun_diff.roll()
            if attack.stun_diff.last >= self.dexterity:
                self.stun_turns = attack.stun_steps

    def update(self) -> None:
        super().update()
        if self.stun_turns > 0:
            self.stun_turns -= 1
    
    def get_attack(self) -> Optional[Attack]:
        if self.stun_turns == 0:
            return super().get_attack()
        return None


class Gladiator(StunMixin, BurnMixin, BleedMixin, PhysicalDamageMixin, HitResolutionMixin, BaseGladiator):
    def __init__(self, name="empty", hp=10, strength=8, dexterity=8):
        super().__init__()
        self.name = name 
        self.hp = hp
        self.strength = strength
        self.dexterity = dexterity
    
    def add_equipment(self, equipment):
        self.equipments.append(equipment)

    def print(self):
        print(f"{self.name}(dуxterity {self.dexterity}, strength {self.strength})")
        print(f"hp {self.hp}{["", " горит"][self.burn_turns > 0]}{["", " оглушен"][self.stun_turns > 0]}")
        print(f"equipments {", ".join(eq.__class__.__name__ for eq in self.equipments)}")
