from deck import Deck
import random
import copy

# Define the Game class to manage the Pirate King card game
class Game:
    MAX_ROUNDS = 10

    def __init__(self, players, room, game_id):
        """
        Initialize a new game of Pirate King.

        Args:
            deck (Deck): The deck of cards for the game.
            round (int): The number of rounds in the game.
            player_num (int): The number of players in the game.
        """
        self.round = 1
        self.deck = None
        self.game_id = game_id
        self.players = players
        self.room = room
        # List of cards representing a single trick
        self.trick = []
        self.tricks = {}
        self.bids = {}
        self.dealer = random.choice(self.players)
        # Index that keeps track of whose turn it is
        self.current_player = self.who_goes_first()
        self.phase = "DEALING"
        self.round_is_over = False

    def set_players(self, players):
        self.players = players

    def get_players(self):
        return self.players

    def set_deck(self, deck):
        self.deck = deck

    def get_deck(self):
        return self.deck
    
    def get_room(self):
        return self.room

    def increment_round(self):
        self.round += 1
    
    def get_round(self):
        return self.round

    def get_max_rounds(self):
        return self.MAX_ROUNDS

    def get_game_id(self):
        return self.game_id

    def get_dealer(self):
        return self.dealer
    
    def get_current_player(self):
        return self.players[self.current_player]
    
    def get_bids(self):
        return self.bids
    
    def get_trick(self):
        return self.trick

    def deal_hand(self):
        """
        Deal a hand of cards from the deck.

        Args:
            deck (Deck): The deck from which cards are dealt.

        Returns:
            list: A list of cards representing a hand.
        """
        hand = []
        for _ in range(self.round):
            card = self.deck.deal()
            card_dict = card.to_dict()
            hand.append(card_dict)
        return hand


    def game_reducer(self, action):
        if not self.validate_action(action):
            return False

        new_state = copy.deepcopy(self)

        if self.phase == "DEALING":
            if action['type'] == 'DEAL_CARDS':
                new_state.deal_cards()
                new_state.phase = "BIDDING" 
        elif self.phase == "BIDDING":
            if action['type'] == 'MAKE_BID':
                new_state.make_bid(action['player_index'], action['bid_amount'])

            # Check if bidding is over and move to the next phase
            if all(player.bid > 0 for player in new_state.players):
                new_state.phase = "PLAYING"

        elif self.phase == "PLAYING":
            if action['type'] == 'PLAY_CARD':
                new_state.play_card(action['player_index'], action['card'])

            # Check if the trick is complete and move to resolving phase
            if len(new_state.current_trick) == len(new_state.players):
                new_state.phase = "RESOLVING"

        elif self.phase == "RESOLVING":
            if action['type'] == 'RESOLVE_TRICK':
                new_state.resolve_trick()

            # Check if the round is over and move to the next phase or round
            # Logic to check round completion goes here
            if self.round_is_over:
                new_state.round_number += 1
                new_state.phase = "BIDDING"

        return new_state


    def make_bid(self, player_id, bid):
        self.bids[player_id] = bid
    
    def has_bid(self, player_id):
        if player_id in self.bids:
            has_bid = True
        else:
            has_bid = False
        return has_bid
    
    def validate_bid(self, player_id):
        if self.has_bid(player_id):
            validate_bid = False
        else:
            validate_bid = True
        return validate_bid
    
    def validate_play_card(self, player_id, card):
        if not self.is_player_turn(player_id):
            valid_play = False
            print("It is not your turn...")
        else:
            player = self.players[self.current_player]
            if card in player.get('hand'):
                valid_play = True
            else:
                valid_play = False
                print("That card is not in your hand...")            
        
        return valid_play

    def play_card(self, player_id, card):
        player = self.players[self.current_player]
        hand = player.get('hand')
        hand.remove(card)
        self.trick[player_id] = card

    # Function that chooses the first "dealer" at random
    # among the current players in the game
    def choose_next_dealer(self):
        current_dealer_index = self.players.index(self.dealer)
        # If the current dealer is not the last player in the list,
        # add 1 to the index to find the next one.
        if current_dealer_index < (len(self.players) - 1):
            dealer = self.players[current_dealer_index + 1]
        # If the current dealer is the last player,
        # loop back around to the first person
        elif current_dealer_index == (len(self.players) - 1):
            dealer = self.players[0]

        self.dealer = dealer
        return self.dealer

    def who_goes_first(self):
        dealer_index = self.players.index(self.dealer)
           # If the current dealer is not the last player in the list,
        # add 1 to the index to find the next one.
        if dealer_index < (len(self.players) - 1):
            first_player = self.players[dealer_index + 1]
        # If the current dealer is the last player,
        # loop back around to the first person
        elif dealer_index == (len(self.players) - 1):
            first_player = self.players[0]

        return self.players.index(first_player)

    def is_player_turn(self, player_id):
        return self.players[self.current_player].get('player_id') == player_id

    def advance_turn(self):
        self.current_player = (self.current_player + 1) % len(self.players)
