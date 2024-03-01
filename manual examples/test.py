from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

task =  """[INST]
1. Create a class for the banking system that includes all the necessary functions and attributes to operate the system.
2. Define a main() function that acts as the entry point for the program, where users can select from different options using a menu.
3. Write functions for each of the banking operations (e.g., create account, deposit money, withdraw money, check balance) and make sure they are properly implemented.
4. Implement error handling mechanisms to ensure the system can handle user inputs correctly and prevent errors from occurring.
5. Use a user-friendly main menu to guide users through the various functionalities of the banking system.
6. Ensure that all functions and classes have appropriate documentation strings and docstrings.
7. Test the system thoroughly using various test cases to ensure it works as intended and identify any issues or bugs.
[/INST]
"""

prompt = """Your task is NOT to implement or expand the given list of task.
Your task is to write python testing code for the each element in the given task, which can be tested for using unittest.
Infer the structure of your answer from the given example. 
You should make assumptions about the signature of the functions.
Do not write outside the numbered list.

Here is an example:
[INST]
1. Create a class for the inventory management system with attributes representing the state of the inventory (e.g., products, quantities, prices).
2. Define a main() function to serve as the program's entry point, allowing users to choose from different options through a menu.
3. Write functions for essential inventory operations, such as adding products, updating quantities, setting prices, and viewing the inventory.
[/INST]

#Your reply should look like this:
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
"""


completion = client.chat.completions.create(
  model="",
  messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": task}
  ]
)

print(completion.choices[0].message.content)