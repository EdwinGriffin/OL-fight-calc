import random

attributes = {0:'', 1:'1d4', 2:'1d6', 3:'1d8', 4:'1d10', 5:'2d6', 6:'2d8', 7:'2d10', 8:'3d8', 9:'3d10'}

def attr_roll(attr, bonus):
    #initialise the roll list with a d20 roll
    roll_list = [random.randint(1, 20)]
    attr = attributes[attr]

    #check if the attr used is a non 0 value and add the appropriate rolls in
    if attr:
        num, die = attr.split('d')
        num = int(num)
        die = int(die)

        for i in range(0, num + abs(bonus)):
            roll_list.append(random.randint(1, die))
    else:
        if bonus:
            roll_list.append(random.randint(1, 20))

    current = roll_list.copy()

    #Check to see if there is advantage or disadvantage, and subtract the appropriate values
    if bonus > 0:
        roll_list.sort()
    elif bonus < 0:
        roll_list.sort(reverse=True)
    final_roll_list = [explode(x, die) for x in roll_list[abs(bonus)::]]

    #Checks to see if an explosion happened and a string was returned, handles it, then returns a tuple containing the results at various stages
    output = 0
    for v in final_roll_list:
        if type(v) is str:
            output += eval(v)
        else:
            output += v
    output_dict = {'Original': current, 'After Explosion': final_roll_list, 'Total': output}
    return output_dict

def explode(result, die):
    '''Takes a rolled value, and the face total of a die roll, checks to see if it explodes, and returns the result of the explosion as a string'''

    if result == die:
        return str(result) + ' + ' + str(explode(random.randint(1, die), die))
    else:
        return result