from warrior import *
from headquarter import Headquarter


class City:
    def __init__(self, idx):
        self.idx = idx
        self.life = 0
        self.flag = None
        self.red = None
        self.blue = None
        self.lastWin = None
        self.winStreak = 0
        self.units = []


    def collect(self, game, minute_tag):
        if self.life <= 0:
            return
        if self.red and not self.blue:
            game.hqR.life += self.life
            print(f"{game.hour:03d}:{minute_tag:02d} red {self.red.type} {self.red.id} earned {self.life} elements for his headquarter")
            self.life = 0
        elif self.blue and not self.red:
            game.hqB.life += self.life
            print(f"{game.hour:03d}:{minute_tag:02d} blue {self.blue.type} {self.blue.id} earned {self.life} elements for his headquarter")
            self.life = 0

    def useBomb(self, game):
        if not (self.red and self.blue):
            return
        firstRed = (self.flag == 'red') or (self.flag is None and self.idx % 2 == 1)
        attacker = self.red if firstRed else self.blue
        defender = self.blue if firstRed else self.red
        
        atkSword = 0
        if hasattr(attacker, 'swordPower'):
            atkSword = attacker.swordPower
            
        defSword = 0
        if hasattr(defender, 'swordPower'):
            defSword = defender.swordPower
        defenderWillDie = defender.willDie(attacker.attack, atkSword)
        attackerWillDie = False
        if not defenderWillDie and defender.type != 'ninja':
            attackerWillDie = attacker.willDie(defender.attack // 2, defSword)
        defender_has_bomb = False
        if hasattr(defender, 'bomb'):
            defender_has_bomb = defender.bomb > 0
        elif hasattr(defender, 'weapons'):
            defender_has_bomb = 'bomb' in defender.weapons
        
        if defenderWillDie and defender_has_bomb:
            if hasattr(defender, 'bomb') and defender.bomb > 0:
                defender.bomb -= 1
            elif hasattr(defender, 'weapons') and 'bomb' in defender.weapons:
                defender.weapons.remove('bomb')
            if firstRed:
                print(f"{game.hour:03d}:38 blue {defender.type} {defender.id} used a bomb and killed red {attacker.type} {attacker.id}")
            else:
                print(f"{game.hour:03d}:38 red {defender.type} {defender.id} used a bomb and killed blue {attacker.type} {attacker.id}")
            if self.red:
                self.red.alive = False
            if self.blue:
                self.blue.alive = False
            self.red = None
            self.blue = None
            self.units = []
            if self.red:
                self.units.append(self.red)
            if self.blue:
                self.units.append(self.blue)
            return
        attacker_has_bomb = False
        if hasattr(attacker, 'bomb'):
            attacker_has_bomb = attacker.bomb > 0
        elif hasattr(attacker, 'weapons'):
            attacker_has_bomb = 'bomb' in attacker.weapons
        
        if attackerWillDie and attacker_has_bomb:
            if hasattr(attacker, 'bomb') and attacker.bomb > 0:
                attacker.bomb -= 1
            elif hasattr(attacker, 'weapons') and 'bomb' in attacker.weapons:
                attacker.weapons.remove('bomb')
            if firstRed:
                print(f"{game.hour:03d}:38 red {attacker.type} {attacker.id} used a bomb and killed blue {defender.type} {defender.id}")
            else:
                print(f"{game.hour:03d}:38 blue {attacker.type} {attacker.id} used a bomb and killed red {defender.type} {defender.id}")
            if self.red:
                self.red.alive = False
            if self.blue:
                self.blue.alive = False
            self.red = None
            self.blue = None
            self.units = []
            if self.red:
                self.units.append(self.red)
            if self.blue:
                self.units.append(self.blue)

    def battle(self, game, redWinners, blueWinners):
        if not (self.red and self.blue):
            return
        firstRed = (self.flag == 'red') or (self.flag is None and self.idx % 2 == 1)
        attacker = self.red if firstRed else self.blue
        defender = self.blue if firstRed else self.red
        atkColor = 'red' if firstRed else 'blue'
        defColor = 'blue' if firstRed else 'red'
        redLion = self.red if self.red and self.red.type == 'lion' else None
        blueLion = self.blue if self.blue and self.blue.type == 'lion' else None
        preDefHp = defender.hp
        print(f"{game.hour:03d}:40 {atkColor} {attacker.type} {attacker.id} attacked {defColor} {defender.type} {defender.id} in city {self.idx} with {attacker.hp} elements and force {attacker.attack}")
        atkSword = 0
        if hasattr(attacker, 'swordPower'):
            atkSword = attacker.swordPower
        totalAtk = attacker.attack + atkSword
        defender.hp -= totalAtk
        if atkSword > 0:
            attacker.swordPower = int(atkSword * 0.8)
        if defender.hp <= 0:
            print(f"{game.hour:03d}:40 {defColor} {defender.type} {defender.id} was killed in city {self.idx}")
            if attacker.type == 'wolf':
                attacker.weapons.extend(defender.weapons)
                if hasattr(defender, 'arrows'):
                    attacker.arrows += defender.arrows
                if hasattr(defender, 'bomb'):
                    attacker.bomb += defender.bomb
                if hasattr(defender, 'sword'):
                    attacker.sword += defender.sword
                if hasattr(defender, 'swordPower'):
                    attacker.swordPower = max(attacker.swordPower, defender.swordPower)
            if defender.type == 'lion':
                attacker.hp += preDefHp
            if firstRed:
                if self.blue:
                    self.blue.alive = False
                self.blue = None
                redWinners.append((self.idx, attacker))
                if game.hqR.life >= 8:
                    game.hqR.life -= 8
                    attacker.hp += 8
            else:
                if self.red:
                    self.red.alive = False
                self.red = None
                blueWinners.append((self.idx, attacker))
                if game.hqB.life >= 8:
                    game.hqB.life -= 8
                    attacker.hp += 8
            if self.lastWin == atkColor:
                self.winStreak += 1
            else:
                self.lastWin = atkColor
                self.winStreak = 1
            if self.winStreak >= 2 and self.flag != atkColor:
                self.flag = atkColor
                print(f"{game.hour:03d}:40 {atkColor} flag raised in city {self.idx}")
            if attacker.type == 'dragon':
                attacker.morale = (attacker.morale or 0) + 0.2
                if attacker.morale > 0.8:
                    print(f"{game.hour:03d}:40 {atkColor} dragon {attacker.id} yelled in city {self.idx}")
            self.units = []
            if self.red:
                self.units.append(self.red)
            if self.blue:
                self.units.append(self.blue)
            return
        if defender.type != 'ninja':
            print(f"{game.hour:03d}:40 {defColor} {defender.type} {defender.id} fought back against {atkColor} {attacker.type} {attacker.id} in city {self.idx}")
            defSword = 0
            if hasattr(defender, 'swordPower'):
                defSword = defender.swordPower
            counter = defender.attack // 2 + defSword
            attacker.hp -= counter
            if defSword > 0:
                defender.swordPower = int(defSword * 0.8)
            if attacker.hp <= 0:
                print(f"{game.hour:03d}:40 {atkColor} {attacker.type} {attacker.id} was killed in city {self.idx}")
                if defender.type == 'wolf':
                    defender.weapons.extend(attacker.weapons)
                    if hasattr(attacker, 'arrows'):
                        defender.arrows += attacker.arrows
                    if hasattr(attacker, 'bomb'):
                        defender.bomb += attacker.bomb
                    if hasattr(attacker, 'sword'):
                        defender.sword += attacker.sword
                    if hasattr(attacker, 'swordPower'):
                        defender.swordPower = max(defender.swordPower, attacker.swordPower)
                if attacker.type == 'lion':
                    defender.hp += attacker.hp + (attacker.attack - (defender.attack // 2))
                if firstRed:
                    if self.red:
                        self.red.alive = False
                    self.red = None
                    blueWinners.append((self.idx, defender))
                    if game.hqB.life >= 8:
                        game.hqB.life -= 8
                        defender.hp += 8
                else:
                    if self.blue:
                        self.blue.alive = False
                    self.blue = None
                    redWinners.append((self.idx, defender))
                    if game.hqR.life >= 8:
                        game.hqR.life -= 8
                        defender.hp += 8
                winCol = defColor
                if self.lastWin == winCol:
                    self.winStreak += 1
                else:
                    self.lastWin = winCol
                    self.winStreak = 1
                if self.winStreak >= 2 and self.flag != winCol:
                    self.flag = winCol
                    print(f"{game.hour:03d}:40 {winCol} flag raised in city {self.idx}")
                if defender.type == 'dragon':
                    defender.morale = (defender.morale or 0) + 0.2
                    if defender.morale > 0.8:
                        print(f"{game.hour:03d}:40 {defColor} dragon {defender.id} yelled in city {self.idx}")
            else:
                if attacker.type == 'dragon':
                    attacker.morale = max(0.0, (attacker.morale or 0) - 0.2)
                if defender.type == 'dragon':
                    defender.morale = max(0.0, (defender.morale or 0) - 0.2)
        if redLion and (not redWinners or redWinners[-1][0] != self.idx):
            redLion.loyalty = max(0, redLion.loyalty - game.k)
        if blueLion and (not blueWinners or blueWinners[-1][0] != self.idx):
            blueLion.loyalty = max(0, blueLion.loyalty - game.k)
        self.units = []
        if self.red:
            self.units.append(self.red)
        if self.blue:
            self.units.append(self.blue)

class game:
    def __init__(self, life, strengths, n=0, r=0, k=0, t=0, attacks=None):
        self.life = life
        self.strengths = strengths
        self.n = n
        self.r = r
        self.k = k
        self.t = t
        self.end = False
        self.hour = 0
        self.minute = 0
        self.hqR = Headquarter('red', life, strengths, r, attacks)
        self.hqB = Headquarter('blue', life, strengths, r, attacks)
        self.cities = [City(i) for i in range(1, n + 1)] if n else []
        self.locR = []
        self.locB = []
        self.pendingRewards = []

    def produce(self):
        r = self.hqR.produce(self.hour)
        b = self.hqB.produce(self.hour)
        if r:
            print(r)
            if self.hqR.warriors:
                w = self.hqR.warriors[-1]
                self.locR.append([w, 0])
        if b:
            print(b)
            if self.hqB.warriors:
                w = self.hqB.warriors[-1]
                self.locB.append([w, self.n + 1 if self.n else 0])

    def lionEcsape(self):
        for idx, c in enumerate(self.cities, start=1):
            if c.red and c.red.type == 'lion':
                loyalty = 1
                if hasattr(c.red, 'loyalty'):
                    loyalty = c.red.loyalty
                if loyalty <= 0:
                    print(f"{self.hour:03d}:05 red lion {c.red.id} ran away")
                    c.red = None
            if c.blue and c.blue.type == 'lion':
                loyalty = 1
                if hasattr(c.blue, 'loyalty'):
                    loyalty = c.blue.loyalty
                if loyalty <= 0:
                    print(f"{self.hour:03d}:05 blue lion {c.blue.id} ran away")
                    c.blue = None

    def march(self):
        if not self.cities:
            return
        for c in self.cities:
            c.red = None
            c.blue = None
        filtered_locR = []
        for w, pos in self.locR:
            alive = True
            if hasattr(w, 'alive'):
                alive = w.alive
            if alive and w.hp > 0:
                filtered_locR.append([w, pos])
        self.locR = filtered_locR
        
        filtered_locB = []
        for w, pos in self.locB:
            alive = True
            if hasattr(w, 'alive'):
                alive = w.alive
            if alive and w.hp > 0:
                filtered_locB.append([w, pos])
        self.locB = filtered_locB
        blueArrivals = 0
        redArrivals = 0
        for item in self.locR:
            w, pos = item
            if pos == self.n + 1:
                continue
            newPos = pos + 1
            item[1] = newPos
            if w.type == 'iceman':
                steps = 1
                if hasattr(w, 'steps'):
                    steps = w.steps + 1
                w.steps = steps
                if steps % 2 == 0:
                    w.hp = max(1, w.hp - 9)
                    w.attack += 20
            if newPos == self.n + 1:
                elems = max(0, w.hp)
                print(f"{self.hour:03d}:10 red {w.type} {w.id} reached blue headquarter with {elems} elements and force {w.attack}")
                redArrivals += 1
                item[1] = self.n + 1
            elif 1 <= newPos <= self.n:
                elems = max(0, w.hp)
                print(f"{self.hour:03d}:10 red {w.type} {w.id} marched to city {newPos} with {elems} elements and force {w.attack}")
        for item in self.locB:
            w, pos = item
            if pos == 0:
                continue
            newPos = pos - 1
            item[1] = newPos
            if w.type == 'iceman':
                steps = 1
                if hasattr(w, 'steps'):
                    steps = w.steps + 1
                w.steps = steps
                if steps % 2 == 0:
                    w.hp = max(1, w.hp - 9)
                    w.attack += 20
            if newPos == 0:
                elems = max(0, w.hp)
                print(f"{self.hour:03d}:10 blue {w.type} {w.id} reached red headquarter with {elems} elements and force {w.attack}")
                blueArrivals += 1
                item[1] = 0
            elif 1 <= newPos <= self.n:
                elems = max(0, w.hp)
                print(f"{self.hour:03d}:10 blue {w.type} {w.id} marched to city {newPos} with {elems} elements and force {w.attack}")
        for w, pos in self.locR:
            if 1 <= pos <= self.n:
                self.cities[pos - 1].red = w
        for w, pos in self.locB:
            if 1 <= pos <= self.n:
                self.cities[pos - 1].blue = w
        for c in self.cities:
            c.units = []
            if c.red:
                c.units.append(c.red)
            if c.blue:
                c.units.append(c.blue)
        redInBlue = sum(1 for _, pos in self.locR if pos == self.n + 1)
        blueInRed = sum(1 for _, pos in self.locB if pos == 0)
        if redInBlue >= 2 and not self.end:
            print(f"{self.hour:03d}:10 blue headquarter was taken")
            self.end = True
        if blueInRed >= 2 and not self.end:
            print(f"{self.hour:03d}:10 red headquarter was taken")
            self.end = True

    def produceLife(self):
        for c in self.cities:
            c.life += 10

    def collect(self):
        for c in self.cities:
            c.collect(self, 30)

    def shoot(self):
        if not self.cities:
            return
        for i, c in enumerate(self.cities[:-1]):
            if c.red:
                arrows = 0
                if hasattr(c.red, 'arrows'):
                    arrows = c.red.arrows
                if arrows > 0:
                    nxt = self.cities[i + 1]
                    if nxt.blue:
                        c.red.arrows -= 1
                        nxt.blue.hp -= c.red.arrowPower
                        killed = nxt.blue.hp <= 0
                        if killed:
                            print(f"{self.hour:03d}:35 red {c.red.type} {c.red.id} shot and killed blue {nxt.blue.type} {nxt.blue.id}")
                            self.pendingRewards.append(('red', i + 1, c.red))
                            nxt.blue = None
                        else:
                            print(f"{self.hour:03d}:35 red {c.red.type} {c.red.id} shot")
        for i in range(1, len(self.cities)):
            c = self.cities[i]
            if c.blue:
                arrows = 0
                if hasattr(c.blue, 'arrows'):
                    arrows = c.blue.arrows
                if arrows > 0:
                    prev = self.cities[i - 1]
                    if prev.red:
                        c.blue.arrows -= 1
                        prev.red.hp -= c.blue.arrowPower
                        killed = prev.red.hp <= 0
                        if killed:
                            print(f"{self.hour:03d}:35 blue {c.blue.type} {c.blue.id} shot and killed red {prev.red.type} {prev.red.id}")
                            self.pendingRewards.append(('blue', i - 1 + 1, c.blue))
                            prev.red = None
                        else:
                            print(f"{self.hour:03d}:35 blue {c.blue.type} {c.blue.id} shot")

    def useBomb(self):
        if not self.cities:
            return
        for c in self.cities:
            c.useBomb(self)

    def battle(self):
        if not self.cities:
            return
        if self.pendingRewards:
            reds = [(idx, w) for (col, idx, w) in self.pendingRewards if col == 'red']
            blues = [(idx, w) for (col, idx, w) in self.pendingRewards if col == 'blue']
            for idx, w in sorted(reds, key=lambda x: -x[0]):
                if self.hqR.life >= 8:
                    self.hqR.life -= 8
                    w.hp += 8
            for idx, w in sorted(blues, key=lambda x: x[0]):
                if self.hqB.life >= 8:
                    self.hqB.life -= 8
                    w.hp += 8
            self.pendingRewards.clear()
        redWinners = []
        blueWinners = []
        for c in self.cities:
            c.battle(self, redWinners, blueWinners)
        for c in self.cities:
            c.collect(self, 40)

    def reportLife(self):
        print(f"{self.hour:03d}:50 {self.hqR.life} elements in red headquarter")
        print(f"{self.hour:03d}:50 {self.hqB.life} elements in blue headquarter")

    def reportWeapons(self):
        for w in sorted(self.hqR.warriors, key=lambda x: -x.id):
            items = []
            arrows = 0
            if hasattr(w, 'arrows'):
                arrows = w.arrows
            if arrows > 0:
                items.append(f"arrow({arrows})")
                
            bomb = 0
            if hasattr(w, 'bomb'):
                bomb = w.bomb
            if bomb > 0:
                items.append('bomb')
                
            sword = 0
            if hasattr(w, 'sword'):
                sword = w.sword
            swordPower = 0
            if hasattr(w, 'swordPower'):
                swordPower = w.swordPower
            if sword > 0 or swordPower > 0:
                items.append(f"sword({swordPower})")
            weapons = ','.join(items) if items else 'no weapon'
            print(f"{self.hour:03d}:55 red {w.type} {w.id} has {weapons}")
            
        for w in sorted(self.hqB.warriors, key=lambda x: x.id):
            items = []
            arrows = 0
            if hasattr(w, 'arrows'):
                arrows = w.arrows
            if arrows > 0:
                items.append(f"arrow({arrows})")
                
            bomb = 0
            if hasattr(w, 'bomb'):
                bomb = w.bomb
            if bomb > 0:
                items.append('bomb')
                
            sword = 0
            if hasattr(w, 'sword'):
                sword = w.sword
            swordPower = 0
            if hasattr(w, 'swordPower'):
                swordPower = w.swordPower
            if sword > 0 or swordPower > 0:
                items.append(f"sword({swordPower})")
            weapons = ','.join(items) if items else 'no weapon'
            print(f"{self.hour:03d}:55 blue {w.type} {w.id} has {weapons}")

