from deck import Deck
import random
import copy
import time

# Define the Game class to manage the Pirate King card game
class Game:
    MAX_ROUNDS = 10

    def __init__(self, players, game_id, action_translator, game_state_dict, action_queue):
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
        self.action_queue = action_queue
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
        self.previous_player = 0
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
    
    def get_previous_player(self):
        return self.players[self.previous_player]
    
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
    
    def trick_complete(self):
        return len(self.trick) == len(self.players)
    
    def get_player_from_id(self, player_id):
        for player in self.players:
            if player_id in player.values():
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
        new_instance.previous_player = copy.deepcopy(self.previous_player, memo)

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
            print(f"In the starting phase...")
            new_state.init_round_variables()
            new_state.send_state()
            # new_state.game_state_dict.put(state_to_send)
            # print(self.game_state_dict.get('game_state'))
            if new_state.can_advance_game_state():
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
                if new_state.can_advance_game_state():
                    new_state.phase = "START_PLAYING"

        elif new_state.phase == "START_PLAYING":
            # print("We are in the start playing phase...")
            new_state.send_state()
            new_state.phase = "PLAYING"

        elif new_state.phase == "PLAYING":
            print("We are in the playing phase...")
            if action['type'] == 'PLAY_CARD' and new_state.validate_play_card(action['player_id'], action['card_index']):
                new_state.play_card(action['player_id'], action['card_index'])
                new_state.previous_player = self.current_player
                if len(new_state.trick) < len(new_state.players):
                    new_state.advance_turn()
                    print(f"Advancing turn to {new_state.get_current_player().get('username')}")
            if new_state.action_queue.empty():
                new_state.send_state()

            # Check if the trick is complete and move to resolving phase
            if new_state.trick_complete() and self.can_advance_game_state():
                new_state.phase = "RESOLVING"

        elif new_state.phase == "RESOLVING":
            print("We are in the resolving phase...")
            winner_id = new_state.resolve_trick()
            # print(f"This is the winner_id: {winner_id}")
            winner = new_state.get_player_from_id(winner_id)
            print(f"This is the winning player: {winner}")
            new_state.current_player = new_state.players.index(winner) 
            new_state.leading_suit = ''
            new_state.trick = {}
            new_state.send_state()
            new_state.round_is_over = new_state.check_round_over()
            print(f"Round is over: {new_state.round_is_over}")

            # Check if the round is over and move to the next phase or round
            # Logic to check round completion goes here
            if new_state.round_is_over and new_state.can_advance_game_state():
                print("Incrementing round.... Going into STARTING phase...")
                new_state.round += 1
                new_state.phase = "STARTING"
            elif not new_state.round_is_over and new_state.can_advance_game_state():
                new_state.phase = "START_PLAYING"

        # new_state.action_translator.get_send_game_state_flag().clear()
        return new_state

    def can_advance_game_state(self):
        
        while not self.action_queue.full():
            pass
        
        acks_list = []
        while not self.action_queue.empty():
            game_action_ack = self.action_queue.get() 
            if game_action_ack.get('type') == 'ack':
                acks_list.append(True)

        return all(ack == True for ack in acks_list)
    
    def check_round_over(self):
        trick_sum = 0
        for trick_dict in self.tricks.values():
            trick_sum += len(trick_dict)

        return trick_sum == self.round
    
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
    
    def suit_not_in_hand(self, player_id):
        player_hand = self.hands.get(player_id)
        for card in player_hand:
            suit = card.get('suit')
            if suit == self.leading_suit:
                return False
        return True
       
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
                                if self.suit_not_in_hand(player_id):
                                    valid_play = True
                                else:
                                    valid_play = False
                        else:
                            valid_play = True
            else:
                valid_play = False
                print("That card is not in your hand...")            

        return valid_play

    def play_card(self, player_id, card_index):
        player_hand = self.hands.get(player_id)
        card = player_hand[card_index]
        player_hand.remove(card)
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
        self.leading_suit = ''
        self.tricks = {}
        self.trick_winner = {}
        self.trick = {}
        self.bids = {}
        self.round_is_over = False
        self.set_deck(Deck())
        self.deck.shuffle()
        # self.update_state()
    
    def start_round(self):
        self.phase = "STARTING"
        new_state = self.game_reducer()
        self.update_state(new_state)

    def start_dealing_phase(self):
        # print(f"Dealing cards...")
        new_state = self.game_reducer()
        self.update_state(new_state)

    def start_bidding_phase(self):
        # print(f"Started bidding phase...")
        new_state = self.game_reducer()

        while not self.action_queue.full():
            pass

        self.update_state(new_state)

    def accept_bids(self):
        while not self.action_queue.empty():
            action = self.action_queue.get()
            new_state = self.game_reducer(action)
            self.update_state(new_state)

    def start_playing_phase(self):
        new_state = self.game_reducer()
        self.update_state(new_state)
    
    def play_round(self):
        while not self.round_is_over:
            new_state = None

            while not self.action_queue.full():
                pass

            while not self.action_queue.empty():
                action = self.action_queue.get()
                # print(f"Processing action: {action}")
                new_state = self.game_reducer(action)
                self.update_state(new_state)
            print("Out of action loop...")
            if self.phase == "RESOLVING":
                new_state = self.game_reducer()
                if new_state.phase == "START_PLAYING":
                    new_state.start_playing_phase()

            self.update_state(new_state)

    def resolve_trick(self):
        highest_priority = -1
        highest_number = -1
        for player_id, card in self.trick.items():
            priority = card.get('priority')
            number = card.get('number')
            # print(number)
            if priority > highest_priority:
                highest_priority = priority
                highest_number = number
                winner = player_id
                # print(winner)
            elif priority == highest_priority:
                suit = card.get('suit')
                number = card.get('number')
                if suit == self.leading_suit and number > highest_number:
                    highest_number = number
                    winner = player_id
                    # print(winner)
        # Trick winner is a dict that holds the trick (array of the cards) that was won at the player_id of the winning player
        self.trick_winner = self.get_player_from_id(winner) 
        
        self.determine_tricks(winner, list(self.trick.values()))
        # print(winner)
        return winner

    def determine_tricks(self, winner, trick):
        if winner not in self.tricks:
            self.tricks[winner] = {}
        
        # Dictionary of all tricks won for that player in a round
        trick_dict = self.tricks.get(winner)
        # Find the number of tricks already in the dictionary to determine the nth number of the trick we're currently adding
        trick_number = len(trick_dict)
        # Determine trick_string name based on previously found trick_number
        trick_string = "trick" + str(trick_number + 1)
        # Add the new trick array with trick_string as its key
        trick_dict[trick_string] = trick

    def game_loop(self):
        while self.round < self.MAX_ROUNDS:
            if self.round > 1:
                print("Choosing next dealer...")
                self.choose_next_dealer()
                print("Choosing who goes first this round...")
                self.current_player = self.who_goes_first()
            
            self.start_round()
            self.start_dealing_phase()
            self.start_bidding_phase()
            self.accept_bids()
            self.start_playing_phase()
            self.play_round()