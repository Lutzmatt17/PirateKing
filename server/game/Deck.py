import random

class Card:
    def __init__(self, suit, number, bonus, priority):
        self.suit = suit
        self.number = number
        self.bonus = bonus
        self.priority = priority

    def __str__(self):
        return f"{self.number} of {self.suit} with bonus of {self.bonus} and priority of {self.priority}"
    

class Special_Card:
    def __init__(self, type, priority, bonus):
        self.type = type
        self.priority = priority
        self.bonus = bonus
    
    def __str__(self):
        return f"{self.type} with bonus of {self.bonus} and priority of {self.priority}"

class Tigress(Special_Card):
    def __init__(self, type, priority, bonus):
        super().__init__(type, priority, bonus)

class Deck:
    def __init__(self):
        suits = ["Parrot", "Pirate Map", "Treasure Chest", "Jolly Roger"]
        # acts as priority and number
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.cards = []
        specials = {
            "Pirate": 5,
            "Escape": 5,
            "Tigress": 1,
            "Skull King": 1
        }

        # self.cards = [Card(suit, number) for suit in suits for number in numbers]

        self.make_deck(suits, numbers)
        self.make_special_deck(specials)

    def make_deck(self, suits, numbers):
        for suit in suits:
            match suit:
                case "Jolly Roger":
                    priority = 2
                case _:
                    priority = 1
            for number in numbers:
                if priority == 1:
                    match number:
                        case 14:
                            bonus = 10
                        case _:
                            bonus = 0
                elif priority == 2:
                    match number:
                        case 14:
                            bonus = 20
                        case _:
                            bonus = 0

                self.cards.append(Card(suit, number, bonus, priority))

    def make_special_deck(self, specials):
          for key, value in specials.items():
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
                self.cards.append(Special_Card(key, priority, bonus))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None
    
    def print_deck(self):
        # Deal and print some cards
        for _ in range(68):
            card = deck.deal()
            if card:
                print(card)
            else:
                print("No more cards in the deck.")

# Create a deck and shuffle it
deck = Deck()
# deck.shuffle()
# deck.print_deck()


