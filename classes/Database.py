import sqlite3
import log
from datetime import datetime


class Database:
    def __init__(self):
        self.name = 'mpgbot.db'

        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Orders (\
            id INTEGER,\
            type VARCHAR(16),\
            side VARCHAR(5),\
            price REAL,\
            quantity REAL,\
            status VARCHAR(10),\
            timestamp INTEGER,\
            PRIMARY KEY (id)\
        )")
        cursor.execute("CREATE TABLE IF NOT EXISTS Profits (\
            id INTEGER,\
            value REAL,\
            timestamp TIMESTAMP,\
            PRIMARY KEY (id)\
        )")
        connection.commit()
        cursor.close()
        connection.close()

    def __str__(self):
        return "{name:" + self.name + "}"

    def save_order(self, order):
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Orders VALUES (%s, '%s', '%s', %s, %s, '%s', %s)" % (
            order['id'], order['type'], order['side'], order['price'], order['amount'], order['status'], order['timestamp']))
        connection.commit()
        cursor.close()
        connection.close()

    def save_profit(self, profit):
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Profits VALUES(value, timestamp) (?, ?)" % (
            profit, datetime.now()))
        connection.commit()
        cursor.close()
        connection.close()

    def update_order_status(self, order):
        # switch status names
        status = order['status']
        if status == 'closed':
            status = 'filled'

        # only update when value has changed
        order_db = self.read_order_by_id(order['id'])
        if not order_db == None and not status == order_db[5]:
            connection = sqlite3.connect(self.name)
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE Orders SET status='%s' WHERE id=%s" % (status, order['id']))
            connection.commit()
            cursor.close()
            connection.close()

            # info message
            log.info("Order id " + order['id'] +
                     " changed status to: " + status)

    def read_orders(self):
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM Orders ORDER BY timestamp DESC LIMIT 300")
        orders = cursor.fetchall()
        cursor.close()
        connection.close()

        return orders

    def read_order_by_id(self, id):
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Orders WHERE id=%s" % id)
        order = cursor.fetchone()
        cursor.close()
        connection.close()
        return order

    def clear_orders(self, ids=[]):
        if len(ids) <= 0:
            connection = sqlite3.connect(self.name)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Orders")
            cursor.close()
            connection.close()
        else:
            for id in ids:
                self.clear_order(id)

    def clear_order(self, id):
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Orders WHERE id=%s" % id)
        connection.commit()
        cursor.close()
        connection.close()
