import sqlite3
import log


class Database:
    def __init__(self):
        self.name = 'mpgbot.db'
        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Orders (\
            id INT,\
            type VARCHAR(16),\
            side VARCHAR(5),\
            price REAL,\
            quantity REAL,\
            status VARCHAR(10),\
            timestamp INT,\
            PRIMARY KEY (id)\
        )")
        self.connection.commit()
        # cursor.close()

    def __str__(self):
        return "{name:" + self.name + "}"

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        self.connection = None

    def save_order(self, order):
        # cursor = self.connection.cursor()
        self.cursor.execute("INSERT INTO Orders VALUES (%s, '%s', '%s', %s, %s, '%s', %s)" % (
            order['id'], order['type'], order['side'], order['price'], order['amount'], order['status'], order['timestamp']))
        self.connection.commit()
        # cursor.close()

    def update_order_status(self, order):
        # switch status names
        status = order['status']
        if status == 'closed':
            status = 'filled'

        # only update when value has changed
        order_db = self.read_order_by_id(order['id'])
        if not order_db == None and not status == order_db[5]:
            self.cursor.execute(
                "UPDATE Orders SET status='%s' WHERE id=%s" % (status, order['id']))
            self.connection.commit()

            # info message
            log.info("Order id " + order['id'] +
                     " changed status to: " + status)

    def read_orders(self):
        # cursor = self.connection.cursor()
        self.cursor.execute(
            "SELECT * FROM Orders ORDER BY timestamp DESC LIMIT 300")
        orders = self.cursor.fetchall()
        # cursor.close()

        return orders

    def read_order_by_id(self, id):
        self.cursor.execute("SELECT * FROM Orders WHERE id=%s" % id)
        return self.cursor.fetchone()

    def clear_orders(self, ids=[]):
        # cursor = self.connection.cursor()
        if len(ids) <= 0:
            self.cursor.execute("DELETE FROM Orders")
        else:
            for id in ids:
                self.clear_order(id)

        # self.connection.commit()
        # cursor.close()

    def clear_order(self, id):
        self.cursor.execute("DELETE FROM Orders WHERE id=%s" % id)
        self.connection.commit()
