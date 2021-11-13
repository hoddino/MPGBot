import log
import ccxt


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
            return 0

    def get_order_by_id(self, id):
        order = self.db.read_order_by_id(id)
        if order == None:
            return None
        else:
            return {
                "id": int(order[0]),
                "type": order[1],
                "side": order[2],
                "price": float(order[3]),
                "quantity": float(order[4]),
                "status": order[5],
                "timestamp": order[6]
            }

    def get_last_open_order(self):
        orders = self.db.read_orders()

        # get most recent open order
        for order in orders:
            if order[5] == 'open':
                return order

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

        for order in list(orders):
            if order[5] == 'filled':
                return order

        return None

    def get_filled_exchange_orders(self):
        # from exchange
        orders = self.exchange.get_order_history()

        # only take closed/filled orders
        filled_orders = []
        for order in orders:
            if order['status'] == 'closed':
                filled_orders.append(order)

        return filled_orders

    def get_filled_orders(self):
        # from database
        orders = self.db.read_orders()

        # only take closed/filled orders
        filled_orders = []
        for order in orders:
            if order[5] == 'filled':
                filled_orders.append({
                                "id": int(order[0]),
                                "type": order[1],
                                "side": order[2],
                                "price": float(order[3]),
                                "quantity": float(order[4]),
                                "status": order[5],
                                "timestamp": order[6]
                            })

        return filled_orders

    def create_order(self, side, quantity, price):
        success = True
        # check order quantity
        compare_market = self.quote_coin + "/USD"
        if self.exchange.market_exists(compare_market):
            # order quantity must be >10 USD
            quantity_usd = self.exchange.get_exchange_rate(compare_market) * quantity
            if quantity_usd < 10:
                log.error("Order size is below 10 USD. Please top up your account or change USE_EQUITY in config.")
        else:
            log.warn("Order size could not be validated over 10 USD!")

        # quantity in base currency
        # price in quote currency
        try:
            order = self.exchange.create_order(side, quantity, price)
        except ccxt.RequestTimeout as exc:
            log.warn("Order creation has timed out!")
            return
        except ccxt.InvalidOrder as exc:
            log.error("Order size too small: " + str(exc))
        except Exception as exc:
            log.error("Unexpected exception thrown! " + str(exc))

        # save order details to db
        self.db.save_order(order)

        # print log msg
        log.info(f"{str(side).capitalize()} order id {order['id']} has been placed! {quantity} {self.base_coin} @ {price} {self.quote_coin}")

        return order

    def cancel_open_orders(self):
        order_ids = []

        # concat ids
        for order in self.get_open_orders():
            order_ids.append(order[0])
        # print(order_ids)

        if len(order_ids) > 0:
            for id in order_ids:
                # self.exchange.cancel_order(id)
                # self.db.clear_order(id)
                self.cancel_order(id)

    def cancel_order(self, id):
        self.exchange.cancel_order(id)
        self.db.clear_order(id)
        log.info(f"Order id {id} canceled")

    def update_all_orders_status(self):
        orders = self.exchange.get_order_history()
        for order in orders:
            self.db.update_order_status(order)

    def save_profit(self, profit):
        self.db.save_profit(profit)
