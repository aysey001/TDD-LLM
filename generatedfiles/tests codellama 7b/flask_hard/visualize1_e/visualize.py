
from flask import Flask, render_template, request, redirect, url_for, send_file
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        # Get the data from the form and save it to a file
        data = request.form['data']
        with open('data.json', 'w') as file:
            json.dump(data, file)
        return redirect(url_for('home'))
    else:
        return render_template('data.html')

@app.route('/barchart', methods=['GET', 'POST'])
def barchart():
    if request.method == 'POST':
        # Create a bar chart with the data from data.json
        data = json.load(open('data.json'))
        # ...
        return send_file('barchart.png', mimetype='image/png')
    else:
        return render_template('barchart.html')

@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        # Create a table with the data from data.json
        data = json.load(open('data.json'))
        # ...
        return send_file('table.png', mimetype='image/png')
    else:
        return render_template('table.html')

@app.route('/piechart', methods=['GET', 'POST'])
def piechart():
    if request.method == 'POST':
        # Create a pie chart with the data from data.json
        data = json.load(open('data.json'))
        # ...
        return send_file('piechart.png', mimetype='image/png')
    else:
        return render_template('piechart.html')

if __name__ == '__main__':
    app.run(debug=True)