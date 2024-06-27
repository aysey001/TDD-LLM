
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from datetime import datetime
from app import app, socketio  # Import the Flask app and socketio module
from app.chat import users, messages  # Import the users and messages dictionaries from chat module

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['username'] = None
    return redirect(url_for('chat'))

@socketio.on('connect', namespace='/chat')
def connect():
    emit('message', {'data': f'{datetime.now()} {session["username"]} connected'})
    users[session['username']] = session['username']
    print('connect')
    print(users)

@socketio.on('message', namespace='/chat')
def message(message):
    emit('message', {'data': f'{datetime.now()} {session["username"]} {message["data"]}'}, broadcast=True)
    messages.append(message["data"])
    print(messages)

@socketio.on('disconnect', namespace='/chat')
def disconnect():
    emit('message', {'data': f'{datetime.now()} {session["username"]} disconnected'})
    users.pop(session['username'])
    print('disconnect')
    print(users)

if __name__ == '__main__':
    socketio.run(app)
