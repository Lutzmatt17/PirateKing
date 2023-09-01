from Hand import Hand
from Deck import Deck
from Player import Player

# Define the Game class to manage the Pirate King card game
class Game:
    def __init__(self, deck, round, player_num):
        """
        Initialize a new game of Pirate King.

        Args:
            deck (Deck): The deck of cards for the game.
            round (int): The number of rounds in the game.
            player_num (int): The number of players in the game.
        """
        self.deck = deck
        self.round = round
        self.player_num = player_num
        self.player_hands = []

    def deal_hand(self, deck):
        """
        Deal a hand of cards from the deck.

        Args:
            deck (Deck): The deck from which cards are dealt.

        Returns:
            list: A list of cards representing a hand.
        """
        hand = []
        for _ in range(self.round):
            card = deck.deal()
            hand.append(card)
        return hand

    def deal_players(self):
        """
        Deal hands to all players in the game.
        """
        for _ in range(self.player_num):
            self.player_hands.append(Hand(self.round, self.deal_hand(self.deck)))

    def print_hands(self):
        """
        Print the hands of all players in the game.
        """
        for hand in self.player_hands:
            print("Hand: ")
            for card in hand.cards:
                print("Card: ", card)

    def player_join(self):
        """
        Add a player to the game.
        """
        self.players.append(Player([], 0))

    def game(self):
        """
        Start the game.
        """
        game_over = False

# Define the PirateKingDriver class for managing the game setup
class PirateKingDriver:
    def __init__(self):
        """
        Initialize the Pirate King game driver.
        """
        self.deck = Deck()
        self.game = Game(self.deck, 5, 6)

    def main(self):
        """
        Main entry point for the Pirate King game.
        """
        print("Welcome to Pirate King!")
        self.deck.shuffle()
        self.game.deal_players()
        self.game.print_hands()

if __name__ == "__main__":
    pirate_king_driver =  PirateKingDriver()
    pirate_king_driver.main()



