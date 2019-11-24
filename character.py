import dice
import random

class Character:

    def __init__(self, name):
        self.name = name
        self.level = 0
        self.role = ''
        self.init = 0
        self.offensive = 0
        self.defensive = 0
        self.buffing = 0
        self.debuffing = 0
        self.max_hp = 0
        self.current_hp = 0
        self.guard = 0
        self.resolve = 0
        self.bonus = 0
        self.interrupt = False
        self.unconscious = False
        self.dead = False
        self.lethal = 0
        self.buffed = False
        self.debuffed = False
        self.attack_priority = -1000

    def attack(self, allies, enemies):
        #Identify weakest enemy
        #Attack weakest enemy
        target = Character('empty')
        for enemy in enemies:
            if not enemy.unconscious:
                enemy.attack_priority = 0
                #Attack priority calculations
                enemy.attack_priority += 40/enemy.guard
                enemy.attack_priority += 30/enemy.current_hp
                #Add half their offensive stat to their priority, starting at 4
                enemy.attack_priority += max(0, (enemy.offensive/2) - 2)
                #Add half their bonus stat to their priority
                enemy.attack_priority += enemy.bonus/2    
            
                if enemy.attack_priority > target.attack_priority:
                    target = enemy
                
                if type(self) is NPC:
                    if enemy.current_hp + enemy.guard > target.current_hp + target.guard:
                       target = enemy

        if target.name == 'empty':
            print('There are no more targets')
            return

        print(self.name, 'has selected', target.name, 'as their target as they have the highest priority of', round(target.attack_priority,2))
        attack_roll = dice.attr_roll(self.offensive, self.bonus)
        print(self.name, 'attacks', target.name, 'with:', attack_roll)
        if attack_roll.total > target.guard:
            defend_attempt = False
            starting_hp = target.current_hp
            starting_max = target.max_hp - target.lethal

            damage = max(3, attack_roll.total - target.guard)
            #Check if a defend attempt must be made\
            #A defend will be attempted if the attack will unconscious the target, if there is at least 10 lethal damage, or if the attack is 50% of current health and health is above 15
            if (target.current_hp - damage) <= 0 or attack_roll.lethal >= 10 or ((target.current_hp - damage) < int(target.current_hp/2) and target.max_hp > 15):
                if not target.interrupt:
                    if type(target) is Player:
                        defend_attempt = target.defend(enemies, allies, self, attack_roll.total, attack_roll.lethal)
            #If no defend attempt is made or the attempt fails
            if not defend_attempt:
                target.lethal += attack_roll.lethal
                if attack_roll.lethal:
                    print(target.name, 'suffers lethal damage! Their max hp is reduced by', attack_roll.lethal)
                target.current_hp -= damage
                if target.current_hp < 0:
                    target.lethal += abs(target.current_hp)
                    print(target.name, 'suffers overflow lethal damage! Their max hp is reduced by', abs(target.current_hp))
                    target.current_hp = 0
                new_max = target.max_hp - target.lethal
                print(target.name, 'has a guard of', target.guard, 'so the attack hits and', str(target.name) + "'s hp is reduced by", damage, 'from', str(starting_hp) + '/' + str(starting_max), 'to', str(target.current_hp) + '/' + str(new_max))
            
            #Check health to see if unconscious/dead are needed and apply lethal damage
            if target.current_hp <= 0:
                target.unconscious = True
                if target.lethal >= target.max_hp:
                    fort_save = dice.attr_roll(target.fort, 0)
                    print(target.name, 'has suffered excessive lethal damage and must pass a fortitude check against', (target.lethal - target.max_hp) + 10, 'to stabalise:', fort_save)
                    if fort_save.total >= (target.lethal - target.max_hp) + 10:
                        target.lethal = target.max_hp
                        print(target.name, 'was able to stabalise')
                    else:
                        target.dead = True
                        print(target.name, 'was unable to stabalise and has died')
                else:
                    print(target.name, 'has fallen unconscious')
        else:
            print(self.name, 'was unable to effectively strike', target.name)

    def defend(self, allies, enemies, origin, attack, lethal):
        #If the resolution of an attack action would bring a target below 0 hp, target will attempt a defend action
        # must return true if the defence is successful, false otherwise
        starting_hp = self.current_hp
        starting_max = self.max_hp - self.lethal
        print(self.name, 'is attempting a defend action against', origin.name, 'with an attack of', attack)
        self.interrupt = True
        defend_roll = dice.attr_roll(self.defensive, self.bonus)
        if defend_roll.total > attack:
            print(self.name, 'defended with:', defend_roll)
            print(self.name, 'was able to avoid the attack')
            return True
        elif defend_roll.total <= self.guard:
            print(self.name, 'was unable to defend against the attack with an attempt of:', defend_roll)
            return False
        elif defend_roll.total <= attack:
            #Calc damage, min 3
            damage = max(3, attack - defend_roll.total)
            
            #Edge case for if the defend action result reduces the amount of lethal damage (eg. attack 25 [20 + 5], defend 23, lethal should only be 2, damage 3)
            if (attack - defend_roll.total) < lethal:
                lethal = (attack - defend_roll.total)
            
            print(self.name, 'was able to partially defend the attack with an attempt of:', defend_roll)

            #Check if lethal damage was still dealt
            if lethal:
                self.lethal += lethal
                print(self.name, 'suffers lethal damage! Their max hp is reduced by', lethal)
            
            #Reduce the appropriate health pools
            self.current_hp -= damage
            if self.current_hp < 0:
                self.lethal += abs(self.current_hp)
                print(self.name, 'suffers overflow lethal damage! Their max hp is reduced by', abs(self.current_hp))
                self.current_hp = 0
            
            new_max = self.max_hp - self.lethal
            print(self.name+"'s hp was reduced by", damage, 'from', str(starting_hp) + '/' + str(starting_max), 'to', str(self.current_hp) + '/' + str(new_max))
            return True

    def buff(self, allies, enemies):
        #Check if ally needs healing (<50%?)
        #Check if any allies are attackers or debuffers, buff if they are (prioritise attackers)
        #Attack if no allies are attackers or debuffers
       
        buff_roll = dice.attr_roll(self.buffing, self.bonus)
        
        unconscious = []
        heal_priority = []
        buff_priority = []

        for player in allies:
            if not player.dead:
                if player.unconscious and player.lethal < player.max_hp:
                    unconscious.append(player)
                elif (player.current_hp < (player.max_hp - player.lethal)/2):
                    heal_priority.append(player)
                elif not player.buffed and not player.interrupt and player.role == 'attacker' and not player.unconscious:
                    buff_priority.append(player)

        if unconscious:
            unconscious.sort(key=lambda x: x.lethal)
            print(self.name, 'is attempting to heal', unconscious[0].name, 'with:', buff_roll)
            for i in range(9, 0, -1):
                if self.buffing - i >= 0 and buff_roll.total >= 10 + (i * 2):
                    if buff_roll.total >= 20 + (i * 2):
                        heal_roll = dice.attr_roll(i + 1, 0, True)
                        print('Exceptional Success!', end=' ')
                    else:
                        heal_roll = dice.attr_roll(i, 0, True)
                        print('Success!', end=' ')
                    unconscious[0].unconscious = False
                    unconscious[0].current_hp += heal_roll.total
                    new_max = unconscious[0].max_hp - unconscious[0].lethal
                    if unconscious[0].current_hp > new_max:
                        unconscious[0].current_hp = new_max
                    print(heal_roll, '\n' + unconscious[0].name, 'is conscious and gains', str(heal_roll.total) + 'hp. They are now on', str(unconscious[0].current_hp) + '/' + str(new_max))
                    return
            print('The attempt was unsuccessful')
        elif heal_priority:
            heal_priority.sort(key=lambda x: x.guard)
            print(self.name, 'is attempting to heal', heal_priority[0].name, 'with:', buff_roll)
            for i in range(9, 0, -1):
                if self.buffing - i >= 0 and buff_roll.total >= 10 + (i * 2):
                    if buff_roll.total >= 20 + (i * 2):
                        heal_roll = dice.attr_roll(i + 1, 0, True)
                        print('Exceptional Success!', end=' ')
                    else:
                        heal_roll = dice.attr_roll(i, 0, True)
                        print('Success!', end=' ')
                    heal_priority[0].current_hp += heal_roll.total
                    new_max = heal_priority[0].max_hp - heal_priority[0].lethal
                    if heal_priority[0].current_hp > new_max:
                        heal_priority[0].current_hp = new_max
                    print(heal_roll, '\n' + heal_priority[0].name, 'is healed and gains', str(heal_roll.total) + 'hp. They are now on', str(heal_priority[0].current_hp) + '/' + str(new_max))
                    return
            print('The attempt was unsuccessful')
        elif buff_priority:
            buff_priority.sort(key=lambda x: x.offensive)
            print(self.name, 'is attempting to buff', buff_priority[0].name, 'with:', buff_roll)
            for i in range(9, 0, -3):
                if self.buffing/i >= 1 and buff_roll.total >= 10 + (i * 2):
                    buff_priority[0].buffed = True
                    if buff_roll.total >= 20 + (i * 2):
                        buff_priority[0].bonus += int(self.buffing/i) + 1
                        print('Exceptional Success!', end=' ')
                    else:
                        buff_priority[0].bonus += int(self.buffing/i)
                        print('Success!', end=' ')
                    print(buff_priority[0].name, 'is buffed and now has a bonus of', buff_priority[0].bonus)
                    return
            print('The attempt was unsuccessful')
        else:
            print(self.name, 'has no characters to heal/buff so they will attack')
            self.attack(allies, enemies)

    def debuff(self, allies, enemies):
        #Get debuff roll and initialise priority lists
        debuff_roll = dice.attr_roll(self.debuffing, self.bonus)
        debuff_priority = []
        friendly_attackers = []

        #Build priority list for enemies
        for enemy in enemies:
            if enemy.role == 'attacker' and not enemy.debuffed and not enemy.unconscious:
                debuff_priority.append(enemy)
        
        #Check to see if there are any attackers on your team, otherwise attacking has a higher priority
        for ally in allies:
            if ally.role == 'attacker' and not ally.unconscious:
                friendly_attackers.append(ally)
        
        if not friendly_attackers:
            debuff_priority = []

        #Debuff the highest priority target
        if debuff_priority:
            if type(self) == NPC:
                debuff_priority.sort(key=lambda x: x.current_hp)
            else:
                debuff_priority.sort(key=lambda x: x.offensive)
            target = debuff_priority[0]
            print(self.name, 'is attempting to debuff', target.name, 'with:', debuff_roll)
            if debuff_roll.total >= target.resolve:
                if debuff_roll.total >= target.resolve + 10:
                    target.bonus -= int(self.debuffing/3) + 1
                    target.debuffed = True
                    print('Exceptional Success!', target.name + "'s bonus has been reduced to", target.bonus)
                else:
                    target.bonus -= int(self.debuffing/3)
                    target.debuffed = True
                    print('Success!', target.name + "'s bonus has been reduced to", target.bonus)
            else:
                print('The attempt was unsuccessful')
        #Attack otherwise
        else:
            print(self.name, 'has no characters to debuff so they will attack')
            self.attack(allies, enemies)

    def update(self, allies, enemies):
        if self.dead:
            print(self.name, 'is dead')
        elif self.unconscious:
            print(self.name, 'is unconscious')
            if self.interrupt:
                self.interrupt = False
        elif self.interrupt:
            self.interrupt = False
            print(self.name, 'used a defend action last turn and is unable to act')
        elif not self.interrupt:
            if self.role == 'attacker':
                print(self.name, 'is an attacker')
                self.attack(allies, enemies)
            elif self.role == 'buffer':
                print(self.name, 'is a buffer')
                self.buff(allies, enemies)
            elif self.role == 'debuffer':
                print(self.name, 'is a debuffer')
                self.debuff(allies, enemies)

        #input('-----\nPress enter to continue...')

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
    
    def __init__(self, name, level, role, init, fort, offensive, defensive, buffing, debuffing, hp, guard, resolve, bonus, lethal):
        self.name = name
        self.level = level
        self.role = role
        self.init = init
        self.fort = fort
        self.offensive = offensive
        self.defensive = defensive
        self.buffing = buffing
        self.debuffing = debuffing
        self.max_hp = hp
        self.lethal = lethal
        self.current_hp = hp - lethal
        self.guard = guard
        self.resolve = resolve
        self.bonus = bonus
        self.interrupt = False
        self.unconscious = False
        self.dead = False
        self.buffed = False
        self.debuffed = False
        self.attack_priority = 0

class NPC(Character):
    
    def __init__(self, name, level, role):
        self.name = name
        self.level = level
        self.role = role
        self.primary = int(4 + (self.level * 0.5))
        self.secondary = int(2.5 + (self.level * 0.5))
        self.fort = int(2.5 + (self.level * 0.5))
        self.max_hp = int(14 + (self.level * 2))
        self.current_hp = int(14 + (self.level * 2))
        self.lethal = 0
        self.guard = int(12 + self.level)
        self.bonus = int(self.level/3)
        self.interrupt = False
        self.unconscious = False
        self.dead = False        
        self.buffed = False
        self.debuffed = False
        self.attack_priority = 0

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
