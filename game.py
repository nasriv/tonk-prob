from player import Player
from deck import Deck
from rich.console import Console
import random

class Game:
    def __init__(self):
        self.players = []       # list of players
        self.discard_pile = []  # discard pile
        self.currPlayer = 0     # index of current player
        self.turn_counter = 1           # tracks each player phase as a turn
        self.rounds = 1           # tracks how many times the game has looped through the players
        self.ended = False      # flag to end the game
        self.game_log = {}

    def show_discard_pile(self):
        return self.discard_pile
    
    def show_last_discard(self):
        if len(self.discard_pile) == 0:
            return None
        else:
            return self.discard_pile[-1]

    def get_last_discard(self):
        if len(self.discard_pile) == 0:
            print('No cards in discard pile')
        else:
            return self.discard_pile.pop()

    def dump_to_discard(self, card):
        '''discard a card into the discard pile'''
        self.discard_pile.append(card)

    def player_spread(self, currPlayer):
        '''player spread a set, either a multiple or straight'''
        if currPlayer.check_hand():
            print(currPlayer.spread)

    def player_drop(self, currPlayer):
        '''player drops to check if lowest hand value'''
        player_status = {}
        winning_player = currPlayer     ## assume currPlayer is winner initially, then check
        min_score = winning_player.get_hand_value()
        for player in self.players:
            if player.get_hand_value() <= min_score and player.uuid != winning_player.uuid:
                min_score = player.get_hand_value()
                winning_player = player
        print(f"{winning_player.name} Wins! with a score of {min_score}")
        for player in self.players:
            print(f"{player.name} score: {player.get_hand_value()}")
        ##NOTE: include bank exchange here
        self.ended = True
            
    def check_init_tunk(self):
        for player in self.players:
            if player.get_hand_value() <= 14 or player.get_hand_value() >= 49:
                print(f"{player.name} has an automatic tunk! {player.show_hand()}:value={player.get_hand_value()}")
                ##NOTE: add banking to winning player
                ##BUG: what to do if multiple players get auto-tunk? payout?
                return True
        print("No automatic tunk found")
        return False
    
    def player_simple_multiples(self, player):
        '''simple strategy for a player to only win through multiples and no straights'''
        pass

    def player_simple_straights(self, player):
        '''simple strategy for a player to only win through straights and no multiples'''
        pass

    def play(self, numPlayers, deck):
        console = Console()
        console.print('----- WELCOME TO TUNK! -----')

        self.deck = deck        ## initialize deck
        self.deck.shuffle()     ## shuffle the deck

        for player in range(numPlayers):    ## init players and deal cards
            player = Player()
            player.draw_card(self.deck, 5)  ## deal 5 cards to each player
            self.players.append(player)

        self.currPlayer = random.randint(0, numPlayers-1)  ## randomize which player starts the game
        self.discard_pile.append(self.deck.deal(1))        ## init discard pile

        ### check if any players have a automatic tunk on initial turn (<=14 or >=49)
        self.ended = self.check_init_tunk()

        ## start the game
        while not self.ended:
            currPlayer = self.players[self.currPlayer]
            console.print(f"\n----- {self.players[self.currPlayer].name}'s (idx:{self.currPlayer}) turn -----")
            ## player turn, game status
            console.print(f"[Round: {self.rounds} | Turn: {self.turn_counter}]")
            console.print(f"Hand: {currPlayer.show_hand()}")
            console.print(f"Hand value: {currPlayer.get_hand_value()}")
            console.print(f"Top Discard Pile: {self.show_last_discard()}")
            for player in self.players:
                console.print(f"{player.name} spread: {player.spread} | delay: {player.delay_counter}")

            action = input('\nWhat do you want to do? \n[D]rop\n[S]pread\n[K]nock\nPull [DI]scard\nPull [DE]ck\n\tEnter Action: ')
            if action == 'D':
                self.player_drop(currPlayer)
            if action == 'S':
                self.player_spread(currPlayer)
            if action == 'K':
                pass
            if action == 'DI':
                currPlayer.pull_from_discard(self)
            if action == 'DE':
                currPlayer.draw_card(self.deck, 1)

            # proceed to next player turn
            self.currPlayer += 1
            if self.currPlayer > numPlayers-1:
                self.currPlayer = 0

            self.turn_counter += 1 ## increment turn counter
            if (self.turn_counter-1) % numPlayers == 0:
                self.rounds += 1
                ## decrease delay counter for each player after entire full turn
                for player in self.players:
                    if player.delay_counter > 0:
                        player.delay_counter -= 1

            if self.turn_counter == 20:
                self.ended = True