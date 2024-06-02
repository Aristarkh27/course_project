from datetime import datetime, timedelta, UTC
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




def cast_money(v):
    """
    https://tinkoff.github.io/investAPI/faq_custom_types/
    :param v:
    :return:
    """
    return v.units + v.nano / 1e9 # nano - 9 нулей

conn = sqlite3.connect('invest.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS invest (
                            time TIMESTAMP,
                            volume INTEGER,
                            open REAL,
                            close REAL,
                            high REAL,
                            low REAL)''')

with Client("t.rWXfCVP9o5JNhsgIllWtwxyNPR9dZJZIjSnZ5-xvupVLwsGLLNDa2EMuPvuJM6FzKV3M75rf_DiePZWiCra3fA") as client:
    for c in client.get_all_candles(
            instrument_id="BBG004730N88",
            from_=now() - timedelta(days=10000),
            interval=CandleInterval.CANDLE_INTERVAL_HOUR,
            candle_source_type=CandleSource.CANDLE_SOURCE_UNSPECIFIED,
    ):
        time =  c.time
        volume = c.volume
        open = cast_money(c.open)
        close = cast_money(c.close)
        high = cast_money(c.high)
        low = cast_money(c.low)
        print(time, volume, open, close, high, low)
        cursor.execute("INSERT INTO invest (time, volume, open, close, high, low) VALUES (?, ?, ?, ?, ?, ?)",
                       (time, volume, open, close, high, low))
