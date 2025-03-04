# import pandas as pd
import time
import threading

import config
import log


class GridStrategy(threading.Thread):
    def __init__(self, account):
        threading.Thread.__init__(self)
        self.account = account
        self.buy_id = 0
        self.sell_id = 0
        self.buy_prices = []
        self.trading = True
        coins = config.SYMBOL.split("/")
        self.base_coin = coins[0]
        self.quote_coin = coins[1]
        self.quote_balance = self.account.read_balance(self.quote_coin)
        self.buy_price = 0
        self.buy_quantity = 0
        self.sell_price = 0
        self.sell_quantity = 0
        self.quick_order_set = None
        self.update_quote_balance()

    def run(self):
        # synchronize database and exchange history
        self.account.sync_db_to_exchange()
        # cancel open orders saved in DB
        self.cancel_orders()
        # calculate buy_quantity (amount) in quote currency
        self.buy_quantity = self.quote_balance * config.USE_EQUITY
        # get filled order history
        filled_orders = self.account.get_filled_exchange_orders()
        # no order history -> start quick buy
        if len(filled_orders) == 0:
            self.place_quick_buy_order()
        # last order was sell order -> start quick buy
        elif filled_orders[-1]['side'] == 'sell':
            self.place_quick_buy_order()
        # calc avg price of recently filled buy orders until last sell and then start setting buy and sell orders
        elif filled_orders[-1]['side'] == 'buy':
            for order in list(reversed(filled_orders)):
                if order['side'] == "buy":
                    self.buy_prices.append(float(order['price']))
                elif order['side'] == "sell":
                    break
            self.buy_price = sum(self.buy_prices) / len(self.buy_prices)
            self.place_grid_orders()

        # start trading
        while self.trading:
            try:
                self.update_quote_balance()
                self.update_quick_buy_order()

                # wait for quick buy order
                while not self.quick_order_set == None and self.quick_order_set['status'] == 'open':
                    self.account.cancel_order(self.quick_order_set['id'])
                    self.place_quick_buy_order()
                    log.info("New quick buy order has been placed")

                    time.sleep(config.QUICK_BUY_RATE)
                    self.update_quick_buy_order()

                buy_order = self.account.get_order_by_id(self.buy_id)
                sell_order = self.account.get_order_by_id(self.sell_id)

                # check if order filled
                if buy_order['status'] == 'filled':
                    self.cancel_orders()
                    # append buy price list
                    self.buy_prices.append(buy_order['price'])
                    # buy log message "BUY order of (quantity) at (price) got FILLED."
                    log.buy(
                        f"Order of {round(buy_order['quantity'], config.DECIMAL_PRECISION)} {self.base_coin} at {round(buy_order['price'], config.DECIMAL_PRECISION)} {self.quote_coin} got FILLED.")
                    # place new grid orders
                    self.place_grid_orders()

                elif sell_order['status'] == 'filled':
                    self.cancel_orders()
                    # recalculate buy_quantity (amount) in quote currency
                    self.buy_quantity = self.quote_balance * config.USE_EQUITY
                    # reset buy price list
                    self.buy_prices = []
                    # calculate profit
                    buy_sum = 0
                    for order in self.account.get_filled_orders()[1:]:
                        # stop when sell order
                        if order['type'] == 'sell':
                            break
                        # add buy orders together
                        if order['status'] == 'filled' and order['type'] == 'buy':
                            # value in quote currency
                            buy_sum += order['price'] * order['quantity']
                    profit = sell_order['price'] * \
                        sell_order['quantity'] - buy_sum
                    # sell log message "SELL order of (quantity) at (price) got FILLED.   [Profit: BTC]"
                    log.sell(
                        f"Order of {round(sell_order['quantity'], config.DECIMAL_PRECISION)} {self.base_coin} at {round(sell_order['price'], config.DECIMAL_PRECISION)} {self.quote_coin} got FILLED.         [Profit: {round(profit, config.DECIMAL_PRECISION)} {self.quote_coin}]")
                    # save profit to Database
                    self.account.save_profit(profit)
                    # make quick buy to have a new base balance
                    self.place_quick_buy_order()

            except Exception as exc:
                log.warn(
                    f"Following exception occured but we ignored it succesfully: {str(exc)}")

            time.sleep(config.REFRESH_RATE)

    def update_quote_balance(self):
        self.quote_balance = self.account.read_balance(self.quote_coin)

    def cancel_orders(self):
        self.account.cancel_open_orders()

    def update_quick_buy_order(self):
        self.account.update_all_orders_status()
        if not self.quick_order_set == None:
            self.quick_order_set['status'] = self.account.get_order_by_id(
                self.quick_order_set['id'])['status']

    def place_quick_buy_order(self):
        # get current price -0.001% (basically buy immediately)
        self.buy_price = float(
            self.account.exchange.get_exchange_rate() * (1 - 0.00001))
        buy_amount = self.buy_quantity / \
            self.account.exchange.get_exchange_rate()  # in base currency
        # creat order
        self.quick_order_set = self.account.create_order(
            "buy", buy_amount, self.buy_price)
        # save order id
        self.buy_id = self.quick_order_set['id']

    def place_grid_orders(self):
        self.place_grid_buy_order()
        self.place_grid_sell_order()

    def place_grid_buy_order(self):
        # get last filled order
        last_filled = self.account.get_last_filled_order()
        if last_filled == None:
            log.error("Could not find a filled order in database.")
        last_price = float(last_filled[3])
        self.buy_price = last_price * \
            (1 - config.STEP_DISTANCE)  # in quote currency
        # calculate amount to base currency
        buy_amount = self.buy_quantity / \
            self.account.exchange.get_exchange_rate()  # in base currency
        # create order
        self.buy_id = self.account.create_order(
            "buy", buy_amount, self.buy_price)['id']
        # confirm quick buy order is not active
        self.quick_order_set = None

    def place_grid_sell_order(self):
        # calculate average oder price
        self.sell_price = (sum(self.buy_prices) / len(self.buy_prices)) / \
            (1 - config.TAKE_PROFIT)  # in quote currency
        # get base balance to sell
        self.sell_quantity = self.account.read_balance(
            self.account.base_coin)  # in base currency
        # create order and save order id
        self.sell_id = self.account.create_order(
            "sell", self.sell_quantity, self.sell_price)['id']
