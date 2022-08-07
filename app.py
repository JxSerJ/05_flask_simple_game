from flask import Flask, render_template, request, redirect, url_for

from base import Arena
from classes import unit_classes
from equipment import Equipment, Weapon, Armor
from unit import BaseUnit, PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()
equipment = Equipment()


@app.route("/")
def menu_page():
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template('fight.html', heroes=heroes, result=result)
    return render_template('fight.html', heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
        return render_template('fight.html', heroes=heroes, result=result)
    return render_template('fight.html', heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
        return render_template('fight.html', heroes=heroes, result=result)
    return render_template('fight.html', heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    # TODO кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    if request.method == "GET":
        page_data = {"header": "Выбор игрока",
                     "classes": unit_classes,
                     "weapons": equipment.get_weapons_names(),
                     "armors": equipment.get_armors_names()}

        return render_template('hero_choosing.html', result=page_data)

    if request.method == "POST":
        user_name = request.form.get('name')
        unit_class = unit_classes[request.form.get('unit_class')]
        weapon: Weapon = equipment.get_weapon(request.form.get('weapon'))
        armor: Armor = equipment.get_armor(request.form.get('armor'))

        player = PlayerUnit(name=user_name, unit_class=unit_class)
        player.equip_weapon(weapon)
        player.equip_armor(armor)

        heroes['player'] = player

        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == "GET":
        page_data = {"header": "Выбор противника",
                     "classes": unit_classes,
                     "weapons": equipment.get_weapons_names(),
                     "armors": equipment.get_armors_names()}

        return render_template('hero_choosing.html', result=page_data)

    if request.method == "POST":
        user_name = request.form.get('name')
        unit_class = unit_classes[request.form.get('unit_class')]
        weapon: Weapon = equipment.get_weapon(request.form.get('weapon'))
        armor: Armor = equipment.get_armor(request.form.get('armor'))

        enemy = EnemyUnit(name=user_name, unit_class=unit_class)
        enemy.equip_weapon(weapon)
        enemy.equip_armor(armor)

        heroes['enemy'] = enemy

        return redirect(url_for('start_fight', _external=True))


if __name__ == "__main__":
    app.run(debug=True)
