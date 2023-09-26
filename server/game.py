from deck import Deck
import random

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



    def print_hands(self):
        """
        Print the hands of all players in the game.
        """
        for player in self.players:
            print(player.get_username() + "'s " + "hand: ")
            player.get_hand().print_hand()

    def add_player(self, username):
        """
        Add a player to the local, non-networked version of the game.

        Args:
            username (String): The username of the player received from user input.
        """
        self.players.append(Player(username, Hand([]), 0))

    def join_players(self):
        join_command_format = "/join your_username"
        
        all_players_joined = False

        while not all_players_joined:
            join_input = input("Please join the game by typing the following:\n" + join_command_format)
            join_parts = join_input.split()
            join = join_parts[0]
            username = join_parts[1]

            if join != "/join":
                print("Please enter /join followed by your username")
            else:
                self.add_player(username)
                all_players_joined = self.join_player_again(all_players_joined)
            
           

    def join_player_again(self, all_players_joined):
            
            join_again_options = """
            Yes or No
            """

            join_again_bool = False
            while not join_again_bool:
                join_again = input("Would you like to add another player?\n" + join_again_options)
                if join_again == "No" and len(self.players) < 3:
                    print("Must have a minimum of 3 players to play.")
                elif join_again == "No" and len(self.players) >= 3:
                    all_players_joined = True
                    return all_players_joined
                elif join_again == "Yes" and len(self.players) > 8:
                    print("The max number of 8 players has been reached.")
                elif join_again != "Yes" and join_again != "No":
                    print("Must answer with yes or no.")
                elif join_again == "Yes" and len(self.players) < 8:
                    join_again_bool = True
                


    def start_game(self):
        """
        Start the game.
        """

        string_menu = '''
        1. Start Game
        2. Exit
        '''
        exit = False
        while not exit:
            user_input = input(string_menu)
            option = int(user_input)
            if option == 1:
                 exit = self.game()
            elif option == 2:
                exit(0)
            else:
                print("Please enter one of the valid menu options!")
    
    def game(self):
        game_over = False

        return game_over

# Define the PirateKingDriver class for managing the game setup
class PirateKingDriver:
    def __init__(self):
        """
        Initialize the Pirate King game driver.
        """
        self.deck = Deck()
        self.game = Game(self.deck)

    def main(self):
        """
        Main entry point for the Pirate King game.
        """
        # print("Welcome to Pirate King!\n")
        # self.game.start_game()
        self.game.join_players()
        for round in range(Game.MAX_ROUNDS):
            print("Round: ", round + 1, "\n")
            self.deck = Deck()
            self.game.set_deck(self.deck)
            self.deck.shuffle()
            self.game.deal_players(round + 1)
            self.game.print_hands()

if __name__ == "__main__":
    pirate_king_driver =  PirateKingDriver()
    pirate_king_driver.main()



