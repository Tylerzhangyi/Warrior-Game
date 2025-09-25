from warrior import *


class Headquarter:
    def __init__(self, color, life, strengths, arrowPower=0, attacks=None):
        self.color = color
        self.life = life
        self.strengths = strengths
        self.arrowPower = arrowPower
        self.attacks = attacks or {}
        if color == "red":
            self.order = ['iceman', 'lion', 'wolf', 'ninja', 'dragon']
        else:
            self.order = ['lion', 'dragon', 'ninja', 'iceman', 'wolf']
        self.idx = 0
        self.count = {t: 0 for t in ['dragon', 'ninja', 'iceman', 'lion', 'wolf']}
        self.id = 1
        self.stopped = False
        self.warriors = []

    def _fmt_time(self, hour):
        return f"{hour:03d}:00"

    def produce(self, hour):
        if self.stopped:
            return f"{self._fmt_time(hour)} {self.color} headquarter stops making warriors"
        tried = 0
        while tried < 5:
            wtype = self.order[self.idx]
            strength = self.strengths[wtype]
            if strength <= self.life:
                self.life -= strength
                wid = self.id
                self.id += 1
                self.count[wtype] += 1
                base = f"{self._fmt_time(hour)} {self.color} {wtype} {wid} born"
                extra = None
                if wtype == 'dragon':
                    weaponId = wid % 3
                    weapon = weaponNameById(weaponId)
                    morale = 0.0 if strength == 0 else self.life / strength
                    extra = f"Its morale is {morale:.2f}"
                    wobj = Dragon(self.color, wid, strength, morale, weapon)
                    # 初始化当前生命与攻击
                    wobj.attack = self.attacks.get('dragon', strength)
                    wobj.hp = strength
                    wobj.alive = True
                    if weapon == 'arrow':
                        wobj.arrows = 3
                        wobj.arrowPower = self.arrowPower
                    elif weapon == 'bomb':
                        wobj.bomb = 1
                    elif weapon == 'sword':
                        sword_power = int(wobj.attack * 0.2)
                        if sword_power > 0:
                            wobj.sword = 1
                            wobj.swordPower = sword_power
                    self.warriors.append(wobj)
                elif wtype == 'ninja':
                    w1 = weaponNameById(wid % 3)
                    w2 = weaponNameById((wid + 1) % 3)
                    extra = None
                    wobj = Ninja(self.color, wid, strength, w1, w2)
                    wobj.attack = self.attacks.get('ninja', strength)
                    wobj.hp = strength
                    wobj.alive = True
                    for ww in (w1, w2):
                        if ww == 'arrow':
                            wobj.arrows += 3
                            wobj.arrowPower = self.arrowPower
                        elif ww == 'bomb':
                            wobj.bomb += 1
                        elif ww == 'sword':
                            sword_power = int(wobj.attack * 0.2)
                            if sword_power > 0:
                                wobj.sword += 1
                                wobj.swordPower += sword_power
                    self.warriors.append(wobj)
                elif wtype == 'iceman':
                    weaponId = wid % 3
                    weapon = weaponNameById(weaponId)
                    extra = None
                    wobj = Iceman(self.color, wid, strength, weapon)
                    wobj.attack = self.attacks.get('iceman', strength)
                    wobj.hp = strength
                    wobj.alive = True
                    if weapon == 'arrow':
                        wobj.arrows = 3
                        wobj.arrowPower = self.arrowPower
                    elif weapon == 'bomb':
                        wobj.bomb = 1
                    elif weapon == 'sword':
                        sword_power = int(wobj.attack * 0.2)
                        if sword_power > 0:
                            wobj.sword = 1
                            wobj.swordPower = sword_power
                    self.warriors.append(wobj)
                elif wtype == 'lion':
                    extra = f"Its loyalty is {self.life}"
                    wobj = Lion(self.color, wid, strength, self.life)
                    wobj.attack = self.attacks.get('lion', strength)
                    wobj.hp = strength
                    wobj.alive = True
                    self.warriors.append(wobj)
                else:
                    wobj = Wolf(self.color, wid, strength)
                    wobj.attack = self.attacks.get('wolf', strength)
                    wobj.hp = strength
                    wobj.alive = True
                    self.warriors.append(wobj)
                self.idx = (self.idx + 1) % 5
                return base + ("\n" + extra if extra else "")
            self.idx = (self.idx + 1) % 5
            tried += 1
        self.stopped = True
        return f"{self._fmt_time(hour)} {self.color} headquarter stops making warriors"
