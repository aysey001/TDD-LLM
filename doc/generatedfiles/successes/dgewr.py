import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class DataAnalytics:
    def __init__(self):
        self.data = None
        self.visualization = None

    def load_data(self, filepath):
        self.data = pd.read_csv(filepath)

    def filter_data(self, column, operator, value):
        filtered_data = self.data.loc[self.data[column].apply(lambda x: operator(x, value))]
        return filtered_data

    def sort_data(self, column):
        sorted_data = self.data.sort_values(column)
        return sorted_data

    def visualize_data(self, x, y):
        self.visualization = self.data.plot(kind='scatter', x=x, y=y)
        plt.show()

def main():
    analytics = DataAnalytics()
    analytics.load_data('data.csv')
    filtered_data = analytics.filter_data('column', lambda x, value: x > value, 10)
    sorted_data = analytics.sort_data('column')
    analytics.visualize_data('x', 'y')