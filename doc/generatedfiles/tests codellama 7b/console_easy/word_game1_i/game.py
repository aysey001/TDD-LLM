
class Game:
    def __init__(self):
        self.players = []
        self.sentences = []
        self.hints = []

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

class Sentence:
    def __init__(self, text):
        self.text = text

class Hint:
    def __init__(self, text):
        self.text = text

class Console:
    def __init__(self):
        self.game = Game()
        self.player = Player("Test Player")
        self.sentence = Sentence("Test Sentence")
        self.hint = Hint("Test Hint")

    def start(self):
        print("Welcome to Hangman!")
        print("Please enter a word or phrase:")
        self.sentence = Sentence(input())
        print("Please enter a hint:")
        self.hint = Hint(input())
        print("Please enter your name:")
        self.player = Player(input())
        self.game = Game()
        self.game.players.append(self.player)
        self.game.sentences.append(self.sentence)
        self.game.hints.append(self.hint)
        self.play_game()

    def play_game(self):
        print(f"Welcome, {self.player.name}! You have 6 chances to guess the word.")
        for guess in range(6):
            print(f"Guess {guess+1}:")
            guess = input().lower()
            if guess in self.sentence.text:
                print("Correct!")
                self.player.score += 1
            else:
                print("Incorrect. Try again.")
        print(f"Game over, {self.player.name}! Your final score was {self.player.score}.")
        input("Press enter to continue...")
        self.start()

if __name__ == '__main__':
    console = Console()
    console.start()