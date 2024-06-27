
import unittest
from unittest.mock import patch
import pandas as pd
import matplotlib.pyplot as plt
import os
import tempfile
import numpy as np
import sys
import io
from flask import Flask, request, send_file
from visualize import app

class TestPlant(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.temp_db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.data = pd.read_csv('data.csv')
        self.data['value'] = np.random.rand(len(self.data))
        self.data.to_csv(app.config['DATABASE'], index=False)

    def tearDown(self):
        os.close(self.temp_db_fd)
        os.unlink(app.config['DATABASE'])

    def test_load_data(self):
        with patch('builtins.open', return_value=open(app.config['DATABASE'], 'r')) as mock_open:
            app.load_data()
            mock_open.assert_called_once_with('data.csv', 'r')
            self.assertEqual(app.data, self.data)

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to Plant App', response.data.decode())
        self.assertIn('Select Data Visualization', response.data.decode())
        self.assertIn('Select Data', response.data.decode())
        self.assertIn('View Image', response.data.decode())

    def test_data_visualization(self):
        response = self.app.get('/data-visualization')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Select Data Visualization', response.data.decode())
        self.assertIn('Select Data', response.data.decode())
        self.assertIn('View Image', response.data.decode())

    def test_select(self):
        response = self.app.get('/select')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Select Data', response.data.decode())
        self.assertIn('Submit', response.data.decode())
        self.assertIn('Select Data Visualization', response.data.decode())
        self.assertIn('View Image', response.data.decode())

    def test_data(self):
        response = self.app.get('/data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Select Data', response.data.decode())
        self.assertIn('Submit', response.data.decode())
        self.assertIn('Select Data Visualization', response.data.decode())
        self.assertIn('View Image', response.data.decode())

    def test_image(self):
        response = self.app.get('/image')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data:image/png;base64', response.data.decode())

    def test_save_data(self):
        with patch('builtins.open', return_value=open(app.config['DATABASE'], 'r')) as mock_open:
            app.save_data()
            mock_open.assert_called_once_with('data.csv', 'w')
            self.assertEqual(app.data, self.data)

    def test_create_barchart(self):
        with patch('builtins.open', return_value=open(app.config['DATABASE'], 'r')) as mock_open:
            app.create_barchart()
            mock_open.assert_called_once_with('barchart.png', 'wb')
            self.assertTrue(os.path.isfile('barchart.png'))
            with open('barchart.png', 'rb') as f:
                self.assertEqual(f.read(), b'barchart image')

    def test_create_table(self):
        with patch('builtins.open', return_value=open(app.config['DATABASE'], 'r')) as mock_open:
            app.create_table()
            mock_open.assert_called_once_with('table.png', 'wb')
            self.assertTrue(os.path.isfile('table.png'))
            with open('table.png', 'rb') as f:
                self.assertEqual(f.read(), b'table image')

    def test_create_piechart(self):
        with patch('builtins.open', return_value=open(app.config['DATABASE'], 'r')) as mock_open:
            app.create_piechart()
            mock_open.assert_called_once_with('piechart.png', 'wb')
            self.assertTrue(os.path.isfile('piechart.png'))
            with open('piechart.png', 'rb') as f:
                self.assertEqual(f.read(), b'piechart image')

if __name__ == '__main__':
    unittest.main()
