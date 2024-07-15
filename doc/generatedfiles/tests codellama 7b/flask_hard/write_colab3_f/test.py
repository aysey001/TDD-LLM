
import unittest
import os
import tempfile
import json
from socketio import ClientNamespace  # Import SocketIO client library
from eventlet import wsgi  # Import eventlet WSGI server library
from write_colab import app  # Import Flask app and SocketIO server


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.temp_db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.users = [
            {'username': 'User1', 'socket_id': 'user1'},
            {'username': 'User2', 'socket_id': 'user2'}
        ]
        with open(app.config['DATABASE'], 'w') as f:
            json.dump(self.users, f)

    def tearDown(self):
        os.close(self.temp_db_fd)
        os.unlink(app.config['DATABASE'])

    def test_load_data(self):
        with patch('builtins.open', return_value=open(app.config['DATABASE'], 'r')) as mock_open:
            app.load_data()
            mock_open.assert_called_once_with('users.json', 'r')
            self.assertEqual(app.users, self.users)

    def test_load_data_no_file(self):
        os.unlink(app.config['DATABASE'])
        app.load_data()
        self.assertEqual(app.users, [])

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_chat_room(self):
        response = self.app.get('/chat')
        self.assertEqual(response.status_code, 200)

    def test_username_system(self):
        response = self.app.get('/username')
        self.assertEqual(response.status_code, 200)

    def test_socketio(self):
        namespace = ClientNamespace('/test')  # Create SocketIO client namespace
        with patch('socketio.ClientNamespace.emit') as mock_emit:
            app.socketio.emit('event', {'data': 'test'}, namespace=namespace)
            mock_emit.assert_called_once_with('event', {'data': 'test'}, namespace=namespace)
            self.assertEqual(app.socketio.server, wsgi.server)
            self.assertEqual(app.socketio.async_mode, 'eventlet')
            self.assertEqual(app.socketio.logger, app.logger)
            self.assertEqual(app.socketio.client_manager.logger, app.logger)
            self.assertEqual(app.socketio.client_manager.server, wsgi.server)
            self.assertEqual(app.socketio.client_manager.async_mode, 'eventlet')
            self.assertEqual(app.socketio.client_manager.socket_class, app.socketio._socket_class)
            self.assertEqual(app.socketio._socket_class.server, wsgi.server)
            self.assertEqual(app.socketio._socket_class.async_mode, 'eventlet')
            self.assertEqual(app.socketio._socket_class.logger, app.logger)
            self.assertEqual(app.socketio._socket_class.client_manager, app.socketio.client_manager)

if __name__ == '__main__':
    unittest.main()
