class BankingSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number, name):
        if account_number in self.accounts:
            raise ValueError("Account number already exists")
        self.accounts[account_number] = Account(name)
        return self.accounts[account_number]

    def deposit_money(self, account_number, amount):
        if account_number not in self.accounts:
            raise ValueError("Account number does not exist")
        self.accounts[account_number].deposit(amount)

    def withdraw_money(self, account_number, amount):
        if account_number not in self.accounts:
            raise ValueError("Account number does not exist")
        self.accounts[account_number].withdraw(amount)

    def check_balance(self, account_number):
        if account_number not in self.accounts:
            raise ValueError("Account number does not exist")
        return self.accounts[account_number].balance

    def transfer_money(self, src_acc_num, dst_acc_num, amount):
        if src_acc_num == dst_acc_num:
            raise ValueError("Source and destination account numbers must be different")
        if src_acc_num not in self.accounts or dst_acc_num not in self.accounts:
            raise ValueError("Account number does not exist")
        if amount < 0:
            raise ValueError("Amount must be positive")
        if self.accounts[src_acc_num].balance < amount:
            raise ValueError("Insufficient balance")
        self.accounts[src_acc_num].withdraw(amount)
        self.accounts[dst_acc_num].deposit(amount)

class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Amount must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient balance")
        self.balance -= amount

# self implemented
def main():
    bank = BankingSystem()
    bank.create_account("777777777", "John Doe")
    bank.deposit_money("777777777", 100)
    
    print(bank.accounts["777777777"].name)
    print(bank.check_balance("777777777"))

main()