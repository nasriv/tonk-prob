import uuid

class Player:
    def __init__(self):
        import random
        names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Hovig', 'Ivan', 'Judy', 'Kevin', 'Linda', 'Mark', 'Nancy', 'Olivia', 'Peggy', 'Quentin', 'Randy', 'Steve', 'Trent', 'Ursula', 'Vinny', 'Walter', 'Xander', 'Yvonne', 'Zelda']
        self.name = random.choice(names)    ## intiialize fake player name
        self.uuid = str(uuid.uuid4().hex)       ## assign unique player identifier (uuid)  
        self.hand = []                      ## this is the hand of the player
        self.spreads = []                    ## this is the spread area for each player to drop their sets into
        self.delay_counter = 0              ## delay between dropping if a spread or knock has occured
        self.bank = 0                       ## player bank for betting ##NOTE: NOT IMPLEMENTED YET

    def show_hand(self):
        '''returns the cards in the players current hand'''
        return self.hand

    def get_hand_value(self):
        '''calculates players hand value Ace = 1'''
        hand_value = 0
        for card in self.hand:
            if card[0] in ['J', 'Q', 'K']:
                hand_value += 10   
            elif card[0] == 'A':
                hand_value += 1
            else:
                hand_value += card[0]
        return hand_value
    
    def knock(self, player, spread_id, card_id):
        '''knock another player's spread'''
        knock_card = self.hand[card_id]
        self.hand.pop(card_id)      # remove card from curr player hand

        player.spreads[spread_id].append(knock_card)   # add card to other players spread    
        self.delay_counter += 1     # increment self.player delay counter
        player.delay_counter += 1   # increment other player's delay counter

    def check_hand(self):
        '''check if player has any spreads in their hands
            -> three of a kind
            -> four of a kind
            -> suited straight of len 3 or more without Ace corner round
        '''
        from collections import Counter

        # check for 3 or 4 of a kind
        rank_counts = Counter(card[0] for card in self.hand)
        multiples_found = [rank for rank, count in rank_counts.items() if count >= 3]

        # move mutiples to a spread
        for rank in multiples_found:
            set_cards = [card for card in self.hand if card[0] == rank]
            self.spread.append(set_cards)
            self.hand = [card for card in self.hand if card[0] != rank]

        if multiples_found:
            print(f"Spread added: {self.spread}")
            print(self.hand)
            self.delay_counter += 2 ## must wait n-turns before dropping
            return True
        else:
            return False

    def draw_card(self, deck, numCards):
        '''draws "n" card from the deck and adds it to the players hand'''
        if len(self.hand) == 0:
            self.hand = deck.deal(numCards)
        else:
            for card in deck.deal(numCards):
                self.hand.append(card)

    def pull_from_discard(self, game):
        '''pull card from discard pile and add to hand'''
        try:
            self.hand.append(game.get_last_discard()[0])
        except TypeError:
            print('No cards in discard pile')
        