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

        #Sort the initiative list
        self.initiative_order.sort(key=lambda x: x[1], reverse=True)
        rnd = 1
        while not finished:
            #iterate through initiative list, if they're conscious, update them
            for turn, entry in enumerate(self.initiative_order):
                print('-----')
                print('Round:', rnd, 'Turn:', turn+1)
                character = entry[0]
                #Check if the character can take an action, then determine who their allies and enemies are
                if character.interrupt:
                    character.interrupt = False
                    continue
                if character.unconscious or character.dead:
                    if character in self.conscious_enemies:
                        self.conscious_enemies.remove(character)
                    if character in self.conscious_players:
                        self.conscious_players.remove(character)
                if len(self.conscious_enemies) == 0 or len(self.conscious_players) == 0:
                    finished = True
                    break
                if character in self.players:
                    character.update(self.players, self.enemies)
                if character in self.enemies:
                    character.update(self.enemies, self.players)
                
            print('Players remaining:')
            for character in self.players:
                print(str(character.name) + ': with', character.current_hp, 'remaining.')
            print('Enemies remaining:')
            for character in self.enemies:
                print(str(character.name) + ': with', character.current_hp, 'remaining.')
            rnd += 1
