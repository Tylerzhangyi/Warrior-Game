import os
import sys

# 将 9.10 目录加入到 sys.path，便于 `from games.warrior import ...`
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_SUBDIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_SUBDIR not in sys.path:
    sys.path.insert(0, PROJECT_SUBDIR)

from games.warrior import *


def test_class():
    warrior = Warrior("test", 100, 1, "red")
    assert warrior.type == "test"
    assert warrior.health == 100
    assert warrior.id == 1
    assert warrior.color == "red"
    assert warrior.weapons == []
    assert warrior.morale is None
    assert warrior.loyalty is None


def test_repr():
    warrior = Warrior("dragon", 50, 2, "blue")
    expected = "blue dragon 2 born with strength 50"
    assert str(warrior) == expected


def test_lion():
    lion = Lion(80, 3, "red")
    assert lion.type == "lion"
    assert lion.health == 80
    assert lion.id == 3
    assert lion.color == "red"
    assert isinstance(lion, Warrior)


def test_dragon():
    dragon = Dragon(90, 4, "blue")
    assert dragon.type == "dragon"
    assert dragon.health == 90
    assert dragon.id == 4
    assert dragon.color == "blue"
    assert isinstance(dragon, Warrior)


def test_ninja():
    ninja = Ninja(70, 5, "red")
    assert ninja.type == "ninja"
    assert ninja.health == 70
    assert ninja.id == 5
    assert ninja.color == "red"
    assert isinstance(ninja, Warrior)


def test_iceman():
    iceman = Iceman(60, 6, "blue")
    assert iceman.type == "iceman"
    assert iceman.health == 60
    assert iceman.id == 6
    assert iceman.color == "blue"
    assert isinstance(iceman, Warrior)


def test_wolf():
    wolf = Wolf(75, 7, "red")
    assert wolf.type == "wolf"
    assert wolf.health == 75
    assert wolf.id == 7
    assert wolf.color == "red"
    assert isinstance(wolf, Warrior)


def test_id():
    warrior = Warrior("lion", 1, 0, "red")
    assert warrior.id == 0


def test_health():
    warrior = Warrior("lion", 0, 1, "blue")
    assert warrior.health == 0


def test_color():
    warrior = Warrior("lion", 50, 1, "")
    assert warrior.color == ""





