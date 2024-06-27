from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import os
import base64
from PIL import Image
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'filename': filename})
    else:
        return jsonify({'error': 'No file part in the request'})

@app.route('/apply/<filter>', methods=['POST'])
def apply_filter(filter):
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image = Image.open(filepath)
            if filter == 'comic':
                image = image.convert('L')
                image = image.point(lambda i: i * 0.5)
            image.save(filepath)
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'No file part in the request'})
    else:
        return jsonify({'error': 'Invalid request'})

@app.route('/display', methods=['POST'])
def display():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image = Image.open(filepath)
            image = image.convert('RGB')
            image.save(filepath)
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'No file part in the request'})
    else:
        return jsonify({'error': 'Invalid request'})

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.run(debug=True)