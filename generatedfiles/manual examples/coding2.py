task ="""[INST]
[PYTHON]
import unittest
from banking_system import BankingSystem, Account

class TestBankingSystem(unittest.TestCase):
    #Test cases for the Banking System

    def test_create_account(self):
        #Test case to create a new account
        bank = BankingSystem()
        acc = bank.create_account("1234567890", "John Doe")
        self.assertIsInstance(acc, Account)
        self.assertEqual(acc.account_number, "1234567890")
        self.assertEqual(acc.name, "John Doe")

    def test_deposit_money(self):
        #Test case to deposit money in an account
        bank = BankingSystem()
        acc = bank.create_account("1234567890", "John Doe")
        self.assertEqual(acc.balance, 0)
        bank.deposit_money("1234567890", 100)
        self.assertEqual(acc.balance, 100)

    def test_withdraw_money(self):
        #Test case to withdraw money from an account
        bank = BankingSystem()
        acc = bank.create_account("1234567890", "John Doe")
        self.assertEqual(acc.balance, 0)
        bank.deposit_money("1234567890", 100)
        self.assertEqual(acc.balance, 100)
        bank.withdraw_money("1234567890", 50)
        self.assertEqual(acc.balance, 50)

    def test_check_balance(self):
        #Test case to check the balance of an account
        bank = BankingSystem()
        acc = bank.create_account("1234567890", "John Doe")
        self.assertEqual(acc.balance, 0)
        bank.deposit_money("1234567890", 100)
        self.assertEqual(bank.check_balance("1234567890"), 100)

    def test_transfer_money(self):
        #Test case to transfer money between accounts
        bank = BankingSystem()
        acc1 = bank.create_account("1234567890", "John Doe")
        acc2 = bank.create_account("2234567890", "Jane Doe")
        self.assertEqual(acc1.balance, 0)
        self.assertEqual(acc2.balance, 0)
        bank.deposit_money("1234567890", 100)
        bank.transfer_money("1234567890", "2234567890", 50)
        self.assertEqual(acc1.balance, 50)
        self.assertEqual(acc2.balance, 50)

if __name__ == '__main__':
    unittest.main()
[/PYTHON]
[/INST]
"""

prompt ="""Your task is to provide python-code to solve the following test assertions.
Consider all mentioned classes, libaries and function-signatures and add new ones if needed.
Do not write texts. Do not assume any other role than the assistant. Do not use any other language than Python.
Always wrap your answer in [PYTHON][/PYTHON] tags.

#Here is an example of the given test assertions:
[PYTHON]
import unittest

class TestInventoryManagementSystem(unittest.TestCase):

    def test_create_inventory_management_system(self):
        inventory_system = InventoryManagementSystem()
        self.assertIsInstance(inventory_system, InventoryManagementSystem)

    def test_add_product(self):
        inventory_system = InventoryManagementSystem()
        inventory_system.add_product("Item1", 10, 5.99)
        self.assertIn("Item1", inventory_system.products)

    def test_update_quantity(self):
        inventory_system = InventoryManagementSystem()
        inventory_system.add_product("Item1", 10, 5.99)
        inventory_system.update_quantity("Item1", 15)
        self.assertEqual(inventory_system.products["Item1"]["quantity"], 15)

    def test_set_price(self):
        inventory_system = InventoryManagementSystem()
        inventory_system.add_product("Item1", 10, 5.99)
        inventory_system.set_price("Item1", 7.99)
        self.assertEqual(inventory_system.products["Item1"]["price"], 7.99)

    def test_view_inventory(self):
        inventory_system = InventoryManagementSystem()
        inventory_system.add_product("Item1", 10, 5.99)
        inventory_system.add_product("Item2", 5, 9.99)
        inventory_view = inventory_system.view_inventory()
        self.assertIn("Item1", inventory_view)
        self.assertIn("Item2", inventory_view)

if __name__ == '__main__':
    unittest.main()
[/PYTHON]

#Here is an example of the code you should provide:
[PYTHON]
class InventoryManagementSystem:
    def __init__(self):
        self.products = {}

    def add_product(self, name, quantity, price):
        if not isinstance(quantity, int) or not isinstance(price, (int, float)):
            raise ValueError("Invalid quantity or price")
        self.products[name] = {"quantity": quantity, "price": price}

    def update_quantity(self, name, new_quantity):
        if name not in self.products:
            raise ValueError(f"Product {name} not found")
        self.products[name]["quantity"] = new_quantity

    def set_price(self, name, new_price):
        if name not in self.products:
            raise ValueError(f"Product {name} not found")
        self.products[name]["price"] = new_price

    def view_inventory(self):
        return list(self.products.keys())


def main():
    inventory_system = InventoryManagementSystem()

    while True:
        print("\nMenu:")
        print("1. Add Product")
        print("2. Update Quantity")
        print("3. Set Price")
        print("4. View Inventory")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == "5":
            print("Exiting the Inventory Management System. Goodbye!")
            break

        try:
            if choice == "1":
                inventory_system.add_product(*input("Enter product name, quantity, and price: ").split())

            elif choice == "2":
                inventory_system.update_quantity(*input("Enter product name and new quantity: ").split())

            elif choice == "3":
                inventory_system.set_price(*input("Enter product name and new price: ").split())

            elif choice == "4":
                inventory_view = inventory_system.view_inventory()
                print(f"Current Inventory: {inventory_view or 'Empty'}")

            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

        except ValueError as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
[/PYTHON]
"""

from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

completion = client.chat.completions.create(
  model="",
  messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": task}
  ]
)

print(completion.choices[0].message.content)