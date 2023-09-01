class Hand:
    def __init__(self, amount, cards):
        self.amount = amount
        self.cards = cards
    
    def set_cards(self, cards):
        self.cards = cards

    def print_hand(self, cards):
        print(cards)

    def __str__(self):
        return f"Hand: {self.cards}"

