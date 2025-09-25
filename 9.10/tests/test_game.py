import os
import sys

# 将 9.10 目录加入到 sys.path，便于 `from games.game import ...`
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_SUBDIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_SUBDIR not in sys.path:
    sys.path.insert(0, PROJECT_SUBDIR)

from games.game import Headquarter


def test_produce_stop():
    hqR = Headquarter("red", life=0, strengths={"dragon": 1, "ninja": 1, "iceman": 1, "lion": 1, "wolf": 1})
    msg = hqR.produce(0)
    assert msg == "000 red headquarter stops making warriors"
    assert hqR.stopped is True


def test_output():
    strengths = {"dragon": 3, "ninja": 4, "iceman": 5, "lion": 6, "wolf": 7}
    hqR = Headquarter("red", life=20, strengths=strengths)
    hqB = Headquarter("blue", life=20, strengths=strengths)
    hour = 0
    msg = ""
    while not (hqR.stopped and hqB.stopped):
        r = hqR.produce(hour)
        if r:
            msg = msg + r + "\n"
        b = hqB.produce(hour)
        if b:
            msg = msg + b + "\n"
        hour += 1
    expected = (
        "000 red iceman 1 born with strength 5,1 iceman in red headquarter\n"
        "It has a bomb\n"
        "000 blue lion 1 born with strength 6,1 lion in blue headquarter\n"
        "It's loyalty is 14\n"
        "001 red lion 2 born with strength 6,1 lion in red headquarter\n"
        "It's loyalty is 9\n"
        "001 blue dragon 2 born with strength 3,1 dragon in blue headquarter\n"
        "It has a arrow,and it's morale is 3.67\n"
        "002 red wolf 3 born with strength 7,1 wolf in red headquarter\n"
        "002 blue ninja 3 born with strength 4,1 ninja in blue headquarter\n"
        "It has a sword and a bomb\n"
        "003 red headquarter stops making warriors\n"
        "003 blue iceman 4 born with strength 5,1 iceman in blue headquarter\n"
        "It has a bomb\n"
        "004 blue headquarter stops making warriors\n"
    )
    assert msg == expected
    
    assert hqR.color == "red"
    assert hqR.life == 2  
    assert hqR.order == ['iceman', 'lion', 'wolf', 'ninja', 'dragon']
    assert hqR.idx == 3
    assert hqR.id == 4
    assert hqR.stopped == True

    assert hqB.color == "blue"
    assert hqB.life == 2 
    assert hqB.order == ['lion', 'dragon', 'ninja', 'iceman', 'wolf']
    assert hqB.idx == 4
    assert hqB.id == 5
    assert hqB.stopped == True



def test_init():
    hqR = Headquarter("red", 20, {"dragon": 10, "ninja": 10, "iceman": 10, "lion": 10, "wolf": 10})
    assert hqR.color == "red"
    assert hqR.life == 20
    assert hqR.order == ['iceman', 'lion', 'wolf', 'ninja', 'dragon']
    assert hqR.idx == 0
    assert hqR.id == 1
    assert hqR.stopped == False
    
    hqB = Headquarter("blue", 50, {"dragon": 5, "ninja": 5, "iceman": 5, "lion": 5, "wolf": 5})
    assert hqB.color == "blue"
    assert hqB.life == 50
    assert hqB.order == ['lion', 'dragon', 'ninja', 'iceman', 'wolf']
    assert hqB.idx == 0
    assert hqB.id == 1
    assert hqB.stopped == False


def test_morale():
    hq = Headquarter("red", 20, {"dragon": 10, "ninja": 10, "iceman": 10, "lion": 10, "wolf": 10})
    hq.idx = 4  
    msg = hq.produce(0)
    assert "morale is 1.00" in msg  


def testProduceDragonMoraleZeroCost():

    hq = Headquarter("red", 10, {"dragon": 0, "ninja": 10, "iceman": 10, "lion": 10, "wolf": 10})
    hq.idx = 4  
    msg = hq.produce(0)
    assert "morale is 0.00" in msg 

