from random import randint

class Dice:
    def __init__(self, sides: int):
        self.sides = sides

    def roll(self) -> int:
        return randint(1, self.sides)

    def advantage(self) -> int:
        return max(self.roll(), self.roll())

    def disadvantage(self) -> int:
        return min(self.roll(), self.roll())

# Global constants for dice
D4 = Dice(4)
D6 = Dice(6)
D8 = Dice(8)
D12 = Dice(12)
D20 = Dice(20)

