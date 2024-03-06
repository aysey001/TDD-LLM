class UserAccount:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def balance(self):
        return self.balance

aydin = UserAccount(100)
hassan = UserAccount(200)

print(aydin.balance)
print(hassan.balance)

# E0202 cannot reach balance() method, method is hidden by balance attribute
print(aydin.balance())
print(hassan.balance())

