from conf.database import Connection
import json
import requests
from conf.settings import HGBRASIL
from datetime import datetime

from app import pubsub
from app.last_verify import LastVerify
# from core import notify_up, notify_down

class CurrentPrice(Connection):

    def __init__(self):
        super().__init__()
        self.alerts = self.__dict__
        self.last_price = self.__dict__

    @staticmethod
    def data_api(ticket):

        url = 'https://api.hgbrasil.com/finance/stock_price?key={}&symbol={}'.format(HGBRASIL, ticket)
        r = requests.get(url).text
        data = json.loads(r)
        data = data["results"][ticket]
        return data["price"]



    @staticmethod
    def calculator_price(percent, last_price, price, type_check):

        different_value = (last_price / 100) * percent

        if type_check == 'up':


            expected_price = last_price + different_value

            if price >= expected_price:
                return True
            else:
                return False
        elif type_check == 'down':

            expected_price = last_price - different_value

            if price <= expected_price:
                return True
            else:
                return False
        else:
            return False

    def verify(self):

        for ticket, value in self.alerts.items():
            last_price = self.last_price[ticket]
            last_verify = LastVerify()
            if last_verify.get(ticket, value[2]):
                price = CurrentPrice.data_api(ticket)
                if CurrentPrice.calculator_price(value[1], last_price[0], price, type_check='up'):
                    pubsub.publish('alerts', [value[2], f"{ticket} subiu {value[1]}%ou mais"])
                    last_verify.insert(ticket, value[2])
                elif CurrentPrice.calculator_price(value[1], last_price[0], price, type_check='down'):
                    pubsub.publish('alerts', [value[2], f"{ticket} caiu {value[1]}% ou mais"])
                    last_verify.insert(ticket, value[2])

    def get_last_price(self):
        last_prices = {}

        sql = 'select ticket, preco from price_last_day'
        cur = self._db.cursor()
        cur.execute(sql, )
        data = cur.fetchall()

        for i in data:
            ticket = str(i[0])
            price = float(i[1])

            last_prices[ticket] = [price]
        return last_prices

    def get_alerts(self):

        sql = 'select ticket, up_percent, down_percent, user_id from alerts'

        cur = self._db.cursor()
        cur.execute(sql,)
        data = cur.fetchall()
        alerts = {}
        for i in data:
            ticket = str(i[0])
            down_percent = float(i[1])
            up_percent = float(i[2])
            user_id = str(i[3])
            alerts[ticket] = [down_percent, up_percent, user_id]
        return alerts


if __name__ == "__main__":
    now = datetime.now()
    print(now.hour)

    while True:
        if now.hour > 9 and now.hour < 17:
            current_price = CurrentPrice()
            current_price.alerts = current_price.get_alerts()
            current_price.last_price = current_price.get_last_price()
            current_price.verify()
