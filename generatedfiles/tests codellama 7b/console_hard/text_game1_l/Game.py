class Game:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.game_state = "not-started"
        self.options = ["Start Game", "Quit Game"]
        self.instructions = "Welcome to " + name + "! Please select an option from the menu."
        self.score = 0
        self.high_score = 0
        self.leaderboard = {}
        self.achievements = []
        self.tutorials = []
        self.credits = "Game Developed By: John Doe"
        self.exit_message = "Thank you for playing " + name + "! Would you like to play again?"
    def start(self):
        self.game_state = "in-progress"
    def end(self):
        self.game_state = "completed"
    def display_description(self):
        return self.description
    def display_options(self):
        return self.options
    def display_instructions(self):
        return self.instructions
    def display_score(self):
        return self.score
    def display_high_score(self):
        return self.high_score
    def display_leaderboard(self):
        return self.leaderboard
    def display_achievements(self):
        return self.achievements
    def display_tutorials(self):
        return self.tutorials
    def display_credits(self):
        return self.credits
    def display_exit_message(self):
        return self.exit_message
    def handle_user_input(self, user_input):
        if user_input == "Start Game":
            self.game_state = "in-progress"
        elif user_input == "Quit Game":
            self.game_state = "completed"
        else:
            print("Invalid Input")
    def validate_user_input(self, user_input):
        if user_input == "Start Game" or user_input == "Quit Game":
            return True
        else:
            return False
    def display_menu(self):
        return self.instructions
    def handle_game_logic(self):
        pass
    def handle_game_state(self):
        if self.game_state == "in-progress":
            self.handle_game_logic()
        elif self.game_state == "completed":
            self.handle_game_state()
        else:
            print("Invalid Game State")
    def handle_game_events(self):
        pass
    def handle_game_interactions(self):
        pass