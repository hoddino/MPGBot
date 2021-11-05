import sys
from datetime import datetime
from classes.Account import Account

import log
from classes.Exchange import Exchange
from classes.GridStrategy import *
from classes.Database import Database

if __name__ == '__main__':
    exchange = Exchange()
    database = Database()
    account = Account(exchange, database)

    # using:
    #

    # read symbol
    symbol = config.SYMBOL
    base_coin = symbol.split('/')[0]
    quote_coin = symbol.split('/')[1]

    # load current exchange rate
    exchange_rate = exchange.get_exchange_rate()

    # read balance from exchange
    base_balance = account.read_balance(base_coin)

    # read balance from exchange
    quote_balance = account.read_balance(quote_coin)

    # abort if no money
    while quote_balance <= 0:
        log.error("No capital available! Please top up your account.")
        # print(config.PREFIX_ERROR,
        #       "No capital available! Please top up your account.")
        time.sleep(60 * 60 * 3)  # 3 hours
        account.update_balance()

        # read balance from exchange
        base_balance = account.read_balance(base_coin)

        # read balance from exchange
        quote_balance = account.read_balance(quote_coin)

    # buy = account.create_order("buy", .0001, 52800)['id']
    # print(buy)
    # order = account.get_last_filled_order()
    # print(order)
    # database.save_order(order)
    # database.read_orders()
    # time.sleep(5)
    # account.cancel_open_orders()
    # print(database.read_orders())

    log.info("Setup complete!")
    log.info("")
    log.info("Exchange:      " + exchange.exchange.id)
    log.info("Market:        " + symbol)
    log.info("Base balance:  " + str(base_balance) + " " + base_coin)
    log.info("Quote balance: " + str(quote_balance) + " " + quote_coin)
    log.info("Use equity:    " + str(config.USE_EQUITY))
    log.info("Step distance: " + str(config.STEP_DISTANCE))
    log.info("Take profit:   " + str(config.TAKE_PROFIT))
    log.info("")
    log.info("Current exchange rate: " + str(exchange_rate))
    starting_value = base_balance * exchange_rate + quote_balance
    log.info("Starting value: " + str(starting_value) + " " + quote_coin)
    log.info("")

    # while True:
    #     text = input("Would you like to start the simulation now? (y/n) ")
    #     if text in ["y", "yes"]:
    #         # successful, sim may start
    #         break
    #     elif text in ["n", "no"]:
    #         # abort, shut down
    #         log.info("Simulation aborted! kthxbye")
    #         sys.exit(0)
    #     else:
    #         log.warn("Invalid input, please try again...")

    # start the simulation
    # grid_strategy = GridStrategy()
    # end_value = grid_strategy.start(exchange.historical_data, symbol,
    #                                 base_balance, quote_balance)
    # percent = (end_value / starting_value - 1) * 100
    # log.info("Change: %.3f%%" % percent)

    account.get_filled_orders()
