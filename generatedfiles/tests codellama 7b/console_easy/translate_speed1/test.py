
import unittest
import Hangman

class TestHangman(unittest.TestCase):

    def test_load_words(self):
        words = Hangman.load_words("words.txt")
        self.assertIsInstance(words, dict)
        self.assertTrue(len(words) > 0)
        self.assertIn("apple", words)
        self.assertIn("banana", words)
        self.assertIn("cherry", words)

    def test_display_word(self):
        word = Hangman.display_word("apple")
        self.assertEqual(word, "apple")

    def test_start_timer(self):
        timer = Hangman.start_timer()
        self.assertIsInstance(timer, float)
        self.assertTrue(timer > 0)

    def test_check_input(self):
        word = "apple"
        input = "a"
        correct = Hangman.check_input(word, input)
        self.assertTrue(correct)
        input = "b"
        correct = Hangman.check_input(word, input)
        self.assertFalse(correct)
        input = "c"
        correct = Hangman.check_input(word, input)
        self.assertFalse(correct)

    def test_end_timer(self):
        timer = Hangman.end_timer(Hangman.start_timer())
        self.assertIsInstance(timer, float)
        self.assertTrue(timer > 0)

    def test_print_result(self):
        word = "apple"
        correct = True
        result = Hangman.print_result(word, correct)
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("apple"))
        self.assertIn("correct", result)
        word = "banana"
        correct = False
        result = Hangman.print_result(word, correct)
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("banana"))
        self.assertIn("incorrect", result)

if __name__ == '__main__':
    unittest.main()
