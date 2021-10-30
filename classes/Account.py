class Account:
    def __init__(self, exchange):
        self.exchange = exchange
        self.update_balance()

    def update_balance(self):
        self.balance = self.exchange.read_balance()

    def read_balance(self, coin):
        try:
            return self.balance[coin]['free']
        except KeyError:
            return None
