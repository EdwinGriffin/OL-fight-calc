import dice
import operator

class Encounter:
    def __init__(self):
        self.no_players = 0
        self.no_enemies = 0
        self.players = []
        self.conscious_players = []
        self.enemies = []
        self.initiative_order = []

    def play(self):
        #get initiatives for turn order
        #play out each characters action based on their ai
        #continue play until all enemies or all players below 0hp
        finished = False
        
        #Determine initiative order
        for player in self.players:
            self.conscious_players.append(player)
            self.initiative_order.append((player, dice.attr_roll(player.init, 0)['Total']))
        for enemy in self.enemies:
            self.initiative_order.append((enemy, dice.attr_roll(enemy.init, 0)['Total']))
        
        #Sort the initiative list
        self.initiative_order.sort(key=lambda x: x[1], reverse=True)

        while not finished:
            print('hi')
            #iterate through initiative list, if they're conscious, update them
            for entry in self.initiative_order:
                if entry in self.conscious_players or entry in self.enemies:
                    print(entry[0].update(self.players, self.enemies))
                    if len(self.enemies) == 0 or len(self.conscious_players) == 0:
                        finished = True
                        break
