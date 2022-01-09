from datetime import datetime
import asyncio
from django.db.models.aggregates import Sum

from crypto_app import config
from .models import user_trade_records, Website_users
from binance import Client
from binance.exceptions import BinanceAPIException

class GetUserInfo:
    def __init__(self):
        self.user_id = None
        self.api_key = None
        self.secret_key = None
        self.ALL_TICKERS = config.ALL_TICKERS

    def load_trades_info(self, symbol='BTCUSDT'):

        client = Client(self.api_key, self.secret_key)
        trade_records = client.get_my_trades(symbol=symbol)
        
        if len(trade_records) == user_trade_records.objects.filter(symbol='BTCUSDT').count():
            for data in trade_records:
                if not user_trade_records.objects.filter(record_id=data['id']).exists():

                    raw_date_time = datetime.fromtimestamp((data['time']) / 1000)
                    date_time = str(raw_date_time).split(' ')[0]

                    record = user_trade_records.objects.create(
                        user = Website_users.objects.get(id=self.user_id),
                        record_id = data['id'],
                        symbol = data['symbol'],
                        price = data['price'],
                        quantity = data['qty'],
                        cost = data['quoteQty'],
                        time = date_time,
                        isBuyer = data['isBuyer']
                    )
                    record.save()

        # print(client.get_my_trades(symbol=symbol))
        # this_coin = {
        #     'new_trade': {},
        #     'profit': 0,
        #     'totle_costs': 0,
        #     'totle_amount': 0,
        #     'realized_profit': 0,
        #     'unrealized_profit': 0,
        # }
        # if symbol in self.ALL_TICKERS:
        #     recent_price = float(client.get_recent_trades(symbol=symbol)[0]['price'])
        #     this_coin['new_trade'] = client.get_my_trades(symbol=symbol)

        #     # Calc totole_costs and totle_amount
        #     for trade in this_coin['new_trade']:
        #         if trade['isBuyer']:
        #             this_coin['totle_costs'] += float(trade['quoteQty'])
        #             this_coin['totle_amount'] += float(trade['qty'])
        #         else:
        #             this_coin['realized_profit'] += float(trade['quoteQty'])
        #             this_coin['totle_amount'] -= float(trade['qty'])
        #     this_coin['unrealized_profit'] = recent_price * this_coin['totle_amount']
        #     this_coin['profit'] = this_coin['realized_profit'] + this_coin['unrealized_profit'] - this_coin[
        #         'totle_costs']

        #     # Convert timestamp to datatime
        #     for timestamp in this_coin['new_trade']:
        #         new_date = datetime.fromtimestamp((timestamp['time']) / 1000)
        #         timestamp['time'] = str(new_date).split(' ')[0]
        #     return this_coin
        # else:
        #     return False

    def cur_coin_detail(self, symbol='BTCUSDT'):
        self.load_trades_info(symbol)
        client = Client(self.api_key, self.secret_key)

        trade_query = user_trade_records.objects.filter(symbol=symbol)

        totle_costs = trade_query.filter(isBuyer=True).aggregate(Sum('cost'))['cost__sum']
        totle_amount = (
                trade_query.filter(isBuyer=True).aggregate(Sum('quantity'))['quantity__sum'] - 
                trade_query.filter(isBuyer=False).aggregate(Sum('quantity'))['quantity__sum']
            )
        realized_profit = trade_query.filter(isBuyer=False).aggregate(Sum('cost'))['cost__sum']
        unrealized_profit = float(client.get_recent_trades(symbol=symbol)[0]['price']) * totle_amount

        detail = {
            "totle_costs": totle_costs,
            "totle_amount": totle_amount,
            "realized_profit": realized_profit,
            "unrealized_profit": unrealized_profit,
            "profit": realized_profit + unrealized_profit - totle_costs
        }

        return detail
        
    def get_trade_records(self, symbol='BTCUSDT'):
        return user_trade_records.objects.filter(symbol=symbol)

    def get_asset(self):
        client = Client(self.api_key, self.secret_key)
        user_asset = client.get_account()['balances']
        user_own_asset = []
        for item in user_asset:
            if float(item['free']) > 0:
                user_own_asset.append(item)
        return user_own_asset

    def get_user_status(self):
        client = Client(self.api_key, self.secret_key)
        try:
            client.get_account_status()
            return True
        except BinanceAPIException:
            return False

