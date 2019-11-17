import character
import encounters
import inflect

def explode(result, die):
    '''Takes a rolled value, and the face total of a die roll, checks to see if it explodes, and returns the result of the explosion as a string'''

    if result == die:
        return str(result) + ' + ' + str(explode(random.randint(1, die), die))
    else:
        return result

def roll(num, die, adv = 0):
    '''Rolls a given die, num, number of times, checking for explosions and allowing for adv/disadvantage'''
    
    #Unsure of input type, so all converted to ints.
    num = int(num)
    die = int(die)
    adv = int(adv)
    
    roll_list = []

    #Create the random values for the roll (inc. adv/dis)
    for i in range(0, num + abs(adv)):
        roll_list.append(random.randint(1, die))
    current = roll_list.copy()
    
    #Check to see if there is advantage or disadvantage, and subtract the appropriate values
    if adv > 0:
        roll_list.sort()
    elif adv < 0:
        roll_list.sort(reverse=True)
    final_roll_list = [explode(x, die) for x in roll_list[abs(adv)::]]
    
    #Checks to see if an explosion happened and a string was returned, handles it, then returns a tuple containing the results at various stages
    output = 0
    for v in final_roll_list:
        if type(v) is str:
            output += eval(v)
        else:
            output += v
    return (current, final_roll_list, output)

def parse_dice(text):
    '''Checks to see if adv/disadvantage is required, then passes the correct values to roll()'''
    if 'adv' in text:
        dice, adv = text.split('adv')
        num, die = dice.split('d')
        return roll(num, die, adv)
    elif 'dis' in text:
        dice, adv = text.split('dis')
        num, die = dice.split('d')
        return roll(num, die, -int(adv))
    else:
        num, die = text.split('d')
        return roll(num, die)

def get_number_input(text, repeat=False):
    if not repeat:
        text = text + '\n> '
    try:
        output = int(input(text))
        print('-----')
        return output
    except:
        print('-----\nPlease enter a number')
        return get_number_input(text, repeat = True)

if __name__ == "__main__":
    p = inflect.engine()
    encounter = encounters.Encounter()
    mode = get_number_input("Enter a number:\n1. File\n2. User Entry")
    while mode not in [1, 2]:
        print('Mode must be 1 or 2.')
        mode = get_number_input("1. File\n2. User Entry")
    if mode == 1:
        #TODO
        print('TODO')
    elif mode == 2:
        encounter.no_enemies = get_number_input('Number of enemies:')
        encounter.no_players = get_number_input('Number of players:')
        for i in range(1, encounter.no_enemies + 1):
            enemy_level = get_number_input('What level is the ' + p.number_to_words(p.ordinal(i)) + ' enemy?')
            enemy_type = get_number_input('What type is the ' + p.number_to_words(p.ordinal(i)) + ' enemy?\n1. Attacker\n2. Buffer\n3. Debuffer')
            encounter.enemies.append(character.NPC(enemy_level, enemy_type))
    for enemy in encounter.enemies:
        print(enemy)