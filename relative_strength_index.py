from datetime import datetime, timedelta
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
import numpy as np
from tinkoff.invest import Client, RequestError, CandleInterval
from loading_data import create_df
import pandas as pd
import matplotlib.pyplot as plt
from my_token import my_token

class relative_strength_index:
    def __init__(self, window=5):
        self.window = window

    def fit(self, data):
        self.history_data = data
        return self

    def predict(self, data):
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def score(self, data):
        current_amount = 1
        rsi = self.predict(self.history_data)
        period_start = self.window
        period_end = len(self.history_data)
        buying_price = None
        selling_price = None
        history = self.history_data.tolist()
        for i in range(period_start, period_end):
            if rsi[i] < 50:
                pass
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
            selling_price = history[period_end - 1]
            current_amount /= buying_price
            current_amount *= selling_price
        return current_amount

    def get_params(self, deep=True):
        return {"window": self.window}

    def set_params(self, **new_params):
        for name, param in new_params.items():
            setattr(self, name, param)
        return self

    def decision(self, data):
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi >= 50


def calculate_rsi(data):
    param_grid = {
        'window': np.arange(3, 50),
    }
    grid_model = GridSearchCV(relative_strength_index(data), param_grid=param_grid, cv=TimeSeriesSplit(n_splits=2))
    grid_model.fit(data)
    best_result = grid_model.best_estimator_.predict(data)
    print("The best parameters are:")
    for pair in grid_model.best_params_:
        print(pair, "is", grid_model.best_params_[pair])
    print("The earnings of the best model is:", round((grid_model.best_estimator_.score(data) - 1) * 100, 2), end="%\n")
    print("The earning in case of default investing (not conducting any operation) is",
          round((data[len(data) - 1] - data[0]) / data[0] * 100, 2), end="%\n")
    return (best_result, grid_model.best_estimator_)


def predict_rsi(share_name):
    try:
        pd.set_option('display.max_rows', 2500)
        pd.set_option('display.max_columns', 2500)
        pd.set_option('display.width', 15000)
        with Client(my_token) as client:
            r = client.market_data.get_candles(
                figi=share_name,
                from_=datetime.now() - timedelta(days=350),
                to=datetime.now(),
                interval=CandleInterval.CANDLE_INTERVAL_DAY # см. utils.get_all_candles
            )
            df = create_df(r.candles)
            df1 = df.copy()
            df1.to_csv("local_dataset/" + share_name + ".csv", index=False)
            # https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#ta.trend.ema_indicator

            df['Relative Strength Index'] = calculate_rsi(df['close'])[0]
            ax = df.plot(x='time', y='close')
            df.plot(ax=ax, x='time', y='Relative Strength Index')
            plt.show()

    except RequestError as e:
        print(str(e))


predict_rsi('USD000UTSTOM')
