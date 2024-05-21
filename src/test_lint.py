from prompthandle.lintingTest import lintingTest

def main():
    text = """

class UserAccount:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def balance(self):
        return self.balance

"""
    print(text)
    lt = lintingTest(text)
    print(lt.run_lint(False))
main()