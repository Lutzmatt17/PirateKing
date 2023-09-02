from Hand import Hand
from Deck import Deck
from Player import Player

# Define the Game class to manage the Pirate King card game
class Game:
    MAX_ROUNDS = 10

    def __init__(self, deck):
        """
        Initialize a new game of Pirate King.

        Args:
            deck (Deck): The deck of cards for the game.
            round (int): The number of rounds in the game.
            player_num (int): The number of players in the game.
        """
        self.deck = deck
        self.players = []
        self.player_hands = []

    def set_deck(self, deck):
        self.deck = deck

    def deal_hand(self, deck, round):
        """
        Deal a hand of cards from the deck.

        Args:
            deck (Deck): The deck from which cards are dealt.

        Returns:
            list: A list of cards representing a hand.
        """
        hand = []
        for _ in range(round):
            card = deck.deal()
            hand.append(card)
        return hand

    def deal_players(self, round):
        """
        Deal hands to all players in the game.
        """
        for i in range(len(self.players)):
            self.players[i].set_hand(Hand(self.deal_hand(self.deck, round)))

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



