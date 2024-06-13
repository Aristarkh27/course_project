from tinkoff.invest import HistoricCandle
from pandas import DataFrame
import sqlite3
import pandas as pd


def read_from_database(share_name, period_start, period_end):
    conn = sqlite3.connect('invest_1.db')
    cursor = conn.cursor()
    s = f"""SELECT time, volume, open, close, high, low from hourly_prices where company_code=?, time>?, time<?"""
    cursor.execute(s, (share_name, period_start, period_end, ))
    ans = cursor.fetchall()
    df = pd.DataFrame(ans, columns=['time', 'volume', 'open', 'close', 'high', 'low'])
    return df


def create_df(candles: [HistoricCandle]):
    df = DataFrame([{
        'time': c.time,
        'volume': c.volume,
        'open': cast_money(c.open),
        'close': cast_money(c.close),
        'high': cast_money(c.high),
        'low': cast_money(c.low),
    } for c in candles])
    return df

# Credit: https://azzrael.ru/api-ti?ysclid=lwxvwlpo87613902783


def cast_money(v):
    return v.units + v.nano / 1e9 # nano - 9 нулей
