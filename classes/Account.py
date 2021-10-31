import config


class Account:
    def __init__(self, exchange, database):
        self.exchange = exchange
        self.db = database
        self.update_balance()

    def update_balance(self):
        self.balance = self.exchange.read_balance()

    def read_balance(self, coin):
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

    def create_order(self, side, quantity, price):
        # quantity in base currency
        # price in quote currency
        order = self.exchange.create_order(side, quantity, price)
        print(str(order))

        # save order details to db
        self.db.save_order(order)

        return order

    def cancel_open_orders(self):
        order_ids = []

        # concat ids
        # for order in self.get_open_orders():
        #     order_ids.append(order['id'])
        map(lambda order: order_ids.append(
            order['id']), self.get_open_orders())
        print(order_ids)

        if len(order_ids) > 0:
            if self.exchange.cancel_orders(order_ids):
                self.db.clear_orders(order_ids)
