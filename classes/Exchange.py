import ccxt
# import pandas as pd

# from classes.Database import Database

import config
import log


class Exchange:
    def __init__(self):
        self.historical_data = []
        self.exchange_data = []
        self.open_orders = []
        self.symbol = config.SYMBOL
        coins = self.symbol.split("/")
        self.base_coin = coins[0]
        self.quote_coin = coins[1]

        exchange_class = getattr(ccxt, config.EXCHANGE)
        self.exchange = exchange_class({
            'apiKey': config.API_KEY,
            'secret': config.API_SECRET,
            'enableRateLimit': True
        })
        if config.EXCHANGE == 'ftx' and not config.SUBACCOUNT == '':
            self.exchange.headers = {
                'FTX-SUBACCOUNT': config.SUBACCOUNT
            }

        self.exchange.load_markets()

    # def load_data(self, timeframe='5m'):
    #     self.original_data = self.exchange.fetchOHLCV(self.symbol, timeframe)
    #     self.historical_data = pd.DataFrame.from_dict(self.original_data)

    def market_exists(self, symbol=None):
        if symbol == None:
            return False
        elif symbol in self.exchange.symbols:
            return True
        else:
            return False

    def read_balance(self):
        return self.exchange.fetch_balance()

    def get_exchange_rate(self):
        for market in self.exchange.fetch_markets():
            if market['symbol'] == self.symbol:
                return float(market['info']['price'])

    def create_order(self, side, quantity, price):
        order = self.exchange.create_order(
            self.symbol, config.ORDER_TYPE, side, quantity, price)
        return order

    def cancel_orders(self, id_list):
        try:
            for id in id_list:
                self.exchange.cancel_order(id)
            return True
        except Exception as exc:
            print(exc)
            return False

    def cancel_order(self, id):
        try:
            self.exchange.cancel_order(id)
            return True
        except ccxt.InvalidOrder as exc:
            log.warn(
                f"Failed to cancel order with id {id}! Reason: {str(exc)}")
            return False

    def get_order_history(self):
        orders = self.exchange.fetch_orders(self.symbol, limit=300)
        # print(orders)

        # with open('out.txt', 'w') as f:
        #     print(orders, file=f)
        return orders
