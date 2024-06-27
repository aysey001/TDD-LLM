
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

recipes = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recipes')
def view_recipes():
    return render_template('recipes.html', recipes=recipes)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        # Add the recipe to the data structure
        recipe = {
            'name': request.form['name'],
            'description': request.form['description'],
            'tools': request.form['tools'].split(','),
            'ingredients': [{'name': x['name'], 'amount': x['amount']} for x in json.loads(request.form['ingredients'])],
            'extras': request.form['extras'].split(',')
        }
        recipes.append(recipe)
        save_data()
        # Redirect to the recipes page
        return redirect(url_for('view_recipes'))
    else:
        return render_template('add_recipe.html')

@app.route('/delete_recipe/<int:recipe_id>')
def delete_recipe(recipe_id):
    if 0 <= recipe_id < len(recipes):
        del recipes[recipe_id]
        save_data()
    # Redirect to the recipes page
    return redirect(url_for('view_recipes'))

@app.route('/search', methods=['GET'])
def search_recipes():
    query = request.args.get('query', '').lower()
    results = [recipe for recipe in recipes if query in recipe['name'].lower()]
    return jsonify(results)

def save_data():
    with open('recipes.json', 'w') as file:
        json.dump(recipes, file)

def load_data():
    global recipes
    if os.path.exists('recipes.json'):
        with open('recipes.json', 'r') as file:
            recipes = json.load(file)
    else:
        recipes = []

if __name__ == '__main__':
    load_data()
    app.run(debug=True)