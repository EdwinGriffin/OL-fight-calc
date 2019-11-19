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
        
        #File initialisation statements
        team = get_number_input('Which team is fighting?\n1. Fortune\n2. Noble\n3. Dauntless\n4. Valiant')
        teams = {1:'fortune', 2:'noble', 3:'dauntless', 4:'valiant'}
        
        #Generate players
        players = []
        with open('data/' + teams[team] + '.csv') as players_file:
            reader = csv.reader(players_file)
            next(reader, None)
            for row in reader:
                players.append(character.Player(row[0], int(row[1]), row[2], int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7]), int(row[8]), int(row[9]), int(row[10]), int(row[11]), int(row[12])))
        encounter.players = players.copy()
        
        #Generate enemies
        enemies = []
        with open('data/enemies.csv') as enemies_file:
            reader = csv.reader(enemies_file)
            next(reader, None)
            for row in reader:
                enemies.append(character.NPC(row[0], int(row[1]), int(row[2])))
        encounter.enemies = enemies.copy()
        
        #Begin check (there's a lot of while true loops here, wanna make sure there's break points for easy exit)
        start = get_number_input("Begin Encounter?\n1. Yes\n2. No")
        while start != 1:
            start = get_number_input("Begin Encounter?\n1. Yes\n2. No")
        
        encounter.play()
        
        #Check if the simulations performed so far are sufficient, or if you want to run a new one from scratch
        finished = get_number_input("Restart or quit?\n1. Restart\n2. Quit")
        while finished not in [1,2]:
            finished = get_number_input("Restart or quit?\n1. Restart\n2. Quit")
        if finished == 1:
            finished = False
    print('Finished')