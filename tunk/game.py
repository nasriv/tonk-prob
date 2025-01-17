from tunk.player import Player
from tunk.deck import Deck
from rich.console import Console
import random

class Game:
    global console
    console = Console()
    def __init__(self):
        self.players = []       # list of players
        self.discard_pile = []  # discard pile
        self.currPlayer = 0     # index of current player
        self.turn_counter = 1    # tracks each player phase as a turn
        self.rounds = 1           # tracks how many times the game has looped through the players
        self.ended = False      # flag to end the game
        self.game_log = {}
        self.gui_mode = False  # Add flag for GUI mode

    def set_gui_mode(self, enabled=True):
        self.gui_mode = enabled

    def handle_gui_action(self, action_type, **kwargs):
        """Handle actions from GUI"""
        if action_type == 'draw':
            return self.deck.deal(1)
        elif action_type == 'spread':
            player = kwargs.get('player')
            return self.player_spread(player)
        elif action_type == 'knock':
            curr_player = kwargs.get('curr_player')
            target_player = kwargs.get('target_player')
            spread_id = kwargs.get('spread_id')
            card_id = kwargs.get('card_id')
            return curr_player.knock(target_player, spread_id, card_id)
        elif action_type == 'drop':
            curr_player = kwargs.get('player')
            return self.player_drop(curr_player)

    def get_discard_pile_value(self):
        '''returns the point value of the discard pile'''
        discard_value = 0
        for card in self.cards:
            if card[0] in ['J', 'Q', 'K']:
                discard_value += 10   
            elif card[0] == 'A':
                discard_value += 1
            else:
                discard_value += card[0]
        return discard_value

    def show_discard_pile(self):
        return self.discard_pile
    
    def show_last_discard(self):
        if len(self.discard_pile) == 0:
            return None
        else:
            return self.discard_pile[-1]

    def get_last_discard(self):
        if len(self.discard_pile) == 0:
            console.print('No cards in discard pile')
        else:
            return self.discard_pile.pop()

    def player_spread(self, currPlayer):
        '''player spread a set, either a multiple or straight'''
        if currPlayer.check_hand():
            console.print(currPlayer.spreads)

    def player_drop(self, currPlayer):
        '''player drops to check if lowest hand value'''
        player_status = {}
        winning_player = currPlayer     ## assume currPlayer is winner initially, then check
        min_score = winning_player.get_hand_value()
        for player in self.players:
            if player.get_hand_value() <= min_score and player.uuid != winning_player.uuid:
                min_score = player.get_hand_value()
                winning_player = player
        console.print(f"{winning_player.name} Wins! with a score of {min_score}")
        for player in self.players:
            console.print(f"{player.name} score: {player.get_hand_value()}")
        ##NOTE: include bank exchange here
        self.ended = True
            
    def check_init_tunk(self):
        for player in self.players:
            if player.get_hand_value() <= 14 or player.get_hand_value() >= 49:
                console.print(f"{player.name} has an automatic tunk! {player.show_hand()}:value={player.get_hand_value()}")
                ##NOTE: add banking to winning player
                ##BUG: what to do if multiple players get auto-tunk? payout?
                return True
        console.print("No automatic tunk found")
        return False
    
    def player_simple_multiples(self, player):
        '''simple strategy for a player to only win through multiples and no straights'''
        pass

    def player_simple_straights(self, player):
        '''simple strategy for a player to only win through straights and no multiples'''
        pass

    def play(self, numPlayers, simMode):
    
        console.print('----- WELCOME TO TUNK! -----')

        self.deck = Deck()        ## initialize deck
        self.deck.shuffle()     ## shuffle the deck

        for player in range(numPlayers):    ## init players and deal cards
            player = Player()
            player.pull_from_deck(self.deck, 5)  ## deal 5 cards to each player
            self.players.append(player)

        self.currPlayerIdx = random.randint(0, numPlayers-1)  ## randomize which player starts the game
        self.discard_pile.append(self.deck.deal(1))        ## init discard pile

        ### check if any players have a automatic tunk on initial turn (<=14 or >=49)
        self.ended = self.check_init_tunk()

        if simMode == False:    # flag to trigger if model should be used in simulation mode or turn-based
            ## start the game
            while not self.ended:
                currPlayer = self.players[self.currPlayerIdx]
                console.print(f"\n----- {self.players[self.currPlayer].name}'s (idx:{self.currPlayerIdx}) turn -----")
                ## player turn, game status
                console.print(f"[Round: {self.rounds} | Turn: {self.turn_counter}]")
                console.print(f"Hand: {currPlayer.show_hand()}")
                console.print(f"Hand value: {currPlayer.get_hand_value()}")
                console.print(f"Top Discard Pile: {self.show_last_discard()}")
                console.print(f"Cards remaining in deck: {len(self.deck)}")
                console.print(f"Cards remaining in discard: {len(self.discard_pile)}")
                for player in self.players:
                    console.print(f"{player.name} spread: {player.spreads} | delay: {player.delay_counter}")

                ## start of user input play
                action = input('\nWhat do you want to do? \n[D]rop\n[S]pread\n[K]nock\nPull [DI]scard\nPull [DE]ck\n\nEnter Action: ')
                if action.upper() == 'D':
                    self.player_drop(currPlayer)
                if action.upper() == 'S':
                    if not self.player_spread(currPlayer):
                        console.print("No cards to spread...")
                if action.upper() == 'K':
                    ## ask user which player to knock
                    for player_idx, player in enumerate(self.players):
                        console.print(f"\nplayer: {player.name}\nIndex: {player_idx}\nPlayer Spreads: {player.spreads}")
                    player_knock_id = int(input('\nEnter player ID to knock..'))
                    player_knocked = self.players[player_knock_id]

                    ## get which spread to knock
                    if len(player_knocked.spreads) == 0: ## player hasnt spread, cannot knock on them. Skip
                        continue
                    else:
                        for spread_idx, spread in enumerate(player_knocked.spreads):
                            console.print(f"Spread: {spread}\nIndex: {spread_idx}")
                        spread_knock_idx = int(input("Which spread index to knock?..."))

                        ## ask user which card to knock with
                        for card_idx, card in enumerate(currPlayer.hand):
                            console.print(f"card: {str(card[0])+str(card[1])}, id:[{card_idx}]")
                        card_knock_idx = int(input('\nWhat card id to knock with...'))

                        currPlayer.knock(player_knocked, spread_knock_idx, card_knock_idx)
                if action.upper() == 'DI':
                    currPlayer.pull_from_discard(self)
                    ## ask user which card to discard
                    for card_idx, card in enumerate(currPlayer.hand):
                        console.print(f"card: {str(card[0])+str(card[1])}, id:[{card_idx}]")
                    card_discard_idx = int(input('\nWhat card id to discard: '))    # fetch what card index to discard from players hand
                    currPlayer.dump_to_discard(self, currPlayer.hand[card_discard_idx]) # add card to discard pile
                    del currPlayer.hand[card_discard_idx]    # remove card from players hand
                
                if action.upper() == 'DE':
                    currPlayer.pull_from_deck(self.deck, 1)
                    ## ask user which card to discard
                    for card_idx, card in enumerate(currPlayer.hand):
                        console.print(f"card: {str(card[0])+str(card[1])}, id:[{card_idx}]")
                    card_discard_idx = int(input('\nWhat card id to discard: '))    # fetch what card index to discard from players hand
                    currPlayer.dump_to_discard(self, currPlayer.hand[card_discard_idx]) # add card to discard pile
                    del currPlayer.hand[card_discard_idx]    # remove card from players hand
                ## end of user input play

                ## check if (2) spreads have been placed by player then game ends
                if len(currPlayer.spreads) == 2:
                    console.print(f"{currPlayer.name} Tunk! Game Over")
                    self.ended = True

                ## if no more cards in deck, reshuffle discard pile into new deck
                if len(self.deck) == 0:
                    self.deck = self.discard_pile
                    self.deck.shuffle()
                    self.discard_pile = []

                # proceed to next player turn
                self.currPlayerIdx += 1
                if self.currPlayerIdx > numPlayers-1:
                    self.currPlayerIdx = 0

                self.turn_counter += 1 ## increment turn counter
                if (self.turn_counter-1) % numPlayers == 0:
                    self.rounds += 1
                    ## decrease delay counter for each player after entire full turn
                    for player in self.players:
                        if player.delay_counter > 0:
                            player.delay_counter -= 1
                ##
                if self.turn_counter == 50:
                    self.ended = True   
        elif simMode == True:
            ## run simulation mode here
            pass

        else:
            return print("No valid SimMode boolean entered")