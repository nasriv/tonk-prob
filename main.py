from game import Game
from deck import Deck

def main():
    deck = Deck()
    deck.shuffle()
    deck.get_deck()

    game = Game()
    game.play(numPlayers=1, deck=deck)

if __name__ == "__main__":
    main()

