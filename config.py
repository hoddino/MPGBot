# Exchange settings
EXCHANGE = 'ftx'  # ccxt exchange name
SUBACCOUNT = ''  # name of subaccount, i.e. 'Martin'
API_KEY = ''
API_SECRET = ''
REFRESH_RATE = 0.5  # in seconds
QUICK_BUY_RATE = 60  # in seconds
ORDER_TYPE = 'limit'  # limit or market order

SYMBOL = 'ETH/BTC'  # market to trade in

# Strategy settings
USE_EQUITY = 0.01  # percentage to use
STEP_DISTANCE = 0.0005  # percentage
TAKE_PROFIT = 0.001  # percentage

# General settings
DAILY_RESTART_ENABLED = True
DAILY_RESTART_TIME = '00:30'
DECIMAL_PRECISION = 6  # amount of decimals to round values
PREFIX_ERROR = '[ERROR]'
PREFIX_WARNING = '[WARN]'
PREFIX_INFO = '[INFO]'
PREFIX_BUY = '[BUY]'
PREFIX_SELL = '[SELL]'
