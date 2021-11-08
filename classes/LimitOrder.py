import config


class LimitOrder:
    def __init__(self, exchange, symbol, quantity, price, type):
        order_types = ["buy", "sell"]
        if not type in order_types:
            raise ValueError(
                "Limit Order type can only be one of %r" % order_types)

        self.symbol = symbol  # market, i.e. ETH/BTC
        self.quantity = quantity  # in quote currency
        self.price = price  # in quote/(1 base)
        self.type = type  # sell or buy limit order
        self.filled = False  # order fill status

    def __str__(self) -> str:
        return "{symbol:" + self.symbol + ", quantity:" + str(self.quantity) + ", price:" + str(self.price) + ", type:" + self.type + ", filled:" + str(self.filled) + "}"

    def fill_order(self):
        self.filled = True

        # if self.type == "buy":
        #     base_balance += round(self.quantity / self.price,
        #                           config.DECIMAL_PRECISION)
        #     quote_balance -= self.quantity
        #     buy_prices.append(self.price)

        #     if quote_balance < 0:
        #         raise ValueError("Insufficient quote balance:", quote_balance)
        # elif self.type == "sell":
        #     # base_balance -= round(self.quantity / self.price,
        #     #                       config.DECIMAL_PRECISION)
        #     base_balance = 0
        #     quote_balance += self.quantity
        #     buy_prices.clear()

        #     if base_balance < 0:
        #         raise ValueError("Insufficient base balance:", base_balance)

        # return (base_balance, quote_balance, buy_prices)

    def cancel_order(self):
        pass
