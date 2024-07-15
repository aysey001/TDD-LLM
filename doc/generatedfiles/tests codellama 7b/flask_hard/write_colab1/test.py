
import unittest
from unittest.mock import patch
import os
import tempfile
import json
from flask import session, request
from app import app, socketio  # Import the Flask app and socketio module
from app.socketio import socketio_manage  # Import the socketio_manage function from socketio module
from app.chat import users, messages  # Import the users and messages dictionaries from chat module


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.temp_db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        with open(app.config['DATABASE'], 'w') as f:
            json.dump([], f)

    def tearDown(self):
        os.close(self.temp_db_fd)
        os.unlink(app.config['DATABASE'])

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_chat(self):
        response = self.app.get('/chat')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_message(self):
        response = self.app.post('/message', data=dict(message='Hello, world!'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, world!', messages)

    def test_socketio_manage(self):
        with patch('socketio.socketio_manage') as mock_socketio_manage:
            socketio_manage(request)
            mock_socketio_manage.assert_called_once()

    def test_users(self):
        self.assertEqual(users, {})
        self.app.get('/login', data=dict(username='test', password='test'))
        self.assertEqual(users, {'test': 'test'})

    def test_messages(self):
        self.assertEqual(messages, [])
        self.app.post('/message', data=dict(message='Hello, world!'), follow_redirects=True)
        self.assertEqual(messages, ['Hello, world!'])

if __name__ == '__main__':
    unittest.main()
