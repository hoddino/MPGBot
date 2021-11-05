import log


class Account:
    def __init__(self, exchange, database):
        self.exchange = exchange
        self.db = database
        self.base_coin = exchange.base_coin
        self.quote_coin = exchange.quote_coin
        self.update_balance()

    def update_balance(self):
        self.balance = self.exchange.read_balance()

    def read_balance(self, coin):
        self.update_balance()
        try:
            return self.balance[coin]['free']
        except KeyError:
            return None

    def get_open_orders(self):
        orders = self.db.read_orders()
        open_orders = []

        # get open orders from all orders
        for order in orders:
            if order[5] == 'open':
                open_orders.append(order)

        return open_orders

    def get_last_filled_order(self):
        orders = self.db.read_orders()

        for order in reversed(orders):
            if order[5] == 'filled':
                return order

        return None

    def get_filled_orders(self):
        # from exchange
        orders = self.exchange.get_order_history()

        # only take closed/filled orders
        filled_orders = []
        for order in orders:
            if order['status'] == 'closed':
                filled_orders.append(order)

        return filled_orders

    def create_order(self, side, quantity, price):
        # quantity in base currency
        # price in quote currency
        order = self.exchange.create_order(side, quantity, price)
        # print(str(order))

        # save order details to db
        self.db.save_order(order)

        # print log msg
        log.info(
            f"{side} order has been placed! {quantity} {self.base_coin} @ {price} {self.quote_coin}")

        return order

    def cancel_open_orders(self):
        order_ids = []

        # concat ids
        for order in self.get_open_orders():
            order_ids.append(order[0])
        # print(order_ids)

        if len(order_ids) > 0:
            # if self.exchange.cancel_orders(order_ids):
            #     self.db.clear_orders(order_ids)
            for id in order_ids:
                self.exchange.cancel_order(id)
                self.db.clear_order(id)
