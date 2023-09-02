# Define the Player class representing a player in the game
class Player:
    def __init__(self, username, hand, score):
        """
        Initialize a player.

        Args:
            username (String): The username of the player.
            hand (Hand): The player's hand of cards.
            score (int): The player's score in the game.
        """
        self.username = username
        self.hand = hand
        self.score = score
    
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