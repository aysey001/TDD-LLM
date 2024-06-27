
import unittest
from unittest.mock import patch
import os
import tempfile
import json

import recipe  # Import the Flask app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = recipe.app.test_client()
        self.temp_db_fd, recipe.app.config['DATABASE'] = tempfile.mkstemp()
        recipe.app.config['TESTING'] = True
        self.recipes = [
            {'name': 'Grilled Steak', 'description': 'A classic steak recipe', 'tools': ['Grill', 'Steak knife'],
             'ingredients': [{'name': 'Steak', 'amount': '1'}, {'name': 'Olive oil', 'amount': '1 tablespoon'}],
             'extras': ['Salt', 'Pepper']},
            {'name': 'Chicken Parmesan', 'description': 'A delicious pasta dish', 'tools': ['Frying pan', 'Pasta'],
             'ingredients': [{'name': 'Chicken breast', 'amount': '1'}, {'name': 'Pasta', 'amount': '200g'}],
             'extras': ['Tomato sauce', 'Shredded mozzarella cheese']}
        ]
        with open(recipe.app.config['DATABASE'], 'w') as f:
            json.dump(self.recipes, f)

    def tearDown(self):
        os.close(self.temp_db_fd)
        os.unlink(recipe.app.config['DATABASE'])

    def test_load_data(self):
        with patch('builtins.open', return_value=open(recipe.app.config['DATABASE'], 'r')) as mock_open:
            recipe.load_data()
            mock_open.assert_called_once_with('recipes.json', 'r')
            self.assertEqual(recipe.recipes, self.recipes)

    def test_load_data_no_file(self):
        os.unlink(recipe.app.config['DATABASE'])
        recipe.load_data()
        self.assertEqual(recipe.recipes, [])

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_recipe_get(self):
        response = self.app.get('/add_recipe')
        self.assertEqual(response.status_code, 200)

    def test_add_recipe_post(self):
        new_recipe = {
            'name': 'Stir-Fried Noodles',
            'description': 'A tasty noodle recipe',
            'tools': ['Stir-fry pan', 'Noodles'],
            'ingredients': [{'name': 'Noodles', 'amount': '100g'}, {'name': 'Vegetables', 'amount': '2'}],
            'extras': ['Vinegar', 'Salt']
        }
        response = self.app.post('/add_recipe', data=new_recipe, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(new_recipe, recipe.recipes)

    def test_delete_recipe(self):
        response = self.app.get('/delete_recipe/0', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.recipes[0], recipe.recipes)

    def test_search_recipes(self):
        response = self.app.get('/search')
        self.assertEqual(response.status_code, 200)

    def test_view_recipes(self):
        response = self.app.get('/view_recipes')
        self.assertEqual(response.status_code, 200)

    def test_update_recipe(self):
        new_recipe = {
            'name': 'Chicken Fajitas',
            'description': 'A tasty fajitas recipe',
            'tools': ['Frying pan', 'Stir-fry pan'],
            'ingredients': [{'name': 'Chicken breast', 'amount': '1'}, {'name': 'Noodles', 'amount': '100g'}],
            'extras': ['Salsa', 'Tortillas']
        }
        response = self.app.get('/update_recipe/0', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Recipe updated successfully')
        self.assertIn(new_recipe, recipe.recipes)

if __name__ == '__main__':
    unittest.main()
