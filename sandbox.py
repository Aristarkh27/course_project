from datetime import datetime, timedelta
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
import numpy as np
from pandas import DataFrame
from ta.trend import ema_indicator
from tinkoff.invest import Client, RequestError, CandleInterval, HistoricCandle
from tinkoff.invest.sandbox.client import SandboxClient

import pandas as pd
import matplotlib.pyplot as plt



def run():

    try:
        with SandboxClient("t.rWXfCVP9o5JNhsgIllWtwxyNPR9dZJZIjSnZ5-xvupVLwsGLLNDa2EMuPvuJM6FzKV3M75rf_DiePZWiCra3fA") as client:
            client.sandbox.open_sandbox_account()
            print(client.users.get_accounts())


    except RequestError as e:
        print(str(e))
# def run():
#
#     try:
#         with SandboxClient("t.rWXfCVP9o5JNhsgIllWtwxyNPR9dZJZIjSnZ5-xvupVLwsGLLNDa2EMuPvuJM6FzKV3M75rf_DiePZWiCra3fA") as client:
#             sb: SandboxService = client.sandbox
#             account_info = sb.get_account().accounts
#
#             for account in account_info:
#                 print(account)
#
#     except RequestError as e:
#         print(str(e))


run()
