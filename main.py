from datetime import datetime, timedelta
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
import numpy as np
from pandas import DataFrame
from ta.trend import ema_indicator
from tinkoff.invest import Client, RequestError, CandleInterval, HistoricCandle

import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

class moving_average:
    def __init__(self, window=20):
        self.window = window

    def fit(self, data):
        self.history_data = data
        return self

    def predict(self, data):
        return self.history_data.rolling(window=self.window).mean()

    def score(self, data):
        print("&&&&&&&&&&&&&&", self.window, len(self.history_data[self.window:].tolist()))
        current_mean_squared_error = mean_squared_error(self.history_data[self.window-1:], self.history_data.rolling(window=self.window).mean()[self.window-1:])
        print("&&&&&&&&&&&&&&", self.window, len(self.history_data[self.window:].tolist()), current_mean_squared_error)
        return 10000000 - current_mean_squared_error

    def get_params(self, deep=True):
        return {"window": self.window}

    def set_params(self, **new_params):
        for name, param in new_params.items():
            setattr(self, name, param)
        return self



class rsi:
    def __init__(self, window=20):
        self.window = window

    def fit(self, data):
        self.history_data = data
        return self

    def predict(self, data):
        return self.history_data.rolling(window=self.window).mean()

    def score(self, data):
        print("&&&&&&&&&&&&&&", self.window, len(self.history_data[self.window:].tolist()))
        current_mean_squared_error = mean_squared_error(self.history_data[self.window-1:], self.history_data.rolling(window=self.window).mean()[self.window-1:])
        print("&&&&&&&&&&&&&&", self.window, len(self.history_data[self.window:].tolist()), current_mean_squared_error)
        return 10000000 - current_mean_squared_error

    def get_params(self, deep=True):
        return {"window": self.window}

    def set_params(self, **new_params):
        for name, param in new_params.items():
            setattr(self, name, param)
        return self


def calculate_moving_average(data):
    param_grid = {
        'window': np.arange(1, 50)
    }
    grid_model = GridSearchCV(moving_average(data), param_grid=param_grid) #, cv=TimeSeriesSplit(n_splits=2)
    grid_model.fit(data)
    print(grid_model.best_estimator_.get_params())
    best_result = grid_model.best_estimator_.predict(data)
    best_window_size = 20
    # best_mean_squared_error = mean_squared_error(data.rolling(window=best_window_size).mean(), data[best_window_size:])
    # for current_window_size in range(2, 50):
    #     if mean_squared_error(data.rolling(window=best_window_size).mean(), data[best_window_size:]) < best_mean_squared_error:
    #         best_window_size = current_window_size
    #     best_mean_squared_error = min(data.rolling(window=current_window_size).mean(), best_mean_squared_error)
    new_data = data.rolling(window=best_window_size).mean()
    new_data = new_data.tolist()
    print(type(data.rolling(window=best_window_size).mean()))
    print(len(new_data))
    print(new_data)
    new_data_1 = data.tolist()
    print(len(new_data_1))
    # return data.rolling(window=best_window_size).mean()
    return best_result




def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def run(share_name):

    try:
        with Client("t.rWXfCVP9o5JNhsgIllWtwxyNPR9dZJZIjSnZ5-xvupVLwsGLLNDa2EMuPvuJM6FzKV3M75rf_DiePZWiCra3fA") as client:
            r = client.market_data.get_candles(
                figi=share_name,
                from_=datetime.utcnow() - timedelta(days=300),
                to=datetime.utcnow(),
                interval=CandleInterval.CANDLE_INTERVAL_DAY # см. utils.get_all_candles
            )
            df = create_df(r.candles)
            df1 = df.copy()
            df1.to_csv("local_dataset/" + share_name + ".csv", index=False)
            # https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#ta.trend.ema_indicator
            df['Moving Average'] = calculate_moving_average(df['close'])
            #
            #
            print(df[['time', 'close', 'Moving Average']].tail(30))
            ax=df.plot(x='time', y='close')
            df.plot(ax=ax, x='time', y='Moving Average')
            plt.show()

    except RequestError as e:
        print(str(e))


def create_df(candles : [HistoricCandle]):
    df = DataFrame([{
        'time': c.time,
        'volume': c.volume,
        'open': cast_money(c.open),
        'close': cast_money(c.close),
        'high': cast_money(c.high),
        'low': cast_money(c.low),
    } for c in candles])

    return df


def cast_money(v):
    """
    https://tinkoff.github.io/investAPI/faq_custom_types/
    :param v:
    :return:
    """
    return v.units + v.nano / 1e9 # nano - 9 нулей

run('USD000UTSTOM')
# run('TCS00A102EQ7')
