[TESTS]
import unittest
import WordGuessGame

class TestWordGuessGame(unittest.TestCase):

    def test_intro(self):
        word_guess_game = WordGuessGame()
        word_guess_game.intro()
        self.assertIsNotNone(word_guess_game.current_word)
        self.assertIsNotNone(word_guess_game.current_hint)
        self.assertIsNotNone(word_guess_game.current_life_points)

    def test_get_sentences(self):
        word_guess_game = WordGuessGame()
        sentences = word_guess_game.get_sentences("player")
        self.assertIsInstance(sentences, list)
        self.assertGreater(len(sentences), 0)

    def test_get_random_sentence(self):
        word_guess_game = WordGuessGame()
        sentences = word_guess_game.get_sentences("player")
        random_sentence = word_guess_game.get_random_sentence(sentences)
        self.assertIsInstance(random_sentence, str)
        self.assertGreater(len(random_sentence), 0)

    def test_get_word(self):
        word_guess_game = WordGuessGame()
        sentence = "This is a sentence."
        word = word_guess_game.get_word(sentence)
        self.assertIsInstance(word, str)
        self.assertGreater(len(word), 0)
        self.assertNotEqual(word, " ")

    def test_guess_word(self):
        word_guess_game = WordGuessGame()
        sentence = "This is a sentence."
        word = word_guess_game.get_word(sentence)
        guessed = word_guess_game.guess_word(sentence, word)
        self.assertTrue(guessed)

    def test_print_sentence(self):
        word_guess_game = WordGuessGame()
        sentence = "This is a sentence."
        word_guess_game.print_sentence(sentence)
        self.assertIsNotNone(word_guess_game.current_sentence)
        self.assertIsInstance(word_guess_game.current_sentence, str)
        self.assertGreater(len(word_guess_game.current_sentence), 0)

    def test_print_hint(self):
        word_guess_game = WordGuessGame()
        hint = word_guess_game.print_hint()
        self.assertIsInstance(hint, str)
        self.assertGreater(len(hint), 0)

    def test_print_life_point(self):
        word_guess_game = WordGuessGame()
        life_points = word_guess_game.print_life_point()
        self.assertIsInstance(life_points, int)
        self.assertGreater(life_points, 0)

    def test_game_over(self):
        word_guess_game = WordGuessGame()
        word_guess_game.game_over()
        self.assertIsNotNone(word_guess_game.current_word)
        self.assertIsNotNone(word_guess_game.current_hint)
        self.assertIsNotNone(word_guess_game.current_life_points)
        self.assertIsNotNone(word_guess_game.final_message)
        self.assertIsNotNone(word_guess_game.winner)

    def test_main(self):
        word_guess_game = WordGuessGame()
        word_guess_game.main()
        self.assertIsNotNone(word_guess_game.current_word)
        self.assertIsNotNone(word_guess_game.current_hint)
        self.assertIsNotNone(word_guess_game.current_life_points)
        self.assertIsNotNone(word_guess_game.final_message)
        self.assertIsNotNone(word_guess_game.winner)

if __name__ == '__main__':
    unittest.main()
[/TESTS]