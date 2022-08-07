from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player: BaseUnit = None
    enemy: BaseUnit = None
    game_is_running: bool = False

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        self.player: BaseUnit = player
        self.enemy: BaseUnit = enemy
        self.game_is_running: bool = True
        self.battle_result: str = None
        pass

    def _check_players_hp(self):
        if self.player.health_points > 0 and self.enemy.health_points > 0:
            pass
        if self.player.health_points <= 0 and self.enemy.health_points <= 0:
            self.battle_result = "Ничья!"
        if self.player.health_points <= 0 and self.enemy.health_points > 0:
            self.battle_result = f"Игрок {self.player.name} проиграл компьютеру {self.enemy.name}"
        if self.player.health_points > 0 and self.enemy.health_points <= 0:
            self.battle_result = f"Игрок {self.player.name} одержал победу над компьютером {self.enemy.name}"

    def _stamina_regeneration(self):
        self.player.stamina += self.STAMINA_PER_ROUND * self.player.unit_class.stamina
        self.enemy.stamina += self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina

        if self.player.stamina_points > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina
        if self.enemy.stamina_points > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina

    def next_turn(self):
        self._check_players_hp()
        if self.battle_result:
            return self.battle_result

        self._stamina_regeneration()
        result = self.enemy.hit(self.player)
        return result

    def _end_game(self):
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self):

        result = self.player.hit(self.enemy)
        result = result + ", " + self.next_turn()
        return result

    def player_use_skill(self):
        result = self.player.use_skill(self.enemy)
        result = result + ", " + self.next_turn()
        return result
