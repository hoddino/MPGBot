# Exchange settings
EXCHANGE = 'ftx'  # ccxt exchange name
API_KEY = ''
API_SECRET = ''
REFRESH_RATE = 0.5  # in seconds
QUICK_BUY_RATE = 60  # in seconds
ORDER_TYPE = 'limit'  # limit or market order

SYMBOL = 'BTC/EUR'  # market to trade in

# Strategy settings
USE_EQUITY = 0.1  # percentage to use
STEP_DISTANCE = 0.005  # percentage
TAKE_PROFIT = 0.0075  # percentage

# General settings
DECIMAL_PRECISION = 7  # amount of decimals to round values
PREFIX_ERROR = '[ERROR]'
PREFIX_INFO = '[INFO]'
PREFIX_WARNING = '[WARN]'
