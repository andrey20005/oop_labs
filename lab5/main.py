from equipments.dagger import Dagger
from equipments.full_plate_armor import FullPlateArmor
from equipments.mace import Mace
from equipments.spear import Spear
from equipments.shield import Shield
from equipments.sword import Sword
from equipments.tower_shield import TowerShield
from gladiator import Gladiator
from rich.console import Console

from attacks import Attack
from utils import obj_print

class Game:
    def __init__(self, gladiators: list[Gladiator]):
        self.gladiators = gladiators
        self.console = Console()
    
    def step_attack_and_print(self, step):
        print()
        # obj_print(g1)
        g1.print()
        print()
        # obj_print(g1)
        g2.print()
        attacking, defending = self.gladiators[step % 2], self.gladiators[(step+1) % 2]
        attack = attacking.get_attack()
        print([f"\n-- {g1.name} атакует --", f"\n-- {g2.name} атакует --"][step % 2])
        # obj_print(attack)
        print(attack)
        if attack:
            defending.be_attacked(attack)
    
    def attack_step(self, attacking: Gladiator, defending: Gladiator, step):
        attack = attacking.get_attack()
        if attack:
            defending.be_attacked(attack)

    def uptate_step(self):
        for gladiator in self.gladiators:
            gladiator.update()

    def run(self, max_step=100):
        for step in range(max_step):
            # print(step)
            self.uptate_step()
            if not all(g.is_active() for g in self.gladiators):
                break
            # self.attack_step(self.gladiators[step % 2], self.gladiators[(step+1) % 2], step)
            self.step_attack_and_print(step)
            if not all(g.is_active() for g in self.gladiators):
                break
        print()
        # obj_print(g1)
        g1.print()
        print()
        # obj_print(g1)
        g2.print()


if __name__ == "__main__":
    g1 = Gladiator(name="Борис", hp=24, strength=14, dexterity=10) # Силач
    g1.add_equipment(Sword(owner=g1))

    g2 = Gladiator(name="Астольф", hp=28, strength=10, dexterity=12) # Ловкач в броне
    g2.add_equipment(Mace(owner=g2))
    g2.add_equipment(FullPlateArmor(owner=g2))

    # obj_print(g1)

    game = Game([g1, g2])

    game.run()

    # Новая пара бойцов g3 и g4
    g3 = Gladiator(name="Леон", hp=18, strength=12, dexterity=14)
    g3.add_equipment(Dagger(owner=g3))
    g3.add_equipment(Shield(owner=g3))

    g4 = Gladiator(name="Мартин", hp=22, strength=13, dexterity=9)
    g4.add_equipment(Spear(owner=g4))
    g4.add_equipment(TowerShield(owner=g4))

    print("\n=== Бой g3 vs g4 ===")
    game2 = Game([g3, g4])
    game2.run()

