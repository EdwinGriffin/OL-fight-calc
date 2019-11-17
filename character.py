class Player:
    
    def __init__(self, offensive, defensive, buff, debuff, hp, defence):
        self.offensive = offensive
        self.defensive = defensive
        self.buff = buff
        self.debuff = debuff
        self.hp = hp
        self.defence = defence
        self.has_allies = False

class NPC:
    
    def __init__(self, level, type):
        self.level = level
        self.type = type
        self.primary = int(4 + (self.level * 0.5))
        self.secondary = int(2.5 + (self.level * 0.5))
        self.hp = int(14 + (self.level * 2))
        self.defence = int(12 + self.level)
        self.has_allies = False

        if self.type == 1:
            self.type = 'Attacker'
            self.offensive = self.primary
            self.defensive = self.primary
            self.buff = self.secondary
            self.debuff = self.secondary
        if self.type == 2:
            self.type = 'Buffer'
            self.offensive = self.secondary
            self.defensive = self.primary
            self.buff = self.primary
            self.debuff = self.secondary
        if self.type == 3:
            self.type = 'Debuffer'
            self.offensive = self.primary
            self.defensive = self.secondary
            self.buff = self.secondary
            self.debuff = self.primary    
    
    def __str__(self):
        output = "A level " + str(self.level) + " " + self.type + " npc has:\n" \
            "Offensive Stat: " + str(self.offensive) + "\n" \
                "Defensive Stat: " + str(self.defensive) + "\n" \
                    "Buffing Stat: " + str(self.buff) + "\n" \
                        "Debuffing Stat: " + str(self.debuff) + "\n" \
                            "Hit Points: " + str(self.hp) + "\n" \
                                "Defence Stat: " + str(self.defence) + "\n" \
                                    "-----------------------------------"
        return output