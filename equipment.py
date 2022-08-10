import json
from dataclasses import dataclass
from typing import List, Generic

import marshmallow
import marshmallow_dataclass

from random import uniform


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float
    pass


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return uniform(self.min_damage, self.max_damage)


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armor: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str):
        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                return weapon

    def get_armor(self, armor_name: str):
        for armor in self.equipment.armor:
            if armor.name == armor_name:
                return armor

    def get_weapons_names(self) -> list:
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list:
        return [armor.name for armor in self.equipment.armor]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        weapon_schema = marshmallow_dataclass.class_schema(Weapon)
        armor_schema = marshmallow_dataclass.class_schema(Armor)
        with open('./data/equipment.json', mode='r', encoding='utf-8') as file:
            equipment_data = json.load(file)
        try:
            return EquipmentData(weapons=weapon_schema(many=True).load(equipment_data['weapons']),
                                 armor=armor_schema(many=True).load(equipment_data['armors']))
        except marshmallow.exceptions.ValidationError:
            raise ValueError
