from deck import Deck
import random
import copy
import time
import asyncio


# Define the Game class to manage the Pirate King card game
class Game:
    """
    The Game class represents a game of Pirate King. It manages the game state, including the players, the deck of cards, 
    the current round, and the current phase of the game. It also handles game actions such as dealing cards, accepting bids, 
    and calculating scores.
    """
    MAX_ROUNDS = 10

    def __init__(self, players, game_id, action_translator, game_state_dict, action_queue):
        """
        Initialize a new game of Pirate King.

        Args:
            players (list): The list of players in the game.
            game_id (str): The unique identifier for the game.
            action_translator (ActionTranslator): The object that translates actions between the game and the network.
            game_state_dict (dict): The dictionary that holds the current game state.
            action_queue (Queue): The queue that holds the actions to be processed.
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
        self.score_sheet = {}
        self.dealer = random.choice(self.players)
        # Index that keeps track of whose turn it is
        self.current_player = self.who_goes_first()
        self.previous_player = 0
        self.phase = ""
        self.round_is_over = False
        self.leading_suit = ''

    def set_players(self, players):
        """
        Set the players for the game.

        Args:
            players (list): The list of players.
        """
        self.players = players

    def get_players(self):
        """
        Get the players in the game.

        Returns:
            list: The list of players.
        """
        return self.players

    def set_deck(self, deck):
        """
        Set the deck for the game.

        Args:
            deck (Deck): The deck of cards.
        """
        self.deck = deck

    def get_deck(self):
        """
        Get the deck of cards in the game.

        Returns:
            Deck: The deck of cards.
        """
        return self.deck

    async def increment_round(self):
        """
        Increment the round number by 1.
        """
        self.round += 1
    
    def get_round(self):
        """
        Get the current round number.

        Returns:
            int: The current round number.
        """
        return self.round

    def get_max_rounds(self):
        """
        Get the maximum number of rounds in the game.

        Returns:
            int: The maximum number of rounds.
        """
        return self.MAX_ROUNDS

    def get_game_id(self):
        """
        Get the game ID.

        Returns:
            str: The game ID.
        """
        return self.game_id

    def get_dealer(self):
        """
        Get the dealer of the game.

        Returns:
            Player: The dealer.
        """
        return self.dealer
    
    def get_current_player(self):
        """
        Get the current player whose turn it is.

        Returns:
            Player: The current player.
        """
        return self.players[self.current_player]
    
    def get_previous_player(self):
        """
        Get the previous player who just finished their turn.

        Returns:
            Player: The previous player.
        """
        return self.players[self.previous_player]
    
    def get_bids(self):
        """
        Get the bids made by the players.

        Returns:
            dict: The bids made by the players.
        """
        return self.bids
    
    def get_trick(self):
        """
        Get the current trick.

        Returns:
            dict: The current trick.
        """
        return self.trick
    
    def get_tricks(self):
        """
        Get all the tricks played in the game.

        Returns:
            dict: The tricks played in the game.
        """
        return self.tricks
    
    def get_phase(self):
        """
        Get the current phase of the game.

        Returns:
            str: The current phase of the game.
        """
        return self.phase
    
    def get_round_is_over(self):
        """
        Check if the current round is over.

        Returns:
            bool: True if the round is over, False otherwise.
        """
        return self.round_is_over
    
    def get_hands(self):
        """
        Get the hands of the players.

        Returns:
            dict: The hands of the players.
        """
        return self.hands
    
    def get_trick_winner(self):
        """
        Get the winner of the current trick.

        Returns:
            Player: The winner of the current trick.
        """
        return self.trick_winner
    
    async def get_score_sheet(self):
        """
        Get the score sheet of the game.

        Returns:
            dict: The score sheet of the game.
        """
        return self.score_sheet
    
    def trick_complete(self):
        """
        Check if the current trick is complete.

        Returns:
            bool: True if the trick is complete, False otherwise.
        """
        return len(self.trick) == len(self.players)
    
    def get_player_from_id(self, player_id):
        """
        Get a player from their ID.

        Args:
            player_id (str): The ID of the player.

        Returns:
            Player: The player with the given ID.
        """
        for player in self.players:
            if player_id in player.values():
                return player
            
    def update_state(self, new_state):
        """
        Update the game state.

        Args:
            new_state (Game): The new game state.
        """
        if new_state:
            self.__dict__ = new_state.__dict__

    def send_state(self):
        """
        Send the game state to the network.
        """
        state_to_send = self.action_translator.game_state_to_network(self)
        self.game_state_dict['game_state'] = state_to_send
        self.action_translator.get_send_game_state_flag().set()

    
    def __deepcopy__(self, memo):
        """
        Create a deep copy of the game.

        Args:
            memo (dict): The dictionary of already copied objects.

        Returns:
            Game: The deep copy of the game.
        """

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
        new_instance.score_sheet = copy.deepcopy(self.score_sheet, memo)

        memo[id(self)] = new_instance

        return new_instance


    def deal_hand(self):
        """
        Deal a hand of cards from the deck.

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
        """
        Deal cards to all players.
        """
        print(f"Dealing cards...")
        for player in self.players:
            player_id = player.get('player_id')
            hand = self.deal_hand()
            self.hands[player_id] = hand

    async def game_reducer(self, action=None):
        """
        Reduce the game state based on the given action.

        Args:
            action (dict): The action to be processed.

        Returns:
            Game: The new game state.
        """
        # if action is not None:
        #     if not self.validate_action(action):
        #         return False

        new_state = copy.deepcopy(self)

        if new_state.phase == "STARTING":
            print(f"In the starting phase...")
            new_state.init_round_variables()
            new_state.send_state()
            print("State is sent")
            # new_state.game_state_dict.put(state_to_send)
            # print(self.game_state_dict.get('game_state'))
            if await new_state.can_advance_game_state():
                new_state.phase = "DEALING"

        elif new_state.phase == "DEALING":
            print("In the dealing state")
            new_state.deal_cards()
            new_state.send_state()
            # new_state.game_state_dict.put(state_to_send)
            if await new_state.can_advance_game_state():
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
                if await new_state.can_advance_game_state():
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
            if new_state.trick_complete() and await self.can_advance_game_state():
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
            if new_state.round_is_over and await new_state.can_advance_game_state():
                new_state.phase = "CALCULATE_SCORES"
            elif not new_state.round_is_over and await new_state.can_advance_game_state():
                new_state.phase = "START_PLAYING"
        elif new_state.phase == "CALCULATE_SCORES":
            new_state.calculate_round_scores()
            new_state.send_state()

            if await new_state.can_advance_game_state():
                new_state.round += 1
                new_state.phase = "STARTING"

        # new_state.action_translator.get_send_game_state_flag().clear()
        return new_state

    async def can_advance_game_state(self):
        """
        Check if the game state can be advanced.

        Returns:
            bool: True if all actions in the queue have been acknowledged, False otherwise.
        """
        while not self.action_queue.full():
            await asyncio.sleep(0)  # yield control to the event loop
        
        acks_list = []
        while not self.action_queue.empty():
            game_action_ack = self.action_queue.get() 
            if game_action_ack.get('type') == 'ack':
                acks_list.append(True)

        return all(ack == True for ack in acks_list)
    
    def check_round_over(self):
        """
        Check if the round is over.

        Returns:
            bool: True if the sum of all tricks equals the round number, False otherwise.
        """
        trick_sum = 0
        for trick_dict in self.tricks.values():
            trick_sum += len(trick_dict)

        return trick_sum == self.round
    
    def make_bid(self, player_id, bid):
        """
        Make a bid for a player.

        Args:
            player_id (str): The ID of the player.
            bid (int): The bid amount.
        """
        self.bids[player_id] = bid
    
    def has_bid(self, player_id):
        """
        Check if a player has made a bid.

        Args:
            player_id (str): The ID of the player.

        Returns:
            bool: True if the player has made a bid, False otherwise.
        """
        if player_id in self.bids:
            has_bid = True
        else:
            has_bid = False
        return has_bid
    
    def validate_bid(self, player_id):
        """
        Validate a player's bid.

        Args:
            player_id (str): The ID of the player.

        Returns:
            bool: False if the player has already made a bid, True otherwise.
        """
        if self.has_bid(player_id):
            validate_bid = False
        else:
            validate_bid = True
        return validate_bid
    
    def suit_not_in_hand(self, player_id):
        """
        Check if a player's hand does not contain the leading suit.

        Args:
            player_id (str): The ID of the player.

        Returns:
            bool: True if the player's hand does not contain the leading suit, False otherwise.
        """
        player_hand = self.hands.get(player_id)
        for card in player_hand:
            suit = card.get('suit')
            if suit == self.leading_suit:
                return False
        return True
       
    def validate_play_card(self, player_id, card_index):
        """
        Validate a player's card play.

        Args:
            player_id (str): The ID of the player.
            card_index (int): The index of the card in the player's hand.

        Returns:
            bool: True if the card play is valid, False otherwise.
        """
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
        """
        Removes a card from a player's hand and adds it to the current trick.

        Args:
            player_id (str): The ID of the player.
            card_index (int): The index of the card in the player's hand.
        """
        player_hand = self.hands.get(player_id)
        card = player_hand[card_index]
        player_hand.remove(card)
        self.trick[player_id] = card

    def choose_next_dealer(self):
        """
        Chooses the next dealer from the current players in the game.

        Returns:
            Player: The next dealer.
        """
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
        """
        Determines who goes first in the game.

        Returns:
            int: The index of the first player.
        """
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
        """
        Checks if it is a player's turn.

        Args:
            player_id (str): The ID of the player.

        Returns:
            bool: True if it is the player's turn, False otherwise.
        """
        return self.players[self.current_player].get('player_id') == player_id

    def advance_turn(self):
        """
        Advances the turn to the next player.
        """
        self.current_player = (self.current_player + 1) % len(self.players)

    def init_round_variables(self):
        """
        Initializes the variables for a round.
        """
        self.leading_suit = ''
        self.tricks = {}
        self.trick_winner = {}
        self.trick = {}
        self.bids = {}
        self.round_is_over = False
        self.set_deck(Deck())
        self.deck.shuffle()
        # self.update_state()
    
    async def start_round(self):
        """
        Starts a round.
        """
        self.phase = "STARTING"
        new_state = await self.game_reducer()
        self.update_state(new_state)

    async def start_dealing_phase(self):
        """
        Starts the dealing phase.
        """
        # print(f"Dealing cards...")
        new_state = await self.game_reducer()
        self.update_state(new_state)

    async def start_bidding_phase(self):
        """
        Starts the bidding phase.
        """
        # print(f"Started bidding phase...")
        new_state = await self.game_reducer()

        while not self.action_queue.full():
            await asyncio.sleep(0)

        self.update_state(new_state)

    async def accept_bids(self):
        """
        Accepts the bids from the players.
        """
        while not self.action_queue.empty():
            action = self.action_queue.get()
            new_state = await self.game_reducer(action)
            self.update_state(new_state)

    async def start_playing_phase(self):
        """
        Starts the playing phase.
        """
        new_state = await self.game_reducer()
        self.update_state(new_state)
    
    async def start_calculate_score_phase(self):
        """
        Starts the score calculation phase.
        """
        new_state = await self.game_reducer()
        self.update_state(new_state)
    
    async def play_round(self):
        """
        Plays a round.
        """
        while not self.round_is_over:
            new_state = None

            while not self.action_queue.full():
                await asyncio.sleep(0)

            while not self.action_queue.empty():
                action = self.action_queue.get()
                # print(f"Processing action: {action}")
                new_state = await self.game_reducer(action)
                self.update_state(new_state)
            print("Out of action loop...")
            if self.phase == "RESOLVING":
                new_state = await self.game_reducer()
                if new_state.phase == "START_PLAYING":
                    new_state.start_playing_phase()

            self.update_state(new_state)

    def resolve_trick(self):
        """
        Resolves a trick.

        Returns:
            str: The ID of the winner.
        """
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
        """
        Determines the tricks won by a player.

        Args:
            winner (str): The ID of the winner.
            trick (list): The trick won.
        """
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

    def calculate_round_scores(self):
        """
        Calculates the scores for a round.
        """
        for player_id, bid in self.bids.items():
            print(f"Player id: {player_id}")
            player = self.get_player_from_id(player_id)
            username = player.get('username')
            print(f"Username: {username}")
            if not self.score_sheet.get(username):
                self.score_sheet[username] = 0
            if bid == 0:
                if not self.tricks.get(player_id):
                    self.score_sheet[username] += (self.round * 10)
                else:
                    self.score_sheet[username] += (self.round * -10)
            else:
                if self.tricks.get(player_id):
                    if len(self.tricks.get(player_id)) == bid:
                        self.score_sheet[username] += (bid * 20)
                        total_bonus = self.calculate_bonuses(player_id)
                        self.score_sheet[username] += total_bonus
                    else:
                        num_tricks = len(self.tricks.get(player_id))
                        self.score_sheet[username] += (abs(bid - num_tricks) * -10)
                else:
                    self.score_sheet[username] += (bid * -10)
    
    def calculate_bonuses(self, player_id):
        """
        Calculates the bonuses for a player.

        Args:
            player_id (str): The ID of the player.

        Returns:
            int: The total bonus.
        """
        tricks_won = self.tricks.get(player_id)
        total_bonus = 0
        for trick in tricks_won.values():
            skull_king = False
            for card in trick:
                if 'suit' in card:
                    total_bonus += card.get('bonus')
                else:
                    if card.get('type') == 'Skull King':
                        skull_king = True
                    elif card.get('type') == 'Pirate' and skull_king:
                        total_bonus += card.get('bonus')

        return total_bonus
        
    async def game_loop(self):
        """
        Runs the game loop.
        """
        while self.round < self.MAX_ROUNDS:
            if self.round > 1:
                print("Choosing next dealer...")
                self.choose_next_dealer()
                print("Choosing who goes first this round...")
                self.current_player = self.who_goes_first()
            
            await self.start_round()
            await self.start_dealing_phase()
            await self.start_bidding_phase()
            await self.accept_bids()
            await self.start_playing_phase()
            await self.play_round()
            await self.start_calculate_score_phase()
