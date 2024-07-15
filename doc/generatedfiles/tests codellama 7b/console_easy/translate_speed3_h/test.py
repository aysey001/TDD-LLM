
import unittest
import os
import time
from collections import defaultdict

class TestHangmanGame(unittest.TestCase):

    def test_load_words(self):
        game = HangmanGame()
        game.load_words()
        self.assertGreater(len(game.words), 0)
        self.assertIn("word", game.words)
        self.assertIn("definition", game.words["word"])

    def test_get_random_word(self):
        game = HangmanGame()
        game.load_words()
        random_word = game.get_random_word()
        self.assertIn(random_word, game.words)

    def test_display_random_word(self):
        game = HangmanGame()
        game.load_words()
        random_word = game.get_random_word()
        display = game.display_random_word(random_word)
        self.assertIn("word", display)
        self.assertIn("definition", display["word"])

    def test_display_random_word(self):
        game = HangmanGame()
        game.load_words()
        random_word = game.get_random_word()
        display = game.display_random_word(random_word)
        self.assertIn("word", display)
        self.assertIn("definition", display["word"])

    def test_start_game(self):
        game = HangmanGame()
        game.load_words()
        game.start_game()
        self.assertEqual(game.score, 0)
        self.assertTrue(game.timer)
        self.assertIn("word", game.current_word)
        self.assertIn("definition", game.current_word["word"])
        self.assertIn("_", game.current_word["guess"])
        self.assertEqual(game.lives, 6)

    def test_wait_for_input(self):
        game = HangmanGame()
        game.load_words()
        game.start_game()
        game.wait_for_input()
        self.assertIn("word", game.current_word)
        self.assertIn("definition", game.current_word["word"])
        self.assertIn("_", game.current_word["guess"])
        self.assertEqual(game.lives, 6)

    def test_check_input(self):
        game = HangmanGame()
        game.load_words()
        game.start_game()
        game.wait_for_input()
        game.check_input("a")
        self.assertIn("word", game.current_word)
        self.assertIn("definition", game.current_word["word"])
        self.assertIn("a", game.current_word["guess"])
        self.assertEqual(game.lives, 6)

    def test_update_score(self):
        game = HangmanGame()
        game.load_words()
        game.start_game()
        game.wait_for_input()
        game.check_input("a")
        game.update_score()
        self.assertEqual(game.score, 1)
        self.assertTrue(game.timer)
        self.assertIn("word", game.current_word)
        self.assertIn("definition", game.current_word["word"])
        self.assertIn("a", game.current_word["guess"])
        self.assertEqual(game.lives, 6)

    def test_game_over(self):
        game = HangmanGame()
        game.load_words()
        game.start_game()
        game.wait_for_input()
        game.check_input("a")
        game.update_score()
        game.game_over()
        self.assertEqual(game.score, 1)
        self.assertFalse(game.timer)
        self.assertIn("word", game.current_word)
        self.assertIn("definition", game.current_word["word"])
        self.assertIn("a", game.current_word["guess"])
        self.assertEqual(game.lives, 6)

if __name__ == '__main__':
    unittest.main()
