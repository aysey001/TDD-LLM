
from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms, close_room, disconnect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, String, Integer, Text, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import logging
import eventlet
eventlet.monkey_patch()  # Patch eventlet to fix the bug in gevent
logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG

app = Flask(__name__)  # Create Flask app
app.config['SECRET_KEY'] = 'secret'  # Set secret key for session
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Set database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy tracking modifications
socketio = SocketIO(app)  # Create SocketIO object
socketio.init_app(app)  # Initialize SocketIO object
db = SQLAlchemy(app)  # Create SQLAlchemy object
migrate = Migrate(app, db)  # Create migration object

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/username')
def username():
    return render_template('username.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    session['username'] = username  # Store username in session
    return redirect(url_for('chat'))  # Redirect to chat page

@app.route('/logout')
def logout():
    session['username'] = ''  # Clear username in session
    return redirect(url_for('home'))  # Redirect to home page

@socketio.on('connect')
def connect():
    print('Client connected: ' + str(request.sid))
    emit('my response', {'data': 'Connected', 'count': 0})

@socketio.on('my event')
def handle_my_custom_event(json):
    print('Received my event: ' + str(json))
    emit('my response', {'data': json, 'count': 0})

@socketio.on('my broadcast event')
def handle_my_broadcast_event(json):
    print('Received my broadcast event: ' + str(json))
    emit('my response', {'data': json, 'count': 0})
    emit('my broadcast event', json, broadcast=True)

@socketio.on('join')
def on_join(data):
    print('Client ' + data['username'] + ' joined room ' + data['room'])
    join_room(data['room'])
    send_welcome(data['room'])

@socketio.on('leave')
def on_leave(data):
    print('Client ' + data['username'] + ' left room ' + data['room'])
    leave_room(data['room'])

@socketio.on('close room')
def on_close_room(data):
    print('Room ' + data['room'] + ' closed')
    close_room(data['room'])

@socketio.on('my room event')
def on_my_room_event(json):
    print('Received my room event: ' + str(json))
    room = json['room']
    data = json['data']
    emit('my response', {'data': data, 'count': 0}, room=room)
    emit('my response', {'data': data, 'count': 0}, room=room)

@socketio.on('disconnect request')
def on_disconnect_request(json):
    print('Client requested disconnection: ' + str(json))
    emit('my response', {'data': 'Disconnected', 'count': 0})
    disconnect()

@socketio.on('my message')
def on_my_message(json):
    print('Received my message: ' + str(json))
    room = json['room']
    data = json['data']
    emit('my response', {'data': data, 'count': 0}, room=room)
    emit('my message', data, room=room)

def send_welcome(room):
    emit('my response', {'data': 'Welcome!', 'count': 0}, room=room)

def send_bye(room):
    emit('my response', {'data': 'Goodbye!', 'count': 0}, room=room)

if __name__ == '__main__':
    socketio.run(app)  # Run Flask app with SocketIO server