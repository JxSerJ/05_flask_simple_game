from __future__ import annotations

from abc import ABC, abstractmethod
from random import randint
from typing import Optional

from classes import UnitClass
from equipment import Weapon, Armor


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        damage = self.weapon.damage * self.unit_class.attack
        if target.stamina_points >= target.armor.stamina_per_turn:
            defence = target.armor.defence
        else:
            defence = target.armor.defence

        if damage > defence:
            result_damage = damage - defence
        else:
            result_damage = 0

        return result_damage

    def get_damage(self, damage: float) -> Optional[float]:
        self.hp -= damage
        return self.health_points

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        if self._is_skill_used:
            return 'Навык уже использован.'
        return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:

        if self.stamina_points >= self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
            target.get_damage(damage)

            self.stamina -= self.weapon.stamina_per_hit
            target.stamina -= target.armor.stamina_per_turn

            if target.stamina_points < 0:
                target.stamina = 0

            if damage > 0:
                return f"{self.name} используя {self.weapon.name} пробивает " \
                       f"{target.armor.name} соперника и наносит {damage} урона."
            return f"{self.name} используя {self.weapon.name} наносит удар, но " \
                   f"{target.armor.name} cоперника его останавливает."
        return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if not self._is_skill_used:
            skill_usage_chance = randint(0, 100)
            if skill_usage_chance > 70:
                return self.use_skill(target)

        if self.stamina_points >= self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
            target.get_damage(damage)

            self.stamina -= self.weapon.stamina_per_hit
            target.stamina -= target.armor.stamina_per_turn

            if target.stamina_points < 0:
                target.stamina = 0

            if damage > 0:
                return f"{self.name} используя {self.weapon.name} пробивает " \
                       f"{target.armor.name} соперника и наносит {damage} урона."
            return f"{self.name} используя {self.weapon.name} наносит удар, но " \
                   f"{target.armor.name} cоперника его останавливает."
        return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
