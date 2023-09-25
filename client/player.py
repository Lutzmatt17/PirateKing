import uuid

# Define the Player class representing a player in the game
class Player:
    def __init__(self, username):
        """
        Initialize a player.

        Args:
            username (String): The username of the player.
        """
        self.username = username
        # List of cards representing the hand
        self.hand = []
        self.score = 0
        self.player_id = self.generate_unique_id()
    
    def get_hand(self):
        """
        Get the player's hand of cards.

        Returns:
            Hand: The player's hand of cards.
        """
        return self.hand
    
    def set_hand(self, hand):
        """
        Set the player's hand to a new hand of cards.

        Args:
            hand (Hand): A new hand of cards to replace the player's current hand.
        """
        self.hand = hand
    
    def print_hand(self):
        print("Hand:\n")
        i = 0
        for card in self.hand:
            print(str(i) + ": " + str(card))
            i += 1

    def get_score(self):
        """
        Get the player's score in the game.

        Returns:
            int: The player's score.
        """
        return self.score
    def set_score(self, score):
        self.score = score
    
    def get_username(self):
        return self.username
    
    def get_player_id(self):
        return self.player_id

    def generate_unique_id(self):
        return str(uuid.uuid4())

    def to_dict(self):
        return {'username': self.username, 'hand': self.hand, 'score': self.score, 'player_id': self.player_id}