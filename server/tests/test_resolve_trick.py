import unittest
from unittest.mock import Mock
from game import Game

class TestResolveTrick(unittest.TestCase):
    
    def setUp(self):
        arg1 = Mock()
        arg2 = Mock()
        arg3 = Mock()
        arg4 = Mock()
        arg5 = Mock()
        self.game_instance = Game(arg1, arg2, arg3, arg4, arg5)
    
    def test_highest_priority_wins(self):
        self.game_instance.trick = {
            'player1': {'priority': 1, 'number': 5, 'suit': 'Parrot'},
            'player2': {'priority': 1, 'number': 2, 'suit': 'Pirate Map'},
            'player3': {'priority': 1, 'number': 3, 'suit': 'Treasure Chest'},
            'player4': {'priority': 2, 'number': 3, 'suit': 'Jolly Roger'}
        }
        self.game_instance.leading_suit = 'Parrot'
        
        winner = self.game_instance.resolve_trick()
        self.assertEqual(winner, 'player4')
    
    def test_same_priority_different_suits(self):
        self.game_instance.trick = {
            'player1': {'priority': 1, 'number': 5, 'suit': 'Treasure Chest'},
            'player2': {'priority': 1, 'number': 2, 'suit': 'Parrot'},
            'player3': {'priority': 1, 'number': 2, 'suit': 'Pirate Map'}
        }
        self.game_instance.leading_suit = 'Treasure Chest'
        
        winner = self.game_instance.resolve_trick()
        self.assertEqual(winner, 'player1')
        
    def test_same_priority_same_suit_higher_number(self):
        self.game_instance.trick = {
            'player1': {'priority': 1, 'number': 5, 'suit': 'Pirate Map'},
            'player2': {'priority': 1, 'number': 7, 'suit': 'Pirate Map'}
        }
        self.game_instance.leading_suit = 'Pirate Map'
        
        winner = self.game_instance.resolve_trick()
        self.assertEqual(winner, 'player2')
    
    def test_skull_king_win(self):
        self.game_instance.trick = {
            'player1': {'priority': 0, 'bonus': 0, 'type': 'Escape'},
            'player2': {'priority': 4, 'bonus': 0, 'type': 'Skull King'},
            'player3': {'priority': 0, 'bonus': 0, 'type': 'Tigress'}
        }
        self.game_instance.leading_suit = 'Escape'
        winner = self.game_instance.resolve_trick()
        self.assertEqual(winner, 'player2')
    
    def test_check_round_over(self):
        self.game_instance.tricks = {
            'player1': {'trick1': [{'priority': 4, 'bonus': 0, 'type': 'Skull King'}, 
                                   {'priority': 0, 'bonus': 0, 'type': 'Escape'}, {'priority': 0, 'bonus': 0, 'type': 'Tigress'}],
                        'trick2': [{'priority': 4, 'bonus': 0, 'type': 'Skull King'}, 
                                   {'priority': 0, 'bonus': 0, 'type': 'Escape'}, {'priority': 0, 'bonus': 0, 'type': 'Tigress'}]},
            'player2': {'trick1': [{'priority': 4, 'bonus': 0, 'type': 'Skull King'}, 
                                   {'priority': 0, 'bonus': 0, 'type': 'Escape'}, {'priority': 0, 'bonus': 0, 'type': 'Tigress'}],
                        'trick2': [{'priority': 4, 'bonus': 0, 'type': 'Skull King'}, 
                                   {'priority': 0, 'bonus': 0, 'type': 'Escape'}, {'priority': 0, 'bonus': 0, 'type': 'Tigress'}]},
            'player3': {'trick1': [{'priority': 4, 'bonus': 0, 'type': 'Skull King'}, 
                                   {'priority': 0, 'bonus': 0, 'type': 'Escape'}, {'priority': 0, 'bonus': 0, 'type': 'Tigress'}],
                        'trick2': [{'priority': 4, 'bonus': 0, 'type': 'Skull King'}, 
                                   {'priority': 0, 'bonus': 0, 'type': 'Escape'}, {'priority': 0, 'bonus': 0, 'type': 'Tigress'}],
                        'trick3': [{'priority': 4, 'bonus': 0, 'type': 'Skull King'}, 
                                   {'priority': 0, 'bonus': 0, 'type': 'Escape'}, {'priority': 0, 'bonus': 0, 'type': 'Tigress'}],
                        'trick4': [{'priority': 4, 'bonus': 0, 'type': 'Skull King'}, 
                                   {'priority': 0, 'bonus': 0, 'type': 'Escape'}, {'priority': 0, 'bonus': 0, 'type': 'Tigress'}],
                        'trick5': [{'priority': 4, 'bonus': 0, 'type': 'Skull King'}, 
                                   {'priority': 0, 'bonus': 0, 'type': 'Escape'}, {'priority': 0, 'bonus': 0, 'type': 'Tigress'}]}
        }
        
        self.game_instance.round = 9
        is_round_over = self.game_instance.check_round_over()
        self.assertEqual(is_round_over, True)
if __name__ == '__main__':
    unittest.main()