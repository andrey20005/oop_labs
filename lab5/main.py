from equipment_examples import FullPlateArmor, Mace, Sword
from gladiator import Gladiator
from rich.console import Console
from rich.table import Table

from attacks import Attack
from utils import obj_print

class Game:
    def __init__(self, gladiators: list[Gladiator]):
        self.gladiators = gladiators
        self.console = Console()
    
    def step_attack_and_print(self, step):
        print("\n-- g1 --")
        obj_print(g1)
        print("\n-- g2 --")
        obj_print(g1)
        attacking, defending = self.gladiators[step % 2], self.gladiators[(step+1) % 2]
        attack = attacking.get_attack()
        print(["\n-- g1 attack --", "\n-- g2 attack --"][step % 2])
        obj_print(attack)
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
        print("\n-- g1 --")
        obj_print(g1)
        print("\n-- g2 --")
        obj_print(g1)
    

if __name__ == "__main__":
    g1 = Gladiator(name="Борис", hp=24, strength=14, dexterity=10) # Силач
    g1.add_equipment(Sword(owner=g1))

    g2 = Gladiator(name="Астольф", hp=28, strength=10, dexterity=12) # Ловкач в броне
    g2.add_equipment(Mace(owner=g2))
    g2.add_equipment(FullPlateArmor(owner=g2))

    # obj_print(g1)

    game = Game([g1, g2])

    game.run()

