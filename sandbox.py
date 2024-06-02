from datetime import datetime, timedelta
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
import numpy as np
from pandas import DataFrame
from ta.trend import ema_indicator
from tinkoff.invest import Client, RequestError, CandleInterval, HistoricCandle
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest import MoneyValue



import pandas as pd
import matplotlib.pyplot as plt


# Delete all existing accounts
def clear_sandbox():
    try:
        with (SandboxClient("t.rWXfCVP9o5JNhsgIllWtwxyNPR9dZJZIjSnZ5-xvupVLwsGLLNDa2EMuPvuJM6FzKV3M75rf_DiePZWiCra3fA") as client):
            accounts_info = client.users.get_accounts().accounts
            for account in accounts_info:
                client.sandbox.close_sandbox_account(account_id=account.id)
    except RequestError as e:
        print(str(e))


def create_new_account():
    try:
        with (SandboxClient("t.rWXfCVP9o5JNhsgIllWtwxyNPR9dZJZIjSnZ5-xvupVLwsGLLNDa2EMuPvuJM6FzKV3M75rf_DiePZWiCra3fA") as client):
            new_account_id = client.sandbox.open_sandbox_account().account_id
            client.sandbox.sandbox_pay_in(
                account_id=new_account_id,
                amount=MoneyValue(currency="rub", units=10000, nano=0)
            )
            return new_account_id
    except RequestError as e:
        print(str(e))


def account_info(account_id):
    try:
        with SandboxClient("t.rWXfCVP9o5JNhsgIllWtwxyNPR9dZJZIjSnZ5-xvupVLwsGLLNDa2EMuPvuJM6FzKV3M75rf_DiePZWiCra3fA") as client:
            return client.operations.get_portfolio(account_id=account_id)

    except RequestError as e:
        print(str(e))


def run():
    try:
        with SandboxClient("t.rWXfCVP9o5JNhsgIllWtwxyNPR9dZJZIjSnZ5-xvupVLwsGLLNDa2EMuPvuJM6FzKV3M75rf_DiePZWiCra3fA") as client:
            accounts_info = client.users.get_accounts().accounts
            for account in accounts_info:
                print(account.id)
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

clear_sandbox()
new_account_id = create_new_account()
print(new_account_id)
print(account_info(new_account_id))
