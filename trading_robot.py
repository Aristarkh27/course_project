from tinkoff.invest import Client, RequestError
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest import MoneyValue
from tinkoff.invest import OrderDirection, OrderType
from time import sleep
from uuid import uuid4
from loading_data import read_from_database
from my_token import my_token
from datetime import datetime, timedelta
from relative_strength_index import calculate_rsi
from pytz import timezone

# Delete all existing accounts
def clear_sandbox():
    try:
        with (SandboxClient(my_token) as client):
            accounts_info = client.users.get_accounts().accounts
            for account in accounts_info:
                client.sandbox.close_sandbox_account(account_id=account.id)
    except RequestError as e:
        print(str(e))


def create_new_account(amount=100000):
    try:
        with (SandboxClient(my_token) as client):
            new_account_id = client.sandbox.open_sandbox_account().account_id
            client.sandbox.sandbox_pay_in(
                account_id=new_account_id,
                amount=MoneyValue(currency="rub", units=amount, nano=0)
            )
            return new_account_id
    except RequestError as e:
        print(str(e))


def account_info(account_id):
    try:
        with SandboxClient(my_token) as client:
            return client.operations.get_portfolio(account_id=account_id)

    except RequestError as e:
        print(str(e))


def get_accounts_info():
    try:
        with SandboxClient(my_token) as client:
            return client.users.get_accounts().accounts
    except RequestError as e:
        print(str(e))


def get_accounts_info():
    try:
        with SandboxClient(my_token) as client:
            accounts_info = client.users.get_accounts().accounts
            for account in accounts_info:
                print(account.id)
    except RequestError as e:
        print(str(e))


def buy_stocks(account_id, instrument_id, quantity=1):
    try:
        with SandboxClient(my_token) as client:
            order = client.orders.post_order(
                instrument_id=instrument_id,
                # figi=figi,
                quantity=quantity,
                order_id=str(uuid4()),
                direction=OrderDirection.ORDER_DIRECTION_BUY,
                order_type=OrderType.ORDER_TYPE_MARKET,
                account_id=account_id
            )
    except RequestError as e:
        print(str(e))


def sell_stocks(account_id, instrument_id, quantity=1):
    try:
        with SandboxClient(my_token) as client:
            order = client.orders.post_order(
                instrument_id=instrument_id,
                quantity=quantity,
                order_id=str(uuid4()),
                direction=OrderDirection.ORDER_DIRECTION_SELL,
                order_type=OrderType.ORDER_TYPE_MARKET,
                account_id=account_id
            )
    except RequestError as e:
        print(str(e))


# def run():
#
#     try:
#         with SandboxClient(my_token) as client:
#             sb: SandboxService = client.sandbox
#             account_info = sb.get_account().accounts
#
#             for account in account_info:
#                 print(account)
#
#     except RequestError as e:
#         print(str(e))


def start_trading(account_id, share_name, period_start, period_end, algorithm):
    data = read_from_database(share_name, period_start, period_end)
    print(data)
    print(1000)
    model = algorithm(data['close'], 10)[1]
    buying_price = None
    selling_price = None
    current_amount = 1
    while True:
        data = read_from_database(share_name, period_start, period_end)
        # 0 means sell and 1 means buy
        if model.decision(data['close']) and buying_price is None:
            buy_stocks(account_id, share_name)
            buying_price = data['close'][-1]
        elif selling_price is None:
            sell_stocks(account_id, share_name)
            selling_price = data['close'][-1]
        sleep(60)


clear_sandbox()
new_account_id = create_new_account(100000)
# BBG0047730N88
# BBG0000BBV4MA
start_trading(new_account_id, "BBG00FZMB3Y3", datetime.now(timezone("UTC")) - timedelta(days=1300), datetime.now(timezone("UTC")), calculate_rsi)
# print(new_account_id)
# # buy_stocks(new_account_id, "BBG0047730N88")
# buy_stocks(new_account_id, "TCS00A102EQ7")
# sleep(10)
# print(account_info(new_account_id))
