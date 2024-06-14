import datetime
from tinkoff.invest import HistoricCandle
from pandas import DataFrame
import sqlite3
import pandas as pd
from pytz import timezone

def read_from_database(share_name, period_start, period_end):
    conn = sqlite3.connect('invest.db')
    cursor = conn.cursor()
    s = f"""SELECT time, volume, open, close, high, low from daily_prices where company_code=?"""
    cursor.execute(s, (share_name, ))
    all_data = cursor.fetchall()
    data = []
    for a in all_data:
        if period_start <= datetime.datetime.fromisoformat(a[0]) <= period_end:
            data.append(a)
    df = pd.DataFrame(data, columns=['time', 'volume', 'open', 'close', 'high', 'low'])
    return df


def read_from_database_all(share_name):
    conn = sqlite3.connect('invest_1.db')
    cursor = conn.cursor()
    s = f"""SELECT time, volume, open, close, high, low from hourly_prices where company_code=?"""
    cursor.execute(s, (share_name, ))
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


# read_from_database_all("TCS00A1028C7")
# print(type(datetime.datetime.now(timezone("UTC"))))
# print(read_from_database("TCS00A1028C7", datetime.datetime.now(timezone("UTC")) - datetime.timedelta(days=3000)
#       , datetime.datetime.now(timezone("UTC"))))