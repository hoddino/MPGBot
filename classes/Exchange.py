import ccxt
import pandas as pd

import config


class Exchange:
    def __init__(self,):
        self.historical_data = []
        self.exchange_data = []
        self.open_orders = []
        self.symbol = config.SYMBOL

        exchange_class = getattr(ccxt, config.EXCHANGE)
        self.exchange = exchange_class({
            'apiKey': config.API_KEY,
            'secret': config.API_SECRET,
            'enableRateLimit': True
        })
        self.exchange.load_markets()

    def load_data(self, timeframe='5m'):
        self.original_data = self.exchange.fetchOHLCV(self.symbol, timeframe)
        self.historical_data = pd.DataFrame.from_dict(self.original_data)

    def market_exists(self, symbol=None):
        if symbol == None:
            return False
        elif symbol in self.exchange.symbols:
            return True
        else:
            return False

    def read_balance(self):
        return self.exchange.fetch_balance()

    def read_filled_orders(self):
        pass

    def get_exchange_rate(self):
        for market in self.exchange.fetch_markets():
            if market['symbol'] == self.symbol:
                return float(market['info']['price'])

    def create_order(self, side, quantity, price):
        # quantity in base currency
        # price in quote currency
        order = self.exchange.create_order(
            self.symbol, config.ORDER_TYPE, side, quantity, price)
        print(str(order))
        self.open_orders.append(order['id'])
        return order

    def cancel_open_orders(self):
        for id in self.open_orders:
            self.exchange.cancel_order(id)
