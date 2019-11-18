class Character:

    def __init__(self):
        pass

    def attack(self, allies, enemies):
        #Identify weakest enemy
        #Attack weakest enemy
        print(self.name, 'is an attacker')
        pass

    def defend(self, allies, enemies, origin, attack):
        #If the resolution of an attack action would bring a target below 0 hp, target will attempt a defend action
        print(self.name, 'is attempting a defend action against', origin.name, 'with an attack of', attack)
        self.interrupt = True
        pass

    def buff(self, allies, enemies):
        #Check if ally needs healing (<50%?)
        #Check if any allies are attackers or debuffers, buff if they are (prioritise attackers)
        #Attack if no allies are attackers or debuffers
        print(self.name, 'is a buffer')
        pass

    def debuff(self, allies, enemies):
        #Check if any allies are attackers, if none attack weakest enemy, otherwise:
        #Identify strongest enemy
        #Debuff enemy
        print(self.name, 'is a debuffer')
        pass

    def update(self, allies, enemies):
        if self.role == 'attacker':
            self.attack(allies, enemies)
        elif self.role == 'buffer':
            self.buff(allies, enemies)
        elif self.role == 'debuffer':
            self.debuff(allies, enemies)

    def __str__(self):
        output = self.name + ", a level " + str(self.level) + " " + self.role + " has:\n" \
            "Initiative Stat: " + str(self.init) + "\n" \
            "Offensive Stat: " + str(self.offensive) + "\n" \
            "Defensive Stat: " + str(self.defensive) + "\n" \
            "Buffing Stat: " + str(self.buffing) + "\n" \
            "Debuffing Stat: " + str(self.debuffing) + "\n" \
            "Max Hit Points: " + str(self.max_hp) + "\n" \
            "Current Hit Points: " + str(self.current_hp) + "\n" \
            "Guard: " + str(self.guard) + "\n" \
            "Resolve: " + str(self.resolve) + "\n" \
            "Role Bonus: " + str(self.bonus) + "\n" \
            "-----------------------------------"
        return output

class Player(Character):
    
    def __init__(self, name, level, role, init, offensive, defensive, buffing, debuffing, hp, guard, resolve, bonus):
        self.name = name
        self.level = level
        self.role = role
        self.init = init
        self.offensive = offensive
        self.defensive = defensive
        self.buffing = buffing
        self.debuffing = debuffing
        self.max_hp = hp
        self.current_hp = hp
        self.guard = guard
        self.resolve = resolve
        self.bonus = bonus
        self.interrupt = False

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
        self.interrupt = False        

        if self.role == 1:
            self.role = 'attacker'
            self.init = self.primary
            self.offensive = self.primary
            self.defensive = self.primary
            self.buffing = self.secondary
            self.debuffing = self.secondary
            self.resolve = int(self.guard * 0.75)
        if self.role == 2:
            self.role = 'buffer'
            self.init = self.secondary
            self.offensive = self.secondary
            self.defensive = self.primary
            self.buffing = self.primary
            self.debuffing = self.secondary
            self.resolve = int(self.guard * 0.9)
        if self.role == 3:
            self.role = 'debuffer'
            self.init = self.secondary
            self.offensive = self.primary
            self.defensive = self.secondary
            self.buffing = self.secondary
            self.debuffing = self.primary
            self.resolve = self.guard
