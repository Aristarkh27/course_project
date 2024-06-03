from datetime import datetime, timedelta
import os
from pandas import DataFrame
from ta.trend import ema_indicator
from tinkoff.invest import Client, RequestError, CandleInterval, HistoricCandle
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import csv
from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.schemas import CandleSource
from tinkoff.invest.utils import now
import pytz



def cast_money(v):
    """
    https://tinkoff.github.io/investAPI/faq_custom_types/
    :param v:
    :return:
    """
    return v.units + v.nano / 1e9 # nano - 9 нулей

conn = sqlite3.connect('invest_1.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS  hourly_prices  (
                            company_code TEXT,
                            time TIMESTAMP,
                            volume INTEGER,
                            open REAL,
                            close REAL,
                            high REAL,
                            low REAL)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS  daily_prices  (
                            company_code TEXT,
                            time TIMESTAMP,
                            volume INTEGER,
                            open REAL,
                            close REAL,
                            high REAL,
                            low REAL)''')

def insert_prices_into_db_daily(share_name):

    start_days = 10010
    start_days_7 = start_days-6

    now = datetime.now()
    midnight_today = datetime(year=now.year, month=now.month, day=now.day, hour=1, minute=0, second=0)

    while start_days >= 0:

        if start_days < 6:
            start_days_7 = 0

        try:
            with Client("") as client:
                date = midnight_today
                r = client.market_data.get_candles(
                    figi=share_name,
                    from_=date - timedelta(days = start_days),
                    to=date - timedelta(days = start_days_7 + 1),
                    #interval=CandleInterval.CANDLE_INTERVAL_HOUR
                    interval=CandleInterval.CANDLE_INTERVAL_DAY# см. utils.get_all_candles
                )
                # print(r)

                if len(r.candles) == 0:
                    start_days -= 6
                    start_days_7 -= 6
                else:
                    daily_candles(share_name, r.candles)
                    conn.commit()
                    start_days -= 6
                    start_days_7 -= 6
                print(start_days)
        except RequestError as e:
            print(str(e))


def daily_candles(share_name, candles : [HistoricCandle]):

    for c in candles:
        time =  c.time
        volume = c.volume
        open = cast_money(c.open)
        close = cast_money(c.close)
        high = cast_money(c.high)
        low = cast_money(c.low)
        cursor.execute("INSERT INTO  daily_prices (company_code, time, volume, open, close, high, low) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (share_name, time, volume, open, close, high, low))
        # print(share_name, time, volume, open, close, high, low)
# insert_prices_into_db('USD000UTSTOM')
def insert_prices_into_db_hourly(share_name):

    start_days = 10010
    start_days_7 = start_days-6

    now = datetime.now()
    midnight_today = datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)

    while start_days >= 0:

        if start_days < 6:
            start_days_7 = 0

        try:
            with Client("") as client:
                date = midnight_today
                r = client.market_data.get_candles(
                    figi=share_name,
                    from_=date - timedelta(days = start_days),
                    to=date - timedelta(days = start_days_7),
                    interval=CandleInterval.CANDLE_INTERVAL_HOUR # см. utils.get_all_candles
                )
                # print(r)

                if len(r.candles) == 0:
                    start_days -= 6
                    start_days_7 -= 6
                else:
                    create_df(share_name, r.candles)
                    conn.commit()
                    start_days -= 6
                    start_days_7 -= 6
                print(start_days)
        except RequestError as e:
            print(str(e))


def create_df(share_name, candles : [HistoricCandle]):

    for c in candles:
        time =  c.time
        volume = c.volume
        open = cast_money(c.open)
        close = cast_money(c.close)
        high = cast_money(c.high)
        low = cast_money(c.low)
        cursor.execute("INSERT INTO  hourly_prices (company_code, time, volume, open, close, high, low) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (share_name, time, volume, open, close, high, low))
        # print(share_name, time, volume, open, close, high, low)


codes = ['TCS00A1028C7', 'BBG00HBPXX50', 'BBG00R83FV73', 'BBG00A102RX6', 'BBG00FZMB3Y3', 'TCS00A1029T9', 'BBG00FX0RDF5', 'BBG00PVL2PM1', 'BBG00YJKHN65', 'BBG00PM8S500', 'TCS00A102DK3', 'BBG00QG2Y896', 'BBG011PCH913', 'BBG00HTSM1G5', 'BBG00NHLC0N5', 'TCS00A103VH9', 'TCS00A103VM9', 'TCS00A102EQ8']

for i in codes:
    print(i)
    insert_prices_into_db_daily(i)
    #insert_prices_into_db_hourly(i)


def fill_table_with_latest_values_daily():
    s = """SELECT distinct company_code from  daily_prices"""
    cursor.execute(s)
    ans = cursor.fetchall()
    for i in ans:
        code = i[0]
        s = """select max(time) from daily_prices where company_code = ?"""
        cursor.execute(s, (code,))
        a = cursor.fetchone()
        try:
            date = a[0]
            date_time = datetime.fromisoformat(date)
            new_date_time = date_time + timedelta(hours=1)
            print(new_date_time)
            with Client(
                    "") as client:
                for c in client.get_all_candles(
                        instrument_id=code,
                        from_=new_date_time,
                        interval=CandleInterval.CANDLE_INTERVAL_DAY,
                        candle_source_type=CandleSource.CANDLE_SOURCE_UNSPECIFIED,
                ):
                    time = c.time
                    volume = c.volume
                    open = cast_money(c.open)
                    close = cast_money(c.close)
                    high = cast_money(c.high)
                    low = cast_money(c.low)
                    print(time, volume, open, close, high, low)
                    cursor.execute(
                        "INSERT INTO daily_prices (company_code, time, volume, open, close, high, low) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (code, time, volume, open, close, high, low))
                    conn.commit()

        except:
            print('No such company')

def fill_table_with_latest_values_hourly():
    s = """SELECT distinct company_code from  hourly_prices"""
    cursor.execute(s)
    ans = cursor.fetchall()
    for i in ans:
        code = i[0]
        s = """select max(time) from hourly_prices where company_code = ?"""
        cursor.execute(s, (code,))
        a = cursor.fetchone()
        try:
            date = a[0]
            date_time = datetime.fromisoformat(date)
            new_date_time = date_time + timedelta(hours=1)
            print(new_date_time)
            with Client(
                    "") as client:
                for c in client.get_all_candles(
                        instrument_id=code,
                        from_=new_date_time,
                        interval=CandleInterval.CANDLE_INTERVAL_HOUR,
                        candle_source_type=CandleSource.CANDLE_SOURCE_UNSPECIFIED,
                ):
                    time = c.time
                    volume = c.volume
                    open = cast_money(c.open)
                    close = cast_money(c.close)
                    high = cast_money(c.high)
                    low = cast_money(c.low)
                    print(time, volume, open, close, high, low)
                    cursor.execute(
                        "INSERT INTO hourly_prices (company_code, time, volume, open, close, high, low) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (code, time, volume, open, close, high, low))
                    conn.commit()

        except:
            print('No such company')
