import random

# Define the Card class representing standard playing cards
class Card:
    def __init__(self, suit, number, bonus, priority):
        """
        Initialize a standard playing card.

        Args:
            suit (str): The suit of the card.
            number (int): The number of the card.
            bonus (int): The bonus associated with the card.
            priority (int): The priority of the card.
        """
        self.suit = suit
        self.number = number
        self.bonus = bonus
        self.priority = priority

    def __str__(self):
        """
        Return a string representation of the card.
        """
        return f"{self.number} of {self.suit} with bonus of {self.bonus} and priority of {self.priority}"

    def to_dict(self):
        return {'suit': self.suit, 'number': self.number, 'bonus': self.bonus, 'priority': self.priority}

# Define the Special_Card class for special cards
class Special_Card:
    def __init__(self, type, priority, bonus):
        """
        Initialize a special card.

        Args:
            type (str): The type of the special card.
            priority (int): The priority of the special card.
            bonus (int): The bonus associated with the special card.
        """
        self.type = type
        self.priority = priority
        self.bonus = bonus
    
    def __str__(self):
        """
        Return a string representation of the special card.
        """
        return f"{self.type} with bonus of {self.bonus} and priority of {self.priority}"

    def to_dict(self):
        return {'type': self.type, 'priority': self.priority, 'bonus': self.bonus}        

# Define a subclass Tigress, inheriting from Special_Card
class Tigress(Special_Card):
    def __init__(self, type, priority, bonus):
        """
        Initialize a Tigress special card.

        Args:
            type (str): The type of the Tigress special card.
            priority (int): The priority of the Tigress special card.
            bonus (int): The bonus associated with the Tigress special card.
        """
        super().__init__(type, priority, bonus)

    def to_dict(self):
        return {'type': self.type, 'priority': self.priority, 'bonus': self.bonus}    
    
# Define the Deck class for managing a deck of cards
class Deck:
    def __init__(self):
        """
        Initialize a deck of cards.
        """
        suits = ["Parrot", "Pirate Map", "Treasure Chest", "Jolly Roger"]
        # Acts as priority and number
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.cards = []  # Initialize an empty list to store cards
        specials = {
            "Pirate": 5,
            "Escape": 5,
            "Tigress": 1,
            "Skull King": 1
        }

        # Initialize the deck by creating standard and special cards
        self.make_deck(suits, numbers)
        self.make_special_deck(specials)

    def make_deck(self, suits, numbers):
        """
        Create standard playing cards and add them to the deck.

        Args:
            suits (list): List of card suits.
            numbers (list): List of card numbers.
        """
        for suit in suits:
            # Assign priority based on the suit
            match suit:
                case "Jolly Roger":
                    priority = 2
                case _:
                    priority = 1
            for number in numbers:
                if priority == 1:
                    # Assign bonus based on conditions
                    match number:
                        case 14:
                            bonus = 10
                        case _:
                            bonus = 0
                elif priority == 2:
                    # Assign bonus based on conditions
                    match number:
                        case 14:
                            bonus = 20
                        case _:
                            bonus = 0

                # Create and append a Card object to the deck
                self.cards.append(Card(suit, number, bonus, priority))

    def make_special_deck(self, specials):
        """
        Create special cards and add them to the deck.

        Args:
            specials (dict): Dictionary of special card types and quantities.
        """
        for key, value in specials.items():
            # Assign bonus and priority based on the special card type
            match key:
                case "Pirate":
                    bonus = 30
                    priority = 3
                case "Escape":
                    bonus = 0
                    priority = 0
                case "Skull King":
                    # Skull king bonus only used in expansion. Not used for now.
                    bonus = 40
                    priority = 4
            for _ in range(value):
                # Create and append a Special_Card object to the deck
                self.cards.append(Special_Card(key, priority, bonus))

    def shuffle(self):
        """
        Shuffle the deck's cards.
        """
        random.shuffle(self.cards)

    def deal(self):
        """
        Deal a card from the deck.

        Returns:
            Card: The card dealt from the deck, or None if the deck is empty.
        """
        if len(self.cards) > 0:
            return self.cards.pop()  # Remove and return the top card from the deck
        else:
            return None  # Return None if there are no more cards in the deck
    
    # def print_deck(self):
    #     """
    #     Deal and print some cards from the deck.
    #     """
    #     for _ in range(68):
    #         card = deck.deal()
    #         if card:
    #             print(card)  # Print the card if available
    #         else:
    #             print("No more cards in the deck.")  # Print a message if the deck is empty


# Create a deck and shuffle it for testing
# deck = Deck()
# deck.shuffle()
# deck.print_deck()



