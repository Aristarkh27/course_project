import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import mean_squared_error

def calculate_moving_average(data, window=20):
    return data.rolling(window=window).mean()

class moving_average:
    def __init__(self, window):
        self.window = window

    def fit(self, data):
        self.data = data
        return self

    def predict(self):
        return self.data.rolling(window=self.window).mean()

    def scoring(self):
        return mean_squared_error(self.data[self.window:], self.data.rolling(window=self.window).mean())

    def get_params(self, deep=True):
        return self.window

    def set_params(self, window):
        self.window = window


def main():
    # file with stocks
    df = pd.read_csv('stock_data.csv')

    # convert index (datetime)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # count MA
    param_grid = {
        'data': list(range(2, 51))
    }
    grid_model = GridSearchCV(moving_average(), param_grid=param_grid, cv=TimeSeriesSplit(n_splits=10))
    grid_model.fit(df['Close'])
    df['Moving Average'] = calculate_moving_average(df['Close'])

    print(df)

if __name__ == "__main__":
    main()
