# Package shim that re-exports base Equipment classes from the top-level modules
import importlib.util
import os

_here = os.path.dirname(__file__)
_spec = importlib.util.spec_from_file_location("_equipments_module", os.path.join(_here, "..", "equipments.py"))
_equip_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_equip_mod)

# Re-export base classes
Equipment = _equip_mod.Equipment
MissArmor = _equip_mod.MissArmor
PhysicalArmor = _equip_mod.PhysicalArmor
FireWard = _equip_mod.FireWard
EvasiveGear = _equip_mod.EvasiveGear
ParryArmor = _equip_mod.ParryArmor

__all__ = ["Equipment", "MissArmor", "PhysicalArmor", "FireWard", "EvasiveGear", "ParryArmor"]
