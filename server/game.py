from deck import Deck
import random
import copy
import time

# Define the Game class to manage the Pirate King card game
class Game:
    MAX_ROUNDS = 10

    def __init__(self, players, game_id, action_translator, game_state_dict, game_state_acks_queue):
        """
        Initialize a new game of Pirate King.

        Args:
            deck (Deck): The deck of cards for the game.
            round (int): The number of rounds in the game.
            player_num (int): The number of players in the game.
        """
        self.players = players
        self.game_id = game_id
        self.action_translator = action_translator
        self.game_state_dict = game_state_dict
        self.game_state_acks_queue = game_state_acks_queue
        self.round = 1
        self.deck = None
        # List of cards representing a single trick
        self.trick = {}
        self.tricks = {}
        self.bids = {}
        self.hands = {}
        self.trick_winner = {}
        self.dealer = random.choice(self.players)
        # Index that keeps track of whose turn it is
        self.current_player = self.who_goes_first()
        self.phase = ""
        self.round_is_over = False
        self.leading_suit = ''

    def set_players(self, players):
        self.players = players

    def get_players(self):
        return self.players

    def set_deck(self, deck):
        self.deck = deck

    def get_deck(self):
        return self.deck

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
    
    def get_tricks(self):
        return self.tricks
    
    def get_phase(self):
        return self.phase
    
    def get_round_is_over(self):
        return self.round_is_over
    
    def get_hands(self):
        return self.hands
    
    def get_trick_winner(self):
        return self.trick_winner
    
    def get_player_from_id(self, player_id):
        for player in self.players:
            if player_id in player:
                return player
            
    def update_state(self, new_state):
        if new_state:
            self.__dict__ = new_state.__dict__

    # To be called inside the reducer on the new state
    def send_state(self):
        state_to_send = self.action_translator.game_state_to_network(self)
        self.game_state_dict['game_state'] = state_to_send
        self.action_translator.get_send_game_state_flag().set()

    
    def __deepcopy__(self, memo):

        new_instance = copy.copy(self)
        new_instance.players = copy.deepcopy(self.players, memo)
        new_instance.game_id = copy.deepcopy(self.game_id, memo)
        new_instance.round = copy.deepcopy(self.round, memo)
        new_instance.deck = copy.deepcopy(self.deck, memo)
        new_instance.trick = copy.deepcopy(self.trick, memo)
        new_instance.tricks = copy.deepcopy(self.tricks, memo)
        new_instance.bids = copy.deepcopy(self.bids, memo)
        new_instance.hands = copy.deepcopy(self.hands, memo)
        new_instance.trick_winner = copy.deepcopy(self.trick_winner, memo)
        new_instance.dealer = copy.deepcopy(self.dealer, memo)
        new_instance.current_player = copy.deepcopy(self.current_player, memo)
        new_instance.phase = copy.deepcopy(self.phase, memo)
        new_instance.round_is_over = copy.deepcopy(self.round_is_over, memo)
        new_instance.leading_suit = copy.deepcopy(self.leading_suit, memo)

        memo[id(self)] = new_instance

        return new_instance


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

    def deal_cards(self):
        print(f"Dealing cards...")
        for player in self.players:
            player_id = player.get('player_id')
            hand = self.deal_hand()
            self.hands[player_id] = hand

    def game_reducer(self, action=None):
        # if action is not None:
        #     if not self.validate_action(action):
        #         return False

        new_state = copy.deepcopy(self)

        if new_state.phase == "STARTING":
            # print(f"Starting...")
            new_state.init_round_variables()
            new_state.send_state()
            # new_state.game_state_dict.put(state_to_send)
            # print(self.game_state_dict.get('game_state'))
            if self.can_advance_game_state():
                new_state.phase = "DEALING"

        elif new_state.phase == "DEALING":
            new_state.deal_cards()
            new_state.send_state()
            # new_state.game_state_dict.put(state_to_send)
            if new_state.can_advance_game_state():
                new_state.phase = "START_BIDDING" 
       
        elif new_state.phase == "START_BIDDING":
            new_state.send_state()
            new_state.phase = "BIDDING"

        elif new_state.phase == "BIDDING":
            if action['type'] == 'BID' and new_state.validate_bid(action['player_id']):
                new_state.make_bid(action['player_id'], action['bid'])
            # Check if bidding is over and move to the next phase
            if len(new_state.get_bids()) == len(new_state.get_players()):
                new_state.send_state()
                new_state.phase = "START_PLAYING"

        elif new_state.phase == "START_PLAYING":
            new_state.send_state()
            new_state.phase = "PLAYING"

        elif new_state.phase == "PLAYING":
            if action['type'] == 'PLAY_CARD' and new_state.validate_play_card(action['player_id'], action['card_index']):
                new_state.play_card(action['player_index'], action['card'])
                new_state.send_state()

            # Check if the trick is complete and move to resolving phase
            if len(new_state.current_trick) == len(new_state.players):
                new_state.phase = "RESOLVING"

        elif new_state.phase == "RESOLVING":
            if action['type'] == 'RESOLVE_TRICK':
               winner_id = new_state.resolve_trick()
               winner = new_state.get_player_from_id(winner_id)
               new_state.current_player = new_state.players.index(winner) 
               new_state.send_state()

            # Check if the round is over and move to the next phase or round
            # Logic to check round completion goes here
            if new_state.round_is_over:
                new_state.round_number += 1
                new_state.phase = "BIDDING"
            else:
                new_state.phase = "START_PLAYING"

        # new_state.action_translator.get_send_game_state_flag().clear()
        return new_state

    def can_advance_game_state(self):
        while not self.game_state_acks_queue.full():
            pass
        
        acks_list = []
        while not self.game_state_acks_queue.empty():
            game_state_ack = self.game_state_acks_queue.get() 
            acks_list.append(game_state_ack)
        
        return all(ack == True for ack in acks_list)

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
    
    def validate_play_card(self, player_id, card_index):
        if not self.is_player_turn(player_id):
            valid_play = False
            print("It is not your turn...")
        else:
            player_hand = self.hands.get(player_id)
            card = player_hand[card_index]
            if card in player_hand:
                if not self.leading_suit:
                    valid_play = True
                    if 'suit' in card:
                        self.leading_suit = card.get('suit')
                    else:
                        # Made with the assumption that type "Tigress" will never be used because her type will be set to either escape or pirate in the client
                        if card.get('type') in ['Pirate', 'Skull King', 'Kraken', 'White Whale', 'Mermaid']:
                            self.leading_suit = "None Pirate"
                        else:
                            self.leading_suit = "None Escape"
                else:
                    if self.leading_suit == "None Pirate":
                        valid_play = True
                    elif self.leading_suit == "None Escape":
                        valid_play = True
                        if 'suit' in card:
                            self.leading_suit = card.get('suit')
                        else:
                            # Made with the assumption that type "Tigress" will never be used because her type will be set to either escape or pirate in the client
                            if card.get('type') in ['Pirate', 'Skull King', 'Kraken', 'White Whale', 'Mermaid']:
                                self.leading_suit = "None Pirate"
                            else:
                                self.leading_suit = "None Escape"
                    else:
                        if 'suit' in card:
                            if card.get('suit') == self.leading_suit:
                                valid_play = True
                            else:
                                valid_play = False
                        else:
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

    def init_round_variables(self):
        self.tricks = {}
        self.bids = {}
        self.round_is_over = False
        self.set_deck(Deck())
    
    def start_round(self):
        self.phase = "STARTING"
        new_state = self.game_reducer()
        self.update_state(new_state)

    def start_dealing_phase(self):
        # print(f"Dealing cards...")
        new_state = self.game_reducer()
        self.update_state(new_state)

    def start_bidding_phase(self, action_queue):
        # print(f"Started bidding phase...")
        new_state = self.game_reducer()

        while not action_queue.full():
            pass

        self.update_state(new_state)

    def accept_bids(self, action_queue):
        while not action_queue.empty():
            action = action_queue.get()
            new_state = self.game_reducer(action)
            self.update_state(new_state)

    def start_playing_phase(self):
        new_state = self.game_reducer()
        self.update_state(new_state)
    
    def play_round(self, action_queue):
        while not self.round_is_over:
            new_state = None

            while action_queue.empty():
                pass

            if not action_queue.empty():
                action = action_queue.get()
                new_state = self.game_reducer(action)

            self.update_state(new_state)

            if self.phase == "RESOLVING":
                new_state = self.game_reducer()
                self.start_playing_phase()
            else:
                self.advance_turn()

            self.update_state(new_state)

    def resolve_trick(self):
        highest_priority = -1
        highest_number = -1
        for player_id, card in self.trick.items():
            priority = card.get('priority')
            number = card.get('number')
            if priority > highest_priority:
                highest_priority = priority
                highest_number = number
                winner = player_id
            elif priority == highest_priority:
                suit = card.get('suit')
                number = card.get('number')
                if suit == self.leading_suit and number > highest_number:
                    highest_number = number
                    winner = player_id
        # Trick winner is a dict that holds the trick (array of the cards) that was won at the player_id of the winning player
        self.trick_winner[winner] = self.trick.values()
        
        self.determine_tricks(winner, self.trick_winner.get(winner))

        return winner

    def determine_tricks(self, winner, trick):
        if winner not in self.tricks:
            self.tricks[winner] = {}
        
        # Dictionary of all tricks won for that player in a round
        trick_dict = self.trick.get(winner)
        # Find the number of tricks already in the dictionary to determine the nth number of the trick we're currently adding
        trick_number = len(trick_dict)
        # Determine trick_string name based on previously found trick_number
        trick_string = "trick" + str(trick_number + 1)
        # Add the new trick array with trick_string as its key
        trick_dict[trick_string] = trick

    def game_loop(self, action_queue):
        while self.round < self.MAX_ROUNDS:
            # self.round += 1
            message = f"Starting round {self.round}"
            # print(message)
            self.start_round()
            self.start_dealing_phase()
            self.start_bidding_phase(action_queue)
            self.accept_bids(action_queue)
            self.start_playing_phase()