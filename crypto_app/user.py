from datetime import datetime
from symtable import Symbol
from typing import Dict, List
from xmlrpc.client import Boolean
from django.db.models.aggregates import Sum

from .models import user_trade_records, Website_users
from binance import Client
from binance.exceptions import BinanceAPIException


class GetUserInfo:
    def __init__(self):
        self.user_id = None
        self.api_key = None
        self.secret_key = None

    # check user api info is right or not
    def get_user_status(self) -> Boolean:
        client = Client(self.api_key, self.secret_key)
        try:
            client.get_account_status()
            return True
        except BinanceAPIException:
            return False

    # load matched symbol trade records into database
    def load_trades_info(self, symbol='BTCUSDT') -> None:
        client = Client(self.api_key, self.secret_key)
        trade_records = client.get_my_trades(symbol=symbol)

        if len(trade_records) != user_trade_records.objects.filter(symbol=symbol).count():
            for data in trade_records:
                if not user_trade_records.objects.filter(record_id=data['id']).exists():

                    raw_date_time = datetime.fromtimestamp(
                        (data['time']) / 1000)
                    date_time = str(raw_date_time).split(' ')[0]

                    record = user_trade_records.objects.create(
                        user=Website_users.objects.get(id=self.user_id),
                        record_id=data['id'],
                        symbol=data['symbol'],
                        price=data['price'],
                        quantity=data['qty'],
                        cost=data['quoteQty'],
                        time=date_time,
                        isBuyer=data['isBuyer']
                    )
                    record.save()

    # will return trade analytics with matched symbol
    def cur_coin_detail(self, symbol='BTCUSDT') -> Dict:
        client = Client(self.api_key, self.secret_key)

        # object for the matched symbol in database
        trade_query = user_trade_records.objects.filter(symbol=symbol)

        sum_of_buy_quantity = trade_query.filter(
            isBuyer=True).aggregate(Sum('quantity'))['quantity__sum']
        sum_of_sell_quantity = trade_query.filter(
            isBuyer=False).aggregate(Sum('quantity'))['quantity__sum']

        # data for detail
        totle_costs = trade_query.filter(
            isBuyer=True).aggregate(Sum('cost'))['cost__sum']
        totle_amount = (sum_of_buy_quantity -
                        sum_of_sell_quantity) if sum_of_sell_quantity else sum_of_buy_quantity
        realized_profit = trade_query.filter(
            isBuyer=False).aggregate(Sum('cost'))['cost__sum'] or 0
        unrealized_profit = float(client.get_recent_trades(
            symbol=symbol)[0]['price']) * totle_amount
        profit = realized_profit + unrealized_profit - totle_costs
        average_price = ((totle_costs - realized_profit) /
                         totle_amount) if unrealized_profit > 1 else 0

        return {
            "totle_costs": totle_costs,
            "totle_amount": totle_amount,
            "realized_profit": realized_profit,
            "unrealized_profit": unrealized_profit,
            "profit": profit,
            "average_price": average_price
        }

    # return QuerySet with matched symbol
    # ex <QuerySet [<user_trade_records: user_trade_records object (1)>, ...]>
    def get_trade_records(self, symbol='BTCUSDT') -> user_trade_records:
        return user_trade_records.objects.filter(symbol=symbol)

    # return user current asset
    # ex [{'asset': 'BTC', 'free': '0.00872000', 'locked': '0.00000000'},...]
    def get_asset(self) -> List[Dict]:
        client = Client(self.api_key, self.secret_key)
        user_asset = client.get_account()['balances']
        user_own_asset = []
        for item in user_asset:
            if float(item['free']) > 0:
                user_own_asset.append(item)

        return user_own_asset
