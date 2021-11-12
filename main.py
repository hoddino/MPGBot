import sys
from datetime import datetime
from classes.Account import Account

import log
from classes.Exchange import Exchange
from classes.GridStrategy import *
from classes.Database import Database

if __name__ == '__main__':
    # check config parameters
    if config.EXCHANGE == '':
        log.error("Please specify an exchange market in config.py!")
        sys.exit(0)
    elif config.API_KEY == '':
        log.error("Please specify an API key in config.py!")
        sys.exit(0)
    elif config.API_SECRET == '':
        log.error("Please specify an API secret in config.py!")
        sys.exit(0)
    elif not config.ORDER_TYPE in ['limit', 'market']:
        log.error("Please specify a valid order type in config.py!")
        sys.exit(0)

    exchange = Exchange()
    database = Database()
    account = Account(exchange, database)

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
    while quote_balance == None and quote_balance <= 0:
        log.error("No capital available! Please top up your account.")
        # print(config.PREFIX_ERROR,
        #       "No capital available! Please top up your account.")
        time.sleep(60 * 60 * 3)  # 3 hours
        account.update_balance()

        # read balance from exchange
        base_balance = account.read_balance(base_coin)

        # read balance from exchange
        quote_balance = account.read_balance(quote_coin)


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


    strategy = GridStrategy(account)
    strategy.start()
