from random import randint
from typing import Optional
from rich.pretty import pprint


def tab(text: str, spaces: int = 4):
    padding = " " * spaces
    return "".join(padding + line for line in text.splitlines(keepends=True))

def to_deep_dict(obj):
    """Рекурсивно превращает любые объекты и их вложенности в словари."""
    # Если это кастомный класс, берем его поля
    if hasattr(obj, "__dict__"):
        return {obj.__class__.__name__: {k: to_deep_dict(v) for k, v in obj.__dict__.items() if k != "owner"}}
    # Если это словарь, обрабатываем его значения
    elif isinstance(obj, dict):
        return {k: to_deep_dict(v) for k, v in obj.items()}
    # Если это список, кортеж или сет, обрабатываем каждый элемент
    elif isinstance(obj, (list, tuple, set)):
        return [to_deep_dict(item) for item in obj]
    # Если это базовый тип (str, int, float и т.д.), возвращаем как есть
    return obj

def obj_print(obj):
    pprint(to_deep_dict(obj))


def stat_to_modiff(stat: int) -> int:
    return (stat - 10) // 2


class DiceRoll:
    def __init__(self, sides: int, quality=0, modif=0):
        self.sides: int = sides
        self.quality: int = quality
        self.modif: int = modif
        self.last: Optional[int] = None
    
    def advantage(self):
        self.quality += 1
    
    def disadvantage(self):
        self.quality -= 1

    def add_modif(self, modif):
        self.modif += modif
    
    def roll(self):
        self.last = self.modif
        if self.quality < 0:
            self.last += min(randint(1, self.sides) for _ in range(-self.quality))
        elif self.quality > 0:
            self.last += max(randint(1, self.sides) for _ in range(self.quality))
        else:
            self.last += randint(1, self.sides)
        return self.last

    def __str__(self):
        res = []
        if self.quality != 0:
            res.append(f"q{["+", ""][self.quality < 0]}{self.quality}")
        if self.modif != 0:
            res.append(f"m{["+", ""][self.modif < 0]}{self.modif}")
        return f"D{self.sides}({" ".join(res)})"
