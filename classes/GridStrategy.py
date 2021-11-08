import pandas as pd
import time

import config


class GridStrategy:
    def __init__(self, account):
        self.account = account
        self.buy_id = 0
        self.sell_id = 0
        self.buy_prices = []
        self.trading = True
        coins = config.SYMBOL.split("/")
        self.quote_balance = self.account.get_balance(coins[0])
        self.base_balance = self.account.get_balance(coins[1])

    # def start(self, data, symbol, starting_base_balance, starting_quote_balance):
    #     self.starting_base_balance = starting_base_balance
    #     self.starting_quote_balance = starting_quote_balance

    #     # buy quantity of base currency to start out
    #     quote_quantity = round(
    #         self.starting_quote_balance * config.USE_EQUITY, config.DECIMAL_PRECISION)
    #     self.buy_price = round(data.iat[0, 1], config.DECIMAL_PRECISION)
    #     self.buy_prices.append(self.buy_price)
    #     self.base_balance = starting_base_balance + \
    #         round(quote_quantity / self.buy_price,
    #               config.DECIMAL_PRECISION)  # ETH
    #     self.quote_balance = round(
    #         starting_quote_balance - quote_quantity, config.DECIMAL_PRECISION)  # BTC

    #     self.place_orders(symbol)

    #     for index, dataset in data.iterrows():
    #         # order of dataset:
    #         # 0: time millis, 1: Open, 2: High, 3: Low, 4: Close, 5: Volume
    #         # check for fill order
    #         if not self.buy_order == None and dataset[3] < self.buy_order.price:
    #             (self.base_balance, self.quote_balance, self.buy_prices) = self.buy_order.fill_order(
    #                 self.base_balance, self.quote_balance, self.buy_prices)

    #         if not self.sell_order == None and dataset[2] > self.sell_order.price:
    #             (self.base_balance, self.quote_balance, self.buy_prices) = self.sell_order.fill_order(
    #                 self.base_balance, self.quote_balance, self.buy_prices)

    #         # buy order filled
    #         if not self.buy_order == None and self.buy_order.filled:
    #             self.cancel_orders()
    #             self.place_orders(symbol)

    #         # sell order filled
    #         elif not self.sell_order == None and self.sell_order.filled:
    #             self.cancel_orders()

    #             self.buy_quantity = round(self.starting_quote_balance *
    #                                       config.USE_EQUITY, config.DECIMAL_PRECISION)  # in quote currency
    #             self.buy_price = round(
    #                 self.sell_price * (1 - .0001), config.DECIMAL_PRECISION)

    #             # if is affordable
    #             if self.quote_balance > self.buy_quantity:
    #                 self.buy_order = LimitOrder(
    #                     symbol, self.buy_quantity, self.buy_price, "buy")

    #         # adjust buy order price by setting a new one
    #         elif len(self.buy_prices) == 0:
    #             # nein -> buy order neu setzen für preis = open der neuen candle * (1 - 0.0001) und menge die wir anfangs bestimmt haben
    #             self.buy_quantity = round(self.starting_quote_balance *
    #                                       config.USE_EQUITY, config.DECIMAL_PRECISION)  # in quote currency
    #             self.buy_price = round(
    #                 dataset[1] * (1 - .0001), config.DECIMAL_PRECISION)

    #             # if is affordable
    #             if self.quote_balance > self.buy_quantity:
    #                 self.buy_order = LimitOrder(
    #                     symbol, self.buy_quantity, self.buy_price, "buy")

    #         time.sleep(.01)

    #     print("Final base balance:", self.base_balance, symbol.split("/")[0])
    #     print("Final quote balance:", self.quote_balance, symbol.split("/")[1])
    #     end_value = (self.base_balance *
    #                  data.iat[data.shape[0] - 1, 4]) + self.quote_balance
    #     print("End value:", end_value, symbol.split("/")[1])

    #     return end_value

    def start(self):
        # cancel open orders saved in DB
        self.account.cancel_open_orders()

        # get filled order history
        filled_orders = self.account.get_filled_orders()

        if filled_orders[-1]['side'] == 'sell':
            # buy small base
            pass
        elif filled_orders[-1]['side'] == 'buy':
            # calc avg price of x recently filled buy orders
            buys = []

            for order in reversed(filled_orders):
                if order['side'] == "buy":
                    buys.append(float(order['price']))

        while self.trading:
            open_orders = self.account.get_open_orders()
            break

            time.sleep(config.REFRESH_RATE)

    def cancel_orders(self):
        self.account.cancel_open_orders()

    def place_grid_orders(self):
        self.place_grid_buy_order()
        self.place_grid_sell_order()

    def place_grid_buy_order(self):
        last_price = float(self.account.get_last_filled_order()[3])
        self.buy_price = round(last_price *
                               (1 - config.STEP_DISTANCE), config.DECIMAL_PRECISION)  # in quote currency
        self.buy_quantity = round(self.quote_balance * config.USE_EQUITY /
                                  self.account.exchange.get_exchange_rate(), config.DECIMAL_PRECISION)  # in base currency

        # self.buy_order = LimitOrder(
        #     symbol, self.buy_quantity, self.buy_price, "buy")
        self.buy_id = self.account.create_order(
            "buy", self.buy_quantity, self.buy_price)['id']

    def place_grid_sell_order(self):
        self.sell_price = round((sum(self.buy_prices) / len(self.buy_prices)
                                 ) / (1 - config.TAKE_PROFIT), config.DECIMAL_PRECISION)  # in quote currency
        self.sell_quantity = round(self.account.read_balance(
            self.account.base_coin), config.DECIMAL_PRECISION)  # in base currency

        # self.sell_order = LimitOrder(
        #     symbol, self.sell_quantity, self.sell_price, "sell")
        self.sell_id = self.account.create_order(
            "sell", self.sell_quantity, self.sell_price)['id']
