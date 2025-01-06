class Deck:
    def __init__(self):
        suits = ['\u2665', '\u2664', '\u2663', '\u2666']
        ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
        self.cards = [(rank, suit) for suit in suits for rank in ranks]
        self.card_values = {str(rank): rank for rank in range(1,11)}
        self.card_values.update({'J': 10, 'Q': 10, 'K': 10, 'A': 11})
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.cards})'

    def __len__(self):
        '''returns the remaining len of cards in the deck'''
        return len(self.cards)
    
    def get_deck_value(self):
        '''returns the remaining point value of the card deck'''
        deck_value = 0
        for card in self.cards:
            if card[0] in ['J', 'Q', 'K']:
                deck_value += 10   
            elif card[0] == 'A':
                deck_value += 1
            else:
                deck_value += card[0]
        return deck_value

    def get_deck(self):
        ''' returns the remaining cards in the deck'''
        return self.cards
    
    def deal(self, numCards):
        '''deals an "n" number of cards from the deck'''
        return [self.cards.pop() for _ in range(numCards)]

    def shuffle(self):
        '''shuffles the deck'''
        import random
        random.shuffle(self.cards)
