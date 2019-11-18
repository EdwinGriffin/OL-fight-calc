class Character:

    def __init__(self):
        pass

    def attack(self, target):
        pass

    def defend(self, attack, target):
        pass

    def buff(self, target):
        pass

    def debuff(self, target):
        pass

    def update(self, players, enemies):
        return 'TODO'

    def __str__(self):
        output = self.name + ", a level " + str(self.level) + " " + self.role + " has:\n" \
            "Initiative Stat: " + str(self.init) + "\n" \
            "Offensive Stat: " + str(self.offensive) + "\n" \
            "Defensive Stat: " + str(self.defensive) + "\n" \
            "Buffing Stat: " + str(self.buff) + "\n" \
            "Debuffing Stat: " + str(self.debuff) + "\n" \
            "Max Hit Points: " + str(self.max_hp) + "\n" \
            "Current Hit Points: " + str(self.current_hp) + "\n" \
            "Guard: " + str(self.guard) + "\n" \
            "Resolve: " + str(self.resolve) + "\n" \
            "Role Bonus: " + str(self.bonus) + "\n" \
            "-----------------------------------"
        return output

class Player(Character):
    
    def __init__(self, name, level, role, init, offensive, defensive, buff, debuff, hp, guard, resolve, bonus):
        self.name = name
        self.level = level
        self.role = role
        self.init = init
        self.offensive = offensive
        self.defensive = defensive
        self.buff = buff
        self.debuff = debuff
        self.max_hp = hp
        self.current_hp = hp
        self.guard = guard
        self.resolve = resolve
        self.bonus = bonus
        self.has_allies = False

class NPC(Character):
    
    def __init__(self, name, level, role):
        self.name = name
        self.level = level
        self.role = role
        self.primary = int(4 + (self.level * 0.5))
        self.secondary = int(2.5 + (self.level * 0.5))
        self.max_hp = int(14 + (self.level * 2))
        self.current_hp = int(14 + (self.level * 2))
        self.guard = int(12 + self.level)
        self.bonus = 1
        self.has_allies = False

        if self.role == 1:
            self.role = 'attacker'
            self.init = self.primary
            self.offensive = self.primary
            self.defensive = self.primary
            self.buff = self.secondary
            self.debuff = self.secondary
            self.resolve = int(self.guard * 0.75)
        if self.role == 2:
            self.role = 'buffer'
            self.init = self.secondary
            self.offensive = self.secondary
            self.defensive = self.primary
            self.buff = self.primary
            self.debuff = self.secondary
            self.resolve = int(self.guard * 0.9)
        if self.role == 3:
            self.role = 'debuffer'
            self.init = self.secondary
            self.offensive = self.primary
            self.defensive = self.secondary
            self.buff = self.secondary
            self.debuff = self.primary
            self.resolve = self.guard