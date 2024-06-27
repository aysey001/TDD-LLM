import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['DATABASE'] = 'plants.json'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/plants')
def view_plants():
    with open(app.config['DATABASE'], 'r') as f:
        plants = json.load(f)
    return render_template('plants.html', plants=plants)

@app.route('/add_plant', methods=['GET', 'POST'])
def add_plant():
    if request.method == 'POST':
        new_plant = {
            'species': request.form['species'],
            'watering_schedule': request.form['watering_schedule'],
            'sunlight_requirements': request.form['sunlight_requirements'],
            'notes': request.form['notes']
        }
        with open(app.config['DATABASE'], 'r') as f:
            plants = json.load(f)
        plants.append(new_plant)
        with open(app.config['DATABASE'], 'w') as f:
            json.dump(plants, f)
        return redirect(url_for('view_plants'))
    else:
        return render_template('add_plant.html')

@app.route('/delete_plant/<int:plant_id>')
def delete_plant(plant_id):
    with open(app.config['DATABASE'], 'r') as f:
        plants = json.load(f)
    if plant_id >= 0 and plant_id < len(plants):
        del plants[plant_id]
        with open(app.config['DATABASE'], 'w') as f:
            json.dump(plants, f)
    return redirect(url_for('view_plants'))

if __name__ == '__main__':
    app.run(debug=True)