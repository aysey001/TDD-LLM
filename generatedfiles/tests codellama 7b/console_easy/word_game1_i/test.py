
import unittest
from game import Game
from player import Player
from sentence import Sentence
from hint import Hint
from console import Console

class TestGame(unittest.TestCase):
    def test_create_game(self):
        game = Game()
        self.assertIsInstance(game, Game)

    def test_create_player(self):
        player = Player()
        self.assertIsInstance(player, Player)

    def test_create_sentence(self):
        sentence = Sentence()
        self.assertIsInstance(sentence, Sentence)

    def test_create_hint(self):
        hint = Hint()
        self.assertIsInstance(hint, Hint)

    def test_create_console(self):
        console = Console()
        self.assertIsInstance(console, Console)

if __name__ == '__main__':
    unittest.main()
