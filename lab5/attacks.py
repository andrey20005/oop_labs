from utils import DiceRoll

# Это просто структуры и у мих не может быть методов. Плюс у всех атак должен быть пустой конструктор 
# Создавая нового наследника с новыми полями, убедись что имена полей не совпадают с именами в других атаках 
class Attack:
    def __init__(self):
        self.name = "empty"


class MissAttack(Attack):
    def __init__(self):
        super().__init__()
        # попадание если больше или равен 10
        # броня может менять модификатор и/или сделать перймощество/помеху
        self.accuracy: DiceRoll = DiceRoll(20)
        self.accuracy_passed = True  # Устанавливается боевой системой после броска точности

    def is_active_miss(self) -> bool:
        return self.accuracy_passed


class PhysicalAttack(MissAttack):
    def __init__(self):
        super().__init__()
        self.name: str = "physical attack"
        self.dmg: DiceRoll = DiceRoll(1, modif=-1)
        self._phys_active = True

    def is_active_phys(self) -> bool:
        # Физика работает только если прошло попадание И флаг не сбит
        return self.is_active_miss() and self._phys_active


class Hit(PhysicalAttack):
    def __init__(self):
        super().__init__()
        self.name = "hit"
        self.dmg: DiceRoll = DiceRoll(4)


class CuttingAttack(PhysicalAttack):
    def __init__(self):
        super().__init__()
        self.name = "cut"
        self.dmg = DiceRoll(6)
        self.bleeding_dmg = DiceRoll(4) 
        self._cut_active = True

    def is_active_cut(self) -> bool:
        return self.is_active_phys() and self._cut_active


class StunAttack(MissAttack):
    def __init__(self):
        super().__init__()
        self.name = "stun"
        self.stun_steps = 1
        # значение точности которое должно сработать что-бы прошел стан
        self.stun_diff: DiceRoll = DiceRoll(20, modif=5) 
        
        self._stun_active = True

    def is_active_stun(self) -> bool:
        return self.is_active_miss() and self._stun_active


class FireAttack(MissAttack):
    def __init__(self):
        super().__init__()
        self.fire_dmg: int = 2
        self._fire_active = True

    def is_active_fire(self) -> bool:
        return self.is_active_miss() and self._fire_active


class TestAttack1(FireAttack, StunAttack):
    def __init__(self):
        super().__init__()
        self.name = "test attack 1"


if __name__ == "__main__":
    print(CuttingAttack())
    print(TestAttack1())
