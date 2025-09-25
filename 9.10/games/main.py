from warrior import *
from game import *


first = input().strip()
tokens = first.split()
while len(tokens) < 5:
    tokens += input().split()
M, N, R, K, T = map(int, tokens[:5])
lifeVals = list(map(int, input().split()))
atkVals = list(map(int, input().split()))
strengths = {'dragon': lifeVals[0], 'ninja': lifeVals[1], 'iceman': lifeVals[2], 'lion': lifeVals[3], 'wolf': lifeVals[4]}
attacks = {'dragon': atkVals[0], 'ninja': atkVals[1], 'iceman': atkVals[2], 'lion': atkVals[3], 'wolf': atkVals[4]}

g = game(M, strengths, n=N, r=R, k=K, t=T, attacks=attacks)
hour = 0
minute = 0
while hour * 60 + minute <= T and not g.end:
    g.hour = hour
    g.minute = minute
    if minute == 0:
        g.produce()
    elif minute == 5:
        g.lionEcsape()
    elif minute == 10:
        g.march()
    elif minute == 20:
        g.produceLife()
    elif minute == 30:
        g.collect()
    elif minute == 35:
        g.shoot()
    elif minute == 38:
        g.useBomb()
    elif minute == 40:
        g.battle()
    elif minute == 50:
        g.reportLife()
    elif minute == 55:
        g.reportWeapons()
    minute += 1
    if minute == 60:
        minute = 0
        hour += 1

