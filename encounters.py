import dice
import operator

class Encounter:
    def __init__(self):
        self.no_players = 0
        self.no_enemies = 0
        self.players = []
        self.conscious_players = []
        self.enemies = []
        self.conscious_enemies = []
        self.initiative_order = []
        self.player_output = {}

    def play(self):
        #get initiatives for turn order
        #play out each characters action based on their ai
        #continue play until all enemies or all players below 0hp
        finished = False
        
        #Determine initiative order
        for player in self.players:
            self.conscious_players.append(player)
            self.initiative_order.append((player, dice.attr_roll(player.init, 0).total))
        for enemy in self.enemies:
            self.conscious_enemies.append(enemy)
            self.initiative_order.append((enemy, dice.attr_roll(enemy.init, 0).total))

        print(', '.join([x.name for x in self.conscious_players]), 'are facing off against', ', '.join([x.name for x in self.conscious_enemies]))

        #Sort the initiative list
        self.initiative_order.sort(key=lambda x: x[1], reverse=True)
        rnd = 1
        while not finished:
            #iterate through initiative list, if they're conscious, update them
            for turn, entry in enumerate(self.initiative_order):
                print('-----')
                print('Round:', str(rnd) + ',', 'Turn:', turn+1)
                character = entry[0]
                
                #Take character actions (update method handles consciousness)
                if character in self.players:
                    character.update(self.players, self.enemies)
                if character in self.enemies:
                    character.update(self.enemies, self.players)
                
                #After character actions, check consciousness
                for character in (self.conscious_enemies + self.conscious_players):
                    if character.unconscious or character.dead:
                        if character in self.conscious_enemies:
                            self.conscious_enemies.remove(character)
                        if character in self.conscious_players:
                            self.conscious_players.remove(character)
                
                #Check if there are any opposing combatants left
                if len(self.conscious_enemies) == 0 or len(self.conscious_players) == 0:
                    print('-----')
                    print('No more conscious opposing combatants')
                    print('-----')
                    finished = True
                    break
            print('Round', rnd, 'has finished. Current situation:\n')
            print('Players remaining:')
            for character in self.players:
                new_max = character.max_hp - character.lethal
                print('\t', str(character.name) + ': with', str(character.current_hp) + '/' + str(new_max), 'hp remaining.', character.lethal, 'lethal damage suffered.', 'Character is dead' if character.dead else '')
            print('Enemies remaining:')
            for character in self.enemies:
                new_max = character.max_hp - character.lethal
                print('\t', str(character.name) + ': with', str(character.current_hp) + '/' + str(new_max), 'hp remaining.', character.lethal, 'lethal damage suffered.', 'Character is dead' if character.dead else '')
            print('-----')
            #input('Press enter to continue...') if not finished else print()
            rnd += 1
        for character in self.players:
            self.player_output[character.name] = character.lethal
        return self.player_output
