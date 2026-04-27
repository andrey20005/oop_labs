from random import random
from typing import List
from rich.console import Console
from rich.table import Table

class Animal:
    def __init__(self, name: str):
        self.pos: float = 0 # положение животного а метрах от старта
        self.move_callback = None
        self.name = name

    def move(self, step: float):
        self.pos += step
        if self.move_callback: 
            self.move_callback(self, step)

    def set_move_callback(self, move_collback):
        self.move_callback = move_collback

    def _get_random_coef(self, a=0.1) -> float:
        return (1. - (a)) + 2. * a * (random() + random() + random() + random()) / 4

    # абстрактные методы
    def get_species(self) -> str:
        raise NotImplementedError

    def start_race(self):
        self.pos = 0.

    def get_status(self) -> str:
        raise NotImplementedError 

    def go(self):
        raise NotImplementedError


class Horse(Animal):
    def __init__(self, name: str, speed: float):
        super().__init__(name)
        self.speed = speed

    def get_species(self):
        return "лошадь"

    def start_race(self):
        super().start_race()

    def get_status(self) -> str:
        return f"бежит"

    def go(self):
        random_coef = self._get_random_coef()
        step = self.speed * random_coef
        self.move(step)


class Cheetah(Animal):
    def __init__(self, name: str, average_speed: float, jerk_speed: float):
        super().__init__(name)
        self.average_speed = average_speed
        self.jerk_speed = jerk_speed
        self.status = "бежит"

    def get_species(self):
        return "гепард"

    def start_race(self):
        super().start_race()
        self.status = "бежит"

    def get_status(self):
        return self.status

    def go(self):
        if self.status == "бежит" and random() < 0.4:
            self.status = "делает рывок"
            step = self.jerk_speed * self._get_random_coef()
            self.move(step)
        else:
            self.status = "бежит" 
            step = self.average_speed * self._get_random_coef()
            self.move(step)


class Rabbit(Animal):
    def __init__(self, name: str, hop_speed: float):
        super().__init__(name)
        self.hop_speed = hop_speed
        self.status = "отдыхает"

    def get_species(self) -> str:
        return "кролик"

    def start_race(self):
        super().start_race()
        self.status = "отдыхает"

    def get_status(self) -> str:
        return self.status

    def go(self):
        if self.status == "отдыхает":
            if random() < 0.65:
                self.status = "прыгает"
        else:
            if random() < 0.25:
                self.status = "отдыхает"
        if self.status == "прыгает":
            self.move(self.hop_speed * self._get_random_coef() * 1.4)


class Turtle(Animal):
    def __init__(self, name: str, base_speed: float):
        super().__init__(name)
        self.base_speed = base_speed
        self.status = "ползёт"

    def get_species(self) -> str:
        return "черепаха"

    def start_race(self):
        super().start_race()
        self.status = "ползёт"

    def get_status(self) -> str:
        return self.status

    def go(self):
        if self.status == "ползёт":
            if random() < 0.08:
                self.status = "прячется в панцирь"
        else:
            if random() < 0.4:
                self.status = "ползёт"
        
        if self.status == "ползёт":
            self.move(self.base_speed * self._get_random_coef(a=0.05))


class Kangaroo(Animal):
    def __init__(self, name: str, base_jump_speed: float, max_momentum: float = 0.0):
        super().__init__(name)
        self.base_jump_speed = base_jump_speed
        self.max_momentum = max_momentum if max_momentum else base_jump_speed * 2.
        self.momentum = 0.0
        self.status = "готовится к прыжку"

    def get_species(self) -> str:
        return "кенгуру"

    def start_race(self):
        super().start_race()
        self.momentum = 0.0
        self.status = "готовится к прыжку"

    def get_status(self) -> str:
        return self.status

    def go(self):
        if random() < 0.2:  # Вероятность сброса инерции
            self.momentum = 0.0
            self.status = "споткнулся, теряет инерцию"
            return
        if self.status == "споткнулся, теряет инерцию":
            self.status = "готовится к прыжку"
        else:
            self.status = "прыгает"
        self.momentum += self.base_jump_speed * 0.4
        self.move(min(self.momentum + self.base_jump_speed, self.max_momentum) * self._get_random_coef(a=0.15))


from typing import List
from rich.console import Console
from rich.table import Table

class Race:
    def __init__(self, animals: List[Animal], distance: float = 200.0):
        self.animals = animals
        self.distance = distance
        self.console = Console()
        self.winners: List[Animal] = []

    def _on_move(self, animal: Animal, step: float):
        print(f"{animal.get_species()} {animal.name} {animal.get_status()}, продвинулся на {step:.2f} метров")

    def _setup(self):
        for animal in self.animals:
            animal.start_race()
            animal.set_move_callback(self._on_move)

    def print_status(self):
        table = Table(title=f"Гонка (дистанция: {self.distance:.1f} м)")
        table.add_column("Имя", style="cyan")
        table.add_column("Вид", style="blue")
        table.add_column("Состояние", style="magenta")
        table.add_column("Положение", style="yellow", justify="center")
        for animal in self.animals:
            table.add_row(
                animal.name,
                animal.get_species(),
                animal.get_status(),
                f"{animal.pos:.2f}"
            )
        self.console.print(table)

    def run(self) -> Animal:
        self._setup()
        self.print_status()

        ticks = 0
        while ticks < 2000:
            ticks += 1
            for animal in self.animals:
                animal.go()
                if animal.pos >= self.distance:
                    self.print_status()
                    return animal

            self.print_status()

        if not self.winners:
            self.console.print("Гонка завершена по лимиту тактов. Победителей нет")


if __name__ == "__main__":
    participants: List[Animal] = [
        Horse("Буцефал", 23.5),
        Horse("Пегас", 27.9),
        Cheetah("Гром", 18.0, 46.5),
        Cheetah("Флэш", 15.5, 69.2),
        Rabbit("Зайка", 17.5),
        Rabbit("Крош", 19.0),
        Turtle("Тортилла", 2.8),
        Turtle("Панцирь", 3.1),
        Kangaroo("Скачок", 19.5),
        Kangaroo("Рыжий", 23.0)
    ]

    race = Race(animals=participants, distance=200.0)
    winner = race.run()
    print(f"{winner.get_species().capitalize()} {winner.name} победил(а)!!!")
