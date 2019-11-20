import character
import encounters
import inflect
import csv
import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

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
    players_final = {}
    players_lethal = {}
    finished = False
    #File initialisation statements
    team = get_number_input('Which team is fighting?\n1. Fortune\n2. Noble\n3. Dauntless\n4. Valiant')
    teams = {1:'fortune', 2:'noble', 3:'dauntless', 4:'valiant'}

    num_of_encounters = 100

    for i in range(num_of_encounters):
        blockPrint()
        #initialisation
        p = inflect.engine()
        encounter = encounters.Encounter()
        
        #Generate players
        players = []
        with open('data/' + teams[team] + '.csv') as players_file:
            reader = csv.reader(players_file)
            next(reader, None)
            for row in reader:
                players.append(character.Player(row[0], int(row[1]), row[2], int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7]), int(row[8]), int(row[9]), int(row[10]), int(row[11]), int(row[12]), int(row[13])))
        encounter.players = players.copy()
        
        #Generate enemies
        enemies = []
        with open('data/enemies.csv') as enemies_file:
            reader = csv.reader(enemies_file)
            next(reader, None)
            for row in reader:
                enemies.append(character.NPC(row[0], int(row[1]), int(row[2])))
        encounter.enemies = enemies.copy()
        
        #player the encounter and get the lethal damage
        players_lethal = encounter.play()
        
        for key in players_lethal:
            if key in players_final:
                players_final[key] += players_lethal[key]
            else: 
                players_final[key] = players_lethal[key]
        enablePrint()
        print(i)

    enablePrint()
    for key in players_final:
        print(key, int(players_final[key]/num_of_encounters))
    #print(players_final)