import pandas as pd
import time
from classes.LimitOrder import LimitOrder

import config


class GridStrategy:
    def __init__(self, account):
        self.buy_order = None
        self.sell_order = None
        self.base_balance = 0
        self.quote_balance = 0
        self.buy_prices = []
        self.simulate = True
        self.account = account

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
        while self.simulate:
            open_orders = self.account.get_open_orders()

    def cancel_orders(self):
        if not self.buy_order == None:
            self.buy_order.cancel_order()
        if not self.sell_order == None:
            self.sell_order.cancel_order()

        self.buy_order = None
        self.sell_order = None

    def place_orders(self, symbol):
        self.place_buy_order(symbol)
        self.place_sell_order(symbol)

    def place_buy_order(self, symbol):
        self.buy_price = round(self.buy_price *
                               (1 - config.STEP_DISTANCE), config.DECIMAL_PRECISION)
        self.buy_quantity = round(self.starting_quote_balance *
                                  config.USE_EQUITY, config.DECIMAL_PRECISION)  # in quote currency

        # if is affordable
        if self.quote_balance > self.buy_quantity:
            self.buy_order = LimitOrder(
                symbol, self.buy_quantity, self.buy_price, "buy")

    def place_sell_order(self, symbol):
        self.sell_price = round((sum(self.buy_prices) / len(self.buy_prices)
                                 ) / (1 - config.TAKE_PROFIT), config.DECIMAL_PRECISION)
        self.sell_quantity = round(self.sell_price *
                                   self.base_balance, config.DECIMAL_PRECISION)  # calc into quote currency

        self.sell_order = LimitOrder(
            symbol, self.sell_quantity, self.sell_price, "sell")
