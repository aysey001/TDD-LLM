import unittest
from unittest.mock import patch
import os
import tempfile
import json
from quiz import app  # Import the Flask app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.temp_db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.questions = [
            {'title': 'Question 1', 'description': 'Question 1 description', 'options': ['Option 1', 'Option 2'], 'booleans': [True, False]},
            {'title': 'Question 2', 'description': 'Question 2 description', 'options': ['Option 1', 'Option 2'], 'booleans': [False, True]}
        ]
        with open(app.config['DATABASE'], 'w') as f:
            json.dump(self.questions, f)

    def tearDown(self):
        os.close(self.temp_db_fd)
        os.unlink(app.config['DATABASE'])

    def test_load_data(self):
        with patch('builtins.open', return_value=open(app.config['DATABASE'], 'r')) as mock_open:
            app.load_data()
            mock_open.assert_called_once_with('questions.json', 'r')
            self.assertEqual(app.questions, self.questions)

    def test_load_data_no_file(self):
        os.unlink(app.config['DATABASE'])
        app.load_data()
        self.assertEqual(app.questions, [])

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_questions(self):
        response = self.app.get('/questions')
        self.assertEqual(response.status_code, 200)

    def test_add_question_get(self):
        response = self.app.get('/add_question')
        self.assertEqual(response.status_code, 200)

    def test_add_question_post(self):
        new_question = {
            'title': 'New Question',
            'description': 'New Question description',
            'options': ['Option 1', 'Option 2'],
            'booleans': [True, False]
        }
        response = self.app.post('/add_question', data=new_question, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(new_question, app.questions)

    def test_delete_question(self):
        response = self.app.get('/delete_question/0', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.questions[0], app.questions)

    def test_view_question_details(self):
        response = self.app.get('/question/0')
        self.assertEqual(response.status_code, 200)

    def test_submit_answer(self):
        response = self.app.get('/submit_answer/0/0', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(True, app.questions[0]['booleans'])

if __name__ == '__main__':
    unittest.main()