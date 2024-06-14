from datetime import datetime, timedelta
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
import numpy as np
from tinkoff.invest import Client, RequestError, CandleInterval, HistoricCandle
from my_token import my_token
import pandas as pd
import matplotlib.pyplot as plt
from loading_data import create_df
from loading_data import read_from_database
from pytz import timezone

class moving_average:
    def __init__(self, window_short=5, window_long=20):
        self.window_short = window_short
        self.window_long = window_long

    def fit(self, data):
        self.history_data = data
        return self

    def predict(self, data):
        return (self.history_data.rolling(window=self.window_short).mean(),
                self.history_data.rolling(window=self.window_long).mean())

    def score(self, data):
        current_amount = 1
        if self.window_short > self.window_long:
            return 0
        short = self.history_data.rolling(window=self.window_short).mean().tolist()
        long = self.history_data.rolling(window=self.window_long).mean().tolist()
        period_start = self.window_long
        period_end = len(self.history_data)
        buying_price = None
        selling_price = None
        lowest_amount = 1
        history = self.history_data.tolist()
        for i in range(period_start, period_end):
            if short[i] < long[i]:
                if selling_price is None:
                    selling_price = history[i]
                if buying_price is not None:
                    current_amount /= buying_price
                    current_amount *= selling_price
                    buying_price = None
                    selling_price = None
            else:
                if buying_price is None:
                    buying_price = history[i]
            if buying_price is not None:
                current_cash = current_amount / buying_price * history[i]
            else:
                current_cash = current_amount
            lowest_amount = min(current_cash, current_amount)
        if buying_price is not None:
            selling_price = history[period_end - 1]
            current_amount /= buying_price
            current_amount *= selling_price
        # print(self.window_short, self.window_long, current_amount)
        return current_amount + (1 - lowest_amount)

    def get_params(self, deep=True):
        return {"window_short": self.window_short,
                "window_long": self.window_long}

    def set_params(self, **new_params):
        for name, param in new_params.items():
            setattr(self, name, param)
        return self

    def decision(self, data):
        short, long = self.predict(data)
        return short[len(short) - 1] >= long[len(long) - 1]


def calculate_moving_average(data, splits=10):
    param_grid = {
        'window_short': np.arange(3, 20),
        'window_long': np.arange(10, 100)
    }
    grid_model = GridSearchCV(moving_average(data), param_grid=param_grid, cv=TimeSeriesSplit(n_splits=splits))
    grid_model.fit(data)
    print("The best parameters are:")
    for pair in grid_model.best_params_:
        print(pair, "is", grid_model.best_params_[pair])
    print("The earnings of the best model is:", round((grid_model.best_estimator_.score(data) - 1) * 100, 2), end="%\n")
    print("The earning in case of default investing (not conducting any operation) is",
          round((data[len(data) - 1] - data[0]) / data[0] * 100, 2), end="%\n")
    best_result = grid_model.best_estimator_.predict(data)
    return best_result


def predict_ma(share_name, period_start, period_end, splits=2):
    pd.set_option('display.max_rows', 2500)
    pd.set_option('display.max_columns', 2500)
    pd.set_option('display.width', 15000)
    try:
        df = read_from_database(share_name, period_start, period_end)
        print(df.shape)
        # https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#ta.trend.ema_indicator
        df['Moving Average short'], df['Moving Average long'] = calculate_moving_average(df['close'], splits)
        ax = df.plot(x='time', y='close')
        df.plot(ax=ax, x='time', y='Moving Average short')
        df.plot(ax=ax, x='time', y='Moving Average long')
        plt.text(3.5, 0.9, 'Sine wave', fontsize=23)
        plt.show()

    except RequestError as e:
        print(str(e))


# predict_ma('TCS00A1028C7', datetime.now(timezone("UTC")) - timedelta(1480), datetime.now(timezone("UTC")), 10)
# USD000UTSTOM