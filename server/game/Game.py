from Hand import Hand
from Deck import Deck

class Game:
    def __init__(self, deck, round, player_num):
        self.deck  = deck
        self.round = round
        self.player_num = player_num
        self.player_hands = []
    
    def deal_hand(self, deck, round):
        hand = []
        for _ in range(round):
            card = deck.deal()
            hand.append(card)
        print(hand)
        return hand
    
    def deal_players(self, deck, player_num, round):
        for _ in range(player_num):
            self.player_hands.append(Hand(round, self.deal_hand(deck, round)))

    def print_hands(self):
        # print(self.player_hands)
        for hand in self.player_hands:
            print("Hand: ")
            for card in hand.cards:
                print("Card: ", card)

deck = Deck()
deck.shuffle()
game = Game(deck, 5, 5)
game.deal_players(deck, 5, 5)
game.print_hands()