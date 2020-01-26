from conf.database import Connection
from pandas_datareader import data as wb
from datetime import datetime, timedelta
from time import sleep

class GetLastPrice(Connection):

    @staticmethod
    def check_ticket(ticket):
        today = datetime.now()
        today = datetime.strftime(today, '%Y-%m-%d')
        yesterday = datetime.now() - timedelta(days=1)
        yesterday = yesterday.strftime('%Y-%m-%d')
        try:
            preco_fechamento = wb.DataReader(ticket + '.SA', data_source='yahoo', start=today)['Adj Close']
        except:
            preco_fechamento = wb.DataReader(ticket + '.SA', data_source='yahoo', start=yesterday)['Adj Close']
        price = str(preco_fechamento[0])
        return price

    def insert(self, ticket, price):
        sql = 'insert into price_last_day(ticket,preco) values(%s, %s)'

        cur = self._db.cursor()
        cur.execute(sql, (ticket, price,))
        self._db.commit()

    def drop_table(self):
        cur = self._db.cursor()
        sql = 'drop table if exists price_last_day'
        cur.execute(sql)
        self._db.commit()

    def create_table(self):
        cur = self._db.cursor()
        sql = '''create table price_last_day(
                            id serial primary key,
                            ticket varchar(20),
                            preco NUMERIC (4, 2)
                        )'''
        cur.execute(sql)
        self._db.commit()

    def last_price_tickets(self, new_ticket=None):
        last_prices = {}

        if new_ticket:
            price = self.check_ticket(new_ticket)
            last_prices[new_ticket] = price[:5]
            for ticket, price in last_prices.items():
                self.insert(ticket, price)
            self.close()
        else:
            self.drop_table()
            self.create_table()
            cur = self._db.cursor()
            sql = 'select distinct on (ticket) ticket from alerts'
            cur.execute(sql)
            data = cur.fetchall()
            tickets = []
            for i in data:
                tickets.append(i[0])
            for ticket in tickets:
                price = self.check_ticket(ticket)
                last_prices[ticket] = price[:5]
            for ticket, price in last_prices.items():
                self.insert(ticket, price)
            self.close()
            sleep(60)


if __name__ == "__main__":

    a = GetLastPrice()
    a.last_price_tickets()
