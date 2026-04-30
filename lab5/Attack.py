from typing import List

from lab5.utils.dice import Dice, D20

class Attack:
    pass


class FlatDamage(Attack):
    def __init__(self, dmg: int):
        self.dem = dmg 


class DamageAttack(Attack):
    def __init__(self, modifier: int, *damage_dice: List[Dice]):
        self.modifier = modifier
        self.damage_dice = damage_dice

    def roll_damage(self, critical: bool = False) -> int:
        if critical:
            return sum(die.advantage() for die in self.damage_dice)
        return sum(die.roll() for die in self.damage_dice)

    def attempt(self, target_limb_strength: int) -> int:
        dice_result = D20.roll()
        if dice_result == 20:
            return self.roll_damage(critical=True)
        elif dice_result == 1:
            return 0
        
        if (dice_result + self.modifier) >= target_limb_strength:
            return self.roll_damage()
        return 0
