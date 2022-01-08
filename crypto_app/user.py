from crypto_app import config
from datetime import datetime
from binance import Client
from binance.exceptions import BinanceAPIException

class GetUserInfo:
    def __init__(self):
        self.api_key = None
        self.secret_key = None
        self.ALL_TICKERS = config.ALL_TICKERS

    def get_trades_info(self, symbol='BTCUSDT'):
        client = Client(self.api_key, self.secret_key)
        print(client.get_my_trades(symbol=symbol))
        this_coin = {
            'new_trade': {},
            'profit': 0,
            'totle_costs': 0,
            'totle_amount': 0,
            'realized_profit': 0,
            'unrealized_profit': 0,
        }
        if symbol in self.ALL_TICKERS:
            recent_price = float(client.get_recent_trades(symbol=symbol)[0]['price'])
            this_coin['new_trade'] = client.get_my_trades(symbol=symbol)

            # Calc totole_costs and totle_amount
            for trade in this_coin['new_trade']:
                if trade['isBuyer']:
                    this_coin['totle_costs'] += float(trade['quoteQty'])
                    this_coin['totle_amount'] += float(trade['qty'])
                else:
                    this_coin['realized_profit'] += float(trade['quoteQty'])
                    this_coin['totle_amount'] -= float(trade['qty'])
            this_coin['unrealized_profit'] = recent_price * this_coin['totle_amount']
            this_coin['profit'] = this_coin['realized_profit'] + this_coin['unrealized_profit'] - this_coin[
                'totle_costs']

            # Convert timestamp to datatime
            for timestamp in this_coin['new_trade']:
                new_date = datetime.fromtimestamp((timestamp['time']) / 1000)
                timestamp['time'] = str(new_date).split(' ')[0]
            return this_coin
        else:
            return False

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

