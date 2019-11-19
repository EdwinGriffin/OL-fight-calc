import random

attributes = {0:'', 1:'1d4', 2:'1d6', 3:'1d8', 4:'1d10', 5:'2d6', 6:'2d8', 7:'2d10', 8:'3d8', 9:'3d10'}

class Roll:
    def __init__(self, num, bonus, original, exploded, total):
        self.original = original
        self.exploded = exploded
        self.total = total
        self.verbose_orig = []
        self.lethal = 0
        self.num = str(num)
        if bonus > 0:
            self.bonus = " adv " + str(bonus) + ' '
        elif bonus < 0:
            self.bonus = " dis " + str(abs(bonus)) + ' '
        else:
            self.bonus = ''

        if len(original) > 1:
            #check if a d20 was rolled with advantage
            if original[1][1] == 20:
                self.verbose_orig = '1d20' + self.bonus + '[' + str(original[0][0]) + ', ' + str(original[1][0]) + ']'
            #otherwise adv was applied to the attr dice, so represent that in a string
            else:
                self.verbose_orig = '1d20' + '[' + str(original[0][0])+ '] + '
                output = []
                for value in original[1:]:
                    output.append(value[0])
                self.verbose_orig += self.num + 'd' + str(original[1][1]) + self.bonus + '[' + ','.join([str(x) for x in output]) + ']'
        else:
            self.verbose_orig = self.num + 'd' + str(original[0][1]) + '[' + str(original[0][0]) + ']'
        
        if type(exploded[0]) is str:
            explosions = exploded[0].split('+')
            explosions = [int(x.strip()) for x in explosions]
            for v in explosions[1:]:
                self.lethal += v
    
    def __str__(self):
        return '\n    Originally rolled: ' + str(self.verbose_orig) + '\n' \
            '    After exposions and adv/dis this became: ' + str(self.exploded) + '\n' \
                '    For a total of: ' + str(self.total)

def attr_roll(attr, bonus, no_20=False):
    #initialise the roll list with a d20 roll
    roll_list = []
    initial = [(random.randint(1, 20), 20)]
    attr = attributes[attr]
    num = 1
    
    #check if the attr used is a non 0 value and add the appropriate rolls in
    if no_20:
        num, die = attr.split('d')
        num = int(num)
        die = int(die)

        for i in range(0, num + abs(bonus)):
            roll_list.append((random.randint(1, die), die))        
        current = roll_list.copy()
        final_roll_list = [explode(x[0], x[1]) for x in roll_list]
    else:    
        if attr:
            num, die = attr.split('d')
            num = int(num)
            die = int(die)

            for i in range(0, num + abs(bonus)):
                roll_list.append((random.randint(1, die), die))
        else:
            if bonus:
                if bonus > 0:
                    bonus = 1
                elif bonus < 0:
                    bonus = -1
                initial.append((random.randint(1, 20),20))
        current = initial.copy() + roll_list.copy()
        
        #Check to see if there is advantage or disadvantage, and subtract the appropriate values
        if len(initial) == 1:
            if bonus > 0:
                roll_list.sort(key=lambda x: x[0])
            elif bonus < 0:
                roll_list.sort(key=lambda x: x[0], reverse=True)
            final_roll_list = [explode(initial[0][0], 20)] + [explode(x[0], x[1]) for x in roll_list[abs(bonus)::]]
        else:
            if bonus > 0:
                initial.sort(key=lambda x: x[0])
            elif bonus < 0:
                initial.sort(key=lambda x: x[0], reverse=True)
            final_roll_list = [explode(x[0], x[1]) for x in initial[abs(bonus)::]]

    #Checks to see if an explosion happened and a string was returned, handles it, then returns a tuple containing the results at various stages
    output = 0
    for v in final_roll_list:
        if type(v) is str:
            output += eval(v)
        else:
            output += v
    roll = Roll(num, bonus, current, final_roll_list, output)
    return roll

def explode(result, die):
    '''Takes a rolled value, and the face total of a die roll, checks to see if it explodes, and returns the result of the explosion as a string'''

    if result == die:
        return str(result) + ' + ' + str(explode(random.randint(1, die), die))
    else:
        return result