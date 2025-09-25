class Warrior:
    def __init__(self, color, warriorType, id, strength):
        self.color = color
        self.type = warriorType
        self.id = id
        self.strength = strength
        self.weapons = []
        self.morale = None
        self.loyalty = None
        # 武器与战斗数值
        self.arrows = 0      # 剩余箭次数
        self.bomb = 0
        self.sword = 0
        self.arrowPower = 0  # R 值
        self.swordPower = 0  # 当前剑威力
        self.attack = strength
        self.hp = strength

    def damage(self, amount):
        # 统一伤害入口（不处理剑衰减等，该逻辑位于战斗流程）
        if amount <= 0:
            return 0
        self.hp -= amount
        return amount

    def willDie(self, incoming_damage, sword_power=0):
        # 预测承受伤害后是否死亡（<=0 视为死亡）
        # 考虑 swordPower 的影响
        total_damage = max(0, incoming_damage + sword_power)
        return self.hp - total_damage <= 0


class Lion(Warrior):
    def __init__(self, color, id, strength, loyalty):
        super().__init__(color, 'lion', id, strength)
        self.loyalty = loyalty


class Dragon(Warrior):
    def __init__(self, color, id, strength, morale, weapon):
        super().__init__(color, 'dragon', id, strength)
        self.morale = morale
        if weapon:
            self.weapons.append(weapon)


class Ninja(Warrior):
    def __init__(self, color, id, strength, weapon1, weapon2):
        super().__init__(color, 'ninja', id, strength)
        if weapon1:
            self.weapons.append(weapon1)
        if weapon2:
            self.weapons.append(weapon2)


class Iceman(Warrior):
    def __init__(self, color, id, strength, weapon):
        super().__init__(color, 'iceman', id, strength)
        if weapon:
            self.weapons.append(weapon)


class Wolf(Warrior):
    def __init__(self, color, id, strength):
        super().__init__(color, 'wolf', id, strength)


# weapon helpers
def weaponNameById(wid):
    if wid == 0:
        return 'sword'
    elif wid == 1:
        return 'bomb'
    elif wid == 2:
        return 'arrow'
    return None
