import character
import encounters
import inflect
import csv

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
    
    finished = False
    
    while not finished:
        #initialisation
        p = inflect.engine()
        encounter = encounters.Encounter()
        
        #Check which mode to use
        mode = get_number_input("Enter a number:\n1. File\n2. User Entry")
        while mode not in [1, 2]:
            print('Mode must be 1 or 2.')
            mode = get_number_input("1. File\n2. User Entry")
        
        #File initialisation statements
        if mode == 1:
            team = get_number_input('Which team is fighting?\n1. Fortune\n2. Noble\n3. Dauntless\n4. Valiant')
            teams = {1:'fortune', 2:'noble', 3:'dauntless', 4:'valiant'}
            
            #Generate players
            with open(teams[team] + '.csv') as players_file:
                reader = csv.reader(players_file)
                next(reader, None)
                for row in reader:
                    encounter.players.append(character.Player(row[0], int(row[1]), row[2], int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7]), int(row[8]), int(row[9]), int(row[10]), int(row[11])))
            
            #Generate enemies
            with open('enemies.csv') as enemies_file:
                reader = csv.reader(enemies_file)
                next(reader, None)
                for row in reader:
                    encounter.enemies.append(character.NPC(row[0], int(row[1]), int(row[2])))
        
        #Manual initialisation statements
        elif mode == 2:
            encounter.no_enemies = get_number_input('Number of enemies:')
            encounter.no_players = get_number_input('Number of players:')
            for i in range(1, encounter.no_enemies + 1):
                enemy_level = get_number_input('What level is the ' + p.number_to_words(p.ordinal(i)) + ' enemy?')
                enemy_role = get_number_input('What role does the ' + p.number_to_words(p.ordinal(i)) + ' enemy play?\n1. Attacker\n2. Buffer\n3. Debuffer')
                encounter.enemies.append(character.NPC(enemy_level, enemy_role))
            for enemy in encounter.enemies:
                print(enemy)
        
        start = get_number_input("Begin Encounter?\n1. Yes\n2. No")
        while start != 1:
            start = get_number_input("Begin Encounter?\n1. Yes\n2. No")
        
        encounter.play()

        repeat = get_number_input("Repeat Encounter?\n1. Yes\n2. No")
        while repeat:
            while repeat not in [1,2]:
                repeat = get_number_input("Begin Encounter?\n1. Yes\n2. No")
            if repeat == 1:
                encounter.play()
            if repeat == 2:
                repeat = False
        
        finished = get_number_input("Restart or quit?\n1. Restart\n2. Quit")
        while finished not in [1,2]:
            finished = get_number_input("Restart or quit?\n1. Restart\n2. Quit")
        if finished == 1:
            finished = False
    print('Finished')