# Define the Hand class representing a player's hand of cards
class Hand:
    def __init__(self, amount, cards):
        """
        Initialize a player's hand.

        Args:
            amount (int): The number of cards in the hand.
            cards (list): A list of cards in the hand.
        """
        self.amount = amount
        self.cards = cards

    def set_cards(self, cards):
        """
        Set the cards in the hand to a new set of cards.

        Args:
            cards (list): A list of cards to replace the current hand's cards.
        """
        self.cards = cards

    def print_hand(self):
        """
        Print the cards in the hand.
        """
        print(self.cards)

    def __str__(self):
        """
        Return a string representation of the hand.
        """
        return f"Hand: {self.cards}"


