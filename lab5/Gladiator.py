from typing import Dict, List, Optional

class Component:
    pass

class Gladiator:
    def __init__(self):
        # Гладиатор - это просто набор Конечностей
        
        
    def is_active(self) -> bool:
        if self.limbs["head"].hp <= 0 or self.limbs["torso"].hp <= 0:
            return False
        broken_limbs = sum(1 for name in ["left_hand", "right_hand", "left_leg", "right_leg"] 
                           if self.limbs[name].hp <= 0)
        return broken_limbs < 2
